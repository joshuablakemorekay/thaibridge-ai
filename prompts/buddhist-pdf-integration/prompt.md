# Buddhist PDF Integration (Pra Kru Bob's Writings)

> **Category:** content
> **Model used:** Claude (Claude.ai, artifact generation)
> **Project area:** Thai Language & Culture Learning App — Buddhist Dharma content
> **Status:** production
> **Last updated:** 2026-02-19

## What this prompt does

Adds a "Pra Kru Bob's Writings" section to the Buddhist Dharma page, reproducing two of Pra Kru Bob's essays from PDFs exactly — every word and paragraph preserved — as styled HTML pages.

## The prompt

**The request (verbatim):**

```
Add new section called Pra Kru Bob's Writings to the Buddhist Dharma page. Add
both of these PDF documents to it. Make sure they appear exactly as they are
written and with the exact same style as they are in the PDFs. Don't change any
of the wording. Maybe add colours and make it look more stylish if possible.
```

**The correction when paragraphs went missing (verbatim):**

```
There are paragraphs missing. They are not the same as they are in the PDFs. I
told you specifically not to change the wording. I want all the words and
paragraphs added as they originally are.
```

## Inputs

- Two PDF documents (Pra Kru Bob's essays: a children's Buddhism overview, and "Fear as Guardian and Tyrant")
- The existing `theravada.html` Buddhist Dharma page
- A styling brief: keep the original wording exactly; add colour and make it stylish

## Expected output

Two complete HTML article pages containing the full, unaltered text of each PDF (no dropped paragraphs, no reworded sentences), linked from the Dharma page, with new Flask routes — plus visible (gold) navigation buttons.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
