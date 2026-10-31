<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       09-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 09

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Realign the domain documentation (contexts, events, entities and invariants) with the orchestrated Saga introduced by ADR-009, ADR-013 and ADR-014 — replacing the choreographed, event-driven Saga design with `property-workflow` (REST orchestrator) and `property-worker` (expiry job) — and with the single-database-instance-per-engine rule of ADR-008.
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID         | Title                                                                                                                                         | Status (todo/doing/done) | Evidence (PR or commit URL)                            |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------ |
| HU-DOMAIN-001 | Align `domain-map.md` and `domain-events.md` with the orchestrated Saga (contexts, consumers, Saga diagram, idempotency by `Idempotency-Key`) | doing                    | https://github.com/code-corhuila/property-docs/pull/56 |
| HU-DOMAIN-002 | Align `entities-and-rules.md` invariants (INV-004, INV-005) with the orchestrated Saga; model the new `Reembolso` entity and INV-006          | doing                    | https://github.com/code-corhuila/property-docs/pull/58 |

## 2. My individual contribution

- Realigned `02-domain/domain-map.md` and `02-domain/domain-events.md` (PR #56, 272 changed lines) with the orchestrated Saga: each Bounded Context's "Database" row now shows its schema in the single PostgreSQL/MongoDB instance per ADR-008 (not a dedicated instance), the context map was redrawn with `property-workflow` and `property-worker` as transversal orchestration components (not Bounded Contexts), and the Relationships Table now shows `property-workflow` as an Open Host Service consumer of Booking's and Payment's REST APIs rather than Booking and Payment exchanging events directly.
- Updated the Trigger/Consumers of all six domain events to match ADR-013: `ReservaCreada` is now consumed only by Catalog (not Payment), `PagoAprobado`/`PagoRechazado` have no consumer in MVP 1 (published only for ledger traceability, since the workflow reads the result directly from the `POST /pagos` response), and `ReservaExpirada` is triggered by `property-worker`'s scheduled job instead of an internal booking-service timer. Set `causationId` to `null` in every example, since no event is caused by a prior event anymore — every trigger is now an HTTP call.
- Realigned `02-domain/entities-and-rules.md` (PR #58, 160 changed lines): INV-004 (no duplicate charges) now keys off the `Idempotency-Key` of the Saga's `cobrar` step instead of the `ReservaCreada` event's `eventId`, since Payment no longer consumes that event; `Pago.processedEventId` becomes `Pago.idempotencyKey`. Made repeated transitions on a `Reserva` (e.g. `cancelar()` on an already-`CANCELADA` reservation) a no-op instead of a violation, since the workflow's compensations and the worker's job can legitimately run more than once.
- Modeled the new `Reembolso` entity and invariant INV-006 (a refund is a new, immutable ledger entry that reverses exactly one approved `Pago`, never edits it), required because ADR-009 defines `POST /pagos/{id}/reembolsos` as the compensation for a failed `confirmar-reserva` step and nothing in the domain previously said how that refund should be recorded.
- Updated the stack references in `entities-and-rules.md` to match ADR-011: Java 21 (from 17), three Maven modules per service (`<domain>-core` with zero Spring dependency for domain/application layers), and the package root `co.edu.corhuila.property.<domain>` (from `com.pmsproperty`).
- Fixed a Markdown formatting bug in both files: each began with an unclosed code fence, which rendered the entire title and table of contents as a code block.
- Split what the plan originally scoped as one PR into two (#56 / #58) to stay under the project's 400-changed-line PR limit, since `domain-map.md` + `domain-events.md` + `entities-and-rules.md` together exceeded it; the two are independent and can be reviewed/merged in any order.

## 3. Blockers and risks

- Both PRs (#56, #58) are open, awaiting review — not yet merged. Until #58 merges, a reviewer looking only at #56 sees `domain-events.md` referencing `Idempotency-Key` semantics that `entities-and-rules.md` only formalizes in the second PR.
- This realignment is a dependency for four follow-up PRs already identified in the issue bodies (PR-12, PR-13, PR-15, PR-18): rewriting `06-data`'s booking/payment models, rewriting catalog/identity/notification models, adding the workflow's REST contract to `07-api`, and redrawing `08-uml`'s diagrams for the orchestrated Saga. None of those are started yet.
- Prior deliverables already submitted this corte — `06-data`'s four documents, `07-api/guidelines.md`'s error taxonomy, and `08-uml`'s Saga sequence diagrams — were built for the choreographed-Saga/database-per-service design and are now inconsistent with ADR-008/009/013/014.

## 4. Plan for next week

- Get #56 and #58 reviewed and merged.
- Rewrite `06-data`'s booking and payment models around `idempotency_key` and the single-instance schema layout (PR-12), and the catalog/identity/notification models (PR-13).
- Add the workflow's REST contract (`property-workflow`'s Saga steps, `property-worker`'s expiry endpoint) to `07-api` (PR-15), and reconcile it with the error-taxonomy decisions from `07-api/guidelines.md`.
- Redraw `08-uml`'s C2 container diagram and Saga sequence diagrams for the orchestrated flow (PR-18) — the current `seq-saga-booking-payment.md` and `seq-saga-expiration.md` assume the old choreographed design.

## 5. Compliance self-check

- [x] Conventional Commits - `type(scope): summary` — both commits use `docs(domain): ...`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — not applicable: this repo uses `docs/<topic>` branches merging directly to `main`, with an issue (`Closes #NN`) driving each PR instead of per-environment branches
- [x] Testable acceptance criteria — both issues state explicit, checkable acceptance criteria (e.g. "The Consumers row of each of the six events matches the table of ADR-013"; "Repeating a transition a `Reserva` is already in is not an error")
- [ ] Tests added/updated (unit / integration) — N/A, no code implemented yet
- [x] DDD / hexagonal boundaries respected (domain has no I/O) — explicitly the subject of this week's work: `Reserva` and `Pago` stay separate aggregates never sharing a transaction, and the module split (`<domain>-core` with zero Spring dependency) is documented for every entity touched
- [x] No secrets; config via environment variables — no credentials involved, documentation-only work

## 6. Evidence links

- PR #56 — `docs(domain): align contexts and events with the orchestrated saga` — https://github.com/code-corhuila/property-docs/pull/56
- PR #58 — `docs(domain): align entities and invariants with the orchestrated saga` — https://github.com/code-corhuila/property-docs/pull/58
