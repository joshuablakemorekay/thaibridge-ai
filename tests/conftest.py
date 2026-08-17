"""Pytest configuration for ThaiBridge AI.

Pins the whole test suite to the local SQLite database, whatever the environment
says.

Why this file has to exist: app.py calls load_dotenv() at import time, before it
reads DATABASE_URL. So a .env file — or a DATABASE_URL exported in the shell to
try the live database by hand — would silently point every test at Neon. That is
slow, needs the network, and worst of all it would write test accounts straight
into production data.

Clearing the variable here works because pytest imports conftest.py before it
imports any test module, and the test modules are what pull in app.py (and with
it, the database configuration). Once app.py has been imported the URI is fixed,
so this has to happen first.
"""
import os

# Pop, not set-to-empty: app.py treats any truthy value as "use Postgres".
os.environ.pop('DATABASE_URL', None)

# Turn off rate limiting for the suite. The tests hammer the same endpoints
# hundreds of times in a few seconds, which is precisely the traffic the limits
# exist to block — without this they would start failing with 429s that say
# nothing about whether the code is correct.
os.environ['DISABLE_RATE_LIMITS'] = '1'
