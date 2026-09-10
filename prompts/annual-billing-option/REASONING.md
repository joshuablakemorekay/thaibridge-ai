# Reasoning: Annual Billing Option

> Josh delegated the review of this write-up (*"yes just do what you recommend"*),
> so the reasoning below was drafted rather than dictated. The quotes are his,
> word for word; the prose around them is not, and he has not line-edited it.

## Goal

Let someone pay for a year instead of a month, at a price that reads as an offer.

## The part worth keeping: the prompt was wrong, and the prompt caught it

The request was to add a Premium tier at £8.99/month. The same message asked:

> Have we not already done some of these?

The answer was yes to nearly all of it. Two paid tiers already existed at £9.99
and £19.99, the AI chat was already the paid hook, and progress tracking and the
Buddhist-mindfulness angle were already shipped. The one genuine gap in the whole
list was **annual billing** — which the original plan mentioned almost in
passing, as "or £59/year".

Building what was asked for would have quietly cut the price of the existing
product by a pound and called it a launch.

That question is the reason this entry exists. A plan is a hypothesis about the
codebase, and checking it against the code before building is cheap. Josh asked
it himself, in the same breath as the request.

## Iteration history

- **v1 — a new tier at a new price.** Rejected after checking the code, not after
  building it.
- **v2 — annual on the existing tiers.** *"leave £9.99/£19.99 and add an annual
  option"*. Prices fixed by Josh, mechanism left open.

## Failure modes the final version handles

- **The period becoming a fourth product.** It rides in the query string
  (`?period=year`), so it is the same tier on a different clock. Stripe reports
  the real `current_period_end` either way, so no webhook, no access check and no
  database column had to change.
- **Talking someone into a year by accident.** Anything that is not exactly
  `"year"` falls back to monthly — `"YEAR"`, `"yearly"`, `"annual"`, `"12"`, an
  empty value. A stale bookmark or an edited URL lands on the smaller commitment,
  never the larger one. Eight cases are pinned in the tests.
- **PayPal quietly granting the wrong length.** PayPal here is a one-off grant,
  not a real subscription, and it returns the user to a bare URL with nothing of
  ours on it. The chosen period is stashed in the session so the grant can be 365
  days instead of 30 — and defaults to 30 if that has gone missing, because
  under-granting is recoverable and over-granting is not.
- **A mistyped price.** A test asserts a year must save between 1.8 and 2.3
  months. `£19.90` where `£199.00` was meant fails loudly rather than selling a
  year of Pro for the price of one month.

## Outcome

Shipped in `8325d4a`. Full suite green at 1385, of which 23 are new.

Then verified against the **real** Stripe test API rather than the mock, by
driving the app's own route and retrieving the session Stripe actually created:

| | amount | interval | mode |
|---|---|---|---|
| basic / month | GBP 9.99 | month | subscription |
| basic / year | GBP 99.00 | year | subscription |
| pro / year | GBP 199.00 | year | subscription |

That check earned its place. The unit tests prove the app *builds* the right
parameters; only a live call proves Stripe *accepts* them — and this account has
Managed Payments enabled, which rejects any line item without a `tax_code`.

**Still unverified:** the PayPal 365-day branch. PayPal is not configured in this
environment, so it could not be exercised. That is the one line of this feature
resting on inspection rather than a test, and it is recorded here rather than
glossed over.

## Engineering on the output

As with the audit entry, this inverts the usual shape — the code was written
inside Claude Code and Josh directed it, so this section records his decisions
rather than his refactors.

- *Accepted as-is:* the query-string mechanism and the fallback-to-monthly rule.
- *Decided by Josh:* the prices, and the structural choice to **keep two tiers
  rather than restructure to one**. Restructuring would have meant unpicking the
  free/Basic/Pro gating across the whole app; he was given that trade-off and
  chose not to.
- *Rejected on evidence:* his own opening plan, on the strength of his own
  question.
- *Roughly:* one line of the original request survived — the annual option. The
  rest of the plan was already built.

## What I'd change next

Take one real test-card payment through Checkout to completion, so the webhook
path is proven for a yearly subscription and not only for a monthly one. And
configure PayPal in a test environment so its branch stops being the only
untested line.

## Tags

`billing` `stripe` `paypal` `subscriptions` `premise-checking` `testing`
