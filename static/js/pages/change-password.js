// Moved out of templates/progress.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';
    var form = document.getElementById('change-password-form');
    var msg  = document.getElementById('change-password-message');
    var btn  = document.getElementById('change-password-btn');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        btn.disabled = true;
        try {
            var response = await fetch('/change-password', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({
                    current_password: document.getElementById('current_password').value,
                    new_password:     document.getElementById('new_password').value,
                    confirm_password: document.getElementById('confirm_new_password').value
                })
            });
            var result = await response.json();
            msg.textContent = result.message;
            msg.className = 'change-password-message ' + (result.success ? 'ok' : 'bad');
            if (result.success) { form.reset(); }
        } catch (err) {
            msg.textContent = 'A network error occurred. Please try again.';
            msg.className = 'change-password-message bad';
        }
        btn.disabled = false;
    });
}());
