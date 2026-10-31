"""Two metrics of the search, rendered in Prometheus text format."""
import threading

# Seconds. A search is one Mongo query with an index: it should answer well under 300 ms.
BUCKETS = (0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0)


class SearchMetrics:
    def __init__(self):
        self._lock = threading.Lock()
        self.requests = {}  # outcome -> count; outcome in {ok, empty, invalid, error}
        self.bucket_counts = [0] * len(BUCKETS)
        self.count = 0
        self.total = 0.0

    def observe(self, outcome: str, seconds: float) -> None:
        with self._lock:
            self.requests[outcome] = self.requests.get(outcome, 0) + 1
            for i, upper in enumerate(BUCKETS):
                if seconds <= upper:
                    self.bucket_counts[i] += 1
            self.count += 1
            self.total += seconds

    def render(self) -> str:
        route = 'route="/api/v1/propiedades"'
        out = ["# TYPE catalog_search_requests_total counter"]
        out += [f'catalog_search_requests_total{{{route},outcome="{o}"}} {n}' for o, n in self.requests.items()]
        out.append("# TYPE catalog_search_duration_seconds histogram")
        out += [f'catalog_search_duration_seconds_bucket{{le="{b}"}} {c}' for b, c in zip(BUCKETS, self.bucket_counts)]
        out.append(f'catalog_search_duration_seconds_bucket{{le="+Inf"}} {self.count}')
        out.append(f"catalog_search_duration_seconds_sum {self.total}")
        out.append(f"catalog_search_duration_seconds_count {self.count}")
        return "\n".join(out) + "\n"
