"""Minimal catalog-service: GET /api/v1/propiedades and GET /metrics (WSGI)."""
import json
import time
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from .logjson import log
from .metrics import SearchMetrics
from .middleware import TraceMiddleware
from .repository import PropertyRepository


def create_app(collection):
    repository = PropertyRepository(collection)
    metrics = SearchMetrics()

    def app(environ, start_response):
        path = environ.get("PATH_INFO", "")
        if path == "/metrics":
            start_response("200 OK", [("Content-Type", "text/plain; version=0.0.4")])
            return [metrics.render().encode()]
        if path != "/api/v1/propiedades":
            start_response("404 Not Found", [("Content-Type", "application/json")])
            return [b'{"error":"NOT_FOUND"}']

        started = time.perf_counter()
        params = parse_qs(environ.get("QUERY_STRING", ""))
        ciudad = params.get("ciudad", [""])[0]
        try:
            huespedes = int(params.get("huespedes", ["1"])[0])
            if not 1 <= huespedes <= 20:
                raise ValueError
        except ValueError:
            log("WARN", "catalog.search.rejected", "huespedes must be an integer from 1 to 20",
                error_code="VALIDATION_ERROR")
            metrics.observe("invalid", time.perf_counter() - started)
            start_response("400 Bad Request", [("Content-Type", "application/json")])
            return [b'{"error":"VALIDATION_ERROR"}']
        try:
            docs = repository.search(ciudad, huespedes)
        except Exception:  # Mongo down or timed out
            log("ERROR", "mongo.find.failed", "MongoDB did not answer the search")
            metrics.observe("error", time.perf_counter() - started)
            start_response("500 Internal Server Error", [("Content-Type", "application/json")])
            return [b'{"error":"INTERNAL_ERROR"}']
        metrics.observe("ok" if docs else "empty", time.perf_counter() - started)
        body = {"data": docs, "meta": {"page": 1, "limit": 20, "total": len(docs)}}
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(body).encode()]

    return TraceMiddleware(app)


if __name__ == "__main__":
    from tests.fake_mongo import FakeCollection

    server = make_server("", 3002, create_app(FakeCollection.with_sample_data()))
    print("catalog-service listening on :3002 (in-memory properties)")
    server.serve_forever()
