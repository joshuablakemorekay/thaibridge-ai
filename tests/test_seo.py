"""Phase 1 of the website work: the search-engine foundations (seo.py).

These guard the promises the public site makes to Google and to link previews:
every listed page really exists and is indexable, private pages never show up
in search, each public page says what it is about, and version-stamped static
files are cached for a long time.
"""
import os
import re

import pytest

import app as app_module
import seo


@pytest.fixture
def client():
    return app_module.app.test_client()


def _description(html):
    m = re.search(r'<meta name="description" content="([^"]*)"', html)
    return m.group(1) if m else None


def test_robots_txt_points_at_the_sitemap(client):
    body = client.get('/robots.txt').get_data(as_text=True)
    assert 'Sitemap: ' + seo.SITE_URL + '/sitemap.xml' in body
    assert 'Disallow: /api/' in body


def test_robots_txt_does_not_block_private_pages():
    # A blocked page is never fetched, so its noindex is never seen and Google
    # can still list the bare address. Private pages rely on noindex instead.
    for prefix in ('/progress', '/login', '/chat'):
        assert not any(prefix.startswith(d) for d in seo.ROBOTS_DISALLOW)


def test_sitemap_lists_the_main_public_pages(client):
    body = client.get('/sitemap.xml').get_data(as_text=True)
    for path in ('/', '/premium', '/survival', '/theravada', '/chanting', '/expat2000'):
        assert '<loc>' + seo.SITE_URL + path + '</loc>' in body


def test_sitemap_includes_journal_entries_and_dhamma_talks():
    paths = seo.sitemap_paths()
    assert any(p.startswith('/journal/') for p in paths)
    assert any(p.startswith('/dhamma-talk/') for p in paths)


@pytest.mark.parametrize('path', seo.sitemap_paths())
def test_every_sitemap_page_opens_and_is_indexable(client, path):
    response = client.get(path)
    assert response.status_code == 200, path
    assert 'noindex' not in response.headers.get('X-Robots-Tag', '')
    html = response.get_data(as_text=True)
    assert 'content="noindex' not in html, path + ' is in the sitemap but asks not to be indexed'
    assert '<link rel="canonical" href="' + seo.SITE_URL + path + '">' in html


def test_public_pages_have_their_own_descriptions(client):
    default = _description(client.get('/progress').get_data(as_text=True))
    seen = {}
    for path in seo.PUBLIC_PATHS:
        desc = _description(client.get(path).get_data(as_text=True))
        assert desc and desc != default, path + ' still uses the site-wide description'
        assert len(desc) <= 175, path + ' description is too long for a search result'
        assert desc not in seen, path + ' repeats the description of ' + str(seen.get(desc))
        seen[desc] = path


@pytest.mark.parametrize('path', ['/progress', '/login', '/search?q=hello', '/chat',
                                  '/forgot-password', '/developer-login'])
def test_private_pages_are_kept_out_of_search(client, path):
    assert client.get(path).headers.get('X-Robots-Tag') == 'noindex'


def test_locked_section_notice_is_kept_out_of_search(client):
    # A logged-out visitor sees the same "Section Locked" notice on many
    # sections; it must not be indexed as if it were each section's content.
    html = client.get('/lessons').get_data(as_text=True)
    assert 'Section Locked' in html
    assert '<meta name="robots" content="noindex, follow">' in html
    assert '/lessons' not in seo.sitemap_paths()


def test_social_preview_tags_point_at_a_real_image(client):
    html = client.get('/').get_data(as_text=True)
    assert '<meta property="og:image" content="' + seo.SITE_URL + '/static/img/brand/social-preview.png">' in html
    assert os.path.exists(os.path.join(app_module.app.static_folder, 'img', 'brand', 'social-preview.png'))
    assert '<meta property="og:title" content="Home - ThaiBridge AI">' in html


def test_version_stamped_static_files_are_cached_for_a_year(client):
    stamped = client.get('/static/css/base.css?v=123')
    assert 'immutable' in stamped.headers.get('Cache-Control', '')
    plain = client.get('/static/css/base.css')
    assert 'immutable' not in plain.headers.get('Cache-Control', '')


# ── Phase 3b: structured data (schema.org JSON-LD) ──────────────────────────

def _ld_blocks(client, path):
    import json
    html = client.get(path).get_data(as_text=True)
    return [json.loads(b) for b in
            re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


def test_home_page_describes_the_organisation_and_site_search(client):
    (data,) = _ld_blocks(client, '/')
    types = {node['@type']: node for node in data['@graph']}
    assert types['Organization']['url'] == seo.SITE_URL + '/'
    action = types['WebSite']['potentialAction']
    assert action['target'] == seo.SITE_URL + '/search?q={search_term_string}'
    # The search address it advertises must really work.
    assert client.get('/search?q=hello').status_code == 200


def test_pricing_page_describes_the_course(client):
    (data,) = _ld_blocks(client, '/premium')
    assert data['@type'] == 'Course' and data['provider']['name'] == 'ThaiBridge'


def test_journal_entries_and_talks_are_articles_with_authors(client):
    import app as app_module
    entry = app_module.JOURNAL_ENTRIES[0]
    (post,) = _ld_blocks(client, '/journal/' + entry['slug'])
    assert post['@type'] == 'BlogPosting' and post['headline'] == entry['title']
    talk = app_module.DHAMMA_TALKS[0]
    (article,) = _ld_blocks(client, '/dhamma-talk/' + talk['slug'])
    assert article['@type'] == 'Article' and article['author']['name'] == talk['speaker']
