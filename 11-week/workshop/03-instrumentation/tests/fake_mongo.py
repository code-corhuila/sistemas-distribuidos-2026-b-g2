"""In-memory stand-in for the `properties` collection; records the query comment."""


class FakeCollection:
    def __init__(self, documents):
        self.documents = documents
        self.last_comment = None

    @classmethod
    def with_sample_data(cls):
        return cls([
            {"id": "prop-042", "city": "neiva", "capacity": 4, "pricePerNightCents": 18000000},
            {"id": "prop-118", "city": "neiva", "capacity": 2, "pricePerNightCents": 9500000},
            {"id": "prop-207", "city": "pitalito", "capacity": 6, "pricePerNightCents": 21000000},
        ])

    def find(self, query, comment=None):
        self.last_comment = comment
        return [d for d in self.documents
                if d["city"] == query["city"] and d["capacity"] >= query["capacity"]["$gte"]]
