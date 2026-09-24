<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       03-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 03

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Define and document the domain architecture for MVP 1, formalizing the PDR decisions into the base domain documents (System Overview, Domain Events, Domain Map, Entities-and-rules).
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID | Title                                                                                                             | Status (todo/doing/done) | Evidence (PR or commit URL) |
| ----- | ----------------------------------------------------------------------------------------------------------------- | ------------------------ | --------------------------- |
| N/A   | No user stories were worked this week — effort was focused on domain (DDD) documentation, not feature development | N/A                      | Not added yet               |

## 2. My individual contribution

- Wrote and structured the **System Overview** document, describing the system, the problem it solves, main users, and technology stack (React + Spring Boot).
- Wrote the **Domain Events** document, cataloging the booking flow events (`ReservaCreada`, `PagoAprobado`, `PagoRechazado`, `ReservaConfirmada`, `ReservaCancelada`), their payloads, consumers, and reaction policies (choreographed Saga).
- Wrote the **Domain Map — Bounded Contexts** document, defining the three Bounded Contexts (Catalog, Booking, Payment), their Context Map, and their strategic classification (Core/Supporting/Generic).
- Wrote the **Entities, Value Objects, and Business Rules** document, modeling the `Reserva` and `Pago` entities with their business invariants, state machines, and Java/Spring Boot code examples following Hexagonal Architecture.

## 3. Blockers and risks

- The messaging broker (Kafka vs. RabbitMQ) has not been decided yet, leaving the documented topic naming pending adjustment.
- No formal Event Storming session has been held with the team; the Bounded Contexts were defined directly. This is a risk that some contexts or business rules may be missing (e.g. host management).
- Team student IDs and contact information are still pending in the project documentation.

## 4. Plan for next week

- Define the first user stories (HU) for MVP 1 based on the "happy path" described in the PDR.
- Decide on the messaging broker (Kafka or RabbitMQ) and update the event documentation accordingly.
- Start the base setup of the three microservices (Spring Boot project structure with Hexagonal Architecture) in the repository.
- Run a short Event Storming session to validate the Domain Map before starting implementation.

## 5. Compliance self-check

- [ ] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — N/A, no HU work this week, only documentation directly on `main`
- [ ] Testable acceptance criteria — N/A, no HU this week
- [ ] Tests added/updated (unit / integration) — N/A, no code this week
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) — N/A, only the domain model was defined in documentation; no infrastructure code written yet
- [x] No secrets; config via environment variables — no credentials or sensitive configuration were handled this week (documentation-only work)

## 6. Evidence links

- Not added yet
