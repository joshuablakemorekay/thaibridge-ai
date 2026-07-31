# v3 — JSON, single-line values, checks as an array

> **Status:** verbatim from the Claude Code session, 2026-07-31.

```
For Prompt 1 can we add this instruction: JSON with unwrapped single-line values
and the checks as a separate array.
```

**Why it mattered.** Stage 1 was emitting labelled text that stage 2 had to
parse by eye. Two things went wrong with that:

- **Wrapped lines.** Long values folded across lines on the way through the
  clipboard, and Thai script, Paiboon+ diacritics and IAST all survive a wrapped
  line badly.
- **Flags in transit.** Inline `⚠️ CHECK` notes read well on screen but were
  easy to lose when moving the text between two tools.

**What v3 changed.** Stage 1 now emits one JSON object whose keys already match
the dict keys in `chanting.py`, so stage 2 maps them straight across instead of
interpreting them.

Two rules carry the weight:

- **Every value on one line.** No wrapping, no literal newline inside a string.
- **Checks in their own top-level array**, each naming the verse it belongs to,
  or `null` where it concerns the whole chant. An array cannot be
  half-carried, and stage 2 reports how many it moved across.

`working_notes` stays inside the object as a reading aid; stage 2 ignores it.

**Rubric rewritten to match (v4 of the rubric).** Both newline failure modes are
covered — a genuinely wrapped value stops the object parsing at all, and an
escaped `\n` inside a value is caught by a separate criterion.

**Two sandbox traps found while writing it:** the evaluator runs pass conditions
in a restricted namespace with no `bool` and no `list`. An array is now
identified as "not a string, indexable, holding strings", which still catches a
bare blob.
