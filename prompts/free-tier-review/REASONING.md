# Reasoning: Free Tier Review

## Goal

I had five ideas for loosening the free tier and no way to tell which were
generous and which were just expensive. I asked for a verdict on each rather
than a discussion, and I put the sales argument for one of them in the same
breath as the question:

> The whole curriculum outline, visible to everyone people pay more readily when
> they can see what they're buying. Should we do these now?

That sentence is the reason the outline got built the way it did. The point was
never "list the sections" — it was that someone deciding whether to pay can see
what the money opens.

## Iteration history

**v1 — the five questions, asked cold.** All five at once, phrased as
do-or-don't. What came back was three yeses, two nos, and one of the yeses
reframed as a bug rather than a feature.

**v2 — narrowing the Paiboon tool.** The answer to question 2 came back as three
possible builds, and I closed it down to one:

> Yes only do the first one leave the others out of it.

That decision has its own folder — see `prompts/paiboon-lookup/`.

## Failure modes the final version handles

- **Answering from the marketing copy instead of the gate logic.** The tier
  feature lists in `SUBSCRIPTION_TIERS` describe what each plan gives you.
  `SECTION_REQUIREMENTS` decides it. They are not the same, and only the second
  one runs.
- **Treating "free" as a single axis.** Free-vs-paid, level-gated, and
  alphabet-gated are three separate gates in `check_section_access`, checked in
  that order. A proposal can clear one and still be blocked by another.
- **Costing a giveaway by instinct.** The per-message AI cost was already
  written down in a comment above `FREE_AI_DAILY_LIMIT`. Question 4's answer is
  arithmetic, not judgement, once you read it.

## Outcome

Three built, two rejected.

| Proposal | Verdict | Where it went |
|---|---|---|
| Complete reading system free | **Don't** | unchanged |
| Paiboon lookup tool | Do | `e368522` |
| One survival module | Do | `e298ab9` |
| Reduce the 15 AI messages | **Don't** | unchanged |
| Small free Dhamma allowance | Do — as a bug fix | `be35854` |
| Public curriculum outline | Do | `9505e4a` |

**Why the reading system stayed paid.** `vowels_syllables`, `read_write` and
`tones_classes` *are* the Basic tier — the tier is literally named "Thai Reader".
Freeing them leaves £9.99 buying grammar, lessons and sentences with no headline.
There was already a softer version of the same generosity in place: Level 3
earns one free Basic section, so a motivated learner can choose reading and get
it free without the tier collapsing.

**Why 15 AI messages stayed 15.** The costing was already in the code: 0.285p
worst case per message, so 15 a day is about £1.30 a month for a free user who
maxes it out every single day, which almost nobody does. The tutor is the thing
that makes £19.99 believable. Shrinking the best free feature to save pennies is
the wrong trade.

**The curriculum outline** became `curriculum.py`, and the interesting part is
that it is *assembled from the gated routes* rather than hand-listed beside
them. `require_access` now records the section it guards on the view function,
and `assert_outline_is_complete()` fails the import if a section is neither
advertised nor excluded for a written-down reason. That design came straight
out of a scar already in this codebase: the Culture page once built its practice
links by guessing a URL from a dict key, and one story pointed at a 404 for
months with nothing in the code looking wrong.

Building it that way immediately found three sections priced but not built —
`greetings_wai`, `classifiers` and (at the time) `register` — all sitting in
`SECTION_REQUIREMENTS` with a tier and a level and no route anywhere. They are
excluded from the outline with a recorded reason, and a test fires the moment
any of them gets a route.

It also found that Pro adds exactly **one** page against Basic's sixteen. Its
real value is unlimited AI, the roleplay partner and the exercise generator —
none of which are pages. So each tier shows its feature list beside its page
list, or the outline would have undersold the most expensive tier.

## Engineering on the output

- *Accepted as-is:* the three implementations, their tests and the module split.
- *Reworked, and why:* nothing at the code level this session.
- *Decisions made:* reject the reading-system giveaway; reject the AI-cap
  reduction; treat the Dhamma allowance as a bug rather than a feature; build
  the outline from the routes rather than a hand-kept list; keep the three
  unbuilt sections off the public outline instead of advertising them.
- *Roughly:* shipped as-is on code, with the direction and the product
  decisions mine.

> Review of this file was delegated — I asked for a recommendation rather than
> approving each section line by line.

The two rejections are the part of this review I would point a reader at first.
A review where every proposal is accepted is not a review.

## What I'd change next

The outline is honest about what exists but says nothing about what is *good*.
A reader comparing Basic's sixteen pages against Pro's one page plus AI has no
way to judge depth — Sentences and Business Thai are not the same size of thing
and the list presents them as equals.

The three priced-but-unbuilt sections should also be decided rather than
excluded forever. Either build them or delete the entries; a permanent
exclusion list is a to-do list that nobody reads.

## Tags

`analysis` `monetization` `product-decision` `flask` `pricing`
