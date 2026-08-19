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

**Tags:** `content` `copywriting` `cultural-positioning` `human-authored`
