"""
Guards for the test suite's own safety rails (added 2026-08-17).

conftest.py points the suite at local SQLite and switches rate limiting off.
Both are easy to break by accident and neither announces itself when broken: a
suite running against the live database passes exactly as happily as one running
against SQLite — it is just slower, and quietly writing test accounts into
production.

That is not hypothetical. The first version of conftest.py deleted DATABASE_URL,
which achieved nothing, because app.py calls load_dotenv() at import and loaded
the real value straight back. Every test in this repo ran against the live
database, and the run I did to "prove" the guard worked passed for the wrong
reason.

These tests exist so that cannot happen again silently.

Run with:  pytest tests/test_suite_isolation.py -v
"""

import os

os.environ.setdefault("ANTHROPIC_API_KEY", "test-key")
os.environ.setdefault("FLASK_SECRET_KEY", "test-secret")

from app import app  # noqa: E402


def test_the_suite_is_not_pointed_at_a_remote_database():
    """The one that matters. If this fails, tests are reading and writing real
    user data."""
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    assert uri.startswith("sqlite:///"), (
        f"tests are using {uri.split('://')[0]}, not SQLite — "
        "check conftest.py sets DATABASE_URL to an empty string, not None"
    )


def test_the_database_file_is_the_local_one():
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    assert "instance" in uri and uri.endswith(".db")


def test_rate_limiting_is_off_for_the_suite():
    """Assert on the LIMITER, not the config.

    Checking app.config alone is the trap this file exists to catch: Limiter
    reads RATELIMIT_ENABLED when it is constructed and then keeps its own copy,
    so a config set afterwards reads False while the limiter carries on
    limiting. The first version of this test asserted the config, passed, and
    the suite was rate limited anyway — a test failed several files later
    because earlier tests had spent an allowance that was supposedly off.
    """
    from app import limiter
    assert limiter.enabled is False, (
        "the limiter is still active — RATELIMIT_ENABLED must be set BEFORE "
        "Limiter() is constructed, not after"
    )
    assert app.config.get("RATELIMIT_ENABLED") is False


def test_popping_the_variable_would_not_have_worked():
    """Pins the reasoning, not just the outcome.

    Someone tidying conftest.py could reasonably think `del os.environ[...]` is
    the cleaner way to say the same thing. It is not, and the difference is
    invisible at runtime, so it is written down as an executable fact rather
    than a comment nobody has to read.
    """
    from dotenv import dotenv_values
    configured = dotenv_values(
        os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    )
    if "DATABASE_URL" not in configured:
        # No .env on this machine (CI, a fresh clone) — nothing to be re-loaded,
        # so the trap this guards against cannot spring here.
        return
    assert configured["DATABASE_URL"], (
        ".env defines DATABASE_URL, so deleting it in conftest would let "
        "load_dotenv() restore the live database"
    )
    assert os.environ.get("DATABASE_URL") == "", (
        "conftest must leave DATABASE_URL set-but-empty so load_dotenv() "
        "cannot overwrite it"
    )
