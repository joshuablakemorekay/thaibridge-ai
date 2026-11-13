"""Security headers on every response (security_headers.py, added 2026-11-13).

Run with:  pytest tests/test_security_headers.py -v
"""
import pathlib
import re

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


def test_scripts_only_from_this_site_and_meta(client):
    csp = client.get("/").headers["Content-Security-Policy"]
    script_src = [d.strip() for d in csp.split(";") if d.strip().startswith("script-src")]
    assert script_src == ["script-src 'self' https://connect.facebook.net"]
    # Never re-allow inline code: that would undo the whole policy.
    assert "unsafe-inline" not in csp and "unsafe-eval" not in csp


ROOT = pathlib.Path(__file__).resolve().parent.parent


def _templates():
    return [(p, p.read_text(encoding="utf-8")) for p in (ROOT / "templates").rglob("*.html")]


def test_no_template_has_an_inline_script():
    # The CSP refuses them, so one added later would silently do nothing on the
    # live site. Server values go in <script type="application/json"> blocks.
    for path, text in _templates():
        for attrs in re.findall(r"<script(?![^>]*\bsrc=)([^>]*)>", text):
            assert "application/json" in attrs, f"inline <script> in {path.name}"


def test_no_template_or_script_uses_inline_handlers():
    # onclick="..." is inline code too. Use data-on-click (static/js/actions.js).
    files = _templates() + [(p, p.read_text(encoding="utf-8"))
                            for p in (ROOT / "static" / "js").rglob("*.js")
                            if p.name != "actions.js"]
    for path, text in files:
        assert not re.search(r"""\son[a-z]+\s*=\s*["'`$]""", text), f"inline handler in {path.name}"


def test_the_site_never_frames_its_own_pages():
    # frame-ancestors 'none' would break any page that iframes another of ours.
    # Fail loudly if one is ever added, rather than leaving a blank box.
    root = ROOT
    for folder, pattern in (("templates", "*.html"), ("static/js", "*.js")):
        for path in (root / folder).rglob(pattern):
            assert "<iframe" not in path.read_text(encoding="utf-8", errors="ignore"), path
