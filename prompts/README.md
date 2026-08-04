# Prompt Library

[![Prompt Lint & Eval](https://github.com/joshuablakemorekay/thaibridge-ai/actions/workflows/prompt-eval.yml/badge.svg)](https://github.com/joshuablakemorekay/thaibridge-ai/actions/workflows/prompt-eval.yml)

This folder documents the prompts I used while building the Thai Language & Culture Learning App. It exists as **portfolio evidence** of prompt engineering, evaluation, and iteration — not as runtime configuration (settings the app needs to run).

Each prompt folder contains the final version, the reasoning behind it, an executable evaluation rubric (a set of automatic pass/fail checks), and the version history where I refined it over time. Every rubric runs automatically on every push via GitHub Actions (a robot that re-runs the checks for me).

## Index

| Prompt | Category | What it does | Iterated? |
|---|---|---|---|
| [`frontend-build`](./frontend-build/) | code-generation | Builds the app's templates, Thai-themed CSS, and interactive JS in stages | Yes (v1 → v3) |
| [`wireframe-layout-system`](./wireframe-layout-system/) | code-generation | Content-first layout system — site outline, per-page layout templates, reusable partials, responsive tables | Yes (v1 → v3) |
| [`gamification-system`](./gamification-system/) | code-generation | Adds XP/levels, locked sections, developer mode, and subscription tiers | Yes (v1 → v3) |
| [`romanization-system`](./romanization-system/) | language design | The custom Paiboon+ vowel system, beginner mode, and consistent rendering | Yes (v1 → v3) |
| [`buddhist-pdf-integration`](./buddhist-pdf-integration/) | content | Reproduces Pra Kru Bob's essays from PDFs faithfully as styled pages | Yes (v1 → v2) |
| [`ai-tutor-integration`](./ai-tutor-integration/) | agent-workflow | A 6-mode Claude-powered Thai tutor integrated into the app | Yes (v1 → v2) |
| [`claude-code-workflow`](./claude-code-workflow/) | agent-workflow | Driving Claude Code for a bug fix, refactor, tests, and code review with Git | Yes |
| [`market-research-report`](./market-research-report/) | analysis / research | Produces a grounded, source-backed market research report for the app | Yes (v1 → v3) |
| [`product-overview-section`](./product-overview-section/) | content | Generates a structured Product Overview using a clarifying-question loop | Yes (v1 → v2) |
| [`tones-consonant-classes`](./tones-consonant-classes/) | agent-workflow | Explore-first build of one free section teaching tones + consonant classes with progressive drills | No (single version) |
| [`chanting-book-entry`](./chanting-book-entry/) | content / agent-workflow | Two-stage workflow turning a page of a physical chanting book into a five-layer entry, without inventing canonical Pali | Yes (v1 → v4) |
| [`chanting-book-batch`](./chanting-book-batch/) | content / agent-workflow | The same workflow rebuilt for volume — several chants per message across a 286-chant book, with truncation made detectable | No (v1, forked from `chanting-book-entry` v4) |

## Featured iterations

Prompts where the v1 → final journey shows the most learning:

### [`market-research-report`](./market-research-report/)

This started as a one-line "research the market" request. v1 gave breadth but no grounding. In v2 I named the real competitors and pointed it at their websites to scrape — and learned that *naming* a tool doesn't mean it runs (one scraping tool was never actually called, which I only caught by checking). v3 pinned a fixed 10-section structure and fed in my own source documents, turning a freeform essay into a consistent, grounded report I could actually make decisions from.

### [`chanting-book-entry`](./chanting-book-entry/)

Four versions in a single day, each caused by a specific failure rather than a hunch. v1 worked but produced the right content in an unreliable shape — a good run and a poor run differed by luck. v2 made the good run the spec. v3 switched to JSON because long Thai and Paiboon+ values were being mangled by line wrapping in transit. v4 was the interesting one: two questions that were not reporting bugs each found one, both migration debris — rules written for a replaced format, still sitting there looking authoritative, neither producing an error. The lesson the folder records is that **a self-contradicting instruction does not fail loudly, it splits the difference** — a rule saying `ง → ng` beside an example showing `waŋ not wang` produced roughly a 65/35 mix across 900 dictionary cells.

### [`chanting-book-batch`](./chanting-book-batch/)

Forked from `chanting-book-entry` when the job went from one chant at a time to a 286-chant book. The useful part was measuring before rewriting: a finished entry is **×9.1** the size of what gets pasted in, and Thai script, IAST and Paiboon+ all tokenise at about **1.91 chars/token** — roughly half as efficiently as English. So the limit on chants-per-message was arithmetic, not wording, and no amount of rewriting would have moved it. What *did* move it was noticing that ~58% of an entry is commentary written **about** the chant, none of which needs checking against the physical book — so a `DATA-ONLY` depth defers it and fits 8–12 chants instead of 2–3.

The design lesson is about **where a failure report can live**. Batching's real risk is a reply cut off mid-array, which at eight chants is invisible because truncated JSON still parses. Nothing written at the *end* of a reply can report that, since in a truncated reply the end is precisely what is missing — so the manifest is declared **first**, and the count that proves nothing was lost survives the very failure it exists to catch.

It also produced the folder's best argument for negative-testing a rubric. All 17 criteria passed at 100%, which proved nothing until the checks were fed deliberately broken batches. That exposed an inherited condition, `(kh|th|ph)[aeiouɛɔəʉ]`, that had been quietly useless: every Paiboon+ syllable carries a tone mark, so it matched only unaccented spellings — the ones that never occur — while `thâng`, `khǎn` and `phrá` sailed through. **A green check mark is a claim, not evidence.**

### [`buddhist-pdf-integration`](./buddhist-pdf-integration/)

The first attempt quietly dropped paragraphs and reworded a Buddhist essay I'd asked to be reproduced exactly. The lesson — *faithful means faithful* — is the whole point of this folder: when wording matters, you insist on the complete text and check it against the source rather than trusting a tidy-looking summary.

### [`wireframe-layout-system`](./wireframe-layout-system/)

This started as "should I put the wireframe on *every* page?" and became a small **design system**. The key shift was realising a **wireframe is a planning tool, not a feature** — so instead of forcing one layout everywhere, I wrote a content-first outline and gave each page the shape that fits its job (Landing, 3-column content, Simple centered, Full-width tool), built from reusable partials. It also taught me that "tests pass / 200 OK" proves a page *loads*, not that it *looks right*.

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
- **5 minutes:** read this index plus the `REASONING.md` of any prompt above that interests you.
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
