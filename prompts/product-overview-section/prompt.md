# Product Overview Section

> **Category:** content
> **Model used:** Claude (Claude.ai)
> **Project area:** Thai Language & Culture Learning App — market research report input
> **Status:** production
> **Last updated:** 2026-04-16

## What this prompt does

Generates a structured Product Overview section for the app, in five parts: what it does, who it's for, key features, the problem it solves, and the monetisation idea. The model asks scoping questions first, then writes the section from the answers — so the output is shaped to the brief rather than guessed.

## The prompt

**The brief (verbatim):**

```
Can you produce a Product overview:
- What the app does
- Who it's for
- Key features
- Problem it solves
- Monetisation idea (if any)

This is for a market research report.
```

The model replied with three scoping questions (which audience to lead with,
which strength to emphasise, and how much monetisation detail to include).

**The answers that drove the final output (verbatim):**

```
all of the above 2. all of the above 3. Just high-level freemium + subscription
strategy for now.
```

## Inputs

- `audience_focus` — which audience segment(s) to prioritise
- `emphasis` — which differentiator(s) to lead on
- `monetisation_detail` — how much pricing detail to include

## Expected output

A markdown section with all five headings filled in. It should mention the main
audience segments (expats, tourists, heritage learners, Buddhists, business
professionals), describe the key features, state the problem clearly, and lay
out a high-level freemium + subscription model.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
