# Configuration Matrix — pms-properties

> Same built image runs in every environment; only configuration changes.
> Variable **names** stay identical across environments — only their **values** differ.
> Secrets are never committed; they are injected per environment (local `.env`, CI secrets, or a vault).

---

## Environments

| Environment | Purpose | Characteristics |
|---|---|---|
| **develop** | Daily development, fast and disposable | Local containers, test data, can be destroyed and recreated anytime |
| **qa** | Production-like environment for integration testing | Same image as development, controlled test data, used to validate the full Saga flow end-to-end |
| **prod** | Real users | Same image already validated in QA, real credentials, defined resource limits, no test data |

---

## booking-service

| Variable | develop | qa | prod |
|---|---|---|---|
| `SPRING_DATASOURCE_URL` | `jdbc:postgresql://booking-db:5432/booking_dev` | `jdbc:postgresql://qa-booking-db:5432/booking_qa` | `jdbc:postgresql://prod-booking-db:5432/booking` |
| `SPRING_DATASOURCE_USERNAME` | `${BOOKING_DB_USER}` (local `.env`) | `${BOOKING_DB_USER}` (CI-injected) | `${BOOKING_DB_USER}` (vault) |
| `SPRING_DATASOURCE_PASSWORD` | `${BOOKING_DB_PASSWORD}` (local `.env`) | `${BOOKING_DB_PASSWORD}` (CI-injected) | `${BOOKING_DB_PASSWORD}` (vault) |
| `SPRING_PROFILES_ACTIVE` | `dev` | `qa` | `prod` |
| `LOG_LEVEL` | `debug` | `info` | `warn` |

## payment-service

| Variable | develop | qa | prod |
|---|---|---|---|
| `SPRING_DATASOURCE_URL` | `jdbc:postgresql://payment-db:5432/payment_dev` | `jdbc:postgresql://qa-payment-db:5432/payment_qa` | `jdbc:postgresql://prod-payment-db:5432/payment` |
| `SPRING_DATASOURCE_USERNAME` | `${PAYMENT_DB_USER}` (local `.env`) | `${PAYMENT_DB_USER}` (CI-injected) | `${PAYMENT_DB_USER}` (vault) |
| `SPRING_DATASOURCE_PASSWORD` | `${PAYMENT_DB_PASSWORD}` (local `.env`) | `${PAYMENT_DB_PASSWORD}` (CI-injected) | `${PAYMENT_DB_PASSWORD}` (vault) |
| `SPRING_PROFILES_ACTIVE` | `dev` | `qa` | `prod` |
| `LOG_LEVEL` | `debug` | `info` | `warn` |

## catalog-service

| Variable | develop | qa | prod |
|---|---|---|---|
| `SPRING_DATA_MONGODB_URI` | `mongodb://${CATALOG_DB_USER}:${CATALOG_DB_PASSWORD}@catalog-db:27017/catalog_dev?authSource=admin` | `mongodb://${CATALOG_DB_USER}:${CATALOG_DB_PASSWORD}@qa-catalog-db:27017/catalog_qa?authSource=admin` | `mongodb://${CATALOG_DB_USER}:${CATALOG_DB_PASSWORD}@prod-catalog-db:27017/catalog?authSource=admin` |
| `SPRING_PROFILES_ACTIVE` | `dev` | `qa` | `prod` |
| `LOG_LEVEL` | `debug` | `info` | `warn` |

---

## Secrets policy

- No credential value ever appears in this file, in `docker-compose.yml`, `docker-compose.override.yml`, or `compose.prod.yml` — only variable **names**.
- Local development: values live in `.env` (git-ignored); `.env.example` documents the required names with placeholder values.
- QA: values injected via the CI/CD pipeline's secret store.
- Production: values injected via a secrets manager (Vault / AWS Secrets Manager / equivalent) — not yet provisioned, tracked as a pending item.

---

## Branch ↔ Environment mapping

| Branch | Target environment | Rule |
|---|---|---|
| `hu-xxx-dev` | develop | PR to `develop`; validated there first |
| `hu-xxx-qa` | qa | Only after validation in develop, PR to `qa` |
| `hu-xxx-main` | prod (main) | Only after passing qa, PR to `main` |

> **Status:** Not yet implemented. The team currently commits directly to `main` for all changes.
> Introducing `develop` and `qa` branches is a pending decision before MVP2.

---

## Open items

- QA and production database instances are not provisioned yet — this matrix is defined ahead of infrastructure.
- No secrets manager has been selected for qa/prod.
- Startup-time validation of required environment variables (fail fast on missing config) is not yet implemented in any service.
