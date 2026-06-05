# Thai Language & Culture Learning App

A web app that teaches Thai through the lens of Thai culture and Buddhism — built as my first web app and a portfolio project.

> **Honest status:** this is a learning project, not a finished product. It runs locally and works, but it isn't deployed or polished for real users yet. The full build story (including the mistakes) is in [`JOURNAL.md`](./JOURNAL.md).

## What It Does

- Teaches the **Thai alphabet** (44 consonants and the vowels) and vocabulary by topic, with **Paiboon-style romanization** (a way of writing Thai sounds in English letters, with tone marks).
- Includes **lessons, grammar, culture and temple-etiquette modules**, and Theravada Buddhist content.
- Has an **AI tutor** with several modes — conversation, grammar help, quizzes, culture, and Buddhism — powered by the Claude API (a way for the app to talk to the AI).
- Keeps learners motivated with **points, levels, and achievements**, plus a meditation timer.
- Supports **user accounts** (sign-up with a saved profile) and a developer mode for testing.

## Built With

- **Python (Flask)** — runs the web server and the pages
- **SQLite** — a simple file-based database for user accounts
- **Anthropic Claude API** — powers the AI tutor
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

- **Mar–Apr 2026 — Market research.** Researched competitors, UK audience size, and pricing. Learned to ground research in real sources and to **check which tools actually ran**. (The prompts behind this are documented in [`prompts/`](./prompts/).)
- **Feb 2026 — Version control + workflow.** Set up Git and GitHub, then used Claude Code to add user registration, fix a form-validation bug, add **32 tests**, and fix code-review issues. Learned that version control let me take risks safely — and that an AI's changes still need reviewing.
- **Feb 2026 — Buddhist writings.** Added Pra Kru Bob's essays as pages. Learned that **faithful means faithful** — I had to check the text against the source, not trust a summary.
- **Dec 2025 — AI tutor.** Connected the app to the Claude API. The setup fought me at every step (missing Python, missing packages, a vanishing key, a missing pair of quotes). Biggest lesson: **don't trust "it works" — test it yourself.**
- **Dec 2025 — Romanization display.** A Thai vowel with an accent mark kept rendering wrong. Learned **when to stop polishing and use a workaround.**
- **Nov 2025 — First version + debugging.** Built the Flask app and content. Learned that most early errors were **files in the wrong place**, and that **reading the error message** usually told me exactly what was wrong.
- **Nov 2025 — Planning.** Planned with a describe-then-check method. Learned to **cut the scope down to a small working version** instead of building everything at once.

## What's Next

- **Fix the romanization display properly** — the current approach is a workaround, not a real fix.
- **Decide on accounts** — right now the app works without login (a free, open version); enforcing sign-in is a later step.
- **Deploy it** — get it online so other people can try it, rather than running only on my machine.
