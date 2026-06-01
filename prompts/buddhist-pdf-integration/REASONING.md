# Reasoning: Buddhist PDF Integration (Pra Kru Bob's Writings)

## Goal

Add a new "Pra Kru Bob's Writings" section to the Buddhist Dharma page, containing two of Pra Kru Bob's essays from PDF documents — reproduced **exactly, word-for-word, with no wording changed**, and styled nicely.

## Iteration history

**v1 — faithful attempt that wasn't:** added the section, but it quietly **dropped paragraphs and changed wording**. Not acceptable for someone's Buddhist writing.

**v2 — insist on the complete text:** after I pushed back — *"I told you specifically not to change the wording. I want all the words and paragraphs added as they originally are"* — each essay was split into its own **complete HTML page** (the "Option 1" approach), with every paragraph preserved.

**Polish:** changed the clickable buttons' text to gold so they were actually visible against the background.

## Failure modes the final version handles

- **Silent summarising** — when asked for a verbatim reproduction, the AI first abridged it. The lesson: **faithful means faithful** — insist on the complete text and check it against the source rather than trusting a tidy-looking summary.

## Outcome

Two complete article pages added and linked from the Dharma page, faithful to the PDFs, with new routes (`/bob-buddhism-overview`, `/bob-fear-article`) added to `app.py`.

## What I'd change next

Store the article text as data (or load it from the source files) rather than hardcoding it into HTML, and automatically check the reproduced word count against the original so dropped paragraphs get caught immediately.

## Tags

`content` `faithful-reproduction` `html` `buddhism` `verification`
