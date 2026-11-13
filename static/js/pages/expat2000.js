// Moved out of templates/expat2000.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    // Ticks are a per-visitor convenience, so browser storage is the right
    // home for them. Every read and write is guarded: a private window or
    // blocked storage just means the ticks don't survive a reload.
    var KEY = 'expat2000-ticks';
    var RANKS = [
        [0,   '✈️ Just landed'],
        [15,  '🧳 Finding my feet'],
        [40,  '🛵 Getting the hang of it'],
        [70,  '🏠 Settled in'],
        [100, '🚀 Expat2000 legend']
    ];
    var boxes = Array.prototype.slice.call(document.querySelectorAll('.x2k-do input'));
    var ticks = {};
    try { ticks = JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { ticks = {}; }

    var ring = document.getElementById('x2k-ring-fill');
    var circumference = 2 * Math.PI * 42;
    ring.style.strokeDasharray = circumference;

    function rankFor(pct) {
        var current = RANKS[0], next = null;
        for (var i = 0; i < RANKS.length; i++) {
            if (pct >= RANKS[i][0]) { current = RANKS[i]; next = RANKS[i + 1] || null; }
        }
        return { current: current, next: next };
    }

    function missionDone(key) {
        var mine = boxes.filter(function (b) { return b.dataset.mission === key; });
        return mine.every(function (b) { return b.checked; });
    }

    function render() {
        var done = boxes.filter(function (b) { return b.checked; }).length;
        var pct = boxes.length ? Math.round(done * 100 / boxes.length) : 0;
        ring.style.strokeDashoffset = circumference * (1 - pct / 100);
        document.getElementById('x2k-ring-text').textContent = pct + '%';
        var r = rankFor(pct);
        document.getElementById('x2k-rank').textContent = r.current[1];
        document.getElementById('x2k-rank-next').textContent = r.next
            ? done + ' of ' + boxes.length + ' steps done. Next rank at ' + r.next[0] + '%: ' + r.next[1]
            : 'Every step done. Welcome home. 🙏';

        document.querySelectorAll('.x2k-tile').forEach(function (tile) {
            var key = tile.dataset.mission;
            var mine = boxes.filter(function (b) { return b.dataset.mission === key; });
            var n = mine.filter(function (b) { return b.checked; }).length;
            tile.querySelector('.x2k-tile-count').textContent =
                n === mine.length ? '✓ Complete' : n + ' / ' + mine.length;
            tile.classList.toggle('done', n === mine.length);
        });
    }

    var toastTimer;
    function toast(text) {
        var el = document.getElementById('x2k-toast');
        el.textContent = text;
        el.classList.add('show');
        clearTimeout(toastTimer);
        toastTimer = setTimeout(function () { el.classList.remove('show'); }, 2600);
    }

    boxes.forEach(function (box) {
        box.checked = !!ticks[box.dataset.task];
        box.addEventListener('change', function () {
            if (box.checked) { ticks[box.dataset.task] = true; } else { delete ticks[box.dataset.task]; }
            try { localStorage.setItem(KEY, JSON.stringify(ticks)); } catch (e) {}
            if (box.checked && missionDone(box.dataset.mission)) {
                var title = document.querySelector('#' + box.dataset.mission + ' h2').textContent.trim();
                toast('🎉 Mission complete: ' + title);
            }
            render();
        });
    });
    render();
})();
