<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       07-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 07

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Formalize API and event contracts as versioned, machine-readable documents; define backward-compatibility rules; and add the first consumer-driven contract test (Pact) between Payment and Booking Service.
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID           | Title                                                                                                    | Status (todo/doing/done) | Evidence (PR or commit URL) |
| --------------- | -------------------------------------------------------------------------------------------------------- | ------------------------ | --------------------------- |
| HU-CONTRACT-001 | Publish versioned openapi.yaml for booking-service with standard error envelope                          | done                     | Not added yet               |
| HU-CONTRACT-002 | Document versioning and compatibility policy for REST APIs and domain events                             | done                     | Not added yet               |
| HU-CONTRACT-003 | Add first Pact contract test: payment-service (consumer) verifying booking-service's ReservaCreada event | doing                    | Not added yet               |

## 2. My individual contribution

- Formalized `booking-service`'s API contract as `openapi.yaml` (OpenAPI 3.0.3), covering `POST /api/v1/reservas` and `GET /api/v1/reservas/{reservaId}`, with request/response schemas and a standard error envelope (`code`, `message`, `details`, `trace_id`) applied consistently to `400`, `404`, and `409` responses.
- Wrote `versioning-policy.md`, defining backward-compatible vs. breaking changes separately for REST APIs (`/api/v1/...` prefix, add-optional-field-safe, remove/rename/retype-breaks) and for domain events (aligned with the schema evolution strategy already defined in `domain-events.md`).
- Defined the deprecation process for both REST and events: announce via changelog/`Sunset` header (REST) or dual-publishing during a migration window (events), with a minimum one-sprint overlap before retiring the old version.
- Identified the first consumer-driven contract to formalize: Payment Service as consumer of the `ReservaCreada` event published by Booking Service, since this is the most critical link in the Saga (a silent field rename here would directly cause the double-charge / no-charge failure mode the session warns about).
- Drafted the Pact consumer test structure for `payment-service` asserting the shape of the `ReservaCreada` payload (`reservaId`, `propiedadId`, `usuarioId`, `fechaInicio`, `fechaFin`, `montoTotal`, `estado`).
- Logged the two remaining pending contracts (`PagoAprobado`/`PagoRechazado` consumed by Booking, and `ReservaConfirmada`/`ReservaCancelada` consumed by Catalog) in `versioning-policy.md` as not-yet-implemented, for tracking.

## 3. Blockers and risks

- The Pact test for `ReservaCreada` is drafted but not yet wired into CI — the producer-side verification step in `booking-service`'s pipeline is not implemented yet, so a breaking payload change would not currently fail the build as intended.
- Two other consumer-driven contracts (Booking consuming Payment's events, Catalog consuming Booking's confirmation/cancellation events) remain undocumented and untested — only the highest-risk link (Payment) was prioritized this week.
- No event schema registry or AsyncAPI file exists yet for domain events; they are currently documented only as Markdown tables in `domain-events.md`, not as a machine-readable schema the way `openapi.yaml` is for REST.

## 4. Plan for next week

- Wire the `ReservaCreada` Pact verification into `booking-service`'s CI pipeline so a breaking change actually fails the build.
- Add the remaining two consumer-driven contracts (`PagoAprobado`/`PagoRechazado`, `ReservaConfirmada`/`ReservaCancelada`).
- Evaluate introducing an AsyncAPI schema file for domain events, to match the same machine-readable rigor already applied to `openapi.yaml`.

## 5. Compliance self-check

- [ ] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — not yet in place; team still works directly on `main`
- [x] Testable acceptance criteria — defined for HU-CONTRACT-003: a breaking change to ReservaCreada's payload must fail booking-service's CI build via the Pact verification step
- [ ] Tests added/updated (unit / integration) — Pact consumer test drafted, but producer-side verification not yet running in CI
- [x] DDD / hexagonal boundaries respected (domain has no I/O) — contract definitions and Pact tests live in the application/adapter layers, not inside domain entities
- [x] No secrets; config via environment variables — no credentials involved in this week's contract documentation work

## 6. Evidence links

- Not added yet
