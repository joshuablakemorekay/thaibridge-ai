// Moved out of templates/login.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';

    var form      = document.getElementById('login-form');
    var msgDiv    = document.getElementById('message');
    var submitBtn = document.getElementById('submit-btn');

    function showMessage(text, type) {
        msgDiv.textContent = text;
        msgDiv.className   = 'message ' + type;
    }

    function clearMessage() {
        msgDiv.className   = 'message';
        msgDiv.textContent = '';
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        clearMessage();

        var data = {
            identifier: document.getElementById('identifier').value.trim(),
            password:   document.getElementById('password').value
        };

        if (!data.identifier || !data.password) {
            showMessage('Please enter your username/email and password.', 'error');
            return;
        }

        submitBtn.disabled    = true;
        submitBtn.textContent = 'Logging in...';

        try {
            var response = await fetch('/login', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(data)
            });
            var result = await response.json();

            if (result.success) {
                showMessage(result.message, 'success');
                submitBtn.textContent = 'Success!';
                setTimeout(function () {
                    window.location.href = result.redirect || '/';
                }, 1000);
            } else {
                showMessage(result.message, 'error');
                submitBtn.disabled    = false;
                submitBtn.textContent = 'Log In';
            }
        } catch (e) {
            showMessage('A network error occurred. Please try again.', 'error');
            submitBtn.disabled    = false;
            submitBtn.textContent = 'Log In';
        }
    });
}());
