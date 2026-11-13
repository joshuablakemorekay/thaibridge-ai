"""Cookie settings and the Monk Mode code limit (added 2026-11-13).

Both were listed as known gaps in SECURITY.md:
  * the login cookies relied on Flask's and the browser's defaults;
  * /monk-mode checked codes with no rate limit, so they could be guessed
    as fast as a script could post them.

The suite normally runs with rate limiting OFF (see conftest.py). The limit
tests run the app in a separate process with limiting left on (see below).

Run with:  pytest tests/test_cookie_and_monk_limits.py -v
"""
import pytest
from werkzeug.exceptions import TooManyRequests

import app as A
from app import app


# --- cookies ----------------------------------------------------------------

def test_login_cookies_are_samesite_lax_and_httponly():
    for prefix in ("SESSION_COOKIE", "REMEMBER_COOKIE"):
        assert app.config[f"{prefix}_SAMESITE"] == "Lax"
        assert app.config[f"{prefix}_HTTPONLY"] is True


def test_secure_flag_follows_render():
    # Off here (no RENDER variable in the suite or CI), on where Render runs.
    # Both cookies must agree, or one would leak over plain http.
    assert app.config["SESSION_COOKIE_SECURE"] == A._ON_RENDER
    assert app.config["REMEMBER_COOKIE_SECURE"] == A._ON_RENDER


def test_the_session_cookie_is_sent_with_samesite_lax():
    client = app.test_client()
    response = client.get("/monk-mode")
    cookies = response.headers.getlist("Set-Cookie")
    session_cookie = [c for c in cookies if c.startswith("session=")]
    assert session_cookie, "the page should start a session"
    assert "SameSite=Lax" in session_cookie[0]
    assert "HttpOnly" in session_cookie[0]


# --- the Monk Mode limit ----------------------------------------------------
#
# The suite runs with rate limiting off, and Flask-Limiter can't be switched
# on afterwards (it never creates its counter storage). So the real limit is
# checked in a separate Python process with limiting left ON, against the
# local database. One process runs all three scenarios to keep it quick.

LIMIT_SCRIPT = r"""
import os, sys
os.environ["DATABASE_URL"] = ""
os.environ.pop("DISABLE_RATE_LIMITS", None)
sys.path.insert(0, os.getcwd())
import app as A
A.is_valid_monk_code = lambda code: code == "right"
c = A.app.test_client()

def post(ip, code):
    r = c.post("/monk-mode", data={"code": code}, headers={"CF-Connecting-IP": ip})
    return r.status_code, r.mimetype, b"Too many codes tried" in r.data

wrong = [post("10.0.0.1", "wrong") for _ in range(6)]
reads = [c.get("/monk-mode", headers={"CF-Connecting-IP": "10.0.0.2"}).status_code
         for _ in range(10)]
right = [post("10.0.0.3", "right")[0] for _ in range(8)] + [post("10.0.0.3", "wrong")[0]]
print(repr({"wrong": wrong, "reads": reads, "right": right}))
"""


@pytest.fixture(scope="module")
def limited_run():
    import ast
    import os
    import subprocess
    import sys
    env = {k: v for k, v in os.environ.items() if k != "DISABLE_RATE_LIMITS"}
    env["DATABASE_URL"] = ""
    env.setdefault("PYTHONIOENCODING", "utf-8")
    out = subprocess.run([sys.executable, "-c", LIMIT_SCRIPT], env=env,
                         cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr[-2000:]
    return ast.literal_eval(out.stdout.strip().splitlines()[-1])


def test_wrong_codes_are_stopped_after_five(limited_run):
    wrong = limited_run["wrong"]
    assert [status for status, _, _ in wrong[:5]] == [200] * 5
    status, mimetype, friendly = wrong[5]
    assert status == 429
    # An ordinary page with a readable message, not raw JSON.
    assert mimetype == "text/html" and friendly


def test_reading_the_page_is_never_limited(limited_run):
    assert limited_run["reads"] == [200] * 10


def test_right_codes_do_not_use_up_the_limit(limited_run):
    # A monastery sharing one connection must not lock itself out by
    # entering correct codes: eight right codes, then a wrong one still
    # gets a normal answer rather than a 429.
    assert limited_run["right"] == [302] * 8 + [200]


def test_only_rejections_count():
    class Response:
        def __init__(self, status):
            self.status_code = status
    assert A._monk_code_rejected(Response(200)) is True     # wrong code, page re-shown
    assert A._monk_code_rejected(Response(302)) is False    # right code, redirected


def test_other_routes_still_get_json_when_limited():
    with app.test_request_context("/api/ai/chat", method="POST"):
        response = A._rate_limit_exceeded(TooManyRequests())
        payload, status = response
        assert status == 429
        assert payload.get_json()["gate"] == "rate_limited"
