// Moved out of templates/chanting_page.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// Book layout or verse by verse. Remembered in this browser, because it is a
// standing preference — someone who chants along wants the book every time,
// and someone studying wants the layers every time. Nothing is sent anywhere.
(function () {
    var STORAGE_KEY = 'chanting-page-view';
    var body = document.getElementById('page-body');
    var buttons = document.querySelectorAll('.view-switch button');
    if (!body || !buttons.length) return;

    function show(view) {
        body.classList.toggle('view-book', view === 'book');
        body.classList.toggle('view-study', view === 'study');
        buttons.forEach(function (button) {
            button.setAttribute('aria-pressed', String(button.dataset.view === view));
        });
        try {
            localStorage.setItem(STORAGE_KEY, view);
        } catch (e) { /* private browsing — the page still works */ }
    }

    buttons.forEach(function (button) {
        button.addEventListener('click', function () { show(button.dataset.view); });
    });

    var saved;
    try {
        saved = localStorage.getItem(STORAGE_KEY);
    } catch (e) {
        saved = null;
    }
    // Book layout is the default: the page exists for chanting along.
    show(saved === 'study' ? 'study' : 'book');
})();

// Arrow keys turn the page, the way they would in any reader. Ignored while
// typing in the jump box, so a reader entering "47" is not thrown to another
// page by the arrows on their own keyboard.
(function () {
    var prev = document.querySelector('.page-bar a[rel="prev"]');
    var next = document.querySelector('.page-bar a[rel="next"]');
    if (!prev && !next) return;

    document.addEventListener('keydown', function (event) {
        if (event.metaKey || event.ctrlKey || event.altKey) return;

        var el = document.activeElement;
        var typing = el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA'
                            || el.isContentEditable);
        if (typing) return;

        if (event.key === 'ArrowLeft' && prev) {
            window.location.href = prev.href;
        } else if (event.key === 'ArrowRight' && next) {
            window.location.href = next.href;
        }
    });
})();
