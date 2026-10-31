<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       08-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 08

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Mature the project's documentation contracts across three fronts — close the remaining 06-data design decisions, add the UML diagram set (C4, sequence, state, ER) to 08-uml, and formalize the REST API's error-body taxonomy in 07-api — so downstream implementation work has nothing left to invent.
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID       | Title                                                                                                                            | Status (todo/doing/done) | Evidence (PR or commit URL)                                                 |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------ | --------------------------------------------------------------------------- |
| HU-DATA-001 | Complete the four missing 06-data documents: modeling conventions, data dictionary, migration strategy, normalization assessment | done                     | https://github.com/code-corhuila/property-docs/pull/20                      |
| HU-UML-001  | Add the diagram registry and C4 architecture diagrams (system context, container, bounded-context map) to 08-uml                 | doing                    | TODO: paste real PR URL for branch `docs/uml-c4-diagrams`                   |
| HU-UML-002  | Add sequence diagrams (login, booking-payment saga, expiration) to 08-uml                                                        | todo                     | TODO: confirm branch/PR status                                              |
| HU-UML-003  | Add the Reserva lifecycle state diagram to 08-uml                                                                                | todo                     | TODO: confirm branch/PR status                                              |
| HU-UML-004  | Add ER diagrams for booking, payment, identity and notification services to 08-uml                                               | todo                     | TODO: confirm branch/PR status                                              |
| HU-API-001  | Formalize REST guidelines and the three-shape error-body taxonomy in 07-api/guidelines.md                                        | doing                    | TODO: paste real PR URL for branch `docs/api-guidelines-and-error-taxonomy` |

## 2. My individual contribution

- Completed the four documents `06-data/README.md` listed as missing: `modeling-conventions.md` (naming, identifiers, date/money handling, delete policy), `data-dictionary.md` (meaning and possible values of every field per service), `migration-strategy.md` (Flyway policy, forward-only migrations, expand/contract changes on live data) and `normalization-assessment.md` (normal-form check per table, register of 11 intentional denormalizations, 5 open design points with a suggested owner each).
- Designed and wrote the full `08-uml` diagram set: a registry (`diagram-index.md`) plus 11 Mermaid diagrams — 3 architecture (C4 System Context, C4 Container, DDD Bounded-Context Map), 3 sequence (login, the booking→payment Saga with both outcomes, the 15-minute expiration path), 1 state diagram (`Reserva` lifecycle) and 4 ER diagrams (one per relational service). Split across 4 planned PRs to keep each PR-diffable and under the project's ~400-line PR guideline.
- Wrote `07-api/guidelines.md`, closing 6 REST decisions (D-C1 to D-C6: URI versioning, endpoint naming, mandatory pagination, date-range validation, and — the core of the contribution — formalizing that the error response has **three distinct shapes** instead of one generic schema, plus a status-code-to-shape mapping table). This formalized a pattern a teammate's already-merged `booking-service.yaml` was already using informally (`INV_001_OVERLAPPING_DATES`) without it being documented anywhere as a project-wide rule. Logged 8 open gaps with a suggested owner, including two concrete corrections needed in the already-merged `booking-service.yaml` and `_shared.yaml`.
- Reviewed the professor's `api-contract.md` reference example (published in the course repo, `08-week/02-session/spec/`) against what was submitted, and identified that the reference is an audit of an already-implemented, running system (verified via curl probes), while this project has no code yet — so the same evidentiary rigor (endpoint "fichas" with live-tested request/response pairs) isn't yet achievable and is called out as a gap rather than faked.

## 3. Blockers and risks

- Three of the four planned 08-uml PRs (sequence, state, ER diagrams) were prepared but their branch/push/PR steps were not confirmed executed this week.
- The `07-api/guidelines.md` and `08-uml` (`docs/uml-c4-diagrams`) PRs are pushed but not yet confirmed merged/approved — evidence links above are placeholders pending the real PR URLs.
- `07-api/guidelines.md`'s core contribution (the `context` field needed for the third error shape) requires editing `_shared.yaml`, a file shared by every contract; that edit was deliberately left as a follow-up with an owner instead of being applied directly, to avoid touching a teammate's already-merged file without coordinating first.
- No code exists yet for any microservice, so none of this week's decisions have been validated against a running system — only against the written domain and architecture docs.

## 4. Plan for next week

- Push and open PRs for the remaining `08-uml` diagrams (sequence, state, ER), and confirm merge status for all four `08-uml` PRs and the `07-api/guidelines.md` PR.
- Apply the two corrections `guidelines.md` flagged for `booking-service.yaml` (the `/api/v1/...` URL prefix and the missing `400` case for `fechaInicio < fechaFin`), and add the `context` field to `_shared.yaml`'s `ErrorResponse` schema.
- Once `identity-service.yaml` and a payment-service REST decision exist, add endpoint "fichas" (concrete request/response examples per endpoint) to `07-api`, closer to the professor's reference format, clearly labeled as contract-level rather than live-verified until a service is actually implemented.

## 5. Compliance self-check

- [x] Conventional Commits - `type(scope): summary` — all commits this week followed `docs(data): ...`, `docs(uml): ...`, `docs(api): ...`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — not applicable: this is a documentation-only repo, and `00-governance/branching-policy.md` defines `docs/<topic>` branches merging directly to `main`, not per-environment branches
- [ ] Testable acceptance criteria — not formally written this week; the work was documentation (data model, diagrams, API guidelines), not a user-facing feature with testable AC
- [ ] Tests added/updated (unit / integration) — N/A, no service is implemented yet
- [x] DDD / hexagonal boundaries respected (domain has no I/O) — the API error-code convention (`INV_<NNN>_<DESC>`) and the ER diagrams both explicitly derive from, and stay consistent with, the domain invariants in `02-domain/entities-and-rules.md` rather than inventing new ones
- [x] No secrets; config via environment variables — no credentials involved in this week's documentation work

## 6. Evidence links

- 06-data: PR #20, `docs(data): add additional-data-documentation` (merged)
- 08-uml: PR for `docs/uml-c4-diagrams` — TODO: paste real URL
- 07-api: PR for `docs/api-guidelines-and-error-taxonomy` — TODO: paste real URL
