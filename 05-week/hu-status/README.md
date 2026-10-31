<!-- HU-STATUS TEMPLATE - do NOT remove the <!-- ... --> markers or the table headers.

     Your weekly grade is read AUTOMATICALLY from this file:
       05-week/hu-status/README.md  (inside YOUR fork). English. -->

# Weekly Status - Week 05

<!-- CONFIG-START - must match your profile repo (username/username) CONFIG -->

- FULL_NAME: Juan Esteban Oliveros Duran
- GITHUB_USER: JuanOliveros2497
- TEAM: pms-properties
- SPRINT_GOAL: Containerize the three MVP1 microservices (booking-service, payment-service, catalog-service) with multi-stage Dockerfiles and a shared docker-compose.yml, running against real databases with configuration via environment variables.
<!-- CONFIG-END -->

## 1. User stories worked this week

| HU ID        | Title                                                                                           | Status (todo/doing/done) | Evidence (PR or commit URL) |
| ------------ | ----------------------------------------------------------------------------------------------- | ------------------------ | --------------------------- |
| HU-INFRA-001 | Containerize booking-service, payment-service, and catalog-service with multi-stage Dockerfiles | done                     | Not added yet               |
| HU-INFRA-002 | Create docker-compose.yml orchestrating all services and their databases on a shared network    | done                     | Not added yet               |
| HU-INFRA-003 | Externalize configuration via .env / .env.example and secure secrets with .gitignore            | done                     | Not added yet               |

## 2. My individual contribution

- Wrote the multi-stage `Dockerfile` for `booking-service`, `payment-service`, and `catalog-service` (Maven build stage + lightweight JRE runtime stage).
- Wrote the root `docker-compose.yml`, orchestrating three microservices and their databases (PostgreSQL for Booking and Payment, MongoDB for Catalog) on a shared Docker network, with named volumes for data persistence.
- Created `.env.example` as the configuration template and `.gitignore` to prevent secrets from being committed.
- Fixed structural issues found during review: moved `docker-compose.yml` to the repository root (it was incorrectly nested inside `booking-service/`), and corrected the `.dockerignore` filename (was misnamed `docker.dockerignore`).
- Updated `README.md` with setup instructions (`.env` setup, `docker-compose up`, service health endpoints, teardown).

## 3. Blockers and risks

- Services are containerized but not yet verified end-to-end against real databases (pending a full `docker-compose up` run and `/health` check for all three services).
- Database credentials in `.env.example` are placeholders; real values still need to be agreed upon and shared securely with the team (not via the repo).
- `.dockerignore` per service is duplicated across `booking-service/`, `payment-service/`, and `catalog-service/` — could be simplified later, not a blocker for MVP1.

## 4. Plan for next week

- Run `docker-compose up --build` and validate that all three services start correctly and respond on their `/health` endpoints against real databases.
- Finalize the MVP1 API contract (openapi.yaml) and wire the first vertical slice (HU-BOOK-001) on top of this containerized base.
- Add evidence links (PRs/commits) once the containerization changes are pushed to GitHub.

## 5. Compliance self-check

- [ ] Conventional Commits - `type(scope): summary`
- [ ] Per-environment HU branch + PR to that environment (hu-xxx-dev -> develop, ...) — N/A, work done directly on `main` this week
- [ ] Testable acceptance criteria — N/A, infrastructure setup, not yet tied to a testable business HU
- [ ] Tests added/updated (unit / integration) — N/A, no application code changed this week
- [ ] DDD / hexagonal boundaries respected (domain has no I/O) — N/A, purely infrastructure/containerization work
- [x] No secrets; config via environment variables — all DB credentials externalized via `.env` / `.env.example`, `.env` excluded via `.gitignore`

## 6. Evidence links

- Not added yet
