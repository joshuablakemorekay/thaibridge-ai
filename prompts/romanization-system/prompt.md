# Paiboon+ Romanization System (Beginner Mode, Display & Consistency)

> **Category:** code-generation
> **Model used:** Claude (Claude.ai, artifact generation)
> **Project area:** Thai Language & Culture Learning App — custom romanization
> **Status:** production (system still being actively refined)
> **Last updated:** 2025-12-09

## What this prompt does

Refines the app's custom Paiboon+ romanization: a beginner mode that swaps confusing final letters, consistent rendering of the special vowel/tone characters across the whole app, and aligning the AI tutor's romanization to the app's house style.

## The prompt

Several related requests refined the system over time.

**Beginner mode (verbatim):**

```
Firstly, for the romanized text, would it be possible to replace the letter i
to y & o to w but only for the final letters at the end of a word that contains
a single i & a single o? If yes, can we create a beginner mode that applies
this? It helps beginners avoid confusion.
```

**Vowel display consistency (verbatim):**

```
Can you fix the problem with this vowel - ɔ̌ɔ? The symbols don't match for all
ɔɔ long vowel combinations. They should be the exact same size & shape
throughout.
```

followed by:

```
Can you implement the fix for this vowel combination for the entire web app?
```

**Match the AI tutor (verbatim):**

```
In AI Chat: Remove h in khâ & thîi. Replace ng with ŋ in yang-ngai...
Fix the IPA characters so they are same font + size.
```

## Inputs

- The app's custom Paiboon+ vowel set (documented in [`REASONING.md`](./REASONING.md))
- Paiboon romanized strings to transform (beginner mode) or render (display)
- The AI tutor's system prompt (to align its romanization)

## Expected output

A beginner-mode toggle that swaps word-final single `i`→`y` and `o`→`w` without touching vowel combos or double vowels; CSS that renders the special characters (`ʉ`, `ɛ`, `ɔ`, `ə` and combining tone marks) at a consistent size everywhere; and an AI tutor whose romanization matches the app's house style.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
