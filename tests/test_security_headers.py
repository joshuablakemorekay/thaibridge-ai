"""Security headers on every response (security_headers.py, added 2026-11-13).

Run with:  pytest tests/test_security_headers.py -v
"""
import pytest

import security_headers
from app import app

# One of each kind of response: a page, a JSON API, a static file, a redirect
# and a 404. A header added only to rendered pages would miss the rest.
URLS = ["/", "/api/categories", "/static/css/base.css", "/bob-buddhism-overview",
        "/no-such-page"]


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


@pytest.mark.parametrize("url", URLS)
def test_every_response_carries_the_headers(client, url, monkeypatch):
    monkeypatch.delenv("RENDER", raising=False)
    response = client.get(url)
    for name, value in security_headers.HEADERS.items():
        assert response.headers.get(name) == value, f"{name} missing on {url}"


def test_no_other_site_may_frame_the_pages(client):
    headers = client.get("/").headers
    assert headers["X-Frame-Options"] == "DENY"
    assert "frame-ancestors 'none'" in headers["Content-Security-Policy"]


def test_microphone_stays_allowed_for_pronunciation(client):
    # pronounce.js uses getUserMedia; turning the microphone off would break it.
    assert "microphone=(self)" in client.get("/").headers["Permissions-Policy"]


def test_hsts_only_on_the_live_site(client, monkeypatch):
    monkeypatch.delenv("RENDER", raising=False)
    assert "Strict-Transport-Security" not in client.get("/").headers

    monkeypatch.setenv("RENDER", "true")
    assert client.get("/").headers["Strict-Transport-Security"] == "max-age=31536000"


def test_no_script_policy_yet(client):
    # A script-src rule would block the inline scripts most pages still use.
    # When they move into files this test should change along with the policy.
    csp = client.get("/").headers["Content-Security-Policy"]
    assert "script-src" not in csp and "default-src" not in csp


def test_the_site_never_frames_its_own_pages():
    # frame-ancestors 'none' would break any page that iframes another of ours.
    # Fail loudly if one is ever added, rather than leaving a blank box.
    import pathlib
    root = pathlib.Path(__file__).resolve().parent.parent
    for folder, pattern in (("templates", "*.html"), ("static/js", "*.js")):
        for path in (root / folder).rglob(pattern):
            assert "<iframe" not in path.read_text(encoding="utf-8", errors="ignore"), path
