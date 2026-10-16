"""The login manager and the rate limiter, created before the app exists.

app.py attaches both with init_app(). They live here rather than in app.py so
auth.py can decorate its routes with them without importing app.py.
"""

from flask import request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager

# Flask-Login keeps track of "who is logged in" across requests. It stores only
# the user's id in the (signed) session cookie, then uses the loader in auth.py
# to fetch the full User from the database on each request.
login_manager = LoginManager()
login_manager.login_view = 'auth.login'     # where @login_required sends guests
login_manager.login_message = "Please log in to continue."


# ============================================
# RATE LIMITING (protects the AI spend)
# ============================================

# The daily AI cap counts per SESSION, which is a cookie — so it only slows down
# a person, not a script. Anything that ignores cookies gets a fresh allowance on
# every request, which means the AI endpoints have no floor under them at all.
# These limits are that floor. They are deliberately generous: high enough that
# no real learner will ever notice, low enough that an automated caller cannot
# empty the API credits before anyone spots it.

def _rate_limit_key():
    """Identify the visitor for rate limiting.

    request.remote_addr is useless here: Render serves through Cloudflare, so
    every request arrives wearing a proxy's address. Limiting on that would hand
    all visitors on earth ONE shared quota — the first person to hit the limit
    would lock out everybody, which is worse than having no limit.

    Cloudflare sets CF-Connecting-IP to the real client address no matter how
    many proxies are in the chain, so we prefer it and never have to guess the
    hop count (Render's own edge, plus Cloudflare again when a custom domain is
    proxied). X-Forwarded-For's first entry is the fallback, and remote_addr the
    last resort for local development, where there is no proxy at all.

    Trusting a header sounds careless, so the reason it is safe here: every
    request to the live site arrives through Cloudflare, and Cloudflare
    overwrites CF-Connecting-IP rather than passing on whatever the caller sent.
    A spoofed value never survives the edge. Off Render there is no Cloudflare
    and no limiter worth defeating, so the same trust costs nothing.
    """
    cf = request.headers.get('CF-Connecting-IP')
    if cf:
        return cf.strip()
    forwarded = request.headers.get('X-Forwarded-For')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return get_remote_address()

# In-memory storage is sound here specifically because Render runs this on a
# single worker (the deploy log sets WEB_CONCURRENCY=1). With more workers each
# would keep its own separate tally and the real limit would multiply. If this
# ever scales beyond one worker, this needs a shared store — Postgres is already
# available — so the assumption is written down rather than left implicit.
limiter = Limiter(
    key_func=_rate_limit_key,
    storage_uri="memory://",
    strategy="fixed-window",
)

def _failed_attempt_only(response):
    """Count a request against its limit only when the attempt failed.

    Used on the sign-in routes. A successful login must not consume anyone's
    allowance: this app's users are monks and expats who may well share one
    monastery or guesthouse connection, and charging them for logging in
    correctly would let ordinary use lock the whole building out. Brute force,
    by definition, produces failures — so counting only failures targets the
    attack without touching normal traffic.

    Checks the body, not just the status: /developer-login answers a wrong
    password with a 200 carrying success:false, so status alone would read every
    failed guess as a success and never count it.

    NOT used on /signup. There the abuse to stop is mass account creation, and
    that succeeds every time — counting only failures would miss it entirely.
    """
    if response.status_code != 200:
        return True
    body = response.get_json(silent=True) or {}
    return not body.get('success', False)
