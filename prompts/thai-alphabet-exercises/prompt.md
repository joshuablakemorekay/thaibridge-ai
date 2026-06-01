# Thai Alphabet Module & Ordering Exercises

> **Category:** code-generation
> **Model used:** Claude (Claude.ai, artifact generation)
> **Project area:** Thai Language & Culture Learning App — alphabet learning & practice
> **Status:** production
> **Last updated:** 2025-12-04

## What this prompt does

Adds a complete Thai alphabet section (44 consonants, vowels, tone marks) available to Level 1 users, makes completing it a prerequisite for the rest of the app, and provides an interactive drag-and-drop exercise for learning the alphabet's order.

## The prompt

**Add the alphabet as a gated first step (verbatim):**

```
Can we add the Thai Alphabet & make it accessible to Level 1 users. Make
alphabet completion requirement before moving onto anything else.
```

**Improve the practice exercise (verbatim):**

```
For Thai alphabet exercise: Don't show all answers. Make user work for it.
Add Romanised translation for every consonant. Either improve the existing
exercise or change to a more effective one?
```

> (The same turn that introduced the alphabet also asked to fix romanization spacing — that thread is archived under [`romanization-system`](../romanization-system/).)

## Inputs

- The existing gamified `app.py` and its level/locking system
- The full Thai alphabet data (consonants by class, vowel forms, tone marks)
- The correct Thai dictionary ordering of the 44 consonants

## Expected output

An `alphabet.html` page covering consonants, vowels and tone marks; backend changes making the alphabet accessible at Level 1 and required before other sections unlock; and a progressive drag-and-drop ordering exercise with no "Show Answer" button and romanization shown on every consonant card.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
