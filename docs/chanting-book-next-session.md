# Chanting book — next session

Paste-ready brief for picking this work up cold. Updated 2026-08-10 after page
51 went in.

## Read first, in this order

1. `docs/chanting-book-photo-map.md` — the brief, read it fully
2. `prompts/chanting-book-batch/README.md` — the two-stage workflow
3. `C:\Users\joshk\OneDrive\Documents\Documents\Digital Chanting Book\chanting-book-batch-prompts.pdf`
   — the Stage 1 and Stage 2 prompts. **Read it before any fresh page read.**

## State — verify with git, don't take this file's word

- **Pages 1–51 are in and unbroken**, plus 217–221. **74 chants, 1,021 verses.**
  `/chanting` derives that line itself, so it is never stale.
- 11 of the 17 pre-page chants are verified against their photographs.
- Page 51 was applied on 2026-08-10; pages 32–50 landed the day before.

## How to work — this matters more than the tasks

**One page at a time.** Read the photograph, write the batch, apply it, show the
diff, commit, then **stop** and say the page is done. Ask before pushing and
before any commit to `main`. No `Co-Authored-By` trailer.

A page can hold more than one chant, and often three. **Read the whole page
before deciding what it contains** — page 30 was expected to be Pabbatopama
alone and turned out to hold the end of one chant, a brand-new one, and the
start of a third.

## Next: page 52, `IMG_0315`

It continues **คำเชิญบูชาและสวดนะโมและพระพุทธคุณ**, which opens at the foot of
page 51 and — going by the contents, whose next entry is at page ๕๕ — runs to
page 54.

**Its verse 2 is a PARTIAL line, `โย […]`.** Page 51's last printed line ends
with that single word, which begins the next unit. So page 52's batch is a
`continuation_of` that carries **verse 2 again, whole** — not a verse 3. That is
the one case where incoming text overwrites what is in the file; the rule and the
`# ‼ COMPLETED FROM p<N>` comment it requires are in the stage 2 prompt.

The evening service reprints the morning one's opening: page 51 holds the same
offering, salutation and invitation as pages 1–2, under titles the book prints
differently. They were entered again rather than stubbed as repeats, so page 51
shows what the book prints on it. Expect more of the same down this stretch —
and expect to have to check each printing against the earlier one word by word,
because the differences are real but small (punctuation, one title in three).

Pages 222 and 223 sit beside 217–221 which are already in, so they are a cheap
excursion whenever wanted.

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

## Three things waiting on Josh — ask, don't guess

**สวากขาโต, and which mark goes over the ส.** Page 51 prints it TWICE with a
mark above the ส, and at high magnification that mark is the same shape as the
thanthakhat in ประดิษฐ์ four lines above it, in the same face and size — so page
51 was read as **ส์วากขาโต**. The app now holds this one word three ways:
plain `สวากขาโต` (page 1, and the page-1 นมัสการ), `ส์วากขาโต` and `ส๎วากขาโต`.
Two of the three must be wrong. One look at the book settles the whole word
everywhere, and it is a chanted line, so it is worth doing early.

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
