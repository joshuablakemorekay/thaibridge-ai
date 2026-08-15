# Chanting book — next session

Paste-ready brief for picking this work up cold. Updated 2026-08-15 after pages
61 to 65 went in.

## Read first, in this order

1. `docs/chanting-book-photo-map.md` — the brief, read it fully
2. `prompts/chanting-book-batch/README.md` — the two-stage workflow
3. `C:\Users\joshk\OneDrive\Documents\Documents\Digital Chanting Book\chanting-book-batch-prompts.pdf`
   — the Stage 1 and Stage 2 prompts. **Read it before any fresh page read.**

## State — verify with git, don't take this file's word

- **Pages 1–65 are in and unbroken**, plus 217–221. **94 chants, 1,264 verses.**
  `/chanting` derives that line itself, so it is never stale.
- 11 of the 17 pre-page chants are verified against their photographs.
- Pages 61–65 were applied 2026-08-14 and 2026-08-15; pages 55–60 landed
  2026-08-11 and 2026-08-12, and 51 to 54 over the two days before that.

## How to work — this matters more than the tasks

**One page at a time.** Read the photograph, write the batch, apply it, show the
diff, commit, then **stop** and say the page is done. Ask before pushing and
before any commit to `main`. No `Co-Authored-By` trailer.

A page can hold more than one chant, and often three. **Read the whole page
before deciding what it contains** — page 30 was expected to be Pabbatopama
alone and turned out to hold the end of one chant, a brand-new one, and the
start of a third.

## Next: page 66, `IMG_0329`

Page 65's closing paragraph is **cut by the page turn** — it ends at
`หลังจากเสร็จพิธีปรกติแล้ว` with no full stop, so page 66 opens by finishing
that sentence. Expect the same shape pages 62–65 have had: explanatory prose
around the chants rather than chant text alone.

**Page 63 was the first page in the book with no chant on it at all** — the
whole sheet is `คำอธิบายประกอบทำวัตรเย็น`, so its batch has an EMPTY manifest
and everything on it is a block. `check_batch`, `apply_batch` and `check_pages`
all handle that now; `check_pages` needed one fix to stop reporting such a page
as unrecorded. More pages like it are coming.

**A block's `number` can be a Thai letter.** Page 63's sub-notes ก and ข go in
as `'number': 'ก'`, and the template renders them exactly as printed. Do not
convert them to digits.

### Settled since: a prose chant with paragraphs

The gap the last brief flagged is closed. `para_start` on a verse plus
`verse_paragraphs` in `chanting.py` (commit `c3b38e6`) splits a prose chant into
the paragraphs the BOOK sets it in. Page 61 used it second and renders four
justified blocks; page 64's passage has no paragraph break at all and correctly
renders as one group of 37.

Pages 222 and 223 sit beside 217–221 which are already in, so they are a cheap
excursion whenever wanted.

## A rubric printed inside a chant goes on the VERSE

Pages 53 and 54 both print หมอบลงพร้อมกัน… between verse 14 and verse 15 of a
hymn. A page block cannot go there — `build_page_index` can only put blocks
between whole chants — so it rides on verse 14 as `'rubric'`, which the template
renders under that line. Same mechanism as page 1's (กราบพร้อมกัน).

`apply_batch` carries a verse `rubric` through, so declare it on the verse in
the batch file and it lands. Do not try to force it into `batch.pages.blocks`.

## The tooling, and what it will and won't do

`check_batch.py` then `apply_batch.py --dry-run` then apply. Both need
`PYTHONIOENCODING=utf-8` on Windows or they die on the first Thai character.

Three kinds of entry:

- **new** — a chant not in the app. Appended.
- **continuation** — `continuation_of`, bringing later verses of a chant already
  started. Carries on the verse numbering; never restarts at 1.
- **merge** — `merge_only: true`, for a chant already in the app in full. Brings
  `page_start`, `book_number`, `layout`, `source_printed`, a `closing`,
  `corrections` and `page_markers`, and **no verses**.

`corrections` overwrite text already in the app and are matched on the whole
literal, required to appear exactly once inside that chant, or they raise and
write nothing. `page_markers` record where a printed page turns inside a chant
already in the file — **without one, every verse lands on `page_start`** and the
page shows far more than the book prints. That was missed once already, on
Saccapāna verse 11.

### Then `check_pages.py`, which is the one that answers Josh's question

`scripts/check_pages.py` reconciles EVERY batch file against the app: does each
page show the chants, the verses and the blocks its photograph recorded, with
the same text. It is the third check, and the only one that asks whether the app
page matches the printed page — `check_batch` checks a batch against itself and
`apply_batch` only writes. Run it after every page. It also runs as a test
(`tests/test_check_pages.py`), so a page going out of step with its photograph
breaks the suite instead of waiting to be noticed.

It knows one rule worth knowing yourself: a line cut by a page break belongs to
the page it STARTS on, and the completed line must begin with the partial one.
The `english` layer is exempt from that prefix test — the gloss of half a
sentence is not the start of the gloss of the whole one.

## Raised on pages 61–65 — all open, all need the book

**The chant printed twice, and the app now holds it twice on purpose.**
Dhātupaṭikūlapaccavekkhaṇa is printed at page 61 AND page 207 — the สารบัญ
lists both. The pre-existing `dhatupatikula-paccavekkhana` has a Thai
translation, ~30 short verses and parenthesised rubrics; page 61 has none of
that, being Pali-only in four run-on paragraphs. Josh chose two entries, one per
printing, on the condition the app shows exactly what each page shows. So page
61 is `dhatupatikula-paccavekkhana-p61`, and the old entry takes `page_start`
207 when that page is read. **`IMG_0477` (page 207) has still not been read**,
so which printing the old entry came from is inference from its shape.

**The same chant name is spelt three ways in three places.** `อุทิสสะ` in the
book's own สารบัญ (so, in `CONTENTS`), `อุททิสสะ` on page 62's title and
colophon, `อุททิสะ` in page 63's sub-note ก. All read at 5–7×, all reproduced,
none reconciled. One look settles all three.

**Page 64 verse 24 is the ฬ/พ hazard on a chanted line.** The page reads
`โอพารกา` / `โอพาริเกนะ`; the canon has *oḷārikā* / *oḷārikena*, and the sense
of the clause — beings who need something tangible, which is why the stūpa was
allowed — favours the canon. The glyph was compared at 16× against a known พ on
the same page and matched, but the photo map already records that this exact
comparison cannot settle ฬ from พ. Reproduced as it appears. The first word also
appears to lack the ิ the second has, so the book may be inconsistent too.

**Vowels the book shortens where standard editions lengthen them.** Page 61
verse 14 prints `นีชชีโว` with a long ี where its other three paragraphs print
`นิชชีโว` — declared as a diacritic exception, since the book itself differs
from itself. Page 62 prints `หินา` and `วิริยัมหินา` short where editions have
*hīnā* and *vīriyamhinā*. All kept as printed.

**Two chants on pages 64–65 have no colophon**, unlike pages 60, 61 and 62.
Checked against both pages; the `closing` key is left off rather than composed.

## Four things waiting on Josh — ask, don't guess

**The orphan footnote across pages 57, 58 and 59.** Page 57 prints a marker ๑
with no footnote under it. Page 58 prints a footnote `1. วิ.มหา. 4/170` with no
marker anywhere in its body — every line end checked at 3×. Page 59 then prints
**both**: a marker ¹ on its last verse and `1. วิ.มหา. 4/171` at its foot. So 59
is the intact version of what 57 and 58 each have half of, and 4/170 and 4/171
are consecutive references in the same Vinaya volume.

That is evidence the note on 58 belongs to the marker on 57, carried over to the
next page's foot. It is **not** proof, because footnote numbers restart on every
page and the rule is not to pair across pages. Nothing was changed. Page 59's
own footnote is filed as `source_printed` on its chant; pages 57 and 58 have
`source_printed` left off entirely, and 58's note sits as a page block. One look
at the book settles all three at once.

**สวากขาโต, and which mark goes over the ส.** Page 51 prints it TWICE with a
mark above the ส, and at high magnification that mark is the same shape as the
thanthakhat in ประดิษฐ์ four lines above it, in the same face and size — so page
51 was read as **ส์วากขาโต**. The app now holds this one word three ways:
plain `สวากขาโต` (page 1, and the page-1 นมัสการ), `ส์วากขาโต` and `ส๎วากขาโต`.
Two of the three must be wrong. One look at the book settles the whole word
everywhere, and it is a chanted line, so it is worth doing early.

Pages 52–53 widened it from one word to a **class**. The same small mark turns
up over the ล of กัล์ยาโณ, the ธ of พุทธ์วา, the ส of พุทธัสสาหัส์มิ and the ส of
ส์วากขาตะตา — and the app already holds the first of those the other way, as
กัล๎ยาณัง with U+0E4E in `buddhabhithuti`. So the question is not "which mark on
this word" but **which of the two marks this book's printer uses**, U+0E4C
(thanthakhat ์) or U+0E4E (yamakkan ๎). One answer fixes every one of them, and
they are all chanted lines. Everything entered on pages 51–60 uses ์.

**Page 60 is the best evidence so far, and it points at ์ (U+0E4C).** It carries
the mark five times — อะปัจจะเวกขิต์วา, ท์วายะ, พ์รัห์มะ, ยาต์รา, อัพ์ยา — and on
ท์วายะ it stands alone at the start of a line with nothing crowding it. At 11×
it is an ε-shaped curl with a tail, not the crescent of yamakkan. That is a
photograph reading well, not a verdict: it says what the printer cuts, and the
book in Josh's hands is still what settles กัล๎ยาณัง. Nothing was changed on it.

**Page 60 also found the opposite case.** The book prints **อุณหัสสะ with no
mark at all**, where standard editions have อุณ๎หัสสะ. Both occurrences were
checked at high magnification and neither is marked; both are stored unmarked.
Worth knowing that this printer omits the mark as well as cutting it, because
the omission is exactly what a reader would "correct" without noticing.

**The ฬ/พ hazard.** These photographs cannot tell ฬ from พ at body-text size.
Proven twice against Josh's own readings from the book: page 23 line 19, and
อะสัมมุฬโห on page 22. Words written with ฬ as a **judgement, not a reading**:

- อะวิรุฬหิฉันทา — page 22
- ปีฬิตัสสะ — page 24
- วาฬะมิคานิ — page 29

**And the one that matters most.** Paṭiccasamuppāda writes the sense-bases word
as สะพายะตะนัง with พ at verses 4, 5, 16 and 17, and the photograph appears to
agree. Standard Pali is *saḷāyatana*, with ฬ. Josh's instruction to "let the
photo win" was given for paste damage and **must not be applied here** — the
photograph is precisely what cannot settle this, and applying it would fix four
wrong readings permanently. Left untouched pending the book.

## Eight chants still print their colophon as a chanted verse

A closing formula — `<title> นิฏฐิตา.` — is printed as a centred colophon, and
the app has a `closing` field that renders it that way. Twenty-eight chants use
it. But **eight of the pre-page chants hold that line as their last VERSE**, so
the app numbers it and lists it as though it were chanted:

Tilakkhaṇādi (p27), Devatābhisammantana (p27), Mettānisaṃsasutta (p22),
Mettānisaṃsagāthā (p23), Pabbatopama (p30), Ariyadhana (p31), Buddhaudāna (p32),
Bhaddekaratta (p33).

Devatādissa was the ninth and is fixed — `IMG_0288.PNG` shows its colophon set
exactly like the one above it, which the app already held as a `closing`. The
other eight were left alone deliberately: their pages are on the "to verify"
list in the photo map, and **the page is the only thing that can say which page
the colophon is printed on.** Pabbatopama proves why — page 30 runs its verses
to the very foot, so its colophon is on page 31, and the app currently shows it
on 30. Fix them as each page is read, not in a sweep.

## Settled — do not re-open

- **Page 59 repeats itself, and the book is what repeats.** Its last line prints
  `ประธานกล่าวเชิญชวนว่า หันทะ มะยัง ทะสะนาถะกะระณะธัมมะสุตตะ` for the second
  time in three lines. Page 60's first line completes that sentence, so the
  duplication is the compositor's, not an artefact of the page turn. Page 59's
  text stays exactly as printed.
- Page 23 line 19 is **วิรุฬหะ** (Josh, against the physical book).
- Variant readings **do** get a field; it exists as of `b40c9c5`.
- **Pages 5 and 21 are on both the index and the contents**, as of `a97326d`
  and `169777f`. An earlier version of this file said their absence was "not a
  fault and settled". That was wrong and Josh was right to push back: the
  *book* names neither, because both are pages a chant continues onto rather
  than starts on — but the *app* could still reach them, and now does. A chant
  card shows every page it runs across (`pages 4–5`, `pages 20–22`), and a
  contents line offers a button for every page in its stretch.
- **`/chanting` states its coverage** — "Pages 1–31 and 217–221 are in so far",
  as runs rather than a count, because a count reads as a continuous range.

## Things learned the hard way, worth not relearning

- **A new chant is appended to the end of `CHANTS`**, so it lands at the foot of
  its page whatever its number. Down-page order is now settled by the book's own
  chant numbering where every chant on a page has one — but nothing orders the
  unnumbered ones, so check a multi-chant page renders top to bottom correctly.
- **A pre-page chant's `source` may cite the wrong chant entirely.**
  Pabbatopama's named page 30's two footnotes, which belong to the two chants
  above it. Suspect any `source` naming more than one reference.
- **Not every missing chant is one of the seventeen.** Ādiyasutta, numbered 13,
  had simply never been entered, between two chants that were both already in.
- **A Render deploy usually takes about a minute but has taken 15.** Check with
  `render deploys list srv-d8k5ucm7r5hc738qhcb0 -o json --confirm` rather than
  polling the live page and guessing.
- **The English of a reprinted text is copied from the earlier printing**, not
  written again. The evening service reprints a great deal of the morning one,
  and two glosses of the same Pali that differ in wording read as two different
  lines. Pages 52 and 54 take their English straight from the app's pages 2 and
  3 wherever the Pali matches, and note in a check where it does not.

## Two faults in `apply_batch`, fixed 2026-08-11

Both were cosmetic and both misreported rather than miswrote, which is why they
survived so long — the data was right every time.

- **`# ‼ COMPLETED FROM p?`** wrote a literal `?`. It read `verse['page']`, but
  a completing verse correctly has no `page` key: the line belongs to the page
  it STARTS on, which is the earlier one. The page it arrived FROM now comes
  from `page_of()`, which asks the batch's own page map and takes the later of
  the two rows claiming that verse. The four existing comments were backfilled
  to p35, p41, p47 and p52, each confirmed against the comment beside it.
- **`CONTINUES markers: n -> n` was counted around the removal only**, so a
  batch that finished one chant and opened another reported `1 -> 0` of a file
  that still held one. It is now counted over the whole run. The guard that
  refuses to claim a removal it did not make is unchanged and still local.

## Batch 9 is readable again — and what it turned up

`check_batch --all` used to fail on one file: the page-9 batch, whose checks
were written as plain strings before the shape was settled. Its six checks are
now objects, the seventh was dropped (it was a `‼ COMMENTARY PENDING` marker,
which `apply_batch` writes from `depth` and is not a check at all), and the
three that name a verse have been moved in `chanting.py` to sit above the verse
they are about instead of floating at the top of an eighteen-verse chant.

**Page 9 renders byte for byte identically** — proved by hashing it before and
after — and it already matches the book: instruction items 3, 4 and 5, then the
eighteen verses, then the closing editorial note, in that order, each once.

**But "readable" is not "safe to re-apply".** Diffing the file against what
`render_chant` would now produce turned up one real difference beyond the
comments: `kham-choen-bucha-phitsadan` carries `'group': 'Morning chanting'` and
the renderer hard-codes `'General chanting'`. Re-applying would quietly
downgrade it. Nothing reads `group` today — it is the only chant of 81 that does
not say `General chanting`, so it is an outlier rather than a treasure — but the
lesson generalises: **before re-applying any batch, diff it against the file
first.** The file wins, and the renderer does not know that.
