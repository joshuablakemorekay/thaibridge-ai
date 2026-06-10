# 🪷 ThaiBridge AI

**Learn Thai through the lens of Thai culture and Buddhism — with an AI tutor that teaches you one-to-one.**

[![Live Demo](https://img.shields.io/badge/▶_Live_Demo-thaibridge--ai.smoald.com-brightgreen?style=for-the-badge)](https://thaibridge-ai.smoald.com)

![Python](https://img.shields.io/badge/Python-3.12.8-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![Claude API](https://img.shields.io/badge/AI-Claude_API-D97757)
![Stripe](https://img.shields.io/badge/Payments-Stripe-635BFF?logo=stripe&logoColor=white)
![Hosted on Render](https://img.shields.io/badge/Hosted_on-Render-46E3B7?logo=render&logoColor=white)

> **Honest status:** this is my **first web app** and a learning project — not a finished commercial product. But it's **live on the internet**, the payments work end-to-end (in test mode), and the AI tutor genuinely teaches. The full build story, mistakes and all, is in [`JOURNAL.md`](./JOURNAL.md).

<p align="center">
  <img src="./docs/screenshots/home-desktop.jpg" alt="ThaiBridge AI — a Theravada Buddhism page showing the three-column layout, navigation, and dictionary search" width="100%">
</p>

---

## ✨ What it does

- 🔤 **Teaches the Thai alphabet** (44 consonants and the vowels) and vocabulary by topic, with **Paiboon-style romanization** (a way of writing Thai sounds in English letters, with tone marks).
- 📚 **Lessons, grammar, culture and temple-etiquette modules**, plus Theravada Buddhist teachings and a meditation timer.
- 🤖 **An AI tutor** with several modes — conversation, grammar help, quizzes, culture and Buddhism — powered by the **Claude API** (a way for the app to talk to the AI). It's **freemium**: free users get a daily taste, Pro unlocks every mode unlimited.
- 🏆 **Keeps learners motivated** with points, levels and achievements.
- 👤 **Real user accounts** — sign up, log in, log out — so progress and plans belong to *you*.
- 💳 **Subscription tiers with Stripe checkout**, verified end-to-end in test mode, with the **database (not a browser cookie) as the source of truth** — so a paid plan can't be faked.

---

## 📸 A look inside

| The learning side | The AI tutor |
|---|---|
| <img src="./docs/screenshots/learning-desktop.jpg" alt="The Paiboon Romanization guide with the full learning sidebar" width="100%"> | <img src="./docs/screenshots/ai-tutor.jpg" alt="The AI tutor with its mode buttons and the free-message counter" width="320"> |
| The Paiboon romanization guide, with the full learning menu down the side. | The AI tutor — pick a mode and chat. Free users see how many messages they have left today. |

---

## 💡 What I built and why

I'm learning to code in public, and I wanted a *real* project rather than a toy — something with genuine accounts, real payments, and an AI feature that actually does something useful. I chose Thai-with-Buddhism because the big language apps don't teach Thai well, and **none of them connect the language to its culture** — which is the gap I set out to fill.

Along the way I deliberately built the "grown-up" parts properly: real login, database-backed subscriptions, a payment webhook as the single source of truth, and a freemium model that can't be cheated from the browser. I made the **Dhamma teachings free for everyone** (it didn't feel right to paywall them) and kept the costly AI features as the paid product.

---

## 🛠️ Tech stack

| Tool | What it does here |
|---|---|
| **Python + Flask** | Runs the web server and renders the pages |
| **Flask-Login** | Handles real sign-up, log-in and log-out |
| **SQLite + Flask-SQLAlchemy** | Stores users, plans and progress in a simple database |
| **Anthropic Claude API** | Powers the AI tutor |
| **Stripe** | Subscription payments (verified in test mode) |
| **HTML, CSS, JavaScript** | The pages and interactive bits (quizzes, flashcards, chat) |
| **pytest** | The automatic test suite |
| **Render** | Hosts the live site (free tier) |

---

## 🚀 Run it locally

You'll need **Python 3.12** (the live site runs 3.12.8) and a free [Anthropic API key](https://console.anthropic.com) for the AI tutor.

1. **Get the code** (clone the repo — copy the project to your machine):
   ```bash
   git clone https://github.com/joshuablakemorekay/thaibridge-ai.git
   cd thaibridge-ai
   ```
2. **Install the dependencies** (the external tools the project relies on):
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your two secret values** (Windows Command Prompt shown):
   ```cmd
   set ANTHROPIC_API_KEY=sk-ant-your-key-here
   set FLASK_SECRET_KEY=any-long-random-string
   ```
   > On Mac/Linux use `export ANTHROPIC_API_KEY="..."` instead. Generate a secret key with:
   > `python -c "import secrets; print(secrets.token_hex(32))"`
4. **Run the app:**
   ```bash
   python app.py
   ```
   Open **http://localhost:5000** — the database is created automatically the first time.
5. **Run the tests** (optional):
   ```bash
   python -m pytest tests/ -v
   ```

---

## 🎓 What I learned

The honest, useful lessons — the full story (newest first) is in [`JOURNAL.md`](./JOURNAL.md):

- **"It works" needs proof.** A green "200 OK" or "deploy succeeded" only means a page *loaded* — not that it did the right thing. Checking the actual database caught a payment bug; reading the build log caught the server quietly using the wrong Python version.
- **Pick one source of truth.** Storing subscription status in the database (written only by Stripe's signed webhook) — never a browser cookie — removed a whole class of bugs and cheats in one decision.
- **Cut the scope, then grow it.** My first plan was a huge, expensive vision. Real progress came from shipping a small working version first, then layering on accounts, payments and the AI.

---

## 🗺️ What's next

- **Move to a hosted database (Postgres).** The free host wipes the SQLite file on each restart, so accounts don't survive yet — and add database migrations.
- **Complete & verify PayPal.** Checkout is scaffolded; it needs sandbox credentials and a real test payment, the same way Stripe was verified.
- **Switch Stripe to live keys.** The full test flow already works end-to-end — going live just needs the real keys.

---

<p align="center"><em>🙏 May your practice bring wisdom and peace.</em></p>
