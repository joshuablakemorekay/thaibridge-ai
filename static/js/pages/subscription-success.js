// Moved out of templates/subscription_success.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// Confetti effect
setTimeout(() => {
    console.log('🎊 Subscription activated! 🎊');
}, 500);
