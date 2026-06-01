# Frontend Build (Templates, Styling, Interactivity)

> **Category:** code-generation
> **Model used:** Claude (Claude.ai, artifact generation)
> **Project area:** Thai Language & Culture Learning App — front-end layer
> **Status:** production
> **Last updated:** 2025-11-19

## What this prompt does

Generates the app's front end in three deliberate stages — HTML templates, then external CSS with a Thai theme, then interactive JavaScript — built on top of the existing Flask backend.

## The prompt

This was a staged build. The assistant offered a menu of options (A = HTML templates, B = enhanced CSS, C = JavaScript features, D = deployment), and each stage was triggered with a short go-ahead after the previous one was reviewed.

**Stage 1 — templates (verbatim):**

```
Yes. Create Option A now. Create other Option B, C, D later
```

**Stage 2 — styling (verbatim):**

```
Yes. Create Option B. Create Options C, D later
```

**Stage 3 — interactivity (verbatim):**

```
Yes, lets do Option C now. Do Option D later
```

## Inputs

- The existing Flask `app.py` with its routes and vocabulary data
- A design brief: *"Elegant. Simplistic. Modern. Natural colours of Thailand... Buddhism/Monastic/Mythology"* — realised as a deep-red / gold / cream theme
- The chosen option letter (A, B, or C) for each stage

## Expected output

For **Option A**: a set of Jinja2 templates that each extend a shared `base.html`, use the Thai colour theme, and include the quiz interface. For **Option B**: external CSS with a variable-based theme and animations. For **Option C**: JavaScript for flashcards, progress saving, and quiz feedback.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
