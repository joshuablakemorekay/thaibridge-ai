# Free Tier Review — Five Giveaway Proposals, Judged One at a Time

**Category:** analysis
**Model:** Claude (Opus)
**Project area:** `SECTION_REQUIREMENTS`, `SUBSCRIPTION_TIERS`, `/premium`
**Status:** shipped 2026-08-19 — three of five built, two deliberately rejected

---

## Final prompt

> I am considering five changes to the free tier. For each one, tell me do or
> don't, and why:
>
> 1. The complete Thai reading system, free.
> 2. A Paiboon lookup tool — small utility, daily use, keeps people in the app
>    between lessons.
> 3. One full survival module — greetings, numbers, food, directions.
>    Finishable, genuinely useful.
> 4. Is 15 AI messages a day right, or should it be reduced?
> 5. A small free Dhamma allowance.
>
> Also: the whole curriculum outline, visible to everyone. People pay more
> readily when they can see what they're buying.
>
> Ground every answer in the actual code before answering — read
> `SECTION_REQUIREMENTS` and `SUBSCRIPTION_TIERS` rather than reasoning from
> what the marketing copy claims. Where a proposal would gut a paid tier, say
> so plainly and name the tier. Where the code already contains a costing or a
> stated principle, quote it back to me and hold the answer to it.
>
> I want a recommendation on each, not a survey of options. If you think a
> proposal is wrong, say don't and give me the trade-off I would be accepting.

---

## Why this prompt is shaped this way

**"Do or don't"** forces a verdict. The same five items phrased as "what do you
think about…" produce five balanced paragraphs and no decision.

**"Ground every answer in the actual code"** is the line that made the review
worth running. Two of the five answers turned on facts that are only visible in
`app.py` — that the reading sections *are* the Basic tier, and that the AI cost
per message was already worked out in a comment.

**"Where the code already contains a stated principle, hold the answer to it"**
is what turned proposal 5 from a giveaway into a bug report. The principle was
already written down; the code did not honour it.

**"If you think a proposal is wrong, say don't"** gave permission to reject.
Two of the five were rejected, which is the part of this review that makes the
other three credible.
