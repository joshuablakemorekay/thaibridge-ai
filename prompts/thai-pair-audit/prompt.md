# Thai/English Pair Audit

> **Category:** analysis
> **Model used:** Claude Opus 5 (Claude Code)
> **Project area:** Thai Language & Culture Learning App — teaching data integrity
> **Status:** production
> **Last updated:** 2026-09-10

## What this prompt does

Starts from one visible mismatch on the home page and asks whether the same
problem exists everywhere else. The app pairs Thai with English in hundreds of
places — vocabulary rows, conversation lines, page headings — and each pair is an
assertion that the two sides mean the same thing. Nothing had ever checked that
assertion in bulk.

It is the enforcement sequel to [`romanization-system`](../romanization-system/),
which is where the house romanisation was *decided*. This prompt is what found
out how widely it had stopped being followed.

## The prompt

**The opening question (verbatim) — this is the whole prompt that started it:**

```
Also there are corrections that need to be made, some of the Thai script doesn't
match, eg, 🪷 ThaiBridge AI
Learn the Dhamma. Learn Thai. Find Your Own Path.
พระธรรมและภาษาไทย - On Homepage here does the Thai script match the English?
```

**The go-ahead to generalise it (verbatim):**

```
Do it.
```

**The scope ruling, once the findings were split into "certain" and "needs a
native speaker" (verbatim):**

```
Do the ones you can verify, hold the rest for my teacher
```

## Inputs

- Every dict in `app.py`, `register_levels.py` and `thai_reading.py` carrying
  both a `thai` and an `english` key — 707 pairs
- Every `<span class="thai">` page heading in `templates/`
- `thai_consonants.py` as the authority on what each letter sounds like
- `prompts/romanization-system/REASONING.md` as the authority on house style
- Deliberately **excluded**: `chanting.py` (22,000 lines of Thai, with its own
  separate review pass already running)

## Why it is shaped this way

The question is narrow and answerable — *does this one line match?* — rather than
"check my Thai". That matters, because the narrow version can be answered
definitively and then generalised by machine, while the broad version produces an
essay. The home page mismatch was the worked example that proved the class of
bug existed; extracting all 707 pairs proved how often.

The second half of the shape is the scope ruling. Splitting findings into
*verifiable* and *needs a human* is what stopped the audit from doing damage:
around half the broken rows could only be repaired by inventing Thai, and
inventing Thai to fix wrong Thai is not a repair.

## Expected output

- A count of what was actually checked, and an explicit list of what was not
- Findings separated into outright errors, internal inconsistencies, and
  judgement calls — because they carry different risk
- File and line for every finding, so each one can be verified independently
- For each proposed fix, evidence the replacement is already used elsewhere in
  the codebase — or an admission that it is not
- Findings that turned out to be wrong on closer checking, reported as wrong
