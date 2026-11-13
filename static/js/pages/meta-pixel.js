// Moved out of templates/partials/meta_pixel.html, where it ran as an inline <script>.
// Values from the server now arrive in a JSON block on the page (a
// data block, which never runs), so the Content-Security-Policy can
// refuse inline scripts (see security_headers.py).

(function () {
    var KEY = 'tb-ad-consent';
    var PIXEL_DATA = JSON.parse(document.getElementById('meta-pixel-data').textContent);
    var PIXEL_ID = PIXEL_DATA.id;
    var EVENTS = PIXEL_DATA.events;
    var banner = document.getElementById('tb-consent');

    function readChoice() {
        try { return localStorage.getItem(KEY); } catch (e) { return null; }
    }

    function loadPixel() {
        // Meta's standard loader, unchanged apart from layout.
        !function (f, b, e, v, n, t, s) {
            if (f.fbq) return; n = f.fbq = function () {
                n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
            };
            if (!f._fbq) f._fbq = n; n.push = n; n.loaded = !0; n.version = '2.0';
            n.queue = []; t = b.createElement(e); t.async = !0; t.src = v;
            s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
        }(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', PIXEL_ID);
        fbq('track', 'PageView');
        EVENTS.forEach(function (ev) {
            if (ev.event_id) fbq('track', ev.name, ev.params, { eventID: ev.event_id });
            else fbq('track', ev.name, ev.params);
        });
    }

    function clearMetaCookies() {
        // Meta's first-party cookies, in case the visitor accepted before.
        ['_fbp', '_fbc'].forEach(function (name) {
            var parts = location.hostname.split('.');
            for (var i = 0; i < parts.length - 1; i++) {
                var domain = parts.slice(i).join('.');
                document.cookie = name + '=; Max-Age=0; path=/; domain=.' + domain;
            }
            document.cookie = name + '=; Max-Age=0; path=/';
        });
    }

    window.tbConsent = function (choice) {
        try { localStorage.setItem(KEY, choice); } catch (e) { /* storage off */ }
        banner.hidden = true;
        if (choice === 'granted') loadPixel();
        else clearMetaCookies();
    };

    // The footer's "Cookie choices" link brings the banner back.
    window.tbCookieChoices = function () { banner.hidden = false; };

    var choice = readChoice();
    if (choice === 'granted') loadPixel();
    else if (choice !== 'denied') banner.hidden = false;
})();
