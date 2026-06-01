# Prompt Library

[![Prompt Lint & Eval](https://github.com/MungManBaoIsan/Thai-App-NEW/actions/workflows/prompt-eval.yml/badge.svg)](https://github.com/MungManBaoIsan/Thai-App-NEW/actions/workflows/prompt-eval.yml)

This folder documents the prompts I used while building the Thai Language & Culture Learning App. It exists as **portfolio evidence** of prompt engineering, evaluation, and iteration — not as runtime configuration (settings the app needs to run).

Each prompt folder contains the final version, the reasoning behind it, an executable evaluation rubric (a set of automatic pass/fail checks), and the version history where I refined it over time. Every rubric runs automatically on every push via GitHub Actions (a robot that re-runs the checks for me).

## Index

| Prompt | Category | What it does | Iterated? |
|---|---|---|---|
| [`market-research-report`](./market-research-report/) | analysis / research | Produces a grounded, source-backed market research report for the app | Yes (v1 → v3) |
| [`product-overview-section`](./product-overview-section/) | content | Generates a structured Product Overview using a clarifying-question loop | Yes (v1 → v2) |

## Featured iterations

Prompts where the v1 → final journey shows the most learning:

### [`market-research-report`](./market-research-report/)

This started as a one-line "research the market" request. v1 gave breadth but no grounding. In v2 I named the real competitors and pointed it at their websites to scrape — and learned that *naming* a tool doesn't mean it runs (one scraping tool was never actually called, which I only caught by checking). v3 pinned a fixed 10-section structure and fed in my own source documents, turning a freeform essay into a consistent, grounded report I could actually make decisions from.

## Skills demonstrated

This library is structured to show:

- [x] **Prompt design** — every prompt has a documented goal and structure
- [x] **Iteration** — see `versions/` folders for prompts I refined
- [x] **Evaluation** — every prompt has a rubric with executable pass conditions
- [x] **Automated testing** — rubrics run on every push via [`prompt-eval.yml`](../.github/workflows/prompt-eval.yml)
- [x] **Regression prevention** — `--fail-under 0.8` blocks changes that drop the score below 80%
- [x] **Documentation** — every prompt has a REASONING.md explaining the *why*
- [x] **Verification habit** — I check which tools actually ran rather than assuming

## How to read this folder

- **90 seconds:** read this index and skim the featured iteration above.
- **5 minutes:** read this index plus the two `REASONING.md` files.
- **Longer:** read the [CHANGELOG](./CHANGELOG.md), then run the checks yourself (below).

## Running the evaluations locally

```bash
pip install pyyaml
python3 scripts/eval_runner.py --provider mock
```

This validates every prompt against its rubric using saved sample outputs (called fixtures), so it runs for free with no API calls. See [`results-summary.md`](./results-summary.md) for the latest run.

To run against the real API: set `ANTHROPIC_API_KEY` and pass `--provider anthropic`.

## Changelog

See [`CHANGELOG.md`](./CHANGELOG.md) for a dated view of how these prompts evolved.
