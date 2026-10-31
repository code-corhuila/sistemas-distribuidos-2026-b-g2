# CP9 · Incident drill: MongoDB slow under the search

**Drill.** The hop marked in CP1 is hop 3: `catalog-service` → MongoDB (`find` on
`properties`). For 40 minutes, MongoDB answers in **3 seconds for 25 % of the
searches**. `catalog-service` gives up on a Mongo call after **2 s** (driver
`socketTimeoutMS`), so those searches end in `500 INTERNAL_ERROR`.

Traffic: a Saturday afternoon peak of **300 searches per hour** (the CP6 average is about
80). 40 minutes → **200 searches**, of which **50 fail**.

## One failed request: span tree

`trace_id 6d2e8f1a4b7c40d9e3f5a6b7c8d9e0f1` — total 2,047 ms, answer `500`.

```
GET /api/v1/propiedades?ciudad=Neiva&huespedes=2   api-gateway        2,047 ms
└─ GET /api/v1/propiedades                         catalog-service    2,031 ms
   ├─ parse and validate filters                   catalog-service        1 ms
   └─ mongo find properties (comment=traceparent)  catalog-service    2,002 ms  ✗ timeout
```

## Four log lines of that trace

```json
{"timestamp":"2026-10-24T14:23:41.108Z","level":"INFO","service":"api-gateway","version":"2.0.0","environment":"main","trace_id":"6d2e8f1a4b7c40d9e3f5a6b7c8d9e0f1","span_id":"a1b2c3d4e5f60718","correlation_id":"corr-9c1d","event":"http.request.received","message":"GET /api/v1/propiedades routed to catalog-api:3002"}
{"timestamp":"2026-10-24T14:23:41.124Z","level":"INFO","service":"catalog-service","version":"2.0.0","environment":"main","trace_id":"6d2e8f1a4b7c40d9e3f5a6b7c8d9e0f1","span_id":"b2c3d4e5f6071829","correlation_id":"corr-9c1d","event":"catalog.search.started","message":"search with 2 filters","ciudad":"neiva","huespedes":2}
{"timestamp":"2026-10-24T14:23:43.127Z","level":"ERROR","service":"catalog-service","version":"2.0.0","environment":"main","trace_id":"6d2e8f1a4b7c40d9e3f5a6b7c8d9e0f1","span_id":"c3d4e5f60718293a","correlation_id":"corr-9c1d","event":"mongo.find.failed","message":"MongoDB did not answer the search in 2000 ms","duration_ms":2002,"mongo_operation":"find","ciudad":"neiva"}
{"timestamp":"2026-10-24T14:23:43.155Z","level":"INFO","service":"catalog-service","version":"2.0.0","environment":"main","trace_id":"6d2e8f1a4b7c40d9e3f5a6b7c8d9e0f1","span_id":"b2c3d4e5f6071829","correlation_id":"corr-9c1d","event":"http.request.completed","message":"GET /api/v1/propiedades","status":500,"duration_ms":2031,"error_code":"INTERNAL_ERROR"}
```

## SLIs during the 40 minutes

| SLI | Value | Target |
|---|---|---|
| A — search answers | 150 / 200 = **75 %** | 99.9 % |
| B — search ≤ 250 ms | **75 %** (the 50 failures took 2 s) | 95 % |
| C — availability fresh | ~100 % (`updateOne` by `_id` uses the `_id` index) | 99 % |

## Which alert fires first, and when

`CatalogSearchFastBurn` needs > 1.44 % in the 5 min **and** the 1 h window, for 2 min.

- 5 min window: 25 % after the first minute.
- 1 h window: 25 % × t / 60 > 1.44 % → t > **3.5 min**.
- Plus `for: 2m` → it **pages at minute 6 (14:16)**.

`CatalogSearchSlowBurn` (6 h window: 25 % × t / 360 > 0.6 % → t > 8.6 min, + 5 min)
would follow at minute 14, but the page already went out.

## Which runbook step stops it

Mitigation 1 (search without dates) was tried first and did **not** help — the slow part
was the city filter. Step 4 of "Confirm it" (`explain`) showed **`COLLSCAN`**: the index
was gone. **Mitigation 2, re-create the indexes**, stopped the bleeding.

## Blameless postmortem

**Timeline — Saturday 2026-10-24**

| Time | What happened |
|---|---|
| 14:05 | The seed script of `property-catalog-db` is run again on `main` to add new properties. It drops and re-creates the collection, without `idx_properties_city_capacity` |
| 14:10 | Peak starts; searches for big cities (Neiva, 25 % of them) scan the whole collection |
| 14:16 | `CatalogSearchFastBurn` pages the on-call |
| 14:19 | Mitigation 1 applied, no change |
| 14:31 | `explain()` shows `COLLSCAN`; Catalog owner joins |
| 14:46 | Indexes re-created from the seed script |
| 14:50 | Errors at 0; alert resolved 14:53 |

**Impact.** 50 failed searches of the **60** allowed per month: **83 % of the SLO A
budget** in one afternoon. In minutes: 40 × 25 % = 10 min of full outage = 23 % of 43.2;
the request number is the real one, because the peak had almost 4 times the average.
SLO B: 50 of 3,000 = 1.7 %. SLO C: nothing. No booking was lost by Booking itself, but
some guests left before reaching it. The 75 % policy applies: only fixes until it recovers.

**Root cause.** The seed script creates the indexes only on the first run; when it was
run again it dropped the collection and the indexes with it.

**Contributing factors.**
- Nobody checks the indexes after a seed or a deploy.
- The runbook put the date-filter flag first; it cost 12 minutes on the wrong fix.
- The seed script is allowed to run on `main` with live traffic.

**Action items.**

1. *As the Catalog owner, I want the seed script to create the indexes every time it
   runs, so that re-seeding never leaves the search without them.*
   Given the seed runs on a database that already has `properties`, when it ends, then
   `idx_properties_city_capacity` and `idx_properties_geo` exist, and the script fails
   if one is missing.
2. *As on-call, I want the runbook to check `explain()` before the flag, so that a missing
   index is found in the first 5 minutes.*
   Given `CatalogSearchFastBurn` fires and `explain` shows `COLLSCAN`, when I follow the
   runbook, then the first mitigation offered is to re-create the indexes.
3. *As the team, I want a check in CI of `property-catalog-db` that fails without the
   indexes, so that the problem never reaches `main`.*
   Given a PR that changes the seed, when CI runs it on an empty MongoDB, then the job
   lists the indexes and fails if `idx_properties_city_capacity` is not there.
