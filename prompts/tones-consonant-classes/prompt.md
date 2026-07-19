# Unified "Tones & Consonant Classes" Section

> **Category:** agent-workflow
> **Model used:** Claude (Claude Code, Opus)
> **Project area:** ThaiBridge AI — core reading skills (tones + consonant classes)
> **Status:** production — merged to `main` and live at https://thaibridge-ai.smoald.com/tones-classes
> **Last updated:** 2026-07-19

## What this prompt does

Drives Claude Code to build ONE free, unified learning section that teaches Thai consonant classes and tone rules together as a single skill — reusing the app's existing content and quiz/XP mechanics rather than building anything parallel. The prompt's defining feature is an **explore-first gate**: Claude must survey the codebase and recommend *merge vs rebuild* before it is allowed to edit anything.

## The prompt

**Full brief (verbatim):**

```
You are working on my Thai language learning Flask app (Python backend, Jinja2
HTML templates). I'm a beginner developer — explain your plan in plain language
before editing, and don't refactor anything unrelated.

## Goal
Create ONE unified learning section called "Tones & Consonant Classes" that
teaches consonant classes and tone rules together as a single skill (classes
exist only to determine tones, so they shouldn't be separate sections).

## Step 1 — Explore first, then propose add vs replace
Before writing any code, find my existing content on tones and/or consonant
classes (search app.py, any data/content files, and templates for: tone,
consonant class, high class, mid class, low class). Then tell me what exists
and recommend ONE of:
  a) Merge existing tone + consonant content into the new unified section, or
  b) Build the new section fresh and retire the old ones.
Wait for my confirmation before editing.

## Step 2 — Content the section must teach
Core concept: Thai tones aren't written directly — they're calculated from
(1) consonant class, (2) live/dead syllable, (3) tone mark. Consonant class is
the primary factor.
[...full class letter lists, the live/dead tone chart, the leading-ห rule,
contrast examples...]

## Step 3 — Practice drills (progressive levels within the section)
1. Class ID  2. Tone calculation  3. Contrast pairs  4. Leading ห drill
Reuse my existing quiz/XP/points mechanics — don't invent a new scoring system.

## Constraints
- Core learning content → FREE tier, no level gate.
- Match existing code style, route patterns (@require_access), template structure.
- Skip the obsolete letters ฃ and ฅ in drills (reference chart only).
- Don't add audio/AI features to this section — text-based drills only for now.

## Step 4 — Verify
Confirm the app imports/runs, then tell me how to test: the URL of the new
section, and check it's accessible logged out.
```

> The full brief also included the exact consonant letter lists per class, the complete live/dead-syllable tone chart, the leading-ห rule (มา vs หมา), and the contrast pairs (คา/ข่า, ไก่ series) — trimmed here for readability but supplied verbatim in the actual prompt.

## Inputs

- The existing `app.py` (`SECTION_REQUIREMENTS`, the `@require_access` decorator, the `/api/check_answer` scoring endpoint)
- Existing scattered content: `THAI_ALPHABET`, `GRAMMAR['consonant_classes']`, `PAIBOON_GUIDE`
- `vowels_syllables.html` as the template to copy the layout from

## Expected output

A new free `tones_classes` section: a `TONES_AND_CLASSES` data dict, a `/tones-classes` route, a `tones_classes.html` template with reference tabs and four progressive drills that post to the existing `/api/check_answer`, plus nav links — all without touching unrelated code.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
