# Reasoning: Alphabet Gate Audit

## Goal

I asked what looked like a simple question:

> is it right for Alphabet page to be free?

The answer to the question as asked is yes, and it takes one paragraph. The
useful part was the question underneath it, which I had not asked.

## Iteration history

**v1 — the question as posed.** Answered from the data: all 21 paid sections
carry `requires_alphabet: True`, so charging for the Alphabet would put a paid
prerequisite in front of everything paid. Nothing on the language side could be
sampled before paying, and the free tier would collapse to Buddhism only. It is
not really a generosity decision — it is structurally forced.

**v2 — the harder question.** Having established that, the answer went on to ask
whether the prerequisite was drawn in the right place, and I took that up:

> yes look at that

That is where the findings came from.

## Failure modes the final version handles

- **Answering the question instead of the problem.** "Should the Alphabet be
  free" has a one-paragraph answer. "Is the prerequisite drawn in the right
  place" is the question worth someone's time, and it only appears once the
  first one is settled.
- **Asserting rather than measuring.** The claim that Culture does not need
  script-reading is backed by a count: 31% of its strings contain any Thai at
  all, against roughly 10,000 characters of mostly English prose about the wai,
  temple manners and festivals.
- **Ignoring gate order.** The alphabet gate is checked *first* in
  `check_section_access`, before level and tier. So a Basic subscriber who has
  paid £9.99 and opens Tour Guide is told "Complete Thai Alphabet first" — the
  paywall was not even the thing that stopped them.
- **Re-opening a settled decision.** The Instant Access Pass exists precisely to
  skip these gates. It was fenced off at the top of the prompt so the audit
  looked at where the gate is drawn rather than at whether it should exist.

## Outcome

Shipped in `d99c524`. Two changes, both small.

**Culture lost the alphabet prerequisite.** Level 3 and the Basic tier are
untouched — the progression and the paywall still do their work. Only the
requirement that taught nothing is gone. Two tests assert Culture stays paid and
level-gated, so nobody can later read this as "Culture was made free".

**The pricing page lost a flag that read badly.** `premium` carried
`requires_alphabet: True`. It never fired, because `/premium` has no
`@require_access` — but it read as "pass a quiz before you may see our prices",
and it would have become true the day someone added the decorator for
consistency.

The sorting behind those two changes:

| | Sections | Verdict |
|---|---|---|
| Genuinely need the script | `vowels_syllables`, `read_write`, `tones_classes` | keep the gate |
| Not real sections | `premium`, `greetings_wai`, `classifiers` | dead or unbuilt |
| Taught in romanisation | the remaining 15 | gate does no teaching work |

Only Culture was changed of those 15. "Learn the script early, don't get stuck in
romanisation" is a defensible teaching position and clearly the intent — it just
does not extend to an English page about bowing.

Passing the gate means naming **35 of 44** consonants, which is a real hurdle
rather than a formality. That is the right price for reading Thai and the wrong
price for reading about a wai.

## Engineering on the output

- *Accepted as-is:* both changes and the three tests.
- *Reworked, and why:* nothing at the code level this session.
- *Decisions made:* take the follow-up question rather than stopping at the
  answer; change only Culture of the 15 candidates rather than the whole set;
  keep the Instant Access Pass out of scope.
- *Roughly:* shipped as-is on code, with the direction and the product
  decisions mine.

> Review of this file was delegated — I asked for a recommendation rather than
> approving each section line by line.

The audit was also verified differently from the rest of the session. The
working tree held another session's in-flight work and a failing test that was
not mine, so the commit was checked out into a throwaway `git worktree` and the
suite run against it alone — 1,240 passing — which proved the failure was theirs
without touching their files.

## What I'd change next

Fourteen sections are still alphabet-gated on pages taught in romanisation.
That is now a deliberate position rather than an accident, but it is undocumented
anywhere a learner can see: nothing on the site explains *why* the alphabet
opens things that do not appear to need it. A sentence on the locked page would
turn an obstacle into a teaching choice.

`greetings_wai` and `classifiers` are also still priced and unbuilt. Excluding
them from the outline was the right call for the pricing page; leaving them in
`SECTION_REQUIREMENTS` indefinitely is not a decision, it is a deferral.

## Tags

`analysis` `audit` `access-control` `monetization` `flask` `product-decision`
