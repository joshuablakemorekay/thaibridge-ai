# Reasoning: Chanting Book Entry

## Goal

Turn a page from a physical Thai chanting book into a finished entry in the
app's Digital Chanting Book — five layers per verse, plus the background and
meaning sections — **without the model ever inventing canonical text.**

That last clause is the whole design. Pali chants are exactly the kind of text
a language model half-remembers. Ask it to fill a gap and it will produce
something that scans beautifully, reads plausibly, and is not what the book
says. In a chanting book destined for print, that is the worst possible failure
mode, because nothing about the output looks wrong.

## Why two stages on two surfaces

| Stage | Surface | Why there |
|---|---|---|
| 1 | Claude.ai chat | Language work — transliteration, romanisation, translation, writing the background. It needs reading and correcting, which suits a chat window. |
| 2 | Claude Code | File work — writing a Python dict into `chanting.py` and proving it renders. Needs an agent that can run the app. |

Splitting them also puts a human checkpoint in the middle, which is where the
verification against the physical book actually happens.

## The techniques doing the work

**Context and examples.** Stage 1 carries a full worked chant. One example
teaches format, register and romanisation together, far more reliably than
description alone.

**Output constraints.** Fixed field labels (`TITLE_THAI:`, `VERSE 1`, `pali:`)
so stage 2 can map them mechanically. Free-form prose here would mean guessing
at stage 2, and guessing is the thing being designed out.

**Think-first.** Stage 1 splits and pairs the text and reports what it could
not resolve *before* producing anything, so the uncertainty surfaces instead of
being smoothed over.

**Role.** "I am the editor; you are the typist and translator" sets the
relationship: the model does not get a vote on what the text says.

## The rules that came from real failures

Each of these was added after something went wrong.

**"Never reconstruct from memory."** On the first chant, four OCR errors were
caught by reading against the physical book. A model asked to tidy those would
have silently corrected them into a different text.

**"Add ⚠️ CHECK rather than guess."** Turns a silent corruption into a visible
question. On the second chant this produced four flags in one pass — a missing
Pali title, an uncertain source, a crossed Pali/Thai order, and a probable
one-character slip (ฉุฑโท where standard editions read chuddho). None of those
would have been visible otherwise.

**"One Pali line per verse."** The first attempt at the second chant grouped
several Pali lines into one verse where the source ran them together. It was
faithful, but it did not read like a chanting book — you could not chant a line
and then read what it meant. A chanting book breaks per line, and the prompt
now says so.

**"Never invent a title, source or invitation."** The second chant had no Pali
title and no invitation line. The instinct to fill every field is strong and
has to be explicitly disabled; the template was changed to skip empty fields
instead.

**"Do not convert the Paiboon."** The romanisation layer uses Paiboon+, the
custom system described in [`romanization-system`](../romanization-system/).
Draft outputs kept drifting into RTGS (`khɔ̌ɔng`, `thîang`, `phrá`) which,
mixed into the same book as `kɔ̌ɔŋ`, `tîaŋ`, `prá`, stops the layer teaching
anything. One book, one system.

## What "good" looks like

The stage 2 verification is the honest test, and it is a character count in
both directions: every Thai and Pali character in the source appears in the
file, and no character appears that was not in the source. On the second chant
that came out 869 in, 869 out, nothing added or dropped.

"It imports and the page returns 200" proves the file parses. It does not prove
the text is right.

## Known limits

- Stage 1 has been dry-run in Claude Code rather than in Claude.ai itself.
  Running it in its real surface is still outstanding.
- The `paiboon` and `pali_roman` layers remain **unreviewed drafts** until
  checked against the physical book — flagged in the `chanting.py` docstring.
- Attribution of a canonical source is the weakest part. The prompt tells the
  model to omit it rather than guess, and stage 2 marks any inferred source
  with a ⚠️ UNVERIFIED comment.
