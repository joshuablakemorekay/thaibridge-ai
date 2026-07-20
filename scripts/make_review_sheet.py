"""Build a Thai-teacher review sheet for NEW Monk Mode content.

Every Thai line in the monk lessons starts life as an AI draft. Before it can be
trusted it needs a native speaker — and specifically a Thai teacher of English,
because half of it is pronunciation instruction rather than plain translation.

This script produces the sheet she marks up. The important part is that it only
asks about material she has NOT already seen: it loads each lesson file as it is
now, loads the same file as it was at a base git ref, and reports the
difference. Re-run it after the next batch of content and she gets the next
batch of questions, never the same ones twice.

Usage:

    python scripts/make_review_sheet.py                    # vs HEAD~1
    python scripts/make_review_sheet.py --base HEAD~3
    python scripts/make_review_sheet.py --all              # everything, no diff
    python scripts/make_review_sheet.py --out docs/review-x # writes .md and .html

Output is one Markdown file (easy to read in a chat app) and one HTML file
(prints cleanly on paper, which is how it actually gets marked up).
"""

import argparse
import glob
import html
import json
import os
import subprocess
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT_DIR = os.path.join(REPO_ROOT, "content", "monk")

# The Thai-bearing fields we want checked, in the order they should be read,
# with the label the teacher sees. Anything not listed here is either English
# (she is not reviewing my English) or machinery.
THAI_FIELDS = [
    ("english_tip_th", "คำอธิบายการออกเสียง"),
    ("meaning_th", "คำแปล"),
    ("note_th", "หมายเหตุ"),
    ("nuance_th", "ความต่างของคำ"),
    ("context_th", "บริบท"),
]


def load_lessons(base_ref=None):
    """Every monk lesson, either from disk or from a git ref.

    Returns {filename: lesson dict}. A file that does not exist at the base ref
    (a brand new lesson) simply has no entry, which makes all of its content
    count as new — exactly what we want.
    """
    lessons = {}
    for path in sorted(glob.glob(os.path.join(CONTENT_DIR, "*.json"))):
        name = os.path.basename(path)
        if base_ref is None:
            with open(path, encoding="utf-8") as f:
                lessons[name] = json.load(f)
            continue
        rel = "content/monk/" + name
        try:
            raw = subprocess.run(
                ["git", "show", "{}:{}".format(base_ref, rel)],
                cwd=REPO_ROOT, capture_output=True, check=True,
            ).stdout.decode("utf-8")
        except subprocess.CalledProcessError:
            continue  # didn't exist at that ref — all of it is new
        lessons[name] = json.loads(raw)
    return lessons


def entry_items(entry, group):
    """Turn one vocab/phrase/drill/option dict into a review item, or None.

    An item is worth reviewing only if it actually carries Thai prose. A drill
    line with no meaning_th and no tip has nothing for her to correct.
    """
    thai_bits = [(lbl, entry[key]) for key, lbl in THAI_FIELDS if entry.get(key)]
    if not thai_bits:
        return None
    return {
        "kind": "entry",
        "group": group,
        "english": entry.get("english", ""),
        "thai": entry.get("thai", ""),
        "paiboon": entry.get("paiboon", ""),
        "respell": entry.get("english_respell", ""),
        "respell_us": entry.get("english_respell_us", ""),
        "ipa": entry.get("english_ipa", ""),
        "thai_bits": thai_bits,
        # Identity for the diff. Keyed on the English, because that is what
        # stays fixed while the Thai gets corrected.
        "key": (group, entry.get("english", "")),
    }


def prose_item(group, label, text, key_extra=""):
    """A standalone block of Thai prose — a section intro, a reading tip."""
    if not text:
        return None
    return {
        "kind": "prose",
        "group": group,
        "english": label,
        "thai_bits": [("ข้อความ", text)],
        "key": (group, label + key_extra),
    }


def walk(lesson):
    """Every reviewable item in one lesson, in reading order."""
    items = []
    title = lesson.get("title", {}).get("en", "")

    for e in lesson.get("vocab", []):
        it = entry_items(e, "คำศัพท์ / Vocabulary")
        if it:
            items.append(it)
    for e in lesson.get("phrases", []):
        it = entry_items(e, "วลี / Phrases")
        if it:
            items.append(it)

    for sec in lesson.get("drill_sections", []):
        group = "บทฝึก / " + sec.get("title", {}).get("en", "Drills")
        it = prose_item(group, "คำนำของบทฝึก / section intro", sec.get("intro_th"))
        if it:
            items.append(it)
        for d in sec.get("drills", []):
            it = entry_items(d, group)
            if it:
                items.append(it)

    wc = lesson.get("word_choices")
    if wc:
        group = "เลือกใช้คำ / " + wc.get("title", {}).get("en", "Word choices")
        it = prose_item(group, "คำนำ / intro", wc.get("intro_th"))
        if it:
            items.append(it)
        for s in wc.get("sets", []):
            # The concept, not the block, names the group — otherwise every set
            # repeats the same heading and she cannot tell them apart at a
            # glance. Thai first, since that is the language she reads.
            concept = s.get("concept", {})
            label = "เลือกใช้คำ — {} / {}".format(
                concept.get("th", ""), concept.get("en", ""))
            for o in s.get("options", []):
                it = entry_items(o, label)
                if it:
                    items.append(it)

    rg = lesson.get("reading_guide")
    if rg:
        group = "วิธีอ่าน / " + rg.get("title", {}).get("en", "Reading guide")
        it = prose_item(group, "คำนำ / intro", rg.get("intro_th"))
        if it:
            items.append(it)
        for i, tip in enumerate(rg.get("tips", []), 1):
            it = prose_item(
                group, "{}. {}".format(i, tip.get("en", "")), tip.get("th"),
                key_extra=str(i))
            if it:
                items.append(it)

    for p in lesson.get("passages", []):
        group = "บทอ่าน / Readings"
        it = prose_item(
            group, "คำนำ — " + p.get("title", {}).get("en", ""), p.get("intro_th"))
        if it:
            items.append(it)

    return title, items


def new_items(current, base):
    """Items in `current` that are new, or whose Thai has been rewritten.

    Both cases need her eyes; a changed line is as unreviewed as a new one.
    """
    base_by_key = {i["key"]: i for i in base}
    out = []
    for item in current:
        old = base_by_key.get(item["key"])
        if old is None:
            item["status"] = "new"
            out.append(item)
        elif old["thai_bits"] != item["thai_bits"]:
            item["status"] = "changed"
            item["old_thai"] = old["thai_bits"]
            out.append(item)
    return out


def collect(base_ref, review_all):
    """[(lesson title, [items])] for every lesson with something to review."""
    now = load_lessons(None)
    before = {} if review_all else load_lessons(base_ref)

    sections = []
    for name in sorted(now):
        title, items = walk(now[name])
        if review_all:
            for i in items:
                i["status"] = "new"
            fresh = items
        else:
            _, base_items = walk(before.get(name, {}))
            fresh = new_items(items, base_items)
        if fresh:
            sections.append((title, fresh))
    return sections


# ── Rendering ────────────────────────────────────────────────────────────────

INTRO_TH = (
    "ภาษาไทยทั้งหมดในเอกสารนี้เขียนโดย AI ยังไม่มีเจ้าของภาษาตรวจ"
)
INTRO_EN = (
    "All the Thai below was drafted by an AI and has not been checked by a "
    "native speaker."
)
ASK = [
    ("ความถูกต้อง", "คำอธิบายวิธีออกเสียงถูกไหม (V, F, TH และ R, L)"),
    ("ภาษา", "สำนวนอ่านเป็นธรรมชาติไหม เหมาะกับพระอ่านไหม"),
    ("คำแปล", "คำแปลภาษาไทยตรงกับประโยคภาษาอังกฤษไหม"),
]


def meta_line(item):
    """The English + pronunciation line, as plain text pieces."""
    bits = []
    if item.get("respell"):
        bits.append("คำอ่าน: " + item["respell"])
    if item.get("respell_us"):
        bits.append("US: " + item["respell_us"])
    if item.get("ipa"):
        bits.append("IPA: " + item["ipa"])
    if item.get("thai"):
        bits.append("คำไทย: " + item["thai"])
    return bits


def render_md(sections, base_ref, review_all):
    total = sum(len(items) for _, items in sections)
    L = []
    L.append("# ตรวจเนื้อหาใหม่ — Monk Mode English")
    L.append("## Review of new material — {}".format(TODAY))
    L.append("")
    L.append("**{}**".format(INTRO_TH))
    L.append(INTRO_EN)
    L.append("")
    L.append("ช่วยตรวจ {} อย่าง / Please check:".format(len(ASK)))
    L.append("")
    for i, (head, detail) in enumerate(ASK, 1):
        L.append("{}. **{}** — {}".format(i, head, detail))
    L.append("")
    L.append("**เขียนแก้ตรงบรรทัด \"แก้เป็น:\" ได้เลย / "
             "Write corrections on the \"แก้เป็น:\" line.**")
    L.append("")
    L.append("> เนื้อหาทั้งหมดนี้สร้างขึ้นจากสิ่งที่อาจารย์ให้มา — บทฝึกลิ้น บทอ่านธรรมะ "
             "และคำแนะนำเรื่องเสียง V, F, TH การนำคำไปใส่ในประโยค และการอ่านเอาความ "
             "ส่วนที่เป็นภาษาไทยผมให้ AI ร่างไว้ก่อน ยังไม่มีใครตรวจเลยครับ "
             "ขอบพระคุณมากครับ 🙏")
    L.append("")
    L.append("---")

    for title, items in sections:
        L.append("")
        L.append("# {}".format(title))
        group = None
        for item in items:
            if item["group"] != group:
                group = item["group"]
                L.append("")
                L.append("## {}".format(group))
            L.append("")
            flag = " *(แก้ไขใหม่ / changed)*" if item["status"] == "changed" else ""
            L.append("### {}{}".format(item["english"] or "—", flag))
            meta = meta_line(item)
            if meta:
                L.append("- " + "  ·  ".join("`{}`".format(m) for m in meta))
            if item["status"] == "changed":
                for lbl, val in item.get("old_thai", []):
                    L.append("- *เดิม — {}:* {}".format(lbl, val))
            for lbl, val in item["thai_bits"]:
                L.append("- **{}:** {}".format(lbl, val))
            L.append("- แก้เป็น: __________________________________________")

    L.append("")
    L.append("---")
    L.append("รวม {} ข้อ · ขอบคุณมากครับ 🙏".format(total))
    L.append("")
    return "\n".join(L)


HTML_CSS = """
  body { font-family: "Noto Sans Thai", "Leelawadee UI", Tahoma, "Segoe UI", sans-serif;
         max-width: 52rem; margin: 2rem auto; padding: 0 1.2rem; color: #222;
         line-height: 1.65; font-size: 15px; }
  h1 { font-size: 1.45rem; margin-bottom: .2rem; }
  h1.lessontitle { font-size: 1.3rem; margin-top: 2.4rem; border-bottom: 3px solid #FF9933;
                   padding-bottom: .3rem; }
  h2.lesson { font-size: 1.08rem; background: #f4efe6; border-left: 5px solid #FF9933;
              padding: .45rem .8rem; margin: 1.6rem 0 .8rem; border-radius: 0 6px 6px 0; }
  .sub { color: #666; margin-top: 0; }
  .notice { background: #fff6e8; border: 1px solid #f0d9ad; border-radius: 8px;
            padding: .8rem 1rem; margin: 1rem 0; }
  .entry { border: 1px solid #e3ddd2; border-radius: 8px; padding: .7rem .9rem .8rem;
           margin: .7rem 0; break-inside: avoid; page-break-inside: avoid; }
  .entry h3 { margin: 0 0 .3rem; font-size: 1.02rem; }
  .entry.changed { border-color: #d6b26a; background: #fffdf6; }
  .tag { font-size: .74em; background: #d6b26a; color: #fff; border-radius: 4px;
         padding: .05em .45em; vertical-align: middle; margin-left: .4em; }
  .meta { font-size: .86em; color: #555; margin-bottom: .45rem; }
  .meta code { background: #f4f1ea; border-radius: 4px; padding: 0 .35em; font-size: 1.02em; }
  .th { background: #f2f8ee; border-radius: 6px; padding: .3rem .5rem; margin: .25rem 0; }
  .th .lbl { display: inline-block; min-width: 10.5em; font-weight: 700; color: #2c6e2f; }
  .old { color: #888; font-size: .9em; }
  .old .lbl { display: inline-block; min-width: 10.5em; font-weight: 700; }
  .fix { margin-top: .4rem; }
  .fix .line { display: inline-block; width: 70%; border-bottom: 1.5px dotted #aaa;
               height: 1.15em; }
  @media print {
    body { margin: 0 auto; font-size: 12.5px; }
    .entry { margin: .45rem 0; }
    h2.lesson, h1.lessontitle { break-after: avoid; page-break-after: avoid; }
    a { color: inherit; text-decoration: none; }
  }
"""


def render_html(sections, base_ref, review_all):
    total = sum(len(items) for _, items in sections)
    e = html.escape
    L = ['<!DOCTYPE html>', '<html lang="th">', '<head>', '<meta charset="utf-8">',
         '<title>ตรวจเนื้อหาใหม่ — Monk Mode English</title>',
         '<style>' + HTML_CSS + '</style>', '</head>', '<body>']
    L.append('<h1>ตรวจเนื้อหาใหม่ — Monk Mode English</h1>')
    L.append('<p class="sub">Review of new material · {} · ThaiBridge AI</p>'
             .format(TODAY))
    L.append('<div class="notice">')
    L.append('<strong>{}</strong><br>{}<br><br>'.format(INTRO_TH, INTRO_EN))
    L.append('ช่วยตรวจ {} อย่าง / Please check:<br>'.format(len(ASK)))
    for i, (head, detail) in enumerate(ASK, 1):
        L.append('{}. <strong>{}</strong> — {}<br>'.format(i, head, detail))
    L.append('<br>เขียนแก้ตรงบรรทัด <strong>แก้เป็น:</strong> ได้เลย / '
             'Write corrections on the dotted line.<br><br>')
    L.append('เนื้อหานี้สร้างขึ้นจากคำแนะนำของอาจารย์เมื่อวันที่ 20 กรกฎาคม — '
             'เรื่องเสียง V, F, TH การนำคำไปใส่ในประโยค และการอ่านเอาความ '
             'ขอบพระคุณมากครับ 🙏')
    L.append('</div>')

    for title, items in sections:
        L.append('<h1 class="lessontitle">{}</h1>'.format(e(title)))
        group = None
        for item in items:
            if item["group"] != group:
                group = item["group"]
                L.append('<h2 class="lesson">{}</h2>'.format(e(group)))
            cls = "entry changed" if item["status"] == "changed" else "entry"
            L.append('<div class="{}">'.format(cls))
            tag = ('<span class="tag">แก้ไขใหม่</span>'
                   if item["status"] == "changed" else '')
            L.append('<h3>{}{}</h3>'.format(e(item["english"] or "—"), tag))
            meta = meta_line(item)
            if meta:
                L.append('<div class="meta">{}</div>'.format(
                    " · ".join("<code>{}</code>".format(e(m)) for m in meta)))
            for lbl, val in item.get("old_thai", []):
                L.append('<div class="old"><span class="lbl">เดิม — {}</span>{}</div>'
                         .format(e(lbl), e(val)))
            for lbl, val in item["thai_bits"]:
                L.append('<div class="th"><span class="lbl">{}</span>{}</div>'
                         .format(e(lbl), e(val)))
            L.append('<div class="fix"><strong>แก้เป็น:</strong> '
                     '<span class="line"></span></div>')
            L.append('</div>')

    L.append('<hr><p>รวม {} ข้อ · ขอบคุณมากครับ 🙏</p>'.format(total))
    L.append('</body></html>')
    return "\n".join(L)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="HEAD~1",
                        help="git ref to diff against (default HEAD~1)")
    parser.add_argument("--all", action="store_true", dest="review_all",
                        help="include every item, not just new ones")
    parser.add_argument("--out", default=None,
                        help="output path without extension")
    parser.add_argument("--date", default=None, help="date shown on the sheet")
    args = parser.parse_args()

    global TODAY
    TODAY = args.date or __import__("datetime").date.today().isoformat()

    sections = collect(args.base, args.review_all)
    if not sections:
        print("Nothing new to review against {}.".format(args.base))
        return 0

    out = args.out or os.path.join(
        REPO_ROOT, "docs", "review-{}-new-material".format(TODAY))
    os.makedirs(os.path.dirname(out), exist_ok=True)

    with open(out + ".md", "w", encoding="utf-8") as f:
        f.write(render_md(sections, args.base, args.review_all))
    with open(out + ".html", "w", encoding="utf-8") as f:
        f.write(render_html(sections, args.base, args.review_all))

    total = sum(len(i) for _, i in sections)
    for title, items in sections:
        print("  {:<45} {} items".format(title[:44], len(items)))
    print("\n{} items across {} lessons".format(total, len(sections)))
    print("Wrote: {}.md\n       {}.html".format(out, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
