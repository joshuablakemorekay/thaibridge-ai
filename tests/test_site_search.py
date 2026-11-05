"""Site search: the box under the top menu, and /search.

Most of these guard the two promises in site_search.py's docstring: every
result links somewhere real, and searching gives nothing paid away.
"""
import pytest

import app as app_module
import curriculum
import paiboon_lookup
import site_search


@pytest.fixture
def client():
    return app_module.app.test_client()


def outline():
    return curriculum.build_outline(app_module)


class TestTheBoxIsEverywhere:
    @pytest.mark.parametrize('path', ['/', '/about', '/survival', '/premium'])
    def test_every_page_has_the_search_box(self, client, path):
        body = client.get(path).get_data(as_text=True)
        assert 'action="/search"' in body
        assert 'role="search"' in body

    def test_the_box_has_a_label_a_screen_reader_can_read(self, client):
        body = client.get('/').get_data(as_text=True)
        assert '<label for="site-search-q"' in body

    def test_the_box_keeps_the_query_on_the_results_page(self, client):
        body = client.get('/search?q=grammar').get_data(as_text=True)
        assert 'value="grammar"' in body


class TestPages:
    def test_a_page_is_found_by_name(self):
        urls = [p['url'] for p in site_search.search_pages('grammar', outline())]
        assert urls[0] == '/grammar'

    def test_every_word_must_match_not_any(self):
        """'thai culture' finds Thai Culture, not every page with 'Thai' in it."""
        titles = [p['title'] for p in site_search.search_pages('thai culture', outline())]
        assert titles[0] == 'Thai Culture'
        assert 'Thai Alphabet' not in titles

    def test_a_word_must_start_a_word_not_hide_inside_one(self):
        """'ai' once matched 11 pages because 'Thai' contains it."""
        titles = [p['title'] for p in site_search.search_pages('ai', outline())]
        assert titles[0] == 'AI Tutor'
        assert 'Thai Culture' not in titles
        assert site_search.search_pages('art', outline()) == []   # not via 'start'

    def test_the_start_of_a_word_is_enough(self):
        urls = [p['url'] for p in site_search.search_pages('gram', outline())]
        assert urls == ['/grammar']

    def test_non_lesson_pages_are_found_by_keyword(self):
        urls = [p['url'] for p in site_search.search_pages('refund', outline())]
        assert urls == ['/policies']

    def test_a_locked_page_says_which_plan_opens_it(self, client):
        body = client.get('/search?q=dictionary').get_data(as_text=True)
        assert '🔒 Thai Master (Pro) · level 8' in body

    def test_every_learning_section_is_searchable(self):
        """A new section joins the search the day it joins the outline."""
        searchable = {p['url'] for p in site_search._all_pages(outline())}
        for group in outline():
            for section in group['sections']:
                assert section['url'] in searchable


class TestWords:
    @pytest.mark.parametrize('query', ['hello', 'sawatdii', 'สวัสดี'])
    def test_english_romanisation_and_thai_all_find_hello(self, query):
        thai = [w['thai'] for w in site_search.search_words(query)]
        assert any(t.startswith('สวัสดี') for t in thai), thai

    def test_every_source_links_to_a_page(self):
        """If the word index gains a source, it needs a page to link to."""
        sources = {e.source for e in paiboon_lookup.get_index()}
        missing = sources - set(site_search.SOURCE_URLS)
        assert not missing, missing

    def test_every_source_url_is_a_real_page(self, client):
        for url in set(site_search.SOURCE_URLS.values()):
            path = url.split('#')[0]
            assert client.get(path).status_code in (200, 302), url

    def test_words_give_nothing_the_free_lookup_does_not(self):
        """Word results must be a subset of what free /paiboon already shows."""
        for query in ('hello', 'temple', 'aroi'):
            ours = {(w['thai'], w['paiboon']) for w in site_search.search_words(query)}
            free = {(e.thai, e.paiboon) for e in paiboon_lookup.search(query)}
            assert ours <= free


class TestEdges:
    def test_search_is_free_for_a_new_visitor(self, client):
        response = client.get('/search?q=hello')
        assert response.status_code == 200
        assert 'สวัสดี' in response.get_data(as_text=True)

    def test_an_empty_search_shows_examples_not_an_error(self, client):
        body = client.get('/search').get_data(as_text=True)
        assert 'Type in the search box above' in body

    def test_a_miss_says_so(self, client):
        body = client.get('/search?q=zzqqxx').get_data(as_text=True)
        assert 'No page names match' in body
        assert 'No Thai words match' in body

    def test_the_query_is_escaped(self, client):
        body = client.get('/search?q=<script>alert(1)</script>').get_data(as_text=True)
        assert '<script>alert(1)</script>' not in body

    def test_a_huge_query_is_cut_short(self, client):
        """A 5,000-character search still answers, and only the first
        MAX_QUERY characters are used or echoed back."""
        response = client.get('/search?q=' + 'k' * 5000)
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert 'k' * site_search.MAX_QUERY in body
        assert 'k' * (site_search.MAX_QUERY + 1) not in body
