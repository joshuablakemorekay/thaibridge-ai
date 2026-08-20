# Reasoning — Hero Copy Rewrite

**Date:** 2026-08-19
**Commits:** `95635ef`, `9b234c4`, `9cf3302`, `74341c6` — all live and verified

---

## Goal

Rewrite the home page hero so it makes a promise rather than describing the
site's own structure, then make sure the culture-freedom it promises is actually
stated rather than implied.

## Where it started

> "This doesn't sound very convincing."

That was the whole brief, aimed at this hero:

```
🪷 ThaiBridge AI
Theravada Buddhism & the Thai language · พระธรรมและภาษาไทย
Two subjects, side by side. Study the Dhamma on its own, learn Thai on its
own, or follow how the two meet in Thailand's temples.
```

The diagnosis that followed: it describes the site's filing system, and its
sentence is built from hedges, so it reads as an apology for two subjects
sharing a page rather than a promise about either.

## Iteration history

**v1 — structure to offer.** Replaced the subtitle with one naming the four
doors the page actually opens (Buddhist teachings, Thai language, chanting,
culture), and moved the strapline into the `<h1>`. Shipped as `95635ef`.

**v2 — the culture-freedom line, rejected three times.** This is where the
real work happened, and none of the AI's wordings survived.

**v3 — rewritten by hand.** The final copy is the author's own, and it restored
something v2 had lost.

## The corrections that shaped it

Each of these killed a proposed wording, and each names a rule worth keeping:

> "I want to preserve and respect Thai and it's language, culture and traditions so how can we reword it?"

This reframed the whole passage. The draft on the table read *"Keep your own
culture, take on part of another, or follow none at all"* — in which Thai
culture never appears as itself, only as an unnamed "another", grammatically the
one option being declined. On an app built to honour that culture, the sentence
was backwards.

> "life shoudn't allow life is what we make it. I'm not sure about learn how the dhamma is lived in Thailand it sounds envious."

Two rejections in one line. *"Practise it however your own life allows"* writes
the reader's life as a set of walls. *"Learn how the Dhamma is lived in
Thailand"* puts the reader outside a window watching someone else's practice.

> "Should we mention any of this - Adopt aspects of another culture if you wish. Or follow no culture at all. ... Because this is very important."

**This is the question that found the bug.** The shipped v1 hero promised
freedom in general terms and had silently dropped the culturally-neutral option
from the front page. It was still one click away on `/dhamma-and-culture`, but
the hero no longer named it. A general promise of freedom is not the same thing
as naming the option.

Worth recording precisely, because it is a failure mode this archive should
guard against: the objection that removed the clause was to the *phrase*
"follow no culture at all" — which contradicts this site's own argument that no
Buddhism sits anywhere culture-free — and **not** to the option itself. A
wording objection was allowed to delete a commitment. The fix borrowed the
explainer page's own language so the two pages agree.

## Failure modes the final version handles

- Copy that describes a site's architecture instead of its offer.
- Freedom language that frames the host culture as the thing being declined.
- A general promise of freedom standing in for a specifically named option.
- Front-page copy contradicting an argument the site makes elsewhere.

## Outcome

Four commits, all pushed and verified serving on the live site.

## Engineering on the output

- **Accepted as-is:** the structural change — strapline moved into the `<h1>`
  as its own `.brand-strapline` span, sized down from the 3rem brand weight so
  a full sentence neither swamps the hero on desktop nor walls up on mobile
  (with a matching 768px rule); the subtitle naming the four doors; the
  supporting CSS; and the site-wide spelling normalisation of "Theravada"
  across all 26 mentions.

- **Reworked, and why:** every sentence of the culture-freedom copy. Three AI
  wordings were rejected in turn — "another culture" made Thai culture the
  unnamed thing being declined; "however your life allows" made life a
  constraint; "how the Dhamma is lived in Thailand" read as spectating someone
  else's practice. The shipped text is the author's own, and it reinstated the
  culturally-neutral option that the AI draft had dropped.

- **Roughly:** the layout shipped as-is; the copy is entirely the author's.

## The clearest evidence in this folder

The `/about` card **On "Thainess" — a personal note** is 100% the author's
words. Concerns were put to him before it shipped — an internal contradiction
between "evidence proves diversity is worth protecting" and diversity as a cause
of decline; "evidence proves" with nothing cited; the war-debts claim being weak
on the facts; a Churchill misquote that drops its four conditions; and the fact
that `/about` is linked from both CVs. His answer:

> "Just add it exactly as I have written it."

It shipped verbatim, with four mechanical spellings corrected and nothing else
touched. Recorded here because an archive that only shows the AI being right is
not evidence of anything.

## What I'd change next

Check the hero note on a phone. It is eleven sentences and sits between the
headline and the buttons — the natural split, if it reads heavy, is keeping the
first four sentences and moving the closing lines to `/dhamma-and-culture`.

---

## Round 2 — 2026-08-20, commits `064a055`, `016cc01`

The section above ends by predicting this one:

> Check the hero note on a phone. It is eleven sentences and sits between the
> headline and the buttons — the natural split, if it reads heavy, is keeping
> the first four sentences and moving the closing lines to
> `/dhamma-and-culture`.

The question that reopened it:

> "Do you think I've overdone this? Consider the fact that my target audience is mainly English speaking expats in Thailand, tourists, students, English speakers and learners in general who are interested in Thai culture and language."

An outside critique answered yes and proposed cutting the hero to 28 words:
*"We teach the Dhamma as Thailand preserves it, because that's where the
language lives."* Its recap said to drop "The Dhamma is Universal", move the
rest to an About/FAQ page, and stop letting one critic write the front page.

**Half of that was right.** The note stated one promise five times over — "no
Thai needed", "not required", "without adopting any… at all", "on your own
terms", "your own path" — and its closing line restated the strapline three
lines above it. Two sentences said the same thing twice in heavier English than
the audience reads comfortably.

**The other half would have repeated round 1's failure exactly.** The proposed
replacement says the site teaches the Dhamma *as Thailand preserves it*, and
nothing else. The culturally neutral branch — the thing round 1 was entirely
spent putting back — is absent from it. A second wording objection came within
one edit of deleting the same commitment, for the second time, on grounds that
had nothing to do with the commitment itself.

What made it survivable was not judgement, and that is the point worth
recording. `tests/test_dhamma_open_to_all.py` asserts the clause is present on
the rendered page. **The commitment is guarded by a test rather than by
whoever happens to be editing the file that day** — which is the only form of
protection that survives a persuasive argument.

### What the guard tests taught in passing

The assertions match exact substrings of the *rendered HTML*, so wrapping a
guarded phrase across two lines of the template fails them while the copy
itself is perfectly correct. Two tests failed on the first attempt at this
rewrite for exactly that reason. Either keep guarded phrases on one source
line, or make the assertions whitespace-tolerant — but know which you have
chosen, because a test that fails for a formatting reason trains people to
ignore it.

### Same round: the explainer's closing card

`/dhamma-and-culture` still ended on *"Keep your own culture, take up part of
another, or follow none at all"* — the wording round 1 rejected for the hero,
still live at the bottom of the page that exists to explain the position. It
now mirrors the hero. Two pages arguing the same case in different words is
how a position drifts.

## Engineering on the output — round 2

- **Accepted as-is:** the tightened hero body, the `/dhamma-and-culture` FAQ
  paragraph and the reworded closing card all shipped as drafted.

- **Reworked, and why:** the author wrote the "Welcome to ThaiBridge AI"
  opener himself, and restored the closing line *"Keep the Dhamma close to your
  heart yet remain detached"* after the draft had cut it as the one instruction
  in a passage otherwise about not instructing. His page, his call.

- **Whose decisions these were:** the substantive calls in this round —
  rejecting the 28-word hero, keeping the welcoming clause in the `/about`
  note, and *not* adding a justification page — were the agent's
  recommendations, which the author accepted. Recorded plainly, because an
  archive that quietly credits every good call to the human is worth as little
  as one that credits them all to the model.

**Tags:** `content` `copywriting` `cultural-positioning` `human-authored` `guarded-by-tests`
