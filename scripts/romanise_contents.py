"""Romanise the chanting book's contents lines — Thai script to Latin.

The contents names 286 chants and the book prints not one letter of Latin
anywhere, so a reader who cannot read Thai script cannot use it at all. This
script produces the romanised line that goes under each title.

TWO SYSTEMS, NEVER MIXED ON ONE LINE
------------------------------------
Most of these titles are PALI written in Thai script, and those get IAST
(Ratanattayappaṇāmagāthā). The rest are ordinary THAI — คำบูชา…, บทขัด…,
ระเบียบ… — and those are not Pali at all, so IAST would be a lie about what
the words are. They get Paiboon, which is what the rest of the app teaches and
which carries the tones IAST has no way to write.

Which one a title gets is decided by the script itself rather than by eye:
Pali-in-Thai-script uses a strict subset of the Thai alphabet. It has no tone
marks, no ศ ษ ซ, no ใ ไ, no ๆ — those letters exist for sounds Pali does not
have. So a title containing any of them cannot be Pali, and a title containing
none of them is. That is a rule a reader can check, which matters more here
than a shorter script: this is hand-transcribed data and the classifier is the
only thing standing between a Thai title and a confidently wrong Pali reading.

The Pali half is fully mechanical — see `translit_pali`. The Thai half cannot
be, because Paiboon needs tone rules and word boundaries, so this script only
REPORTS which titles need Paiboon and leaves the writing of them to the table
in chanting.py.

USAGE
    python scripts/romanise_contents.py              # the whole contents
    python scripts/romanise_contents.py --pali       # only the Pali lines
    python scripts/romanise_contents.py --thai       # only the Thai lines
    python scripts/romanise_contents.py --check      # compare against the
                                                     # table already in
                                                     # chanting.py
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import chanting  # noqa: E402


# ── The Pali alphabet as Thai script writes it ─────────────────────────────
# Pali has 41 sounds and Thai has 44 letters, several of which exist only for
# Thai or for Sanskrit loans. A letter outside this map is the tell that a
# title is not Pali.
CONSONANTS = {
    'ก': 'k',  'ข': 'kh', 'ค': 'g',  'ฆ': 'gh', 'ง': 'ṅ',
    'จ': 'c',  'ฉ': 'ch', 'ช': 'j',  'ฌ': 'jh', 'ญ': 'ñ',
    'ฏ': 'ṭ',  'ฐ': 'ṭh', 'ฑ': 'ḍ',  'ฒ': 'ḍh', 'ณ': 'ṇ',
    'ต': 't',  'ถ': 'th', 'ท': 'd',  'ธ': 'dh', 'น': 'n',
    'ป': 'p',  'ผ': 'ph', 'พ': 'b',  'ภ': 'bh', 'ม': 'm',
    'ย': 'y',  'ร': 'r',  'ล': 'l',  'ว': 'v',
    'ส': 's',  'ห': 'h',  'ฬ': 'ḷ',
    'อ': '',   # the vowel carrier — it writes no sound of its own
}

# Vowel signs that follow their consonant.
VOWELS_AFTER = {
    'ะ': 'a', 'ั': 'a', 'า': 'ā',
    'ิ': 'i', 'ี': 'ī',
    'ุ': 'u', 'ู': 'ū',
}

# Vowel signs written BEFORE the consonant they are pronounced after. Thai
# writes them to the left; the reader says them to the right.
VOWELS_BEFORE = {'เ': 'e', 'โ': 'o'}

# Marks that cancel a vowel rather than write one. Both mean "this consonant
# joins the next" — a cluster, e.g. ท์ว = dv — which is exactly what a bare
# consonant already does in this book's spelling, so both are simply skipped.
SILENT = {'์', 'ฺ'}

NIKKHAHIT = 'ํ'          # the ṃ written as a ring above the letter

THAI_DIGITS = '๐๑๒๓๔๕๖๗๘๙'

# Every character Pali-in-Thai-script is allowed to use. Anything else means
# the title is Thai.
PALI_CHARS = (
    set(CONSONANTS) | set(VOWELS_AFTER) | set(VOWELS_BEFORE)
    | SILENT | {NIKKHAHIT} | set(THAI_DIGITS) | set(' ()-')
)

# Letters that prove a title is NOT Pali, listed so the reason can be shown.
# Tone marks and ศ ษ ซ ฝ ฟ ฎ ด บ ใ ไ ำ ็ ื ึ แ ๆ all write sounds Pali lacks.
NOT_PALI_REASON = {
    '่': 'tone mark', '้': 'tone mark', '๊': 'tone mark', '๋': 'tone mark',
    'ศ': 'Sanskrit sibilant', 'ษ': 'Sanskrit sibilant', 'ซ': 'Thai letter',
    'ฝ': 'Thai letter', 'ฟ': 'Thai letter', 'ฎ': 'Thai letter',
    'ด': 'Thai letter', 'บ': 'Thai letter', 'ฃ': 'Thai letter',
    'ฅ': 'Thai letter', 'ฤ': 'Sanskrit vowel', 'ฦ': 'Sanskrit vowel',
    'ใ': 'Thai vowel', 'ไ': 'Thai vowel', 'แ': 'Thai vowel',
    'ำ': 'Thai vowel', 'ื': 'Thai vowel', 'ึ': 'Thai vowel',
    '็': 'Thai vowel', 'ๆ': 'Thai repetition mark',
}


# The consonant pairs Pali actually allows inside a word. A bare consonant —
# one written with no vowel of its own — has to be the first half of one of
# these, because Pali has no other way to end a syllable.
#
# Doubling of any consonant, and a stop followed by its own aspirate (tt, tth,
# pp, pph …), are generated rather than listed; what remains is the nasal +
# same-class stop series and the short list of genuine oddities.
_SAME_CLASS = [
    ('k', 'kh', 'g', 'gh', 'ṅ'),
    ('c', 'ch', 'j', 'jh', 'ñ'),
    ('ṭ', 'ṭh', 'ḍ', 'ḍh', 'ṇ'),
    ('t', 'th', 'd', 'dh', 'n'),
    ('p', 'ph', 'b', 'bh', 'm'),
]
LEGAL_CONJUNCTS = {(c, c) for row in _SAME_CLASS for c in row}
for _row in _SAME_CLASS:
    *_stops, _nasal = _row
    # tt/tth, dd/ddh … a stop may be followed by itself or its aspirate.
    for _i in (0, 2):
        LEGAL_CONJUNCTS |= {(_row[_i], _row[_i]), (_row[_i], _row[_i + 1])}
    # ṅk, ñc, ṇṭ, nt, mp … a nasal may be followed by any stop of its class.
    LEGAL_CONJUNCTS |= {(_nasal, _stop) for _stop in _stops}
LEGAL_CONJUNCTS |= {
    ('ṇ', 'h'), ('n', 'h'), ('m', 'h'), ('l', 'h'), ('ḷ', 'h'),
    ('y', 'h'), ('v', 'h'), ('s', 'n'), ('s', 'm'), ('s', 'v'),
    ('t', 'v'), ('d', 'v'), ('n', 'y'), ('h', 'm'), ('h', 'v'),
    ('y', 'y'), ('l', 'l'), ('s', 's'), ('m', 'm'), ('n', 'n'),
    # NOT ('b', 'r'). Pali keeps one r-cluster, in brahma, and admitting it
    # here waved through every พระ ("phra") in the book — พระสังคะณี came out
    # as Brasaṅgaṇī rather than Phra Saṅgaṇī. All 42 พร titles in this
    # contents are the Thai word; not one is brahma. If a brahma title is
    # ever entered, it belongs in the hand-written table, not in this rule.
}


def _parse(title):
    """One pass over a title, yielding a token per written unit.

    Both the reading and the checking are built on this. They were once two
    separate walks over the string and they drifted immediately: the checker
    did not carry the before-written vowels (เ and โ sit to the LEFT of the
    consonant they are said after), so it read เม as a bare ม and declared
    half the real Pali titles Thai. Parsing once means a fix to how the script
    is read cannot fail to reach the check.

    Each token is (consonant, vowel, joined) — the vowel being '' where the
    syllable writes none, and `joined` marking a consonant the book has
    explicitly tied to the next with ์ or ฺ (ท์ว, ธ์ย).
    """
    tokens = []
    pending = ''          # a vowel written before its consonant, waiting
    i = 0
    while i < len(title):
        ch = title[i]

        if ch in VOWELS_BEFORE:
            pending = VOWELS_BEFORE[ch]
            i += 1
            continue

        if ch == NIKKHAHIT:
            tokens.append(('', 'ṃ', False))
            i += 1
            continue

        if ch in SILENT:
            i += 1
            continue

        if ch in CONSONANTS:
            joined = i + 1 < len(title) and title[i + 1] in SILENT
            nxt = title[i + 1] if i + 1 < len(title) else ''
            if nxt in VOWELS_AFTER:
                tokens.append((ch, VOWELS_AFTER[nxt], joined))
                i += 2
            elif pending:
                tokens.append((ch, pending, joined))
                pending = ''
                i += 1
            else:
                tokens.append((ch, '', joined))
                i += 1
            continue

        tokens.append((ch, '', False))     # spaces, brackets, Thai numerals
        i += 1
    return tokens


def _syllable_faults(title):
    """Where a title breaks the rules of Pali spelling, described in words.

    This is the test that actually separates Pali from Thai, because the
    alphabet alone does not: พระวินัยสังเขป uses nothing but Pali-legal
    letters and is ordinary Thai. What gives it away is the SHAPE — a bare พ
    against a ร (no such cluster in Pali) and a word ending in ย (Pali words
    end in a vowel or in ṃ). Checking the shape rather than the letters is
    what stops a Thai title being handed a confident, wrong Pali reading.
    """
    faults = []
    tokens = _parse(title)
    for n, (ch, vowel, joined) in enumerate(tokens):
        if vowel or joined or ch not in CONSONANTS:
            continue
        # อ writes no sound of its own and stands for a plain 'a'; ง is the
        # niggahita and is allowed to precede anything at all.
        if ch in 'อง':
            continue

        nxt = tokens[n + 1][0] if n + 1 < len(tokens) else ''
        if nxt in CONSONANTS:
            pair = (CONSONANTS[ch], CONSONANTS[nxt])
            if pair not in LEGAL_CONJUNCTS:
                faults.append(
                    f'{ch}{nxt} ({pair[0]}{pair[1]} is not a Pali cluster)')
        else:
            faults.append(
                f'{ch} (a Pali word cannot end in {CONSONANTS[ch]})')
    return faults


def why_not_pali(title):
    """Everything proving this title is Thai, or [] where it is Pali."""
    letters = {
        f'{ch} ({NOT_PALI_REASON.get(ch, "not a Pali letter")})'
        for ch in title if ch not in PALI_CHARS
    }
    return sorted(letters) + _syllable_faults(title)


def is_pali(title):
    """True where the title is Pali written in Thai script.

    Two tests, and a title has to pass both: every character has to be one
    Pali uses, and every syllable has to be shaped the way Pali spells them.
    """
    return not why_not_pali(title)


def translit_pali(title):
    """One Pali title, Thai script to IAST.

    Mechanical, because this book spells Pali phonetically: every syllable
    writes its vowel (which is why these titles are full of ะ), so a consonant
    with no vowel sign is always the final consonant of the syllable before it
    or the first half of a cluster. That one fact is what makes the whole
    thing decidable without a dictionary.

    The single judgement call is ง, which Thai uses for two different Pali
    sounds: the guttural nasal ṅ and the niggahita ṃ. They are told apart by
    what follows — ง before a k-class consonant is ṅ (saṅgha, maṅgala),
    anywhere else it is ṃ (suttaṃ, saṃvega). Getting this wrong would be
    invisible to a reader who cannot read Thai, which is exactly the reader
    this line is for.
    """
    tokens = _parse(title)
    out = []
    for n, (ch, vowel, _joined) in enumerate(tokens):
        if ch == 'ง':
            nxt = tokens[n + 1][0] if n + 1 < len(tokens) else ''
            # ง carrying its own vowel is a real ṅ syllable, not a nasal
            # ending; only a bare one is the ambiguous case. `nxt and` is
            # load-bearing: at the end of a title nxt is '', and '' in 'กขคฆ'
            # is True in Python, which turned every final ṃ into ṅ (suttaṅ).
            out.append('ṅ' if (vowel or (nxt and nxt in 'กขคฆ')) else 'ṃ')
        elif ch in CONSONANTS:
            out.append(CONSONANTS[ch])
            # อ writes no consonant, so a bare อ is not a silent letter — it is
            # a syllable whose vowel is the unwritten 'a' (อริยะ = ariya).
            # Without this it vanished and left Riyadhanagāthā.
            if ch == 'อ' and not vowel:
                out.append('a')
        elif ch and ch in THAI_DIGITS:
            # `ch and` guards the niggahita token, whose consonant is '' —
            # and '' in '๐๑๒…' is True in Python, which turned every ṃ into a
            # literal 0. Same trap as the final-ง one below it.
            # A romanised line exists for a reader who cannot read Thai
            # script, and ๕ is Thai script.
            out.append(str(THAI_DIGITS.index(ch)))
        else:
            out.append(ch)       # spaces and brackets, the book's own marks
        out.append(vowel)
    roman = ''.join(out)
    return roman[:1].upper() + roman[1:]


# ── Paiboon, for the titles that are Thai rather than Pali ─────────────────
# These cannot be generated: Paiboon needs tone rules and word boundaries, so
# they are written by hand into _CONTENTS_ROMAN. What CAN be checked is
# whether each one is a well-formed Paiboon syllable — which catches a typo or
# a stray letter, though not a wrong reading. On hand-written data that is the
# only mechanical check there is, so it is worth having.

PAIBOON_INITIALS = [
    'bpl', 'bpr', 'dtr', 'gl', 'gr', 'gw', 'kl', 'kr', 'kw', 'pl', 'pr', 'tr',
    'bl', 'br', 'fl', 'fr', 'bp', 'dt', 'ch',
    'b', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'ŋ', 'p', 'r', 's',
    't', 'w', 'y',
    '',                       # a syllable may begin with its vowel (an, ùu)
]
PAIBOON_VOWELS = [
    'ʉʉa', 'uua', 'iia', 'aao', 'aai', 'ɔɔi', 'ooi', 'ɛɛo', 'eeo', 'iao',
    'ɔɔ', 'əə', 'ɛɛ', 'ʉʉ', 'aa', 'ii', 'uu', 'ee', 'oo',
    'ia', 'ʉa', 'ua', 'ai', 'ao', 'ui', 'ɔi', 'oi',
    'a', 'i', 'ʉ', 'u', 'e', 'ɛ', 'o', 'ɔ', 'ə',
]
PAIBOON_FINALS = {'p', 't', 'k', 'm', 'n', 'ŋ', 'i', 'o', 'y', 'w', ''}

# The four tone marks Paiboon writes over the vowel. Stripped before a
# syllable is matched, because they say how it is said, not what it is.
TONE_MARKS = '̀́̂̌'


def paiboon_faults(reading):
    """Where a hand-written Paiboon reading is not a well-formed syllable."""
    import unicodedata

    faults = []
    bare = unicodedata.normalize('NFD', reading)
    bare = ''.join(c for c in bare if c not in TONE_MARKS)

    for word in bare.replace('(', ' ').replace(')', ' ').split():
        for syllable in word.split('-'):
            if not syllable or syllable.isdigit():
                continue
            rest = syllable
            for initial in PAIBOON_INITIALS:
                if rest.startswith(initial):
                    rest = rest[len(initial):]
                    break
            for vowel in PAIBOON_VOWELS:
                if rest.startswith(vowel):
                    rest = rest[len(vowel):]
                    break
            else:
                faults.append(f'{syllable} (no vowel)')
                continue
            if rest not in PAIBOON_FINALS:
                faults.append(f'{syllable} ({rest!r} is not a Paiboon ending)')
    return faults


def contents_titles():
    """Every distinct title the contents prints, in the order it prints them."""
    seen = set()
    titles = []
    for row in chanting.build_contents():
        if row['title'] not in seen:
            seen.add(row['title'])
            titles.append(row['title'])
    return titles


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pali', action='store_true',
                        help='only the titles that are Pali')
    parser.add_argument('--thai', action='store_true',
                        help='only the titles that are Thai, with the reason')
    parser.add_argument('--check', action='store_true',
                        help='compare against the table in chanting.py')
    args = parser.parse_args()

    titles = contents_titles()
    pali = [t for t in titles if is_pali(t)]
    thai = [t for t in titles if not is_pali(t)]

    if args.check:
        return check(titles)

    if not args.thai:
        for title in pali:
            print(f'{title}\t{translit_pali(title)}')

    if not args.pali:
        for title in thai:
            print(f'{title}\tTHAI — {", ".join(why_not_pali(title))}')

    print(
        f'\n{len(titles)} titles: {len(pali)} Pali (IAST, generated above), '
        f'{len(thai)} Thai (Paiboon, written by hand)',
        file=sys.stderr,
    )
    return 0


def check(titles):
    """Compare the generated IAST against what chanting.py actually carries.

    The table in chanting.py is the one that renders, and it is hand-edited
    wherever this script's reading needed correcting. This says where the two
    disagree, so a correction stays visible instead of quietly rotting.
    """
    table = getattr(chanting, '_CONTENTS_ROMAN', {})
    if not table:
        print('chanting.py carries no _CONTENTS_ROMAN table yet.')
        return 1

    missing = [t for t in titles if t not in table]

    # A Pali title whose entry was corrected after the script produced it.
    differs = [
        (t, table[t], translit_pali(t))
        for t in titles
        if is_pali(t) and t in table and table[t] != translit_pali(t)
    ]

    # A title the script calls Thai but which has been romanised as Pali by
    # hand. Worth reporting separately, and easy to miss: an earlier version
    # of this check only compared the titles the script itself calls Pali, so
    # the single override in the table — the one thing --check exists to
    # surface — was the one thing it could not see.
    overridden = [
        (t, table[t]) for t in titles
        if not is_pali(t) and t in table and paiboon_faults(table[t])
    ]

    for title in missing:
        print(f'MISSING   {title}')
    for title, have, generated in differs:
        print(f'EDITED    {title}\n          table:  {have}\n          script: {generated}')
    for title, have in overridden:
        print(f'OVERRIDE  {title}\n          read as Pali by hand: {have}')
        for fault in why_not_pali(title):
            print(f'          script refused it: {fault}')

    print(
        f'\n{len(titles)} titles, {len(missing)} missing, '
        f'{len(differs)} corrected after generation, '
        f'{len(overridden)} romanised as Pali by hand.',
        file=sys.stderr,
    )
    return 1 if missing else 0


if __name__ == '__main__':
    sys.exit(main())
