# Market Research Report

> **Category:** analysis / research
> **Model used:** Claude (Claude.ai, extended research + MCP tools)
> **Project area:** Thai Language & Culture Learning App — go/no-go market research
> **Status:** production
> **Last updated:** 2026-04-17

## What this prompt does

Produces a long, structured, source-backed market research report for the app: competitor analysis, audience size, pricing, market gap, risks, and a go/no-go recommendation. It is grounded by feeding the model two source documents (a Product Overview and an analyst framing) and by scraping real competitor websites, instead of letting the model write a freeform essay from memory.

## The prompt

This was sent across two parts in the same turn: a framing document and an execution instruction.

**Part 1 — analyst framing (pasted document):**

```
You are a senior market research analyst and startup strategist. Produce a
comprehensive, high-quality market research report for the following business
idea: Thai language and culture learning web app like this one.
- It also teaches Buddhism, temple etiquette, business etiquett
```

> **TODO (verbatim gap):** the pasted framing document continues past this point but is truncated in the saved chat history. Paste the full original document here — you still have it. Do not let anyone "reconstruct" it from memory; quote it exactly.

**Part 2 — execution instruction (verbatim):**

```
Use two PASTED documents to produce a comprehensive, data-rich market research
report.
2. Use firecrawl-mcp to scrape : 1. https://ling-app.com 2. https://www.duolingo.com
3. https://thaipod101.com
2. Use brave-search-mcp and whichever tools are available to produce the report.
```

## Inputs

- `app_description` — what the app does and who it serves
- `market` — the geographic market to focus on (e.g. "UK")
- Two attached source documents: the Product Overview and the analyst framing above
- Three competitor URLs to scrape: ling-app.com, duolingo.com, thaipod101.com

## Expected output

A long markdown report covering roughly ten sections: Executive Summary, Target
Market Analysis, Customer Personas, Competitor Analysis, Monetization & Pricing,
Distribution Channels, Branding & Positioning, Risks & Challenges, Go-To-Market
Strategy, and a Feasibility / Final Recommendation. It should name the real
competitors (Ling, ThaiPod101, Duolingo), include concrete UK market figures
(£ amounts and audience sizes), and lay out a structured pricing model.

## Related files

- Reasoning: [`REASONING.md`](./REASONING.md)
- Evaluation rubric: [`rubric.yaml`](./rubric.yaml)
- Version history: [`versions/`](./versions/)
