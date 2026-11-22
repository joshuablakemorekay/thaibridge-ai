// The "live lessons: register your interest" box on the pricing page.
// A file, not an inline <script>, so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';
    var box = document.getElementById('live-lessons');
    if (!box) { return; }
    var form = document.getElementById('live-lessons-form');
    var msg  = document.getElementById('live-lessons-message');
    var withdraw = document.getElementById('live-lessons-withdraw');

    function post(url, body) {
        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body || {})
        }).then(function (r) { return r.json(); });
    }

    function done(text) {
        var p = document.createElement('p');
        p.className = 'live-lessons-done';
        p.textContent = text;
        box.querySelector('.live-lessons-body').replaceChildren(p);
    }

    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var picked = form.querySelector('input[name="lesson_format"]:checked');
            var price = form.querySelector('input[name="price_band"]:checked');
            var send = document.getElementById('live-lessons-send');
            send.disabled = true;
            post('/api/live-lessons/interest', {
                lesson_format: picked ? picked.value : 'either',
                price_band: price ? price.value : null,
                note: document.getElementById('live-lessons-note').value
            }).then(function (result) {
                if (result.success) { done(result.message); return; }
                msg.textContent = result.message;
                send.disabled = false;
            }).catch(function () {
                msg.textContent = 'A network error occurred. Please try again.';
                send.disabled = false;
            });
        });
    }

    if (withdraw) {
        withdraw.addEventListener('click', function () {
            withdraw.disabled = true;
            post('/api/live-lessons/interest/withdraw').then(function (result) {
                done(result.message);
            }).catch(function () {
                msg.textContent = 'A network error occurred. Please try again.';
                withdraw.disabled = false;
            });
        });
    }
}());
