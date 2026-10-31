<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       06-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 06

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Harden the local orchestration of the three microservices with Docker Compose (real healthchecks, deterministic startup order, per-environment overrides), and plan the environment strategy, configuration matrix, and branch-to-environment mapping for MVP2.
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID        | Title                                                                                              | Status (todo/doing/done) | Evidence (PR or commit URL) |
| ------------ | -------------------------------------------------------------------------------------------------- | ------------------------ | --------------------------- |
| HU-INFRA-004 | Add healthchecks to all databases (booking-db, payment-db, catalog-db)                             | done                     | Not added yet               |
| HU-INFRA-005 | Add healthchecks to all microservices and gate startup with depends_on: condition: service_healthy | done                     | Not added yet               |
| HU-INFRA-006 | Split configuration into docker-compose.override.yml (dev) and compose.prod.yml (prod)             | done                     | Not added yet               |
| HU-INFRA-007 | Add curl to each service's runtime image to support HTTP healthchecks                              | done                     | Not added yet               |
| HU-ORQ-001   | All services start with a single docker compose up gated by healthchecks                           | done                     | Not added yet               |
| HU-ORQ-002   | Configuration is read from the environment in every service (no hardcoded values)                  | doing                    | Not added yet               |
| HU-ORQ-003   | QA environment runs the same images as development, only configuration differs                     | todo                     | Not added yet               |
| HU-ORQ-004   | Documented configuration matrix (variable names + values per environment) added to the repo        | doing                    | Not added yet               |
| HU-ORQ-005   | Each service validates required environment variables at startup                                   | todo                     | Not added yet               |

## 2. My individual contribution

- Updated `docker-compose.yml` to add real healthchecks for each database (`pg_isready` for PostgreSQL, `mongosh` ping for MongoDB) and changed `depends_on` to `condition: service_healthy` for all three microservices, eliminating the previous race condition between "container started" and "database actually ready".
- Added HTTP healthchecks to `booking-service`, `payment-service`, and `catalog-service` against their `/health` endpoint, and updated each `Dockerfile` to install `curl` in the runtime stage.
- Created `docker-compose.override.yml` (development) and `compose.prod.yml` (production) to separate per-environment configuration from the base compose file, following the "build once, promote the artifact" principle.
- Defined the three environments for the project (develop, qa, prod) and drafted a configuration matrix documenting variable names (`SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`, `SPRING_PROFILES_ACTIVE`, `LOG_LEVEL`) that stay consistent across environments, with only their values changing per environment.
- Reviewed the current branching model (everything committed directly to `main`) against the expected per-environment branch flow (`hu-xxx-dev` → `develop`, `hu-xxx-qa` → `qa`, `hu-xxx-main` → `main`), and flagged this as a gap to close before MVP2.
- Broke down the MVP2 orchestration work into five testable user stories (HU-ORQ-001 to HU-ORQ-005) covering healthcheck-gated startup, environment-based configuration, image promotion across environments, a documented configuration matrix, and startup-time validation of required variables.

## 3. Blockers and risks

- The team currently works directly on `main` with no `develop`/`qa` branches — this does not yet match the per-environment branch-to-environment mapping expected for MVP2, and will require a process change communicated to the whole team.
- QA and production environments (databases, hosts, secret storage) are not provisioned yet — the configuration matrix is defined on paper, but there is nothing to promote the image to outside of local development.
- No secret manager (Vault, AWS Secrets Manager, etc.) has been chosen yet for qa/prod; secrets currently only have a local `.env` workflow defined.
- `/health` endpoints for `payment-service` and `catalog-service` are still pending, which blocks validating HU-ORQ-001 end-to-end for those two services.

## 4. Plan for next week

- Provision a QA environment (even a minimal one) and validate that the exact same Docker image built for development runs there with only configuration changes (HU-ORQ-003).
- Add startup-time validation for required environment variables in each service, so missing configuration fails fast with a clear error (HU-ORQ-005).
- Introduce `develop` and `qa` branches and align the team's Git workflow with the per-environment branch model.
- Finalize and commit the configuration matrix document (`config-matrix.md`) to the repo, keeping it in sync with `.env.example`.

## 5. Compliance self-check

- [ ] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — not yet in place; identified as a gap this week, still working directly on `main`
- [x] Testable acceptance criteria — defined for all five HU-ORQ stories (e.g. HU-ORQ-001: `docker-compose up --build` starts databases first, waits for healthy, then starts services)
- [ ] Tests added/updated (unit / integration) — N/A, infrastructure/orchestration and planning work, no application code changed
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) — N/A, purely Docker Compose / infrastructure and environment planning work
- [x] No secrets; config via environment variables — configuration matrix confirms variable names stay consistent across environments while values are injected per environment, never hardcoded

## 6. Evidence links

- Not added yet
