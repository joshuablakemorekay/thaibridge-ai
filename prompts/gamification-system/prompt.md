# Gamification & Subscription System

> **Category:** code-generation
> **Model used:** Claude (Claude.ai, artifact generation)
> **Project area:** Thai Language & Culture Learning App — progression & monetisation
> **Status:** production
> **Last updated:** 2025-12-03

## What this prompt does

Adds a points-based progression system to the app: learners earn XP to unlock sections in a logical order, a hidden developer mode bypasses all locks for testing, and three subscription tiers gate the premium content.

## The prompt

**The request (verbatim):**

```
Make app challenging. Earn points to unlock new sections. Gamify it in a way
that makes sense logically. Add developer mode for me only so I can access
everything but add the challenging mode which for users. Can we add a
subscription system to this?
```

## Inputs

- The existing Flask `app.py` with its routes and content sections
- A desired progression order (basics → intermediate → advanced → premium)
- A developer password for the bypass mode
- Subscription tier definitions (Free, Buddhist Scholar £9.99, Thai Master £19.99)

## Expected output

Flask code (merged into `app.py`, not a standalone file) that defines an XP/level system, a `require_access`-style gate that locks sections behind a level, a password-protected developer mode that bypasses the locks, and subscription tiers — plus the supporting templates (`progress.html`, `locked.html`, `developer_login.html`, `subscription_success.html`).

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
