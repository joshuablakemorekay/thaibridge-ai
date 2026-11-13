// Moved out of templates/monk_lesson_detail.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    // One Audio object reused for every button. Tapping a second word while the
    // first is still playing should replace it, not talk over it — and a page
    // with 20 separate <audio> elements is needlessly heavy on a phone.
    var player = null;

    document.querySelectorAll('.monk-audio-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            if (player) { player.pause(); }
            player = new Audio(btn.dataset.audio);

            btn.classList.add('is-playing');
            var clear = function () { btn.classList.remove('is-playing'); };
            player.addEventListener('ended', clear);
            // If the file is missing or the browser blocks playback, drop the
            // highlight rather than leaving the button stuck mid-play.
            player.addEventListener('error', clear);
            player.play().catch(clear);
        });
    });
})();
