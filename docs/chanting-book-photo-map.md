# Chanting book — page to photograph map

The book was photographed in one pass: 333 PNGs in
`OneDrive\Pictures\Digital Chanting Book`, `IMG_0250.PNG` – `IMG_0594.PNG`.

**Filename order matches page order, but there is no fixed offset.** Some pages
were shot twice and the spare shot later deleted, so the gap between the file
number and the page number grows as you go through the book. Do not calculate a
filename — look it up here, or read the page number off the top of the photo.

`IMG_0250` – `IMG_0263` are the cover and front matter. Body page 1 starts at
`IMG_0264`.

## Verified anchors

Every row below was read directly off the page number printed at the top of the
photograph.

| page | photo | offset |
|-----:|-------|-------:|
| 1 | IMG_0264 | 263 |
| 15 | IMG_0278 | 263 |
| 16 | IMG_0279 | 263 |
| 17 | IMG_0280 | 263 |
| 18 | IMG_0281 | 263 |
| 19 | IMG_0282 | 263 |
| 20 | IMG_0283 | 263 |
| 22 | IMG_0284 | 262 |
| 23 | IMG_0285 | 262 |
| 26 | IMG_0288 | 262 |
| 27 | IMG_0289 | 262 |
| 28 | IMG_0290 | 262 |
| 30 | IMG_0292 | 262 |
| 31 | IMG_0294 | 263 |
| 32 | IMG_0295 | 263 |
| 33 | IMG_0296 | 263 |
| 34 | IMG_0297 | 263 |
| 61 | IMG_0324 | 263 |
| 68 | IMG_0331 | 263 |
| 207 | IMG_0477 | 270 |
| 213 | IMG_0483 | 270 |
| 215 | IMG_0485 | 270 |
| 217 | IMG_0487 | 270 |
| 218 | IMG_0488 | 270 |
| 220 | IMG_0490 | 270 |
| 221 | IMG_0491 | 270 |
| 222 | IMG_0492 | 270 |
| 223 | IMG_0493 | 270 |

The offset is 262–263 through the low pages and 270 by page 207, so seven pages
somewhere between 68 and 207 were shot twice. Those stretches are unmapped.

## ⚠ Page 21 was never photographed

`IMG_0283` is page 20 and `IMG_0284` is page 22. There is no photograph of page
21. It needs re-shooting before the page pass can get past page 20.

Missing file numbers elsewhere (255, 293, 337, 350, 394–396, 398–399, 450,
587–588) are deleted duplicate shots, not missing pages — page 30 is present as
`IMG_0292` despite `IMG_0293` being absent.

## The 17 chants entered before the page pass

Chants 1–17 in `CHANTS` were transcribed from pasted text rather than from the
photographs, and had no `page_start`. Page numbers below come from the book's
own สารบัญ (already in `CONTENTS`) and the photos are the verified map above.

| chant id | page | photo | state |
|---|---:|---|---|
| mettanisamsa-sutta | 22 | IMG_0284 | to verify |
| mettanisamsa-gatha | 23 | IMG_0285 | ✅ verified 2026-08-08 |
| devatadissa-dakkhinanumodana | 26 | IMG_0288 | to verify |
| tilakkhanadi-gatha | 27 | IMG_0289 | to verify |
| devatabhisammantana | 27 | IMG_0289 | to verify |
| khemakhema-saranadipika | 28 **or** 215 | IMG_0290 / IMG_0485 | ambiguous — two similar titles |
| pabbatopama-gatha | 30 | IMG_0292 | to verify |
| ariyadhana-gatha | 31 | IMG_0294 | to verify |
| paticcasamuppada-patho | 31 | IMG_0294 | to verify |
| buddhaudana-gatha | 32 | IMG_0295 | to verify |
| bhaddekaratta-gatha | 33 | IMG_0296 | to verify |
| dhatupatikula-paccavekkhana | 61 **or** 207 | IMG_0324 / IMG_0477 | printed twice in the book |
| dvattimsakara-patha | 217–218 | IMG_0487 / IMG_0488 | ✅ verified 2026-08-08 |
| bharasutta-gatha | 218–219 | IMG_0488 / IMG_0489 | ✅ verified 2026-08-08 |
| **tilokavijaya-pattidana** | **220–221** | **IMG_0490 / IMG_0491** | **✅ verified and rebuilt 2026-08-08** |
| sankhara-contemplation | 222 | IMG_0492 | to verify |
| abhinha-paccavekkhana | 223 | IMG_0493 | to verify |

### Two to settle by eye

- **khemakhema-saranadipika** — the สารบัญ lists
  `เขมาเขมะสะระณะทีปิกะคาถา` at page 215 and
  `เขมาเขมะสะระณะคะมะนะปะริทีปิกาคาถา` at page 28. The entry's title matches
  the shorter one more closely, but page 28 sits in the same run as the other
  early chants. Check both photos.
- **dhatupatikula-paccavekkhana** — genuinely printed twice, at 61 and 207.
  Decide which printing the entry represents, or whether it needs two.

## Upgrade in place — never re-add

These chants already exist in `CHANTS`. When the page pass reaches their pages,
**edit the existing entry** — give it `page_start` and a `page` marker on the
verse where the page turns. Adding a fresh entry would leave two copies of the
same chant, one paginated and one not.

## What "verified" cost, for planning

Tilokavijaya took two full-page reads plus three crops. Reading only the page
number is far cheaper: crop the top ~170px of several photos, stack them into
one image, and read them in a single pass. That is how the table above was
built.

## Layout is per chant — do not infer it

The two-column setting in this book means different things in different chants,
and there is no way to tell but to look:

- **Two Pali pādas to a line**, Thai as a block beneath or absent —
  Tilokavijaya (220), Mettānisaṃsagāthā (23), Bhaddekaratta (33),
  Pabbatopama (30).
- **One Pali pāda to a line, Thai alongside in the right column** —
  Bhārasutta (218–219).
- **A two-column list, one item per cell, read left cell then right cell** —
  Dvattiṃsākāra (217–218).

A pāda-pairing pass that assumed the first of these joined Bhārasutta's eight
lines into four. That was wrong and has been undone. Check the layout on the
photograph before touching line division.

## The recurring fault in the pasted text

Wherever the book uses two columns, the paste tended to read them in the wrong
order — right cell before left, or grouping across the row boundary. It has
turned up in three chants so far (Tilokavijaya lines 1–3, Dvattiṃsākāra
throughout, and it is what the old "kept as printed, standard editions differ"
notes were actually seeing). Suspect it in any chant whose order disagrees with
the canonical text.
