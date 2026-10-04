<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       09-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 09

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Brahiam Yara
- GITHUB_USER: BrayanYara1
- TEAM: Group 2
- SPRINT_GOAL: Retrospective (Sep 28-Oct 04): add appointment-route test coverage/CI and document system UML diagrams.
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| HU-002 | Login - sequence flow documented | doing | [UML diagrams](https://github.com/code-corhuila/appt-mgmt-docs/commit/ff3c4530583a96c7d90c9d8a453c7d4e5896c0fe) |
| HU-007 | Request Medical Appointment - availability tests, CI, and sequence flow | doing | [Merged appointment-test PR](https://github.com/BrayanYara1/ProyectoDistribuidos2026/pull/1); [UML diagrams](https://github.com/code-corhuila/appt-mgmt-docs/commit/ff3c4530583a96c7d90c9d8a453c7d4e5896c0fe) |
| HU-008 | Medication Management - data relationships documented | doing | [Healthcare data model](https://github.com/code-corhuila/appt-mgmt-docs/commit/ff3c4530583a96c7d90c9d8a453c7d4e5896c0fe) |
| HU-011 | Store Medical Studies - data relationships documented | doing | [Healthcare data model](https://github.com/code-corhuila/appt-mgmt-docs/commit/ff3c4530583a96c7d90c9d8a453c7d4e5896c0fe) |
| HU-014 | Integrated Chat - message data relationship documented | doing | [Healthcare data model](https://github.com/code-corhuila/appt-mgmt-docs/commit/ff3c4530583a96c7d90c9d8a453c7d4e5896c0fe) |

## 2. My individual contribution
- Added automated tests for appointment availability, including missing-input and available-slot behavior, and introduced backend CI/coverage configuration in a PR that was merged.
- Documented the context and container architecture, healthcare data relationships (including medication, study, and chat entities), and login/appointment sequences.
- HU-007 remains `doing`: the PR covers selected availability paths, not all scheduling acceptance criteria or concurrent reservation behavior.
- HU-002, HU-008, HU-011, and HU-014 remain `doing`: their evidence this week is a sequence or data-model diagram, not completed product behavior.

## 3. Blockers and risks
- Appointment creation checks availability and then saves separately; the available implementation evidence does not establish atomic reservation under concurrent requests.
- The CI workflow and tests provide some regression coverage but do not establish coverage of every API flow or deployment environment.

## 4. Plan for next week
- Add integration/edge-case coverage for appointment creation, cancellation, and concurrent requests.
- Validate the other HU acceptance criteria against implemented behavior; update the diagrams when architecture or data ownership changes.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [ ] DDD / hexagonal boundaries respected (domain has no I/O)
- [ ] No secrets; config via environment variables

The backend-test PR is merged, but it used a feature branch rather than the course's `hu-xxx-main` branch naming pattern. HU-007 has testable availability criteria and the PR adds tests; unverified architectural/security checks are intentionally left unchecked.

## 6. Evidence links
- [Merged PR: appointment availability tests and backend CI](https://github.com/BrayanYara1/ProyectoDistribuidos2026/pull/1)
- [Salud Activa UML diagrams](https://github.com/code-corhuila/appt-mgmt-docs/commit/ff3c4530583a96c7d90c9d8a453c7d4e5896c0fe)
- [HU-007 requirements and acceptance criteria](https://github.com/code-corhuila/appt-mgmt-docs/blob/main/04-requirements/user-stories.md)
