# CP3 · How to run (catalog-service, Python)

Python 3.9 or newer. Only the standard library: no `pip install` needed.

- `catalog_service/tracing.py` — W3C `traceparent` parse/create, kept in a `ContextVar`.
- `catalog_service/middleware.py` — WSGI middleware: reads or creates the trace, returns
  it in the response, logs every request.
- `catalog_service/logjson.py` — CP2 log contract.
- `catalog_service/repository.py` — outbound call: the MongoDB `find` on `properties`
  carries the `traceparent` in the query `comment`.
- `catalog_service/metrics.py` — `catalog_search_requests_total` and
  `catalog_search_duration_seconds` on `/metrics`.

## Test

```bash
cd 11-week/workshop/03-instrumentation
python -m unittest -v
```

## Run

```bash
python -m catalog_service.app
curl -i "http://localhost:3002/api/v1/propiedades?ciudad=Neiva&huespedes=2" -H "traceparent: 00-4e0b7d2a9c15f3866d0e1a2b3c4d5f60-1122334455667788-01"
curl http://localhost:3002/metrics
```

It runs on in-memory sample properties; the real service uses `pymongo` with the same
`find(query, comment=...)` call.

## Console output on my machine

```text
test_metrics_count_requests_by_outcome (tests.test_trace_propagation.TracePropagationTest.test_metrics_count_requests_by_outcome) ... {"timestamp": "2026-10-20T04:15:53.182Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "4e0b7d2a9c15f3866d0e1a2b3c4d5f60", "span_id": "08240944281668f7", "correlation_id": "corr-e3ae76fb", "event": "mongo.find.completed", "message": "find on properties", "mongo_operation": "find", "ciudad": "neiva", "huespedes": 2, "results_count": 2, "duration_ms": 0}
{"timestamp": "2026-10-20T04:15:53.183Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "4e0b7d2a9c15f3866d0e1a2b3c4d5f60", "span_id": "08240944281668f7", "correlation_id": "corr-e3ae76fb", "event": "http.request.completed", "message": "GET /api/v1/propiedades", "status": 200, "duration_ms": 0}
{"timestamp": "2026-10-20T04:15:53.183Z", "level": "WARN", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "4e0b7d2a9c15f3866d0e1a2b3c4d5f60", "span_id": "481b0d6c0825d94d", "correlation_id": "corr-6bf23dec", "event": "catalog.search.rejected", "message": "huespedes must be an integer from 1 to 20", "error_code": "VALIDATION_ERROR"}
{"timestamp": "2026-10-20T04:15:53.183Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "4e0b7d2a9c15f3866d0e1a2b3c4d5f60", "span_id": "481b0d6c0825d94d", "correlation_id": "corr-6bf23dec", "event": "http.request.completed", "message": "GET /api/v1/propiedades", "status": 400, "duration_ms": 0}
{"timestamp": "2026-10-20T04:15:53.184Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "0b095d8d1b57bb73e24fc39debd26b7b", "span_id": "0724512a36ab8ef3", "correlation_id": "corr-39c4c0ca", "event": "http.request.completed", "message": "GET /metrics", "status": 200, "duration_ms": 1}
ok
test_new_trace_when_the_caller_sends_none (tests.test_trace_propagation.TracePropagationTest.test_new_trace_when_the_caller_sends_none) ... {"timestamp": "2026-10-20T04:15:53.184Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "715cf7a67871bc590fc4b0817a92f703", "span_id": "30fcdb8f35576a2f", "correlation_id": "corr-79dd21bd", "event": "mongo.find.completed", "message": "find on properties", "mongo_operation": "find", "ciudad": "neiva", "huespedes": 1, "results_count": 2, "duration_ms": 0}
{"timestamp": "2026-10-20T04:15:53.184Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "715cf7a67871bc590fc4b0817a92f703", "span_id": "30fcdb8f35576a2f", "correlation_id": "corr-79dd21bd", "event": "http.request.completed", "message": "GET /api/v1/propiedades", "status": 200, "duration_ms": 0}
ok
test_trace_id_received_is_the_trace_id_sent_to_mongo (tests.test_trace_propagation.TracePropagationTest.test_trace_id_received_is_the_trace_id_sent_to_mongo) ... {"timestamp": "2026-10-20T04:15:53.185Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "4e0b7d2a9c15f3866d0e1a2b3c4d5f60", "span_id": "a59b9304bc685830", "correlation_id": "corr-7b289d95", "event": "mongo.find.completed", "message": "find on properties", "mongo_operation": "find", "ciudad": "neiva", "huespedes": 3, "results_count": 1, "duration_ms": 0}
{"timestamp": "2026-10-20T04:15:53.185Z", "level": "INFO", "service": "catalog-service", "version": "2.0.0", "environment": "dev", "trace_id": "4e0b7d2a9c15f3866d0e1a2b3c4d5f60", "span_id": "a59b9304bc685830", "correlation_id": "corr-7b289d95", "event": "http.request.completed", "message": "GET /api/v1/propiedades", "status": 200, "duration_ms": 0}
ok
```
