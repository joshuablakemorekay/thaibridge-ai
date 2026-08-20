# Reasoning — Critique to Product Decision

**Date:** 2026-08-20
**Commits:** `d91a06a`, `1e77b07` — live and verified

---

## Goal

Work out whether a hostile critique of Thai Buddhism and of the app's Thai
focus should change the product at all, and if so what specifically — rather
than writing another paragraph of front-page copy answering the critic.

## Why the framing mattered more than the answer

The two rounds before this one had both ended in defensive copy: the home page
hero and the `/about` closing note were each rewritten in response to the same
person. Neither rewrite made the app better at teaching Thai or better at
earning money. The question that broke the pattern was this one:

> "Now take what Chris said and Claude's response then tell me how any of this would affect the app as a product for making money and providing free teaching."

Asking what a criticism does to the *product* separates two things that feel
identical when you are the one being criticised: whether an argument is correct,
and whether it should change anything you ship.

## The answer, and the part of the critique that survived it

Most of it changed nothing. The critic is not in the paying segment — not
learning Thai, not visiting temples, not buying. The paying segment is the
opposite person: someone with a Thai partner, in-laws they cannot speak to, a
temple invitation they do not want to get wrong. For them the Thai cultural
material *is* the product, and the only thing distinguishing it from Duolingo.
Removing it to satisfy someone outside the funnel would cost the differentiator
and gain nothing.

**One part did survive**, and it was not the part the critique thought was its
strongest. The Buddhist content presented the tradition only at its best, which
to a sceptical adult reads as devotional material rather than teaching. That is
a credibility gap, and it is cheap to close.

The critic's own best argument — *"do you think if Buddha was alive today, that
he would approve of this behaviour?"* — answers itself. The Buddha wrote the
rules against monastic wealth. Condemning luxury monks means using Buddhism's
own standard, which is an argument for the tradition rather than against it. So
the fix was to put that standard on the page.

## What shipped

**Three Vinaya rules** added to `/theravada` alongside the ones already there:
the money rule (Nissaggiya Pācittiya 18), eating at the wrong time (Pācittiya
37, 38 and 40), and the ไวยาวัจกร — the lay steward who holds funds on the
Sangha's behalf. With a short note, *How the tradition judges itself*, making
the point explicit: when a Thai newspaper runs a story about an abbot with a
private jet, the standard being used comes from this same book.

Those three were chosen because they do three jobs at once. They are real
teaching content; they explain why Thai monastic charity runs through a temple
committee rather than looking like a church soup kitchen (a monk may not handle
money, store food, cook or dig the ground); and ไวยาวัจกร is genuinely useful
Thai vocabulary for anyone who spends time around a temple.

## The decision not to make a change

> "Should we justify the app being focused on Thai culture? Because Chris was critisicing and dissaproving of it."

The recommendation was **no** — and this is the entry's most useful line,
because it records a change that was considered and refused rather than one
that was never thought of.

The app is called ThaiBridge. The focus is the product, and the position had
already been made three times over: a whole explainer page, a hero naming both
paths, four subject doors that let a learner skip the culture entirely, and the
entire Dhamma side free with no Thai needed. A fourth explanation would have
been the third piece of defensive copy in a week, and defensive copy is
self-defeating — the more paragraphs spent proving you are not pushing
something, the more it sounds like something the reader needs protecting from.

What went in instead was one sentence stated as **pedagogy rather than
apology**: Thai pronouns shift with who is being addressed, the politeness
registers the site already teaches are hierarchy made grammatical, and much
formal vocabulary is Pali and Sanskrit that arrived with Buddhism. Teaching Thai
with the culture stripped out would mean teaching a Thai nobody speaks. Stated
as a teaching fact it is confident; the same sentence offered as a reply to a
critic sounds nervous. It went on the explainer page, where the explanation
already lives — not on the home page.

## Failure modes this prompt handles

- Answering a critic in product copy instead of deciding whether to change the
  product.
- Removing the thing that differentiates a product in order to satisfy someone
  who was never going to buy it.
- Treating "this criticism is partly correct" as "this criticism should change
  everything".
- Producing improvements because improvements were asked for, when the honest
  answer is that no change is needed.

## Outcome

One new teaching section, one new FAQ paragraph, and one explicit decision not
to add a justification page. Both commits live and verified serving.

## Engineering on the output

- **Accepted as-is:** the Vinaya rules, the *How the tradition judges itself*
  note and the `/dhamma-and-culture` pedagogy paragraph all shipped as drafted.

- **Reworked, and why:** the author's one instruction changed the shape of it —

  > "Yes add Paiboon romanisation to it then put it in"

  which meant the three new cards, and the three already there, all gained a
  Paiboon line. The section had been drafted with Thai and English only, which
  would have made it the one part of the site a learner could not read aloud.

- **Whose decisions these were:** the recommendation not to add a justification
  page was the agent's, and the author accepted it. So was the choice to put the
  Vinaya material in the existing `/theravada` section rather than build a new
  page for it.

- **Roughly:** shipped as drafted, with Paiboon added on instruction.

## What I'd change next

The Pali, Thai and Paiboon in the three new cards are **unreviewed drafts**, as
is the rule numbering. They need checking against a printed Vinaya and a
native-speaker pass before anything cites them.

**Tags:** `analysis` `product-decision` `content` `deciding-not-to-change`
