# Reasoning: XP Economy Audit

## Goal

I wanted to know whether the XP system I'd built months earlier was actually
doing anything, and I had a specific suspicion about who it wasn't working for:

> Is the user XP system effective in the app? For example, how do users get XP
> when only Alphabet, Paiboon and Buddhism is free? Can other sections be
> unlocked with XP or do they require payment?

The last part is the real question. If XP can't unlock anything, it isn't a
progression system — it's a scoreboard.

## Iteration history

**v1 — the audit.** The question above, asked cold against the live code. It
came back with a per-audience answer: the levelling is real for Monk Mode users
(payment is waived, so XP is the only gate left) and real for subscribers (it
paces the content), and does nothing whatsoever for free users, because every
free-tier section is level 1. About 360 XP is earnable on free content, which
reaches Level 3, and Levels 2 and 3 unlock nothing that isn't also behind a
paywall.

**v2 — the remediation.** Having had the finding, I asked for fixes and said
which one mattered:

> How can we fix this? Especially so that a free user watches a progress bar
> fill up toward a reward that doesn't exist issue can be fixed.

That sentence is what shaped the work. Three options came back for the free-user
problem — re-level the free sections, add badges instead of access, or make XP
buy one real paid section — and the third is the one that shipped.

## Failure modes the final version handles

- **"Is it working?" instead of "is it effective?"** — the first is a question
  about code and the code was fine. The whole finding lives in the gap between
  the two.
- **A single verdict for an app with three audiences.** Free, paying and Monk
  Mode users hit completely different gates. Averaging them hides the problem.
- **Trusting the marketing over the gate logic.** `max_level_access` is set on
  all three tiers and the docs advertise "Levels 6–7" for Basic — but nothing in
  the codebase ever reads it. Only checking the enforcement found that.

## Outcome

The audit found four things: the dead progress bar for free users, an
unenforced `max_level_access`, four of six `POINT_REWARDS` defined and never
used, and two endpoints that would mint XP on request — one of which,
`/api/award_points`, took the *amount* from the caller and had no callers at all.

All four were fixed and shipped in one session, as four separate commits:

| Commit | Fix |
|---|---|
| `0a627da` | Deleted `/api/award_points` |
| `fa160c2` | Locked sections now name the paywall, not just the level |
| `a4385f3` | The earned unlock — Level 3 buys one Thai Reader section |
| `f006e23` | Daily ceiling on drill XP |

The earned unlock is the one that answers the original question. XP now unlocks
something for a free learner: one Basic section of their choosing, permanently,
free. It is deliberately narrow — one section, Basic only, and only a section
whose level they already meet, so the unlock can't be burned on a door the level
gate still keeps shut.

## Engineering on the output

- *Accepted as-is:* the four implementations and their tests.
- *Reworked, and why:* nothing at the code level this session.
- *Decisions made:* free the Paiboon guide; prioritise the free-user dead end
  over the other findings; accept the four-phase fix order; ship the earned
  unlock as a real giveaway rather than a badge scheme.
- *Roughly:* shipped as-is on code, with the direction and the product decisions
  mine.

The Paiboon decision is worth recording separately, because it came from the
same instinct as the audit. Paiboon romanisation was a Basic (£9.99) section
while the free chanting and meditation pages *print Paiboon on screen* — so a
free reader was shown `kam buu-chaa` and then sold the key to it. The
instruction was three words:

> make paiboon free

That change shipped in `601624d`, though it landed inside an unrelated dāna
commit rather than its own — noted here because the commit message doesn't
mention it, so this file is the only place the reasoning is written down.

## What I'd change next

The drill cap bounds XP farming but doesn't stop it. `/api/check_answer` is sent
both the answer *and* the correct answer and compares them to each other, so it
can't tell a learner from a script — the drills are generated in the browser, so
the page already holds the answer. Fixing that properly means generating the
drills server-side and keeping the answer out of the page. Until then the
ceiling is the honest mitigation, not a solution, and it matters more now that
XP earns a free section.

Level 3 as the earned-unlock threshold is also a guess rather than a measured
choice — 250 XP against roughly 360 earnable. It wants watching once real
learners hit it.

## Tags

`analysis` `audit` `gamification` `monetization` `security` `flask`
