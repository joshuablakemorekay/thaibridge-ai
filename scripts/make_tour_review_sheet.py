"""Build the Thai teacher's review sheet for the Tour Guide trips.

Every Thai line in tour_trips.py is an AI draft until a native speaker has
read it. This writes the sheet she marks up: a short list of questions I am
genuinely unsure about first, then every line a learner hears or says, trip by
trip, with a column to tick or correct.

What is left out, on purpose:
  * the deliberately wrong answers ("miss"). They are plain words used in the
    wrong place, and asking her to check them would double the sheet for
    almost nothing;
  * Thai words quoted inside the English tips, which are single dictionary
    words already shown elsewhere.

Usage:

    python scripts/make_tour_review_sheet.py
    python scripts/make_tour_review_sheet.py --out docs/tour-trips-review-2026-10-09

Writes a .md (easy to read in a chat app) and a .html (prints cleanly, which
is how it actually gets marked up), like make_review_sheet.py.
"""

import argparse
import html
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

import tour_trips  # noqa: E402

# Questions I could not settle myself. Each names the line as the app shows
# it, says what I am unsure about, and what answer would help.
QUESTIONS = [
    ('เอาหนึ่งชาม', 'ao nʉ̀ŋ chaam', 'One bowl, please (Chinatown noodle stall)',
     'ลำดับคำนี้เป็นธรรมชาติไหมครับ หรือคนไทยพูด "เอาชามนึง" / "หนึ่งชาม" มากกว่า',
     'Is this word order natural, or would people say เอาชามนึง / หนึ่งชาม?'),
    ('ปลาตอดเท้าใช่ไหม', 'bplaa dtɔ̀ɔt táao châi mǎi', 'The fish are nibbling your feet, aren’t they?',
     'คำว่า "ตอด" ใช้กับปลาที่น้ำตกถูกไหมครับ',
     'Is ตอด the right verb for small fish nibbling your feet?'),
    ('ตลาดกลางคืนอยู่ที่ไหน', 'dtà-làat glaaŋ-kʉʉn yùu tîi-nǎi', 'Where is the night market?',
     'คนในเมืองกาญจนบุรีเรียกตลาดกลางคืนว่าอะไรครับ เช่น ตลาดโต้รุ่ง หรือ ตลาดนัด',
     'What would locals actually call it: ตลาดกลางคืน, ตลาดโต้รุ่ง, ตลาดนัด?'),
    ('เก็บเงินด้วย / เช็คบิล', 'gèp ŋən dûai / chék-bin', 'Asking for the bill',
     'แอปสอนว่า "เก็บเงินด้วย" ใช้ที่ร้านข้างทาง "เช็คบิล" ใช้ที่ร้านอาหาร ถูกต้องไหมครับ',
     'The app says เก็บเงินด้วย at street stalls and เช็คบิล in restaurants. Is that right?'),
    ('ใส่อันนี้ครับ', 'sài an-níi kráp', 'Put this on (temple guard lending a wrap)',
     'ยามที่วัดพูดแบบนี้เป็นธรรมชาติไหมครับ',
     'Would a temple guard say it like this?'),
    ('อีกไกลไหม', 'ìik glai mǎi', 'Is it much further?',
     'ใช้ถามว่า "ยังต้องเดินอีกไกลไหม" ได้ไหมครับ',
     'Does this work for "is there much further to walk?"'),
    ('ร้อนแต่สบาย', 'rɔ́ɔn dtɛ̀ɛ sà-baai', 'Hot but lovely (in a hot spring)',
     'เป็นธรรมชาติไหมครับ',
     'Does this sound natural?'),
    ('แซ่บ', 'sɛ̂ɛp', 'Delicious (Isan word)',
     'แอปสอนว่า "แซ่บ" เป็นคำอีสานที่คนไทยทุกภาคเข้าใจ ถูกต้องไหมครับ',
     'The app says แซ่บ is an Isan word every Thai understands. Fair?'),
    ('คำตอบที่ตั้งใจให้ผิด', '', 'The deliberately wrong (funny) answers',
     'ในแต่ละฉากมีคำตอบผิดที่ใส่ไว้ให้ขำ ๆ เช่น ตอบคนขายว่า "อร่อย" มีข้อไหนที่หยาบหรือไม่สุภาพไหมครับ',
     'Each scene has a deliberately wrong, light-hearted answer. Is any of them rude or embarrassing?'),
]


def both_forms(text):
    """The learner's line as a man says it, then as a woman says it."""
    male = tour_trips.fill_particles(text, 'male')
    female = tour_trips.fill_particles(text, 'female')
    return male if male == female else '{} / {}'.format(male, female)


def both_paiboon(text):
    male = tour_trips.fill_particles(text, 'male', paiboon=True)
    female = tour_trips.fill_particles(text, 'female', paiboon=True)
    return male if male == female else '{} / {}'.format(male, female)


def trip_rows(trip):
    """(who, thai, romanisation, english) for every line worth checking."""
    rows = [('ชื่อสถานที่', trip['place_thai'], trip['place_paiboon'], trip['place_english'])]
    for scene in trip['scenes']:
        if scene['thai']:
            rows.append((scene['who'], scene['thai'], scene['paiboon'], scene['english']))
        for choice in scene['choices']:
            if choice['verdict'] == 'miss':
                continue
            rows.append(('ผู้เรียน (learner)', both_forms(choice['thai']),
                         both_paiboon(choice['paiboon']), choice['english']))
    return rows


INTRO_TH = (
    'เรียน อาจารย์ครับ 🙏\n\n'
    'ผมทำหน้า **"Tour Guide"** ในแอป ThaiBridge ใหม่ ตอนนี้เป็น **การเดินทาง 7 เส้นทาง** '
    'ทั่วประเทศไทย ในแต่ละจุด จะมีคนไทยพูดกับผู้เรียน แล้วผู้เรียนเลือกคำตอบเป็นภาษาไทย\n\n'
    'ประโยคภาษาไทยทั้งหมด **ยังเป็นฉบับร่าง** ผมอยากขอให้อาจารย์ช่วยตรวจว่า '
    'ถูกต้อง เป็นธรรมชาติ และสุภาพพอดีไหมครับ'
)
INTRO_EN = (
    'I have rebuilt the Tour Guide page as seven short trips around Thailand. At each '
    'stop a Thai person speaks to the learner, who picks a reply in Thai. All the Thai '
    'is still a draft. Please check it is correct, natural, and polite enough.'
)
HOW_TH = ('**ส่วน ก** มี 9 คำถามที่ผมไม่แน่ใจ (ประมาณ 10 นาที) **ส่วน ข** เป็นทุกประโยค '
          'ถ้าถูกแล้วทำเครื่องหมาย ✓ ถ้าผิดเขียนคำที่ถูกได้เลยครับ ข้อไหนไม่แน่ใจ ข้ามได้เลยนะครับ')
HOW_EN = ('Part A is nine questions I am unsure about (about 10 minutes). Part B is every '
          'line: tick it if it is fine, or write the correction. Skip anything you are unsure of.')
# The learner-facing name since 2026-10-09; the Paiboon+ credit stays.
SPELLING_TH = ('คำอ่านที่เขียนเป็นตัวอักษรโรมันในแอป เรียกว่า **ThaiBridge Spelling** '
               '(พัฒนาจากระบบ Paiboon+) ถ้าคำอ่านตรงไหนผิด ช่วยแก้ได้เลยครับ')
SPELLING_EN = ('The romanised pronunciation in the app is called ThaiBridge Spelling '
               '(based on Paiboon+). Please correct a reading too if it is wrong.')
PARTICLE_TH = ('ประโยคของผู้เรียนเขียนไว้ 2 แบบ คือ **ผู้ชาย / ผู้หญิง** '
               '(ผู้หญิงใช้ "คะ" เวลาถาม และ "ค่ะ" เวลาบอก)')
PARTICLE_EN = ('Learner lines are shown twice: as a man says it / as a woman says it '
               '(a woman uses คะ on questions and ค่ะ on statements).')


def build_md():
    out = ['# ขอความช่วยเหลือตรวจภาษาไทยในหน้า Tour Guide ครับ',
           '## Tour Guide trips: Thai review · ThaiBridge AI · 2026-10-09', '',
           INTRO_TH, '', '*' + INTRO_EN + '*', '', '> ' + HOW_TH, '>', '> *' + HOW_EN + '*', '', SPELLING_TH, '', '*' + SPELLING_EN + '*', '',
           '---', '', '# ก. คำถามที่ผมไม่แน่ใจ', '## A. Questions I am unsure about', '']
    for n, (thai, pb, en, q_th, q_en) in enumerate(QUESTIONS, 1):
        out += ['### {}. {}'.format(n, thai), '']
        if pb:
            out += ['*{}* · {}'.format(pb, en), '']
        else:
            out += [en, '']
        out += [q_th, '', '*' + q_en + '*', '', '**ตอบ:** ______________________________________________', '']
    out += ['---', '', '# ข. ทุกประโยคในแต่ละเส้นทาง', '## B. Every line, trip by trip', '',
            PARTICLE_TH, '', '*' + PARTICLE_EN + '*', '']
    for n, trip in enumerate(tour_trips.TRIPS, 1):
        out += ['### {}. {} ({})'.format(n, trip['title'], trip['place']), '',
                '| ใครพูด | ภาษาไทย | ThaiBridge Spelling | ความหมาย | ✓ / แก้เป็น |', '|---|---|---|---|---|']
        for who, thai, pb, en in trip_rows(trip):
            out.append('| {} | {} | {} | {} | |'.format(who, thai, pb, en))
        out.append('')
    out += ['---', '', 'ขอบพระคุณมากครับ 🙏', '', '*Thank you very much.*', '']
    return '\n'.join(out)


def md_inline(text):
    """Escape, then turn **bold** into <strong> (the only markup the intro uses)."""
    parts = html.escape(text).split('**')
    return ''.join('<strong>{}</strong>'.format(p) if i % 2 else p for i, p in enumerate(parts))


def build_html():
    e = html.escape
    out = ['<!DOCTYPE html>', '<html lang="th">', '<head>', '<meta charset="utf-8">',
           '<title>ตรวจภาษาไทยในหน้า Tour Guide — ThaiBridge AI</title>', '<style>', CSS, '</style>',
           '</head>', '<body>',
           '<h1>ขอความช่วยเหลือตรวจภาษาไทยในหน้า Tour Guide ครับ</h1>',
           '<p class="sub">Tour Guide trips: Thai review · ThaiBridge AI · 2026-10-09</p>',
           '<div class="intro">']
    for para in INTRO_TH.split('\n\n'):
        out.append('<p>{}</p>'.format(md_inline(para)))
    out += ['<p class="en">{}</p>'.format(e(INTRO_EN)),
            '<p class="time">{}</p>'.format(md_inline(HOW_TH)),
            '<p class="en">{}</p>'.format(e(HOW_EN)),
            '<p>{}</p>'.format(md_inline(SPELLING_TH)),
            '<p class="en">{}</p>'.format(e(SPELLING_EN)), '</div>',
            '<h2 class="part">ก. คำถามที่ผมไม่แน่ใจ · A. Questions I am unsure about</h2>']
    for n, (thai, pb, en, q_th, q_en) in enumerate(QUESTIONS, 1):
        out += ['<div class="q">', '<h3>{}. <span class="thai">{}</span></h3>'.format(n, e(thai))]
        out.append('<p><span class="pb">{}</span>{}</p>'.format(e(pb), (' · ' if pb else '') + e(en)))
        out += ['<p>{}</p>'.format(e(q_th)), '<p class="en">{}</p>'.format(e(q_en)),
                '<p class="answer"><strong>ตอบ:</strong></p>', '</div>']
    out += ['<h2 class="part">ข. ทุกประโยคในแต่ละเส้นทาง · B. Every line, trip by trip</h2>',
            '<p>{}</p>'.format(md_inline(PARTICLE_TH)), '<p class="en">{}</p>'.format(e(PARTICLE_EN))]
    for n, trip in enumerate(tour_trips.TRIPS, 1):
        out += ['<h3 class="trip">{}. {} <span class="place">({})</span></h3>'.format(
                    n, e(trip['title']), e(trip['place'])),
                '<table>', '<tr><th>ใครพูด</th><th>ภาษาไทย</th><th>ThaiBridge Spelling</th>'
                '<th>ความหมาย</th><th class="mark">✓ / แก้เป็น</th></tr>']
        for who, thai, pb, en in trip_rows(trip):
            out.append('<tr><td class="who">{}</td><td class="thai">{}</td><td class="pb">{}</td>'
                       '<td>{}</td><td class="mark"></td></tr>'.format(e(who), e(thai), e(pb), e(en)))
        out.append('</table>')
    out += ['<p class="thanks">ขอบพระคุณมากครับ 🙏 <span class="en">Thank you very much.</span></p>',
            '</body>', '</html>']
    return '\n'.join(out)


# Same look as the vowel sheet, plus a table for Part B. Noto Sans comes
# second so the romanisation's ǎ ǐ ǔ draw properly (see base.css).
CSS = """
  body { font-family: "Noto Sans Thai", "Noto Sans", "Leelawadee UI", Tahoma, "Segoe UI", sans-serif;
         max-width: 56rem; margin: 2rem auto; padding: 0 1.3rem; color: #222;
         line-height: 1.7; font-size: 15px; }
  h1 { font-size: 1.5rem; margin: 0 0 .2rem; color: #7a3b00; }
  .sub { color: #666; margin-top: 0; font-size: .95rem; }
  .en { color: #666; font-size: .89em; font-style: italic; }
  .intro { background: #fff8ee; border: 1px solid #f0d9ad; border-radius: 10px;
           padding: 1rem 1.2rem; margin: 1.2rem 0; }
  .time { background: #fff; border-left: 5px solid #FF9933; border-radius: 0 8px 8px 0;
          padding: .6rem .9rem; margin: .9rem 0 .3rem; }
  h2.part { margin: 2.4rem 0 .6rem; font-size: 1.2rem; color: #fff;
            background: #7a3b00; border-radius: 8px; padding: .5rem .9rem; }
  .q { border: 1px solid #ddd6c9; border-radius: 10px; padding: .8rem 1rem;
       margin: 1rem 0; break-inside: avoid; page-break-inside: avoid; }
  .q h3 { margin: 0 0 .3rem; font-size: 1.1rem; }
  .q p { margin: .25rem 0; }
  .thai { font-size: 1.12em; }
  .pb { color: #8a5a00; font-style: italic; }
  .answer { border-bottom: 1px solid #bbb; padding-bottom: 1.6rem; margin-top: .6rem !important; }
  h3.trip { margin: 2rem 0 .5rem; color: #4A1A6B; font-size: 1.1rem; break-after: avoid; }
  h3.trip .place { color: #888; font-weight: 400; }
  table { border-collapse: collapse; width: 100%; font-size: .92em; }
  th, td { border: 1px solid #ddd6c9; padding: .3rem .45rem; vertical-align: top; text-align: left; }
  th { background: #f6efe2; }
  tr { break-inside: avoid; page-break-inside: avoid; }
  td.who { color: #666; width: 8rem; }
  .mark { width: 9rem; }
  .thanks { margin-top: 2.5rem; font-size: 1.1rem; }
  @media print { body { margin: 0 auto; font-size: 12.5px; } }
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--out', default=os.path.join('docs', 'tour-trips-review-2026-10-09'),
                        help='path without extension; writes .md and .html')
    args = parser.parse_args()
    base = os.path.join(REPO_ROOT, args.out) if not os.path.isabs(args.out) else args.out
    with open(base + '.md', 'w', encoding='utf-8') as f:
        f.write(build_md())
    with open(base + '.html', 'w', encoding='utf-8') as f:
        f.write(build_html())
    rows = sum(len(trip_rows(t)) for t in tour_trips.TRIPS)
    print('Wrote {}.md and .html: {} questions, {} lines across {} trips'.format(
        args.out, len(QUESTIONS), rows, len(tour_trips.TRIPS)))


if __name__ == '__main__':
    main()
