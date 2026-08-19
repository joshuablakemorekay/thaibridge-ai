"""Survival Thai — the free tier's answer to "I want to speak Thai".

The point of this section is that it is reachable by someone who has paid
nothing, has no account, and has not learned the alphabet. Almost every test
here is really the same test from a different angle: nothing may stand between
a brand-new visitor and these forty-odd phrases.
"""
import pytest

import app as app_module
import curriculum
import survival


@pytest.fixture
def client():
    return app_module.app.test_client()


class TestItIsActuallyFree:
    def test_a_brand_new_visitor_can_read_it(self, client):
        """No account, no payment, no progress — the page must simply open."""
        assert client.get('/survival').status_code == 200

    def test_the_page_is_the_lesson_not_a_locked_notice(self, client):
        # A gate that renders locked.html also returns 200, so status alone
        # proves nothing. Check the actual phrases are on the page.
        body = client.get('/survival').get_data(as_text=True)
        assert 'สวัสดี' in body
        assert 'sà-wàt-dii' in body

    def test_it_does_not_require_the_alphabet(self):
        """The prerequisite that would defeat the whole thing. Every other
        language section demands the alphabet quiz first, which is right for
        reading and wrong for saying hello."""
        assert app_module.SECTION_REQUIREMENTS['survival']['requires_alphabet'] is False

    def test_it_is_free_tier_at_level_one(self):
        requirement = app_module.SECTION_REQUIREMENTS['survival']
        assert requirement['tier'] == 'free'
        assert requirement['level'] == 1

    def test_the_tour_guide_was_not_freed_to_make_room_for_it(self):
        """The reason this is its own section rather than part of Tour Guide.
        If a later change quietly frees Tour Guide, the justification for the
        split is gone and someone should think again."""
        tour = app_module.SECTION_REQUIREMENTS['tour_guide']
        assert tour['tier'] == 'basic', 'Tour Guide is meant to stay paid'


class TestTheContent:
    def test_every_phrase_has_all_three_parts(self):
        for phrase in survival.all_phrases():
            assert phrase['thai'], phrase
            assert phrase['paiboon'], phrase['thai']
            assert phrase['english'], phrase['thai']

    def test_it_is_finishable(self):
        """'Finishable in one sitting' is the design constraint — the free tier
        already had plenty to read and nothing to complete. If this grows into
        a hundred phrases it has stopped being the thing it was for."""
        assert 30 <= len(survival.all_phrases()) <= 70

    def test_the_four_promised_sets_are_there(self):
        assert {s['key'] for s in survival.SETS} == {
            'greetings', 'numbers', 'food', 'directions'}

    def test_no_phrase_is_listed_twice(self):
        thai = [p['thai'] for p in survival.all_phrases()]
        assert len(thai) == len(set(thai))


class TestTheAudioStrings:
    def test_the_placeholder_template_is_not_sent_for_recording(self):
        """'ไป...ครับ/ค่ะ' is a shape, not a sentence — the blank is where a
        place name goes. Recording it would produce nonsense."""
        assert all('...' not in text for text in survival.thai_strings())

    def test_the_bare_particles_are_recorded_on_their_own(self):
        """A learner taps them separately to hear kráp against kâ."""
        strings = survival.thai_strings()
        assert 'ครับ' in strings
        assert 'ค่ะ' in strings

    def test_every_audio_string_is_thai(self):
        for text in survival.thai_strings():
            assert any('฀' <= ch <= '๿' for ch in text), text


class TestHowItIsPresented:
    def test_the_draft_warning_is_shown(self, client):
        """The Thai here has not been through teacher review yet. A learner
        repeating a wrong tone to a real person deserves the warning."""
        body = client.get('/survival').get_data(as_text=True)
        assert 'Draft translations' in body

    def test_both_polite_particles_are_offered(self, client):
        """Picking one would quietly teach half the learners to sound wrong."""
        body = client.get('/survival').get_data(as_text=True)
        assert 'if you are male' in body
        assert 'if you are female' in body

    def test_it_points_at_the_alphabet_as_the_next_step(self, client):
        # The section is a doorway, not a dead end.
        body = client.get('/survival').get_data(as_text=True)
        assert '/alphabet' in body


class TestItIsWiredIntoTheRestOfTheSite:
    def test_it_appears_on_the_public_curriculum_outline(self):
        outline = curriculum.build_outline(app_module)
        free = next(g for g in outline if g['tier'] == 'free')
        assert any(s['id'] == 'survival' for s in free['sections'])

    def test_its_phrases_join_the_paiboon_lookup(self):
        """New content reaches the lookup because the index walks the module,
        not because someone remembered to add it."""
        import paiboon_lookup
        results = paiboon_lookup.search('mai kao jai', limit=5)
        assert any(e.thai == 'ไม่เข้าใจ' for e in results)

    def test_the_home_page_sends_people_here_first(self, client):
        """A free front door nobody can find does nothing. The home page's
        language card used to open on the alphabet — "starts with the 44
        consonants" — which was the wall this section exists to route around."""
        body = client.get('/').get_data(as_text=True)
        assert 'href="/survival"' in body

    def test_it_is_step_one_of_the_language_path(self, client):
        """It is the only step with no prerequisite, so it cannot sit behind
        the alphabet in the path that describes the route."""
        import re
        body = client.get('/').get_data(as_text=True)
        steps = re.findall(r'step-number">(\d+)</div>\s*<h3>([^<]+)', body)
        assert steps, 'the learning path steps could not be found'
        assert steps[0][1].strip() == 'Survival Thai'

    def test_it_is_in_the_learn_sidebar(self, client):
        body = client.get('/survival').get_data(as_text=True)
        assert 'href="/survival"' in body
