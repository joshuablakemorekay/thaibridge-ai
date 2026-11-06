"""Which chant lines are verse, and where they split into half-lines.

Shared by the printed book (scripts/build_chanting_print.py) and the app's
chant pages, so both set the same lines the same way. Josh asked for verse to
be printed in two halves, left and right, as Ajarn Owen's chanting book does
(2026-11-06).
"""
import re

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
