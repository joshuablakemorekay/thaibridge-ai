# Reasoning — Meta AI Post Prompts

**Date:** 2026-09-17
**Commits:** none — the prompts were run in Meta AI, not in this codebase

> Review of this file was delegated — *"just do it"* — so it is drafted from
> the session rather than signed off line by line. The quotes are word-for-word.

---

## Goal

Fill in the course's two GenAI templates — one for the post's text, one for
its image — for ThaiBridge AI, so they can be pasted into Meta AI as the
activity asks. The whole brief was the activity text and four words:

> Do this for ThaiBridge-AI

## Iteration history

**v1 — as run.** Both prompts were drafted once and pasted into Meta AI. What shaped them was
not iteration but reuse: the four coursework documents from two days earlier
had already settled the persona, the platform and the decision to show the
paid Sentences page rather than the free chanting book, so the templates were
filled from those facts instead of from scratch. The brand colours came from
`static/css/base.css`.

**v2 — the CTA domain.** v1's call to action pointed at
`thaibridge-ai.onrender.com`, the Render hosting URL, while the live site and
all four coursework documents use `thaibridge-ai.smoald.com`. Corrected, with
v1 kept in `versions/` because the way it was found is worth recording: not by
re-reading the prompt, but by writing the rubric and asking what a *wrong*
output would look like. The image prompt is unchanged — it carries no URL.

## Failure modes the prompts handle

- A generic "learn Thai" post — handled by making the key message the three
  politeness levels, the one thing the paid page does that the persona was
  burned by elsewhere.
- Over-promising — *"Do not promise fluency; promise confidence."*
- Image models inventing Thai script — *"Keep any Thai script accurate or
  leave it out entirely."*
- Stock-tourist imagery for an audience with Thai family — *"No stock-photo
  smiling tourists."*
- American spelling in a British founder's voice — the prompt asks for
  British spelling outright.

## Outcome

The author ran both prompts in Meta AI and **reworked the output** before it
was usable. What Meta AI produced, and what he changed, were not pasted back
into this session, so this folder cannot show the before and after.

> TODO: paste Meta AI's text output and describe the image, and note what was
> changed before posting — that is the receipt this entry is missing.

One flaw is recorded rather than hidden: the version that was actually run
pointed the CTA at the Render hosting URL, `thaibridge-ai.onrender.com`, when
the live site and all four coursework documents use `thaibridge-ai.smoald.com`.
v2 fixes it, v1 stays in `versions/`, and the rubric now fails any output
carrying the hosting URL.

## Engineering on the output

- **Accepted as-is:** not known — the prompts themselves went into Meta AI as
  drafted.

- **Reworked, and why:** the author says he reworked Meta AI's output before
  he would post it. Which parts, and why, were **not captured**.

- **Roughly:** not tracked.

Recorded plainly. A folder that guessed at a proportion here would be worth
less than one that says it doesn't know.

## What I'd change next

- Capture Meta AI's raw output and the edited version side by side — the
  activity is *about* that comparison, and this entry has the prompt but not
  the receipt.

**Tags:** `content` `marketing` `coursework` `meta-ai` `template-fill` `not-tracked` `caught-by-its-own-rubric`
