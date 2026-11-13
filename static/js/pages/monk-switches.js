// Moved out of templates/base.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// Turning Monk Mode ON needs a code (handled on the /monk-mode page).
// Turning it OFF needs no code — flip it and reload so every gate
// re-evaluates with the new state.
function turnMonkModeOff() {
    fetch('/set-monk-mode/off')
        .then(function (r) { return r.json(); })
        .then(function () { window.location.reload(); })
        .catch(function () { window.location.reload(); });
}
// Flip the monk lessons between learning Thai and learning English.
function setMonkDirection(dir) {
    fetch('/set-monk-direction/' + dir)
        .then(function (r) { return r.json(); })
        .then(function () { window.location.reload(); })
        .catch(function () { window.location.reload(); });
}
// Flip the English side between British and American.
function setMonkAccent(accent) {
    fetch('/set-monk-accent/' + accent)
        .then(function (r) { return r.json(); })
        .then(function () { window.location.reload(); })
        .catch(function () { window.location.reload(); });
}
