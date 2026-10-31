# Domain Modeling Exercise — Weekly Self-Check

## Self-check answers

**Question 1.** In hexagonal architecture, dependencies point...
**Inward: adapters → application → domain**

**Question 2.** An aggregate root is...
**The only place where domain invariants are modified**

**Question 3.** A value object is...
**Immutable, equality by value, no identity**

**Question 4.** In DDD, a repository is...
**A port (interface) in the domain, implemented in infrastructure**

**Question 5.** Adding a JPA `@Entity` annotation to a domain class...
**Leaks infrastructure into the domain (a boundary violation)**

**Question 6.** The "anemic domain" smell is fixed by...
**Moving invariants into the aggregate; private fields; thin services**

---

## This week's exercise: model a Bounded Context from your product

**Bounded Context chosen:** Booking

**Aggregate Root:** `Reserva`

**Internal entities:** None — `Reserva` is a simple aggregate with no child entities in this MVP; it is composed directly of Value Objects.

**Value Objects:**

- `DateRange` (fechaInicio, fechaFin) — the requested date range
- `Money` (monto, moneda) — total amount to be charged for the booking

**Invariants it protects:**

1. **No overlapping dates** — a property cannot have two bookings in `PENDIENTE` or `CONFIRMADA` status with overlapping date ranges.
2. **Valid state transitions** — only `PENDIENTE → CONFIRMADA` or `PENDIENTE → CANCELADA` are allowed; `CONFIRMADA` and `CANCELADA` are terminal states.
3. **Positive amount** — the booking's total must always be greater than zero.

**Domain events it emits:**

- `ReservaCreada` — when the booking is created and the dates are temporarily locked.
- `ReservaConfirmada` — when the `PagoAprobado` event is received from Payment.
- `ReservaCancelada` — when the `PagoRechazado` event is received from Payment (compensating action: releases the dates).

**Why this is a good aggregate example:** all of the invariants above can only be guaranteed if `Reserva` is treated as a single transactional unit — its status, dates, and amount must always change together and consistently, backed by PostgreSQL's local ACID guarantees in Booking Service.
