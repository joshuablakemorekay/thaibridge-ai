"""Build the Thai-teacher review sheet for the Sentences page's new Thai.

Two things on /sentences were added as unreviewed drafts on 2026-10-09: the
Answering Questions section (app.SENTENCE_PATTERNS['answering']) and the
Build the Sentence drill (sentence_builder.SENTENCES). This prints them as a
sheet a teacher can mark up — built from the live data, so she checks exactly
what learners see, not a copy that may have drifted.

Only the male version of each line is listed: the female one differs only in
ดิฉัน and ค่ะ/คะ, which gets one question of its own at the end rather than
doubling the sheet.

    python scripts/make_sentences_review.py
    python scripts/make_sentences_review.py --out docs/sentences-review-2026-10-09

Writes a .md (easy to send in a chat app) and a .html (prints cleanly).
"""

import argparse
import html
import os
import sys

# Importing app connects to the database at startup. Empty, not popped — the
# same reason as tests/conftest.py: dotenv would load the LIVE url back in.
os.environ["DATABASE_URL"] = ""

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import app  # noqa: E402
import sentence_builder  # noqa: E402

BLANK = "______________________________________________"

INTRO = """# ขอความช่วยเหลือตรวจประโยคภาษาไทยครับ
## Sentences page — new Thai to check · ThaiBridge AI · {date}

เรียน อาจารย์ครับ 🙏

ผมทำแอปสอนภาษาไทยให้ชาวต่างชาติ ในหน้า **ประโยคและบทสนทนา** ผมเพิ่มของใหม่ 2 ส่วน:
**วิธีตอบคำถาม** (ใช่/ไม่ใช่, ยังไม่, ไม่ได้) และ **แบบฝึกเรียงประโยค** ที่ผู้เรียนต้องเรียงคำให้ถูก

ทุกประโยคผมร่างเอง **ยังไม่มีคนไทยตรวจ** เลยขอให้อาจารย์ช่วยดูว่า
**ถูกต้องและเป็นธรรมชาติไหม** — คนไทยพูดแบบนี้จริงหรือเปล่าครับ

> **ใช้เวลาประมาณ 20 นาที** — ถ้าประโยคไหนถูกแล้ว ทำเครื่องหมาย ✓ ได้เลย
> ถ้าผิดหรือไม่เป็นธรรมชาติ เขียนแบบที่ถูกตรงบรรทัด **ตอบ:** ครับ
> ถ้าข้อไหนไม่แน่ใจ ข้ามได้เลยนะครับ

*I teach Thai to foreigners through an app. I've added two things to its
Sentences page: how to answer questions, and a drill where learners put Thai
words in the right order. I drafted every line myself and no Thai speaker has
checked them yet. Please mark each one ✓ if it's correct and natural, or write
the better version. About 20 minutes — skip anything you're unsure of.*

---
"""

QUESTIONS = [
    ("ผู้หญิงใช้ **ดิฉัน** ทุกประโยคในหน้านี้ ในชีวิตประจำวันเป็นทางการเกินไปไหมครับ "
     "ควรใช้ **ฉัน** แทนหรือเปล่า",
     "Every woman's line on this page uses ดิฉัน. Is that too formal for everyday "
     "speech — should it be ฉัน?"),
    ("ผู้หญิงถามลงท้าย **คะ** และตอบลงท้าย **ค่ะ** — ถูกต้องไหมครับ",
     "Women's questions end in คะ and their answers in ค่ะ. Is that right?"),
    ("**เมื่อวานไปทำงานไหม** — ถามเรื่องที่ผ่านไปแล้ว ใช้ **ไหม** ได้ไหมครับ "
     "หรือควรเป็น **หรือเปล่า**",
     "For a question about yesterday, is ไหม natural, or should it be หรือเปล่า?"),
    ("ตอบว่า \"ยังไม่ได้กิน\" กับตอบสั้น ๆ ว่า \"ยัง\" — คนไทยพูดแบบไหนบ่อยกว่าครับ",
     "Answering 'not yet': is ยังไม่ได้กิน or just ยัง more common?"),
]


def answering_rows():
    for pattern in app.SENTENCE_PATTERNS["answering"]["patterns"]:
        for ex in pattern["examples"]["male"]:
            for part in ("q", "yes", "no"):
                yield pattern["name"], ex[part]


def builder_rows():
    for s in sentence_builder.SENTENCES:
        tiles = sentence_builder.tiles_for(s, "male")
        yield s["english"], " · ".join(tiles), sentence_builder.answer_text(tiles)


def build_markdown(date):
    out = [INTRO.format(date=date)]

    out.append("# ก. วิธีตอบคำถาม\n## A. Answering questions\n")
    out.append("*Each question is followed by its yes and no answer.*\n")
    n = 0
    current = None
    for heading, line in answering_rows():
        if heading != current:
            out.append(f"\n### {heading}\n")
            current = heading
        n += 1
        out.append(f"**{n}.** {line['thai']}  ·  *{line['paiboon']}*  ·  {line['english']}  \n"
                   f"**ตอบ:** ✓ / {BLANK}\n")

    out.append("\n---\n\n# ข. แบบฝึกเรียงประโยค\n## B. Build the sentence\n")
    out.append("*The learner sees the English and puts the Thai words in order. "
               "The words are shown split as the learner sees them — please also "
               "say if a word is split in the wrong place.*\n")
    for english, tiles, joined in builder_rows():
        n += 1
        out.append(f"**{n}.** {english}  \n{joined}  ·  ({tiles})  \n"
                   f"**ตอบ:** ✓ / {BLANK}\n")

    out.append("\n---\n\n# ค. คำถามเพิ่มเติม\n## C. A few questions\n")
    for thai, english in QUESTIONS:
        n += 1
        out.append(f"**{n}.** {thai}  \n*{english}*  \n**ตอบ:** {BLANK}\n")

    out.append("\n---\n\nขอบคุณมากครับ 🙏\n")
    return "\n".join(out)


def build_html(markdown_text, date):
    """A plain printable page. Light formatting only: headings, bold, italics."""
    import re

    def inline(text):
        text = html.escape(text)
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        return re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)

    body = []
    for block in markdown_text.split("\n"):
        line = block.rstrip()
        if not line:
            continue
        if line == "---":
            body.append("<hr>")
        elif line.startswith("### "):
            body.append(f"<h3>{inline(line[4:])}</h3>")
        elif line.startswith("## "):
            body.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            body.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("> "):
            body.append(f"<blockquote>{inline(line[2:])}</blockquote>")
        else:
            body.append(f"<p>{inline(line.rstrip(' '))}</p>")
    return f"""<!doctype html>
<html lang="th"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sentences review {date}</title>
<style>
body {{ font-family: 'Sarabun', 'Leelawadee UI', sans-serif; max-width: 780px;
       margin: 2rem auto; padding: 0 16px; line-height: 1.7; color: #222; background: #fff; }}
h1 {{ font-size: 1.5rem; margin-top: 2rem; }} h2 {{ font-size: 1.05rem; color: #555; }}
h3 {{ font-size: 1.05rem; margin-top: 1.5rem; }}
blockquote {{ border-left: 4px solid #d4af37; margin: 0.5rem 0; padding: 0.25rem 1rem; background: #fff9e6; }}
p {{ margin: 0.4rem 0 0.9rem; break-inside: avoid; }}
hr {{ margin: 2rem 0; }}
@media print {{ body {{ margin: 0; }} }}
</style></head><body>
{chr(10).join(body)}
</body></html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--out", default="docs/sentences-review-2026-10-09")
    parser.add_argument("--date", default="2026-10-09")
    args = parser.parse_args()

    md = build_markdown(args.date)
    base = os.path.join(REPO_ROOT, args.out)
    with open(base + ".md", "w", encoding="utf-8") as f:
        f.write(md)
    with open(base + ".html", "w", encoding="utf-8") as f:
        f.write(build_html(md, args.date))
    print(f"wrote {args.out}.md and .html")


if __name__ == "__main__":
    main()
