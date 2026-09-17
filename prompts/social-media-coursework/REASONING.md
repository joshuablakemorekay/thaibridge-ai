# Reasoning — Social Media Coursework

**Date:** 2026-09-15
**Commits:** `a1df2f9` (the tutor fix the screenshots found). The four PDFs
live outside the repo, in the coursework folder beside the SMOALD originals.

> Review of this file was delegated — *"just do it"* — so the sections below
> are drafted from the session transcript and the shipped documents, not from
> a line-by-line sign-off. The quotes are word-for-word; the prose around them
> is the assistant's reading of what happened.

---

## Goal

Rebuild the four Meta Social Media Marketing course submissions — business
description + SMART goal + KPIs, customer persona and journey, Facebook post,
content calendar — for ThaiBridge AI, keeping the structure of the SMOALD
versions that had already been marked and replacing every word of content.

## Where it started

The session began with a read-only step and a check that it had been done:

> "Read the README and landing-page files in this repo and tell me what thaibridge-ai does, who its users are, and its current stage. Then wait — don't write anything yet." Have you done this?

Then the chain instruction, which is the prompt this folder archives:

> Do it one document at a time. Business description first, then feed that into the SMART goal, then the persona, and so on — same chain as the course. Don't ask for all five in one go; each should build on the last for consistency.

## Iteration history

**v1 — the chain.** Business description first, reviewed, then the SMART goal
drafted from it, reviewed, then the persona, and so on. Each step got the same
two-word gate — *"All correct, carry on to the SMART goal"* — before the next
was written. Settled content: B2C, sole trader, Lichfield, "Buddhist monk and
web developer" said openly; SMART goal = switch Stripe live and win 10 paying
subscribers / £100 in 60 days via Facebook, TikTok and LinkedIn; KPIs = paying
subscribers, new free accounts, free-to-paid rate; persona = Claire Bennett,
38, Manchester nurse married into a Thai family, temple volunteer.

**v2 — the post image.** The first Facebook post draft illustrated the free
Digital Chanting Book. This is the question that changed it:

> Hang on. Why use Image: a screenshot of the Digital Chanting Book page … WOuld it be better to show part of the paid product like an image of the AI chat?

The answer was yes — the goal is paying subscribers, so the picture has to show
what the money buys. Two candidates were offered (the AI tutor and the Sentences
page with its three politeness levels). The ruling: *"Sentences page, go with
your pick"*, then *"Can you do both?"* — so the post carries two screenshots:
an everyday question at three levels of politeness, and the temple dialogue
whose monastic note explains that ถวาย, not ให้, is the word for giving to a
monk.

**v3 — real screenshots, and the bug they found.** *"Take the two screenshots
from the live site and add them."* Taking the AI-tutor screenshot meant asking
the live tutor the exact question the caption poses — which word for "give" to
a monk — and it answered backwards, twice: ให้ to the monk, ถวาย for elders.
The tutor's prompt had never mentioned politeness registers, so it was answering
from memory. Rather than screenshot a wrong answer or quietly swap the image:

> Firstly, can we fix this issue for the AI Tutor mode? Secondlt, Yes, go with the monastic note screenshot if this resoves the issue?

The fix is `a1df2f9`: the register rules now live once, in
`thai_registers.py` beside the notes the Sentences page renders, and
`ai_agent.py` imports them into every mode's prompt, with tests in
`tests/test_ai_register_rules.py`. The post uses the monastic-note screenshot
instead of the tutor.

## Failure modes the final version handles

- Marketing copy that describes a product the assistant imagined rather than
  the one in the repo — handled by the read-first step and the per-document
  review gate.
- Five documents that each satisfy the brief but contradict each other —
  handled by the chain, each fed into the next.
- Showing the easiest thing to screenshot instead of the thing being sold.
- A screenshot of the product proving the product wrong. A marketing task
  found a tutoring bug that no test had, because the marketing task asked the
  live app a real customer's question.

## Outcome

Four PDFs saved to the coursework folder beside the SMOALD originals, with two
screenshots of the live Sentences page embedded in the Facebook post. One
product fix committed and pushed the same afternoon. The persona photo for
Claire is still a placeholder box.

## Engineering on the output

- **Accepted as-is:** the structure and content of all four documents at the
  drafting stage — each was answered *"All correct, carry on"*. The SMART goal
  numbers, the persona, the KPIs and the calendar's twelve ideas are as drafted.

- **Reworked, and why:** the Facebook post's images (free chanting book → two
  screenshots of the paid Sentences page, for the reason above); the choice of
  second screenshot (tutor → monastic note, because the tutor was wrong); and
  the wording of the submitted documents — the author says he **edited wording
  before submitting**, but which lines changed was not recorded, so this folder
  cannot say. The calendar and post both carry a *"Draft for review — edit any
  wording to make it yours"* footer, and he did.

- **Roughly:** the documents' shape and substance shipped as drafted; the
  images and the product decision behind them are the author's; the final
  wording edits are real but **not tracked**.

- **Whose decisions these were:** the paid-product image and the tutor fix
  were the author's calls, both raised by him against a draft that had gone
  the other way. The Sentences page over the AI chat was the assistant's
  recommendation, which he accepted and then widened to both.

## What I'd change next

- Record the wording edits at submission time, so the next entry like this can
  show the before and after instead of saying "not tracked".
- Verify the Ok Phansa date on the calendar against the temple's own calendar
  before it goes anywhere near a real post.
- Replace Claire's placeholder photo.

**Tags:** `content` `marketing` `coursework` `agent-workflow` `found-a-bug` `paid-product-first`
