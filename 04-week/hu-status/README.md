<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       04-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 04

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Structure booking-service as a walking skeleton (hexagonal folders, composition root, /health endpoint against a real database) and plan the MVP1 sprint contract-first (API contract, task board, MoSCoW scope, and Definition of Done).
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID       | Title                                                                                      | Status (todo/doing/done) | Evidence (PR or commit URL) |
| ----------- | ------------------------------------------------------------------------------------------ | ------------------------ | --------------------------- |
| HU-00       | Walking skeleton: booking-service folder structure, composition root, and /health endpoint | done                     | Not added yet               |
| HU-PLAN-001 | Design MVP1 API contract-first (openapi.yaml) for booking-service                          | done                     | Not added yet               |
| HU-PLAN-002 | Define MVP1 task board, MoSCoW scope, and Definition of Done                               | done                     | Not added yet               |

## 2. My individual contribution

- Designed the hexagonal folder structure for `booking-service` (`domain/`, `application/`, `adapters/in`, `adapters/out`, `config/`, `tests/`), keeping the domain layer free of framework/infrastructure imports.
- Wrote the composition root pattern (`CompositionRoot.java`) wiring the `ReservaRepository` port to its JPA adapter, and the `CrearReservaUseCase` depending only on the port, not on a concrete implementation.
- Implemented the walking skeleton entry point (`/health` endpoint) as the thinnest end-to-end slice to validate the service runs against a real database container before adding full Saga logic.
- Drafted the MVP1 API contract (`openapi.yaml`) for `POST /api/v1/reservas` and `GET /api/v1/reservas/{reservaId}`, including request/response schemas and error cases (409 for overlapping dates, 404 for not found).
- Broke down the MVP1 sprint into small, testable tasks (HU-BOOK-001 to HU-BOOK-004, HU-PAY-001, HU-CAT-001) and prioritized them using MoSCoW, protecting the sprint goal from scope creep (discounts, refunds, and multi-currency were pushed to the backlog).
- Wrote the Definition of Done for the MVP1 release: tests green, services running in containers against real databases, happy path and key error path both handled, and no secrets committed.

## 3. Blockers and risks

- The API contract is drafted but not yet validated against a running implementation — endpoints are defined on paper (openapi.yaml), not yet fully wired end-to-end.
- Lock TTL / `ReservaExpirada` logic is scoped as a Should, not a Must, for MVP1 — risk of scope creep if the team decides mid-sprint it's needed sooner.
- No formal contract yet defined for the Identity service's user event (`UsuarioRegistrado`), which the Shared Kernel relationship in the Domain Map depends on.

## 4. Plan for next week

- Containerize the three microservices (Dockerfiles + docker-compose.yml) so the walking skeleton runs against real databases in containers, not just locally.
- Implement `POST /reservas` end-to-end following the contract-first design (controller → use case → domain → port → JPA adapter → PostgreSQL).
- Add evidence links (PRs/commits) once the walking skeleton and planning artifacts are pushed to GitHub.

## 5. Compliance self-check

- [ ] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — N/A, work done directly on `main` this week
- [x] Testable acceptance criteria — defined for HU-BOOK-001 (POST /reservas → 201/409) and HU-PAY-001 (idempotent charge) as part of MVP1 planning
- [ ] Tests added/updated (unit / integration) — N/A, walking skeleton only, no business logic tests yet
- [x] DDD / hexagonal boundaries respected (domain has no I/O) — `Reserva` domain class has zero framework imports; JPA/Spring only appear in `adapters/out/persistence`
- [x] No secrets; config via environment variables — database connection wired via environment variables, no credentials hardcoded

## 6. Evidence links

- Not added yet
