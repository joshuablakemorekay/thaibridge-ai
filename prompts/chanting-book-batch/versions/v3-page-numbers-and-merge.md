# v3 — page numbers, and merging the chants already in

**2026-08-04**

## The request

```
Is it worth adding this set of instructions to Stage 1: include every page
number as appears when I paste chants so it is laid out exactly like the Thai
chanting book where I'm getting the chants from. Important so users can keep up
with the Monk who calls out page numbers or chant titles as we chant along.
```

```
Don't bother adding any of the 17 chants that already exist in the app Digital
Chanting Book which I added in previous sessions. Is it possible to include
these 17 existing chants in the pipeline as we go along adding the entire book's
chanting pages and re fit them as to fit the new structure we will be creating
rather than overwriting and ending up with duplicates?
```

```
Merge and report differences but keep existing chant unless I say otherwise.
```

```
Does this need to be stated everytime I use Stage 2 ?
```

It does not — it lives in the prompt. Anything you must remember to say is what
gets forgotten on batch 40 at ten at night.

## What changed

**A monk calls out a page, and everyone chants from it.** A wrong page number is
met in public, mid-chant, with no recovery — so its rules match the fidelity
rules: never infer, never estimate, never carry forward. No marker means no
`page_start` and a raised check. Pages are marked `[p.47]` on their own line.

Re-pasting the seventeen is how they get page numbers, and **the only chance to
check them against the book a second time.** The merge rule: never append or
suffix; add only what is missing; **the file wins**; compare anyway and report
every difference, acting on none. Stage 2 checks `len(CHANTS)` grew by the
number of **new** chants only.

Added: `page_start` and per-verse `page`; card badge and page-turn markers, both
guarded; three negative-tested criteria — page values must be bare integers, and
`page_start` must agree with the first marker.

## Deferred

```
At some point add a search tab so find a specific chant rather than having to
scroll the page. Add an alphabet list to select letter which opens all chants
with that letter and in alphabetic order.
Tried & tested method is to add two Spacing options and a table.
```

```
A tab for searching number and title would be great.
```

Spacing follows SuttaCentral's two-state toggle: compact rows versus opened-up
cards. Held back — designing a browse view against seventeen chants would be
guesswork about browsing 286.
