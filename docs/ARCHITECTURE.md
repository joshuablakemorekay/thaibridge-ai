# Architecture & Codebase Guide

This is the developer's-eye view of the Thai Language & Culture Learning App — what
the code is, how it's put together, how it runs, and the design decisions (and a few
"gotchas") behind it. It was written by reading the real source files, so it reflects
what's actually in the repo, not what we hoped to build.

If you just want to *use* the app, start with the root `README.md`. If you want to
*work on* it, start here.

---

## The one-paragraph summary

This is a **Flask web app** (Flask = a Python toolkit that turns Python functions into
web pages) for learning Thai through culture and Buddhism. Almost everything lives in a
single large file, `app.py`. Learning content (vocabulary, grammar, meditation guides)
is written directly into Python as data, the way you'd fill in a spreadsheet. An
AI tutor powered by Claude lives in a separate file, `ai_agent.py`. Player progress —
points, levels, unlocked sections — is tracked per browser session, and there's a
gamified "level up to unlock more" system on top.

---

## Tech stack (the tools it relies on)

From `requirements.txt`:

- **Flask 3.1** — the web framework (the toolkit that gives the project its web-page structure)
- **Flask-SQLAlchemy** — talks to the database in Python instead of raw SQL
- **SQLite** — a tiny file-based database (one `.db` file, no separate database server needed)
- **Flask-Login** — keeps track of who is logged in across requests (real sign-in/sign-out)
- **Werkzeug** — used here to hash passwords safely (turn a password into scrambled text that can't be reversed)
- **anthropic** — the official Claude SDK (the library that lets the app talk to Claude)
- **stripe** — the Stripe SDK for taking subscription payments (test mode)
- **httpx** — used to talk to PayPal's REST API directly (second payment option)
- **python-dotenv** — loads secret settings from a `.env` file
- **pytest** — the testing tool

---

## How to run it

1. **Install the dependencies** (the external tools the project needs):
   ```
   pip install -r requirements.txt
   ```
   (Or run `install.bat` on Windows / `install.sh` on Mac/Linux.)

2. **Create a `.env` file** (copy `.env.example`) and fill in:
   - `ANTHROPIC_API_KEY` — **required.** The app refuses to start without it.
   - `FLASK_SECRET_KEY` — **required.** Used to secure browser sessions.
   - `DEVELOPER_PASSWORD` — optional. Unlocks a developer test mode (defaults to `changeme`).

3. **Start the app:**
   ```
   python app.py
   ```

4. **Open** http://127.0.0.1:5000 in your browser.

On startup the app prints a banner, creates the SQLite database file if it doesn't
exist, and tries to initialise the AI agent. If the AI key is missing it still runs —
it just disables the AI features and tells you why.

---

## The big picture (how the pieces fit)

```
                ┌──────────────────────────────────────────┐
   Browser ───► │  app.py  (the whole web app)             │
                │   • config + secrets (from .env)         │
                │   • User model (SQLite)                  │
                │   • gamification rules (levels, tiers)   │
                │   • learning content (Python dicts)      │
                │   • ~60 routes (pages + JSON APIs)       │
                └───────────────┬──────────────────────────┘
                                │ AI calls
                                ▼
                ┌──────────────────────────────────────────┐
                │  ai_agent.py  (Claude wrapper)           │
                │   • 6 teaching "modes"                   │
                │   • per-session chat history             │
                └───────────────┬──────────────────────────┘
                                │
                                ▼
                         Claude (Anthropic API)

   Side data:  data/*.tsv  (Thai–English dictionary)
   Templates:  templates/*.html  (the actual pages)
```

---

## File-by-file tour

### `app.py` — the heart of everything (~5,400 lines)

This single file holds the entire web app. It's organised top-to-bottom roughly like this:

1. **Setup & secrets** — loads `.env`, creates the Flask app, and *fails fast* if the
   API key or secret key is missing (it raises an error rather than running half-broken).
2. **Database config + `User` model** — one table, `users`. Identity columns
   (`id`, `username`, `email`, `password_hash`, `created_at`) plus **subscription
   columns** (`subscription_tier`, `subscription_status`, `stripe_customer_id`,
   `stripe_subscription_id`, `current_period_end`). It also has a `effective_tier`
   property — the one rule that decides what a user gets *right now* (a paid tier
   only counts while active and not expired). Helpers set/check passwords safely.
3. **Gamification & subscription rules** — the level thresholds, point rewards,
   achievements, section-unlock requirements, and subscription tiers (all explained below).
4. **Learning content** — large Python dictionaries holding vocabulary, gendered/formal
   sentence patterns, grammar, culture notes, Buddhist teachings, and more.
5. **Helper functions** — things like `add_xp()`, `get_user_level()`,
   `check_section_access()`, `check_achievements()`, and a `require_access()` decorator
   that locks a page behind a level/tier requirement.
6. **Routes** — about 60 of them: page routes (`/`, `/alphabet`, `/chat`, `/dictionary`…)
   and JSON API routes (`/api/...`) that the front-end calls for quizzes, points, and AI.

**Design note:** keeping everything in one file makes the app very easy to run and read
top-to-bottom, but hard to maintain as it grows. Splitting `app.py` into modules
(models, content, routes, gamification) is the most obvious future refactor
("refactor" = rewriting code to be cleaner without changing what it does).

### `ai_agent.py` — the Claude-powered tutor (~500 lines)

A clean, self-contained class called `ThaiLearningAI` that wraps Claude. Key points:

- **Model used:** `claude-sonnet-4-20250514`.
- **Six teaching modes**, each defined by its own system prompt (the instructions that
  shape how Claude behaves):
  - `conversation` — a practice partner that corrects one mistake at a time
  - `tutor` — explains concepts in a fixed three-step structure
  - `generator` — creates custom exercises and quizzes
  - `cultural` — explains Thai culture through the language it shapes
  - `buddhist` — teaches dharma terms as vocabulary
  - `helper` — gives progressive hints without spoiling the answer
- **A shared "rulebook"** sits at the top of every prompt: the **Paiboon+ romanization
  rules** (a precise, IPA-based way of writing Thai sounds in Latin letters). This is the
  single most important design choice in the AI layer — it forces consistent, accurate
  pronunciation across every mode.
- **Conversation memory:** chat history is kept per session in memory (the last 20
  messages), so the tutor remembers the current conversation but nothing is saved to disk.
- **Singleton pattern:** `get_ai_agent()` returns one shared instance, created once.

The app talks to this file through endpoints like `/api/ai/chat`, `/api/ai/hint`,
`/api/ai/explain`, `/api/ai/generate`, `/api/ai/clear`, and `/api/ai/status`.

### `new_routes.py` — ⚠️ a draft, not wired in

This file defines tourist vocabulary, business-Thai vocabulary, and meditation data,
plus `/tour-guide`, `/business-thai`, and `/meditation` routes. **But `app.py` already
has its own versions of those three routes**, and `new_routes.py` is **never imported**
by the app. Its own header comment says *"Add these two routes to app.py"* — so it's a
**staging/scratch file**, a place where new content was drafted before being copied in.

**Gotcha for future-you:** editing `new_routes.py` changes nothing in the running app.
The live versions live in `app.py`. This file is currently untracked (not yet saved into
git) — decide whether to fold it into `app.py` and delete it, or keep it as a drafting pad.

### The Paiboon dictionary pipeline

The app ships a real English–Thai dictionary (~4,894 entries, sourced from the
NECTEC LEXiTRON / Yaitron corpus). The data and the scripts that process it:

- `data/yaitron_dictionary_paiboon_fixed.tsv` — the dictionary **with** Paiboon
  pronunciation added. This is what the app prefers to load.
- `data/yaitron_dictionary.tsv` — the plain English–Thai base file (used as a fallback).
- `generate_paiboon.py` — adds Paiboon romanization to the base dictionary.
- `fix_paiboon.py` / `rerun_paiboon.py` — clean up and re-process entries that came out
  wrong the first time (`data/needs_rerun.tsv` lists those).

`_load_yaitron()` in `app.py` loads this once at startup, prefers the Paiboon-enriched
file, removes duplicates, and falls back gracefully if the enriched file isn't there.

> **Heads-up:** at the time of writing, the base `data/yaitron_dictionary.tsv` is
> *deleted* in the working folder (an uncommitted change). The app still runs fine
> because it loads the `_paiboon_fixed.tsv` version, but it's worth deciding whether
> that deletion was intentional before committing it.

### `templates/` — the actual web pages (~30 files)

Standard Jinja2 templates (HTML with placeholders Flask fills in). They all extend
`base.html` for shared layout. There's one template per feature — `alphabet.html`,
`dictionary.html`, `chat.html`, `meditation.html`, `progress.html`, and so on.

### `tests/` and `test_api.py`

- `tests/test_calculator.py` — unit tests for the gamification maths (XP and level calculations).
- `test_api.py` — a smoke test for the API.

### `docs/`

Setup and phase guides written during the build — `QUICK_START.md`,
`PHASE_1_SETUP_GUIDE.md`, `AI_INTEGRATION_SIMPLE_GUIDE.md`, and others.

---

## How the gamification system works

The app is built like a game: you earn points, level up, and unlock content.

- **10 levels**, each with an XP threshold (`XP_LEVELS`): Level 1 starts at 0 XP and
  Level 10 needs 12,000 XP.
- **Points are earned** for actions (`POINT_REWARDS`) — e.g. a correct quiz answer = 10,
  a perfect quiz = 50, a daily login = 15.
- **Six achievements** (`ACHIEVEMENTS`) — badges like *First Steps*, *Word Learner*, and
  *Enlightened*, each unlocked by meeting a condition.
- **Every section has an unlock rule** (`SECTION_REQUIREMENTS`): a minimum level, a
  subscription tier, and — for most learning sections — **completing the Thai alphabet
  first**. The alphabet is the gateway to the rest of the app.
- The `require_access()` decorator enforces these rules on protected routes.

**Where things are stored:**
- **Subscriptions live in the database** (on the `User` row) — this is the source of
  truth, written by the Stripe webhook. A tampered session cookie cannot grant paid
  access; access is always checked against the DB via `active_tier()`.
- **Learning progress** (XP, level, unlocked sections) still lives in the **Flask
  session** (`user_progress`), tied to the browser rather than synced across devices —
  a known trade-off and the next obvious thing to move into the database.

## Subscription tiers

Three tiers are defined (`SUBSCRIPTION_TIERS`):

| Tier | Name | Price | Unlocks |
|------|------|-------|---------|
| `free` | Free Explorer | $0 | Levels 1–5, core vocab, grammar, culture, Paiboon guide |
| `basic` | Buddhist Scholar | $9.99 | + Theravada teachings, meditation timer, Levels 6–7, 2× points |
| `pro` | Thai Master | $19.99 | + Full dictionary, premium AI tools, Levels 8–10, 3× points |

These power the `/premium` and `/subscribe/<tier>` pages.

**How a subscription actually flows (production-style):**
1. A logged-in user picks a tier → `/subscribe/<tier>/stripe` creates a Stripe
   Checkout session, tagged with their `user_id` (so we know whose payment it is).
2. They pay on Stripe (test mode), then Stripe calls our **webhook**
   (`/stripe/webhook`) server-to-server. The webhook verifies the signature and is
   the **source of truth** — it writes the tier, status, Stripe ids and the
   period-end date onto the `User` row.
3. The webhook also handles **renewals** (`invoice.paid` pushes the period out) and
   **cancellations** (`customer.subscription.deleted` flips the status, so
   `effective_tier` drops the user back to free).
4. PayPal is offered as a second option; since this demo doesn't use PayPal's
   recurring billing, a PayPal payment is recorded as a 30-day access grant.

(Test mode only — no real money moves. To go live you'd swap in live Stripe/PayPal
keys and move off SQLite, see the README's deploy notes.)

## Developer mode

`/developer-login` accepts a password (hashed from the `DEVELOPER_PASSWORD` environment
variable) and unlocks everything for testing, so you don't have to grind levels while
developing. `/developer-logout` ends it.

---

## Security & secrets

- **All secrets come from environment variables**, loaded from `.env` — the API key, the
  Flask secret key, and the developer password. Nothing sensitive is hard-coded. (This was
  a deliberate clean-up: an earlier commit moved the developer password out of the source
  code and into an environment variable.)
- **Passwords are hashed** with Werkzeug before being stored — the raw password is never
  saved.
- **Sign-in is handled by Flask-Login** — only the user's id is kept in the signed
  session cookie; the full account is loaded from the database each request.
- **Subscriptions are verified server-side** — the Stripe webhook checks the event
  signature, and paid access is read from the database, never from the cookie, so a
  user can't edit a cookie to unlock paid content.
- `.env`, the database file, and other local artifacts are kept out of git via `.gitignore`.

---

## Key design decisions, in plain English

- **One big `app.py`.** Simple to run and follow; harder to maintain as it grows. The
  natural next step is splitting it into modules.
- **Content as Python data, not a database/CMS.** Vocabulary and lessons are written
  directly into Python dictionaries. Easy to edit by hand, but it mixes content with code.
- **Progress in the session, not the database.** Lightweight and quick, but not synced
  across devices and lost if the session is cleared.
- **A strict shared romanization rulebook for the AI.** The Paiboon+ rules are injected
  into every AI prompt so pronunciation stays consistent and accurate everywhere.
- **Fail-fast on missing secrets.** The app stops immediately if the API key or secret key
  is absent, rather than running in a broken state.

---

## Suggested first refactors (if you pick this up later)

1. **Split `app.py`** into `models.py`, `content/`, `gamification.py`, and `routes/`.
2. **Resolve `new_routes.py`** — fold it into `app.py` and delete it, or clearly mark it as a drafting pad.
3. **Move learning progress into the database** so it survives across devices and sessions
   (subscriptions already live there — progress is the remaining session-only piece).
4. **Decide on the deleted `data/yaitron_dictionary.tsv`** before committing that change.
5. **Before going live:** add Flask-Migrate (so schema changes don't need a DB wipe) and
   move off SQLite to a persistent database (e.g. Postgres) — Render's free disk is
   ephemeral, so SQLite there would lose data on redeploy.
