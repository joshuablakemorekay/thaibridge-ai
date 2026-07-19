# Prompt Changelog

Chronological record of prompt creation and refinement. Newest entries at the top.

Each entry follows this format:
- **Date** — what changed and why

---

## tones-consonant-classes

### 2026-07-19 — v1 (explore-first build)
**Change:** Added one free, unified "Tones & Consonant Classes" section — a `TONES_AND_CLASSES` data dict, a `/tones-classes` route, a template with reference tabs and four progressive drills, built on the `feature-experiment` branch.
**Reason:** Consonant classes only exist to determine tones, so teaching them as separate sections was confusing; the content also lived scattered across three places (one paywalled).
**Impact:** A single free reading skill that reuses the existing `/api/check_answer` XP scoring. Taught me the value of an explore-first gate — surveying the codebase and recommending merge-vs-rebuild *before* editing avoided duplicating content and kept the change from touching unrelated code.

---

## frontend-build

### 2025-11-19 — v3 (Option C)
**Change:** Added the interactive JavaScript layer — flashcards, progress saving, confetti, sounds, keyboard nav.
**Reason:** A static app isn't engaging; learners need feedback and persistence.
**Impact:** A genuinely interactive front end (and where the front-end bugs lived).

### 2025-11-19 — v2 (Option B)
**Change:** Moved styling into external CSS with a variable-based Thai theme and animations.
**Reason:** Inline styles were unmaintainable.
**Impact:** One place to change the whole colour scheme.

### 2025-11-19 — v1 (Option A)
**Change:** Generated the 6 core HTML templates with a deep-red / gold / cream theme.
**Reason:** Needed the actual pages on top of the Flask backend.
**Impact:** A working multi-page UI; taught me that pasting code into chat ≠ putting it in the project folder.

---

## gamification-system

### 2025-12-03 — v3 (templates added)
**Change:** Added the new templates (`progress`, `locked`, `developer_login`, `subscription_success`).
**Reason:** Routes throw `TemplateNotFound` until their templates exist.
**Impact:** Developer mode, progress dashboard and subscription tiers all working end to end.

### 2025-12-03 — v2 (integrated app)
**Change:** Merged the gamification into a single `app.py`.
**Reason:** The paste-in snippet couldn't run on its own.
**Impact:** Surfaced a duplicate `/formality` route that crashed startup until removed.

### 2025-12-03 — v1 (paste-in snippet)
**Change:** First version delivered as a `gamification_system.py` snippet.
**Reason:** Add XP/levels, locked sections, developer mode and subscriptions.
**Impact:** Hit `name 'app' is not defined` — a snippet has no Flask app to run on its own.

---

## thai-alphabet-exercises

### 2025-12-04 — v3 (progressive, no-cheat)
**Change:** Removed the "Show Answer" button, added romanization to every consonant, and split the exercise into an unlocking 5-level system.
**Reason:** The old exercise could be cheated and was overwhelming.
**Impact:** Learners now work for it, in manageable stages.

### 2025-12-04 — v2 (correct full order)
**Change:** Fixed the exercise to all 44 consonants in true Thai dictionary order.
**Reason:** v1 used only the first 10 and the wrong order.
**Impact:** The exercise teaches the real alphabet sequence.

### 2025-12-04 — v1 (alphabet + first exercise)
**Change:** Added the alphabet module (Level 1, required first) and a drag-and-drop ordering exercise.
**Reason:** Mastering the alphabet first is how you start learning Thai.
**Impact:** A gated first step, though the first exercise was incomplete.

---

## romanization-system

### 2025-12-09 — v3 (AI tutor match)
**Change:** Pinned the AI tutor's romanization to the app's house style (`khâ`→`kâ`, `ng`→`ŋ`, `thai`→`tai`).
**Reason:** The tutor used a different romanization than the app.
**Impact:** One consistent romanization everywhere.

### 2025-12-04 — v2 (display consistency)
**Change:** After several failed CSS attempts on the `ɔ̌ɔ` vowel, switched all romanization to a monospace font.
**Reason:** Combining diacritics render unevenly in proportional fonts.
**Impact:** Characters line up consistently — a pragmatic workaround, not a true typographic fix.

### 2025-11-19 — v1 (beginner mode)
**Change:** Added a beginner mode that swaps word-final single `i`→`y` and `o`→`w`, leaving vowel combos and double vowels alone.
**Reason:** Beginners misread final `i`/`o` as "ee"/"oh".
**Impact:** Clearer pronunciation cues, toggleable on/off.

---

## buddhist-pdf-integration

### 2026-02-19 — v2 (complete, faithful)
**Change:** Reproduced each essay in full on its own HTML page, every paragraph preserved, linked via new routes.
**Reason:** v1 quietly dropped paragraphs and reworded the text.
**Impact:** Faithful pages — *faithful means faithful*; check against the source, don't trust a summary.

### 2026-02-19 — v1 (dropped paragraphs)
**Change:** First attempt adding the "Pra Kru Bob's Writings" section.
**Reason:** Add two PDF essays to the Dharma page, styled.
**Impact:** Looked nice but abridged the content — not acceptable.

---

## ai-tutor-integration

### 2025-12-09 — v2 (running)
**Change:** Got the Claude-powered tutor actually working through a chain of setup fixes (Python, Flask, API key quoting, loading the key at the top of the file).
**Reason:** Phase 1 code was correct but wouldn't run as a beginner setup.
**Impact:** A live 6-mode tutor at `/chat`; biggest lesson — don't trust "it works" until you test it.

### 2025-12-08 — v1 (Phase 1 core)
**Change:** Built `ai_agent.py` (6 modes), `chat.html`, and integration routes.
**Reason:** Add an in-app AI tutor, built in phases.
**Impact:** The core chat system, ready to wire in.

---

## claude-code-workflow

### 2026-02-23 — tests & review
**Change:** Added 32 unit tests for the XP/level logic; ran a code review and fixed high-priority issues (HTTP 400s, try/except around the DB commit).
**Reason:** Make the gamification logic verifiable and the signup route robust.
**Impact:** A test suite and safer error handling; made two fixes by hand when Claude Code ran out of credits.

### 2026-02-22 — bug fix & refactor
**Change:** Fixed the empty-form submission bug (removed `novalidate`, added `required`) and refactored the signup `fetch` to async/await.
**Reason:** Build real features safely via Claude Code with a Git safety net.
**Impact:** Cleaner code and a clean commit history; decided to adopt feature branches + PRs going forward.

---

## market-research-report

### 2026-04-17 — v3
**Change:** Pinned a fixed 10-section structure and attached two source documents (a Product Overview and an analyst framing); kept the competitor-scraping instruction.
**Reason:** v2 was grounded but still freeform; I wanted a consistent, predictable report shape.
**Impact:** A consistently structured, source-backed report I could use to make a go/no-go decision.

### 2026-04-16 — v2
**Change:** Named the three competitors (ling-app.com, duolingo.com, thaipod101.com) and asked the model to scrape them with dedicated tools.
**Reason:** v1 was broad but not anchored to real rivals.
**Impact:** Concrete, current competitor analysis. Also surfaced a key lesson — naming a tool doesn't guarantee it runs; one scraping tool was never actually called.

### 2026-04-16 — v1
**Change:** Initial broad research request.
**Reason:** Needed a first read on the UK market for the app.
**Impact:** Good breadth, but ungrounded and unstructured.

---

## product-overview-section

### 2026-04-16 — v2
**Change:** Added answers to the model's three scoping questions (audience, emphasis, monetisation depth).
**Reason:** The bare brief left the angle ambiguous.
**Impact:** A full, structured five-part overview in one pass — later reused as a source document for the market research report.

### 2026-04-16 — v1
**Change:** Initial five-part brief (what it does / who it's for / features / problem / monetisation).
**Reason:** Needed a Product Overview section for the market research report.
**Impact:** Prompted the model to ask three scoping questions before writing.

---

## wireframe-layout-system

### 2026-06-06 — v3 (reusable distillation)
**Change:** Distilled the layout work into a reusable prompt — outline → per-page layout templates → reusable partials → responsive roll-out.
**Reason:** Capture the whole workflow in a form reusable on any multi-page project.
**Impact:** A documented site outline, three Jinja partials, the 3-column layout across Learn/Culture/Buddhism, and fill-or-scroll tables.

### 2026-06-06 — v2 (content-first)
**Change:** Switched from "stamp a wireframe on every page" to writing a content-first site outline first.
**Reason:** A wireframe is a planning tool, not a feature — plan content before styling.
**Impact:** A deliberate per-page plan instead of one forced layout.

### 2026-06-06 — v1 (all pages)
**Change:** First instinct — apply the wireframe layout to all pages.
**Reason:** Wanted a consistent look.
**Impact:** Would have made simple info and full-width pages look wrong; corrected by matching the layout to each page's job.

<!-- Add more entries above as the library grows. -->
