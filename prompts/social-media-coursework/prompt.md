# Social Media Coursework — One Document at a Time, Each Fed Into the Next

**Category:** content / agent-workflow
**Model:** Claude (Opus, via Claude Code)
**Project area:** marketing — Meta Social Media Marketing coursework, four submissions rebuilt for ThaiBridge AI
**Status:** shipped 2026-09-15 — four PDFs in the coursework folder, two live screenshots, and one product bug fixed along the way (`a1df2f9`)

---

## Final prompt (v3)

The prompt is a chain, not a single message. The core instruction is quoted
exactly as given, with the two constraints that were added in later rounds
below it.

> "Now, using the files in /marketing-examples as format templates only (copy their structure and tone, not their content), draft a short business description for thaibridge-ai. We'll do the SMART goal, persona, journey, post and content calendar after, one at a time." i.e. Give it a clear instruction with the examples named. Something like: "Using the SMOALD files in /marketing-examples as format templates only, create the same set of documents for thaibridge-ai based on what you learned about the product. Keep the structure; replace all content."
> Do it one document at a time. Business description first, then feed that into the SMART goal, then the persona, and so on — same chain as the course. Don't ask for all five in one go; each should build on the last for consistency.
> Review and correct each one. Claude Code will make assumptions about your product — check them, fix anything wrong,

**Added in v2 — the post image shows the paid product, not the free one:**

> Hang on. Why use Image: a screenshot of the Digital Chanting Book page on thaibridge-ai.smoald.com, showing one chant laid out in its five coloured layers — Pali in Thai script, romanised Pali, Thai translation, Paiboon, and English — with the layer on/off switches visible at the top. (Placed as the post image on Slide 2 of the Facebook template.) ? WOuld it be better to show part of the paid product like an image of the AI chat?

> Sentences page, go with your pick

> Can you do both?

**Added in v3 — real screenshots from the live site, and the bug they found:**

> Take the two screenshots from the live site and add them

> Firstly, can we fix this issue for the AI Tutor mode? Secondlt, Yes, go with the monastic note screenshot if this resoves the issue?

---

## Inputs

- The four SMOALD course submissions, used as **format templates only** —
  structure and tone copied, every word of content replaced
- The repo's `README.md`, landing page and key files, read first so the
  documents describe the product as it actually is
- The live site at `thaibridge-ai.smoald.com`, logged in, for the two
  screenshots of the paid Sentences page

## Why the prompt is shaped this way

**"Read the README … then wait — don't write anything yet."** The session
opened with a read-only step and a check that it had happened before any
writing started. The documents have to be *accurate* before they can be
*persuasive*, and an assistant asked to write marketing will happily invent a
product.

**"One document at a time … each should build on the last."** The course
teaches the five documents as a chain — business description → SMART goal →
persona → post → calendar — and the prompt copies that chain on purpose. Asking
for all five at once would have produced five documents that agree with the
brief but not with each other. Each one was reviewed (*"All correct, carry on
to …"*) before the next was drafted from it.

**"Format templates only … Keep the structure; replace all content."** The
SMOALD versions had already been marked (the first scored 92.85%), so their
shape was proven. The risk was the assistant leaning on their *content*, so the
prompt says twice that only the structure carries over.

**"Would it be better to show part of the paid product?"** The first draft of
the Facebook post illustrated the free chanting book — the easiest thing to
show and the wrong thing to sell. The SMART goal is paying subscribers, so the
pictures have to show what £9.99 buys; the free content stays in the caption as
the low-risk first step. That one question changed the post's images, and the
persona's journey with them.

## Expected output

- Four documents that share one persona, one goal and one set of prices
- A Facebook post whose text names the customer's problem and whose images
  show the paid page that fixes it
- Real screenshots of live pages, not mock-ups — the audience checks carefully
  before trusting anything to do with their faith or their family
- Every product claim checkable against the repo or the live site
