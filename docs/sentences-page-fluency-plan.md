# Sentences & Conversations — does it teach fluency?

*Review and plan, 2026-10-09.*

**Status (2026-10-09):** Steps 1–3 are built on branch `feat/sentences-fluency`. Josh chose the recommended order and hand-split tiles. The builder sits beside the Verb Practice table rather than replacing it. Steps 4–5 are not started.

The aim of `/sentences` is to teach learners to **put Thai sentences together
and speak**. This note checks the page against that aim and sets out what to
build, in what order, and what is Josh's call.

## The short answer

Partly. The page is good at **showing** Thai sentences — clear patterns, real
dialogues, audio, politeness levels. It almost never asks the learner to
**make** one. Fluency comes from producing sentences you haven't seen before,
and that step is missing.

## What already works

- **Tense markers** — กำลัง (ongoing), แล้ว (done), จะ (will), each with a
  pattern ("Subject + จะ + Verb") and male/female examples with audio.
- **Questions** — ไหม for yes/no, and question words for "what / where / when".
- **Ten real-life conversations** with audio. *Practice mode* hides the Thai so
  the learner has to say the line before checking it. That is real recall
  practice, and it's the best thing on the page.
- **Everyday "glue" phrases** (keeping a chat going, buying time, reacting).
- **Formal / Neutral / Casual** shown on each line — what makes speech sound
  natural rather than textbook.

## What's missing

### 1. Learners never build a sentence themselves
Every sentence on the page is finished. The verb table shows กำลังไป and
จะกิน, but nothing asks *"How would you say 'I will study'?"* and checks the
answer. This is the biggest gap.

### 2. Learners can't answer "no"
The page teaches how to **ask** "Do you want to go?" (ไปไหม) but never how to
**answer** it. In Thai you answer by repeating the verb — ไป (yes) or ไม่ไป
(no) — and that habit is one of the first things that makes a learner sound
fluent.

*Correction to what I said earlier:* negation isn't missing from the app.
The **Grammar** page (Level 3) has a Negation section with ไม่, ไม่มี,
ไม่ได้ and ยังไม่. But it is a four-row table with one-word examples, no
audio, and no ไม่ใช่ ("that's not it"). So the basics already have a home.
What's missing is how to *use* them in a reply.

### 3. Conversations are scripts
Practice mode tests whether you remember a fixed line. Real people go
off-script.

*Correction:* the AI tutor (`/chat`) **already has roleplay scenes** for 5 of
the 10 conversations: restaurant, market, taxi, directions, meeting. The
Sentences page just doesn't link to them. The temple, alms and meditation
scenes were left out of the tutor on purpose (Josh's call, 2026-07-23 — the
live model slips out of monastic register), so those three stay script-only.

### 4. No listening on its own
The Thai text and romanisation are always on screen, so a learner can read
instead of listening. Understanding spoken Thai is half of a conversation.

### 5. "Practice Suggestions" hands the job back
The box at the bottom says *record yourself, write sentences, transform
sentences* — all things the app could do itself.

## The plan

Smallest first, so something useful ships quickly and each step stays easy to
review.

### Step 1 — "Try it off-script" button (small) ✅ done
On each of the 5 conversations that have a matching roleplay, add a button
that opens `/chat` with that scene already chosen.

- **Sentences page:** a link like `/chat?scenario=restaurant` under the
  conversation, shown only when that id is in `ROLEPLAY_SCENARIOS`.
- **Chat page:** a few lines of JavaScript to read `?scenario=` and click the
  matching chip. The chips already exist (`templates/chat.html`). The server
  still looks the scene up by id, so nothing is trusted from the browser.
- **Why first:** it uses something already built and gets learners into
  free conversation straight away.

### Step 2 — "Answering questions" section (medium) ✅ done
Put it straight after Question Formation on the Sentences page — that's where
it belongs, not on a new page.

- Answer by repeating the verb: ไปไหม → ไป / ไม่ไป.
- ใช่ / ไม่ใช่ for "is it X?" questions.
- ยัง / ยังไม่ for "not yet" — the natural reply to a แล้ว question.
- ไม่ได้ + verb for "didn't".
- Male/female examples with audio, and Formal/Neutral/Casual levels, same as
  the rest of the page.
- One line linking to the Grammar page's Negation table for the rules.

**Watch out:** all new Thai is an unreviewed draft until a teacher has checked
it. Label it that way and add it to the next teacher review sheet.

### Step 3 — Sentence builder drill (biggest) ✅ done

Built as `sentence_builder.py` (21 hand-split sentences) plus `/api/sentence-builder` and `/api/sentence-builder/check`. A wrong answer reveals the right order by testing every pool answer against the stored token, so the order never reaches the browser.
The learner sees an English prompt and taps Thai word tiles into the right
order. The app marks it.

> *"I am eating"* → [ ผม ] [ กำลัง ] [ กิน ] [ ครับ ]

- **Where:** on the Sentences page, next to (or replacing) the Verb Practice
  table, since it drills the same patterns.
- **How the marking works:** use the existing server-side drill pattern
  (`/api/drill/<kind>` + `issue_question()`), so the answer stays on the
  server and XP falls under the daily drill cap. Don't repeat the old mistake
  of putting the answer in the page.
- **Particles follow the learner:** ผม/ครับ or ดิฉัน/ค่ะ from their gender
  setting, like the rest of the page.
- **Later:** a few wrong "decoy" tiles, and prompts that mix two markers
  ("I haven't eaten yet").

### Step 4 — Listening mode (small, once 1–3 exist)
A second toggle on each conversation that hides the Thai *and* the
romanisation and plays the audio. The learner picks or types the meaning.
Only offer it on lines that have a recording.

### Step 5 — Replace the Practice Suggestions box
Once Steps 1–4 exist, swap the "do it yourself" tips for buttons that open
them: *Build sentences → Try a scene → Listen only*.

## Decisions for Josh (all settled 2026-10-09)

1. **Order.** I suggest 1 → 2 → 3. Step 3 is the one that teaches the most,
   so if you'd rather start there, that's a sensible choice too.
2. **Where the builder's word tiles come from.** Thai has no spaces, so each
   sentence must be split into words somehow.
   - **Hand-written splits (recommended):** I write the tile list for each
     sentence. Accurate and checkable, but slower to add new sentences.
   - **Automatic splitting** with a Thai word-cutting library (PyThaiNLP).
     Faster, but it adds a large dependency and sometimes splits words wrongly
     — which would teach the wrong thing.
3. **How many builder sentences to start with.** About 20–30, all made from
   words the page already teaches, is enough to see if learners use it.
4. **Should the builder replace the Verb Practice table** or sit beside it?

## Before anyone edits

- On 2026-10-09 about 19 files had **uncommitted changes**, including
  `app.py`, `ai_agent.py` and `templates/base.html` — probably from another
  Claude session. Find out whose they are (or use a separate worktree) before
  touching those files.
- I haven't checked how many conversation lines actually have audio. Step 4
  depends on that.

## Still to do

- **Teacher check** of every new Thai line. The sheet is ready: `docs/sentences-review-2026-10-09.md` / `.html`, rebuilt from the live data by `scripts/make_sentences_review.py`. Not yet sent.
- Steps 4 and 5 above.
