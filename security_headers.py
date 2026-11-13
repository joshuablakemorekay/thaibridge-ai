"""Security headers: extra instructions sent with every page, telling the browser what to refuse.

Each one closes a door the browser would otherwise leave open:

  * X-Content-Type-Options: nosniff
        Use the file type the server states. Without it a browser may "sniff" an
        uploaded or mislabelled file and decide it's a script.
  * X-Frame-Options: DENY  +  CSP frame-ancestors 'none'
        No other website may show ThaiBridge inside a frame. That stops
        "clickjacking": an invisible copy of the site laid over a fake button,
        so a learner clicks "Cancel subscription" thinking they clicked
        something else. Two headers because older browsers only know the first.
        Nothing on the site frames its own pages, so 'none' costs nothing.
  * Referrer-Policy: strict-origin-when-cross-origin
        When a learner follows a link to another site (Stripe, 12Go, Wikipedia),
        that site learns only "thaibridge.smoald.com", not the full page address.
  * Permissions-Policy
        Turns off browser features the site never uses (camera API, location,
        payment API), so nothing loaded into a page can ask for them. The
        microphone stays allowed for this site only, for pronunciation practice.
        Photo upload in Translator mode is a file picker, which this doesn't touch.
  * Strict-Transport-Security (live site only)
        After one visit, the browser goes straight to https:// for a year, even
        if someone types http:// or follows an old link. Only sent on Render:
        on http://localhost it would be ignored at best, and at worst teach the
        browser to refuse plain-http localhost for every project on the machine.

NOT here yet: a Content-Security-Policy that controls which scripts may run.
Most pages have their scripts written inline, so a strict policy would block
the site's own code. Moving those scripts into files comes first. See
SECURITY.md, "Known gaps".

Like the other modules this never imports app.py. app.py calls init_app(app).
"""

import os

HSTS_MAX_AGE = 60 * 60 * 24 * 365   # one year, in seconds

HEADERS = {
    'X-Content-Type-Options': 'nosniff',
    'X-Frame-Options': 'DENY',
    'Content-Security-Policy': "frame-ancestors 'none'; base-uri 'self'; object-src 'none'",
    'Referrer-Policy': 'strict-origin-when-cross-origin',
    'Permissions-Policy': 'camera=(), geolocation=(), payment=(), microphone=(self)',
}


def _on_render():
    # Render always sets RENDER=true. Read at call time, not import time, so a
    # test can switch it on without reimporting the app.
    return os.environ.get('RENDER', '').lower() == 'true'


def add_security_headers(response):
    for name, value in HEADERS.items():
        # setdefault: a route that deliberately sets its own value keeps it.
        response.headers.setdefault(name, value)
    if _on_render():
        response.headers.setdefault('Strict-Transport-Security',
                                    f'max-age={HSTS_MAX_AGE}')
    return response


def init_app(app):
    app.after_request(add_security_headers)
