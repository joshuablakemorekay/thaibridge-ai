# Test-Payment Setup Guide — ThaiBridge AI

How to run subscription payments in **test/sandbox mode** (no real money), and
what to change when you eventually go live.

## Current status (2026-06-06)

| Provider | State |
|---|---|
| **Stripe** | ✅ Done — test keys in `.env`, real test-card payment + cancellation verified end-to-end, documented |
| **PayPal** | ⏳ Pending — code is built, but no sandbox credentials added or test payment run yet |

The plans (from `SUBSCRIPTION_TIERS` in `app.py`):
**Buddhist Scholar** $9.99/mo · **Thai Master (Pro)** $19.99/mo.

> The Stripe checkout builds the price **inline** (`price_data`), so you do
> **not** need to create Products/Prices in the Stripe dashboard — just keys.

---

## Part A — Stripe (already done; here for redo / reference)

### 1. Get your test API keys
- Dashboard: <https://dashboard.stripe.com/test/apikeys> (make sure **Test mode** is ON)
- Copy the **Publishable key** (`pk_test_…`) and **Secret key** (`sk_test_…`)

### 2. Stripe CLI (for the webhook secret)
The CLI forwards Stripe's webhook events to your local app — that's what flips
a user to "paid" in the database.

- Installed user-space at `~/.local/bin/stripe.exe` (v1.42.1).
- You can skip the interactive browser login by passing the key directly:
  ```
  stripe listen --api-key sk_test_... --forward-to localhost:5000/stripe/webhook
  ```
  It prints a signing secret `whsec_…`. Leave this window running while testing.

### 3. Put the three values in `.env`
```
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

### 4. Run the test payment
1. Start the app **without the reloader** (avoids a confusing parent/child process on Windows):
   - run `app.py`, but with `use_reloader=False` for a single clean process
2. Go to <http://localhost:5000>, **sign up / log in** (required — checkout attaches your user id)
3. `/premium` → pick a paid plan → **Subscribe** → **Stripe**
4. Test card: **4242 4242 4242 4242**, any future expiry, any CVC, any ZIP
5. You should land back on `/subscribe/success`

### 5. Confirm it worked
- The `stripe listen` window shows `checkout.session.completed` → `200`
- Your `User` row gets `subscription_tier`, a real `cus_…` / `sub_…`, and a renewal date
- Locked content (full AI modes, dictionary, levels 8–10) unlocks
- Fire synthetic events for pipeline tests:
  ```
  stripe trigger checkout.session.completed \
    --add checkout_session:metadata.user_id=<id> \
    --add checkout_session:metadata.tier=<tier>
  ```

---

## Part B — PayPal (the remaining to-do)

1. <https://developer.paypal.com/dashboard/applications/sandbox> → create a sandbox app
2. Copy its **Client ID** and **Secret** into `.env` (keep `PAYPAL_MODE=sandbox`):
   ```
   PAYPAL_CLIENT_ID=...
   PAYPAL_CLIENT_SECRET=...
   PAYPAL_MODE=sandbox
   ```
3. Run the app, `/premium` → paid plan → **PayPal**, pay with a sandbox buyer account,
   and confirm `/paypal/success` captures the order and upgrades the user.

---

## Gotchas worth remembering

- **`.env` needs `FLASK_SECRET_KEY`** (not `SECRET_KEY`) — the app raises `ValueError` on boot without it.
- **`.env` is gitignored** — keys never get committed, so a fresh clone has an empty `.env` you must refill.
- **`current_period_end`** moved onto the subscription *item* in newer Stripe API versions
  (`sub['items']['data'][0]['current_period_end']`) — handled by `_subscription_period_end()`.
- **Stray processes**: old `app.py` / `stripe listen` processes can linger and double-deliver
  webhooks (harmless — handlers are idempotent). Check with
  `Get-NetTCPConnection -LocalPort 5000` and `Get-CimInstance Win32_Process`.

---

## When you go LIVE (later)

1. Swap **test** keys for **live** keys (`sk_live_…`, `pk_live_…`) and a live webhook secret
2. Set `PAYPAL_MODE=live` with live PayPal credentials
3. **Before** real users: add **Flask-Migrate** (no more DB wipes for schema changes) and
   move off SQLite to **Postgres** (Render's free disk is ephemeral)
