# CP6 · SLOs for the property search

Journey of CP1: `GET /api/v1/propiedades` (E-05) on `catalog-service`, and the
availability kept fresh by the consumer of Booking events. Metrics of CP4:
`catalog_search_requests_total{outcome}`, `catalog_search_duration_seconds`,
`catalog_event_lag_seconds`.

## How much traffic

A guest searches many times before booking: changes the city, the dates, the number
of guests. We count about **10 searches per booking attempt**. With about 200 booking
attempts a day (team estimate), that is **2,000 searches a day = 60,000 per 30 days**.
Booking publishes about 2 events per attempt (`ReservaCreada` plus `ReservaConfirmada`,
`ReservaCancelada` or `ReservaExpirada`): **12,000 events per 30 days**.
Window for every SLO: **30 days = 43,200 minutes**.

## SLO A — the search answers

SLI = searches that did not fail on our side / valid searches. A `400 VALIDATION_ERROR`
(for example `huespedes=30`) is the guest's mistake and is left out of the valid ones.

```promql
1 - (
  sum(increase(catalog_search_requests_total{outcome="error"}[30d]))
  /
  sum(increase(catalog_search_requests_total{outcome!="invalid"}[30d]))
)
```

Target **99.9 %**. It is a read on one collection with an index, and without search
nobody can book, so it should be higher than the Saga's 99.5 %.
Budget: 0.1 % × 60,000 = **60 failed searches**; 0.1 % × 43,200 = **43.2 minutes**.

## SLO B — the search is fast

SLI = searches answered in 250 ms or less / all searches. 250 ms is the bucket closest
under the 300 ms goal of CP4; the portal shows the cards with no visible wait.

```promql
sum(increase(catalog_search_duration_seconds_bucket{le="0.25"}[30d]))
/
sum(increase(catalog_search_duration_seconds_count[30d]))
```

Target **95 %**. Budget: 5 % × 60,000 = **3,000 slow searches**; 5 % × 43,200 =
**2,160 minutes**.

## SLO C — availability is fresh (our extra SLO)

Catalog is eventually consistent on purpose. What hurts the guest is a property shown
as free long after Booking took the dates: she picks it and gets `422` (INV-001).

SLI = events applied to `unavailableRanges` within 60 s of `occurredAt` / all events.

```promql
sum(increase(catalog_event_lag_seconds_bucket{le="60.0"}[30d]))
/
sum(increase(catalog_event_lag_seconds_count[30d]))
```

Target **99 %**. Budget: 1 % × 12,000 = **120 late events**; 1 % × 43,200 =
**432 minutes**.

## Summary

| SLO | Target | Budget in requests | Budget in minutes |
|---|---|---|---|
| A — search answers | 99.9 % | 60 searches | 43.2 |
| B — search ≤ 250 ms | 95 % | 3,000 searches | 2,160 |
| C — availability fresh ≤ 60 s | 99 % | 120 events | 432 |

## Error budget policy of the team

- **50 % used:** say it in the team chat; check the last releases of
  `property-catalog-portal`, `catalog-service` and the seed of `property-catalog-db`.
- **75 % used:** no new features in Catalog; only fixes and small changes go to `main`,
  each one with its rollback written in the PR.
- **100 % used:** freeze Catalog until the 30-day window is green again. The next sprint
  starts with the postmortem stories. If it is SLO C, Booking and Catalog owners review
  the outbox relay and the consumer together.
