# Session Notes — Planning: Service Design, Data Ownership & Contracts

## Self-check answers

**Question 1.** Each piece of data must be...
Correct answer: **Owned by a single service; others use its contract.**

**Question 2.** A service contract must define...
Correct answer: **Method/route (or event), request, response, and errors — versioned.**

**Question 3.** Prefer an asynchronous event when...
Correct answer: **The caller does not need an immediate response (decoupling/resilience).**

**Question 4.** An Anti-Corruption Layer (ACL) is used to...
Correct answer: **Translate an external/legacy model so it doesn't leak into your domain.**

**Question 5.** A good sprint slice is...
Correct answer: **A thin vertical slice that works end-to-end and is demonstrable.**

**Question 6.** Two services need the customer's email. What's the best approach?
Correct answer: **An owner exposes a contract; others keep a minimal copy through events.**

---

## This week's exercise, applied to my project (pms-properties)

### 1. Data ownership per entity

| Entity                              | Owning service       | Who must NOT read its database directly                                                           |
| ----------------------------------- | -------------------- | ------------------------------------------------------------------------------------------------- |
| Reserva                             | Booking Service      | Catalog, Payment, Notification — all receive events only                                          |
| Pago                                | Payment Service      | Booking only knows the outcome via PagoAprobado/PagoRechazado                                     |
| Propiedad                           | Catalog Service      | Booking only keeps a minimal copy (propiedadId + a price/name snapshot at booking time)           |
| User / profile                      | Identity Service     | All other contexts keep only userId as a reference (Shared Kernel, as defined in the Context Map) |
| Message templates and delivery logs | Notification Service | No one else — it is purely reactive to events                                                     |

### 2. Service contracts

**Synchronous contract** (used when an immediate decision is needed):

This is the only point where Booking needs an immediate response from Catalog: when creating a booking, to validate that the property exists and to fetch a price snapshot (not to check availability — that is controlled by Booking itself through its strict date locking).

**Asynchronous contracts** (already defined in `domain-events.md`): `ReservaCreada`, `PagoAprobado`, `PagoRechazado`, `ReservaConfirmada`, `ReservaCancelada`, and the newly added `ReservaExpirada` from the updated Domain Map.

**Still pending:** the formal contract for the event Identity emits when a user registers — something like `UsuarioRegistrado`, since the Domain Map currently states that Shared Kernel has "no formal event yet specified."

### 3. Anti-Corruption Layer (ACL)

The clearest place for an ACL in this project is **Payment Service toward the external payment gateway** (Stripe/PayPal, per the updated Domain Map). The external gateway has its own data model (field names, error codes, conventions) that should not leak into the domain:

The ACL translates, for example, Stripe's own error code into the domain's `motivoRechazo`, and Stripe's `charge.id` into the domain's `transaccionId`. If the payment provider changes later, only the ACL needs to be rewritten, not the whole `Pago` domain.

### 4. Vertical slice for MVP 1

Already defined in the PDR as the "happy path." Formalized here as user stories with testable acceptance criteria:

**HU-BOOK-001** — As a guest, I can request a booking for a property on specific dates, so the system locks the inventory while my payment is processed.
Acceptance criteria: `POST /api/v1/reservas` with a valid `propiedadId` and `fechas` returns `201` with `estado: PENDIENTE`; if the dates overlap an existing active booking, it returns `409`.

**HU-PAY-001** — As the system, when I receive `ReservaCreada`, I attempt to process the charge idempotently.
Acceptance criteria: given the same `eventId` received twice, only one `Pago` is created (verifiable in the ledger).

**HU-BOOK-002** — As a guest, my booking is automatically confirmed when the payment is approved.
Acceptance criteria: upon receiving `PagoAprobado`, `Reserva.estado` changes to `CONFIRMADA` within X seconds.

This is exactly the kind of vertical slice the session asks for: it crosses all three services (Booking -> Payment -> Booking), is demonstrable end-to-end, and avoids the common mistake of "this sprint we do all the databases."
