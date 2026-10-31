"""W3C trace context for catalog-service, kept per request in a ContextVar."""
import re
import secrets
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Optional

_TRACEPARENT = re.compile(r"^00-([0-9a-f]{32})-([0-9a-f]{16})-[0-9a-f]{2}$")


@dataclass(frozen=True)
class Span:
    trace_id: str
    span_id: str

    def header(self) -> str:
        return f"00-{self.trace_id}-{self.span_id}-01"

    def child(self) -> "Span":
        return Span(self.trace_id, secrets.token_hex(8))


current_span: ContextVar[Optional[Span]] = ContextVar("current_span", default=None)
current_correlation: ContextVar[Optional[str]] = ContextVar("current_correlation", default=None)


def span_from(traceparent: Optional[str]) -> Span:
    """Continue the caller's trace with a new span, or start a new trace."""
    match = _TRACEPARENT.match((traceparent or "").strip())
    if match:
        return Span(match.group(1), secrets.token_hex(8))
    return Span(secrets.token_hex(16), secrets.token_hex(8))
