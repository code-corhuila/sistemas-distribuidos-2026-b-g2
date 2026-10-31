# CP8 · Runbook: CatalogSearchFastBurn

> Page. More than 1.44 % of `GET /api/v1/propiedades` failed in the last hour **and**
> in the last 5 minutes. Guests cannot find properties, so they cannot book.

## Symptoms

- The Catalog portal (`:4201`) shows the error message instead of the cards.
- The gateway answers `500 INTERNAL_ERROR` on `/api/v1/propiedades`.
- Logs of `catalog-service` with `"event":"mongo.find.failed"` or `"mongo.update.timeout"`.

## Confirm it

1. How bad, by outcome:
   ```promql
   sum by (outcome) (rate(catalog_search_requests_total[5m]))
   ```
2. Is it Mongo?
   ```promql
   histogram_quantile(0.95, sum by (le, operation) (rate(catalog_mongo_operation_duration_seconds_bucket[5m])))
   sum by (reason) (rate(catalog_mongo_operation_errors_total[5m]))
   ```
3. Follow one failed search end to end with its `trace_id`:
   ```bash
   docker compose logs --since 10m catalog-service | grep '"level":"ERROR"'
   docker compose logs --since 10m | grep '"trace_id":"<trace_id>"'
   ```
   The `traceparent` is also in the `comment` of the Mongo query, so the slow query in
   the Mongo log (`db.system.profile` or the slow-query log) can be matched to the trace.
4. Check the plan of the query:
   `db.properties.find({city: "neiva", capacity: {$gte: 2}}).explain("executionStats")` —
   `COLLSCAN` instead of `IXSCAN` means the index `idx_properties_city_capacity` is gone.

## Mitigations (lowest risk first)

1. **Feature flag: search without the date filter.** Set `CATALOG_DATE_FILTER_ENABLED=false`
   and restart `catalog-service`. The query skips `unavailableRanges` and becomes cheaper.
   Risk: a guest may see a property whose dates are taken; Booking still rejects it with
   `422` (INV-001), so no double booking is possible.
2. **Repair the indexes, or roll back.** If `explain` shows `COLLSCAN`, re-create the
   indexes with the script of `property-catalog-db` (`createIndexes` works online). If a
   release of `catalog-service` came just before, put the previous tag in the compose
   file and `docker compose up -d catalog-service`.
3. **Scale out.** `catalog-service` keeps no state, so
   `docker compose up -d --scale catalog-service=2` is safe. It does not help if MongoDB
   itself is the bottleneck.

## Escalation

- **On-call of the week** — confirms and applies mitigation 1 (first 10 minutes).
- **Catalog owner** — decides index repair or rollback (after 15 minutes).
- **Whole team + teacher** — if the search is still failing after 30 minutes, or if
  MongoDB itself is down (data at risk).

## Recovery is verified when

- `sum(rate(catalog_search_requests_total{outcome="error"}[5m]))` is 0 for 15 minutes
  and the alert resolves.
- A search for `neiva` with dates in `qa` returns cards and its trace shows a fast
  `mongo find properties` span.
- The flag of mitigation 1 is set back to `true`, and `CatalogAvailabilityStale` stays
  quiet (the consumer caught up).
