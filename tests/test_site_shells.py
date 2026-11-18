"""The menu: one classic tab-style menu for everyone.

Josh chose (2026-11-18) the classic tab menu from the protected tag
webapp-classic-menu-2026-11-18 over both the grouped learner menu and the
separate visitor "website" menu. These tests guard that choice: visitors and
learners see the same menu, every main page is one tap away, every link
opens, and the later decisions (no Developer Login link) still hold.
"""
import re
import uuid

import pytest

from app import app
from models import User, db

# Every page the classic menu must reach (account links depend on login).
MENU_PAGES = {
    '/', '/instructions', '/alphabet', '/tones-classes', '/vowels_syllables',
    '/read_write', '/paiboon', '/grammar', '/formality', '/gender-examples',
    '/sentences', '/learn', '/lessons', '/tour-guide', '/business-thai',
    '/culture', '/calendar', '/expat2000', '/practising-anywhere',
    '/dhamma-and-culture', '/theravada', '/chanting', '/bob-writings',
    '/journal', '/meditation', '/dictionary', '/chat', '/premium', '/monk-mode',
}


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
def test_a_visitor_gets_the_classic_menu(path):
    nav = _nav(app.test_client().get(path).get_data(as_text=True))
    assert MENU_PAGES <= _hrefs(nav), sorted(MENU_PAGES - _hrefs(nav))
    assert 'href="/signup"' in nav and 'href="/login"' in nav


def test_a_learner_gets_the_same_classic_menu(learner):
    client, name = learner
    nav = _nav(client.get('/').get_data(as_text=True))
    assert MENU_PAGES <= _hrefs(nav), sorted(MENU_PAGES - _hrefs(nav))
    assert name in nav and 'href="/progress"' in nav and 'href="/logout"' in nav


def test_the_retired_menus_are_gone():
    html = app.test_client().get('/').get_data(as_text=True)
    assert 'class="nav-site"' not in html
    assert 'class="site-footer-columns"' not in html
    assert 'href="/developer-login"' not in html


def test_learning_support_is_in_the_menu():
    assert 'id="rs-large"' in _nav(app.test_client().get('/').get_data(as_text=True))


def test_every_menu_link_opens():
    client = app.test_client()
    for href in sorted(_hrefs(_nav(client.get('/').get_data(as_text=True)))):
        assert client.get(href).status_code in (200, 302), href
