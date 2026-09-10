# v2 — the sweep

Two words, once the single-line answer showed the bug class was real.

```
Do it.
```

## What changed

The unit of work moved from a line to a codebase. Every dict carrying both a
`thai` and an `english` key was extracted by parsing the AST rather than
grepping — 707 pairs across three modules — plus every `<span class="thai">`
page heading.

Structural checks ran first, because they are cheap and objective: same Thai with
different English, same English with different Thai, Thai fields with no Thai
script in them. Only then a semantic read of all 707.

`chanting.py` was excluded and the exclusion was stated. It holds 22,000 lines of
Thai and has its own review pass; including it would have buried the findings.

## What it produced

Roughly 40 defects, and — more usefully — proof that most of them violated a
romanisation standard the project had already written down in
[`romanization-system`](../../romanization-system/REASONING.md).

## What it got wrong

Extracting by dict key missed two whole shapes: `_syl()`/`_word()` positional
calls in `thai_reading.py`, and the `sound` field in `thai_consonants.py`. Both
surfaced later, one from a live-site check after the fix had already shipped.

An extraction method quietly defines the scope of its own audit. Ours said
"everything" and meant "everything shaped like a dict".
