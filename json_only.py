"""Every POST must be JSON: a site-wide rule against forged requests from other websites.

A form on someone else's website can make a learner's browser POST to
ThaiBridge. That's a "cross-site request forgery" (CSRF). Ordinary forms can
only send a few simple formats, though. To send `Content-Type: application/json`
from another site, the browser must ask ThaiBridge's permission first (a "CORS
preflight"), and ThaiBridge never gives it. So a POST that arrives as JSON came
from ThaiBridge's own pages.

That makes this one rule a second lock on every action, on top of the
SameSite=Lax login cookie (see the COOKIE SETTINGS block in app.py). Before it
existed, five older routes (Monk Mode, developer log-in, dāna, claiming the
earned unlock and cancelling a subscription) took plain form posts, and a few
small APIs accepted any format at all. They all send JSON now, through
static/js/json-forms.js.

The one exception is Stripe's webhook. Stripe isn't a browser, it posts its own
format, and every event is checked against Stripe's signature instead.

Like the other modules this never imports app.py. app.py calls init_app(app).
"""

from flask import jsonify, request

# Endpoints (Flask's names for routes) allowed to receive non-JSON POSTs.
EXEMPT_ENDPOINTS = {'stripe_webhook'}

CHANGING_METHODS = {'POST', 'PUT', 'PATCH', 'DELETE'}


def refuse_non_json():
    if request.method not in CHANGING_METHODS:
        return None
    if request.endpoint in EXEMPT_ENDPOINTS:
        return None
    if request.is_json:
        return None
    return jsonify({
        'success': False,
        'message': 'This request needs to come from a ThaiBridge page. '
                   'Please reload the page and try again.',
    }), 415


def init_app(app):
    app.before_request(refuse_non_json)
