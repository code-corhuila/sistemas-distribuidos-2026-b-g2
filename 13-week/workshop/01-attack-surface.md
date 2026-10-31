# CP1 — Attack surface of Property

Sources: property-docs 05-architecture/overview.md, 05-architecture/deployment.md and the
OpenAPI contracts in 07-api/contracts/. My boundary, in red: **payment-api -> Stripe (external API)**.

```mermaid
flowchart LR
  subgraph TB1["TB1 Internet"]
      user([Guest / Host / Admin])
      front[property-front + 5 portals]
  end
  subgraph TB2["TB2 Property platform"]
      gw[property-api-gateway :8080]
      wf[property-workflow :3006]
      booking[property-booking-api :3001]
      catalog[property-catalog-api :3002]
      payment[property-payment-api :3003]
      identity[property-identity-api :3004]
      notif[property-notification-api :3005]
      worker[property-worker]
      mq[[RabbitMQ]]
      pg[(PostgreSQL 16: booking, payment, identity, notification, workflow)]
      mongo[(MongoDB 7: catalog)]
  end
  subgraph TB3["TB3 Third party"]
      stripe[(Stripe sandbox)]
  end
  user --> front
  front -->|HTTPS| gw
  gw -->|/api/v1/sagas| wf
  gw -->|/register /login /refresh /jwks| identity
  gw --> booking
  gw --> catalog
  gw --> payment
  gw --> notif
  wf -->|crear-reserva / confirmar| booking
  wf -->|cobrar / reembolso| payment
  payment -->|charge, refund| stripe
  worker -->|expire| booking
  booking -->|outbox| mq
  payment -->|outbox| mq
  mq --> notif
  mq --> catalog
  booking -->|booking_app| pg
  payment -->|payment_app| pg
  identity -->|identity_app| pg
  notif -->|notification_app| pg
  wf -->|workflow_app| pg
  catalog -->|catalog_app| mongo
  linkStyle 10 stroke:#d00,stroke-width:4px
```

## Assets of my boundary

| Asset | Where it lives | Classification |
|---|---|---|
| Stripe secret key | env file of payment-api (not versioned) | restricted |
| tokenPago (card token) | request from workflow; sent to Stripe; never stored or logged | restricted |
| montoCents of the charge | computed by booking-api, sent to Stripe | confidential |
| gateway_transaction_id | payment.payment | confidential |
| Idempotency key of the charge (<sagaId>:cobrar) | payment.idempotency_key and the Stripe request | internal |

## Entry points of my boundary

| Entry point | Who calls it | Authentication today |
|---|---|---|
| HTTPS call to the Stripe API (charge, refund) | payment-api | secret key in the Authorization header |
| Step cobrar from property-workflow | workflow -> payment-api | JWT with scope service |
| GET /api/v1/pagos/{id} (E-07) | front through the gateway | JWT; own Pago only, ADMIN or service read any |
