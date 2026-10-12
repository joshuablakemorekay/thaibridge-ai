"""Build the Digital Chanting Book as one print-ready A4 PDF.

    python scripts/build_chanting_print.py            # proof copy
    python scripts/build_chanting_print.py --final    # no "proof" stamp

Every chant in book order, with all five layers and a short commentary, laid
out by templates/print/chanting_book_print.html and turned into a PDF by the
copy of Chrome already on this machine (headless, so no window opens).
Nothing new to install: Chrome shapes Thai properly, which ReportLab does
not — its stacked vowels and tone marks land in the wrong place.

ONE A4 volume. The first layout was A5, which ran to over 1,100 pages and
needed three volumes — too many, and too expensive to print. A4 with the
verses in two columns holds the whole book in one.

The commentary is the short version from chanting_print_short.py; the app
keeps the full text. A chant with no short version yet is printed with its
full text, and the script says how many those are.

The contents page needs to know which PDF page each chant lands on, and that
is only known once the PDF exists. So the book is rendered TWICE: pass one
with placeholder numbers, then PyMuPDF finds each chant's invisible locator
text, then pass two with the real numbers. The page-number column is a fixed
width in the CSS, so both passes paginate identically — and the script
checks that rather than trusting it.

Reads only chanting.py and chanting_print_short.py. It never imports app, so
it never touches the live database.
"""
import argparse
import collections
import datetime
import os
import shutil
import subprocess
import sys
import tempfile

import fitz  # PyMuPDF
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import chanting  # noqa: E402
from chanting_print_short import SHORT  # noqa: E402

CHROME_PATHS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
]

# Chants with no book page cannot be placed, and go at the end under a
# heading that says so rather than being guessed into a part.
UNPLACED = {'title': '', 'title_english': 'Chants not yet placed on a page of the book'}

# The app's own ThaiBridge Spelling font, so paper and screen draw the
# spelling from one file. See scripts/fetch_spelling_font.py for why the
# spelling has a font of its own.
SPELLING_FONT = os.path.join(ROOT, 'static', 'fonts', 'thaibridge-spelling.woff2')


def locator(chant_id):
    return f'LOC[{chant_id}]'


def find_chrome():
    for path in CHROME_PATHS:
        if os.path.exists(path):
            return path
    found = shutil.which('chrome') or shutil.which('msedge')
    if found:
        return found
    sys.exit('Could not find Chrome or Edge to print the PDF with.')


def book_parts():
    """Every chant in book order, grouped under the book's own part headings.

    The part headings are the `section` rows of CONTENTS (ทำวัตรเช้า and the
    like), each with the book page it starts on. A chant belongs to the last
    part that starts at or before its own first page. Chants before the
    first part sit in a part with no heading; chants with no page at all
    get the UNPLACED heading.
    """
    sections = sorted(
        (e for e in chanting.CONTENTS
         if e.get('level') == 'section' and isinstance(e.get('page'), int)),
        key=lambda e: e['page'])
    parts = [{'heading': None, 'chants': []}]
    upcoming = list(sections)
    for chant in chanting.chants_in_book_order():
        page = chant.get('page_start')
        while upcoming and isinstance(page, int) and page >= upcoming[0]['page']:
            parts.append({'heading': upcoming.pop(0), 'chants': []})
        if not isinstance(page, int) and parts[-1]['heading'] is not UNPLACED:
            parts.append({'heading': UNPLACED, 'chants': []})
        parts[-1]['chants'].append(chant)
    return [p for p in parts if p['chants']]


def commentary(chant, key):
    """The paragraphs to print for one commentary section of one chant:
    the short version where there is one, otherwise the app's full text."""
    short = SHORT.get(chant['id'], {}).get(key)
    if short:
        return [short]
    return chant.get(key) or []


def render_html(template, parts, contents_pages, proof):
    return template.render(
        spelling_font_url='file:///' + SPELLING_FONT.replace('\\', '/'),
        book=chanting.BOOK,
        how=chanting.HOW_TO_USE,
        sections=chanting.CHANT_SECTIONS,
        commentary=commentary,
        parts=parts,
        contents_pages=contents_pages,
        locator=locator,
        proof=proof,
        built_on=datetime.date.today().isoformat(),
    )


def print_pdf(chrome, html, pdf_path, workdir):
    html_path = os.path.join(workdir, 'book.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    subprocess.run([
        chrome,
        '--headless=new',
        '--disable-gpu',
        f'--user-data-dir={os.path.join(workdir, "profile")}',
        '--no-pdf-header-footer',
        '--generate-pdf-document-outline',
        # Gives the Google Fonts time to arrive before the page is printed.
        '--virtual-time-budget=20000',
        f'--print-to-pdf={pdf_path}',
        'file:///' + html_path.replace('\\', '/'),
    ], check=True, timeout=600, capture_output=True)
    if not os.path.exists(pdf_path):
        sys.exit('Chrome ran but wrote no PDF.')


def find_pages(pdf_path, chant_ids):
    """Which PDF page (1-based) each chant's locator text sits on."""
    pages = {}
    with fitz.open(pdf_path) as doc:
        for number, page in enumerate(doc, start=1):
            text = page.get_text()
            for chant_id in chant_ids:
                if chant_id not in pages and locator(chant_id) in text:
                    pages[chant_id] = number
        total = doc.page_count
    return pages, total


# The commentary and English are set in 8.5pt, so that is the commonest text
# size in a correctly printed book. If anything on any page is wider than
# the page, Chrome shrinks EVERY page to fit and says nothing — an A5 volume
# once came out at 85% — and this is how that gets caught.
BODY_SIZE = 8.5


# Fonts Chrome falls back on when the chosen font lacks a letter. Finding one
# in the PDF means a letter is printed in a different typeface from the rest
# of its word — how ɛ ɔ ʉ ə first came out in the spelling layer. Roboto
# Mono is listed because it has no ɛ ɔ ʉ ǎ: finding it means the spelling
# font failed to load and Chrome fell back to the old one.
STAND_IN_FONTS = ('Arial', 'Times', 'Segoe', 'Calibri', 'Consolas', 'Courier',
                  'Lucida', 'Cambria', 'Leelawadee', 'RobotoMono')


def check_fonts_and_scale(pdf_path):
    sizes = collections.Counter()
    stand_ins = collections.Counter()
    with fitz.open(pdf_path) as doc:
        for page in doc:
            for block in page.get_text('dict')['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        sizes[round(span['size'], 1)] += len(span['text'])
                        if any(name in span['font'] for name in STAND_IN_FONTS):
                            line_text = ''.join(s['text'] for s in line['spans'])
                            stand_ins[(span['text'].strip(), span['font'],
                                       line_text[:50])] += 1
    if stand_ins:
        sample = '\n  '.join(f'{t!r} in {font}, in "{context}"'
                             for (t, font, context), _ in stand_ins.most_common(8))
        sys.exit(f'{os.path.basename(pdf_path)}: some letters were printed in a stand-in '
                 f'font, not the book\'s own:\n  {sample}')
    commonest = sizes.most_common(1)[0][0]
    if abs(commonest - BODY_SIZE) > 0.1:
        sys.exit(f'{os.path.basename(pdf_path)}: body text came out at {commonest}pt, '
                 f'not {BODY_SIZE}pt — Chrome has shrunk the pages to fit something '
                 'too wide. Find the overflowing line before printing.')


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--final', action='store_true',
                        help='leave off the "proof copy" stamp')
    parser.add_argument('--out', default=os.path.join(ROOT, '_print', 'chanting-book-a4.pdf'))
    args = parser.parse_args()

    unknown = sorted(set(SHORT) - {c['id'] for c in chanting.CHANTS})
    if unknown:
        sys.exit(f'chanting_print_short.py has entries for chants that do not exist: {unknown[:5]}')

    chrome = find_chrome()
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')),
                      autoescape=True)
    template = env.get_template('print/chanting_book_print.html')
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    proof = not args.final

    parts = book_parts()
    chant_ids = [c['id'] for p in parts for c in p['chants']]
    if sorted(chant_ids) != sorted(c['id'] for c in chanting.CHANTS):
        sys.exit('The book does not hold every chant exactly once.')

    with tempfile.TemporaryDirectory() as workdir:
        first = os.path.join(workdir, 'pass1.pdf')
        print('Pass 1: laying out the book...', flush=True)
        print_pdf(chrome, render_html(template, parts, {}, proof), first, workdir)
        pages, total1 = find_pages(first, chant_ids)
        check_fonts_and_scale(first)

        missing = [cid for cid in chant_ids if cid not in pages]
        if missing:
            sys.exit(f'{len(missing)} chants were not found in the PDF, e.g. {missing[:5]}')

        print('Pass 2: filling in the contents page numbers...', flush=True)
        numbers = {cid: str(n) for cid, n in pages.items()}
        print_pdf(chrome, render_html(template, parts, numbers, proof), args.out, workdir)
        check, total2 = find_pages(args.out, chant_ids)

    if check != pages or total1 != total2:
        sys.exit('The second pass paginated differently from the first — '
                 'the contents numbers cannot be trusted. Nothing was fixed up.')

    print(f'Done: {total2} A4 pages, {len(chant_ids)} chants -> {args.out}')
    long_left = sum(1 for cid in chant_ids
                    if not all(SHORT.get(cid, {}).get(s['key']) for s in chanting.CHANT_SECTIONS
                               if chanting.get_chant(cid).get(s['key'])))
    if long_left:
        print(f'  {long_left} chants still print their FULL commentary — '
              'no short version in chanting_print_short.py yet.')
    if total2 % 2:
        print('  Note: odd page count; most printers add a blank page at the end.')


if __name__ == '__main__':
    main()
