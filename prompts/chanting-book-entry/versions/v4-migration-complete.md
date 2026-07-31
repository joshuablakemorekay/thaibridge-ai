# v4 — Finishing the migration three questions exposed

> **Status:** verbatim from the Claude Code session, 2026-07-31.

Three questions, none of them reporting a bug. Each found one.

## Question 1

```
Does the JSON from Stage 1 mean the Stage 1 output? Is it the same thing?
```

They were not. The prompt asked for working notes as prose *before* the entry,
while the schema also carried a `working_notes` key — two instructions for one
thing, left from v3. A reply could carry the notes twice, once, or either, run
to run. That reads as flakiness rather than a bug with a cause.

## Question 2

```
Is the JSON object and it's closing sentence contained in the whole Stage 1
reply? Or do I get it from elsewhere?
```

Yes — but nowhere did either prompt say so. Undocumented is fine until someone
else reads it.

**Fixed by both:** the reply is now one JSON object plus a closing sentence, and
the note headings renamed to match the keys they feed (`Count` → `units`) —
having one field under two names is how the duplication survived review.

**It removed a live hazard too.** The JSON is found by taking the first `{` to
the last `}`, so prose above it was one stray bracket from breaking the parse —
fine on nine chants, broken on the tenth.

## Question 3

```
Did you update the Stage 2 prompt in GitHub? I can't see any changes.
```

It had. Reading it to *prove* it exposed the rest: three rules still looked for
`TITLE_PALI`, `INVITATION` and `SOURCE`, labels stage 1 stopped emitting at v3.
They could never fire — and they guarded **do not invent a title, a source or an
invitation the book does not give.** Silently dead.

**Fixed:** rewritten around what stage 1 sends — *an empty string is meaningful,
not missing data.*

## Also in v4

```
Add this to chant 2 card in app Digital Chanting Book so users can quickly and
easily identify which chant to look for in the book.
```

```
Can we add Reflection on Conditioned Phenomena (Sabbe saṅkhārā aniccā) rather
than Reflection on Conditioned Phenomena (Saṅkhāra)
```

Added `title_roman` — the Thai title romanised, so a reader who cannot read Thai
script can find the chant in a printed book. Its own field, not `title_pali`,
because mixing Pali and Thai romanisation is the confusion this workflow exists
to prevent.

The rename works the same way: *Saṅkhāra* is a topic several chants touch;
*Sabbe saṅkhārā aniccā* is this chant's opening line, and opening lines are how
chants are found.

## The lesson v4 records

All three bugs were migration debris — rules written for a format that had been
replaced, still sitting there looking authoritative. **None produced an error.**
All three were found by questions that assumed nothing.
