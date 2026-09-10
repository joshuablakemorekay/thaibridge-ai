# v3 — verify or escalate

The constraint that decided what actually shipped.

```
Do the ones you can verify, hold the rest for my teacher
```

## What changed

It replaced a plan. The audit had proposed reconstructing five corrupt vowel
entries from their surviving romanisation and glosses. This ruling threw that
out and split the findings by evidence instead:

- **Fixable here** — the word *and* its romanisation already appear elsewhere in
  the codebase, so the replacement asserts nothing new.
- **Not fixable here** — anything needing Thai that exists nowhere in the repo,
  or a decision about vowels (`เอียะ`, `เอือะ`) that barely occur in real words.

## Why it was the right call

Two of the five entries were corrupt in the English gloss as well as the Thai —
`sʉ̀ŋ` glossed "tall building" matches no Thai word. Reconstruction would have
produced something confident and wrong, on a page people pay for. A visibly
broken row at least announces itself.

## What it produced

Eight vowel rows corrected against attested words; six left deliberately broken
and escalated to a native speaker in `docs/vowel-review-2026-09-10.md`, bilingual
and Thai-first with a correction line per row.

The general form is worth keeping: **an audit's most valuable output is sometimes
the list of things it refused to fix.**
