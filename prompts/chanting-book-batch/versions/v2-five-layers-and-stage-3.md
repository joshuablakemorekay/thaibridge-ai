# v2 — all five layers, and a third stage

**2026-08-04**

## The question that caused it

v1's `DATA-ONLY` dropped the per-verse `english` with the commentary:

```
If I choose to do DATA-ONLY does that mean all 5 layers of translation verse by
verse will be applied to 8-12 chants per input on claude.ai ? Then would it be
possible for me to add background, meaning and summary for each and every chant
afterwards?
```

It gave four, not five. The depth was named for what it kept.

```
1. Can DATA-ONLY include the fifth layer English? If yes then include it
2. Write the Stage 3 commentary prompt now.
```

```
Or do you think DATA-ONLY was good with 4 layers and English can be added to
each and every chant afterwards? Go ahead and get Stage 3 done.
```

## What changed

The batch count favoured four — 36 batches instead of 48. **Stage 3's safety
guarantee settled it:** it may not alter a character of any verse, proved by an
empty before/after diff. Writing English later means reaching inside ~5,800
verse dicts, weakening that check to "one key was added".

Added: `english` at every depth; rubric widened to five layers; **Stage 3**, the
commentary pass, reading chants from `chanting.py`; conservative `source` rules.

## Lesson

**The cheaper option was cheaper on the metric being optimised and worse on the
one that mattered.** Josh questioning the first answer surfaced that.
