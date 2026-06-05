# Wireframe Layout System (content-first, per-page templates)

> **Category:** code-generation
> **Model used:** Claude (Claude Code)
> **Project area:** ThaiBridge AI — front-end layout
> **Status:** production
> **Last updated:** 2026-06-06

## What this prompt does

Designs a consistent, **content-first** layout system for a multi-page web app: a written site outline, a small set of layout "shapes" matched to each page's job, implemented with reusable template partials and rolled out page by page — kept responsive so wide content never gets clipped.

## The prompt

This was an iterative, staged build driven from Claude Code. Unlike a single crafted prompt, it was **distilled from a back-and-forth session** — so the real verbatim turns are quoted below, followed by the generalised version worth reusing.

**v1 — the starting question (verbatim):**

```
Should the wireframe layout be applied to all pages? If yes. Instruction: Add the wireframe layout to all pages.
```

**v2 — switch to content-first (verbatim):**

```
Start with the outline so the plan is on paper first
```

**v3 — roll it out (verbatim):**

```
Roll the 3-column layout out to the other Learn pages, Culture, Buddhism
```

**Reusable distillation (what to reuse on a new project):**

```
Design a content-first layout system for my multi-page web app.

1. First write a site outline: list every page and what each page is FOR (its
   job and key content) — before any styling.
2. Define a small set of layout templates, each matched to a page's job — e.g.
   Landing (the front door), 3-column content (reference pages with a sidebar
   and extras), Simple centered (short info pages / forms), Full-width tool
   (interactive apps). Don't force one layout on every page.
3. Implement the shared layout with reusable partials (e.g. a sidebar and a
   right-column include) so each page opts in by filling named blocks, with the
   current page highlighted automatically.
4. Roll it out page by page.
5. Keep it responsive: wide content (tables) should fill the column when there's
   room and scroll sideways when it doesn't — at any zoom — never clip.
```

## Inputs

- An existing multi-page app (here: a Flask/Jinja app) with its routes and templates
- A web-design method: **content-first outline → wireframe** (the "create an outline" step before styling)
- The list of pages and what each one is for

## Expected output

- A written **site outline** document (e.g. `docs/SITE_OUTLINE.md`)
- A shared base layout with **optional named blocks** (sidebar / main / right column)
- **Reusable partials** for each shared region, with automatic active-page highlighting
- The chosen layout applied to the **right** pages, kept **responsive** (fill-or-scroll tables)

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
