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
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

import fitz  # PyMuPDF
from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup, escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import chanting  # noqa: E402
from chanting_print_short import SHORT  # noqa: E402
from chanting_owen import OWEN_BOOK, OWEN_CHANTS  # noqa: E402

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


# ── Verse layout, after Ajarn Owen's chanting book (Josh, 2026-11-06) ──
# A verse line of Pali holds two half-lines (pādas). Where a line splits
# evenly by syllables at a word boundary, the book sets the two halves side
# by side, left and right, as a printed verse book does; prose lines stay
# full width. Counting is done on the romanised Pali, whose words match the
# Thai-script words one for one; a line where they do not is never split.
_SYLLABLE = re.compile('[aeiouāīū]')


def _even_split(syllables, tolerance=1):
    """The index splitting a run of words into two even halves, or None."""
    total = sum(syllables)
    best, running = None, 0
    for k in range(1, len(syllables)):
        running += syllables[k - 1]
        gap = abs(running - (total - running))
        if best is None or gap < best[0]:
            best = (gap, k)
    return best[1] if best and best[0] <= tolerance else None


def verse_rows(v, tolerance=3):
    """Where a Pali line splits into verse rows of two half-lines.

    Returns a list of (start, middle, end) word indexes, one per row, or None
    for prose. A single verse line (13-26 syllables: a śloka line is 16, a
    triṣṭubh 22) gives one row; an entry holding two verse lines (27-52
    syllables) gives two rows, each split in half again.
    """
    roman = (v.get('pali_roman') or '').split()
    thai = (v.get('pali') or '').split()
    if len(roman) < 2 or len(roman) != len(thai):
        return None
    syl = [len(_SYLLABLE.findall(w.lower())) for w in roman]
    total = sum(syl)
    if 13 <= total <= 26:
        # A metre's halves need not be equal (Ajarn Owen splits
        # "Sakko ujū ca suhujū ca | suvaco cassa mudu anatimānī" 9:12).
        k = _even_split(syl, tolerance=tolerance)
        return [(0, k, len(roman))] if k else None
    if 27 <= total <= 52 and len(roman) >= 4:
        m = _even_split(syl, tolerance=2)
        if not m:
            return None
        a, b = _even_split(syl[:m], tolerance=tolerance), _even_split(syl[m:], tolerance=tolerance)
        if a and b:
            return [(0, a, m), (m, m + b, len(roman))]
    return None


def verse_split(v):
    """True when the line is verse (kept for the chant-level test)."""
    return verse_rows(v) is not None


def halves(v):
    """Verse rows as (thai left, thai right, roman left, roman right), or None."""
    rows = verse_rows(v)
    if not rows:
        return None
    thai, roman = v['pali'].split(), v['pali_roman'].split()
    j = lambda ws: ' '.join(ws)
    return [(j(thai[a:m]), j(thai[m:e]), j(roman[a:m]), j(roman[m:e])) for a, m, e in rows]


# A line's length cannot tell verse from a prose sentence of the same length
# (the precepts, a formal request), so a chant that is only partly verse is
# set as verse only when its name says it is: a gāthā, a paritta, an
# abhigīti, the introductory verses (bot khat), or a known verse sutta.
_VERSE_NAME = re.compile(
    r'gatha|gāthā|paritt|bot-khat|abhigiti|karaniyametta|mangala-sutt|'
    r'ratanattaya|sambuddhe|namokara|jinabanjara|uddissana|sarabhanna|'
    r'unhissa|bhiyacana|chakkrawan-yai|sarathaphrot', re.I)


# Prose whose sentences happen to split evenly: formal requests, the
# disrobing formula, a request for forgiveness and the Abhidhamma Yamaka.
_PROSE_IDS = {
    'phra-yamaka', 'kham-la-sikkha', 'kham-aradhana-sin-8',
    'kham-kho-khama-thot-phra-therauthera', 'kham-aradhana-sin-5-prokati',
    'kham-aradhana-sin-8-prokati',
}


def is_verse_chant(chant):
    """Set full width with its verse lines in half-lines: mostly verse, or
    a named verse chant at least half of whose lines split as verse. Its
    other lines stay full lines."""
    lines = [v for v in chant.get('verses') or [] if v.get('pali_roman')]
    if not lines or chant['id'] in _PROSE_IDS:
        return False
    # The plain test uses the strict, even split that only verse passes;
    # the looser split (uneven halves) is trusted only in a named verse chant.
    strict = sum(1 for v in lines if verse_rows(v, tolerance=1)) / len(lines)
    loose = sum(1 for v in lines if verse_rows(v)) / len(lines)
    named = _VERSE_NAME.search(chant['id'] + ' ' + (chant.get('title_pali') or ''))
    return strict >= 0.7 or (loose >= 0.5 and bool(named))


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


def render_html(template, parts, contents_pages, proof, pad_blank=False):
    return template.render(
        pad_blank=pad_blank,
        spelling_font_url='file:///' + SPELLING_FONT.replace('\\', '/'),
        book=chanting.BOOK,
        how=chanting.HOW_TO_USE,
        sections=chanting.CHANT_SECTIONS,
        commentary=commentary,
        parts=parts,
        owen_chants=OWEN_CHANTS,
        owen_book=OWEN_BOOK,
        owen_part=sum(1 for p in parts if p.get('number')) + 1,
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
    env.filters['book_spelling'] = book_spelling
    env.filters['pali_words'] = pali_words
    env.filters['halves'] = halves
    env.filters['is_verse_chant'] = is_verse_chant
    template = env.get_template('print/chanting_book_print.html')
    os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
    proof = not args.final

    parts = number_parts(book_parts())
    chant_ids = [c['id'] for p in parts for c in p['chants']]
    if sorted(chant_ids) != sorted(c['id'] for c in chanting.CHANTS):
        sys.exit('The book does not hold every chant exactly once.')
    # Ajarn Owen's chants are paged too, for the contents, but they are a
    # separate Part from another book and are not chants of chanting.py.
    chant_ids += [c['id'] for c in OWEN_CHANTS]

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
        # Lulu prints only an even number of pages. An odd book gets one blank
        # page before the credit page, which keeps the credit on the last
        # page and moves no chant, so the contents numbers still hold.
        pad = bool(total1 % 2)
        print_pdf(chrome, render_html(template, parts, numbers, proof, pad), args.out, workdir)
        check, total2 = find_pages(args.out, chant_ids)

    if check != pages or total1 + pad != total2:
        sys.exit('The second pass paginated differently from the first — '
                 'the contents numbers cannot be trusted. Nothing was fixed up.')

    print(f'Done: {total2} A4 pages, {len(chant_ids)} chants -> {args.out}')
    long_left = sum(1 for cid in chant_ids if chanting.get_chant(cid)
                    if not all(SHORT.get(cid, {}).get(s['key']) for s in chanting.CHANT_SECTIONS
                               if chanting.get_chant(cid).get(s['key'])))
    if long_left:
        print(f'  {long_left} chants still print their FULL commentary — '
              'no short version in chanting_print_short.py yet.')
    if pad:
        print('  Added one blank page before the credit page to make the count even.')


if __name__ == '__main__':
    main()
