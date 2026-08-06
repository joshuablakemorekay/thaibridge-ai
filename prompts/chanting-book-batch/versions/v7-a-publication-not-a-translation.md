# v7 — a publication, not a translation

**2026-08-06**

## The request

```
A good approach is to treat the project like a digital publication, not just a
translation.

Workflow summary:

OCR & Extract - Convert each book page into editable text.
Translate - Generate the five translation layers consistently.
AI Quality Check - Have Claude Code compare the OCR text, translations,
formatting, and Pali diacritics for errors.
Human Review - Read each page yourself (or with a knowledgeable reviewer) to
verify accuracy, especially for doctrinal or liturgical content.
Enrich Each Page - Where helpful, add: Introduction, Meaning, Purpose, Context,
Vocabulary, References.
Final QA Pass - Check spelling, navigation, formatting, audio, search, mobile
responsiveness, and that all five translation layers remain aligned.

For a 325-page chanting app, the best balance is:
Claude Code for automation, consistency checks, and generating supporting
content. You (or an experienced reviewer) for the final doctrinal and editorial
approval.

This approach creates more than a digital copy of the book - it produces a
richer educational resource with explanations, context, and learning material
that add value beyond the original text.
```

## What changed

**A seven-step lifecycle, stated once and inherited by every stage.** The prompt
had three stages and no account of how they fit together or where Josh sits in
it. Now: read the page, write the layers, quality check, human review, enrich,
final QA, approve — with steps 4 and 7 marked as Josh's and explicitly not
delegable. Both stage prompts carry a condensed copy, because a framing that
lives only in the documentation around the fenced blocks never reaches the
thing actually doing the work.

**Stage 1 now checks itself against the photograph before closing.** Four
checks: the layers agree with each other (`pali` against `pali_roman` unit for
unit, `thai` against `paiboon`, `english` against `thai`); romanised Pali is
spelled the same way throughout the batch; Paiboon+ has not drifted; and every
printed thing on the page is accounted for somewhere. This belongs in stage 1
and nowhere else — stage 2 may not open the images, so this is the last moment
the page is visible.

**Stage 1 collects vocabulary while the page is open.** Six to ten load-bearing
Pali terms a chant, glossed as this tradition uses them. Cheap with the page in
front of you and expensive as a re-read later.

**Stage 2 may no longer drop anything stage 1 recorded.** Every key of the batch
file has to be shown to have landed somewhere — a chant field, a `PAGE_BLOCKS`
entry, a check comment, or a stated decision to defer. "There is no field for
it" now stops the batch instead of quietly losing the content.

**Stage 2 ends with a QA pass on the rendered page.** Six checks that the data
checks could not catch: full test suite, `check_page_blocks()` clean, every new
string present exactly once, layers still aligned down the rendered page, book
layout showing only what the book shows, page turns working. Audio, search and
phone rendering are named as Josh's to check rather than assumed fine.

**Stage 3 states what enrichment is for.** A table mapping the questions a
learner arrives with onto the fields that answer them, and the note that a
`meaning` explaining the words but never saying why anyone recites the chant is
half written.

## Why

The workflow was built to reproduce a book accurately and did that well. What it
had no account of was the *value beyond the original text* — and, more urgently,
no step where anything checked that what stage 1 read actually reached the app.

That gap was not hypothetical. Pages 7 and 8 went live in August showing roughly
half of what the printed page shows. Stage 1 had read the rest correctly and
written it into the batch file; stage 2 had no field for it and let it go. No
error, no failing test, found weeks later by Josh reading the app beside the
book. The "everything must land somewhere" rule is that failure written down so
it cannot repeat, and the framing section explains why it matters: a page that
silently omits a third of the printed page is not a publication, whatever the
chant text says.

The division of labour is the other half. Josh's time is the scarce input on a
325-page book, and it was being spent partly on things a machine can prove —
whether two layers have the same number of units, whether a word is romanised
consistently. Moving those into stage 1 means his reading goes on doctrine and
liturgy, which is the only part nothing else can do.

## Impact

The vocabulary and references fields are deliberately NOT written into
`chanting.py` yet, and the prompt says so twice. `chanting.py` has no field for
either and the templates render neither, and writing data the app cannot display
is the same class of mistake as dropping data the app has no field for — a
second copy of the truth that nothing renders and nothing tests, drifting from
the batch file it came from. They stay in the batch files until the app grows
somewhere to show them.

One bug found while building the sheet: the PDF builder asserts the number of
fenced blocks matches the number of stages, and adding a fenced `json` example
inside stage 1's prompt block broke the fence and made the file look like it had
four stages. The assertion did exactly its job — it was added in v2 for this and
had not fired since. Examples inside a stage prompt are indented, never fenced.

Sheet rebuilt to 29 pages; prompt-sheet tests still pass.
