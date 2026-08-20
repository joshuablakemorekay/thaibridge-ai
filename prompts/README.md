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
| [`chanting-book-batch`](./chanting-book-batch/) | content / agent-workflow | The same workflow rebuilt for volume — a 286-chant book read from photographs, page by page, as a digital edition rather than a translation | Yes (v1 → v7, forked from `chanting-book-entry` v4) |
| [`xp-economy-audit`](./xp-economy-audit/) | analysis | Audits the live XP system per audience — found free-tier levelling unlocks nothing, plus two endpoints that minted XP on request | Yes (v1 audit → v2 remediation) |
| [`inclusive-positioning`](./inclusive-positioning/) | analysis / content | Separates the universal teaching from one culture's expression of it — found the app's copy contradicted its own access rules | Yes (v1 → v2) |
| [`register-levels-draft`](./register-levels-draft/) | content | Drafts nine levels of Thai formality against an existing template's contract, grounded in the app's own Paiboon index and flagged for review | No (single version) |
| [`free-tier-review`](./free-tier-review/) | analysis | Judges five free-tier giveaway proposals do-or-don't against the real gate logic — two were rejected, and one turned out to be a bug rather than a feature | Yes (v1 verdicts → v2 narrowing) |
| [`paiboon-lookup`](./paiboon-lookup/) | code-generation | Establishes what a romanisation lookup *can* be before building one — searches 1,217 reviewed entries rather than transliterating, so a miss reads as a miss | Yes (v1 options → v2 chosen build) |
| [`dhamma-ai-allowance`](./dhamma-ai-allowance/) | analysis | Checks a principle stated in a code comment against the gate that actually runs — found the Thai tutor could exhaust the Dhamma's free questions | Yes (v1 finding → v2 fix) |
| [`survival-thai`](./survival-thai/) | content | Builds a free, finishable starter section — and decides where it belongs first, which is what stopped it landing on a paid, alphabet-gated page | Yes (v1 → v3 findability) |
| [`alphabet-gate-audit`](./alphabet-gate-audit/) | analysis | Answers whether the alphabet should be free, then asks the harder question underneath — is the prerequisite drawn in the right place? | Yes (v1 answer → v2 breadth) |
| [`hero-copy-rewrite`](./hero-copy-rewrite/) | content | Rewrites the home page hero from a description of the site's structure into a promise — and records the three AI wordings that were rejected before the author wrote the final copy himself, then a second round where a tightening nearly deleted the same commitment again | Yes (v1 → v4, author-written) |
| [`critique-to-product-decision`](./critique-to-product-decision/) | analysis | Turns a hostile critique into a product decision instead of defensive copy — one section added, and one change explicitly refused | No (single version) |

## Featured iterations

Prompts where the v1 → final journey shows the most learning:

### [`hero-copy-rewrite`](./hero-copy-rewrite/)

The one entry here where **none of the AI's wording survived**, which is why it
is worth reading. A one-line brief — *"This doesn't sound very convincing"* —
produced a clean rewrite that was structurally right and culturally wrong. Three
proposed wordings were rejected in turn, each for a reason worth keeping: one
made Thai culture the unnamed thing being declined, one wrote the reader's life
as a set of walls, one positioned the reader as a spectator of someone else's
practice.

The failure it records is the useful part. An objection to the *phrase* "follow
no culture at all" was allowed to delete the *option* it described, dropping the
culturally-neutral path from the front page entirely. It took a direct question
to catch it. Every constraint in the v3 prompt was discovered by rejecting a
draft rather than stated up front.

**Round 2 is why the entry is still worth reading.** A later critique called the
hero overdone — correctly; it stated one promise five times — and proposed a
28-word replacement that quietly dropped the culturally-neutral branch all over
again. The same commitment came within one edit of being deleted twice, both
times by an argument about wording rather than about the commitment. What caught
it the second time was not judgement but `tests/test_dhamma_open_to_all.py`,
which asserts the clause is on the rendered page. **A position that matters
should be guarded by a test, not by whoever is editing the file that day.**

### [`critique-to-product-decision`](./critique-to-product-decision/)

The entry where the recommendation was **to change almost nothing** — which is
the hardest answer to get out of an assistant, and the reason the prompt is
worth copying. It asks what a criticism does to *the product*, names both things
the product exists for, and ends *"if any at all"*: explicit permission to say
no. Without that clause, anything asked for improvements will find some.

One change survived the sort, and it was not the one the critic thought was his
best point. One change was considered and refused, and the refusal is written
down with its reasoning — which is the part most archives leave out.

### [`market-research-report`](./market-research-report/)

This started as a one-line "research the market" request. v1 gave breadth but no grounding. In v2 I named the real competitors and pointed it at their websites to scrape — and learned that *naming* a tool doesn't mean it runs (one scraping tool was never actually called, which I only caught by checking). v3 pinned a fixed 10-section structure and fed in my own source documents, turning a freeform essay into a consistent, grounded report I could actually make decisions from.

### [`chanting-book-entry`](./chanting-book-entry/)

Four versions in a single day, each caused by a specific failure rather than a hunch. v1 worked but produced the right content in an unreliable shape — a good run and a poor run differed by luck. v2 made the good run the spec. v3 switched to JSON because long Thai and Paiboon+ values were being mangled by line wrapping in transit. v4 was the interesting one: two questions that were not reporting bugs each found one, both migration debris — rules written for a replaced format, still sitting there looking authoritative, neither producing an error. The lesson the folder records is that **a self-contradicting instruction does not fail loudly, it splits the difference** — a rule saying `ง → ng` beside an example showing `waŋ not wang` produced roughly a 65/35 mix across 900 dictionary cells.

### [`chanting-book-batch`](./chanting-book-batch/)

Forked from `chanting-book-entry` when the job went from one chant at a time to a 286-chant book. The useful part was measuring before rewriting: a finished entry is **×9.1** the size of what gets pasted in, and Thai script, IAST and Paiboon+ all tokenise at about **1.91 chars/token** — roughly half as efficiently as English. So the limit on chants-per-message was arithmetic, not wording, and no amount of rewriting would have moved it. What *did* move it was noticing that ~58% of an entry is commentary written **about** the chant, none of which needs checking against the physical book — so a `DATA-ONLY` depth defers it and fits 8–12 chants instead of 2–3.

The design lesson is about **where a failure report can live**. Batching's real risk is a reply cut off mid-array, which at eight chants is invisible because truncated JSON still parses. Nothing written at the *end* of a reply can report that, since in a truncated reply the end is precisely what is missing — so the manifest is declared **first**, and the count that proves nothing was lost survives the very failure it exists to catch.

It also produced the folder's best argument for negative-testing a rubric. All 17 criteria passed at 100%, which proved nothing until the checks were fed deliberately broken batches. That exposed an inherited condition, `(kh|th|ph)[aeiouɛɔəʉ]`, that had been quietly useless: every Paiboon+ syllable carries a tone mark, so it matched only unaccented spellings — the ones that never occur — while `thâng`, `khǎn` and `phrá` sailed through. **A green check mark is a claim, not evidence.**

**v7** is where the prompt stopped being about reproduction. Two pages went live showing about 40% of what the printed page shows — stage 1 had read the rest correctly and written it into the batch file, and stage 2 had no field for it and let it go. Nothing raised and no test failed; it was found by a human reading the app beside the book. The gap was structural: reconciliation compared chants against the manifest, and *nothing compared the leftovers against anything*. So v7 adds the rule that **everything stage 1 recorded must land somewhere, or the batch does not close** — "there is no field for it" is now a finding that stops the run, not a reason to drop content. Its mirror sits beside it: never write data the app cannot render, or you get a second copy of the truth that nothing tests and nobody reads.

The same release reframed the job — a digital **publication**, not a translation — with a seven-step lifecycle in which two steps, human review and approval, are marked as the developer's and explicitly not delegable. A machine can prove two layers have the same number of units; it cannot know that a line of Pali is the one the tradition actually chants. The five criteria added for v7 were each negative-tested before being trusted, on the same principle the paragraph above learned the hard way.

### [`inclusive-positioning`](./inclusive-positioning/)

A learner said the app felt culturally exclusionary. The instinct is to rewrite the copy; adding *"check what the access rules actually grant before proposing anything"* turned it into a finding instead — `SECTION_REQUIREMENTS` already made every Buddhism page free, level 1 and free of the alphabet prerequisite, with a comment reading *"you do not need to read Thai to chant along."* **The permissions were right and the shop window was lying about them.** The home page had been telling people to "pass the quiz to unlock the site" for a quiz that unlocks nothing in the Buddhism section.

The two constraints in v2 are both there because the first attempt got it wrong in a way only a human could see. It illustrated lay practice with *"practising the precepts in Britain"* — which is the same parochialism wearing a different flag, and led to the page being rebuilt on the Sigālovāda Sutta's six directions, universal by construction because every society has parents, teachers, partners, friends, people who work and people who teach. Then "foreigner" was renamed to "non-Thai", which is politer and **structurally identical** — both define a reader by not belonging. The fix was noticing that almost every sentence carrying the label already said "you", which made the label redundant: *"As a foreigner, you're NOT expected to initiate wai"* → *"You're not expected to initiate the wai."* The lesson the folder records is that **renaming a category is not the same as removing it.**

### [`register-levels-draft`](./register-levels-draft/)

The instructive part is what the prompt found rather than what it wrote. `templates/register.html` had been in the repo since the first commit, calling for a `REGISTER_LEVELS` dict that **never existed in any commit** — traced through the whole history including the deleted 236KB `app_backup.py`, where the name was also only ever *used*. Because the access gate ran before the view, the resulting `NameError` was invisible to everyone except learners who had paid or reached Level 4, and nothing linked to the page, so nobody ever reported it. **The gate hid the crash from exactly the people who could have reported it, and showed it only to the people who had paid.**

It also shows two review habits worth keeping: the review sheet is *generated from* the data so a corrected sheet cannot drift from an uncorrected dict, and the draft flags its own uncertainty per register rather than presenting nine registers at one confidence level.

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
- [x] **Honest authorship** — where I rewrote the AI's output myself, the rejected drafts and my reasons are recorded rather than hidden

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
