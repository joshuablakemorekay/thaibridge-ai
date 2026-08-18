# XP Economy Audit

> **Category:** analysis
> **Model used:** Claude Opus 5 (Claude Code)
> **Project area:** Thai Language & Culture Learning App — progression & monetisation
> **Status:** production
> **Last updated:** 2026-08-18

## What this prompt does

Audits a live gamification system by asking whether it actually *works* for each
audience the app has, rather than whether it runs. The prompt names a specific
suspicion — that a free learner has almost nothing to earn XP on — and asks the
model to check it against the real access rules in the codebase.

It is the sequel to [`gamification-system`](../gamification-system/), which is
the prompt that built the XP system in the first place. This one asks, eight
months later, whether the thing that prompt produced is doing its job.

## The prompt

**The request (verbatim):**

```
Is the user XP system effective in the app? For example, how do users get XP
when only Alphabet, Paiboon and Buddhism is free? Can other sections be unlocked
with XP or do they require payment?
```

**The follow-up, once the audit came back (verbatim):**

```
How can we fix this? Especially so that a free user watches a progress bar fill
up toward a reward that doesn't exist issue can be fixed.
```

## Inputs

- The live `app.py` — `SECTION_REQUIREMENTS`, `SUBSCRIPTION_TIERS`, `XP_LEVELS`,
  `POINT_REWARDS` and `check_section_access`
- The three real audiences: free visitors, paying subscribers, and Monk Mode
  (monastics, who have payment waived but still level up)
- Every route that grants XP

## Why it is shaped this way

The question carries its own worked example — *"how do users get XP when only
Alphabet, Paiboon and Buddhism is free?"* — which forces the answer to be
arithmetic rather than opinion. A vaguer version ("is the gamification any
good?") invites a design essay. Naming the free sections makes the model add up
what is actually earnable and compare it against what that XP unlocks.

Asking "is it effective?" rather than "is it working?" is the other half. Working
is a question about code; effective is a question about people, and it is the one
that surfaced that the system is well designed for two audiences and decorative
for the third.

## Expected output

- A per-audience verdict, not a single yes/no
- The XP genuinely available to a free learner, totalled from the code
- What that XP unlocks — checked against the real gate logic, not the marketing
- Any dead or unenforced configuration found along the way
