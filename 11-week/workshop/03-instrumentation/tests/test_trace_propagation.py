import io
import unittest

from catalog_service.app import create_app
from tests.fake_mongo import FakeCollection

TRACE_ID = "4e0b7d2a9c15f3866d0e1a2b3c4d5f60"
INCOMING = f"00-{TRACE_ID}-1122334455667788-01"


def call(app, path, query="", traceparent=None):
    environ = {"REQUEST_METHOD": "GET", "PATH_INFO": path, "QUERY_STRING": query,
               "wsgi.input": io.BytesIO(b"")}
    if traceparent:
        environ["HTTP_TRACEPARENT"] = traceparent
    captured = {}

    def start_response(status, headers, exc_info=None):
        captured["status"] = status
        captured["headers"] = dict(headers)

    body = b"".join(app(environ, start_response))
    return captured["status"], captured["headers"], body.decode()


class TracePropagationTest(unittest.TestCase):
    def setUp(self):
        self.collection = FakeCollection.with_sample_data()
        self.app = create_app(self.collection)

    def test_trace_id_received_is_the_trace_id_sent_to_mongo(self):
        status, headers, _ = call(self.app, "/api/v1/propiedades", "ciudad=Neiva&huespedes=3", INCOMING)

        self.assertEqual("200 OK", status)
        sent = self.collection.last_comment.split("=", 1)[1]
        self.assertEqual(TRACE_ID, sent.split("-")[1])
        self.assertNotEqual("1122334455667788", sent.split("-")[2])
        self.assertEqual(TRACE_ID, headers["traceparent"].split("-")[1])

    def test_new_trace_when_the_caller_sends_none(self):
        _, headers, _ = call(self.app, "/api/v1/propiedades", "ciudad=neiva&huespedes=1")
        self.assertRegex(headers["traceparent"], r"^00-[0-9a-f]{32}-[0-9a-f]{16}-01$")

    def test_metrics_count_requests_by_outcome(self):
        call(self.app, "/api/v1/propiedades", "ciudad=neiva&huespedes=2", INCOMING)
        call(self.app, "/api/v1/propiedades", "ciudad=neiva&huespedes=30", INCOMING)
        _, _, metrics = call(self.app, "/metrics")
        self.assertIn('catalog_search_requests_total{route="/api/v1/propiedades",outcome="ok"} 1', metrics)
        self.assertIn('catalog_search_requests_total{route="/api/v1/propiedades",outcome="invalid"} 1', metrics)
        self.assertIn("catalog_search_duration_seconds_count 2", metrics)


if __name__ == "__main__":
    unittest.main()
