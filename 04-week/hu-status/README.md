<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       04-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 04

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brahiam Yara
- GITHUB_USER: BrayanYara1
- TEAM: Group 2
- SPRINT_GOAL: Retrospective (Aug 24-30): refine requirements, traceability, architecture, and data models.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-001 | User Registration - requirement and acceptance-criteria refinement | doing | [Requirements and architecture update](https://github.com/code-corhuila/appt-mgmt-docs/commit/f4dae481dc78766497e38a5e613cce5d81ccf4aa) |
| HU-002 | Login - requirement and acceptance-criteria refinement | doing | [Requirements and architecture update](https://github.com/code-corhuila/appt-mgmt-docs/commit/f4dae481dc78766497e38a5e613cce5d81ccf4aa) |
| HU-007 | Request Medical Appointment - requirement, traceability, and data-model refinement | doing | [Requirements and architecture update](https://github.com/code-corhuila/appt-mgmt-docs/commit/f4dae481dc78766497e38a5e613cce5d81ccf4aa) |

## 2. My individual contribution
- Refined the registration, login, and appointment-request stories and their acceptance criteria in the backlog.
- Updated non-functional requirements and the requirements traceability matrix.
- Revised the architecture overview, ADR material, and healthcare data-model documentation, including context/container diagrams.
- These are requirements/design deliverables. The linked commit does not establish that the implementation passes the HUs' full Definition of Done, so the statuses remain `doing`.

## 3. Blockers and risks
- No code/test blocker is recorded. The remaining delivery risk is that requirements and architecture updates alone do not verify implementation, review, staging deployment, or each HU's acceptance criteria.

## 4. Plan for next week
- Select the Corte 1 MVP scope and document discovery findings, UX/UI, and the technology-stack decision.
- Keep HU-001, HU-002, and HU-007 in progress until their implementation acceptance criteria are verified.

## 5. Compliance self-check
- [ ] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [ ] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [ ] No secrets; config via environment variables

Conventional-commit format, a per-HU environment PR, tests, runtime boundary checks, and configuration changes are not evidenced by this documentation-only commit; unchecked items are intentionally not claimed.

## 6. Evidence links
- [Revised requirements, traceability, architecture, and data models](https://github.com/code-corhuila/appt-mgmt-docs/commit/f4dae481dc78766497e38a5e613cce5d81ccf4aa)
