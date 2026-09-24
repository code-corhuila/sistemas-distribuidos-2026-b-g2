# Session Notes — Planning: MVP 1 Sprint (Contract-First, Estimation, Scope)

## Self-check answers

**Question 1.** "Contract-first" means...
Correct answer: **Agree the API (request/response/errors) before implementing.**

**Question 2.** MoSCoW is used to...
Correct answer: **Prioritize: Must / Should / Could / Won't.**

**Question 3.** A sprint goal serves as...
Correct answer: **A shield against scope creep (commit only what serves it).**

**Question 4.** A release-grade Definition of Done includes...
Correct answer: **Tests green + runs in a container against a real DB + key error handled.**

**Question 5.** Story points estimate...
Correct answer: **Relative size/complexity (not hours-as-promises).**

**Question 6.** Mid-sprint "let's also add payments" should...
Correct answer: **Go to the backlog; re-plan next sprint (protect the goal).**

---

## This week's exercise, applied to my project (pms-properties)

### 1. API contract-first (openapi.yaml excerpt — MVP 1 happy path)

```yaml
openapi: 3.0.3
info:
  title: Booking Service API
  version: 1.0.0
paths:
  /api/v1/reservas:
    post:
      summary: Create a booking request (locks dates temporarily)
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [propiedadId, usuarioId, fechaInicio, fechaFin]
              properties:
                propiedadId:
                  type: string
                  format: uuid
                usuarioId:
                  type: string
                  format: uuid
                fechaInicio:
                  type: string
                  format: date
                fechaFin:
                  type: string
                  format: date
      responses:
        "201":
          description: Booking created, dates locked, status PENDIENTE
          content:
            application/json:
              schema:
                type: object
                properties:
                  reservaId:
                    type: string
                    format: uuid
                  estado:
                    type: string
                    example: PENDIENTE
        "409":
          description: Requested dates overlap an existing active booking
          content:
            application/json:
              schema:
                type: object
                properties:
                  error:
                    type: object
                    properties:
                      code:
                        type: string
                        example: FECHAS_NO_DISPONIBLES
                      message:
                        type: string
  /api/v1/reservas/{reservaId}:
    get:
      summary: Get current booking status
      parameters:
        - name: reservaId
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        "200":
          description: Current booking state
          content:
            application/json:
              schema:
                type: object
                properties:
                  reservaId:
                    type: string
                    format: uuid
                  estado:
                    type: string
                    enum: [PENDIENTE, CONFIRMADA, CANCELADA, EXPIRADA]
        "404":
          description: Booking not found
```

### 2. Task board — MVP 1 small tasks (testable AC)

| To Do                                                 | In Progress                                   | Done                                            |
| ----------------------------------------------------- | --------------------------------------------- | ----------------------------------------------- |
| HU-BOOK-003 GET /reservas/{id} status check           | HU-PAY-001 idempotent charge on ReservaCreada | HU-00 walking skeleton (health + real DB)       |
| HU-BOOK-004 emit ReservaExpirada on lock TTL timeout  | HU-BOOK-002 confirm booking on PagoAprobado   | HU-BOOK-001 POST /reservas + date-overlap check |
| HU-CAT-001 GET /propiedades/{id} snapshot for Booking |                                               |                                                 |

WIP limit: finish before starting — no more than 2 stories "In Progress" per person at once.

### 3. MoSCoW prioritization

| Must (MVP1)                                              | Should                                   | Could                                | Won't (now)                  |
| -------------------------------------------------------- | ---------------------------------------- | ------------------------------------ | ---------------------------- |
| POST /reservas (create + lock dates, INV-001 no overlap) | GET /reservas/{id} status endpoint       | Refund flow for a CONFIRMADA booking | Discounts / coupons          |
| ReservaCreada -> Payment idempotent charge (INV-004)     | Lock TTL / ReservaExpirada compensation  | Host-facing property management UI   | Multi-currency support       |
| PagoAprobado -> ReservaConfirmada                        | Basic email notification on confirmation | SMS/Push notifications               | Full Identity/OAuth2 service |
| PagoRechazado -> ReservaCancelada (compensation)         |                                          |                                      |                              |

Sprint goal (shield against scope creep): "A guest can request a booking for an available property, have the payment processed idempotently, and see the booking confirmed or cancelled accordingly." Anything outside this — discounts, refunds, multi-currency, full Identity service — goes to the backlog, not into MVP 1.

### 4. Definition of Done — MVP 1

- Acceptance criteria met for HU-BOOK-001, HU-PAY-001, HU-BOOK-002 (the committed Musts).
- Unit tests green for the domain layer (Reserva invariants: no overlap, valid transitions, positive amount; Pago idempotency).
- Integration tests green using Testcontainers against real PostgreSQL instances for booking-service and payment-service.
- Each service runs in a container (docker-compose) against a real database — not just "it compiles."
- The happy path responds correctly (POST /reservas -> 201 PENDIENTE -> event flow -> CONFIRMADA) and the key error case is handled (overlapping dates -> 409; payment rejection -> CANCELADA compensation, not a silent failure).
- No secrets committed; all configuration (DB credentials, gateway keys) is via environment variables.
- README and domain-events.md / entities-and-rules.md updated to match whatever was actually implemented, including the ReservaExpirada event if the TTL logic ships in MVP 1.
