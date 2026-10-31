# CP7 · Alert policy for the search

The rules in `06-alerts.yml` look at how fast we spend the CP6 budgets, using two
windows each: the long one proves it is not a blip, the short one proves it is still
happening (so the alert also clears soon after a fix).

## What each alert costs before it fires

SLO A budget: 60 failed searches or 43.2 min per 30 days (720 hours).

- **`CatalogSearchFastBurn` (page)** — burn rate 14.4 over 1 h, confirmed over 5 min.
  14.4 × 1 / 720 = **2 % of the monthly budget** is gone when it fires:
  2 % of 60 = **1.2 failed searches**, 2 % of 43.2 = **0.86 minutes**. At this speed the
  whole budget lasts 720 / 14.4 = 50 hours.
- **`CatalogSearchSlowBurn` (ticket)** — burn rate 6 over 6 h, confirmed over 30 min.
  6 × 6 / 720 = **5 %**: **3 failed searches**, **2.16 minutes**. The budget would last
  5 days, so it can wait for working hours.
- **`CatalogAvailabilityStale` (ticket)** — SLO C, burn rate 6 over 6 h and 30 min.
  5 % of the freshness budget: **6 late events** of 120, **21.6 minutes** of 432.

SLO B (latency) has no alert of its own: with a 5 % budget and searches that are mostly
under 100 ms, a slow Mongo shows first as timeouts, which SLO A already catches. We
will add it if the drill (CP9) proves us wrong.

The fast alert pages because search is the door of the product: if it fails, nobody
reaches "Reservar". Searches are about 80 per hour, so 1.44 % means at least one or two
failures in an hour — a real signal, not a single unlucky request.

## Alerts we decided NOT to create

1. **MongoDB connections above 80 %.** `mongodb_connections{state="current"}` can be
   high during a normal peak while every search still answers in 50 ms. If the pool is
   really exhausted, searches time out and `CatalogSearchFastBurn` fires with the
   guest's point of view. We keep it in the dashboard.
2. **RabbitMQ queue `catalog.reservas` above 100 messages.** A burst after Booking comes
   back from a deploy fills the queue for a minute and drains by itself. What matters is
   whether the guest sees stale dates for too long, and that is exactly
   `CatalogAvailabilityStale` (lag over 60 s), not the queue size.
