"""Build the Digital Chanting Book as one print-ready A4 PDF.

    python scripts/build_chanting_print.py            # proof copy
    python scripts/build_chanting_print.py --final    # no "proof" stamp
    python scripts/build_chanting_print.py --volumes  # the three-volume edition

THREE VOLUMES (2026-11-12): Pra Kru Bob asked for the book in three volumes
with an index of every chant. `--volumes` prints the same chants, in the
same order, as _print/chanting-volume-1/2/3.pdf, following the plan in
chanting_volumes.py — which Part goes in which volume is one number there,
so the abbot's decision is a one-line change. Both editions carry the
occasion guide, the day-of-the-week chants, the Amaravati reflections
(chanting_amaravati.py) and the indexes.

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
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import chanting  # noqa: E402
from chanting_print_short import SHORT  # noqa: E402
from chanting_owen import OWEN_BOOK, OWEN_CHANTS, OWEN_GLOSSARY  # noqa: E402
from chanting_amaravati import (  # noqa: E402
    AMARAVATI_BOOK, AMARAVATI_BOOK_FULL, AMARAVATI_CHANTS, AMARAVATI_LICENCE)
from chanting_volumes import (  # noqa: E402
    AMARAVATI_VOLUME, CHANT_VOLUME, DAILY_ORDER, DAY_CHANTS, OCCASIONS, OWEN_VOLUME,
    PART_VOLUME, SPLITS, VOLUMES)

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


# The printed book writes a final ย as i (dûai, nɔ́ɔi, ləəi), where the app
# writes y (dûay, nɔ́ɔy, ləəy). Josh's choice for the book, 2026-11-06; its
# pronunciation guide explains both. Done here, at print time, so the data
# and the app keep one spelling. ai/aai never had a y, and a word with no
# tone mark or ɛ ɔ ə ʉ ŋ (English, Pali IAST) is never touched.
_TONES = '̀́̂̌'
_WORD = re.compile('[a-zA-ZɛɔəʉŋÀ-ɏḀ-ỿ̀-ͯ]+')
_FINAL_Y = re.compile('(u[%s]?a|ʉ[%s]?a|o[%s]?o?|ɔ[%s]?ɔ?|ə[%s]?ə?|u[%s]?)y$' % ((_TONES,) * 6))
_THAIISH = re.compile('[%sɛɔəʉŋ]' % _TONES)
_PLAIN_FINAL_Y = {'dooy', 'kuy', 'rooy', 'ooy'}


def book_spelling(text):
    """ThaiBridge Spelling as the printed book shows it: final ย as i."""
    if not text:
        return text

    def swap(m):
        word = unicodedata.normalize('NFD', m.group(0))
        if _FINAL_Y.search(word) and (_THAIISH.search(word) or word.lower() in _PLAIN_FINAL_Y):
            return m.group(0)[:-1] + 'i'
        return m.group(0)
    return _WORD.sub(swap, text)


# Verse layout: which lines are verse and where they split. Shared with the
# app's chant pages, so it lives in chanting_layout.py.
from chanting_layout import halves, is_verse_chant, verse_rows, verse_split  # noqa: E402,F401


# Thai script has no spaces inside a word, so the browser will break a Pali
# word anywhere, and did, mid-word and with no sign of it. Ordinary words are
# now kept whole. A word too long for a column may break only after a
# syllable ending in ะ or า, and shows a dash there (a soft hyphen).
_LONG_WORD = 30
_SYLLABLE_END = re.compile('([ะา])(?=[ก-ฮเแโใไ])')


def pali_words(text):
    if not text:
        return text
    out = []
    for word in text.split(' '):
        if len(word) <= _LONG_WORD:
            out.append('<span class="nw">%s</span>' % escape(word))
        else:
            out.append(_SYLLABLE_END.sub(lambda m: m.group(1) + '­', str(escape(word))))
    return Markup(' '.join(out))


# ── Contents, organised like Ajarn Owen's and Ajarn Sujan's books ──
# (Josh, 2026-11-06.) The parts stay in the temple book's order, so monks
# chanting from its Thai text can follow; they are numbered and given short,
# plain English names, keyed by the book's own Thai heading.
PART_NAMES = {
    'ทำวัตรเช้า': 'Morning Chanting',
    'เสขิยวัตร': 'The 75 Training Rules (Sekhiya)',
    'พระสูตร ปาฐะ และคาถาที่กำหนดสวดในภาคเช้า': 'Morning Suttas and Verses',
    'สวดแจง': 'Suat Jaeng: the Canon in Summary',
    'พระอภิธรรมสังเขป': 'The Abhidhamma in Summary',
    'ทำวัตรเย็น': 'Evening Chanting',
    'พระสูตร พระปริตร ปาฐะ และคาถาที่กำหนดสวดในภาคเย็น': 'Evening Suttas and Protection Chants',
    'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันโกน วันพระ เวลาเย็น': 'The Observance Day and its Eve (Evening)',
    'พระสูตร พระปริตร พระปาฐะที่กำหนดสวดในวันขึ้นหรือแรม ๘ ค่ำ เวลาเย็น': 'The Eighth Day of the Moon (Evening)',
    'พระสูตรที่กำหนดสวดในวันขึ้น ๑๔ ค่ำ เวลาเย็น': 'The 14th Day of the Waxing Moon (Evening)',
    'พระสูตรที่กำหนดสวดในวันแรม ๗ ค่ำ เวลาเย็น': 'The 7th Day of the Waning Moon (Evening)',
    'พระสูตรที่กำหนดสวดในวันแรม ๑๓ ค่ำหรือ ๑๔ ค่ำ เวลาเย็น': 'The 13th or 14th Day of the Waning Moon (Evening)',
    'บทสวดมนต์ ทำวัตรเช้า-เย็น แปล': 'Morning and Evening Chanting, with Thai Translation',
    'ภาคปกิณกะ': 'Miscellaneous Chants and Formal Requests',
    'ภาคผนวก': 'Appendix: Ceremonies and Procedures',
    '': 'Other Chants',            # chants with no page in the temple book
}


def number_parts(parts):
    """Give each headed part its number and short name, in book order."""
    n = 0
    for part in parts:
        h = part['heading']
        if not h:
            continue
        n += 1
        part['number'] = n
        part['name'] = PART_NAMES.get(h.get('title'), h.get('title_english'))
    return parts


# ── One book or three volumes (Pra Kru Bob's request, 2026-11-12) ──
# The same chants, the same order, the same template. A "book" below is
# either the whole one-volume edition or one of the three volumes; the plan
# for which Part goes in which volume is chanting_volumes.py.

# Locators for the guide sections, so the contents can give their pages.
GUIDE_IDS = ('guide-occasions', 'guide-days', 'index-chants', 'index-first-lines')


def split_into_volumes(parts):
    """Each numbered part cut into runs by volume, in book order.

    Returns {volume number: [part, ...]}, where a part that is split keeps
    its number and name and is marked `continued` in every volume after the
    one it starts in."""
    out = {v['number']: [] for v in VOLUMES}
    for part in parts:
        volume = PART_VOLUME[part.get('number') or 16]
        pieces = []
        for chant in part['chants']:
            volume = SPLITS.get(chant['id'], volume)
            home = CHANT_VOLUME.get(chant['id'], volume)
            if not pieces or pieces[-1]['volume'] != home:
                pieces.append({'volume': home, 'chants': []})
            pieces[-1]['chants'].append(chant)
        for i, piece in enumerate(pieces):
            out[piece['volume']].append(dict(part, chants=piece['chants'], continued=i > 0))
    return out


def _sort_key(text):
    """Alphabetical order that ignores accents, 'The' and quote marks."""
    text = unicodedata.normalize('NFD', text or '')
    text = ''.join(ch for ch in text if not unicodedata.combining(ch))
    text = re.sub(r'^[\W_]+', '', text).lower()
    return re.sub(r'^(the|a|an) ', '', text)


def _first_line(text, limit=60):
    text = re.sub(r'\s+', ' ', (text or '').split('\n')[0]).strip().rstrip(',.;:')
    return text if len(text) <= limit else text[:limit].rsplit(' ', 1)[0] + ' …'


def index_entries(books):
    """Every chant of the edition, for the index of chants: label, the
    romanised title under it, and the book it is in."""
    entries = []
    for book in books:
        for part in book['parts']:
            for c in part['chants']:
                roman = c.get('title_pali') or c.get('title_roman') or ''
                label = c.get('title_english') or roman or c.get('title_thai')
                entries.append({'id': c['id'], 'label': label,
                                'roman': roman if roman != label else '',
                                'thai': c.get('title_thai', '')})
        for c in book['owen_chants'] + book['amaravati_chants']:
            entries.append({'id': c['id'], 'label': c['title_english'],
                            'roman': c['title'], 'thai': c.get('title_thai', '')})
    return sorted(entries, key=lambda e: _sort_key(e['label']))


def first_line_entries(book):
    """This book's chants by the first line of their Pali, as the Amaravati
    book indexes them. A chant with no romanised Pali (an order of service in
    Thai) has no first line to index."""
    lines = []
    for part in book['parts']:
        for c in part['chants']:
            first = next((v.get('pali_roman') for v in c['verses'] if v.get('pali_roman')), '')
            if first:
                lines.append({'id': c['id'], 'line': _first_line(first)})
    for c in book['owen_chants']:
        first = next((ln.get('pali_roman') for s in c['sections'] for ln in s['lines']
                      if ln.get('pali_roman')), '')
        if first:
            lines.append({'id': c['id'], 'line': _first_line(first)})
    for c in book['amaravati_chants']:
        lines.append({'id': c['id'], 'line': _first_line(c['first_line'])})
    return sorted(lines, key=lambda e: _sort_key(e['line']))


def make_books(volumes):
    """The books to print: one, or the three volumes."""
    parts = number_parts(book_parts())
    owen_part = sum(1 for p in parts if p.get('number')) + 1
    common = {'owen_part': owen_part, 'amaravati_part': owen_part + 1}
    if not volumes:
        return [dict(common, key='one', volume=None, parts=parts, full_front=True, day_guide=True,
                     owen_chants=OWEN_CHANTS, amaravati_chants=AMARAVATI_CHANTS,
                     out=os.path.join(ROOT, '_print', 'chanting-book-a4.pdf'))]
    by_volume = split_into_volumes(parts)
    books = []
    for v in VOLUMES:
        n = v['number']
        books.append(dict(
            common, key=f'volume-{n}', volume=v, parts=by_volume[n],
            full_front=(n == 1), day_guide=(n == 1),
            owen_chants=OWEN_CHANTS if OWEN_VOLUME == n else [],
            amaravati_chants=AMARAVATI_CHANTS if AMARAVATI_VOLUME == n else [],
            out=os.path.join(ROOT, '_print', f'chanting-volume-{n}.pdf')))
    return books


def book_ids(book):
    """Everything in one book that the contents or an index gives a page for."""
    ids = [c['id'] for p in book['parts'] for c in p['chants']]
    ids += [c['id'] for c in book['owen_chants']]
    if book['owen_chants']:
        ids.append(OWEN_GLOSSARY['id'])
    ids += [c['id'] for c in book['amaravati_chants']]
    ids += [g for g in GUIDE_IDS if g != 'guide-days' or book['day_guide']]
    return ids


def render_html(template, book, books, pages, proof, pad_blank=False):
    """`pages` maps (book key, id) -> PDF page; empty on the first pass,
    when every number prints as a same-width placeholder."""
    home = {i: b for b in books for i in book_ids(b)}
    many = len(books) > 1

    def page(item_id):
        """The page of something in THIS book (contents, its own index)."""
        return str(pages.get((book['key'], item_id), '000'))

    def ref(item_id):
        """Where to find a chant anywhere in the edition: 'p. 123', or
        'Vol. 2, p. 123' when the edition is in volumes."""
        b = home.get(item_id)
        if b is None:
            return '—'
        n = pages.get((b['key'], item_id), '000')
        return f"Vol. {b['volume']['number']}, p. {n}" if many else f'p. {n}'

    chants_by_id = {c['id']: c for c in chanting.CHANTS}
    chants_by_id.update({c['id']: dict(c, title_pali=c['title']) for c in OWEN_CHANTS + AMARAVATI_CHANTS})
    return template.render(
        pad_blank=pad_blank,
        spelling_font_url='file:///' + SPELLING_FONT.replace('\\', '/'),
        book=chanting.BOOK,
        how=chanting.HOW_TO_USE,
        sections=chanting.CHANT_SECTIONS,
        commentary=commentary,
        parts=book['parts'],
        volume=book['volume'],
        volumes=VOLUMES if many else [],
        full_front=book['full_front'],
        day_guide=book['day_guide'],
        owen_chants=book['owen_chants'],
        owen_book=OWEN_BOOK,
        glossary=OWEN_GLOSSARY,
        owen_part=book['owen_part'],
        amaravati_chants=book['amaravati_chants'],
        amaravati_book=AMARAVATI_BOOK,
        amaravati_book_full=AMARAVATI_BOOK_FULL,
        amaravati_licence=AMARAVATI_LICENCE,
        amaravati_part=book['amaravati_part'],
        occasions=OCCASIONS,
        day_chants=DAY_CHANTS,
        daily_order=DAILY_ORDER,
        chant_by_id=chants_by_id,
        index_chants=index_entries(books),
        index_first_lines=first_line_entries(book),
        page=page,
        ref=ref,
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
    import fitz  # PyMuPDF: imported here so the tests can load this script without it
    pages = {}
    with fitz.open(pdf_path) as doc:
        for number, page in enumerate(doc, start=1):
            text = page.get_text()
            for chant_id in chant_ids:
                if chant_id not in pages and locator(chant_id) in text:
                    pages[chant_id] = number
        total = doc.page_count
    return pages, total


# The commentary and English are set in 10pt, so that is the commonest text
# size in a correctly printed book. If anything on any page is wider than
# the page, Chrome shrinks EVERY page to fit and says nothing — an A5 volume
# once came out at 85% — and this is how that gets caught.
BODY_SIZE = 10   # raised from 8.5 after the teacher's review (text too small)


# Fonts Chrome falls back on when the chosen font lacks a letter. Finding one
# in the PDF means a letter is printed in a different typeface from the rest
# of its word — how ɛ ɔ ʉ ə first came out in the spelling layer. Roboto
# Mono is listed because it has no ɛ ɔ ʉ ǎ: finding it means the spelling
# font failed to load and Chrome fell back to the old one.
STAND_IN_FONTS = ('Arial', 'Times', 'Segoe', 'Calibri', 'Consolas', 'Courier',
                  'Lucida', 'Cambria', 'Leelawadee', 'RobotoMono')


def check_fonts_and_scale(pdf_path):
    import fitz  # PyMuPDF
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
    parser.add_argument('--volumes', action='store_true',
                        help='print the three-volume edition (chanting_volumes.py) '
                             'instead of the one-volume book')
    args = parser.parse_args()

    unknown = sorted(set(SHORT) - {c['id'] for c in chanting.CHANTS})
    if unknown:
        sys.exit(f'chanting_print_short.py has entries for chants that do not exist: {unknown[:5]}')

    chrome = find_chrome()
    env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'templates')),
                      autoescape=True)
    env.filters['book_spelling'] = book_spelling
    env.filters['pali_words'] = pali_words
    env.filters['halves'] = halves
    env.filters['is_verse_chant'] = is_verse_chant
    template = env.get_template('print/chanting_book_print.html')
    os.makedirs(os.path.join(ROOT, '_print'), exist_ok=True)
    proof = not args.final

    books = make_books(args.volumes)
    temple_ids = [c['id'] for b in books for p in b['parts'] for c in p['chants']]
    if sorted(temple_ids) != sorted(c['id'] for c in chanting.CHANTS):
        sys.exit('The edition does not hold every chant exactly once.')
    if sum(bool(b['owen_chants']) for b in books) != 1 or \
            sum(bool(b['amaravati_chants']) for b in books) != 1:
        sys.exit("Ajarn Owen's and the Amaravati chants must each be in exactly one book.")

    # Every book is laid out once with placeholder numbers; only then are all
    # pages known, because the occasion guide and the index in one volume
    # give pages in the others. Then every book is laid out again with the
    # real numbers, and must come out paginated exactly as before.
    with tempfile.TemporaryDirectory() as workdir:
        pages, totals = {}, {}
        print('Pass 1: laying out...', flush=True)
        for book in books:
            first = os.path.join(workdir, f"{book['key']}-pass1.pdf")
            print_pdf(chrome, render_html(template, book, books, {}, proof), first, workdir)
            found, totals[book['key']] = find_pages(first, book_ids(book))
            check_fonts_and_scale(first)
            missing = [i for i in book_ids(book) if i not in found]
            if missing:
                sys.exit(f"{book['key']}: {len(missing)} chants were not found in the PDF, "
                         f'e.g. {missing[:5]}')
            pages.update({(book['key'], i): n for i, n in found.items()})

        print('Pass 2: filling in the page numbers...', flush=True)
        for book in books:
            # Lulu prints only an even number of pages. An odd book gets one
            # blank page before the credit page, which keeps the credit on
            # the last page and moves no chant, so the numbers still hold.
            pad = bool(totals[book['key']] % 2)
            print_pdf(chrome, render_html(template, book, books, pages, proof, pad),
                      book['out'], workdir)
            check, total2 = find_pages(book['out'], book_ids(book))
            if any(check.get(i) != pages[(book['key'], i)] for i in book_ids(book)) \
                    or totals[book['key']] + pad != total2:
                sys.exit(f"{book['key']}: the second pass paginated differently from the "
                         'first — the page numbers cannot be trusted. Nothing was fixed up.')
            name = f"Volume {book['volume']['number']}" if book['volume'] else 'The book'
            print(f"Done: {name}: {total2} A4 pages -> {book['out']}"
                  + (' (one blank page added to make the count even)' if pad else ''))

    long_left = sum(1 for cid in temple_ids
                    if not all(SHORT.get(cid, {}).get(s['key']) for s in chanting.CHANT_SECTIONS
                               if chanting.get_chant(cid).get(s['key'])))
    if long_left:
        print(f'  {long_left} chants still print their FULL commentary — '
              'no short version in chanting_print_short.py yet.')


if __name__ == '__main__':
    main()
