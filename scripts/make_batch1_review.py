"""Build the Thai teacher's Batch 1 review spreadsheet (core learning pages).

Batch 1 is every Thai line a learner meets outside Monk Mode, the chanting
book, the Dhamma talks and the Tour Guide trips: Survival, the Learn
categories, Lessons, Sentences, Grammar, registers, tones, vowels, the
alphabet, Reading & Writing, the spelling guide, Culture, Theravada and
Meditation. It is read from the live data, so she checks exactly what
learners see, not a copy that may have drifted.

Each Thai line appears ONCE, on the first page that uses it, even when several
pages share it. Notes and tips that mix English with Thai words get a row of
their own so the Thai inside them is checked too.

Left out on purpose:
  * the female form of a line, where it differs only in ค่ะ/คะ or ดิฉัน. The
    intro sheet asks about that once instead of doubling the sheet;
  * single tiles of the Build-the-Sentence drill: the whole sentence is listed.

    python scripts/make_batch1_review.py
    python scripts/make_batch1_review.py --out docs/batch1-thai-review-2026-10-13.xlsx

Writes an .xlsx: one "read me" sheet in Thai and English, and one review sheet
with a drop-down to mark each line and a column for the correction.
"""

import argparse
import glob
import html
import os
import re
import sys

# Importing app connects to the database at startup. Empty, not popped — the
# same reason as tests/conftest.py: dotenv would load the LIVE url back in.
os.environ["DATABASE_URL"] = ""

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from openpyxl import Workbook  # noqa: E402
from openpyxl.styles import Alignment, Font, PatternFill  # noqa: E402
from openpyxl.worksheet.datavalidation import DataValidation  # noqa: E402

import app  # noqa: E402
import register_levels  # noqa: E402
import sentence_builder  # noqa: E402
import survival  # noqa: E402
import thai_consonants  # noqa: E402
import thai_reading  # noqa: E402
import thai_registers  # noqa: E402

THAI = re.compile(r"[฀-๿]")
LATIN = re.compile(r"[A-Za-z]")
# A quoted string in a script line: the only part of it a learner sees.
QUOTED = re.compile(r"""'([^']*)'|"([^"]*)\"""")
CODE_HINT = re.compile(r"(\+ *['\"]|['\"] *\+|\? *['\"]|=>|appendChild|;\s*$)")

# The field that holds a line's Thai, its spelling, and its meaning. The data
# grew page by page, so each comes under a few names.
THAI_KEYS = ("thai", "thai_title", "title_th", "name_thai", "thai_name", "thai_term")
SPELLING_KEYS = ("paiboon", "paiboon_title", "title_paiboon")
MEANING_KEYS = ("english", "meaning", "title_en", "name_en", "translation", "name", "title", "label")

# Page by page, in the order a learner meets them: (page name, address, data).
PAGES = [
    ("Survival Thai", "/survival", survival.SETS),
    ("Learn: vocabulary", "/exercise/<category>", app.VOCABULARY),
    ("Lessons", "/lessons", app.LESSONS),
    ("Sentences", "/sentences", app.SENTENCE_PATTERNS),
    ("Sentences: conversations", "/sentences", app.CONVERSATIONS),
    ("Sentences: conversational phrases", "/sentences", app.CONVERSATIONAL_PHRASES),
    ("Grammar", "/grammar", app.GRAMMAR),
    ("Formality", "/formality", app.FORMALITY_LEVELS),
    ("Male & female speech", "/gender-examples", app.GENDER_VARIANTS),
    ("Registers guide", "/register", register_levels.REGISTER_LEVELS),
    ("Register switcher (shown on several pages)", "/survival, /sentences", thai_registers.LEVELS),
    ("Tones & consonant classes", "/tones-classes", app.TONES_AND_CLASSES),
    ("Vowels & syllables", "/vowels_syllables", app.THAI_VOWELS_32),
    ("Reading & writing: vowel positions", "/read_write", thai_reading.VOWEL_POSITIONS),
    ("Reading & writing: Dhamma words", "/read_write", thai_reading.DHARMA_WORDS),
    ("Reading & writing: stories", "/read_write", thai_reading.STORIES),
    ("ThaiBridge Spelling guide", "/paiboon", app.PAIBOON_GUIDE),
    ("Culture", "/culture", app.CULTURAL_INFO),
    ("Culture: stories", "/culture", app.CULTURAL_STORIES),
    ("Culture: feature stories", "/culture", app.CULTURAL_FEATURE_STORIES),
    ("Theravada", "/theravada", app.THERAVADA_TEACHINGS),
    ("Meditation", "/meditation", app.MEDITATION_TECHNIQUES),
    ("Tour Guide vocabulary", "/tour-guide", app.TOUR_VOCAB),
    ("Business Thai", "/business-thai", app.BUSINESS_VOCAB),
]

# Thai typed straight into a page's HTML rather than its data. Monk Mode, the
# chanting book and the journal belong to other batches.
TEMPLATE_SKIP = re.compile(r"(monk|chant|journal|print[\\/]|tour_trips)")


def has_thai(value):
    return isinstance(value, str) and bool(THAI.search(value))


def first(d, keys):
    for k in keys:
        v = d.get(k)
        if isinstance(v, str) and v.strip():
            return v.strip()
    return ""


def label(path):
    """A readable 'where on the page' from the keys walked to get here."""
    parts = [str(p).replace("_", " ") for p in path if not isinstance(p, int)]
    return " › ".join(parts[-3:])


class Sheet:
    """Collects rows, keeping only the first appearance of each Thai text."""

    def __init__(self):
        self.rows = []
        self.seen = set()

    def add(self, page, url, where, thai, spelling="", meaning=""):
        thai = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", thai))).strip()
        if not thai or thai in self.seen:
            return
        # Only an explanation with English in it needs telling apart; a bare
        # Thai word is just a Thai word.
        if meaning.startswith("(") and not LATIN.search(thai):
            meaning = ""
        self.seen.add(thai)
        self.rows.append((page, url, where, thai, spelling, meaning))

    def walk(self, page, url, x, path=()):
        if isinstance(x, dict):
            main = first(x, THAI_KEYS)
            if has_thai(main):
                if x.get("particle"):
                    main += " (+ ครับ/ค่ะ)"
                self.add(page, url, label(path), main, first(x, SPELLING_KEYS),
                         "" if has_thai(first(x, MEANING_KEYS)) else first(x, MEANING_KEYS))
            for k, v in x.items():
                if has_thai(k):
                    self.add(page, url, label(path), k)
                if k in THAI_KEYS and v is x.get(k) and v.strip() == main.replace(" (+ ครับ/ค่ะ)", ""):
                    continue
                if has_thai(v):
                    # Notes, tips, breakdowns, male/female forms: English with
                    # Thai inside, or Thai with no spelling beside it.
                    self.add(page, url, label(path + (k,)), v,
                             x.get("paiboon", "") if k in ("male", "female") else "",
                             "" if k in ("male", "female") else "(note: check the Thai inside)")
                elif isinstance(v, (dict, list, tuple)):
                    self.walk(page, url, v, path + (k,))
        elif isinstance(x, (list, tuple)):
            for i, v in enumerate(x):
                if has_thai(v):
                    self.add(page, url, label(path), v)
                else:
                    self.walk(page, url, v, path + (i,))


def consonant_rows(sheet):
    for c in thai_consonants.CONSONANTS:
        sheet.add("Alphabet: consonants", "/alphabet", "consonant name",
                  "{}  ·  {}".format(c["char"], c["name_thai"]), c["name"], c["meaning"])


def register_switch_rows(sheet):
    """Each phrase the register switcher rewrites, with every version of it."""
    for original, versions in thai_registers.VARIANTS.items():
        for register, v in versions.items():
            if isinstance(v, dict) and has_thai(v.get("thai", "")):
                sheet.add("Register switcher (shown on several pages)", "/survival, /sentences",
                          "{} → {}".format(original, register), v["thai"], v.get("paiboon", ""),
                          v.get("note", ""))


def builder_rows(sheet):
    for s in sentence_builder.SENTENCES:
        level = sentence_builder.level_of(s)
        for n, order in enumerate([s["tiles"]] + s.get("alternates", [])):
            tiles = sentence_builder.tiles_for(s, "male", order)
            spelling = " ".join(sentence_builder.ROMANISATION.get(t, "?") for t in tiles)
            where = "Build the sentence · {}{}".format(level, " · also accepted" if n else "")
            sheet.add("Sentences: build the sentence", "/sentences", where,
                      sentence_builder.answer_text(tiles), spelling, s["english"])
        if has_thai(s.get("tip", "")):
            sheet.add("Sentences: build the sentence", "/sentences", "tip", s["tip"],
                      "", "(note: check the Thai inside)")


def template_rows(sheet):
    for path in sorted(glob.glob(os.path.join(REPO_ROOT, "templates", "**", "*.html"), recursive=True)
                       + glob.glob(os.path.join(REPO_ROOT, "static", "js", "*.js"))):
        rel = os.path.relpath(path, REPO_ROOT).replace("\\", "/")
        if TEMPLATE_SKIP.search(rel):
            continue
        with open(path, encoding="utf-8") as f:
            for line in f:
                text = line.strip()
                # Comments and template logic never reach the learner.
                if text.startswith(("//", "{%", "{#", "*", "/*")):
                    continue
                text = re.sub(r"\{\{.*?\}\}", "", text)
                if rel.endswith(".js") or CODE_HINT.search(text):
                    texts = [a or b for a, b in QUOTED.findall(text)]
                else:
                    texts = [re.sub(r"<[^>]+>", " ", text)]
                for t in texts:
                    if has_thai(t):
                        sheet.add("Written into the page", rel, "page text", t, "",
                                  "(note: check the Thai inside)")


INTRO_TH = [
    "เรียน อาจารย์ครับ 🙏",
    "นี่คือภาษาไทยทั้งหมดในส่วนเรียนหลักของแอป ThaiBridge AI (ชุดที่ 1) "
    "เช่น หน้า Survival, คำศัพท์, ประโยค, ไวยากรณ์, วรรณยุกต์, สระ, พยัญชนะ, การอ่าน, วัฒนธรรม",
    "ประโยคส่วนใหญ่ผมร่างเอง ยังไม่มีคนไทยตรวจ ขอให้อาจารย์ช่วยดูว่าถูกต้อง "
    "เป็นธรรมชาติ และสุภาพพอดีไหมครับ",
    "วิธีตรวจ: ในแผ่นงาน \"ตรวจ\" ช่อง ผล ให้เลือก ✓ ถ้าถูกแล้ว ✗ ถ้าต้องแก้ "
    "แล้วเขียนแบบที่ถูกในช่อง แก้เป็น หรือ ? ถ้าไม่แน่ใจ ข้อไหนไม่แน่ใจ ข้ามได้เลยนะครับ",
    "คำอ่านตัวอักษรโรมันเรียกว่า ThaiBridge Spelling (พัฒนาจากระบบ Paiboon+) "
    "ถ้าวรรณยุกต์หรือเสียงในคำอ่านผิด ช่วยบอกด้วยครับ",
    "แถวที่เขียนว่า (note) เป็นคำอธิบายภาษาอังกฤษที่มีคำไทยอยู่ข้างใน ช่วยตรวจเฉพาะคำไทยครับ",
    "ส่วนใหญ่แสดงแบบผู้ชาย (ครับ / ผม) แอปเปลี่ยนเป็น ค่ะ / คะ / ดิฉัน ให้ผู้หญิงเอง "
    "ถ้ามีประโยคไหนที่ผู้หญิงควรพูดต่างออกไป ช่วยบอกในช่อง หมายเหตุ ครับ",
    "ขอบพระคุณมากครับ",
]
INTRO_EN = [
    "This is all the Thai in the app's core learning pages (Batch 1): Survival, vocabulary, "
    "sentences, grammar, tones, vowels, consonants, reading and culture.",
    "Most of it is my own draft and no Thai speaker has checked it yet. Please check that "
    "each line is correct, natural and polite enough.",
    "How: on the review sheet, choose ✓ if a line is fine, ✗ if it needs changing (and "
    "write the better version under Correction), or ? if unsure. Skip anything you like.",
    "The romanised line is ThaiBridge Spelling (based on Paiboon+). Please flag any "
    "wrong tone or sound in it too.",
    "Rows marked (note) are English explanations with Thai words inside: only the Thai needs checking.",
    "Lines are mostly shown as a man says them (ครับ / ผม). The app switches to ค่ะ / คะ / ดิฉัน "
    "for women. If a woman should say a line differently, please add it under Comment.",
    "Each Thai line is listed once, on the first page that uses it.",
]

HEADERS = ["#", "หน้า · Page", "ที่อยู่ · Address", "ส่วน · Where on the page",
           "ภาษาไทย · Thai", "ThaiBridge Spelling", "ความหมาย · Meaning",
           "ผล · Result", "แก้เป็น · Correction", "หมายเหตุ · Comment"]
WIDTHS = [6, 24, 18, 30, 40, 30, 34, 10, 36, 30]
THAI_FONT = "Leelawadee UI"


def build(out_path):
    sheet = Sheet()
    for page, url, data in PAGES:
        sheet.walk(page, url, data)
        if page == "Sentences: conversational phrases":
            builder_rows(sheet)
        if page == "Register switcher (shown on several pages)":
            register_switch_rows(sheet)
        if page == "Vowels & syllables":
            consonant_rows(sheet)
    template_rows(sheet)

    wb = Workbook()
    intro = wb.active
    intro.title = "อ่านก่อน · Read me"
    intro.column_dimensions["A"].width = 110
    intro.append(["ตรวจภาษาไทย ชุดที่ 1 · ThaiBridge AI · Batch 1 Thai review"])
    intro["A1"].font = Font(name=THAI_FONT, size=16, bold=True, color="7A3B00")
    intro.append([])
    for para in INTRO_TH:
        intro.append([para])
    intro.append([])
    for para in INTRO_EN:
        intro.append([para])
    intro.append([])
    intro.append(["{} lines to check.".format(len(sheet.rows))])
    for row in intro.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            if cell.font is None or not cell.font.b:
                cell.font = Font(name=THAI_FONT, size=12)

    ws = wb.create_sheet("ตรวจ · Review")
    ws.append(HEADERS)
    for i, w in enumerate(WIDTHS):
        ws.column_dimensions[chr(65 + i)].width = w
    head_fill = PatternFill("solid", fgColor="F6EFE2")
    for cell in ws[1]:
        cell.font = Font(name=THAI_FONT, bold=True)
        cell.fill = head_fill
        cell.alignment = Alignment(wrap_text=True, vertical="top")
    for n, (page, url, where, thai, spelling, meaning) in enumerate(sheet.rows, 1):
        ws.append([n, page, url, where, thai, spelling, meaning, "", "", ""])
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.font = Font(name=THAI_FONT, size=11)
        row[4].font = Font(name=THAI_FONT, size=14)
        row[5].font = Font(name=THAI_FONT, size=11, italic=True, color="8A5A00")
    result = DataValidation(type="list", formula1='"✓,✗,?"', allow_blank=True)
    ws.add_data_validation(result)
    result.add("H2:H{}".format(len(sheet.rows) + 1))
    ws.freeze_panes = "E2"
    ws.auto_filter.ref = "A1:J{}".format(len(sheet.rows) + 1)

    wb.save(out_path)
    return sheet.rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default=os.path.join("docs", "batch1-thai-review-2026-10-13.xlsx"))
    args = parser.parse_args()
    out = args.out if os.path.isabs(args.out) else os.path.join(REPO_ROOT, args.out)
    rows = build(out)
    pages = {}
    for r in rows:
        pages[r[0]] = pages.get(r[0], 0) + 1
    for page, n in pages.items():
        print("{:5}  {}".format(n, page))
    print("Wrote {}: {} lines".format(args.out, len(rows)))


if __name__ == "__main__":
    main()
