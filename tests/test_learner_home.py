"""Phase 4 of the website work: "/" is two pages.

A visitor gets the website's front page (index.html). A logged-in learner gets
home_learner.html: their next step, their level and a few ways in. Both come
from the same address, and search engines only ever see the visitor version.
"""
import re
import uuid

import pytest

import app as app_module
from app import app
from models import User, db


@pytest.fixture
def learner():
    tag = uuid.uuid4().hex[:8]
    with app.app_context():
        u = User(username=f"home_{tag}", email=f"home_{tag}@example.com", password_hash="x")
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


def test_a_visitor_still_gets_the_website_front_page():
    html = app.test_client().get('/').get_data(as_text=True)
    assert 'Welcome back' not in html
    assert 'Learn the Dhamma. Learn Thai.' in html


def test_a_learner_gets_their_own_home(learner):
    client, name = learner
    html = client.get('/').get_data(as_text=True)
    assert 'Welcome back, ' + name in html
    assert '<title>Continue learning — Jaiway</title>' in html
    assert 'Your next step' in html
    assert 'Learn the Dhamma. Learn Thai.' not in html


def test_the_next_step_is_a_real_course_section_the_learner_can_open(learner):
    client, _ = learner
    html = client.get('/').get_data(as_text=True)
    # The step comes from learning_path.build_path (the same as /progress);
    # whatever it picks, the button must lead to a real section that opens.
    match = re.search(r'<a href="([^"]+)" class="btn btn-gold">Continue:', html)
    assert match, 'the learner home must offer one clear next step'
    href = match.group(1)
    assert href in {s['url'] for s in app_module._outline_sections()}
    assert client.get(href).status_code == 200


def test_the_level_bar_is_within_range(learner):
    client, _ = learner
    html = client.get('/').get_data(as_text=True)
    value = int(re.search(r'aria-valuenow="(\d+)"', html).group(1))
    assert 0 <= value <= 100


def test_every_link_on_the_learner_home_opens(learner):
    client, _ = learner
    html = client.get('/').get_data(as_text=True)
    main = html.split('<main', 1)[1].split('</main>', 1)[0]
    for href in sorted(set(re.findall(r'href="(/[^"#?]*)', main))):
        assert client.get(href).status_code == 200, href
