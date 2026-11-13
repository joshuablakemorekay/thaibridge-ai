// Moved out of templates/partials/chanting_layers_js.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// Layer toggles. Pure front-end — the choice is remembered in this browser
// only, nothing is sent to the server. Same approach as Learning Support.
(function () {
    var STORAGE_KEY = 'chanting-hidden-layers';
    var book = document.getElementById('chant-book');
    if (!book) return;

    var hidden;
    try {
        hidden = JSON.parse(localStorage.getItem(STORAGE_KEY)) || [];
    } catch (e) {
        hidden = [];
    }

    function apply() {
        document.querySelectorAll('.layer-toggle').forEach(function (box) {
            var on = hidden.indexOf(box.dataset.layer) === -1;
            box.checked = on;
            book.classList.toggle('hide-' + box.dataset.layer, !on);
        });
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify(hidden));
        } catch (e) { /* private browsing — the page still works */ }
    }

    document.querySelectorAll('.layer-toggle').forEach(function (box) {
        box.addEventListener('change', function () {
            var layer = box.dataset.layer;
            var at = hidden.indexOf(layer);
            if (box.checked) {
                if (at !== -1) hidden.splice(at, 1);
            } else if (at === -1) {
                hidden.push(layer);
            }
            apply();
        });
    });

    apply();
})();
