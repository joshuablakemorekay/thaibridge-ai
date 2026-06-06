# ThaiBridge AI

A web app that teaches Thai through the lens of Thai culture and Buddhism — built as my first web app and a portfolio project.

> **Honest status:** this is a learning project, not a finished product. It runs locally and works, but it isn't deployed or polished for real users yet. The full build story (including the mistakes) is in [`JOURNAL.md`](./JOURNAL.md).

## What It Does

- Teaches the **Thai alphabet** (44 consonants and the vowels) and vocabulary by topic, with **Paiboon-style romanization** (a way of writing Thai sounds in English letters, with tone marks).
- Includes **lessons, grammar, culture and temple-etiquette modules**, and Theravada Buddhist content.
- Has an **AI tutor** with several modes — conversation, grammar help, quizzes, culture, and Buddhism — powered by the Claude API (a way for the app to talk to the AI).
- Keeps learners motivated with **points, levels, and achievements**, plus a meditation timer.
- Supports **user accounts** (sign-up with a saved profile) and a developer mode for testing.
- Offers **subscription tiers** with **Stripe & PayPal** checkout (test/sandbox mode — no real money moves).

## Built With

- **Python (Flask)** — runs the web server and the pages
- **SQLite** — a simple file-based database for user accounts
- **Anthropic Claude API** — powers the AI tutor
- **Stripe & PayPal** (via `httpx`) — handle subscription payments in test mode
- **HTML, CSS, JavaScript** — the pages and the interactive bits (quizzes, flashcards)
- **pytest** — runs the automatic tests

## How to Run It

You'll need **Python 3.10+** and a free [Anthropic API key](https://console.anthropic.com) (for the AI tutor).

1. **Get the code** (clone the repo — copy the project folder to your machine):
   ```bash
   git clone https://github.com/joshuablakemorekay/thaibridge-ai.git
   cd thaibridge-ai
   ```
2. **Install the dependencies** (the external tools the project relies on):
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your two secret values** (Windows Command Prompt shown — see the note below for Mac/Linux):
   ```cmd
   set ANTHROPIC_API_KEY=sk-ant-your-key-here
   set FLASK_SECRET_KEY=any-long-random-string
   ```
   > On Mac/Linux use `export ANTHROPIC_API_KEY="..."` instead. You can generate a secret key with: `python -c "import secrets; print(secrets.token_hex(32))"`
4. **Run the app:**
   ```bash
   python app.py
   ```
   Then open **http://localhost:5000** in your browser. The database is created automatically the first time.
5. **Run the tests** (optional):
   ```bash
   python -m pytest tests/ -v
   ```

## My Journey

The build story, newest first. Full version with lessons learned in [`JOURNAL.md`](./JOURNAL.md).

- **6 Jun 2026 — Real Stripe test payment + a renewal-date fix.** I took my first real test-card payment all the way through Stripe Checkout and confirmed the webhook (Stripe's server messaging mine) activated a paid subscription in the database, with a real Stripe customer and subscription attached. Along the way I fixed a bug where the renewal date wasn't being saved — Stripe had moved that field onto the subscription *item* in a newer version of their API. **Lesson:** a "200 OK" doesn't prove it worked — checking the actual database caught both the bug and a stale browser tab that had hijacked my first attempt.
- **5 Jun 2026 — Wireframe layout, rename & payments.** I finished a proper wireframe layout system — four page "shapes" built from a content-first outline — and rolled the 3-column version across the learning pages using reusable partials. I also fixed a database-startup crash, added a Help page, settled the app's display name as **ThaiBridge AI**, and shipped **Stripe + PayPal** subscriptions. **Lesson:** a wireframe is a *planning* tool, not a feature — and "tests pass / 200 OK" proves a page *loads*, not that it *looks right* (eight "broken" pages were actually working paywalls).
- **Mar–Apr 2026 — Market research.** Researched competitors, UK audience size, and pricing. Learned to ground research in real sources and to **check which tools actually ran**. (The prompts behind this are documented in [`prompts/`](./prompts/).)
- **Feb 2026 — Version control + workflow.** Set up Git and GitHub, then used Claude Code to add user registration, fix a form-validation bug, add **32 tests**, and fix code-review issues. Learned that version control let me take risks safely — and that an AI's changes still need reviewing.
- **Feb 2026 — Buddhist writings.** Added Pra Kru Bob's essays as pages. Learned that **faithful means faithful** — I had to check the text against the source, not trust a summary.
- **Dec 2025 — AI tutor.** Connected the app to the Claude API. The setup fought me at every step (missing Python, missing packages, a vanishing key, a missing pair of quotes). Biggest lesson: **don't trust "it works" — test it yourself.**
- **Dec 2025 — Romanization display.** A Thai vowel with an accent mark kept rendering wrong. Learned **when to stop polishing and use a workaround.**
- **Nov 2025 — First version + debugging.** Built the Flask app and content. Learned that most early errors were **files in the wrong place**, and that **reading the error message** usually told me exactly what was wrong.
- **Nov 2025 — Planning.** Planned with a describe-then-check method. Learned to **cut the scope down to a small working version** instead of building everything at once.

## What's Next

- **Deploy it** — get it online so other people can try it, rather than running only on my machine.
- **Make it deploy-ready** — add database migrations and move from SQLite to a hosted database (Postgres), so accounts and subscriptions survive on a live server.
- **Switch payments to live keys** — the full Stripe test flow now works end-to-end; going live just needs the real keys (and the same for PayPal).
