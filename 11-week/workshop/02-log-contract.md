# CP2 · Structured log contract (catalog journey)

`catalog-service` (Python) and the services that feed it (`api-gateway`,
`booking-service`) write one JSON object per line to stdout. Same names in every
service, so one search by `trace_id` or by `event_id` shows the whole path of a search
or of an availability update.

## Mandatory fields

| Field | Type | Required | Example | Why |
|---|---|---|---|---|
| `timestamp` | ISO-8601 UTC string | yes | `2026-10-19T15:02:10.530Z` | Put lines of Booking and Catalog in order; the update lags by design (eventual consistency) |
| `level` | `ERROR` / `WARN` / `INFO` / `DEBUG` | yes | `WARN` | Filter by severity |
| `service` | string | yes | `catalog-service` | Who wrote it |
| `version` | string | yes | `2.0.0` | Match the `v2.0.0` tag of the repo |
| `environment` | `dev` / `qa` / `main` | yes | `qa` | Our three environments |
| `trace_id` | 32 hex | yes | `4e0b7d2a9c15f3866d0e1a2b3c4d5f60` | One search or one event, end to end |
| `span_id` | 16 hex | yes | `7c3d4e5f60718293` | Which hop |
| `correlation_id` | string | yes | `corr-77ab` | `X-Correlation-Id`, also copied into the event |
| `event` | `noun.verb` string | yes | `event.received` | Stable name for counting |
| `message` | string | yes | `ReservaCreada received` | For people |
| `duration_ms` | integer | on the end of a request, a query or a consume | `2002` | Latency without a tracing backend |

## Domain fields

| Field | Type | Example | Why |
|---|---|---|---|
| `propiedad_id` | string | `prop-042` | The `Propiedad` searched, opened or updated |
| `ciudad` | string | `neiva` | Search filter of E-05, normalized (lowercase, no accents) — the same rule Catalog uses to match |
| `fecha_inicio`, `fecha_fin` | date `YYYY-MM-DD` | `2026-12-18` | Availability filter; needed to explain why a property was hidden |
| `huespedes` | integer 1–20 | `4` | Capacity filter |
| `results_count` | integer | `12` | An empty search for a city that has properties is a symptom |
| `event_id`, `event_type` | string | `ev-81c4`, `ReservaCreada` | Idempotent consumer: the `event_id` is the key of `processed_events` |
| `delivery_attempt` | integer | `2` | RabbitMQ redelivery count before the DLQ |
| `reserva_id` | uuid | `2f7c…` | Ties the range in `unavailableRanges` to its `Reserva` |

## Never log

| Data | Where | Masking |
|---|---|---|
| Guest identity (`usuarioId`, name, e-mail) | event payloads of Booking | Catalog does not need it: the consumer logs only `reserva_id`, `propiedad_id` and the dates |
| `Authorization` header / JWT | requests that pass the gateway | Header dropped; Catalog endpoints are public anyway |
| Host data (`host.displayName`) | `PropiedadDetail` | Not logged; `propiedad_id` is enough |
| Full query string with unknown params | E-05 | Only the four known filters are logged, never the raw URL |
| Full event payload | consumer | Only ids and dates; the payload stays in RabbitMQ |

## Seven lines of one failed availability update

`booking-service` publishes `ReservaCreada`; Catalog times out on MongoDB, the message
comes back, and the second try is rejected by a rule of the Catalog schema, so it goes
to the dead-letter queue.

```json
{"timestamp":"2026-10-19T15:02:10.004Z","level":"INFO","service":"booking-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"5a1b2c3d4e5f6071","correlation_id":"corr-77ab","event":"reserva.created","message":"reservation created as PENDIENTE","duration_ms":388,"reserva_id":"2f7c9d10-4b6e-4a8f-9c3d-1e2f3a4b5c6d","propiedad_id":"prop-042"}
{"timestamp":"2026-10-19T15:02:10.512Z","level":"INFO","service":"booking-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"6b2c3d4e5f607182","correlation_id":"corr-77ab","event":"outbox.event.published","message":"ReservaCreada published to RabbitMQ","duration_ms":12,"event_id":"ev-81c4","event_type":"ReservaCreada","reserva_id":"2f7c9d10-4b6e-4a8f-9c3d-1e2f3a4b5c6d"}
{"timestamp":"2026-10-19T15:02:10.530Z","level":"INFO","service":"catalog-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"7c3d4e5f60718293","correlation_id":"corr-77ab","event":"event.received","message":"ReservaCreada received","event_id":"ev-81c4","event_type":"ReservaCreada","delivery_attempt":1,"propiedad_id":"prop-042"}
{"timestamp":"2026-10-19T15:02:12.536Z","level":"ERROR","service":"catalog-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"8d4e5f6071829304","correlation_id":"corr-77ab","event":"mongo.update.timeout","message":"MongoDB did not answer updateOne on properties, message requeued","duration_ms":2002,"event_id":"ev-81c4","propiedad_id":"prop-042","mongo_operation":"updateOne"}
{"timestamp":"2026-10-19T15:02:13.541Z","level":"INFO","service":"catalog-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"9e5f607182930415","correlation_id":"corr-77ab","event":"event.received","message":"ReservaCreada received again","event_id":"ev-81c4","event_type":"ReservaCreada","delivery_attempt":2,"propiedad_id":"prop-042"}
{"timestamp":"2026-10-19T15:02:13.566Z","level":"WARN","service":"catalog-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"9e5f607182930415","correlation_id":"corr-77ab","event":"event.rejected","message":"property already has 500 unavailableRanges, the limit of the schema","duration_ms":25,"event_id":"ev-81c4","propiedad_id":"prop-042","error_code":"BUSINESS_RULE_VIOLATION"}
{"timestamp":"2026-10-19T15:02:13.571Z","level":"WARN","service":"catalog-service","version":"2.0.0","environment":"qa","trace_id":"4e0b7d2a9c15f3866d0e1a2b3c4d5f60","span_id":"9e5f607182930415","correlation_id":"corr-77ab","event":"event.dead_lettered","message":"ReservaCreada sent to the dead-letter queue catalog.reservas.dlq","event_id":"ev-81c4","propiedad_id":"prop-042","queue":"catalog.reservas.dlq"}
```

## Levels

| Level | When | Example |
|---|---|---|
| `ERROR` | A dependency failed and the work is not done | `mongo.update.timeout`; RabbitMQ connection lost |
| `WARN` | Handled but abnormal | `event.rejected`, `event.dead_lettered`, a duplicate `event_id` skipped |
| `INFO` | Normal business fact | `catalog.search.completed` with `results_count`, `event.received` |
| `DEBUG` | Local only | The Mongo filter built from the query params |
