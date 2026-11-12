"""Build the cover of the printed chanting book, as one PDF sheet for Lulu.

    python scripts/build_chanting_print.py     # the inside pages first
    python scripts/build_chanting_cover.py     # then this
    python scripts/build_chanting_cover.py --final

A paperback cover is one sheet: back, spine and front side by side, with
3.175mm (0.125in) of bleed round the edge that Lulu trims away. The spine
is as thick as the book, so its width is worked out from the inside pages'
PDF using Lulu's formula for a softcover: pages / 444 + 0.06 inches.

Run it again whenever the page count changes — the cover is only right
for the book it was measured against, and the script says which that was.
"""
import argparse
import datetime
import os
import sys
import tempfile

import fitz  # PyMuPDF
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import chanting  # noqa: E402
from chanting_volumes import VOLUMES  # noqa: E402
from build_chanting_print import find_chrome, print_pdf  # noqa: E402

TRIM_W, TRIM_H = 210.0, 297.0     # A4, mm
BLEED = 3.175                     # Lulu's 0.125in
MM_PER_INCH = 25.4

# The emblem for the front of the three volumes (Josh, 2026-11-12). Kept
# OUTSIDE the repository, in the chanting book's OneDrive folder, because it
# is an emblem, not ThaiBridge artwork. With no emblem file the cover keeps
# the drawn Dhamma wheel.
DEFAULT_EMBLEM = os.path.join(os.path.expanduser('~'), 'OneDrive', 'Documents', 'Documents',
                              'SMOALD', 'ThaiBridge', 'Digital Chanting Book', 'Cover emblem.png')


def spine_width_mm(pages):
    """Lulu's softcover perfect-bound spine: pages / 444 + 0.06in."""
    return (pages / 444 + 0.06) * MM_PER_INCH


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--final', action='store_true', help='leave off the "proof copy" mark')
    parser.add_argument('--volume', type=int, choices=[v['number'] for v in VOLUMES],
                        help='make the cover for one volume of the three-volume edition')
    parser.add_argument('--emblem', default=DEFAULT_EMBLEM,
                        help='image for the front; used only if the file exists')
    parser.add_argument('--interior')
    parser.add_argument('--out')
    args = parser.parse_args()
    stem = f'chanting-volume-{args.volume}' if args.volume else 'chanting-book-a4'
    args.interior = args.interior or os.path.join(ROOT, '_print', f'{stem}.pdf')
    args.out = args.out or os.path.join(ROOT, '_print', f'{stem}-cover.pdf')
    volume = next((v for v in VOLUMES if v['number'] == args.volume), None)
    emblem = args.emblem if args.emblem and os.path.exists(args.emblem) else None

    if not os.path.exists(args.interior):
        sys.exit('Build the inside pages first: python scripts/build_chanting_print.py')
    with fitz.open(args.interior) as doc:
        pages = doc.page_count
    if pages % 2:
        sys.exit(f'The inside has {pages} pages; Lulu wants an even number.')

    spine = spine_width_mm(pages)
    sheet_w = BLEED + TRIM_W + spine + TRIM_W + BLEED
    sheet_h = BLEED + TRIM_H + BLEED
    # The spine text has to fit across the spine with room to spare.
    spine_font = round(min(14, spine * 0.32 / 0.3528 * 0.9), 1)

    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')), autoescape=True)
    html = env.get_template('print/chanting_cover.html').render(
        book=chanting.BOOK, proof=not args.final, built_on=datetime.date.today().isoformat(),
        trim_w=TRIM_W, bleed=BLEED, spine=spine, sheet_w=sheet_w, sheet_h=sheet_h,
        spine_font=spine_font, volume=volume,
        emblem_url=('file:///' + emblem.replace(os.sep, '/')) if emblem else None)

    with tempfile.TemporaryDirectory() as workdir:
        print_pdf(find_chrome(), html, args.out, workdir)

    with fitz.open(args.out) as doc:
        w_mm = doc[0].rect.width / 72 * MM_PER_INCH
        h_mm = doc[0].rect.height / 72 * MM_PER_INCH
        sheets = doc.page_count
    if sheets != 1 or abs(w_mm - sheet_w) > 0.5 or abs(h_mm - sheet_h) > 0.5:
        sys.exit(f'The cover came out {sheets} page(s) of {w_mm:.1f} x {h_mm:.1f}mm, '
                 f'not one sheet of {sheet_w:.1f} x {sheet_h:.1f}mm.')

    print(f'Done: cover for {pages} pages{" (emblem)" if emblem else ""}, spine {spine:.1f}mm, '
          f'sheet {sheet_w:.1f} x {sheet_h:.1f}mm -> {args.out}')


if __name__ == '__main__':
    main()
