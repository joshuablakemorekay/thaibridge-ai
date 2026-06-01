# Reasoning: Gamification & Subscription System

## Goal

Turn the app from a flat set of pages into something challenging and motivating — earn points (XP) to unlock new sections in a logical learning order. I also wanted a **developer mode just for me** to bypass all the locks while testing, a **challenging mode for real users**, and a **subscription system** to monetise the premium content.

## Iteration history

**v1 — as a paste-in snippet:** the gamification came as a separate `gamification_system.py` to paste into `app.py`. I tried to *run* that file on its own and hit `NameError: name 'app' is not defined`.

**v2 — merged into one file:** it was integrated into a single `app.py`. That then crashed with `AssertionError: View function ... is overwriting an existing endpoint function: formality_guide` — a **duplicate `/formality` route** that had to be removed.

**v3 — templates added:** the new pages (`progress`, `locked`, `developer_login`, `subscription_success`) threw `TemplateNotFound` until I actually placed them in the `templates/` folder.

## Failure modes the final version handles

- **Running a snippet as a standalone app** — a code fragment has no Flask `app` object; it has to be imported/merged, not run directly.
- **Duplicate routes** — two functions registered on the same URL crash Flask on startup.
- **Missing templates** — a route is useless until its template exists in the right folder.

## Outcome

A 10-level XP progression, sections that unlock in a sensible order, a password-protected developer mode that bypasses every lock, and 3 subscription tiers (Free / £9.99 / £19.99). Working.

## What I'd change next

The points/levels logic only got proper unit tests (32 of them) *months later* — I'd write those alongside the feature next time. And the developer password is hardcoded (`buddha2025`) — it should be an environment variable, not sitting in the source.

## Tags

`code-generation` `gamification` `flask` `feature-design` `monetization`
