// Moved out of templates/forgot_password.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';

    var form      = document.getElementById('forgot-form');
    var msgDiv    = document.getElementById('message');
    var submitBtn = document.getElementById('submit-btn');

    function showMessage(text, type) {
        msgDiv.textContent = text;
        msgDiv.className   = 'message ' + type;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        var email = document.getElementById('email').value.trim();
        if (!email) {
            showMessage('Please enter your email address.', 'error');
            return;
        }

        submitBtn.disabled    = true;
        submitBtn.textContent = 'Sending...';

        try {
            var response = await fetch('/forgot-password', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify({ email: email })
            });
            var result = await response.json();
            if (result.success) {
                showMessage(result.message, 'success');
                form.style.display = 'none';
                return;
            }
            showMessage(result.message, 'error');
        } catch (e) {
            showMessage('A network error occurred. Please try again.', 'error');
        }
        submitBtn.disabled    = false;
        submitBtn.textContent = 'Send reset link';
    });
}());
