// Moved out of templates/signup.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';

    var form      = document.getElementById('signup-form');
    var msgDiv    = document.getElementById('message');
    var submitBtn = document.getElementById('submit-btn');
    var pwdInput  = document.getElementById('password');
    var pwdStrDiv = document.getElementById('password-strength');

    function showMessage(text, type) {
        msgDiv.textContent = text;
        msgDiv.className   = 'message ' + type;
    }

    function clearMessage() {
        msgDiv.className   = 'message';
        msgDiv.textContent = '';
    }

    // Live password strength indicator
    pwdInput.addEventListener('input', function () {
        var val = this.value;
        if (!val) { pwdStrDiv.textContent = ''; return; }

        var strength, cls;
        if (val.length < 8) {
            strength = 'Too short'; cls = 'strength-weak';
        } else if (!/[a-zA-Z]/.test(val) || !/[0-9]/.test(val)) {
            strength = 'Needs a letter and a number'; cls = 'strength-fair';
        } else if (val.length < 12) {
            strength = 'Good'; cls = 'strength-good';
        } else {
            strength = 'Strong'; cls = 'strength-strong';
        }

        pwdStrDiv.textContent = 'Strength: ' + strength;
        pwdStrDiv.className   = 'password-strength ' + cls;
    });

    function validateForm(data) {
        var usernameRe = /^[a-zA-Z0-9_]{3,20}$/;
        var emailRe    = /^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$/;

        if (!data.username || !data.email || !data.password || !data.confirm_password) {
            return 'All fields are required.';
        }
        if (!usernameRe.test(data.username)) {
            return 'Username must be 3\u201320 characters: letters, numbers, and underscores only.';
        }
        if (!emailRe.test(data.email)) {
            return 'Please enter a valid email address.';
        }
        if (data.password.length < 8) {
            return 'Password must be at least 8 characters.';
        }
        if (!/[a-zA-Z]/.test(data.password) || !/[0-9]/.test(data.password)) {
            return 'Password must contain at least one letter and one number.';
        }
        if (data.password !== data.confirm_password) {
            return 'Passwords do not match.';
        }
        return null;
    }

    form.addEventListener('submit', async function (e) {
        e.preventDefault();
        clearMessage();

        var data = {
            username:         document.getElementById('username').value.trim(),
            email:            document.getElementById('email').value.trim(),
            password:         document.getElementById('password').value,
            confirm_password: document.getElementById('confirm-password').value
        };

        var clientError = validateForm(data);
        if (clientError) {
            showMessage(clientError, 'error');
            return;
        }

        submitBtn.disabled    = true;
        submitBtn.textContent = 'Creating account...';

        try {
            var response = await fetch('/signup', {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(data)
            });
            var result = await response.json();

            if (result.success) {
                showMessage(result.message, 'success');
                submitBtn.textContent = 'Account Created!';
                setTimeout(function () {
                    window.location.href = result.redirect || '/';
                }, 1500);
            } else {
                showMessage(result.message, 'error');
                submitBtn.disabled    = false;
                submitBtn.textContent = 'Create My Account';
            }
        } catch (e) {
            showMessage('A network error occurred. Please try again.', 'error');
            submitBtn.disabled    = false;
            submitBtn.textContent = 'Create My Account';
        }
    });
}());
