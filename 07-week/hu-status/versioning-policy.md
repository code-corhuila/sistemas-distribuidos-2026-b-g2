# Versioning & Compatibility Policy — pms-properties

> Contracts are the single source of truth between services. This document defines how
> REST APIs and domain events evolve without silently breaking a consumer, per the
> contract-first and consumer-driven-testing principles adopted this sprint.

---

## REST APIs

- All endpoints are prefixed with a version: `/api/v1/...`.
- **Backward-compatible changes (stay in the same version):**
  - Add a new optional field to a request or response.
  - Add a new endpoint.
  - Add a new optional query parameter.
  - Add a new value to an enum, as long as consumers already tolerate unknown values.
- **Breaking changes (require a new version, e.g. `/api/v2/...`):**
  - Remove a field.
  - Rename a field.
  - Change a field's type.
  - Make a previously optional field required.
  - Change an existing error code's meaning.
- **Deprecation process:**
  1. Announce the deprecation in the changelog and add a `Sunset` HTTP header to the
     deprecated version's responses.
  2. Keep the old version running for at least one full sprint after the new version ships.
  3. Retire the old version only after confirming no consumer still calls it.

---

## Domain Events

- Every event envelope carries a `version` field (already defined in `domain-events.md`).
- **Backward-compatible changes (stay in `v1`):**
  - Add a new optional field to the `payload` (e.g. adding `cuponAplicado` to `ReservaCreada`).
  - Add a new event type.
  - Change a required payload field to optional.
- **Breaking changes (require a new version, e.g. `ReservaCreadaV2`):**
  - Remove a payload field.
  - Rename a payload field.
  - Change a payload field's type.
  - Change an optional field to required.
  - Change the event name itself.
- **Migration process** (as already defined in `domain-events.md` §Schema Evolution Strategy):
  1. Publish `EventNameV2` alongside the existing `EventNameV1` during the migration window.
  2. Migrate consumers to `V2` one by one.
  3. Announce deprecation of `V1` at least one sprint in advance.
  4. Stop publishing `V1` once no consumer depends on it.

---

## Standard error envelope (all REST APIs)

Every error response across every service uses this shape:

```json
{
  "error": {
    "code": "FECHAS_NO_DISPONIBLES",
    "message": "The requested dates overlap an existing booking",
    "details": {},
    "trace_id": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

| Field | Description |
|---|---|
| `code` | Stable, machine-readable error code — never changes meaning across the same API version |
| `message` | Human-readable description, safe to display or log |
| `details` | Optional object with extra context (e.g. which field failed validation) |
| `trace_id` | Correlates the error with `metadata.correlationId` from the Saga, for cross-service debugging |

---

## Consumer-driven contract testing (Pact)

Every asynchronous integration between two services must have at least one Pact test where the
**consumer** declares its expectation of the event payload, and the **producer** verifies that
pact in its own CI pipeline. A producer change that breaks a published pact fails the producer's
build — it never reaches the consumer as a silent runtime failure.

Current coverage:

| Consumer | Producer | Contract under test | Status |
|---|---|---|---|
| payment-service | booking-service | `ReservaCreada` event payload | Implemented (see `contracts/pact/reserva-creada-pact.md`) |
| booking-service | payment-service | `PagoAprobado` / `PagoRechazado` event payload | Pending |
| catalog-service | booking-service | `ReservaConfirmada` / `ReservaCancelada` event payload | Pending |

---

## Correlation with other documents

- Event payload definitions → `02-domain/domain-events.md`
- REST contract for booking-service → `07-api/contracts/openapi/booking-service.yaml`
- Consumer-driven Pact test → `07-api/contracts/pact/reserva-creada-pact.md`
