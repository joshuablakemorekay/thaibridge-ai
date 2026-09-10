# v1 — a new Premium tier

The plan as originally written.

```
Add a Premium tier — £8.99/month or £59/year, with the AI chat gated as the paid
feature.
```

## Why it was never built

The same message asked *"Have we not already done some of these?"* — so the code
was checked before anything was written. It had:

- `SUBSCRIPTION_TIERS` already held Basic (£9.99/mo) and Pro (£19.99/mo)
- the AI chat was already the paid hook, free tier capped by a daily allowance
- progress tracking, levelling and the Buddhist-mindfulness angle already shipped

Building it as specified would have introduced an £8.99 tier *below* the existing
£9.99 one, gated on a feature that was already gated. A price cut wearing a
launch announcement.

## What it produced instead

A list of what already existed versus what was actually missing. Exactly one item
on the original roadmap had not been built — annual billing, mentioned in passing
as "or £59/year".

The lesson is cheap to state and easy to skip: **a plan is a hypothesis about the
codebase.** Checking it costs one grep; not checking it costs a release.
