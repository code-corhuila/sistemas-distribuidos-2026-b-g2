<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.
     Your weekly grade is read AUTOMATICALLY from this file:
       13-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 13

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->
- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: Group 2 — Property
- SPRINT_GOAL: Threat model of the boundary payment-api -> Stripe (external API) and turn its top risks into security stories for the team backlog
<!-- CONFIG-END -->

## 1. User stories worked this week
| HU ID | Title | Status (todo/doing/done) | Evidence (PR or commit URL) |
|---|---|---|---|
| #167 | Threat model: payment-api -> Stripe (external API) | done | https://github.com/code-corhuila/property-docs/pull/177 |
| #178 | [security] The Stripe key and tokenPago never leak | todo | https://github.com/code-corhuila/property-docs/issues/178 |
| #179 | [security] A Pago is read only by its owner | todo | https://github.com/code-corhuila/property-docs/issues/179 |
| #180 | [security] Stripe slowness does not stop the platform | todo | https://github.com/code-corhuila/property-docs/issues/180 |

## 2. My individual contribution
- Attack surface map of Property with its trust boundaries, and my boundary payment-api -> Stripe (external API): https://github.com/JuanOliveros2497/sistemas-distribuidos-2026-b-g2/blob/main/13-week/workshop/01-attack-surface.md
- STRIDE analysis with risk ranking, residual risk and the library book [B], updated after the peer review: https://github.com/code-corhuila/property-docs/pull/177
- Three security stories in the team backlog: #178, #179, #180
- Security CI proposal (secret scan, dependency audit, negative test) with the real output of the test: https://github.com/JuanOliveros2497/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop/04-security-ci

## 3. Blockers and risks
- The CI of the code-corhuila organization does not start (billing lock), so the security workflow is a proposal in my fork, run by hand.

## 4. Plan for next week
- Implement the highest-priority story of my boundary in batch 2 of the code.
- Move the negative test of CP8 into the team repository with its pull request.

## 5. Compliance self-check
- [x] Conventional Commits - `type(scope): summary`
- [x] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...)
- [x] Testable acceptance criteria
- [x] Tests added/updated (unit / integration)
- [x] DDD / hexagonal boundaries respected (domain has no I/O)
- [x] No secrets; config via environment variables

## 6. Evidence links
- Workshop folder: https://github.com/JuanOliveros2497/sistemas-distribuidos-2026-b-g2/tree/main/13-week/workshop
- Claim issue: https://github.com/code-corhuila/property-docs/issues/167
- STRIDE pull request and its commits: https://github.com/code-corhuila/property-docs/pull/177/commits
- Stories: https://github.com/code-corhuila/property-docs/issues/178, https://github.com/code-corhuila/property-docs/issues/179, https://github.com/code-corhuila/property-docs/issues/180
- Review comment I left: https://github.com/code-corhuila/property-docs/pull/181#issuecomment-6514101748
- Review received and my answer: https://github.com/code-corhuila/property-docs/pull/177
- Commits of the workshop in my fork: https://github.com/JuanOliveros2497/sistemas-distribuidos-2026-b-g2/commits/main/13-week
- Reflection document: https://docs.google.com/document/d/1FupeNr60jcdsy9oYW_i8IMBirSY7U0ZSBgyE5MiY_vY/edit?hl=es&tab=t.0
