# v6 — what the first real pages taught it

**2026-08-05**

## The request

```
Continue Stage 1 from page 7
```

```
Yes, update the prompt to v6 first
```

Everything in v5 was designed against three photographs: page 41, page 320, and
a contact sheet of page-number strips. v6 is the first version written against
the workflow actually running — pages 1 to 8 read, entered and verified. Three
of its rules turned out to be wrong, and none of them wrong in a way that would
have looked wrong afterwards.

## Two columns are not a property of one section

v5 said the roman-script pages from 319 onward are set in two columns. That was
true and far too narrow.

Page 7 is Thai script, single column for twelve lines of ปัตติทานะคาถา, and then
switches to two columns for the rest of the chant — with no heading, no blank
line, and nothing to announce it but the line lengths changing. `ฐาตุ จิรัง สะตัง
ธัมโม` on the left pairs with `ธัมมัทธะรา จะ ปุคคะลา` on the right to make one
verse.

So the rule is now a page-level check that applies in either script and has to
be repeated wherever the line lengths change, not a note attached to one part of
the book. The page map records `columns`, including `"1 then 2"` for a chant
that changes half way through, and every two-column chant raises a check showing
its first pairing.

It also gained a test the reader can apply alone: read the left column straight
down. If it makes continuous sense, it is one column. If it reads as a series of
unfinished half-lines, it is two and the right side completes them.

This is the most dangerous rule in the prompt, because reading down a column
produces Pali that is fluent, plausible and completely wrong.

## A footnote is not always a citation

v5 called footnotes "the book's own canonical citations" and sent them straight
to `source_printed`. Page 7's is exactly that: `๑. นัย ม. มู ๑๒/๑๓-๘`.

Page 8's is not. It reads `1. คะโต สำหรับอุบาสก ถ้าอุบาสิกา ใช้ คะตา` — use
คะโต if you are a layman, คะตา if a laywoman. An instruction to the reader, in
the same position, keyed the same way. Under v5 it would have been filed as a
canonical source, putting a line of Thai usage guidance into a field the app
prints as a citation.

Now the prompt names both kinds, sends only the citation to `source_printed`,
and puts an editorial note in a check quoting it in full. Where the kind is
unclear, it is treated as editorial: a missing citation costs nothing, a false
one is a wrong reference in a book about the Dhamma.

The same two pages also settled a smaller question. Page 7 numbers its footnote
๑ in Thai numerals; page 8 numbers its 1 in Arabic. Both are the first footnote
on their page. The numerals carry no meaning and are not converted.

## Service closings, on the second sighting

`จบสวดแจงเท่านี้` on page 41 had no home in the schema, and the decision then was
to leave it until a second example appeared rather than design a group level
around one page. `จบพิธีทำวัตรเช้า` on page 8 is that second example.

They belong to the PAGE, not to the chant above them — that chant has already
closed itself with its own จบ line, and attaching a second would say it ends
twice and would follow it anywhere else it is reprinted. So the page map row
carries `service_closing`, and the prompt gives the way to tell them apart: a
chant closing names the chant; a service closing names the service and follows a
chant that has already closed.

Waiting for the second example was right. One page would have produced a guess
about the book's structure; two produced a rule.

## A continuation that completes a line

Stage 1 stopped at the foot of page 6 with `ฑังสะมะกะสะวาตาตะปะสิริงสะปะสัมผัสสานัง
[…]` — a verse cut mid-sentence by the page break, reproduced as far as it was
printed and marked. Page 7 finishes it: `ปะฏิฆาตายะ,`.

Stage 2 had no rule for this. Its continuations append; its merges keep the file
unconditionally. Neither fits a line that must be REPLACED because what is in
the file is a line the book does not contain.

So v6 adds the one case where incoming text wins, with two conditions that must
both hold first: the existing line must end in `[…]`, and the incoming line must
start with the existing line minus that marker. If either fails it is an overlap,
not a completion, and Stage 2 stops. The replacement leaves a
`⚠️ COMPLETED FROM p<N>` comment recording what was there before, and is reported
separately, because "1 line completed" is a different event from "12 verses
added" and should not hide inside it.

## And a rule about reporting, from a bug in the run itself

Stage 2's own script printed "CONTINUES marker removed" and had not removed it.
The regex matched nothing and success was reported anyway, leaving a stale marker
on a chant that was now complete — which is worse than no marker, because those
are what Josh greps for to find outstanding work.

So the instruction to remove the marker now carries the instruction to verify the
removal: count the markers before and after and report both numbers. A step that
reports its own success without checking it is not a step.

## Evidence

Rubric to v4 with two criteria added — `columns` must say 2 or where it changes,
and a `service_closing` must be a real printed line. Both exercised in the mock
fixture rather than passing on absence, and negative-tested: a `columns` value of
`"two"` drops the batch below 100%.

Full suite green, 36 criteria on this prompt, 74 app tests passing.
