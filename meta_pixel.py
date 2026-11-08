"""The Meta (Facebook/Instagram) Pixel, loaded only after the visitor says yes.

Why it exists: a Meta Sales campaign needs to see sign-ups and purchases
happen on the site, or it has nothing to learn from and won't publish.

Why it waits for consent: the Pixel sets an advertising cookie, and UK cookie
law (PECR) only allows a non-essential cookie once the visitor has agreed. So
nothing from Meta is downloaded at all until "Accept" is pressed in the cookie
banner (templates/partials/meta_pixel.html). The choice is kept in the
visitor's own browser storage.

How a server-side moment (an account was just made, a payment just cleared)
reaches the browser: the route calls queue_event(), which parks the event in
the session, and the next page rendered pops it and hands it to the Pixel. If
the visitor said no, the event is simply thrown away in the browser.

What is sent: the event name, and for a purchase the amount and currency.
Never a name, email, username or anything about what someone is studying.
"""

import os

from flask import session

# Not a secret: it appears in every page's source once the Pixel loads. The
# environment variable is there so it can be switched off (set it to empty)
# without a code change.
PIXEL_ID = os.environ.get('META_PIXEL_ID', '1430901398670197').strip()

QUEUE_KEY = 'meta_pixel_events'


def queue_event(name, event_id=None, **params):
    """Remember a Pixel event to fire on the next page this visitor loads.

    event_id lets Meta drop a duplicate (for example a refreshed thank-you
    page) instead of counting the same purchase twice.
    """
    if not PIXEL_ID:
        return
    events = session.get(QUEUE_KEY, [])
    events.append({'name': name, 'params': params,
                   'event_id': str(event_id) if event_id else None})
    session[QUEUE_KEY] = events[-5:]   # a bound, so it can never grow unchecked
    session.modified = True


def queue_purchase(amount_pence, currency, event_id=None):
    """A completed payment. Amounts arrive in pence; Meta wants pounds."""
    if amount_pence is None:
        return
    queue_event('Purchase', event_id=event_id,
                value=round(amount_pence / 100, 2),
                currency=(currency or 'gbp').upper())


def template_context():
    """For the base template: the Pixel ID and any events waiting to fire."""
    if not PIXEL_ID:
        return {'meta_pixel_id': None, 'meta_pixel_events': []}
    return {'meta_pixel_id': PIXEL_ID,
            'meta_pixel_events': session.pop(QUEUE_KEY, [])}
