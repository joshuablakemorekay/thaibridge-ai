// Moved out of templates/base.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    try {
        var s = JSON.parse(localStorage.getItem('tb-reading-support') || '{}');
        var el = document.documentElement;
        if (s.font)    el.classList.add('rs-font');
        if (s.large)   el.classList.add('rs-large');
        if (s.spacing) el.classList.add('rs-spacing');
        if (s.colour)  el.classList.add('rs-colour');
    } catch (e) { /* private mode / storage off: just skip */ }
})();
