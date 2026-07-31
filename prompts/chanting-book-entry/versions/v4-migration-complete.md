# v4 — Finishing the migration two questions exposed

> **Status:** verbatim from the Claude Code session, 2026-07-31.

Two questions, neither of which was reporting a bug, each of which found one.

## Question 1

```
Does the JSON from Stage 1 mean the Stage 1 output? Is it the same thing?
```

They were not. The prompt still told stage 1 to write working notes as a prose
section *before* the entry, while the JSON schema also carried a
`working_notes` key — two instructions for one thing, left over from the v3
switch. A reply could carry the notes twice, once, or in either place depending
on the run. That reads as the prompt being flaky rather than as a bug with a
cause, which is the worst kind to have.

**Fixed:** the whole reply is now one JSON object plus a single closing
sentence, and the notes live in `working_notes`. The four note headings were
renamed to match the keys they feed — `Count` → `units`, `Ordering problems` →
`ordering` — because having the same field under two names in the same prompt is
how the duplication got past review in the first place.

**It also removed a live hazard.** The JSON is located by taking the first `{`
to the last `}`, so any prose above it was one stray curly bracket away from
breaking the parse — fine on nine chants, broken on the tenth, for no visible
reason.

## Question 2

```
Did you update the Stage 2 prompt in GitHub? I can't see any changes.
```

It had. Reading it line by line to *prove* it had is what exposed the rest of
the problem: three rules in stage 2 still looked for `TITLE_PALI`, `INVITATION`
and `SOURCE` — uppercase labels of the text format stage 1 stopped emitting at
v3. Those keys could never arrive, so those three rules could never fire.

They guarded exactly the behaviour that matters most here: **do not invent a
title, a source or an invitation the book does not give.** The protection was
silently dead.

**Fixed:** rewritten around what stage 1 actually sends, with the principle
stated plainly — *an empty string is meaningful, not missing data.*

## Also in v4

```
Add this to chant 2 card in app Digital Chanting Book so users can quickly and
easily identify which chant to look for in the book.
```

Added `title_roman`: the Thai title romanised, so a reader who cannot read Thai
script can still find the chant in a printed book. It gets its own field rather
than borrowing `title_pali`, because mixing Pali romanisation with Thai
romanisation is the one confusion this whole workflow is built to prevent.

## The lesson v4 records

Both bugs were migration debris — rules written for a format that had been
replaced, still sitting there looking authoritative. Neither produced an error.
Both were found by a question that assumed nothing.
