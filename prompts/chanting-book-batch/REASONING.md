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

## Reading the book instead of retyping it

v4 changed where the text comes from: Josh photographs nine pages and pastes the
images, rather than transcribing them and marking each page turn by hand. That is
a smaller change to the prompt than it sounds and a much larger one to the
guarantees.

What it buys is page fidelity for free. The page turn no longer has to be
remembered and typed — it is visible in the image, because one photograph is one
page. Marking 286 chants' worth of page breaks by hand was the part of v3 most
likely to decay quietly around batch forty.

What it costs is the ability to say "reproduce exactly what I pasted". A
photograph has glare, a curved gutter, a cropped last line, a thumb. Every one of
those produces a partial line, and a partial line is exactly what a language
model is best at completing convincingly. So the fidelity rules were re-pointed at
the specific thing that goes wrong: reproduce what is legible, mark the gap
`[…]`, name the image so it can be re-photographed. Knowing the chant is not
permission to finish it — this book's printing sometimes differs from a standard
edition, and recording those differences is part of the point.

## The page map, and why a second manifest

The prompt's oldest good idea is the manifest: declare what should arrive before
writing any of it, so a truncated reply is detectable. v4 applies it to pages.

It is needed because per-verse pages are stored sparsely. A verse carries `page`
only where the printed page turns; everything after it is carried forward. That
is compact and it matches how `section` already works — but it means **one
missing marker moves every following verse onto the wrong page**, and produces
data that looks entirely well-formed. There is no internal contradiction for
anything downstream to catch.

So stage 1 declares a page map — one row per page per chant, with the verse range
— before it writes the entries, and stage 2 rebuilds the pages by carrying forward
and compares the two verse by verse. Neither side may be edited to agree with the
other; a disagreement stops the write and gets shown. One side is what the
photograph said and the other is what would have gone into the app, and which one
is wrong is not stage 2's call to make.

This is the same shape as the paiboon scan: stage 1 checks itself, stage 2 checks
stage 1, and the failure being guarded is one that leaves no trace.

## Continuations, which "finish or don't start" got wrong

Nine images is a photographing rhythm, not a unit of meaning. A chant runs off the
last page most batches. v3 had one rule for an entry that stopped early — *finish
or don't start* — and it was built for truncated replies, where stopping early
means something went wrong.

Here it means the book carried on. Treated as truncation it would be re-sent and
duplicated; treated as completion it would be silently short. The two look
identical in the output, so v4 makes the model say which it is: `continues: true`
on a chant the book carries onward, listed separately in `batch_status.continues`
from `not_started`. The other half arrives next batch carrying `continuation_of`,
keeps counting verses from where the first stopped, and is appended to the same
dict.

Stage 2 prints the seam — the last two verses from before, the first two from
after — because a gap or an overlap at the join is invisible afterwards and is
the one way one chant becomes two. Stage 3 skips anything still marked
`⚠️ CONTINUES`: commentary about half a chant describes something that does not
exist, and unlike the half-chant itself, it would look finished.

## Why the page view is not built by the batch prompts

Stage 2 still may not touch the route or the template, even though every page rule
in v4 exists to serve a page-by-page reading view.

Keeping them apart is the point. A batch prompt runs thirty-odd times against
verified text, and its diffs have to stay boring enough that Josh can actually
read them. A prompt that could also alter how the whole book renders would
produce diffs nobody checks — and the failure it exists to prevent is precisely
the one that hides in a diff nobody checks.

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

## v7 — a publication, not a translation

Josh reframed what the project is:

> "A good approach is to treat the project like a digital publication, not just
> a translation."

The workflow reproduced the book accurately and had no account of two things:
the value beyond the original text, and — more urgently — any step where
something checked that what stage 1 read actually reached the app.

### What found it

Not a test. A question:

> "What about Page 7 & 8 which are both empty?"

I checked the data, the local render and the live site, found the chant text
present in all three, and reported no problem. That was the wrong answer to the
wrong question. Josh corrected it:

> "I checked them in the app against the book and they don't appear to contain
> everything so make it exactly the same as the book."

"Empty" meant *incomplete against the book*, not blank. Page 8 was serving about
40% of what its printed page shows — the service closing, the explanatory
section, its numbered items and a footnote were all missing. Stage 1 had read
every one of them correctly and written them into the batch file; stage 2 had no
field for them and let them go. Nothing raised, no test failed, and it was found
weeks later by a human reading the app beside the book.

### The failure mode v7 handles

The batch file and the app were never compared. Reconciliation checked chants
against the manifest; nothing checked the leftovers against anything.

So v7 adds a gate: every key of the batch file must be shown to have landed
somewhere — a chant field, a `PAGE_BLOCKS` entry, a check comment, or a stated
decision to defer — and **"there is no field for it" now stops the batch** rather
than losing the content. Its mirror is written down beside it: never write data
the app cannot render, or you get a second copy of the truth that nothing tests
and nobody reads, drifting from the batch file it came from.

The rest follows from the same framing. Stage 1 checks itself while the
photograph is still open, because stage 2 may not open the images and that is
therefore the last moment the page is visible. Stage 2 ends with a QA pass on
the rendered page rather than the data. Steps 4 and 7 of the seven — human
review and approval — are marked as Josh's and not delegable, because a machine
can prove two layers have the same number of units and cannot know that a line
of Pali is the one the tradition actually chants.

### Outcome

Shipped. Josh then set the constraint that made it provable:

> "It should still do everthing it did before such as complete app pages to look
> exactly the same as physical book images, except with the additional
> improvements added"

Verified rather than asserted: 229 lines added and **0 removed**; 45 → 49
sections with all 45 originals still present; all 11 page-fidelity rules intact.

### Engineering on the output

- *Accepted as-is:* the bulk of the prompt text and the block-model code went in
  as generated.
- *Reworked, and why:* Josh wrote no code this session. His contribution was
  direction and review, and it changed the work substantially. He found the
  defect by reading the app beside the physical book, which no test could have
  done. He set the standard — "exactly the same as the book" — that turned a
  content gap into an architecture change. He specified the v7 workflow. He
  rejected the first framing of the problem, and demanded proof that v7 was
  additive rather than accepting the claim.
- *Also caught:* two process failures — commits made to `main` without asking,
  and commits carrying a `Co-Authored-By` trailer his own skill forbids. Found
  by a question rather than a review:

  > "Is push part of commit-message-pro?"

  Both are now enforced by tooling rather than by memory.
- *Roughly:* direction and review, not code. The discovery was the highest-value
  act in the session and none of it was the AI's.

### What I'd change next

`vocabulary` and `references` are collected but unwritable — the app has no field
for either, and the prompt says so twice rather than letting them be written
somewhere useless. That is the next piece of work, and until it exists the
enrichment half of the publication framing is only half-built.

**Tags:** `content` `agent-workflow` `quality-assurance` `claude-code`
