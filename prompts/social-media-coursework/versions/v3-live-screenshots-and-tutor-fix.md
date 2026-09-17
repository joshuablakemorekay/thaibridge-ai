# v3 — Real screenshots, and the bug they found (2026-09-15)

**Status:** final — shipped as the four PDFs plus commit `a1df2f9`

## What changed

> Take the two screenshots from the live site and add them

> Done, I'm logged in — take the screenshots

Taking the AI-tutor screenshot meant asking the live tutor the caption's own
question — which word for "give" to a monk. It answered backwards, twice:
ให้ to the monk and ถวาย to elders, the reverse of the monastic note on the
Sentences page two clicks away. Its prompt had never mentioned politeness
registers, so it was answering from memory.

> Firstly, can we fix this issue for the AI Tutor mode? Secondlt, Yes, go with the monastic note screenshot if this resoves the issue?

## Why

A screenshot of the product proving the product wrong cannot go in a post, and
quietly swapping the image would have left a paying feature giving temple
visitors the wrong word. Fix first, then choose the picture.

## What it produced

- `a1df2f9` — `REGISTER_RULES_FOR_AI` in `thai_registers.py`, beside the
  notes the Sentences page renders, imported by `ai_agent.py` into every
  mode's prompt; tests in `tests/test_ai_register_rules.py`.
- The post's second image is the monastic-note screenshot from the Sentences
  page, not the tutor.
- Four PDFs saved beside the SMOALD originals, with both screenshots embedded.

## The lesson

A marketing task found a tutoring bug no test had, because it asked the live
app a real customer's question. The register rules had existed in one place
(the page) and not the other (the tutor), and nothing checked they agreed.
