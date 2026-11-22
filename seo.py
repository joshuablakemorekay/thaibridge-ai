"""Search-engine plumbing for the public side of Jaiway.

Everything a search engine needs that is not page content lives here, so the
page templates stay about the page:

  * /sitemap.xml — the pages worth finding, so Google does not have to guess
  * /robots.txt  — where crawlers should not bother going, and where the
    sitemap is
  * an X-Robots-Tag: noindex header on private pages (progress, checkout,
    login, search results...). A header rather than a meta tag so it covers
    every response under those addresses, including ones that never render
    base.html.
  * long browser caching for static files that carry a ?v= version stamp.
    static_v() changes the stamp whenever the file changes, so a cached copy
    can never be stale — without this, every page re-checked the 77KB
    stylesheet with the server.
  * template values for the <head>: the canonical address of the page and the
    absolute address of the social-preview image.

Registered from app.py with init_app(app, dynamic_paths), where dynamic_paths
is a function returning extra public addresses (journal entries, Dhamma talks)
— passed in rather than imported, so this module never imports app.py.
"""
import json
import os

from flask import Blueprint, Response, current_app, request, url_for

bp = Blueprint('seo', __name__)

# The one public address. Pages can also be reached on the old
# thaibridge.smoald.com or thaibridge-ai.smoald.com (both 301-redirect)
# or on Render's own URL; the canonical link tells search engines which
# one to list.
SITE_URL = os.environ.get('SITE_URL', 'https://jaiway.smoald.com').rstrip('/')

# Public pages with real content for a logged-out visitor, in rough order of
# importance. Locked course sections are deliberately NOT here: until they
# show a proper public preview, a logged-out visitor (and Google) only sees the
# same "Section Locked" notice on each, and locked.html marks that noindex.
PUBLIC_PATHS = [
    '/', '/premium', '/survival', '/alphabet', '/expat2000', '/theravada',
    '/chanting', '/chanting/contents', '/meditation', '/practising-anywhere',
    '/dhamma-and-culture', '/bob-writings', '/paiboon', '/calendar', '/journal',
    '/instructions', '/about', '/policies', '/privacy', '/contact', '/signup',
]

# Addresses that should never appear in search results. Prefix match.
NOINDEX_PREFIXES = (
    '/progress', '/login', '/logout', '/forgot-password', '/reset-password',
    '/developer-login', '/account-deleted', '/subscribe', '/subscription-',
    '/addon', '/paypal', '/stripe', '/dana/thanks', '/reviews', '/search',
    '/api/', '/set-', '/chat', '/exercise/',
)

# Crawlers can skip these entirely: machine endpoints and one-click switches.
# Private PAGES are not listed here on purpose — a crawler that is blocked from
# a page never sees its noindex header, so blocked pages can still be listed.
ROBOTS_DISALLOW = ('/api/', '/stripe/', '/paypal/', '/subscribe/', '/set-')

YEAR_IN_SECONDS = 365 * 24 * 60 * 60

DATES_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sitemap_dates.json')

_dynamic_paths = lambda: []  # noqa: E731 — replaced by init_app


def is_noindex(path):
    return path.startswith(NOINDEX_PREFIXES)


def sitemap_paths():
    """Every address listed in the sitemap, without duplicates, in order."""
    seen, out = set(), []
    for path in PUBLIC_PATHS + list(_dynamic_paths()):
        if path not in seen and not is_noindex(path):
            seen.add(path)
            out.append(path)
    return out


@bp.route('/robots.txt')
def robots_txt():
    lines = ['User-agent: *']
    lines += ['Disallow: ' + p for p in ROBOTS_DISALLOW]
    lines += ['', 'Sitemap: ' + SITE_URL + '/sitemap.xml', '']
    return Response('\n'.join(lines), mimetype='text/plain')


def page_dates():
    """When each sitemap page last changed, from sitemap_dates.json.

    Never today's date for every page: that claims the whole site changes
    daily, and Google learns to ignore a lastmod that lies. The file holds the
    git date of each page's own source files instead — see
    scripts/update_sitemap_dates.py. A page missing from it simply gets no
    <lastmod>, which is honest too.
    """
    try:
        with open(DATES_FILE, encoding='utf-8') as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


@bp.route('/sitemap.xml')
def sitemap_xml():
    dates = page_dates()
    urls = ''
    for p in sitemap_paths():
        lastmod = '<lastmod>{}</lastmod>'.format(dates[p]) if p in dates else ''
        urls += '  <url><loc>{}{}</loc>{}</url>\n'.format(SITE_URL, p, lastmod)
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + urls + '</urlset>\n')
    return Response(xml, mimetype='application/xml')


def _after_request(response):
    path = request.path
    if is_noindex(path):
        response.headers['X-Robots-Tag'] = 'noindex'
    if path.startswith('/static/') and request.args.get('v') and response.status_code == 200:
        response.headers['Cache-Control'] = 'public, max-age={}, immutable'.format(YEAR_IN_SECONDS)
    return response


def _template_values():
    return {
        'site_url': SITE_URL,
        'canonical_url': SITE_URL + request.path,
        'social_image_url': SITE_URL + url_for('static', filename='img/brand/social-preview.png'),
    }


def init_app(app, dynamic_paths=None):
    global _dynamic_paths
    if dynamic_paths is not None:
        _dynamic_paths = dynamic_paths
    app.register_blueprint(bp)
    app.after_request(_after_request)
    app.context_processor(_template_values)
