"""Pytest configuration for ThaiBridge AI.

Pins the whole test suite to the local SQLite database, and switches off rate
limiting, whatever the environment says.

Why DATABASE_URL is set to EMPTY rather than deleted
----------------------------------------------------
app.py calls load_dotenv() at import, before it reads DATABASE_URL. Deleting the
variable here does not help: dotenv sees it missing and loads the real one back
out of .env, so the suite ends up running against the LIVE database — slow,
network-dependent, and writing test accounts into production data.

python-dotenv does not overwrite a variable that is already present, even when
its value is empty. app.py treats an empty value as "not configured" and falls
back to instance/thai_app.db. So an empty string is what actually holds; the
first version of this file popped the variable and quietly did nothing at all.

This runs before any test module imports app, because pytest imports conftest.py
first, and the database URI is fixed at import time.
"""
import os

# Empty, NOT popped. See the note above — popping is silently ineffective.
os.environ["DATABASE_URL"] = ""

# Turn off rate limiting for the suite. The tests hammer the same endpoints
# hundreds of times in a few seconds, which is precisely the traffic the limits
# exist to block — without this they would start failing with 429s that say
# nothing about whether the code is correct.
os.environ["DISABLE_RATE_LIMITS"] = "1"

# ── Signed-in learners ────────────────────────────────────────────────────
#
# Several suites need a client that is past the access gates. They do NOT all
# need the same learner: a test about what a paying subscriber sees must not
# quietly run as a developer with everything unlocked, or it proves nothing.
# So the shared piece is the builder and the defaults, and each test names the
# learner it means.

import pytest  # noqa: E402

from app import app as flask_app  # noqa: E402

UNLOCKED_PROGRESS = {
    "xp": 9999,
    "level": 10,
    "subscription_tier": "pro",
    "is_developer": True,
    "monk_mode": False,
    "full_unlock": True,
    "alphabet_completed": True,
    "sections_unlocked": [],
    "sections_visited": [],
}


@pytest.fixture
def make_client():
    """Build a test client for a learner, described by overrides.

        client = make_client(subscription_tier="basic", is_developer=False)
    """
    def _make(**overrides):
        flask_app.config["TESTING"] = True
        client = flask_app.test_client()
        progress = dict(UNLOCKED_PROGRESS)
        progress.update(overrides)
        with client.session_transaction() as session:
            session["user_progress"] = progress
        return client
    return _make


@pytest.fixture
def unlocked_client(make_client):
    """Everything open — for tests that only need to get past the gate."""
    return make_client()
