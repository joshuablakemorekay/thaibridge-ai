# Reasoning: Thai Alphabet Module & Ordering Exercises

## Goal

Add a proper Thai alphabet section (44 consonants, vowels, tone marks) available to brand-new **Level 1** users, and make **completing the alphabet a requirement** before anything else unlocks — because mastering the alphabet first is genuinely how you start learning Thai. Plus an interactive ordering exercise to practise it.

## Iteration history

**v1 — alphabet + first exercise:** added the alphabet module and a drag-and-drop "alphabetical order" exercise — but it only used the first 10 consonants and wasn't the true Thai order. (The module also first arrived as a paste-in snippet and hit the same `name 'app' is not defined` error when I tried to run it alone.)

**v2 — correct full order:** *"the exercise is great... BUT it is incorrect! Can you make the exercise the correct Thai alphabet in full order?"* — fixed to all 44 consonants in proper dictionary order.

**v3 — make them work for it:** *"Don't show all answers. Make user work for it. Add Romanised translation for every consonant."* — removed the "Show Answer" button, put romanization under every consonant, and replaced the overwhelming dump-all-44 with a **progressive 5-level system** (5 → 5 → 10 → 10 → all 44) that unlocks as you go.

## Failure modes the final version handles

- **An exercise you can cheat** — removed the "Show Answer" button; hints now reveal one letter at a time.
- **An overwhelming exercise** — all 44 at once was too much; broke it into unlocking levels.
- **Wrong alphabet order** — the first version wasn't the real dictionary sequence.
- **Snippet run standalone** — the alphabet module had to be merged into `app.py`, not run on its own.

## Outcome

A complete alphabet module gated as the *first* requirement, with a progressive, no-cheat ordering exercise that shows romanization on every card. Working.

## What I'd change next

Add audio for each letter, and track which letters a learner keeps getting wrong so the exercise can drill those specifically.

## Tags

`code-generation` `education-design` `thai-alphabet` `gamification` `frontend`
