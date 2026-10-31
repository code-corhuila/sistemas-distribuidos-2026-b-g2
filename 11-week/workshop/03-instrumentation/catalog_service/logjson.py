"""CP2 log contract for catalog-service: one JSON object per line on stdout."""
import json
import os
import sys
from datetime import datetime, timezone

from .tracing import current_correlation, current_span

SERVICE = os.getenv("SERVICE_NAME", "catalog-service")
VERSION = os.getenv("SERVICE_VERSION", "2.0.0")
ENVIRONMENT = os.getenv("APP_ENV", "dev")
NEVER_LOG = {"usuarioId", "email", "authorization", "displayName", "payload"}


def log(level: str, event: str, message: str, **fields) -> dict:
    span = current_span.get()
    line = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
        "level": level,
        "service": SERVICE,
        "version": VERSION,
        "environment": ENVIRONMENT,
        "trace_id": span.trace_id if span else None,
        "span_id": span.span_id if span else None,
        "correlation_id": current_correlation.get(),
        "event": event,
        "message": message,
    }
    line.update({k: v for k, v in fields.items() if k not in NEVER_LOG})
    print(json.dumps(line, ensure_ascii=False), file=sys.stdout, flush=True)
    return line
