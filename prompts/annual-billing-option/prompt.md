# Annual Billing Option

> **Category:** code-generation
> **Model used:** Claude Opus 5 (Claude Code)
> **Project area:** Thai Language & Culture Learning App — subscriptions
> **Status:** production
> **Last updated:** 2026-09-10

## What this prompt does

Adds a yearly billing option to two existing subscription tiers without turning
them into new products.

The interesting part is what came before the prompt. The original request was to
build a Premium tier that already existed — and the request contained the
question that caught it.

## The prompt

**The original plan (verbatim):**

```
Add a Premium tier — £8.99/month or £59/year, with the AI chat gated as the paid
feature.
```

**The question in the same message that made it worth checking first (verbatim):**

```
Have we not already done some of these?
```

It had. `SUBSCRIPTION_TIERS` already held Basic at £9.99/mo and Pro at £19.99/mo,
the AI chat was already the Pro hook with a free daily allowance, and levelling
and progress tracking were already built. Building the plan as written would have
been a **price cut** presented as a new feature.

**The revised instruction, once the audit came back (verbatim):**

```
For 1. Pricing — leave £9.99/£19.99 and add an annual option (~£99/yr Basic,
~£199/yr Pro, i.e. two months free).
```

## Inputs

- `SUBSCRIPTION_TIERS` in `app.py` — the live tier definitions
- `subscribe_stripe` and `subscribe_paypal` — the two checkout routes
- `paypal_success` — which grants access for a fixed number of days
- The Stripe webhook handlers, which set `current_period_end`

## Why it is shaped this way

The instruction fixes the prices and leaves the mechanism open, which is the
right split: the numbers are a business decision and the plumbing is not.

"Two months free" is the part that shaped the code. It says the annual price is a
round number chosen for how it reads, not `monthly × 10` computed at runtime — so
`price_year` is stored as its own value rather than derived.

## Expected output

- A billing period that does not become a fourth tier
- Both payment providers handling it, not just the one that is easy
- A safe default when the period is missing or malformed
- Tests that pin the amount and interval actually sent to Stripe, not just the
  page copy
