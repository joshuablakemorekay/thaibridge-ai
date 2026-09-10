# -*- coding: utf-8 -*-
"""Write every chant's commentary out as one readable document.

Stage 3 writes prose into `chanting.py`, which is a 70,000-line data file
nobody can review by reading. This pulls just the five commentary fields out,
in book order, so the writing can be read as writing — on a phone, on paper,
anywhere that is not a code editor.

It reads; it never writes to chanting.py. Run it again after any batch:

    PYTHONIOENCODING=utf-8 DATABASE_URL="" python scripts/build_commentary_review.py

Output: docs/chanting-commentary-review.md
"""
import io
import os
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import chanting  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "docs", "chanting-commentary-review.md")

DONE = lambda c: bool(c.get('summary') and c.get('background'))


def title_of(c):
    """What to call a chant, preferring the book's own words."""
    bits = [c.get('title_thai') or c.get('title_pali') or c.get('title_roman') or '',
            c.get('title_english') or '']
    return " — ".join(b for b in bits if b) or c['id']


def pages_of(c, spans):
    p = spans.get(c['id'])
    if not p:
        return "no page number"
    return "page %d" % p[0] if len(p) == 1 else "pages %d–%d" % (p[0], p[-1])


def main():
    chants = chanting.chants_in_book_order()
    spans = chanting.chant_page_spans()
    done = [c for c in chants if DONE(c)]
    todo = [c for c in chants if not DONE(c)]

    L = []
    L.append("# Digital Chanting Book — commentary for review\n")
    L.append("Generated %s from `chanting.py`. Read-only extract: editing this "
             "file changes nothing.\n" % date.today().isoformat())
    L.append("**%d of %d chants have commentary. %d still to write.**\n"
             % (len(done), len(chants), len(todo)))
    L.append("Everything below is prose written for this edition. The Pali, "
             "Thai and English of the verses themselves are not reproduced "
             "here — this is only the commentary, so that it can be read as "
             "writing rather than checked as data.\n")
    L.append("What to look for: does it sound like the book? Is anything "
             "claimed that the chant does not say? Is a `source` wrong?\n")
    L.append("---\n")

    for c in done:
        L.append("## %s\n" % title_of(c))
        meta = [pages_of(c, spans)]
        if c.get('book_number'):
            meta.append("chant %s in the book" % c['book_number'])
        if c.get('english_unverified'):
            meta.append("English is a working translation")
        L.append("*%s*  \n`%s`\n" % (" · ".join(meta), c['id']))

        if c.get('source'):
            L.append("**Source (written for this edition):** %s\n" % c['source'])
        if c.get('source_printed'):
            L.append("**Source (printed in the book):** %s\n" % c['source_printed'])
        if not c.get('source') and not c.get('source_printed'):
            L.append("**Source:** *left empty — none could be given honestly.*\n")

        L.append("**What it is.** %s\n" % c['summary'])
        L.append("**When it is chanted.** %s\n" % c['when_chanted'])

        L.append("**Historical background**\n")
        for para in c['background']:
            L.append("%s\n" % para)

        L.append("**Meaning and purpose**\n")
        for para in c['meaning']:
            L.append("%s\n" % para)

        L.append("---\n")

    L.append("## Still to write\n")
    L.append("%d chants, in book order:\n" % len(todo))
    for c in todo:
        L.append("- %s — %s (`%s`)" % (pages_of(c, spans), title_of(c), c['id']))
    L.append("")

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write("\n".join(L))

    words = sum(len(" ".join([c['summary'], c['when_chanted']]
                             + c['background'] + c['meaning']).split())
                for c in done)
    print("%d chants written up, %d to go, ~%d words -> %s"
          % (len(done), len(todo), words, OUT))


if __name__ == "__main__":
    main()
