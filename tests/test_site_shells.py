"""Phase 2 of the website work: two menus, one layout.

base.html picks the menu by WHO is looking, not by page:

  * a visitor (not logged in) gets the website menu and footer
    (partials/nav_site.html, partials/footer_site.html) — free things to try,
    Pricing, Log in and a "Start free" button;
  * a logged-in learner, or anyone in Monk Mode, gets the learner menu
    (partials/nav_app.html) — AI Tutor, Help and their account.
"""
import re
import uuid

import pytest

from app import app
from models import User, db


def _nav(html):
    return html.split('id="main-nav"', 1)[1].split('</ul>', 1)[0]


def _hrefs(fragment):
    return set(re.findall(r'href="([^"#?]+)', fragment))


@pytest.fixture
def learner():
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"shell_{tag}", email=f"shell_{tag}@example.com", password_hash="x")
        db.session.add(u)
        db.session.commit()
        uid, version, name = u.id, u.session_version or 0, u.username
    client = app.test_client()
    with client.session_transaction() as s:
        s["_user_id"] = f"{uid}:{version}"
        s["_fresh"] = True
    yield client, name
    with app.app_context():
        User.query.filter_by(id=uid).delete()
        db.session.commit()


@pytest.mark.parametrize("path", ["/", "/theravada", "/premium", "/lessons"])
def test_a_visitor_gets_the_website_menu(path):
    html = app.test_client().get(path).get_data(as_text=True)
    nav = _nav(html)
    assert 'class="nav-site"' in html
    assert 'href="/signup" class="nav-cta">Start free</a>' in nav
    assert 'href="/login"' in nav and 'href="/premium"' in nav
    assert 'href="/chat"' not in nav, "the AI Tutor is a learner tool, not a website link"
    assert 'class="site-footer-columns"' in html


@pytest.mark.parametrize("path", ["/", "/theravada", "/premium"])
def test_a_logged_in_learner_gets_the_app_menu(learner, path):
    client, name = learner
    html = client.get(path).get_data(as_text=True)
    nav = _nav(html)
    assert 'class="nav-site"' not in html
    assert 'href="/chat"' in nav and 'href="/progress"' in nav
    assert name in nav
    assert 'Start free' not in nav
    assert 'class="site-footer-columns"' not in html


def test_both_menus_offer_learning_support():
    visitor = app.test_client().get('/').get_data(as_text=True)
    assert 'id="rs-large"' in _nav(visitor)


def test_every_website_link_is_a_page_that_opens():
    client = app.test_client()
    html = client.get('/').get_data(as_text=True)
    footer = html.split('class="site-footer-columns"', 1)[1].split('</div>\n</div>', 1)[0]
    for href in sorted(_hrefs(_nav(html)) | _hrefs(footer)):
        assert client.get(href).status_code == 200, href + ' is linked from the website menu but does not open'
