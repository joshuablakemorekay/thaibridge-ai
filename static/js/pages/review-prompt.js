// Moved out of templates/progress.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';
    var box     = document.getElementById('review-prompt');
    var form    = document.getElementById('review-form');
    var msg     = document.getElementById('review-message');
    var publish = document.getElementById('review-can-publish');
    var nameBox = document.getElementById('review-name-wrap');

    publish.addEventListener('change', function () { nameBox.hidden = !publish.checked; });

    function post(url, body) {
        return fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body || {})
        });
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        var picked = form.querySelector('input[name="rating"]:checked');
        if (!picked) { msg.textContent = 'Please choose a star rating.'; return; }
        var send = document.getElementById('review-send');
        send.disabled = true;
        try {
            var response = await post('/api/review', {
                rating:       Number(picked.value),
                comment:      document.getElementById('review-comment').value,
                can_publish:  publish.checked,
                display_name: publish.checked ? document.getElementById('review-name').value : ''
            });
            var result = await response.json();
            if (result.success) {
                box.innerHTML = '<h2>🙏 ' + result.message + '</h2>';
                return;
            }
            msg.textContent = result.message;
        } catch (err) {
            msg.textContent = 'A network error occurred. Please try again.';
        }
        send.disabled = false;
    });

    document.getElementById('review-snooze').addEventListener('click', function () {
        post('/api/review/snooze').catch(function () {});
        box.hidden = true;
    });
}());
