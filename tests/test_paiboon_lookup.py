"""Tests for the Paiboon lookup.

The point of this tool is that a beginner can type what they THINK they heard
and still find the row. So most of what is tested here is the folding: the
spellings a self-taught learner actually produces, checked against the spellings
the corpus actually contains.

The corpus itself is live data, so these tests avoid asserting exact counts or
exact result lists — those would break every time Josh adds a lesson. They
assert relationships instead: this query finds this word, this ordering holds,
a miss stays a miss.
"""
import pytest

import paiboon_lookup as pl


class TestFold:
    """The tight fold: tone marks and IPA letters off, separators dropped."""

    def test_tone_marks_are_stripped(self):
        assert pl.fold('à-rɔ̀i') == 'aroi'

    def test_the_ipa_vowels_flatten_to_typeable_letters(self):
        assert pl.fold('ɔ') == 'o'
        assert pl.fold('ɛ') == 'e'
        assert pl.fold('ɯ') == 'u'
        assert pl.fold('ʉ') == 'u'
        assert pl.fold('ə') == 'e'

    def test_the_eng_is_spelled_out_because_that_is_how_it_is_typed(self):
        # The corpus writes ช้าง both ways; folding has to reconcile them.
        assert pl.fold('cháaŋ') == pl.fold('cháang') == 'chaang'

    def test_hyphens_and_spaces_do_not_matter(self):
        assert pl.fold('kɔ̀ɔp-kun') == pl.fold('kɔ̀ɔp kun') == 'koopkun'

    def test_empty_input_is_safe(self):
        assert pl.fold('') == ''
        assert pl.fold(None) == ''


class TestFoldLoose:
    """The fallback fold: forgives vowel length, vowel quality and RTGS."""

    def test_rtgs_aspirates_reach_the_paiboon_spelling(self):
        # Every road sign in Thailand writes kh/ph/th; Paiboon writes k/p/t.
        assert pl.fold_loose('khop khun') == pl.fold_loose('kɔ̀ɔp-kun')

    def test_the_ee_spelling_reaches_paiboons_ii(self):
        # สวัสดี is sà-wàt-dii, and every beginner types "sawatdee".
        assert pl.fold_loose('sawatdee') == pl.fold_loose('sà-wàt-dii')

    def test_vowel_length_is_forgiven(self):
        assert pl.fold_loose('kop') == pl.fold_loose('kɔ̀ɔp')

    def test_the_bp_and_dt_digraphs_are_forgiven(self):
        # Paiboon's notation for บ and ต, which almost nobody reproduces.
        assert pl.fold_loose('bpai') == pl.fold_loose('pai')
        assert pl.fold_loose('dtòk') == pl.fold_loose('tok')

    def test_unreleased_finals_are_forgiven(self):
        assert pl.fold_loose('khob') == pl.fold_loose('khop')


class TestIndex:
    def test_the_index_is_not_empty(self):
        assert len(pl.get_index()) > 500

    def test_every_entry_carries_both_sides(self):
        # A row with nothing to look up, or nothing to show, is a bug.
        for entry in pl.get_index():
            assert entry.thai, f'entry with no Thai: {entry}'
            assert entry.paiboon, f'entry with no romanisation: {entry.thai}'
            assert entry.source, f'entry with no source: {entry.thai}'

    def test_the_alphabet_is_included(self):
        # thai_consonants.py uses the old field names and needs its own adapter,
        # so it is the most likely source to fall out of the index silently.
        assert any(e.source == 'Alphabet' for e in pl.get_index())

    def test_the_same_word_is_not_listed_twice_for_one_spelling(self):
        # De-duplication is on the FOLDED romanisation, so cháaŋ and cháang
        # count as one row rather than two.
        keys = [(e.thai, e.folded) for e in pl.get_index()]
        assert len(keys) == len(set(keys))

    def test_the_folded_forms_are_precomputed(self):
        entry = pl.Entry('อร่อย', 'à-rɔ̀i', 'delicious', 'Test')
        assert entry.folded == 'aroi'
        assert entry.folded_english == 'delicious'


class TestSearch:
    @pytest.mark.parametrize('query, expected_thai', [
        ('aroi',      'อร่อย'),      # romanisation, typed without tones
        ('sawatdee',  'สวัสดี'),      # the "ee" spelling
        ('khopkhun',  'ขอบคุณ'),     # RTGS aspirates, no spaces
        ('khob khun', 'ขอบคุณ'),     # ...and with a voiced final
        ('elephant',  'ช้าง'),        # English gloss
        ('ไม่เผ็ด',    'ไม่เผ็ด'),      # pasted Thai
    ])
    def test_a_learner_spelling_finds_the_word(self, query, expected_thai):
        results = pl.search(query, limit=5)
        assert results, f'{query!r} found nothing'
        assert results[0].thai == expected_thai

    def test_an_exact_match_outranks_an_incidental_substring(self):
        """Regression: searching "chang" used to return three long sentences
        above ช้าง itself, because "dì-chǎn gam-laŋ …" folds to a string that
        happens to CONTAIN "chang" across a syllable boundary. Ranking is now
        band-major, so an exact hit always beats a substring hit."""
        assert pl.search('chang', limit=5)[0].thai == 'ช้าง'

    def test_the_short_word_beats_the_sentence_containing_it(self):
        results = pl.search('aroi', limit=5)
        assert results[0].thai == 'อร่อย'

    def test_the_fuzzy_band_does_not_pad_a_good_result_set(self):
        """Regression: "aroi" returned five matches, two of which were long
        price sentences — "rɔ́ɔi" (hundred) survives the fuzzy merge and sits
        inside them. A loose SUBSTRING now only counts when nothing precise was
        found anywhere, so a good result set stays clean."""
        results = pl.search('aroi', limit=20)
        assert all('อร่อย' in e.thai for e in results),             [e.thai for e in results]

    def test_the_fuzzy_band_still_rescues_a_query_with_no_precise_hit(self):
        # The other half of the same rule: "sawatdee" matches nothing precisely,
        # so the loose band must still be allowed to answer it in full.
        assert len(pl.search('sawatdee', limit=20)) > 1

    def test_a_word_that_is_not_in_the_corpus_returns_nothing(self):
        """The whole honesty of the tool. A miss must be a miss — never a
        guess, and never a nearest-neighbour dressed up as an answer."""
        assert pl.search('zzzzqqqq') == []

    def test_an_empty_query_returns_nothing(self):
        assert pl.search('') == []
        assert pl.search('   ') == []
        assert pl.search(None) == []

    def test_the_limit_is_respected(self):
        assert len(pl.search('a', limit=5)) <= 5


class TestThePageItself:
    """The lookup is served on /paiboon rather than a route of its own, so
    these guard the wiring as well as the search."""

    @pytest.fixture
    def client(self):
        import app
        return app.app.test_client()

    def test_the_page_loads_for_a_logged_out_visitor(self, client):
        # /paiboon is free and ungated on purpose — a romanisation lookup is
        # no use to a beginner if it is behind the paywall.
        assert client.get('/paiboon').status_code == 200

    def test_the_page_loads_with_no_query(self, client):
        body = client.get('/paiboon').get_data(as_text=True)
        assert 'Look up a word' in body
        assert 'No match for' not in body

    def test_a_search_shows_the_word_and_its_romanisation(self, client):
        body = client.get('/paiboon?q=aroi').get_data(as_text=True)
        assert 'อร่อย' in body
        assert 'à-r' in body            # the tone marks survive to the page

    def test_a_thai_search_works(self, client):
        body = client.get('/paiboon?q=ไม่เผ็ด').get_data(as_text=True)
        assert 'mâi pèt' in body

    def test_a_miss_says_so_plainly(self, client):
        body = client.get('/paiboon?q=zzzzqqqq').get_data(as_text=True)
        assert 'No match for' in body

    def test_a_query_is_escaped_not_injected(self, client):
        # The query is echoed back into the page in three places.
        body = client.get('/paiboon?q=<script>alert(1)</script>').get_data(as_text=True)
        assert '<script>alert(1)</script>' not in body
