# Dhamma AI Allowance — Check a Stated Principle Against the Code That Runs

**Category:** analysis
**Model:** Claude (Opus)
**Project area:** `FREE_AI_DAILY_LIMIT`, `/api/ai/chat`, `templates/chat.html`
**Status:** shipped 2026-08-19 — `be35854`, live

---

## Final prompt

> This site's position is that the Dhamma is free, and that charging for the
> follow-up question would be selling the teaching. That position is written
> down in a comment above the AI daily limit.
>
> Check whether the code actually honours it.
>
> Read the gate in `/api/ai/chat` and the counter behind it. Work out what
> happens to a learner who spends the day's allowance on Thai vocabulary and
> then asks a question about the precepts. Tell me what they are shown.
>
> If the principle is being broken, treat it as a bug rather than a feature
> request, and propose the smallest fix that honours it. Cost the fix using the
> per-message figure already in the file — do not estimate.
>
> One constraint: any fix must not take something away from anyone. If the only
> way to fund it is to reduce an existing allowance, tell me that instead of
> doing it quietly.
>
> Check the user-facing wording too, not just the gate. A refusal that upsells
> is the same charge by another name.

---

## Why this prompt is shaped this way

**"Check whether the code actually honours it"** is the entire prompt. The
principle was already written down, clearly, in a comment. The gate underneath
it did something else. Nobody had put the two side by side.

**"Treat it as a bug rather than a feature request"** changes the fix. A feature
request gets weighed against other features; a broken promise gets fixed.

**"Must not take something away from anyone"** ruled out the tidy answer.
Reserving 5 of the existing 15 for the Dhamma would have cost nothing and cut
everyone's tutor allowance from 15 to 10 — funding a promise the site had
already made by taking something back.

**"Check the user-facing wording too"** is what caught the second half. Fixing
the gate but leaving "Go Pro for unlimited →" beside the remaining Dhamma
questions would have kept the sales pitch and moved the counter.
