"""Build the Chanting Book Prompts reference PDFs.

Two sheets, one script: the one-chant-at-a-time workflow and the batch variant.
Each reads its two prompts straight out of its own prompt.md, so a sheet cannot
drift away from the prompt actually in use. Change the prompt, re-run this, and
the sheet is current again.

    python scripts/make_prompt_pdf.py                      # the one-chant sheet
    python scripts/make_prompt_pdf.py chanting-book-batch  # the batch sheet
    python scripts/make_prompt_pdf.py all                  # both

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

# Two sheets are built from this one script, because they are the same workflow
# at two scales and their print furniture should not drift apart. Everything
# below the "How to use this sheet" table — the one rule, the Paiboon+ table,
# the prompt blocks themselves — is shared. Only the framing differs.
VARIANTS = {
    'chanting-book-entry': {
        'folder': 'chanting-book-entry',
        'pdf': 'chanting-book-prompts.pdf',
        'title': 'Chanting Book Prompts',
        'subtitle': 'A two-stage workflow for turning a page of a physical Thai '
                    'chanting book into an entry in the Digital Chanting Book.',
        'howto': [
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
        ],
        'depth': None,
        'stage1_intro': 'Paste this once at the start of a session, then paste '
                        'chants one at a time. It returns one JSON object.',
        'stage2_intro': 'Paste this, then the JSON from Stage 1 underneath it.',
    },
    'chanting-book-batch': {
        'folder': 'chanting-book-batch',
        'pdf': 'chanting-book-batch-prompts.pdf',
        'title': 'Chanting Book Prompts — Batch',
        'subtitle': 'The same two-stage workflow rebuilt for volume: several '
                    'chants per message, across a 286-chant book.',
        'howto': [
            ('1. Open Claude.ai',
             'Paste <b>Stage 1</b> once at the start of a session. It sets the '
             'rules for the whole conversation.'),
            ('2. Choose a depth',
             'Put <b>FULL</b>, <b>COMPACT</b> or <b>DATA-ONLY</b> on the first '
             'line of your paste. See the table below. If you say nothing it '
             'uses COMPACT.'),
            ('3. Paste a batch',
             'Several chants at once, numbered. The reply lists every one it '
             'received <i>before</i> it writes any of them.'),
            ('4. Count the manifest',
             'Check the manifest against how many entries actually arrived. If '
             'they differ, the reply was cut off — re-paste from the id in '
             '<b>resume_from</b>. This is the check batching exists to need.'),
            ('5. Check against the book',
             'The closing sentence counts what needs verifying. Do that with the '
             'book open. This is the step nothing else can do for you.'),
            ('6. Open Claude Code',
             'Paste <b>Stage 2</b>, then the whole reply underneath it. It '
             'reconciles the manifest before it writes anything.'),
        ],
        'depth': [
            ('FULL', 'Everything the one-chant sheet produces. '
                     '<b>2–3 chants</b> per reply.'),
            ('COMPACT', 'background 1 paragraph, meaning 2. Everything else in '
                        'full. <b>4–6 chants</b> per reply.'),
            ('DATA-ONLY', 'Book content and structure only — no background, '
                          'meaning, summary, when_chanted, source or per-verse '
                          'english. <b>8–12 chants</b> per reply.'),
            ('Why it works', 'About 58% of a finished entry is commentary '
                             'written <i>about</i> the chant, and none of it '
                             'needs checking against the physical book. '
                             'DATA-ONLY defers that half and captures the half '
                             'that needs the book open.'),
        ],
        'stage1_intro': 'Paste this once at the start of a session, then paste '
                        'batches of chants. It returns one JSON object holding '
                        'a manifest, an array of entries, and a status.',
        'stage2_intro': 'Paste this, then the whole Stage 1 reply underneath it.',
    },
}

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


def build(variant='chanting-book-entry'):
    cfg = VARIANTS[variant]
    prompt_md = os.path.join(HERE, 'prompts', cfg['folder'], 'prompt.md')
    out_pdf = os.path.join(HERE, 'prompts', cfg['folder'], cfg['pdf'])

    register_fonts()
    st = styles()
    stage1, stage2 = extract_prompts(prompt_md)

    doc = BaseDocTemplate(out_pdf, pagesize=A4,
                          leftMargin=2 * cm, rightMargin=2 * cm,
                          topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                          title=cfg['title'],
                          author='Joshua Kay')
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height,
                  id='main')
    doc.addPageTemplates([PageTemplate(id='all', frames=[frame],
                                       onPage=footer)])

    s = []
    s.append(Paragraph(cfg['title'], st['title']))
    s.append(Paragraph(cfg['subtitle'], st['subtitle']))

    s.append(Paragraph('How to use this sheet', st['h2']))
    s.append(kv_table(cfg['howto'], st))

    if cfg['depth']:
        s.append(Paragraph('Choose a depth before you start', st['h2']))
        s.append(Paragraph(
            'A finished entry is about nine times the size of what you paste '
            'in, and Thai script, IAST and Paiboon+ all tokenise about twice '
            'as expensively as English. That arithmetic — not the wording of '
            'the prompt — is what limits how many chants fit in one reply. So '
            'the batch sheet lets you trade commentary for chants.', st['body']))
        s.append(kv_table(cfg['depth'], st))

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
    s.append(Paragraph(cfg['stage1_intro'], st['body']))
    s.append(prompt_box(stage1, st, doc.width))

    s.append(PageBreak())
    s.append(Paragraph('Stage 2 — paste into Claude Code', st['h2']))
    s.append(Paragraph(cfg['stage2_intro'], st['body']))
    s.append(prompt_box(stage2, st, doc.width))

    s.append(Spacer(1, 10))
    s.append(Paragraph('Before you say it is done', st['h3']))
    s.append(Paragraph(
        f'The canonical copy of both prompts is prompts/{cfg["folder"]}/prompt.md '
        'in the repo — copy from there, not from this sheet, which folds long lines '
        'to fit the page and prints ‼ where the prompt uses the warning emoji.', st['body']))
    if cfg['depth']:
        s.append(Paragraph(
            'Count the manifest against the entries that actually arrived. A '
            'reply cut off mid-array still parses as JSON, so nothing '
            'downstream will notice on your behalf — and nothing written at '
            'the end of a reply can report it, because in a truncated reply '
            'the end is exactly what is missing. That is why the manifest '
            'comes first.', st['body']))
    s.append(Paragraph(
        'Check the character counts Stage 2 reports, both ways: every Thai and '
        'Pali character from your paste should appear in the file, and none '
        'should appear that was not in your paste. That the page loads and the '
        'file imports proves neither.', st['body']))

    doc.build(s)
    return out_pdf


if __name__ == '__main__':
    targets = sys.argv[1:] or ['chanting-book-entry']
    if targets == ['all']:
        targets = list(VARIANTS)
    for name in targets:
        if name not in VARIANTS:
            sys.exit(f'Unknown sheet: {name}. Choose from: '
                     f'{", ".join(VARIANTS)} — or "all".')
        path = build(name)
        print(f'Wrote {path} ({os.path.getsize(path):,} bytes)')
