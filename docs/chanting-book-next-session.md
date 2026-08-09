# Chanting book — next session

Paste-ready brief for picking this work up cold. Written 2026-08-09.

## Read first, in this order

1. `docs/chanting-book-photo-map.md` — the brief, read it fully
2. `prompts/chanting-book-batch/README.md` — the two-stage workflow
3. `C:\Users\joshk\OneDrive\Documents\Documents\Digital Chanting Book\chanting-book-batch-prompts.pdf`

## State — verify with git, don't take this file's word

- `main` is 2 commits ahead of `origin` — unpushed.
- `scripts/check_batch.py` is **modified and uncommitted**: `merge_only()` and
  `verses_of()` were added but are never called.
- `prompts/chanting-book-batch/batches/batch-021-029.json` is **untracked**.
  Stage 1 for pages 21, 22, 24, 25, 29 is finished inside it. It currently
  **fails** `check_batch.py` (4 problems) and **crashes** `apply_batch.py` with
  `KeyError: 'verses'`.
- Pages live in the app: **1–20, 23, 26, 27, 28, 217–221**.

## How to work — this matters more than the tasks

**One page at a time.** Do not read several photographs or apply several pages
in one go; doing that was slow and expensive. For each page: apply it, run the
checks, show the diff, commit with `commit-message-pro`, then **stop** and say
the page is done before moving on. Ask before pushing and before any commit to
`main`. No `Co-Authored-By` trailer.

## Task 0 — unblock the pipeline (before any page)

Wire `merge_only()` / `verses_of()` into `check_batch.py`'s shape check and into
`apply_batch.py`'s `reconcile()`, so an entry that only adds `page_start`,
`book_number`, `source_printed` or a `closing` to a chant already in `CHANTS`
validates without restating its verses. Add `"merge_only": true` to the two
merge entries in the batch (`mettanisamsa-sutta`,
`devatadissa-dakkhinanumodana`). Green `check_batch`, clean `apply_batch
--dry-run`. Commit, then stop.

## Then, one at a time, from the batch that already exists

| task | page | what |
|---|---:|---|
| 1 | 21 | `parittakarana-patha`, verses 4–9, continuation |
| 2 | 22 | `parittakarana-patha` v10 finishes; `mettanisamsa-sutta` starts |
| 3 | 24 | `nidhikanda-gatha` starts |
| 4 | 25 | `nidhikanda-gatha` 26–33; `dhammagaravadi-gatha` starts |
| 5 | 26 | **a repair, not an addition — see below** |
| 6 | 29 | `viharadana-gatha` + `saccapanavidhyanurupa-gatha` |

**Task 5 detail.** Page 26 in the app is missing its top two-thirds: sixteen
verses of ธัมมะคาระวาทิคาถา plus that chant's closing are printed above
เทวะตาทิสสะ and the app shows none of them. Same class of loss as pages 7 and 8,
found the same way — by reading the photograph top to bottom rather than by
anything failing. Treat it as a repair of an existing page and show before/after.

## Then, new stage-1 reads (one page per turn, read the photo fresh)

| task | page | photo | what |
|---|---:|---|---|
| 7 | 30 | `IMG_0292` | Pabbatopama-gāthā |
| 8 | 31 | `IMG_0294` | Ariyadhana-gāthā + Paṭiccasamuppāda-pāṭho |

All three are among the 17 pre-page chants — **upgrade the existing entry in
place, never re-add**, or the book ends up with two copies of one chant.

## After the pages — the coverage wording

`/chanting` reports `page_count = len(pages)`, which reads as "pages 1–29" when
the pages entered are actually sparse. Once 21–31 are in, make the landing page
say what is honestly true about coverage rather than implying a continuous run.
Small change — agree the design with Josh first.

## Three things waiting on Josh — ask, don't guess

The photographs **cannot tell ฬ from พ at body-text size**. Proven twice against
Josh's own readings: page 23 line 19 (he confirmed ฬ; the photo shows พ at
maximum magnification) and the app's อะสัมมุฬโห on page 22. Three chanted words
in this batch were therefore written with ฬ as a **judgement, not a reading**,
and each carries a READING HAZARD check. One character decides each:

- อะวิรุฬหิฉันทา — page 22
- ปีฬิตัสสะ — page 24
- วาฬะมิคานิ — page 29

Also: page 21 prints อิทัมปิ สังเฆ where standard Ratanasutta editions read
ธัมเม. Not a reading doubt. Keep the book's reading and record the standard one
in the variant field added in `b40c9c5`.

## Settled — do not re-open

- Page 23 line 19 is **วิรุฬหะ** (Josh, against the physical book).
- Variant readings **do** get a field; it exists as of `b40c9c5`.
- **Page 5 missing from the contents is not a fault.** The book's own สารบัญ
  lists 1, 2, 3, 4, 6, 8… — page 5 is where Saṃvegaparikittana continues, not
  where anything starts. Same for 7 and 9. It is reachable by page number
  because it is a real page, and that is the correct behaviour.
- **Page 21 missing from the contents is not a fault either** — the สารบัญ jumps
  20 → 22 because Parittakaraṇapāṭha runs onto 21 rather than starting there.
