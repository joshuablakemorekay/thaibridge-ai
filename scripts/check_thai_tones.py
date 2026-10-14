"""Does the tone mark in each romanisation match the tone the Thai spelling gives?

Thai spelling decides the tone: the class of the first consonant, whether the
syllable is live or dead, and the tone mark. This works that out for a single
Thai syllable and compares it with the tone written in the romanisation.

It only judges what it can read with confidence: a Thai string of ONE syllable
romanised as one syllable, either a whole entry or a space-separated word
inside a phrase. Anything it cannot parse it skips, never guesses. What it
reports is a list to CHECK, not a list of errors: spoken Thai has real
exceptions (ไหม is said mái, ฉัน chán), and those are listed in KNOWN_SPOKEN.

    python scripts/check_thai_tones.py
"""
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from thai_consonants import CONSONANTS, CLASS_HIGH, CLASS_LOW, CLASS_MIDDLE  # noqa: E402

CLASS = {c['char']: {CLASS_MIDDLE: 'mid', CLASS_HIGH: 'high', CLASS_LOW: 'low'}[c['cls']]
         for c in CONSONANTS}
CONS = set(CLASS)

MAI_EK, MAI_THO, MAI_TRI, MAI_JATTAWA = '่', '้', '๊', '๋'
MARKS = {MAI_EK, MAI_THO, MAI_TRI, MAI_JATTAWA}
KARAN = '์'                      # ์ silences the letter under it
LEADING = set('เแโใไ')
LOW_SONORANTS = set('งญนมยรลว')       # a leading ห makes these high class
STOP_FINALS = set('กขคฆจชซฌฎฏฐฑฒดตถทธศษสบปพฟภ')
# Short vowel signs. A syllable whose vowel is short and has no final is dead.
SHORT_SIGNS = set('ะัิึุ็')   # ะ ั ิ ึ ุ ็
LONG_SIGNS = set('าีืู')                # า ี ื ู

# Spoken forms Thai people really use, which the spelling rule does not give.
# Romanising these the spoken way is correct, so they are not reported.
KNOWN_SPOKEN = {
    'ไหม': 'mái', 'ฉัน': 'chán', 'น้ำ': 'náam', 'ก็': 'gɔ̂ɔ', 'เขา': 'káo',
    'หนู': 'nǔu', 'ค่ะ': 'kâ', 'คะ': 'ká', 'นะ': 'ná', 'จ้ะ': 'jâ', 'จ๊ะ': 'já',
    'ไหน': 'nǎi', 'ไหร่': 'rài', 'เพราะ': 'prɔ́', 'เหรอ': 'rə̌ə', 'ละ': 'lá',
    # Spelled with a silent letter this checker cannot see (no ์ mark).
    'บาตร': 'bàat',
}

# Isan words follow Isan tones, not the Central Thai spelling rules. They are
# for a native Isan speaker to judge, so they are listed, not checked.
ISAN = {'เด้อ'}

TONE_OF_MARK = {'̀': 'low', '̂': 'falling', '́': 'high', '̌': 'rising'}


def written_tone(roman):
    """The tone a Paiboon syllable is written with."""
    for ch in unicodedata.normalize('NFD', roman):
        if ch in TONE_OF_MARK:
            return TONE_OF_MARK[ch]
    return 'mid'


def spelled_tone(thai):
    """The tone the spelling of one Thai syllable gives, or None if unsure."""
    s = thai.strip()
    if not s or any(c not in CONS and c not in MARKS and c not in LEADING and c not in
                    SHORT_SIGNS | LONG_SIGNS | {KARAN, 'ำ', 'อ', 'ว', 'ย', 'ร'} for c in s):
        return None
    # Drop a silenced final letter (and the one before ์ in clusters like ์).
    while KARAN in s:
        i = s.index(KARAN)
        s = s[:i - 1] + s[i + 1:]
    lead = s[0] in LEADING
    body = s[1:] if lead else s
    if not body or body[0] not in CONS:
        return None

    # The consonant that decides the class
    first = body[0]
    rest = body[1:]
    cls = CLASS[first]
    if first == 'ห' and rest and rest[0] in LOW_SONORANTS:
        cls, rest = 'high', rest[1:]
    elif first == 'อ' and rest[:1] == 'ย':
        cls, rest = 'mid', rest[1:]
    elif rest[:1] in ('ร', 'ล', 'ว') and len(rest) > 1 and rest[1] not in CONS:
        rest = rest[1:]                          # a cluster: กร, คล, ขว …

    mark = next((c for c in rest if c in MARKS), None)
    rest = ''.join(c for c in rest if c not in MARKS)

    # Vowel length and final consonant
    signs = [c for c in rest if c in SHORT_SIGNS | LONG_SIGNS or c == 'ำ']
    tail = [c for c in rest if c in CONS]
    final = tail[-1] if tail else None
    if 'ำ' in rest or s[0] in 'ใไ' or (s[0] == 'เ' and rest.endswith('า')):
        live, short = True, True                 # ำ ใ ไ เ-า: short but live
    else:
        if rest.endswith('ะ') or (s[0] == 'เ' and rest.endswith('าะ')):
            short = True
            final = None
        elif signs:
            short = signs[0] in SHORT_SIGNS
        elif lead:
            short = False                        # เ- แ- โ- with a final: long
        else:
            short = True                         # implicit o between consonants
            if final == 'อ' or final == 'ว' and not tail[:-1]:
                short = False
        if final in ('อ',) and not signs:
            short, final = False, None           # -อ is the long ɔɔ vowel
        if final is None:
            live = not short
        else:
            live = final not in STOP_FINALS
    # Rules
    if mark:
        table = {
            'mid':  {MAI_EK: 'low', MAI_THO: 'falling', MAI_TRI: 'high', MAI_JATTAWA: 'rising'},
            'high': {MAI_EK: 'low', MAI_THO: 'falling'},
            'low':  {MAI_EK: 'falling', MAI_THO: 'high'},
        }[cls]
        return table.get(mark)
    if live:
        return {'mid': 'mid', 'high': 'rising', 'low': 'mid'}[cls]
    if cls == 'low':
        return 'high' if short else 'falling'
    return 'low'


def pairs(entry_thai, entry_roman):
    """Single-syllable (thai, roman) pairs inside an entry, aligned by spaces."""
    t_words = entry_thai.split()
    r_words = entry_roman.replace(',', ' ').replace('?', ' ').replace('.', ' ').split()
    if len(t_words) != len(r_words):
        return []
    return [(t, r) for t, r in zip(t_words, r_words) if '-' not in r and '~' not in r]


CHECKED = set()


def check(entries):
    """(thai, roman, written, spelled, source) for every disagreement."""
    seen, out = set(), []
    for thai, roman, source in entries:
        for t, r in pairs(thai, roman):
            if (t, r) in seen:
                continue
            seen.add((t, r))
            if t in KNOWN_SPOKEN or t in ISAN:
                continue
            # Bare letters and vowel-chart forms are sound labels, not words.
            if len(t) == 1 or ('อ' in t and r[:1] in 'aeiouɔɛəʉ'):
                continue
            spelled = spelled_tone(t)
            if spelled is None:
                continue
            CHECKED.add(t)
            written = written_tone(r)
            if written != spelled:
                out.append((t, r, written, spelled, source))
    return out


def main():
    os.environ.setdefault('DATABASE_URL', '')
    import paiboon_lookup
    entries = [(e.thai, e.paiboon, e.source) for e in paiboon_lookup.get_index()]
    faults = check(entries)
    for t, r, written, spelled, source in sorted(faults, key=lambda f: f[4]):
        print(f'{t}\t{r}\twritten {written}, spelling gives {spelled}\t({source})')
    print(f'\n{len(CHECKED)} syllables checked, {len(faults)} to check')
    return 1 if faults else 0


if __name__ == '__main__':
    sys.exit(main())
