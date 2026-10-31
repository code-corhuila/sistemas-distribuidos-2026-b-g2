"""Outbound call of the journey: the MongoDB find on `properties`.

The Mongo driver has no headers, so the trace context travels in the `comment` of the
query. It appears in the Mongo profiler and slow-query log next to the query.
"""
import time

from .logjson import log
from .tracing import current_span


class PropertyRepository:
    def __init__(self, collection):
        self.collection = collection  # pymongo Collection in the real service

    def search(self, ciudad: str, huespedes: int) -> list:
        span = current_span.get().child()
        query = {"city": ciudad.lower(), "capacity": {"$gte": huespedes}}
        started = time.perf_counter()
        docs = list(self.collection.find(query, comment=f"traceparent={span.header()}"))
        log("INFO", "mongo.find.completed", "find on properties",
            mongo_operation="find", ciudad=ciudad.lower(), huespedes=huespedes,
            results_count=len(docs), duration_ms=round((time.perf_counter() - started) * 1000))
        return docs
