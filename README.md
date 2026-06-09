# ThaiBridge AI

A web app that teaches Thai through the lens of Thai culture and Buddhism — built as my first web app and a portfolio project.

> **Honest status:** this is a learning project, not a finished product — but it's now **live on the internet** at 👉 **[thaibridge-ai.onrender.com](https://thaibridge-ai.onrender.com)** (hosted free on Render). The full build story (including the mistakes) is in [`JOURNAL.md`](./JOURNAL.md).

## What It Does

- Teaches the **Thai alphabet** (44 consonants and the vowels) and vocabulary by topic, with **Paiboon-style romanization** (a way of writing Thai sounds in English letters, with tone marks).
- Includes **lessons, grammar, culture and temple-etiquette modules**, and Theravada Buddhist content.
- Has an **AI tutor** with several modes — conversation, grammar help, quizzes, culture, and Buddhism — powered by the Claude API (a way for the app to talk to the AI). It's **freemium-gated**: free and basic users get a daily taste, Pro unlocks all modes unlimited.
- Keeps learners motivated with **points, levels, and achievements**, plus a meditation timer.
- Supports **real user accounts** — sign up, log in and log out (Flask-Login) — plus a developer mode for testing.
- Offers **subscription tiers** with **Stripe** checkout — verified end-to-end in test mode, with the **database (not the browser cookie) as the source of truth**. PayPal checkout is scaffolded but not yet wired up.

## Built With

- **Python (Flask)** — runs the web server and the pages
- **SQLite** — a simple file-based database for user accounts
- **Anthropic Claude API** — powers the AI tutor
- **Stripe** — handles subscription payments (verified in test mode); **PayPal** scaffolded via `httpx` for later
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

- **9 Jun 2026 — Live on the internet (with a working AI link).** I deployed ThaiBridge to Render so anyone can visit it at **[thaibridge-ai.onrender.com](https://thaibridge-ai.onrender.com)**, and proved the AI tutor responds live by sending it a real message. I made the public demo **cost-safe** — it runs the cheap **Haiku** model and my Anthropic spend is capped — and added a free uptime pinger so the link loads instantly. **Lesson:** when the live app flickered with errors, the server logs showed it was just the free tier waking from sleep, not the crash I'd feared — checking the logs beat guessing from outside.
- **6 Jun 2026 — Real Stripe test payment + a renewal-date fix.** I took my first real test-card payment all the way through Stripe Checkout and confirmed the webhook (Stripe's server messaging mine) activated a paid subscription in the database, with a real Stripe customer and subscription attached. Along the way I fixed a bug where the renewal date wasn't being saved — Stripe had moved that field onto the subscription *item* in a newer version of their API. **Lesson:** a "200 OK" doesn't prove it worked — checking the actual database caught both the bug and a stale browser tab that had hijacked my first attempt.
- **6 Jun 2026 — Real subscription billing service.** I replaced the placeholder paywall with a real system: actual login/logout (Flask-Login), subscription plans stored in the **database** (not a cookie) with the Stripe webhook as the trusted source of truth, a merged premium/pricing page, and a freemium-gated AI tutor (free taste, unlimited on Pro). Checkout was built for both Stripe and PayPal, but only Stripe is configured and verified so far. **Lesson:** pick one source of truth (the database) and keep the access rule in one place, so nothing can be faked from the browser.
- **5 Jun 2026 — Wireframe layout, rename & payments.** I finished a proper wireframe layout system — four page "shapes" built from a content-first outline — and rolled the 3-column version across the learning pages using reusable partials. I also fixed a database-startup crash, added a Help page, settled the app's display name as **ThaiBridge AI**, and shipped **Stripe + PayPal** subscriptions. **Lesson:** a wireframe is a *planning* tool, not a feature — and "tests pass / 200 OK" proves a page *loads*, not that it *looks right* (eight "broken" pages were actually working paywalls).
- **Mar–Apr 2026 — Market research.** Researched competitors, UK audience size, and pricing. Learned to ground research in real sources and to **check which tools actually ran**. (The prompts behind this are documented in [`prompts/`](./prompts/).)
- **Feb 2026 — Version control + workflow.** Set up Git and GitHub, then used Claude Code to add user registration, fix a form-validation bug, add **32 tests**, and fix code-review issues. Learned that version control let me take risks safely — and that an AI's changes still need reviewing.
- **Feb 2026 — Buddhist writings.** Added Pra Kru Bob's essays as pages. Learned that **faithful means faithful** — I had to check the text against the source, not trust a summary.
- **Dec 2025 — AI tutor.** Connected the app to the Claude API. The setup fought me at every step (missing Python, missing packages, a vanishing key, a missing pair of quotes). Biggest lesson: **don't trust "it works" — test it yourself.**
- **Dec 2025 — Romanization display.** A Thai vowel with an accent mark kept rendering wrong. Learned **when to stop polishing and use a workaround.**
- **Nov 2025 — First version + debugging.** Built the Flask app and content. Learned that most early errors were **files in the wrong place**, and that **reading the error message** usually told me exactly what was wrong.
- **Nov 2025 — Planning.** Planned with a describe-then-check method. Learned to **cut the scope down to a small working version** instead of building everything at once.

## What's Next

- **Move to a hosted database (Postgres)** — the free host wipes the SQLite file on each restart, so accounts and subscriptions don't survive yet; add database migrations too.
- **Complete & verify PayPal** — add sandbox credentials and run a real sandbox payment, the same way Stripe was verified.
- **Switch Stripe to live keys** — the full Stripe test flow now works end-to-end; going live just needs the real keys.
