<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       08-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 08

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brahiam Yara
- GITHUB_USER: BrayanYara1
- TEAM: Group 2
- SPRINT_GOAL: Retrospective (Sep 21-27): specify API, authentication, and OpenAPI contracts for Salud Activa.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-001 | User Registration - API contract | doing | [API contracts and OpenAPI schemas](https://github.com/code-corhuila/appt-mgmt-docs/commit/394bf8c9cefe1fa865557a89e60d9ad2534c31d8) |
| HU-002 | Login - authentication contract | doing | [API contracts and authentication specification](https://github.com/code-corhuila/appt-mgmt-docs/commit/394bf8c9cefe1fa865557a89e60d9ad2534c31d8) |
| HU-007 | Request Medical Appointment - API contract | doing | [API contracts and OpenAPI schemas](https://github.com/code-corhuila/appt-mgmt-docs/commit/394bf8c9cefe1fa865557a89e60d9ad2534c31d8) |

## 2. My individual contribution
- Added REST guidelines, authentication documentation, API contracts, and OpenAPI schemas for the Salud Activa API.
- Refined the contract documentation and corrected the documented JWT algorithm/branch conventions in a follow-up change.
- The artifacts support registration, login, and appointment-request work, but do not by themselves prove that the implemented endpoints meet every acceptance criterion.

## 3. Blockers and risks
- No technical blocker is documented. Integration risk remains until the contracts are validated against deployed endpoint behavior and contract tests.

## 4. Plan for next week
- Validate the appointment flow and availability behavior with automated backend tests.
- Document the system context, containers, data model, and primary interaction sequences.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [ ] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [ ] No secrets; config via environment variables

The commits use `docs:` Conventional Commit subjects. The listed contract work is documentation rather than a test run; no HU-specific environment PR, contract-test execution, runtime boundary validation, or configuration/security review is evidenced for this week.

## 6. Evidence links
- [API contracts, REST guidelines, authentication, and OpenAPI schemas](https://github.com/code-corhuila/appt-mgmt-docs/commit/394bf8c9cefe1fa865557a89e60d9ad2534c31d8)
- [API documentation corrections](https://github.com/code-corhuila/appt-mgmt-docs/commit/24fe79fb697a86dee997d5e3b8309d7657e5892b)
