"""Account rules: password checks, reset links and account emails.

The routes that use these live in app.py (/signup, /forgot-password,
/reset-password, /change-password). This module holds the logic behind them,
and like the project's other modules it never imports app.py: app.py imports
it. Anything it needs from the app — the secret key, the request, a way to look
up a user — comes from Flask's request context or is passed in by the caller.

Forgotten passwords are reset by emailed link. The link is a signed, timed
token (itsdangerous, which ships with Flask) rather than a row in a tokens
table. It carries the user id plus a short fingerprint of their CURRENT
password hash. Setting a new password changes the hash, so the fingerprint
stops matching and every outstanding link dies at once. That gives "works only
once" — and "changing your password cancels any reset link someone else
requested" — with no schema change.
"""

import hashlib
import hmac
import logging
import os
import re
import threading

import httpx
from flask import current_app, request
from itsdangerous import BadSignature, URLSafeTimedSerializer

log = logging.getLogger(__name__)

PASSWORD_RESET_MAX_AGE = 30 * 60   # seconds: long enough to find the email, short enough to be stale soon


# ── Password rules ───────────────────────────────────────────────────────

def password_problem(password, confirm_password):
    """The sign-up password rules, shared by every place a password is chosen.
    Returns the message to show, or None when the password is acceptable."""
    if len(password) < 8:
        return 'Password must be at least 8 characters.'
    if not re.search(r'[a-zA-Z]', password) or not re.search(r'[0-9]', password):
        return 'Password must contain at least one letter and one number.'
    if password != confirm_password:
        return 'Passwords do not match.'
    return None


# ── Reset links ──────────────────────────────────────────────────────────

def _serializer():
    # Built per call from the running app's key, so this module needs no app
    # object at import time.
    return URLSafeTimedSerializer(current_app.secret_key, salt='password-reset')


def _password_fingerprint(user):
    return hashlib.sha256(user.password_hash.encode()).hexdigest()[:16]


def make_reset_token(user):
    return _serializer().dumps({'uid': user.id, 'fp': _password_fingerprint(user)})


def user_from_reset_token(token, get_user):
    """The user a reset link belongs to, or None if it is forged, expired or used.

    get_user(user_id) looks the account up. It is passed in because the User
    model lives in app.py, and importing it here would make the two modules
    import each other."""
    try:
        data = _serializer().loads(token, max_age=PASSWORD_RESET_MAX_AGE)
    except BadSignature:   # SignatureExpired is a subclass, so this covers both
        return None
    user = get_user(data.get('uid'))
    if user is None or not hmac.compare_digest(data.get('fp', ''), _password_fingerprint(user)):
        return None
    return user


def public_base_url():
    """Where links in emails should point.

    PUBLIC_BASE_URL on the live site, because behind Render's proxy the
    request's own host can be the internal .onrender.com name, or plain http.
    Unset locally, where the request's own host is exactly right."""
    return (os.environ.get('PUBLIC_BASE_URL') or request.host_url).rstrip('/')


# ── Sending email ────────────────────────────────────────────────────────
#
# Resend (resend.com) sends the email over HTTPS. Settings are read when an
# email is sent rather than at import, because app.py imports its modules
# before it loads .env. No RESEND_API_KEY = no email: the whole email goes to
# the server log instead, so the flow still works on a laptop and nothing
# crashes on a deploy where the key hasn't been added yet.

def send_email(to, subject, text):
    """Send one plain-text email through Resend. Never raises: every caller's
    reply must be the same whether or not the email went, so a delivery failure
    is logged, not shown."""
    key = os.environ.get('RESEND_API_KEY')
    if not key:
        log.warning("RESEND_API_KEY not set; email to %s not sent.\n%s\n\n%s",
                    to, subject, text)
        return
    sender = os.environ.get('PASSWORD_RESET_FROM', 'ThaiBridge AI <no-reply@smoald.com>')
    try:
        resp = httpx.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {key}"},
            json={"from": sender, "to": [to], "subject": subject, "text": text},
            timeout=20,
        )
        resp.raise_for_status()
    except Exception:
        log.exception("Email to %s (%s) failed", to, subject)


def send_in_background(to, subject, text):
    """Send without making the request wait for Resend.

    This is what keeps /forgot-password honest. Its reply text is the same for
    known and unknown emails, but if a known email also waited half a second
    for Resend, timing the reply would still reveal who has an account. A
    thread is enough here: Render runs one worker, and a lost email is
    recoverable — the person just asks again."""
    threading.Thread(target=send_email, args=(to, subject, text), daemon=True).start()


def send_reset_email(user, link):
    send_in_background(user.email, "Reset your ThaiBridge AI password", (
        f"Hi {user.username},\n\n"
        "Someone asked to reset the password for your ThaiBridge AI account. "
        "If that was you, choose a new password here:\n\n"
        f"{link}\n\n"
        "The link works once and expires in 30 minutes.\n\n"
        "If you didn't ask for this, you can ignore this email. "
        "Your password hasn't changed.\n\n"
        "ThaiBridge AI"
    ))


def send_changed_email(user, forgot_link):
    """Tell the owner their password changed, so a change they didn't make is
    noticed by the one person able to act on it."""
    send_in_background(user.email, "Your ThaiBridge AI password was changed", (
        f"Hi {user.username},\n\n"
        "The password for your ThaiBridge AI account was just changed.\n\n"
        "If that was you, there's nothing more to do.\n\n"
        f"If it wasn't, reset it now at {forgot_link} "
        "and email joshua@smoald.com so we can help.\n\n"
        "ThaiBridge AI"
    ))
