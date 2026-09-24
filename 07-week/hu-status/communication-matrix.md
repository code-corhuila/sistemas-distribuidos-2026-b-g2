# Service Communication Matrix — pms-properties

> For each interaction in the system: synchronous or asynchronous, which technology, and why.
> Synchronous interactions use REST; asynchronous interactions use pub/sub topics through the broker.
> Event contracts are specified in `domain-events.md`.

---

## Decision criteria

| Question | Lean synchronous (REST/gRPC) | Lean asynchronous (events) |
|---|---|---|
| Does the caller need an answer now? | Yes | No |
| Must the caller survive the callee being down? | No | Yes |
| Do many consumers share the same fact? | No | Yes |
| Public / browser-accessible? | REST | — |
| Internal and high-throughput? | gRPC | events |

---

## Interaction matrix

| # | Interaction | Mode | Technology | Justification |
|---|---|---|---|---|
| 1 | Frontend (React) → Booking Service — create booking | **Sync** | REST | The guest needs an immediate answer: booking accepted (`201 PENDIENTE`) or dates unavailable (`409`). Browser-facing API, where REST is the natural fit. |
| 2 | Frontend (React) → Catalog Service — search properties | **Sync** | REST | The guest expects results on screen now. Also cacheable, a concrete advantage of REST for read-heavy search. |
| 3 | Booking Service → Catalog Service — validate property + price snapshot | **Sync** | REST | Booking needs an immediate decision before creating the reservation: does the property exist, what is its price? It cannot proceed without that answer. |
| 4 | Booking Service → Payment Service — process charge | **Async** | Topic `reservas.reserva.creada` | Booking does not need the charge result to answer the guest — it returns `PENDIENTE` immediately. This avoids the cascading synchronous chain: if the payment gateway is slow, Booking does not freeze. |
| 5 | Payment Service → Booking Service — charge outcome | **Async** | Topics `pagos.pago.aprobado` / `pagos.pago.rechazado` | Payment needs no response from Booking; it only announces a completed fact. |
| 6 | Booking Service → Catalog + Notification — booking confirmed / cancelled / expired | **Async** | Topics `reservas.reserva.confirmada`, `.cancelada`, `.expirada` | Classic pub/sub: one fact, multiple independent consumers (Catalog updates its read model, Notification sends the email). Booking neither knows nor cares who subscribes. |
| 7 | Payment Service → External gateway (Stripe/PayPal) | **Sync** | REST (through an ACL) | The charge result is needed immediately to decide whether to emit `PagoAprobado` or `PagoRechazado`. Requires timeouts and a circuit breaker. |

---

## Why no gRPC in this system

The synchronous interactions here are either **public/browser-facing** (#1, #2 — where REST is the
correct choice) or **low-volume** (#3 — one call per booking, not a high-throughput path that would
justify gRPC's extra tooling complexity). The bulk of critical internal traffic is already
asynchronous by design through the Saga pattern.

If Catalog were later to receive thousands of validation calls per second from Booking,
interaction #3 would be the natural candidate to migrate to gRPC.

---

## Delivery semantics

The broker is configured for **at-least-once** delivery. Exactly-once delivery does not exist
end-to-end across a network — what this system implements is exactly-once **processing**:
at-least-once delivery plus an idempotency key plus deduplication at the consumer.

| Semantics | Behaviour | Used here? |
|---|---|---|
| At-most-once | May lose messages | No — unacceptable for payment and booking flows |
| At-least-once | May deliver duplicates | **Yes** — the broker default, handled by idempotent consumers |
| Exactly-once (delivery) | Does not exist end-to-end | N/A |
| Exactly-once (processing) | At-least-once + idempotency key + dedup | **Yes** — the design target |

---

## Idempotent consumer

**Consumer:** Payment Service, handling `ReservaCreada`.

Two layers of protection:

1. **Technical idempotency** — has this `eventId` already been consumed? Guards against broker
   redelivery.
2. **Business idempotency** — has this `reservaId` already been charged? Guards against double-charging
   even if the same booking somehow arrives through a different event.

```java
@Transactional
public void handleReservaCreada(ReservaCreadaEvent event) {
    // 1. Technical idempotency: already processed this eventId?
    if (processedEventRepository.existsById(event.getEventId())) {
        return; // broker duplicate, discard silently
    }

    // 2. Business idempotency: already charged this reservation?
    if (paymentRepository.existsByReservaId(event.getPayload().getReservaId())) {
        processedEventRepository.save(new ProcessedEvent(event.getEventId()));
        return; // already charged, do not charge again
    }

    // 3. Apply the effect exactly once
    paymentService.processCharge(event.getPayload());

    // 4. Mark as processed (same transaction)
    processedEventRepository.save(new ProcessedEvent(event.getEventId()));
}
```

Backed at the database level by the `UNIQUE` constraint on `processed_event_id` in the `payments`
table (see `models.md`), so even concurrent duplicate deliveries fail at the constraint rather than
producing a second charge.

---

## Resilience requirements for synchronous calls

Interactions #3 and #7 are the only remaining synchronous service-to-service calls, and both must have:

- **Timeout** — never wait indefinitely for a response.
- **Retry with backoff** — for transient failures only.
- **Circuit breaker** — stop calling a failing dependency rather than piling up threads waiting on it.

This is the direct mitigation for the cascading-failure scenario: without these, a slow external
payment gateway could exhaust Payment Service's thread pool and stall the whole booking flow.

---

## Pending

- Circuit breaker and timeout configuration for interactions #3 and #7 are not yet implemented.
- Broker choice (Kafka vs RabbitMQ) still not finalized; topic names use neutral dot-notation that
  maps to either.
