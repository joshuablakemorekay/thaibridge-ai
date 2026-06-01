# Reasoning: Market Research Report

## Goal

I wanted a proper, data-backed market research report for my Thai learning app — competitors, audience size, pricing, the gap in the market — not a vague "here's some thoughts" answer. I needed it solid enough to actually decide whether the app is worth pursuing.

## Iteration history

**v1** was broad: "produce a market research report for this app." It used the built-in web search and gave me decent breadth, but it wasn't grounded in my specific competitors.

**v2** I named the exact competitors to scrape (ling-app.com, duolingo.com, thaipod101.com) and asked it to use specific scraping tools. Big improvement — the data was now about real rivals, not generic ed-tech.

**v3 (current)** I pinned an exact 10-section structure *and* fed in two source documents (my Product Overview and a senior-analyst framing). That forced a consistent, structured, grounded report instead of a freeform essay.

## Failure modes the final version handles

- **Generic, unfocused output** — fixed by the fixed 10-section framework.
- **Made-up market data** — reduced by forcing it to scrape real competitor sites and work from my pasted source docs.
- **Tool assumptions** — I learned that *naming* a tool ("use brave-search") doesn't guarantee it ran. I had to check, and found one of the two scraping tools wasn't actually used. Now I verify which tools ran before trusting the result.

## Outcome

Produced long, structured, source-backed reports (a UK opportunity report and a competitor report) that genuinely informed my thinking about the market. Good enough to act on.

## What I'd change next

Confirm exactly which tools ran before trusting the output, and split the giant prompt into smaller parts — the report once hit a length limit and had to be continued in a second pass.

## Tags

`market-research` `research-synthesis` `tool-use` `structured-output` `grounding`
