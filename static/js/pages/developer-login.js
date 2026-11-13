// Moved out of templates/developer_login.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

document.getElementById('developer-form').addEventListener('submit', async function(e) {
    e.preventDefault();

    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('message');

    try {
        const response = await fetch('/developer-login', {
            method: 'POST',
            // JSON, like every POST on the site (see json_only.py).
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ password: password })
        });

        const data = await response.json();

        if (data.success) {
            messageDiv.className = 'message success';
            messageDiv.textContent = '✓ ' + data.message;

            setTimeout(() => {
                window.location.href = '/progress';
            }, 1500);
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = '✗ ' + data.message;
            document.getElementById('password').value = '';
        }
    } catch (error) {
        messageDiv.className = 'message error';
        messageDiv.textContent = '✗ An error occurred';
    }
});
