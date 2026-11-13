# Architecture & Codebase Guide

This is the developer's-eye view of ThaiBridge AI. It covers what the code is, how it's
put together, how it runs, and the design decisions (and a few "gotchas") behind it.
It was written by reading the real source files, so it describes what's actually in
the repo, not what we hoped to build.

If you just want to *use* the app, start with the root `README.md`. If you want to
*work on* it, start here. Two companion guides cover the rest:

- **[TESTING.md](./TESTING.md)** explains how the test suite is organised and how to run it safely.
- **[../SECURITY.md](../SECURITY.md)** explains how accounts, payments and the AI spend are protected.

*Last checked against the code: 13 November 2026.*

---

## The one-paragraph summary

ThaiBridge is a **Flask web app** (Flask is a Python toolkit that turns Python functions
into web pages) for learning Thai through its culture and Theravada Buddhism. The live
site is https://thaibridge.smoald.com. `app.py` is still the hub, holding most of the pages
and the billing. Around it sit about 40 smaller modules, each owning one job: accounts,
access rules, progress, quizzes, the chanting book and so on. Learning content is written
directly into Python as data, the way you'd fill in a spreadsheet. A Claude-powered tutor
lives in `ai_agent.py`. Accounts, progress, payments, AI usage and reviews are stored in
**Postgres** in production and a **SQLite** file on a developer's machine.

---

## Tech stack (the tools it relies on)

From `requirements.txt`:

- **Flask 3.1** is the web framework.
- **Flask-SQLAlchemy / SQLAlchemy 2.0** talk to the database in Python instead of raw SQL.
- **psycopg2** is the Postgres driver used in production (on Neon, Frankfurt).
- **Flask-Login** keeps track of who is logged in.
- **Flask-Limiter** puts rate limits on the routes that cost money or guard accounts.
- **Werkzeug** hashes passwords, turning them into scrambled text that can't be reversed.
- **anthropic** is the official Claude SDK, used by the AI tutor.
- **stripe** handles subscriptions, the Instant Access Pass and dāna gifts. It's **live**
  since 5 November 2026.
- **httpx** talks to PayPal's REST API (the second payment option).
- **python-dotenv** loads secret settings from a `.env` file.
- **pytest** is the testing tool. `requirements-dev.txt` adds the extra libraries only the
  tests and scripts need.

**Hosting:** Render (free web service, Frankfurt), built from `render.yaml`, started with
`gunicorn app:app`, served behind Cloudflare. Every push to `main` deploys automatically.
Python is pinned to **3.12.8** in `.python-version`.

---

## How to run it

1. **Install the dependencies:**
   ```
   pip install -r requirements-dev.txt
   ```
   (`requirements-dev.txt` includes everything in `requirements.txt`, plus what the tests need.)

2. **Create a `.env` file** (copy `.env.example`) and fill in:
   - `ANTHROPIC_API_KEY` is **required**. The app refuses to start without it.
   - `FLASK_SECRET_KEY` is **required**. It signs the browser's session cookie.
   - `DEVELOPER_PASSWORD` is optional. It turns on developer mode. **There's no default.**
     If it's left blank, developer mode is switched off entirely.
   - Leave `DATABASE_URL` **unset** locally, so the app uses `instance/thai_app.db`.

3. **Start the app** with Flask's own runner:
   ```
   PYTHONUTF8=1 DATABASE_URL="" python -m flask --app app run --port 5000
   ```
   `DATABASE_URL=""` guarantees you're on the local SQLite file, even if your `.env` holds
   the live connection string (see "Gotchas" below). Avoid `python app.py`. It imports the
   app twice, and one page (`/calendar`) breaks locally when that happens. The live site
   uses gunicorn and isn't affected.

4. **Open** http://127.0.0.1:5000.

On startup the app creates any missing database tables, adds any missing columns, and
tries to start the AI tutor. If the AI can't start, the rest of the site still runs.

---

## The big picture (how the pieces fit)

```
                     Browser
                        │
                        ▼
                  Cloudflare ──► Render (gunicorn)
                                      │
   ┌──────────────────────────────────┴───────────────────────────────────┐
   │  app.py  — the hub (~7,400 lines, ~90 routes)                        │
   │   • config, secrets, database setup                                  │
   │   • page routes for Learn, Culture, Buddhism, Chanting, Tour Guide…  │
   │   • billing: Stripe/PayPal checkout + the Stripe webhook             │
   │   • AI routes (/api/ai/*) with allowances and usage logging          │
   │                                                                      │
   │  Blueprints registered by app.py:                                    │
   │   auth.py (accounts) · quizzes.py (drills) · app_reviews.py (reviews)│
   │                                                                      │
   │  Plain modules app.py imports:                                       │
   │   access.py · progress.py · plans.py · rewards.py · questions.py ·   │
   │   learning_path.py · signup_source.py · site_search.py · curriculum.py│
   │   + content modules (vocabulary, chanting, survival, tour_trips…)    │
   └───────────────┬──────────────────────────────┬───────────────────────┘
                   │                              │
                   ▼                              ▼
          ai_agent.py ──► Claude API      models.py ──► Postgres (live)
                                                       SQLite (local)
   Stripe ──webhook──► /stripe/webhook
   Resend ◄── password-reset emails (accounts.py)
```

**The one rule that keeps this tidy: modules never import `app.py`.** `app.py` imports them,
never the other way round. That means there's no import loop. Each module that needs to
hook into the app gets an `init_app(app)` function that `app.py` calls once.

---

## File-by-file tour

### `app.py` — the hub (~7,400 lines)

Organised top to bottom roughly like this:

1. **Setup & secrets.** It loads `.env`, creates the Flask app, and *fails fast* if
   `ANTHROPIC_API_KEY` or `FLASK_SECRET_KEY` is missing. It also redirects the old domain
   (`thaibridge-ai.smoald.com`) to the new one with a permanent 301.
2. **Database setup.** Postgres when `DATABASE_URL` is set, otherwise SQLite. Two tables are
   defined here: `AiUsage` (one row per AI request) and `Payment` (one row per time money
   moved). Then `db.create_all()` and `ensure_user_columns()` bring any database up to date
   (see "Database" below).
3. **Extensions and blueprints.** It attaches the rate limiter and login manager, then
   registers `auth`, `quizzes` and `app_reviews`, and wires up `progress` and `signup_source`.
4. **Gamification and access helpers.** `ACHIEVEMENTS`, `check_achievements()`, and the
   `require_access()` decorator that puts a page behind its rule in `access.py`.
5. **Learning content** that hasn't been moved out into its own module yet.
6. **Routes** (~90): pages (`/`, `/alphabet`, `/chanting`, `/calendar`…), JSON APIs
   (`/api/...`), billing (`/subscribe/...`, `/dana`, `/stripe/webhook`), and AI
   (`/api/ai/chat`, `/hint`, `/explain`, `/generate`, `/clear`, `/status`).

### Accounts: `models.py`, `auth.py`, `accounts.py`, `extensions.py`

- `models.py` holds the database object (`db`), the `User` model, the `AppReview` model, and
  `utcnow()`. That function deliberately returns a time *without* a timezone; changing it
  breaks the subscription date comparisons, and a test pins it.
- `auth.py` is a Flask **Blueprint** (a bundle of routes registered with the app). It holds
  sign-up, log-in, log-out, forgotten password, reset and change password.
- `accounts.py` holds the password rules, the signed reset links and the account emails.
- `extensions.py` creates the login manager and the rate limiter, plus `rate_limit_key()`,
  which identifies a visitor by their real address behind Cloudflare.

### Access and plans: `access.py`, `plans.py`

- `access.py` holds `SECTION_REQUIREMENTS` (every section's level, tier and alphabet rule),
  `check_section_access()`, `active_tier()` (the tier to enforce *right now*, read from the
  database for logged-in users), and the **earned unlock**: reaching Level 3 lets a free
  learner open one Thai Reader section for good.
- `plans.py` is the price list (`SUBSCRIPTION_TIERS`) and the AI allowances each plan gets.

### Progress and rewards: `progress.py`, `rewards.py`, `questions.py`, `learning_path.py`

- `progress.py` handles a learner's XP, level, streak and settings. The session cookie is
  the working copy, and `User.progress` (a JSON column) is the durable one. It's saved
  after every request and restored at login. Keys that grant anything (tier, unlocks,
  developer mode) are **never** saved from the cookie.
- `rewards.py` holds the point values (`POINT_REWARDS`), `add_xp()` and a **daily cap** on
  drill XP.
- `questions.py` signs each drill question's answer with an **HMAC** (a tamper-proof
  fingerprint made with the secret key), so the browser never learns the answer and
  can't claim XP for one it didn't get right.
- `learning_path.py` is the Personalised Learning Path on `/progress`: goals, a placement
  check, weekly targets.

### Blueprints for features: `quizzes.py`, `app_reviews.py`

- `quizzes.py` holds the exercise pages, quiz questions, listening questions and
  `/api/check_answer`.
- `app_reviews.py` is the in-app review prompt. It shows a card on `/progress` from
  Level 3, saves reviews privately to `app_reviews`, and lists them at `/reviews/private`
  for developer mode only.

### `ai_agent.py` — the Claude-powered tutor (~1,200 lines)

A class called `ThaiLearningAI` that wraps Claude.

- **Model:** `claude-sonnet-5-5`, set by the `AI_MODEL` environment variable. It moved up
  from Haiku in October 2026 because the cheaper model taught wrong Thai.
- **Seven chat modes:** `conversation`, `tutor`, `generator`, `cultural`, `buddhist`,
  `helper` and `translator`. Translator is Pro only and can read a photo of Thai text.
- **A shared rulebook** at the top of every prompt holds the **ThaiBridge Spelling** rules
  (the app's romanisation, based on Paiboon+), so pronunciation is written the same way
  everywhere.
- **A spelling lookup tool.** The tutor can look up a word's confirmed spelling before
  answering, up to three rounds per message.
- **Prompt caching** keeps the long instructions cached between messages, which cuts the
  cost of a follow-up message to about a third.
- **Conversation memory** is kept per session, capped at 20 messages and 16,000 characters.
  It's never saved to disk.
- If the Anthropic account runs out of credit, the tutor shows a calm "resting" message
  instead of an error.

### Content modules

Learning content lives as Python data in its own files: `vocabulary.py`,
`sentence_content.py`, `thai_reading.py`, `thai_registers.py`, `tones.py`, `survival.py`,
`expat2000.py`, `tour_trips.py`, `tour_activities.py`, `thai_calendar.py` and more.
`content/` holds Markdown for the journal, Monk Mode lessons and Dhamma talks.

**The chanting book** is the biggest piece by far. `chanting.py` (~80,000 lines) holds 305
chants in Pali, Thai, ThaiBridge Spelling and English, verse by verse, transcribed from a
printed book. `chanting_layout.py`, `chanting_volumes.py` and `scripts/build_chanting_print.py`
turn the same data into the printed edition.

### The dictionary

About 4,900 English–Thai entries from the NECTEC LEXiTRON / Yaitron corpus.
`data/yaitron_dictionary_paiboon_fixed.tsv` (with pronunciation added) is what the app
loads. The plain file is the fallback. `generate_paiboon.py`, `fix_paiboon.py` and
`rerun_paiboon.py` are the one-off scripts that built it.

### `templates/` and `static/`

65 Jinja2 templates (HTML with placeholders Flask fills in). They all extend `base.html`.
`static/` holds the CSS, JavaScript, fonts and about 2,000 generated MP3 clips (Thai and English).

### `scripts/`, `prompts/`, `evals/`, `tests/`, `docs/`

- `scripts/` holds developer tools: audio generation, the print-book builder, review-sheet
  makers, and checkers for the chanting data.
- `prompts/` is the archived library of prompts used to build features, each with a rubric.
  `evals/` holds the AI tutor's accuracy exam.
- `tests/` holds 71 test files. See [TESTING.md](./TESTING.md).
- `docs/` holds this guide, the database runbook, review sheets and screenshots.

---

## Database

Four tables:

| Table | One row per… | Written by |
|---|---|---|
| `users` | account | `auth.py`, the Stripe webhook, `progress.py` |
| `payments` | time money moved (subscription, renewal, add-on, dāna) | Stripe/PayPal handlers |
| `ai_usage` | AI request: tokens, model, tier, outcome. **Never the message text.** | the AI routes |
| `app_reviews` | learner's review (one per account) | `app_reviews.py` |

**Schema changes without a migration tool.** `db.create_all()` creates whole new tables
on startup. It never adds a column to a table that already exists, so
`ensure_user_columns()` in `models.py` does that by hand, checking first so it's safe to
run on every start. New columns must be nullable or have a default.

For looking at live data safely, see [DATABASE_RUNBOOK.md](./DATABASE_RUNBOOK.md).

---

## How access works

Every section has a rule in `access.py`: a minimum **level**, a **tier**, and often
**"finish the alphabet first"**. `require_access()` enforces it on the page.

- **Tiers and prices** (`plans.py`): Free; **Thai Reader** £9.99/month or £99/year; **Thai
  Master** £19.99/month or £199/year. Pro has a fair-use cap of 75 AI messages a day.
- **The Instant Access Pass** is a one-off purchase that skips the level gates
  (`User.full_unlock`).
- **Monk Mode** opens the monk learning track with a code from `MONK_MODE_CODES`. Since
  21 October 2026 it **does not** waive the paywall.
- **The Dhamma teaching itself is free.** Guided practice, language study and the AI are
  what's paid for.
- **Where the truth lives:** the tier, unlocks and alphabet completion are read from the
  **database**, never from the cookie, so editing a cookie can't unlock anything.

**How a subscription flows:**
1. A logged-in learner picks a plan. `/subscribe/<tier>/stripe` creates a Stripe Checkout
   session tagged with their `user_id`.
2. They pay on Stripe. Stripe then calls `/stripe/webhook` from its own servers. The
   webhook **checks Stripe's signature**, then writes the tier, status, Stripe ids and
   period end onto the `User` row, and adds a `payments` row.
3. Renewals (`invoice.paid`) push the period out. Cancellations end access when the paid
   period does.
4. PayPal is a second option, recorded as a 30-day access grant.

---

## Developer mode

`/developer-login` takes the `DEVELOPER_PASSWORD` and opens everything for testing, plus
the private pages (such as `/reviews/private`). With no password configured, the route is
switched off completely. It doesn't fall back to a default. `/developer-logout` ends it.

---

## Key design decisions, in plain English

- **A hub plus small modules.** `app.py` is still big, but new features now go into
  their own modules (`access`, `progress`, `plans`, `app_reviews`…), and older parts
  move out when they're next touched.
- **Modules never import `app.py`.** No import loops, and each module can be tested alone.
- **Content as Python data.** Easy to edit and review line by line, and tests can walk
  every Thai string. The cost is that content and code live together.
- **The database decides who gets what.** Cookies hold working copies only.
- **Fail closed.** No developer password means no developer mode. No Monk Mode codes
  means Monk Mode can't be opened. A missing secret stops the app starting.
- **Log what it costs, never what was said.** `ai_usage` records tokens and outcomes so
  costs and caps are measurable, and stores none of the conversation.

---

## Gotchas

- **`import app` connects to the live database** if `.env` holds the production
  `DATABASE_URL`. Prefix any ad-hoc script with `DATABASE_URL=""`. The test suite does
  this for itself (see [TESTING.md](./TESTING.md)).
- **Use `flask run`, not `python app.py`, locally.** See "How to run it".
- **Changing a `render.yaml` environment value needs `sync: false`** for anything secret,
  or Render overwrites what you set in the dashboard.
- **A schema change needs a line in `ensure_user_columns()`**, or the live database never
  gets the new column.

---

## Suggested next refactors

1. **Keep shrinking `app.py`.** The billing routes and the AI routes are the two biggest
   self-contained pieces left to move into their own blueprints.
2. **Move `AiUsage` and `Payment` into `models.py`.** They stay in `app.py` today only
   because `Payment` reads the price list. That could be passed in instead.
3. **Adopt a real migration tool** (Flask-Migrate) once schema changes become more than
   "add a nullable column".
