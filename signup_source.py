"""Where a new account came from: remember an ad's tracking tag until sign-up.

Each paid ad links to the site with a tag on the end, for example
    https://thaibridge-ai.smoald.com/?utm_source=tiktok&utm_campaign=chant
Nobody signs up on the page they land on — they read a chant, open the
alphabet, look at the prices — so a tag read only by the sign-up route would
almost always be gone by then. Instead, any page that arrives carrying a tag
puts it in the session, and the sign-up route copies whatever is there onto the
new account.

First tag wins. Someone who arrives from TikTok and later clicks a Facebook ad
in the same browser session counts as TikTok: that is the ad that brought them,
and a later click only shows they were still deciding.

Nothing here identifies a person. The tag names a platform and a campaign, and
it is only ever saved against an account the visitor chose to create.
"""

import re

from flask import request, session
from sqlalchemy import func

from models import User, db

SOURCE_KEY = 'signup_source'
CAMPAIGN_KEY = 'signup_campaign'
MAX_LENGTH = 64   # the width of both User columns


def clean(value):
    """A tag fit to store, or None.

    The value comes straight from a URL anyone can type, so it is cut down to
    lower-case letters, digits, dots, dashes and underscores. "TikTok" and
    "tiktok" become the same platform, and nothing odd reaches the database or
    the report."""
    if not value:
        return None
    value = re.sub(r'[^a-z0-9._-]', '', value.strip().lower())[:MAX_LENGTH]
    return value or None


def remember_tag():
    """Before each request: keep the first ad tag this session arrives with."""
    if request.method != 'GET' or session.get(SOURCE_KEY):
        return
    source = clean(request.args.get('utm_source'))
    if not source:
        return
    session[SOURCE_KEY] = source
    campaign = clean(request.args.get('utm_campaign'))
    if campaign:
        session[CAMPAIGN_KEY] = campaign


def stamp(user):
    """Copy the remembered tag onto a brand-new account (before it is saved)."""
    user.signup_source = session.get(SOURCE_KEY)
    user.signup_campaign = session.get(CAMPAIGN_KEY)


def counts(since=None, until=None):
    """Sign-ups per source, biggest first, as [(source, campaign, n), ...].

    Accounts with no tag come back as source None: people who found the site
    some other way, plus everyone who signed up before this was recorded."""
    query = db.session.query(User.signup_source, User.signup_campaign,
                             func.count(User.id))
    if since is not None:
        query = query.filter(User.created_at >= since)
    if until is not None:
        query = query.filter(User.created_at < until)
    rows = query.group_by(User.signup_source, User.signup_campaign).all()
    return sorted(rows, key=lambda r: (-r[2], r[0] or '', r[1] or ''))


def init_app(app):
    app.before_request(remember_tag)
