# Reasoning — Chanting Book Batch

Why this prompt exists alongside `chanting-book-entry`, and why it is shaped the
way it is.

## The problem

`chanting-book-entry` sets one chant per message. That is the right shape when
you are setting a chant carefully. It is the wrong shape for a 286-chant book.

At one chant a message that is 286 sessions of copy, paste, read, verify. The
question was whether Stage 1 could take 5–10 chants at a time instead.

## What the measurement said

Measured against the 17 chants already in `chanting.py`, with a real tokeniser
rather than an estimate:

| | |
|---|---|
| Pasted in per chant (Pali + Thai only) | 797 chars |
| Finished entry per chant | 7,247 chars |
| Expansion | **×9.1** |
| Thai + IAST + Paiboon+ tokenisation | **1.91 chars/token** |
| Output per average chant | **~3,794 tokens** |
| Longest chant so far (36 verses) | 7,450 tokens |
| All 286 chants | **~1.09M output tokens** |

Thai script, IAST diacritics and Paiboon+ characters tokenise about twice as
expensively as English. That is why a chant that looks short is not.

The conclusion that mattered: **the ceiling is arithmetic, not wording.** No
rewriting makes the output smaller, because the output *is* the book. At full
depth, 5–10 chants is 19,000–38,000 output tokens in one reply, which is past
where a chat reply is reliable.

## Where the room actually was

Breaking a finished entry down by field showed the way through:

```
meaning         22.8%  ┐
background      13.7%  ├ 41.6% — prose written ABOUT the chant
summary          2.8%  │
when_chanted     2.3%  ┘
verse.english   16.9%  ← translation
─────────────────────
verse.pali       9.4%  ┐
verse.pali_roman 9.6%  ├ ~36% — the actual book content,
verse.paiboon    8.3%  │       the part that must never be invented
verse.thai       6.1%  ┘
```

Only about a third of each entry is the fidelity-critical part. Roughly 58% is
commentary, and **none of the commentary needs checking against the physical
book** — it is not the book's words.

So the batch prompt trades commentary for chants, via a depth setting:

- `FULL` — 2–4 chants a reply
- `COMPACT` — 4–6
- `DATA-ONLY` — 6–9, and this is what makes 5–10 achievable

**All five layers are written at every depth.** The first draft dropped the
per-verse `english` at `DATA-ONLY` too, which bought 8–12 chants a reply instead
of 6–9. That was the wrong trade: a verse without its meaning is not usable, the
five layers are read together down the page, and a second pass over 286 chants
just to add one layer per verse costs more than it saves. So the depth setting
now only ever varies the prose written *about* a chant, never the chant itself.

That prose is ~32% of a finished entry. `DATA-ONLY` is not a degraded mode so
much as a reordering: it captures everything that has to happen with the book
open, and defers only what doesn't. Re-running the commentary later cannot put
verified text at risk, because it only adds keys.

Checked before recommending it: the template guards `background`, `meaning`,
`summary`, `when_chanted` and `source` with `{% if %}`, and already has a
`partial` idiom for incomplete chants. A `DATA-ONLY` chant renders correctly —
every verse shows all five layers, and only the chant's context is missing.

## Stage 3

The commentary pass is a third stage rather than a variant of stage 1, because
by the time it runs the chants are already in `chanting.py` — so it reads them
from the file and nothing is pasted at all. That is the real payoff of splitting
the depths: the deferred half stops being a copy-paste job.

Its governing rule is narrow and absolute: **do not touch a single character of
any verse.** It adds five keys to a dict that has been verified against a
physical book. So its verification step is a before-and-after dump of every
verse, title and invitation, diffed to prove the diff is empty — evidence rather
than assurance, since verified Pali that quietly changes would not look wrong
afterwards.

`source` gets its own rules for the same reason it does in stage 1: a plausible
citation is indistinguishable from a real one, so an uncertain source is written
`""`, and any source Claude attributes itself carries a `⚠️ UNVERIFIED SOURCE`
comment.

## The manifest-first design

The failure that batching introduces is a reply cut off mid-array. At one chant
a message you would notice. At eight you would not, because truncated JSON still
looks like JSON — and the entry that survives may be missing its last verses
without anything downstream being able to tell.

A marker at the end of the reply cannot catch this, because in a truncated reply
the end is exactly what is gone.

So the manifest comes **first**: every id Josh pasted, listed before any entry is
written. It survives truncation, and Stage 2's first action is to count it
against the entries that actually arrived. Mismatch means nothing gets written
at all.

Two supporting rules:

- *Finish or don't start* — a missing chant is obvious, a truncated one is not.
- *The manifest describes what you were given, not what you managed* — otherwise
  the model can make the check pass by trimming the manifest, which is the one
  thing that would make it useless.

## The drift check

Paiboon+ adherence decays over a long session; the pull back towards RTGS is
strong, and RTGS spellings look perfectly reasonable. This is the exact failure
`chanting-book-entry` was written to prevent, and batching makes it worse by
making sessions longer.

So Stage 1 scans its own `paiboon` values for `kh`, `th`, `ph` and `ng` before
closing the batch — four strings that cannot legitimately appear — and reports
the count. Stage 2 then re-scans the written file. Cheap, and it catches the one
error that would otherwise reach the app looking fine.

## Other changes from v1

- **Checks are per chant, not pooled.** Across eight chants a shared top-level
  `checks` array cannot be traced back to its chant.
- **Stage 1 proposes the `id`.** The manifest needs stable handles, and at 286
  chants Stage 2 needs to detect collisions against what is already in `CHANTS`.
- **Repeat handling.** The same chant appears in several services in a book this
  size. Stage 1 emits a `repeat_of` stub rather than setting it twice — but only
  on an exact match; any difference in printing means it is set in full with a
  check explaining how it differs.
- **`invitation` now carries all five layers.** The v1 template showed only
  `pali`, `pali_roman` and `english`, but the dicts in `chanting.py` have
  `thai` and `paiboon` too. Fixed here.
- **`english_unverified` is in the template.** It is used on 10 of the 17 chants
  and v1 never mentioned it, so it had to be added by hand each time.
- **Stage 2 reports per chant, not per batch.** A batch-level character-count
  total can balance while two individual chants are both wrong.
- **`PYTHONIOENCODING=utf-8` is stated.** Thai output crashes on Windows without
  it, and every verification step in Stage 2 prints Thai.

## What this does not solve

286 chants is ~1.09M output tokens whichever prompt is used. At `DATA-ONLY` that
is roughly 29–36 batches for the text, plus a commentary pass. It is a real
workflow, but it is still dozens of sessions, and a single chat cannot hold the
book — so the repeat detection only works within one session.

If the manual route proves too slow, the same two prompts run per chant through
the API from Claude Code would remove the reply ceiling and the drift entirely,
since each chant would get a clean context. That was costed at roughly £10–15
for the whole book. Left as a fallback rather than built, because the manual
route keeps Josh's eye on every chant — which is the point.
