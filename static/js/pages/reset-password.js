// Moved out of templates/reset_password.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';

    var form      = document.getElementById('reset-form');
    var msgDiv    = document.getElementById('message');
    var submitBtn = document.getElementById('submit-btn');

    function showMessage(text, type) {
        msgDiv.textContent = text;
        msgDiv.className   = 'message ' + type;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        var data = {
            password:         document.getElementById('password').value,
            confirm_password: document.getElementById('confirm_password').value
        };

        submitBtn.disabled    = true;
        submitBtn.textContent = 'Saving...';

        try {
            // Posts back to this same address, which carries the token.
            var response = await fetch(window.location.pathname, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(data)
            });
            var result = await response.json();
            if (result.success) {
                showMessage(result.message, 'success');
                submitBtn.textContent = 'Saved!';
                setTimeout(function () {
                    window.location.href = result.redirect || '/';
                }, 1200);
                return;
            }
            showMessage(result.message, 'error');
        } catch (e) {
            showMessage('A network error occurred. Please try again.', 'error');
        }
        submitBtn.disabled    = false;
        submitBtn.textContent = 'Save new password';
    });
}());
