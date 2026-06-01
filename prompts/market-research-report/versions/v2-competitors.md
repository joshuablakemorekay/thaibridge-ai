# v2 — Named competitors + scraping tools

> **Status:** close reconstruction (the scraping instruction is preserved; the surrounding framing varied slightly across runs).

Added the specific competitor URLs and asked the model to scrape them with
dedicated tools rather than relying on general search:

```
Produce a market research report. Scrape these competitors directly:
1. https://ling-app.com  2. https://www.duolingo.com  3. https://thaipod101.com
Use the firecrawl / brave search MCP tools and whichever tools are available.
```

**What improved:** the competitor analysis became concrete and current —
real pricing and features from the actual sites, not generic descriptions.

**What I learned here:** naming a tool doesn't guarantee it runs. On the first
pass the report used the built-in web search, not the MCP scraping tools I
named. I had to check the tool usage, and one of the two scraping tools was
never actually called.
