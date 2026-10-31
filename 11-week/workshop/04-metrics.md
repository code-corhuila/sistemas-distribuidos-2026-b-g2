# CP4 · Golden signals and metric catalog (search journey)

Prometheus conventions: `snake_case`, unit suffix, `_total` on counters. The scrape
config adds `service`, `environment` and `version`; the code never does.

## api-gateway (NGINX)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `gateway_request_duration_seconds` | histogram | `route` | `histogram_quantile(0.95, sum by (le) (rate(gateway_request_duration_seconds_bucket{route="/api/v1/propiedades"}[5m])))` |
| Traffic | `gateway_requests_total` | counter | `route`, `status_class` | `sum(rate(gateway_requests_total{route=~"/api/v1/propiedades.*"}[5m]))` |
| Errors | `gateway_requests_total` | counter | `status_class` | `sum(rate(gateway_requests_total{route=~"/api/v1/propiedades.*",status_class="5xx"}[5m]))` |
| Saturation | `nginx_connections_active` | gauge | — | `max(nginx_connections_active)` |

## catalog-service — search (E-05) and detail (E-06)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `catalog_search_duration_seconds` | histogram | — | `histogram_quantile(0.95, sum by (le) (rate(catalog_search_duration_seconds_bucket[5m])))` |
| Traffic | `catalog_search_requests_total` | counter | `route`, `outcome` (`ok`, `empty`, `invalid`, `error`) | `sum by (outcome) (rate(catalog_search_requests_total[5m]))` |
| Errors | `catalog_search_requests_total` | counter | `outcome="error"` | `sum(rate(catalog_search_requests_total{outcome="error"}[5m])) / sum(rate(catalog_search_requests_total{outcome!="invalid"}[5m]))` |
| Saturation | `process_open_fds` / worker busy | gauge | — | `max(catalog_http_workers_busy) / max(catalog_http_workers_total)` |

`outcome="empty"` is not an error, but a jump of empty searches for `neiva` after a
deploy is a symptom (broken city normalization). `invalid` (400) is the guest's mistake
and does not count against availability.

## catalog-service — availability consumer

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `catalog_event_lag_seconds` | histogram | `event_type` | `histogram_quantile(0.95, sum by (le) (rate(catalog_event_lag_seconds_bucket[5m])))` — time from `occurredAt` of the event to the Mongo update |
| Traffic | `catalog_events_consumed_total` | counter | `event_type`, `outcome` (`applied`, `duplicate`, `rejected`) | `sum by (event_type) (rate(catalog_events_consumed_total[5m]))` |
| Errors | `catalog_events_consumed_total` | counter | `outcome="rejected"` | `sum(rate(catalog_events_consumed_total{outcome="rejected"}[5m]))` |
| Saturation | `rabbitmq_queue_messages_ready` | gauge | `queue` | `max(rabbitmq_queue_messages_ready{queue=~"catalog.reservas.*"})` |

## MongoDB (`catalog` database)

| Signal | Metric | Type | Labels | PromQL |
|---|---|---|---|---|
| Latency | `catalog_mongo_operation_duration_seconds` | histogram | `operation` (`find`, `findOne`, `updateOne`) | `histogram_quantile(0.95, sum by (le, operation) (rate(catalog_mongo_operation_duration_seconds_bucket[5m])))` |
| Traffic | `mongodb_op_counters_total` (exporter) | counter | `type` | `sum by (type) (rate(mongodb_op_counters_total[5m]))` |
| Errors | `catalog_mongo_operation_errors_total` | counter | `operation`, `reason` (`timeout`, `network`) | `sum by (reason) (rate(catalog_mongo_operation_errors_total[5m]))` |
| Saturation | `mongodb_connections` (exporter) | gauge | `state` | `mongodb_connections{state="current"} / (mongodb_connections{state="current"} + mongodb_connections{state="available"})` |

## Cardinality

| Label | Values | Count |
|---|---|---|
| `route` | `/api/v1/propiedades`, `/api/v1/propiedades/{id}` | 2 |
| `outcome` | closed lists above | 3–4 |
| `event_type` | `ReservaCreada`, `ReservaConfirmada`, `ReservaCancelada`, `ReservaExpirada` | 4 |
| `operation`, `reason` | closed lists | 3 and 2 |

Forbidden as labels: `ciudad` (free text typed by the guest, unbounded), `propiedad_id`
(grows with the catalog), dates, `event_id`, `reserva_id`, raw query string. They go
in the logs (CP2). If we need "searches per city", we log `ciudad` and count from logs,
or keep a fixed top-10 list and put the rest under `other`.

## Buckets

Search: `0.025, 0.05, 0.1, 0.25, 0.5, 1, 2` seconds. The search is one indexed `find`
(`idx_properties_city_capacity`) plus the `unavailableRanges` filter; the portal shows
a spinner and the guest expects results almost at once, so our target is **300 ms**
(CP6). Buckets are dense under 0.5 s; above 2 s the guest has left.

Consumer lag: `1, 5, 15, 30, 60, 300` seconds. Catalog is eventually consistent by
design (`01-context/scope.md`); a few seconds of lag is normal, minutes are not.
