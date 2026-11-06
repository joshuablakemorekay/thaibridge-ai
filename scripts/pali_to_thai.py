"""Romanised Pali -> Thai-script Pali, in the temple chanting book's style.

The Wat Mahathat UK book writes Pali in the "easy-reading" Thai style: every
open short a is written with sara a (ะ), a closed syllable carries mai han-akat
(ั), ṃ is ง, and there is no phinthu. This converter reproduces that style so
the chants taken from Ajarn Owen's book (romanised only) can be given the same
Thai-script line as the rest of the book.

It is checked against the book itself: `python scripts/pali_to_thai.py --check`
converts every romanised line already in chanting.py and reports how many
words come out exactly as the temple book spells them.

A conversion is a draft. Every line it produces for print is flagged for a
monk to check.
"""
import re
import sys
import unicodedata

# Two-letter consonants first.
_CONS = [
    ('kh', 'ข'), ('gh', 'ฆ'), ('ch', 'ฉ'), ('jh', 'ฌ'), ('ṭh', 'ฐ'), ('ḍh', 'ฒ'),
    ('th', 'ถ'), ('dh', 'ธ'), ('ph', 'ผ'), ('bh', 'ภ'),
    ('k', 'ก'), ('g', 'ค'), ('ṅ', 'ง'), ('c', 'จ'), ('j', 'ช'), ('ñ', 'ญ'),
    ('ṭ', 'ฏ'), ('ḍ', 'ฑ'), ('ṇ', 'ณ'), ('t', 'ต'), ('d', 'ท'), ('n', 'น'),
    ('p', 'ป'), ('b', 'พ'), ('m', 'ม'), ('y', 'ย'), ('r', 'ร'), ('l', 'ล'),
    ('v', 'ว'), ('s', 'ส'), ('ṣ', 'ส'), ('h', 'ห'), ('ḷ', 'ฬ'), ('ṃ', 'ṃ'),  # ṣ: a misprint for s in Ajarn Owen's book
]
_VOWELS = ['ā', 'ī', 'ū', 'a', 'i', 'u', 'e', 'o']


def _tokens(word):
    """Split a romanised word into ('C', thai) and ('V', vowel) tokens."""
    out, i = [], 0
    w = word.lower()
    while i < len(w):
        for rom, th in _CONS:
            if w.startswith(rom, i):
                out.append(('C', th))
                i += len(rom)
                break
        else:
            ch = w[i]
            if ch in _VOWELS:
                out.append(('V', ch))
            else:
                out.append(('X', ch))          # punctuation, digits, etc.
            i += 1
    return out


_ABOVE = {'a': '', 'i': 'ิ', 'ī': 'ี', 'u': 'ุ', 'ū': 'ู'}

# The temple book marks a consonant cluster with yamakkan (๎) on its first
# letter: ส๎ม in tasmā, ต๎ว in sutvā, ห๎ม in brahma, ณ๎ห in tuṇhassa.
_YAMAKKAN = '๎'


def _is_cluster(first, second):
    if first == second:
        return False                       # a doubled letter (dhamma) is not one
    if second in 'ยรลว':
        return True
    if second == 'ม' and first in 'สห':
        return True
    return False                           # h-clusters (ตัณหา) are left unmarked


def convert_word(word):
    toks = _tokens(word)
    # Group into syllables: (onset consonants, vowel, coda consonant or None).
    sylls, onset, i = [], [], 0
    pre = []                                    # leading non-letters
    while i < len(toks) and toks[i][0] == 'X':
        pre.append(toks[i][1]); i += 1
    post = []
    j = len(toks)
    while j > i and toks[j - 1][0] == 'X':
        j -= 1
    post = [t[1] for t in toks[j:]]
    toks = toks[i:j]
    if any(t[0] == 'X' for t in toks):
        return None                             # something we do not understand
    k = 0
    while k < len(toks):
        kind, val = toks[k]
        if kind == 'C' and val != 'ṃ':
            onset.append(val); k += 1; continue
        if kind == 'V':
            coda = None
            nxt = toks[k + 1] if k + 1 < len(toks) else None
            nxt2 = toks[k + 2] if k + 2 < len(toks) else None
            if nxt and nxt[0] == 'C' and nxt[1] == 'ṃ':
                coda = 'ง'; k += 2
            elif (nxt and nxt2 and nxt[0] == 'C' and nxt2[0] == 'C'
                  and nxt[1] == 'พ' and nxt2[1] in 'รย'):
                k += 1                          # br/by begin the next syllable: สะพ๎รัห๎มะ
            elif nxt and nxt[0] == 'C' and (nxt2 is None or nxt2[0] == 'C'):
                coda = nxt[1]; k += 2
            else:
                k += 1
            sylls.append((onset or ['อ'], val, coda))
            onset = []
            continue
        if kind == 'C' and val == 'ṃ':          # stray ṃ after a consonant
            return None
    if onset:                                   # word ends in a bare consonant
        if not sylls:
            return None
        o, v, c = sylls[-1]
        if c:
            return None
        sylls[-1] = (o, v, onset[0])
    out = []
    for n, (onset_, v, coda) in enumerate(sylls):
        base = onset_[0]
        pre_e = ''
        if len(onset_) > 1 and _is_cluster(onset_[0], onset_[1]):
            # เ/โ go after a marked cluster's first letter: ท๎เว (dve)
            pre_e = base + _YAMAKKAN
            body = ''.join(onset_[1:])
        else:
            body = base + ''.join(onset_[1:])
        nxt_onset = sylls[n + 1][0][0] if n + 1 < len(sylls) else None
        if coda and coda != 'ง' and nxt_onset and _is_cluster(coda, nxt_onset):
            coda = coda + _YAMAKKAN
        if v in ('e', 'o'):
            out.append(pre_e + ('เ' if v == 'e' else 'โ') + body + (coda or ''))
        elif v == 'ā':
            out.append(pre_e + body + 'า' + (coda or ''))
        elif v == 'a':
            out.append(pre_e + body + ('ั' + coda if coda else 'ะ'))
        else:
            out.append(pre_e + body + _ABOVE[v] + (coda or ''))
    return ''.join(pre) + ''.join(out) + ''.join(post)


def convert(text, plain=False):
    """A romanised Pali line -> Thai script. Unknown words are kept, marked [?].

    `plain` is for Pali printed without diacritics (Ajarn Owen's Kālāma
    Sutta): a word-final m is then read as ṃ. Long vowels cannot be
    recovered from such text, so its lines need a monk's check.
    """
    text = unicodedata.normalize('NFC', text).replace('ṁ', 'ṃ')
    text = re.sub(r"(?<=\w)['’](?=\w)", '', text)      # pun'evaṃ -> punevaṃ
    if plain:
        text = re.sub(r'm(?=\W|$)', 'ṃ', text)           # word-final m is ṃ
    words = []
    for w in text.split():
        # Quote marks inside a word ("namassitabbā”ti") are kept but not
        # converted; a hyphenated compound is converted part by part and
        # joined, as Thai script writes a compound as one word.
        pieces = re.split(r'([“”"‘’]+)', w)
        out = []
        for piece in pieces:
            if not piece or re.fullmatch(r'[“”"‘’]+', piece):
                out.append(piece)
                continue
            parts = [convert_word(x) for x in piece.split('-')]
            out.append(''.join(parts) if all(p is not None for p in parts) else piece + '[?]')
        words.append(''.join(out))
    return ' '.join(words)


def _check():
    sys.path.insert(0, '.')
    import chanting
    good = total = 0
    misses = {}
    for ch in chanting.CHANTS:
        for v in ch.get('verses') or []:
            r, t = v.get('pali_roman', ''), v.get('pali', '')
            rw, tw = r.split(), t.split()
            if not r or len(rw) != len(tw):
                continue
            for a, b in zip(rw, tw):
                b = b.strip('.,;:!?"“”‘’()')
                c = (convert_word(a.strip('.,;:!?"“”‘’()')) or '')
                total += 1
                if c == b:
                    good += 1
                else:
                    misses[(a, b, c)] = misses.get((a, b, c), 0) + 1
    print('words matching the temple book exactly: %d of %d (%.1f%%)' % (good, total, 100 * good / total))
    for (a, b, c), n in sorted(misses.items(), key=lambda x: -x[1])[:40]:
        print('%4d  %-22s book %-18s mine %s' % (n, a, b, c))


if __name__ == '__main__':
    if '--check' in sys.argv:
        _check()
    else:
        print(convert(' '.join(sys.argv[1:])))
