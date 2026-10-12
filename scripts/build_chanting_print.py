"""Build the Digital Chanting Book as print-ready A5 PDFs, in three volumes.

    python scripts/build_chanting_print.py              # all three volumes, proof copies
    python scripts/build_chanting_print.py --volume 2   # just one volume
    python scripts/build_chanting_print.py --final      # no "proof" stamp

Every chant in book order, with all five layers and the commentary, laid out
by templates/print/chanting_book_print.html and turned into a PDF by the copy
of Chrome already on this machine (headless, so no window opens). Nothing new
to install: Chrome shapes Thai properly, which ReportLab does not — its
stacked vowels and tone marks land in the wrong place.

In one volume the book runs to over 1,100 A5 pages — too thick to hold while
chanting and past what print-on-demand paperbacks allow. So it is printed as
THREE volumes, each opening where one of the book's own parts opens
(see VOLUMES).

The contents page needs to know which PDF page each chant lands on, and that
is only known once the PDF exists. So each volume is rendered TWICE: pass one
with placeholder numbers, then PyMuPDF finds each chant's invisible locator
text, then pass two with the real numbers. The page-number column is a fixed
width in the CSS, so both passes paginate identically — and the script
checks that rather than trusting it.

Reads only chanting.py. It never imports app, so it never touches the live
database.
"""
import argparse
import collections
import datetime
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

import fitz  # PyMuPDF
from jinja2 import Environment, FileSystemLoader

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import chanting  # noqa: E402

CHROME_PATHS = [
    r'C:\Program Files\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
]

# Where the book divides. Each volume opens where one of the book's own parts
# opens, so a split never falls in the middle of one: page 77 begins the
# chants appointed for the evening, page 191 is the divider that opens the
# services again with translation. Chants with no book page cannot be placed
# and go at the end of the last volume, under a heading that says so, rather
# than being guessed into a part.
VOLUMES = {
    1: {'number': 1, 'first_page': 1,
        'title': 'The morning and evening services, with the chants appointed for the morning',
        'pages': 'book pages 1–76'},
    2: {'number': 2, 'first_page': 77,
        'title': 'The suttas, protection chants and verses appointed for the evening',
        'pages': 'book pages 77–190'},
    3: {'number': 3, 'first_page': 191,
        'title': 'The services with translation, miscellaneous chants and appendix',
        'pages': 'book pages 191–325'},
}
LAST_VOLUME = max(VOLUMES)
UNPLACED = {'title': '', 'title_english': 'Chants not yet placed on a page of the book'}


def volume_of(chant):
    page = chant.get('page_start')
    if not isinstance(page, int):
        return LAST_VOLUME
    return max(n for n, v in VOLUMES.items() if page >= v['first_page'])


def in_volume(chant, number):
    return volume_of(chant) == number


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


def book_parts(volume):
    """One volume's chants in book order, grouped under the book's own part
    headings.

    The part headings are the `section` rows of CONTENTS (ทำวัตรเช้า and the
    like), each with the book page it starts on. A chant belongs to the last
    part that starts at or before its own first page. Chants before the
    first part sit in a part with no heading; chants with no page at all
    get the UNPLACED heading. Only the chants of `volume` are kept.
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
        if in_volume(chant, volume):
            parts[-1]['chants'].append(chant)
    return [p for p in parts if p['chants']]


def spelling_chars():
    """Every character set in ThaiBridge Spelling: the spelling layer, the
    chant titles given only in spelling (`title_roman`), and the sample line
    on the 'How each verse is set' page."""
    chars = set('kam bplae paa-sǎa tai')
    for chant in chanting.CHANTS:
        chars.update(chant.get('title_roman') or '')
        for part in [chant.get('invitation'), chant.get('closing'), *chant['verses']]:
            if part and part.get('paiboon'):
                chars.update(part['paiboon'])
    chars.discard('\n')
    return ''.join(sorted(chars))


# A modern browser's user agent, or Google Fonts answers with an old format.
FONT_USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/155.0 Safari/537.36')


def spelling_font_css():
    """An @font-face for the ThaiBridge Spelling, as its own family.

    The letters ɛ ɔ ʉ ə ŋ are not in the parts of Noto Serif that Google Fonts
    sends by default, so Chrome borrowed them from Times or Arial, mid-word,
    with the tone marks set badly. Asking for the font cut to exactly the
    characters the spelling uses (`text=`) gets every one from the full font.
    Google names that cut 'Noto Serif' too, and sharing a name with the main
    Noto Serif muddled which face Chrome used for the Pali — so it is renamed
    here to a family of its own.
    """
    url = ('https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@1,400'
           '&display=block&text=' + urllib.parse.quote(spelling_chars()))
    request = urllib.request.Request(url, headers={'User-Agent': FONT_USER_AGENT})
    try:
        css = urllib.request.urlopen(request, timeout=30).read().decode('utf-8')
    except OSError as error:
        sys.exit(f'Could not fetch the spelling font from Google Fonts: {error}')
    if "font-family: 'Noto Serif'" not in css:
        sys.exit('Google Fonts answered with something unexpected for the spelling font.')
    return css.replace("font-family: 'Noto Serif'", "font-family: 'ThaiBridge Spelling'")


def render_html(template, volume, parts, contents_pages, proof, font_css):
    return template.render(
        volume=VOLUMES[volume],
        spelling_font_css=font_css,
        book=chanting.BOOK,
        how=chanting.HOW_TO_USE,
        sections=chanting.CHANT_SECTIONS,
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
# size in a correctly printed volume. If anything on any page is wider than
# the page, Chrome shrinks EVERY page to fit and says nothing — volume 1 once
# came out at 85% — and this is how that gets caught.
BODY_SIZE = 8.5


# Fonts Chrome falls back on when the chosen font lacks a letter. Finding one
# in the PDF means a letter is printed in a different typeface from the rest
# of its word — how ɛ ɔ ʉ ə first came out in the spelling layer.
STAND_IN_FONTS = ('Arial', 'Times', 'Segoe', 'Calibri')


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
                            stand_ins[span['text'].strip()] += 1
    if stand_ins:
        sample = ', '.join(f'{t!r}' for t, _ in stand_ins.most_common(8))
        sys.exit(f'{os.path.basename(pdf_path)}: some letters were printed in a stand-in '
                 f'font, not the book\'s own: {sample}')
    commonest = sizes.most_common(1)[0][0]
    if abs(commonest - BODY_SIZE) > 0.1:
        sys.exit(f'{os.path.basename(pdf_path)}: body text came out at {commonest}pt, '
                 f'not {BODY_SIZE}pt — Chrome has shrunk the pages to fit something '
                 'too wide. Find the overflowing line before printing.')


def build_volume(chrome, template, volume, out, proof, font_css):
    parts = book_parts(volume)
    chant_ids = [c['id'] for p in parts for c in p['chants']]

    with tempfile.TemporaryDirectory() as workdir:
        first = os.path.join(workdir, 'pass1.pdf')
        print(f'Volume {volume}, pass 1: laying out the book...', flush=True)
        print_pdf(chrome, render_html(template, volume, parts, {}, proof, font_css), first, workdir)
        pages, total1 = find_pages(first, chant_ids)
        check_fonts_and_scale(first)

        missing = [cid for cid in chant_ids if cid not in pages]
        if missing:
            sys.exit(f'{len(missing)} chants were not found in the PDF, e.g. {missing[:5]}')

        print(f'Volume {volume}, pass 2: filling in the contents page numbers...', flush=True)
        numbers = {cid: str(n) for cid, n in pages.items()}
        print_pdf(chrome, render_html(template, volume, parts, numbers, proof, font_css), out, workdir)
        check, total2 = find_pages(out, chant_ids)

    if check != pages or total1 != total2:
        sys.exit('The second pass paginated differently from the first — '
                 'the contents numbers cannot be trusted. Nothing was fixed up.')

    print(f'Done: volume {volume}, {total2} A5 pages, {len(chant_ids)} chants -> {out}')
    if total2 % 2:
        print('  Note: odd page count; most printers add a blank page at the end.')
    return chant_ids


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--final', action='store_true',
                        help='leave off the "proof copy" stamp')
    parser.add_argument('--volume', type=int, choices=sorted(VOLUMES),
                        help='build just this volume (default: all)')
    parser.add_argument('--out-dir', default=os.path.join(ROOT, '_print'))
    args = parser.parse_args()

    chrome = find_chrome()
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')),
                      autoescape=True)
    template = env.get_template('print/chanting_book_print.html')
    os.makedirs(args.out_dir, exist_ok=True)
    font_css = spelling_font_css()

    built = []
    for volume in ([args.volume] if args.volume else sorted(VOLUMES)):
        out = os.path.join(args.out_dir, f'chanting-book-a5-vol{volume}.pdf')
        built += build_volume(chrome, template, volume, out, not args.final, font_css)

    # Every chant in exactly one volume — checked, because a chant dropped
    # between two books would be very easy never to notice on paper.
    if not args.volume and sorted(built) != sorted(c['id'] for c in chanting.CHANTS):
        sys.exit('The volumes do not hold every chant exactly once.')


if __name__ == '__main__':
    main()
