# Case Study — ThaiBridge AI

**Building a live, paid, AI-powered language app as my first web app — and proving every risky part actually works.**

🔗 **Live demo:** https://thaibridge-ai.smoald.com  ·  **Code:** https://github.com/joshuablakemorekay/thaibridge-ai

> *Heads-up for visitors: the demo runs on a free host that "sleeps" when idle, so the first page can take ~30 seconds to wake. The fastest thing to try is the [AI tutor](https://thaibridge-ai.smoald.com/chat) — no install or sign-up needed.*

---

## At a glance

| | |
|---|---|
| **My role** | Sole developer — direction, judgement and review; Claude Code as the agent doing the typing |
| **Type** | My first web app · a learning project, built in public |
| **Timeline** | Nov 2025 → live Jun 2026 · still building |
| **Stack** | Python, Flask, Postgres (Neon) / SQLite, Flask-Login, Claude API, Stripe, HTML/CSS/JS, pytest |
| **Scale** | 8,775-line Flask app · 84 routes · 1,256 automated tests · ~5,000-entry Thai dictionary |
| **Headline proof** | Real test payment verified in the database · 1,256 tests passing · 19 build prompts under an eval harness, all passing |

---

## The problem

I'm learning Thai, and the popular apps fail Thai learners in a specific way. **They don't teach Thai well, and none of them connect the language to its culture** — which, in Thai, is half the language.

I also set myself a harder problem than "make a website." **As a beginner developer, I wanted to prove I could build the parts a real online product actually needs** — proper accounts, real payments, and a genuinely useful AI feature — not another to-do-list demo. Those are exactly the parts that are easy to fake and hard to get right.

## Who it's for

The core audience is anyone standing on the English side of that bridge and wanting to cross:

- **Expats and long-stay foreigners in Thailand** — the largest group, and the most frustrated
- **Foreign monks and Buddhist practitioners** — served by a dedicated Monk Mode, free
- **Tourists, retreat visitors and digital nomads** who want more than phrasebook Thai
- **Thai diaspora and heritage learners** reconnecting with a family language
- **Students, and parents teaching children** — the alphabet track is built for absolute beginners
- **General language learners** drawn in by the culture as much as the language

## My approach

I worked in public, kept an honest build journal, and made a few deliberate calls early that shaped everything after.

**1. I cut a huge plan down to something I could ship.** My first design was a big, expensive vision. Real progress only came when I shrank it to a minimum working version (an MVP — the smallest useful version), got *that* live, then layered on accounts, payments and the AI one at a time.

**2. I chose one source of truth for "who has paid."** Anything the browser can edit, a user can fake. So the database — and only the database — owns subscription status, and it's written only by a signed, server-to-server message from Stripe (a webhook). A tampered cookie can't unlock paid features. This single decision removed a whole category of cheats and bugs.

**3. I refused to trust "it works."** A green "deploy succeeded" only means a page *loaded* — not that it did the right thing. So I built the habit of checking the real evidence: the database, the logs, the actual screen.

**4. I made a values call on pricing — then moved the line twice.** The Buddhist teachings are free for everyone, no account and no paywall (*dāna* — freely given), and monastics get the entire app free through Monk Mode.

Meditation started free, then went paid as it grew from a bare timer into guided sessions. I told myself the teaching was free and the tooling was the product. That didn't survive contact with the actual question: sitting in meditation isn't tooling, it's the practice the teachings exist for, and "the Dhamma is free but learning to practise it costs £9.99" is not a line I could defend. So meditation is free again.

The same line moved once more when I noticed the AI's Dhamma mode was still Pro-only — a reader could reach the free teachings and then hit a paywall asking a question about them. It's free now. The daily message cap stays, because every AI message costs real money to run, but that's the cost of the model, not a toll on the teaching.

Working out *where* a values line actually falls turned out to be harder — and more useful — than declaring one.

**5. I worked with an AI agent, not from its answers.** Rather than pasting chatbot replies in, I used Claude Code as an agent that explores the project, plans, edits files, runs tests and reports back. My job is the other half: set direction, make the judgement calls, review every diff, approve what ships.

That division only works if the review is real. The clearest proof is a change that stripped the indentation off 83 lines, imported cleanly and passed every test — because Python doesn't care about whitespace inside a dict literal. Nothing automated caught it. Reading the diff did.

## What I built

ThaiBridge AI is a server-rendered Flask app.

### The Thai language track

- **Thai Alphabet (free)** — all 44 consonants with tap-to-hear audio, flashcards and a 44-question quiz, each letter illustrated with a hand-drawn icon of its namesake word (ก is *gɔɔ gài*, chicken — so ก shows a chicken). Passing unlocks the rest of the site.
- **Read & Write Thai Script** — a reading trainer for how Thai vowels sit before, above, below or around their consonant; a trace-over-the-guide canvas for all 42 written letters; and graded Jataka stories building up to real, unsimplified Thai.
- **Tones & Consonant Classes** — taught together, because they're really one skill, with four progressive drills.
- **Sentences built for speaking** — every line in three registers (formal, neutral, casual), because the polite register is the right thing to learn first and not how most Thai is actually spoken. Dialogues with monks get a monastic note instead of a casual form, since speaking to a monk swaps the vocabulary rather than sliding down the ladder.
- **Tap-to-hear audio site-wide** — generated once and committed as ordinary files, so the live site needs no speech service and has no per-play cost.

### The AI tutor

Six modes — conversation, grammar, quiz generation, culture, Buddhism and gentle hints — powered by the Claude API, with a shared pronunciation rulebook injected into every prompt so the romanisation stays consistent. Plus scenario roleplay: pick a scene (restaurant, market, taxi) and the AI stays in character while you practise.

### The Buddhist side (free for everyone)

- **Digital Chanting Book** — Thai Buddhist chants in five toggleable layers: Pali in Thai script, romanised Pali, Thai translation, Paiboon+ romanisation, and English meaning. One page serving two different books. **101 chants and 1,495 verses** transcribed so far, with page numbers matching the physical book — because a monk calls out "page 47" and a digital book that can't answer that has failed at the job.
- **Dhamma Talks** — talks by the monks behind the site, published in Thai and English side by side.
- **Monk Mode** — a free lesson track for Buddhist monks, switchable between learning Thai and learning English, with native audio in British or American English (252 files per accent).

### The product infrastructure

Real user accounts with hashed passwords; Stripe subscriptions (Free · Thai Reader £9.99 · Thai Master £19.99, plus a one-time £14.99 Instant Access Pass); gamification with points, levels and achievements; and a Learning Support accessibility panel offering dyslexia-friendly fonts, spacing controls and read-aloud.

## The engineering worth naming

Adding a chant is a three-stage workflow that reads photographs of the physical book off disk. Stage 1 reads a batch of pages and writes what it found to a file; Stage 2 reads that file and writes the chants in, counting every Thai character both ways to prove nothing was added or dropped; Stage 3 writes the commentary separately.

The stages stay apart on purpose: one pass that reads a photograph and writes the chant in the same breath would be marking its own homework. So Stage 1 may not touch the app, and Stage 2 may not open the photographs. Nothing crosses a clipboard, because Thai script, IAST diacritics and Paiboon+ vowels are exactly the characters copy-paste damages quietly.

Checking scripts back this up. The newest is the only one that renders the actual page, because correct data can still render badly, and a block dropped by a template is invisible to the other three.

## Results & evidence

Not "I built it" — here's the proof it works.

- **Payments work end-to-end, and I can prove it.** A real test-card payment through Stripe Checkout, confirmed by checking the *database*: the webhook flipped the user to a paid plan with a genuine Stripe customer and subscription ID attached. Not just a success screen.
- **Checking the database caught a real bug.** The payment *looked* fine, but the renewal date was never saved — Stripe had moved that value onto each subscription *item*, so my code was reading an empty field. Invisible from the success page. Found by inspecting the data, fixed, re-tested.
- **Reading the diff caught what tests couldn't.** A change stripped the indentation off 83 lines. It imported cleanly and passed the entire suite, because Python doesn't care about whitespace inside a dict literal. No automated check would ever have found it.
- **1,256 automated tests pass**, covering the points-and-levels engine, access gating, the chanting pages and the register system.
- **The build prompts are tested too.** 19 prompts behind the app's features run against written rubrics in an evaluation harness — all passing at 100%.
- **The AI costs are walled off.** A cheap model on the public demo, a hard monthly spend ceiling, a separate API key as a kill switch, and a per-visitor daily message cap. A bad day can't run up my card.
- **The data survives now.** Production moved from a disk the host wipes on redeploy to managed Postgres on Neon; the app picks its database from `DATABASE_URL`, so laptops and the test suite still run on SQLite with no config.
- **Audio is free to serve.** 942 Thai phrase clips and 252 English files per accent, generated once and committed as ordinary files — the live site needs no speech service and pays nothing per play.
- **It works on any screen.** I audited the layout across seven widths from a 320px phone upward and fixed a CSS specificity bug so every page collapses cleanly to one column — zero sideways scroll, desktop unchanged.

## Honest limits

- **This is not scripture.** The chanting book, translations and Dhamma content are a learner's aid transcribed from one physical Thai chanting book. They are nowhere near the accuracy of the official Pali Canon (Tipiṭaka), and don't intend to be. Anyone doing serious study should go to the canonical sources.
- **The romanised Pali and Paiboon+ are unreviewed drafts.** Flagged items are still to be checked line by line against the printed copy — each naming the photograph it came from, so the page can be found again.
- **Some chants are printed Pali-only** with no Thai translation beside them. Those say so on the page, so nobody mistakes a working English translation for the book's own words.
- **The project is unfunded.** It is built and maintained by one developer alongside the monastic community that supplies its content.

## Why the Buddhist content is there

The app has drawn some criticism for its Buddhist material on grounds of balance, and it's worth answering plainly.

Buddhism is in ThaiBridge AI because it is structurally inside the Thai language. Register, honorifics, everyday idiom and a large share of formal vocabulary can't be explained without it. Removing it wouldn't make the app neutral — it would make it inaccurate.

What follows from that:

- **Nothing requires belief.** Every Buddhist section is free and open, with no account needed. Nothing is gated behind agreement.
- **The language track stands alone.** A learner who wants only Thai can take the alphabet, script, tones and conversation tracks without touching the Dhamma material.
- **Context is taught as context.** When the app explains why a word changes for a monk, it's teaching a rule of Thai, not making a claim about the world.
- **The source is credited and its limits stated**, rather than presented as authority.

## What I learned

- **"It works" needs proof.** The database, the logs and my own eyes are the real test — not a green tick. This one habit caught a payment bug, a wrong-Python-version deploy, and saved me from shipping broken billing.
- **Decide who owns each fact.** "Source of truth" sounds abstract until it quietly deletes a whole class of bugs and cheats for you.
- **Ship small, then grow.** A small thing that works beats a big thing that doesn't — every time.
- **Version control turns fear into freedom.** Because I could always roll back, I could take big swings (and let an AI take them) without panic.
- **An agent is only as good as the review.** The 83-line indentation catch is the whole argument for reading every diff.

## What's next

- **Switch Stripe from test to live keys** — the full test flow already works, so going live is the last step, not a rebuild.
- **Work through the flagged romanisation items** line by line against the printed book.
- **Finish transcribing the remaining pages** of the chanting book.

---

*ThaiBridge AI is my first web app and an ongoing learning project. It's live, the core is verified, and I'm still building it in the open. The full build story — every win and mistake — is in [`JOURNAL.md`](https://github.com/joshuablakemorekay/thaibridge-ai/blob/main/JOURNAL.md).*
