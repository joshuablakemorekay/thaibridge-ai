# v3 — JSON, single-line values, checks as an array

> **Status:** verbatim from the Claude Code session, 2026-07-31.

## The instruction

```
For Prompt 1 can we add this instruction: JSON with unwrapped single-line values
and the checks as a separate array.
```

One sentence, three decisions in it — the format, the line handling, and where
the flags live. Each solved a different problem.

Asked in the same breath, and kept because it is a check rather than a request:

```
Also did we add this: Make it like a book users can read/chant from and break it
down verse by verse.
```

It had been, at v2. Verifying rather than assuming is the habit that found two
real bugs at v4.

## What changed and why

Labelled text had to be parsed by eye, and long values folded in the clipboard —
Thai, Paiboon+ and IAST all survive a wrapped line badly. Inline flags were easy
to lose between tools.

Stage 1 now emits one JSON object whose keys already match `chanting.py`, so
stage 2 maps rather than interprets. Every value stays on one line. Checks move
to their own array, each naming its verse — an array cannot be half-carried.

Rubric rewritten to match. **Two sandbox traps found doing it:** the evaluator
has no `bool` and no `list`, so an array is identified as "not a string,
indexable, holding strings".
