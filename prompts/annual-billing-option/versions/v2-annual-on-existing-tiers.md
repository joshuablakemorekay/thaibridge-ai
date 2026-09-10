# v2 — annual on the existing tiers

The instruction after the premise was corrected.

```
For 1. Pricing — leave £9.99/£19.99 and add an annual option (~£99/yr Basic,
~£199/yr Pro, i.e. two months free).
```

## What changed

Prices fixed, mechanism left open — the right division. The numbers are a
business decision; how the period reaches Stripe is not.

*"i.e. two months free"* did shape the code. It says the annual price is a round
number chosen for how it reads, so `price_year` is stored rather than computed
from `price × 10`. It also became a test: a year must save between 1.8 and 2.3
months, which is what catches `£19.90` typed for `£199.00`.

## What it produced

`price_year` on both paid tiers, `?period=year` threaded through both checkout
routes, PayPal's grant extended to 365 days when that is what was paid, a period
chooser on the checkout page, and 23 tests.

Verified afterwards against the real Stripe test API, not just the mock: GBP
99.00 per year and GBP 199.00 per year, both `mode=subscription`.
