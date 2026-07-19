# Reasoning: Unified "Tones & Consonant Classes" Section

## Goal

Create one unified, free learning section that teaches consonant classes and tone rules **together** as a single skill — because classes only exist to determine tones, so splitting them is confusing. Reuse the app's existing content and quiz/XP mechanics rather than building anything parallel.

## Iteration history

Single version this session — but the prompt was deliberately structured as a 4-step contract: (Step 1) explore the codebase and *recommend* merge-vs-rebuild before touching anything; (Step 2) an exact content spec; (Step 3) four progressive drills reusing existing scoring; (Step 4) a verify step. The explore-first gate is the key design choice — it forced a plan and an approval checkpoint before any edits.

## Failure modes the final version handles

- **Duplicating or clobbering existing content** — the explore step found tone/class content already lived in three scattered places (one of them paywalled), so the build merged the strongest copy instead of blindly re-creating it.
- **Inventing a parallel scoring system** — the prompt insisted on reusing the existing `/api/check_answer` XP mechanic, so the drills stay consistent with every other quiz.
- **Scope creep / unwanted refactors** — "don't refactor anything unrelated" kept the blast radius small and left the Grammar page untouched.
- **Wrong access level** — free tier with no level/alphabet gate was stated explicitly, so core reading content doesn't end up behind a paywall.
- **Obsolete letters in practice** — ฃ and ฅ appear in the reference chart but are banned from the drills.
- **Feature bloat** — no audio/AI this round; text-based drills only.

## Outcome

Shipped on the `feature-experiment` branch and verified: `/tones-classes` returns 200 while logged out, all four drills award XP through the existing endpoint, the embedded drill JSON validates, and the untouched Grammar page still works. Good enough to ship.

## What I'd change next

(left blank)

## Tags

`agent-workflow` `code-generation` `explore-first` `thai-tones` `education-design`
