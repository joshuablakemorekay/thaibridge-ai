"""Tests for the public curriculum outline.

The outline makes a promise on a page where a broken promise costs money: it
tells someone exactly what their £9.99 or £19.99 opens, and links to every
page. So the tests here care about two things above all — that the list is
COMPLETE (no section quietly missing) and that every link WORKS (no repeat of
the Culture page's story link, which pointed at a 404 for months).
"""
import pytest

import app as app_module
import curriculum


@pytest.fixture(scope='module')
def outline():
    return curriculum.build_outline(app_module)


@pytest.fixture
def client():
    return app_module.app.test_client()


class TestCompleteness:
    def test_every_section_is_advertised_or_deliberately_excluded(self):
        """The startup assertion, run again as a test so the reason for a
        failure is readable. Adding a section to SECTION_REQUIREMENTS without
        either a route or a recorded exclusion should fail here."""
        curriculum.assert_outline_is_complete(app_module)

    def test_the_exclusions_all_name_real_sections(self):
        # An exclusion that outlives the thing it excluded is dead weight that
        # hides the next genuine gap.
        excluded = set(curriculum.NOT_LEARNING_CONTENT) | set(curriculum.NOT_BUILT_YET)
        assert excluded <= set(app_module.SECTION_REQUIREMENTS)

    def test_the_unbuilt_sections_really_have_no_page(self):
        """greetings_wai and classifiers are priced in SECTION_REQUIREMENTS but
        have no route or template. If someone builds one, this fails — which is
        the reminder to start advertising it."""
        gated = {getattr(view, '_section_id', None)
                 for view in app_module.app.view_functions.values()}
        for section_id in curriculum.NOT_BUILT_YET:
            assert section_id not in gated, (
                f'{section_id} now has a route — remove it from NOT_BUILT_YET '
                f'so it appears on the curriculum outline')

    def test_the_paid_sections_are_shown_not_hidden(self):
        # The entire point: someone deciding whether to pay can see the locked
        # pages. An outline that only listed free sections would be useless.
        tiers = {group['tier'] for group in curriculum.build_outline(app_module)}
        assert 'basic' in tiers
        assert 'pro' in tiers


class TestLinksResolve:
    def test_every_advertised_page_exists(self, outline, client):
        """No advertised page may 404. A locked page is fine — that renders
        locked.html with a 200 and is the honest answer for a paid section."""
        for group in outline:
            for section in group['sections']:
                response = client.get(section['url'])
                assert response.status_code != 404, (
                    f"{group['label']} advertises {section['title']} at "
                    f"{section['url']}, which does not exist")

    def test_no_advertised_page_errors(self, outline, client):
        for group in outline:
            for section in group['sections']:
                response = client.get(section['url'])
                assert response.status_code < 500, (
                    f"{section['url']} raised {response.status_code}")


class TestItStaysInStepWithPricing:
    def test_tier_names_come_from_the_pricing_table(self, outline):
        """The names are read from SUBSCRIPTION_TIERS rather than repeated, so
        renaming a tier cannot leave the outline calling it something else.
        The first draft hardcoded them and invented a tier called 'Fluency'."""
        for group in outline:
            assert group['label'] == app_module.SUBSCRIPTION_TIERS[group['tier']]['name']

    def test_tier_prices_come_from_the_pricing_table(self, outline):
        for group in outline:
            assert group['price'] == app_module.SUBSCRIPTION_TIERS[group['tier']]['price']

    def test_a_section_is_filed_under_the_tier_that_actually_gates_it(self, outline):
        for group in outline:
            for section in group['sections']:
                real_tier = app_module.SECTION_REQUIREMENTS[section['id']]['tier']
                assert real_tier == group['tier']

    def test_pro_carries_its_features_because_it_has_almost_no_pages(self, outline):
        """Pro adds one page (the dictionary) but sells unlimited AI. Without
        the feature list beside the page list, the priciest tier reads as the
        emptiest one."""
        pro = next(g for g in outline if g['tier'] == 'pro')
        assert pro['features'], 'Pro must show what it offers beyond pages'


class TestUrlDiscovery:
    def test_the_chanting_link_goes_to_the_book_not_the_page_index(self, outline):
        """Two views guard 'chanting'. The shortest rule is the front door;
        without that tie-break the winner was whichever Flask registered last,
        which sent people to /chanting/pages."""
        sections = [s for g in outline for s in g['sections'] if s['id'] == 'chanting']
        assert sections and sections[0]['url'] == '/chanting'

    def test_the_ungated_alphabet_still_appears(self, outline):
        """The Alphabet carries no @require_access — it is the free gateway
        every other prerequisite points at — so it can only reach the outline
        through UNDISCOVERABLE_URLS."""
        ids = {s['id'] for g in outline for s in g['sections']}
        assert 'alphabet' in ids


class TestThePage:
    def test_the_outline_is_on_the_premium_page(self, client):
        body = client.get('/premium').get_data(as_text=True)
        assert 'Everything the site teaches' in body

    def test_a_logged_out_visitor_sees_the_paid_sections(self, client):
        # Someone who has not paid is exactly who the outline is for.
        body = client.get('/premium').get_data(as_text=True)
        assert 'Business Thai' in body
        assert 'Thai–English Dictionary' in body
