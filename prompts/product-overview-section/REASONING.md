# Reasoning: Product Overview Section

## Goal

I needed a clear, structured Product Overview for my app to drop into the market research report — covering what it does, who it's for, the key features, the problem it solves, and the monetisation idea. I didn't want a generic blurb; I wanted it to actually fit the report.

## Iteration history

**v1** was a short brief: "produce a Product Overview with these five parts." Instead of guessing, the model asked me three scoping questions first — which audience to lead with, which strength to emphasise, and how much detail to put on money.

**v2 (current)** I answered those three questions (lead with *all* my audiences, emphasise *all* my strengths, keep monetisation high-level for now), and it produced the full structured overview from that.

## Failure modes the final version handles

- **Vague scope → generic output.** Answering the three scoping questions first pinned down the angle instead of letting the model pick one at random.
- **Wrong emphasis.** The clarifying loop surfaced the "tourists vs expats" choice as a real decision rather than burying it.
- **It connects to my other prompt.** The overview it produced became a source document I fed into the `market-research-report` prompt — so the two work together.

## Outcome

A structured overview with all five sections that I used as an input to the bigger report. Did its job.

## What I'd change next

I told it to keep monetisation *high-level*, but the output still expanded into full pricing tiers and projections. Next time I'd be firmer — "one paragraph, no pricing numbers" — so it actually sticks to the brief.

## Tags

`content` `structured-output` `clarifying-questions` `requirements-elicitation` `product-marketing`
