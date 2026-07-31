"""Build the Chanting Book Prompts reference PDF.

The two prompts are read straight out of prompts/chanting-book-entry/prompt.md,
so the PDF cannot drift away from the prompts that are actually in use. Change
the prompt, re-run this, and the sheet is current again.

Font note: Tahoma is the only font on a stock Windows machine that covers all
three character sets this project needs at once — Thai script, IAST diacritics
(ā ṃ ṅ ñ ṭ ḍ ṇ ḷ) and the Paiboon+ vowels (ɛ ɔ ə ʉ ŋ). Arial has no Thai;
Leelawadee, Cordia and Angsana have Thai but no IAST or IPA. Do not swap the
font without checking coverage first, or the Pali quietly turns into boxes.

    python scripts/make_prompt_pdf.py
"""

import os
import re
import sys

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Frame, PageBreak, PageTemplate,
                                Paragraph, Spacer, Table, TableStyle,
                                XPreformatted)

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_MD = os.path.join(HERE, 'prompts', 'chanting-book-entry', 'prompt.md')
OUT_PDF = os.path.join(HERE, 'prompts', 'chanting-book-entry',
                       'chanting-book-prompts.pdf')

PURPLE = HexColor('#4A1E5C')
GOLD = HexColor('#B8860B')
INK = HexColor('#222222')
GREY = HexColor('#555555')
BOXBG = HexColor('#FBF7EF')
BOXEDGE = HexColor('#E3D9C2')


def register_fonts():
    """Register Tahoma, the one stock Windows font covering Thai + IAST + IPA."""
    wf = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts')
    faces = [('Body', 'tahoma.ttf'), ('Body-B', 'tahomabd.ttf')]
    for alias, filename in faces:
        path = os.path.join(wf, filename)
        if not os.path.exists(path):
            sys.exit(f'Missing font: {path}. See the font note in this file.')
        pdfmetrics.registerFont(TTFont(alias, path))


def styles():
    return {
        'title': ParagraphStyle('title', fontName='Body-B', fontSize=22,
                                leading=27, textColor=PURPLE, spaceAfter=4),
        'subtitle': ParagraphStyle('subtitle', fontName='Body', fontSize=11,
                                   leading=15, textColor=GREY, spaceAfter=16),
        'h2': ParagraphStyle('h2', fontName='Body-B', fontSize=14, leading=18,
                             textColor=PURPLE, spaceBefore=16, spaceAfter=6),
        'h3': ParagraphStyle('h3', fontName='Body-B', fontSize=11, leading=15,
                             textColor=GOLD, spaceBefore=10, spaceAfter=4),
        'body': ParagraphStyle('body', fontName='Body', fontSize=9.5,
                               leading=14, textColor=INK, alignment=TA_LEFT,
                               spaceAfter=6),
        # The prompt blocks. Small and tight so a whole prompt stays readable
        # without running to a dozen pages. XPreformatted keeps every line
        # break exactly as written; the shading comes from the style rather
        # than a wrapping table, because a table cell cannot split across
        # pages and these blocks are far taller than one page.
        'pre': ParagraphStyle('pre', fontName='Body', fontSize=8.5, leading=11.4,
                              textColor=INK, backColor=BOXBG,
                              borderColor=BOXEDGE, borderWidth=0.8,
                              borderPadding=7, spaceBefore=4, spaceAfter=4),
        'cell': ParagraphStyle('cell', fontName='Body', fontSize=9,
                               leading=12.5, textColor=INK),
        'cellb': ParagraphStyle('cellb', fontName='Body-B', fontSize=9,
                                leading=12.5, textColor=PURPLE),
    }


def extract_prompts(md_path):
    """Pull the two fenced blocks out of prompt.md: stage 1, then stage 2."""
    md = open(md_path, encoding='utf-8').read()
    blocks = re.findall(r'```\n(.*?)\n```', md, re.DOTALL)
    if len(blocks) != 2:
        sys.exit(f'Expected 2 fenced blocks in {md_path}, found {len(blocks)}. '
                 'The PDF builder needs exactly stage 1 then stage 2.')
    return blocks[0], blocks[1]


# Tahoma carries no emoji at all — not the warning sign, not the variation
# selector — so ⚠️ would print as two empty boxes. Swapped for a glyph Tahoma
# does have. The prompts themselves keep the emoji; this is print-only.
GLYPH_SWAPS = {'⚠️': '‼', '⚠': '‼'}


def escaped(text):
    """XPreformatted parses markup, so the prompt's own <angle brackets> and
    ampersands have to be escaped or they vanish from the page."""
    for src, dst in GLYPH_SWAPS.items():
        text = text.replace(src, dst)
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;'))


def soft_wrap(text, max_pt, font, size):
    """Fold over-long lines so nothing runs off the page.

    XPreformatted does not wrap — a long line simply overflows the frame. A
    few lines of the JSON schema run past 160 characters, so they are folded
    here at a word boundary and the continuation is indented to keep the
    structure readable. The unfolded original always lives in prompt.md; this
    is a printed reference, not the canonical copy.
    """
    out = []
    for line in text.split('\n'):
        if pdfmetrics.stringWidth(line, font, size) <= max_pt:
            out.append(line)
            continue
        indent = ' ' * (len(line) - len(line.lstrip()) + 4)
        current = ''
        for word in line.split(' '):
            trial = word if not current else current + ' ' + word
            if pdfmetrics.stringWidth(trial, font, size) > max_pt and current:
                out.append(current)
                current = indent + word
            else:
                current = trial
        if current:
            out.append(current)
    return '\n'.join(out)


def prompt_box(text, st, frame_width):
    """A prompt as a shaded block that can split across pages.

    Deliberately NOT wrapped in a Table: a single table cell cannot split, and
    each prompt is several pages tall. The shading and border come from the
    paragraph style instead, so every page of the block keeps them.
    """
    pre = st['pre']
    usable = frame_width - 2 * pre.borderPadding - 4
    return XPreformatted(escaped(soft_wrap(text, usable, pre.fontName,
                                           pre.fontSize)), pre)


def kv_table(rows, st, widths=(4.6 * cm, 11.6 * cm)):
    data = [[Paragraph(k, st['cellb']), Paragraph(v, st['cell'])] for k, v in rows]
    tbl = Table(data, colWidths=list(widths))
    tbl.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, -2), 0.4, BOXEDGE),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return tbl


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Body', 7.5)
    canvas.setFillColor(GREY)
    canvas.drawString(2 * cm, 1.2 * cm, 'ThaiBridge AI — Digital Chanting Book')
    canvas.drawRightString(19 * cm, 1.2 * cm, f'Page {doc.page}')
    canvas.restoreState()


def build():
    register_fonts()
    st = styles()
    stage1, stage2 = extract_prompts(PROMPT_MD)

    doc = BaseDocTemplate(OUT_PDF, pagesize=A4,
                          leftMargin=2 * cm, rightMargin=2 * cm,
                          topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                          title='Chanting Book Prompts',
                          author='Joshua Kay')
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id='main')
    doc.addPageTemplates([PageTemplate(id='all', frames=[frame],
                                       onPage=footer)])

    s = []
    s.append(Paragraph('Chanting Book Prompts', st['title']))
    s.append(Paragraph(
        'A two-stage workflow for turning a page of a physical Thai chanting '
        'book into an entry in the Digital Chanting Book.', st['subtitle']))

    s.append(Paragraph('How to use this sheet', st['h2']))
    s.append(kv_table([
        ('1. Open Claude.ai',
         'Paste <b>Stage 1</b> once at the start of a session. It sets the '
         'rules for the whole conversation.'),
        ('2. Paste your chant',
         'Copy the Thai from the chanting book — the Pali in Thai script and '
         'its Thai translation — and paste it in. One chant at a time.'),
        ('3. Read the working notes',
         'The reply opens by saying what it split, what it grouped, and what '
         'it could not resolve. Read this before the JSON.'),
        ('4. Check against the book',
         'The reply ends by counting what needs verifying. Do that with the '
         'book open. This is the step nothing else can do for you.'),
        ('5. Open Claude Code',
         'Paste <b>Stage 2</b>, then the JSON underneath it. It writes the '
         'chant into chanting.py and verifies it renders.'),
    ], st))

    s.append(Paragraph('The one rule that matters most', st['h2']))
    s.append(Paragraph(
        'Neither stage may ever reconstruct Pali or Thai from memory. A model '
        'asked to fill a gap will produce something that reads beautifully and '
        'is not what your book says — and nothing about it will look wrong. '
        'Both prompts are built to raise a flag instead of filling a gap. '
        'Every flag it raises is a line for you to check against the physical '
        'book.', st['body']))

    s.append(Paragraph('Paiboon+ quick reference', st['h2']))
    s.append(Paragraph(
        'This app uses Paiboon+, not RTGS. The difference that goes wrong most '
        'often is aspiration: in Paiboon+ a bare <b>k</b> already means the '
        'aspirated sound, because <b>g</b> is reserved for the unaspirated ก. '
        'Never write kh, th or ph. Never write ng — ง is always ŋ.', st['body']))
    s.append(kv_table([
        ('Consonants',
         'ก = g &nbsp; ข ค ฆ = k &nbsp; ง = ŋ &nbsp; จ = j &nbsp; ฉ ช ฌ = ch<br/>'
         'ด = d &nbsp; ต = dt &nbsp; ถ ท ธ = t &nbsp; บ = b &nbsp; ป = bp<br/>'
         'ผ พ ภ = p &nbsp; ฝ ฟ = f &nbsp; ซ ศ ษ ส = s &nbsp; ห = h &nbsp; ร = r &nbsp; ล = l'),
        ('Vowels', 'ɛ (แ) &nbsp; ɔ (อ) &nbsp; ə (เออ) &nbsp; ʉ (อึ)'),
        ('Tones', 'mid unmarked &nbsp; low à &nbsp; falling â &nbsp; high á &nbsp; rising ǎ'),
        ('Watch for',
         'พระ → prá <i>not</i> phrá &nbsp;•&nbsp; ทั้ง → táŋ <i>not</i> thâng<br/>'
         'ขันธ์ → kǎn <i>not</i> khǎn &nbsp;•&nbsp; ของ → kɔ̌ɔŋ <i>not</i> khǎaw'),
    ], st))

    s.append(PageBreak())
    s.append(Paragraph('Stage 1 — paste into Claude.ai', st['h2']))
    s.append(Paragraph(
        'Paste this once at the start of a session, then paste chants one at a '
        'time. It returns one JSON object.', st['body']))
    s.append(prompt_box(stage1, st, doc.width))

    s.append(PageBreak())
    s.append(Paragraph('Stage 2 — paste into Claude Code', st['h2']))
    s.append(Paragraph(
        'Paste this, then the JSON from Stage 1 underneath it.', st['body']))
    s.append(prompt_box(stage2, st, doc.width))

    s.append(Spacer(1, 10))
    s.append(Paragraph('Before you say it is done', st['h3']))
    s.append(Paragraph(
        'The canonical copy of both prompts is prompts/chanting-book-entry/prompt.md '
        'in the repo — copy from there, not from this sheet, which folds long lines '
        'to fit the page and prints ‼ where the prompt uses the warning emoji.', st['body']))
    s.append(Paragraph(
        'Check the character counts Stage 2 reports, both ways: every Thai and '
        'Pali character from your paste should appear in the file, and none '
        'should appear that was not in your paste. That the page loads and the '
        'file imports proves neither.', st['body']))

    doc.build(s)
    return OUT_PDF


if __name__ == '__main__':
    path = build()
    print(f'Wrote {path} ({os.path.getsize(path):,} bytes)')
