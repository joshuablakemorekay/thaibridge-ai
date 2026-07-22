# Case Study — ThaiBridge AI

**Building a live, paid, AI-powered language app as my first web app — and proving every risky part actually works.**

🔗 **Live demo:** https://thaibridge-ai.smoald.com  ·  **Code:** https://github.com/joshuablakemorekay/thaibridge-ai

> *Heads-up for visitors: the demo runs on a free host that "sleeps" when idle, so the first page can take ~30 seconds to wake. The fastest thing to try is the [AI tutor](https://thaibridge-ai.smoald.com/chat) — no install or sign-up needed.*

---

## At a glance

| | |
|---|---|
| **My role** | Sole developer — designed and built it (with AI as a pair-programmer) |
| **Type** | My first web app · a learning project, built in public |
| **Timeline** | Nov 2025 → Jun 2026 (planning → live) |
| **Stack** | Python, Flask, SQLite, Flask-Login, Claude API, Stripe, HTML/CSS/JS, pytest |
| **Status** | Live and public; core features verified end-to-end |
| **Headline proof** | Real test payment verified · 32 automated tests passing · live AI demo capped at £/$ a few pounds a month |

---

## The problem

I'm learning Thai, and the popular apps fail Thai learners in a specific way. **They don't teach Thai well, and none of them connect the language to its culture** — which, in Thai, is half the language. How polite you are literally changes the words you use, and a lot of everyday speech is rooted in Buddhism.

I also set myself a harder problem than "make a website." **As a beginner, I wanted to prove I could build the parts a real online product actually needs** — proper accounts, real payments, and a genuinely useful feature — not another to-do-list demo. The risk: those are exactly the parts that are easy to fake and hard to get right.

## My approach

I worked in public, kept an honest build journal, and made a few deliberate calls early that shaped everything after.

**1. I cut a huge plan down to something I could ship.** My first design was a big, expensive vision. Real progress only came when I shrank it to a minimum working version (an MVP — the smallest useful version), got *that* live, then layered on accounts, payments and the AI one at a time.

**2. I chose one source of truth for "who has paid."** Anything the browser can edit, a user can fake. So I decided that **the database — and only the database — owns subscription status**, and the database is written only by a signed, server-to-server message from Stripe (a webhook). A tampered cookie can't unlock paid features. This single decision removed a whole category of cheats and bugs.

**3. I refused to trust "it works."** This became the spine of the whole project. A green "deploy succeeded" or a "200 OK" only means a page *loaded* — not that it did the right thing. So I made a habit of checking the real evidence: the database, the logs, the actual screen. That habit paid off repeatedly (see Results).

**4. I made a values call on pricing — and then refined where the line sits.** The **Buddhist teachings are completely free** for everyone (no account, no paywall — *dāna*, freely given), and monastics get the entire app free through Monk Mode. My first version put the meditation page on the free side too. As it grew from a bare timer into guided sessions and full technique guides, I moved it to the paid tier: **the teaching stays free, the tooling built on top of it is the product.** That line is easier to defend and easier to explain than "meditation is free but Thai grammar isn't" — and working out *where* a values line actually falls turned out to be harder, and more useful, than declaring one.

## What I built

ThaiBridge AI is a server-rendered Flask app with:

- 🔤 **Vocabulary lessons**, written so complete beginners can read straight away
- 🤖 **An AI tutor with six modes** — conversation, grammar, quiz generation, culture, Buddhism and gentle hints — powered by the Claude API, with a strict shared pronunciation rulebook injected into every prompt so the romanization stays consistent
- 📚 **Lessons, grammar, culture and temple-etiquette modules**, plus Theravada teachings (free for all) and guided meditation sessions
- 🔐 **Real user accounts** — proper sign-up, log-in and log-out, with passwords stored safely (hashed)
- 💳 **Freemium subscriptions** (Free · Buddhist Scholar £9.99 · Thai Master £19.99) through Stripe
- 🏆 **Gamification** — points, levels and achievements, with a learning path that unlocks as you go

## Results & evidence

This is the part I care about most — not "I built it," but "here's the proof it works."

- **Payments work end-to-end, and I can prove it.** I took a real test-card payment through Stripe Checkout and confirmed the webhook flipped the user to a paid plan **in the database**, with a genuine Stripe customer and subscription ID attached — not just a "success" screen.
- **Checking the database caught a real bug.** The payment *looked* fine, but the renewal date was never being saved: Stripe had moved that value onto each subscription *item*, so my code was reading an empty field. **I'd never have caught it by trusting the success page** — only by inspecting the actual data. Found, fixed, re-tested.
- **32 automated tests pass.** The points-and-levels engine is covered by 32 unit tests — level thresholds, the 1× / 2× / 3× points multipliers per plan, level-up detection across boundaries, and progress-bar maths. *(Run `python -m pytest tests/ -v` → `32 passed`.)*
- **The build prompts are tested too.** An evaluation harness checks the ten prompts behind the app's features against written rubrics — **all ten pass at 100%.**
- **It's live, and the AI costs are walled off.** The public demo runs a cheap model, has a **hard monthly spend ceiling**, a **separate API key as a kill switch**, a per-visitor daily message cap, and an uptime pinger to keep it warm. A bad day can't run up my card.
- **It works on any screen.** I audited the layout across seven widths from a 320px phone upward and fixed a CSS specificity bug so every page collapses cleanly to one column — **zero sideways scroll**, desktop unchanged.
- **Scale & workflow:** ~6,100-line Flask app, a ~500-line AI module, 61 routes, ~30 pages, and a real ~4,894-entry English–Thai dictionary. The big recent work landed as a 44-commit feature branch merged cleanly into `main`, and I shipped my first proper pull request with a green automated check before merging.

## What I learned

- **"It works" needs proof.** The database, the logs and my own eyes are the real test — not a green tick. This one habit caught a payment bug, a wrong-Python-version deploy, and saved me from shipping broken billing.
- **Decide who owns each fact.** "Source of truth" sounds abstract until it quietly deletes a whole class of bugs and cheats for you.
- **Ship small, then grow.** A small thing that works beats a big thing that doesn't — every time.
- **Version control turns fear into freedom.** Because I could always roll back, I could take big swings (and let an AI take them) without panic.

## What's next

- **Move to a database that survives restarts** (the free host wipes the current one on redeploy) and add proper database migrations.
- **Finish and verify a second payment option** (PayPal), the same careful, test-it-end-to-end way Stripe was done.
- **Switch Stripe to live keys** — the full test flow already works, so going live is the last step, not a rebuild.

---

*ThaiBridge AI is my first web app and an ongoing learning project. It's live, the core is verified, and I'm still building it in the open. The full build story — every win and mistake — is in [`JOURNAL.md`](https://github.com/joshuablakemorekay/thaibridge-ai/blob/main/JOURNAL.md).*
