# v5 — off chat entirely, and three shapes of page

**2026-08-05**

## The request

```
Claude.ai chat is unable to handle 9 pasted images from the chanting book. Would
it be better to adapt Stage 1 to Claude Code as I'm sure Claude Code can do this
entire job on it's own?
```

```
Lets update this ... as the new Claude Code Stage 1 and Stage 2 prompts. Is it
possible to pass over the rules onto the new Claude Code Stage 1 and Stage 2
prompts? Or is it not necessary?
```

The answer to the second question turned out to be the useful one: **almost all
of the rules carry over, because they are rules about the book, not about the
chat.** What dropped away was the postal service — one JSON object per reply, no
markdown fences, "confirm you understand, then wait". What had to be added was
everything to do with reading files rather than being handed them.

## What changed

**Both stages moved into Claude Code, and nothing is pasted anywhere.** Stage 1
opens the photographs from `~/OneDrive/Pictures/Digital Chanting Book/` and
writes a JSON file to `batches/`; stage 2 reads that file and writes
`chanting.py`. Every batch used to make a round trip through the clipboard, and
Thai script, IAST diacritics and Paiboon+ vowels are precisely the characters
that copy-paste damages quietly.

**Both stages still exist, against the obvious temptation to collapse them.**
One pass that read a photograph and wrote the chant in the same motion would be
marking its own homework, and the failure it guards against — a verse on a
plausible but wrong page — leaves no trace afterwards. So stage 1 is now
forbidden to touch the app, and stage 2 is forbidden to open the photographs.
Each rule exists to stop the pair collapsing back into one pass.

The file between them turned out to be worth more than a transport format. It is
the only permanent record of what each photograph said: `chanting.py` holds what
reached the app, the book is on a shelf, and a disagreement between them is only
diagnosable if the reading in between survived.

**Depth stopped being a ceiling and became a budget.** The `FULL` / `COMPACT` /
`DATA-ONLY` system existed because everything had to fit in one chat reply.
Writing to a file removes that cap. The depths stay, because cost and drift are
real, but the recommendation is now `DATA-ONLY` for a different reason: it keeps
the pass that needs the physical book open short, and that is the pass that must
not drift.

**Checks name the file.** `IMG_0304.PNG`, not "image 3" — the filename is what
lets a photograph be found and retaken.

**Filename order is not page order.** The files run IMG_0250 to IMG_0594 with
gaps where retakes were deleted, so they cannot line up with pages and never
will. Stated as a rule because the assumption is so natural to make.

## Three shapes of page, found by looking

A pre-flight over the photograph set — cropping the top strip of seventeen
images into one contact sheet, rather than reading seventeen full pages — was
meant only to check whether eight gaps in the filenames were missing pages. They
were all deleted retakes; nothing needs re-photographing. But it found two
things worth more than the question it answered.

**The book prints part of itself in roman letters.** From page 319 at least, the
Pali is set in Latin script with IAST diacritics and no Thai script anywhere.
That inverts the prompt's oldest division of labour, which said "you are writing
layers 2, 4 and 5": on those pages layer 2 is *printed*, so `pali_roman` becomes
a reproduce-exactly layer and `pali` is empty. The new rule that matters most is
the negative one — never back-transliterate roman Pali into Thai script to fill
`pali`, because that is inventing a chanted layer and it would look entirely
convincing.

**Those pages are set in two columns, and one line spans both.**
`Sātāgirā tisahassā` on the left pairs with `yakkhā nānattavaṇṇino` on the right
to make one verse. Reading down one column and then the other produces fluent,
plausible, completely wrong Pali — the worst failure available here, because
nothing about it looks wrong afterwards. Where the column structure is ambiguous
the instruction is to stop on that page rather than decide by feel.

**The front matter is numbered separately, and the numbers collide.**
Preliminary pages are numbered `(๓๗)` in bracketed Thai numerals while the body
uses plain Arabic, so the book contains a page `(๓๗)` and a page `37`. Recorded
as the same integer they would merge, and a reader asking for page 37 would get
whichever came first. Front-matter rows now carry `page: null`,
`page_printed: "(๓๗)"` and `front_matter: true`, and never enter the page index.

So a page is now one of three shapes — Thai-script Pali with or without a Thai
translation, Pali-only, or roman-script Pali in two columns — and the prompt
adapts per chant rather than per book.

## What did not change

The fidelity core, word for word: the five layers, the Paiboon+ table and its
drift scan, never reconstructing from memory, reproducing oddities rather than
tidying them, the register rules, the page map, continuations, repeats,
per-chant checks, footnote sources, closings, prose layout, rejoining
hyphenated line breaks, and the rule that only the top-centre number is ever a
page number.

That is the point worth recording. Changing the surface from a chat to a
filesystem changed how the work arrives and how it is written down. It changed
nothing about what is true of the book, which is most of what this prompt is.
