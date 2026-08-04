# v1 — the batch fork

**2026-08-04** · Forked from `chanting-book-entry` v4, left unchanged.

## The request

```
I want to copy paste approximately 300 pages full of chants from a Thai script
chanting book. Can we modify Stage 1 and/or Stage 2 prompts so that they are
able to handle say 5-10 or 10-20 pages Stage 1 could possibly handle in a
Claude.ai chat?
```

```
I counted 286 chants. Can we keep [the existing prompts] as is in GitHub for
chant by chant projects. I would also like duplicate it and modify it so we can
do 5-10 chants with Stage 1. Stage 2 should then be able to handle the output.
```

## What changed

Measured first: an entry is **×9.1** the paste, Thai/IAST/Paiboon+ run
**1.91 chars/token**, the book is ~1.09M output tokens. **The ceiling is
arithmetic, not wording** — so 10–20 pages was refused rather than faked. Only
~36% of an entry is fidelity-critical, which is what the depth setting trades.

Added: three depths; a manifest declared **before** the entries; per-chant
`checks`; a Paiboon+ self-scan. Freezing the one-chant prompt was Josh's call.

## Lesson

**All 17 criteria passed at 100%, and that proved nothing until they were fed
deliberately broken input** — which exposed an inherited check that had never
caught a real error.
