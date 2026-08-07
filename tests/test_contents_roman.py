"""Tests for the romanised line under each contents title.

The contents names 286 chants in Thai script and the book prints no Latin
anywhere, so this line is the only way in for a reader who cannot read Thai.
That makes it worth protecting for a reason particular to it: a WRONG
romanisation is invisible to exactly the reader who needs it. Someone who
could tell that Bravinaysaṃkhep is nonsense could have read พระวินัยสังเขป in
the first place and would never have looked at this line.

So the tests here are less about the letters and more about the two rules that
keep the letters honest:

  * a title only gets a Pali reading when it is actually Pali, and
  * one title never has two spellings depending on the page you came in by.
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))

import chanting  # noqa: E402
from romanise_contents import (  # noqa: E402
    contents_titles, is_pali, paiboon_faults, translit_pali, why_not_pali,
)


# ── The transliterator against the only ground truth there is ──────────────

def chants_with_a_pali_title():
    return [c for c in chanting.CHANTS
            if c.get('title_thai') and c.get('title_pali')]


@pytest.mark.parametrize('chant', chants_with_a_pali_title(),
                         ids=lambda c: c['id'])
def test_the_script_reproduces_a_title_someone_already_romanised(chant):
    """The 19 hand-written `title_pali` values are the check on the other 90.

    These were romanised by hand, before this script existed, from the same
    book. If the script can reproduce them character for character it is doing
    the same thing a person did — and where it cannot, the title is irregular
    and belongs in the table by hand rather than being generated.
    """
    title = chant['title_thai']
    if not is_pali(title):
        pytest.skip(f'irregular spelling, romanised by hand: {why_not_pali(title)}')

    def bare(text):
        return text.replace('-', '').replace(' ', '').lower()

    assert bare(translit_pali(title)) == bare(chant['title_pali'])


# ── The classifier ─────────────────────────────────────────────────────────

def test_a_thai_title_is_never_given_a_pali_reading():
    """The failure this whole classifier exists to prevent.

    พระวินัยสังเขป is ordinary Thai — "the Vinaya in summary" — but every
    letter in it is one Pali also uses, so an alphabet check waves it through
    and produces Bravinaysaṃkhep. What actually gives it away is the shape:
    พ against ร is not a cluster Pali has, and Pali words do not end in ป.
    """
    assert not is_pali('พระวินัยสังเขป')
    assert not is_pali('ถวายพรพระ')
    assert not is_pali('อนุโมทนาวิธี')


def test_the_phra_prefix_does_not_read_as_brahma():
    """Pali keeps one r-cluster, in brahma, and admitting it costs more than
    it earns here: it waved through all 42 พระ titles in this contents, none
    of which is brahma."""
    for title in contents_titles():
        if title.startswith('พระ'):
            assert not is_pali(title), f'{title} would be romanised as Pali'


def test_real_pali_titles_are_still_recognised():
    assert is_pali('ระตะนัตตะยัปปะณามะคาถา')
    assert is_pali('ธัมมะจักกัปปะวัตตะนะสุตตัง')
    assert is_pali('ท์วัตติงสาการะปาโฐ')      # cluster written with ์


# ── The two readings of ง ──────────────────────────────────────────────────

def test_a_title_ending_in_ng_ends_in_the_niggahita():
    """suttaṃ, not suttaṅ.

    Thai writes both the guttural nasal and the niggahita as ง, and the two
    are told apart by what follows. At the END of a title nothing follows,
    which is the case a Python `in` check on an empty string silently got
    wrong for every sutta title in the book.
    """
    assert translit_pali('ทะสะธัมมะสุตตัง') == 'Dasadhammasuttaṃ'
    assert translit_pali('มังคะละสุตตัง') == 'Maṅgalasuttaṃ'


def test_ng_before_a_k_class_consonant_is_the_guttural_nasal():
    assert translit_pali('โพชฌังคะปะริตตัง') == 'Bojjhaṅgaparittaṃ'
    assert translit_pali('สังเวคะปะริกิตตะนะปาฐะ') == 'Saṃvegaparikittanapāṭha'


def test_a_bare_vowel_carrier_is_a_syllable_not_a_silent_letter():
    """อ writes no consonant, but it is not nothing: อริยะ is ariya, and
    dropping it left Riyadhanagāthā."""
    assert translit_pali('อริยะธะนะคาถา') == 'Ariyadhanagāthā'


def test_thai_numerals_become_ones_the_reader_can_read():
    """The line exists for someone who cannot read Thai script, and ๕ is Thai
    script."""
    assert translit_pali('อะภิณหะปัจจะเวกขะณะ ๕').endswith(' 5')


# ── The table as the app actually renders it ───────────────────────────────

def test_the_table_and_the_chants_never_spell_one_title_two_ways():
    """A reader can reach the same chant from the contents or from the chant
    page. Being shown two different romanisations of one title would leave
    them unsure they had arrived at the same thing.

    This covers both fields, because both have drifted before: four Pali
    titles carried an undiacriticked `title_roman` (Ratanattayappanamagatha
    against the table's Ratanattayappaṇāmagāthā), and seven Thai titles
    carried an RTGS reading with no tones in it (Kham Bucha Phra Ratanattaya
    against kam buu-chaa prá-rát-dtà-ná-dtrai).
    """
    for chant in chanting.CHANTS:
        title = chant.get('title_thai')
        if not title:
            continue
        table = chanting._CONTENTS_ROMAN.get(title)
        if not table:
            continue                    # a chant the contents does not list
        for field in ('title_pali', 'title_roman'):
            if chant.get(field):
                assert chant[field] == table, (
                    f"{title}: {field} is {chant[field]!r} but the contents "
                    f"prints {table!r}")


def test_every_contents_title_has_a_romanised_line():
    """All 286, with no quiet gaps.

    A contents page where most lines have a way in and some do not reads as
    unfinished rather than as honest, and there is no reason for a gap: a
    title is either Pali, which the script can transliterate, or Thai, which
    is written by hand.
    """
    missing = [t for t in contents_titles()
               if t not in chanting._CONTENTS_ROMAN]
    assert not missing, f'{len(missing)} titles have no romanised line: {missing[:5]}'


# The one title the script cannot read and the table answers by hand: the book
# spells this Pali word in Thai orthography, so it is classified Thai but is
# deliberately romanised as Pali. Named here rather than worked around, so
# that the exception stays a known one and a SECOND exception appearing would
# still fail.
HAND_ROMANISED_AS_PALI = {'เสขิยวัตร'}


@pytest.mark.parametrize('title', [t for t in contents_titles()
                                   if not is_pali(t)
                                   and t not in HAND_ROMANISED_AS_PALI])
def test_the_thai_readings_are_well_formed_paiboon(title):
    """Not that a reading is RIGHT — nothing here can tell you that — but that
    it is a possible Paiboon syllable. It catches a typo and a stray letter,
    which on 177 hand-written lines is worth having."""
    reading = chanting._CONTENTS_ROMAN[title]
    assert not paiboon_faults(reading), f'{title} → {reading}'


def test_the_thai_readings_use_the_paiboon_alphabet():
    """Paiboon writes ŋ, ʉ, ɛ, ɔ, ə and the four tone marks. A reading using
    'ng' or 'ue' would be some other romanisation wearing Paiboon's clothes,
    and inconsistency here is worse than either system alone."""
    for title in contents_titles():
        if is_pali(title) or title in HAND_ROMANISED_AS_PALI:
            continue
        reading = chanting._CONTENTS_ROMAN[title]
        assert 'ng' not in reading, f'{title} → {reading} (Paiboon writes ŋ)'


def test_every_romanised_line_reaches_the_page():
    rows = chanting.build_contents()
    romanised = [r for r in rows if r['title_roman']]
    assert romanised, 'no contents row carries a romanised title'
    for row in romanised:
        assert row['title_roman'].strip() == row['title_roman']


def test_no_line_is_given_a_reading_in_the_wrong_system():
    """IAST is for the Pali titles and Paiboon for the Thai ones, and the
    diacritics are the tell: ṃ ṅ ñ ṭ ḍ ṇ ḷ belong to Pali, so a Thai title
    carrying them is claiming to be Pali.

    Scoped to the table rather than to the rendered row on purpose. A contents
    line can still fall back to a chant's older `title_roman`, and one of those
    — บทพิจารณาสังขาร, 'Botpijārana Saṅkhāra' — is a Thai title written with
    Pali diacritics. That is pre-existing chant data rather than anything this
    table did, and it is fixed by writing the Paiboon entry, not by loosening
    the rule.
    """
    pali_only = set('ṃṅñṭḍṇḷ')
    for title, roman in chanting._CONTENTS_ROMAN.items():
        if not is_pali(title):
            assert not (set(roman) & pali_only), (
                f'{title} is Thai but is romanised as Pali: {roman}')
