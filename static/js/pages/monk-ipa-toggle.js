// Moved out of templates/monk_lesson_detail.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    var toggle = document.getElementById('monkIpaToggle');
    if (!toggle) return;
    toggle.addEventListener('change', function () {
        document.querySelectorAll('.monk-ipa').forEach(function (el) {
            el.hidden = !toggle.checked;
        });
    });
})();
