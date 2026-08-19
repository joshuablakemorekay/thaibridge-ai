# Survival Thai — A Free Section Someone Can Finish

**Category:** content
**Model:** Claude (Opus)
**Project area:** `survival.py`, `/survival`, `templates/index.html`
**Status:** shipped 2026-08-19 — `e298ab9`, live (Thai awaiting teacher review)

---

## Final prompt

> Build one full survival module: greetings, numbers, food, directions.
> Finishable, genuinely useful.
>
> Before you build it, tell me where it belongs. The Tour Guide page covers
> similar ground — is that the right home for this, or not? Check that page's
> tier and its prerequisites before answering, and if it is the wrong home say
> so and say why.
>
> The point of this section is the person who arrives wanting to SPEAK Thai and
> currently gets an alphabet chart and a paywall. So work out what actually has
> to be true for them to reach it, and make each of those things true.
>
> Constraints:
> - Finishable in one sitting. If it grows into a hundred phrases it has stopped
>   being the thing it is for. Enforce that, don't just intend it.
> - The Thai will be an unreviewed draft. Say so on the page, where a learner
>   sees it, not in a comment.
> - Politeness particles are gendered. Do not pick one.
> - It is a doorway, not a dead end — send them somewhere next.

---

## Why this prompt is shaped this way

**"Tell me where it belongs" before "build it"** is the question that did the
work. Tour Guide was the obvious home and the wrong one: it is `basic` tier,
level 4, and alphabet-gated, so putting a free taster there means either freeing
a paid section or burying the taster behind £9.99 and 44 consonants.

**"Work out what actually has to be true for them to reach it"** produced the
`requires_alphabet: False` decision. Free tier alone would not have been enough —
the alphabet gate is checked *first*, before level and tier.

**"Enforce that, don't just intend it"** turned "finishable" into a test that
fails if the phrase count leaves the 30–70 range.

**"Do not pick one"** — a single particle teaches half the learners to sound
wrong. Both are shown on every phrase that needs one.
