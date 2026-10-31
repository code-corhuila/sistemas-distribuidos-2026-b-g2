"""WSGI middleware: reads or creates traceparent, returns it, logs every request."""
import time
import uuid

from .logjson import log
from .tracing import current_correlation, current_span, span_from


class TraceMiddleware:
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        started = time.perf_counter()
        span = span_from(environ.get("HTTP_TRACEPARENT"))
        correlation = environ.get("HTTP_X_CORRELATION_ID") or f"corr-{uuid.uuid4().hex[:8]}"
        span_token = current_span.set(span)
        corr_token = current_correlation.set(correlation)
        status_holder = {}

        def traced_start_response(status, headers, exc_info=None):
            status_holder["status"] = int(status.split()[0])
            headers = list(headers) + [("traceparent", span.header()), ("X-Correlation-Id", correlation)]
            return start_response(status, headers, exc_info)

        try:
            return self.app(environ, traced_start_response)
        finally:
            log("INFO", "http.request.completed",
                f"{environ.get('REQUEST_METHOD')} {environ.get('PATH_INFO')}",
                status=status_holder.get("status"),
                duration_ms=round((time.perf_counter() - started) * 1000))
            current_span.reset(span_token)
            current_correlation.reset(corr_token)
