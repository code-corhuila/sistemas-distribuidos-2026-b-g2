<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       03-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 03

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brahiam Yara
- GITHUB_USER: BrayanYara1
- TEAM: Group 2
- SPRINT_GOAL: Retrospective (Aug 17-23): establish Salud Activa context, MVP 1.0 story breakdown, and the Turnos domain model.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-007 | Request Medical Appointment - Turnos domain model, invariants, and events | doing | [Domain-model commit](https://github.com/BrayanYara1/ProyectoDistribuidos2026/commit/614d401aa0e25085f1c89ab3a2965959f96449ec) |

The HU-007 mapping is retrospective: the Aug 17 domain-model artifact predates the current HU numbering. `doing` records domain/design progress only; it does not claim the full appointment feature is complete.

## 2. My individual contribution
- Documented the Salud Activa system context and candidate architecture, and recorded ADR-001 and the initial MVP 1.0 backlog.
- Modeled Turnos as a domain context, including its aggregate root, entities, invariants, and domain events.
- Defined MVP data ownership and access-control boundaries in the planning artifact.
- This was analysis and modeling work. No deployed booking feature or completed HU is claimed.

## 3. Blockers and risks
- The artifacts are planning/domain-design deliverables; the available evidence does not show implementation, runtime validation, or a test run for the modeled appointment rules.

## 4. Plan for next week
- Refine the backlog into testable acceptance criteria and align the architecture and data model with the modeled Turnos rules.
- Validate the planned boundaries against the application implementation before marking any feature HU done.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [ ] No secrets; config via environment variables

The backlog and domain-planning artifacts use Given/When/Then acceptance criteria and conventional `docs:` commit subjects. No per-HU environment PR, implementation test, or runtime validation is evidenced for this week.

## 6. Evidence links
- [MVP 1.0 story breakdown and data ownership](https://github.com/BrayanYara1/ProyectoDistribuidos2026/commit/cc7cd39c4eb2ca7210aca5717c9603fd280a07bf)
- [Context map, ADR-001, and MVP backlog](https://github.com/BrayanYara1/ProyectoDistribuidos2026/commit/7ea77a08f16e9e92e2adb0aea8283f131de2456d)
- [Project context/domain documentation update](https://github.com/code-corhuila/appt-mgmt-docs/commit/f323b2bc6d43a4145c19eb2735dd5c42471251b1)
- [Turnos context model: aggregate, invariants, and events](https://github.com/BrayanYara1/ProyectoDistribuidos2026/commit/614d401aa0e25085f1c89ab3a2965959f96449ec)
