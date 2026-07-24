/* Read & Write Thai Script page.
   =============================

   Plain JavaScript, no build step, no libraries — the same constraints as the
   Alphabet page it sits next to. Four things this file does:

     1. Tabs — show one panel at a time (Syllables / Words / Story / Write).
     2. Reveal cards — tap a syllable or word to check your reading.
     3. Story reader — render the Jataka tale one tappable word at a time, and
        gloss the tapped word below.
     4. Trace canvas — draw over a faded letter to practise forming it.

   Audio reuses the site-wide `.th-audio` player in base.js (an element with
   class th-audio and a data-audio="<url>" plays that clip on tap), so this file
   never creates an Audio object of its own — one player for the whole page,
   which is what iOS needs. */

(function () {
    'use strict';

    var CONFIG = window.RW_CONFIG || {};

    function byId(id) { return document.getElementById(id); }
    function readJSON(id) {
        var el = byId(id);
        return el ? JSON.parse(el.textContent) : null;
    }

    /* ── Tabs ──────────────────────────────────────────────────
       Clicking a tab shows its panel and hides the rest. A callback fires when
       a panel becomes visible, which the trace canvas uses to size itself (a
       canvas inside a display:none panel has no size until it is shown). */

    function setupTabs(onShow) {
        var tabs = Array.prototype.slice.call(document.querySelectorAll('.rw-tab'));

        function show(tab) {
            tabs.forEach(function (t) {
                var selected = (t === tab);
                t.setAttribute('aria-selected', selected ? 'true' : 'false');
                var panel = byId(t.getAttribute('aria-controls'));
                if (panel) { panel.hidden = !selected; }
            });
            var shownPanel = tab.getAttribute('aria-controls');
            if (onShow) { onShow(shownPanel); }
        }

        tabs.forEach(function (tab) {
            tab.addEventListener('click', function () { show(tab); });
        });
    }

    /* ── Reveal cards (syllables + words) ──────────────────────
       Tap toggles the hidden answer. aria-expanded doubles as the CSS hook and
       the accessibility state. A tap on the inner "Listen" chip must NOT also
       collapse the card, so those clicks are left for base.js and stopped here. */

    function setupRevealCards() {
        var cards = document.querySelectorAll('.rw-syl, .rw-word');
        Array.prototype.forEach.call(cards, function (card) {
            var answer = card.querySelector('.rw-syl-answer, .rw-word-answer');
            card.addEventListener('click', function (event) {
                if (event.target.closest('.th-audio')) { return; }  // let audio play
                var open = card.getAttribute('aria-expanded') === 'true';
                card.setAttribute('aria-expanded', open ? 'false' : 'true');
                if (answer) { answer.hidden = open; }
            });
        });
    }

    /* ── Story reader ──────────────────────────────────────────
       Render the first story as tappable word tokens. Tapping a word fills the
       gloss panel with its Thai, romanisation and meaning, and (if a recording
       exists) turns the gloss into a play button via the shared th-audio class. */

    function setupStory() {
        var stories = readJSON('rw-stories') || [];
        var audioMap = readJSON('rw-audio-map') || {};
        var mount = byId('rw-story-mount');
        if (!mount || !stories.length) { return; }

        var story = stories[0];
        var activeToken = null;

        var head = document.createElement('div');
        head.className = 'rw-story-head';
        head.innerHTML =
            '<h2 class="rw-story-title-th" lang="th"></h2>' +
            '<p class="rw-story-title-en"></p>';
        head.querySelector('.rw-story-title-th').textContent = story.title_th || '';
        head.querySelector('.rw-story-title-en').textContent = story.title_en || '';
        mount.appendChild(head);

        (story.sentences || []).forEach(function (sentence) {
            var p = document.createElement('p');
            p.className = 'rw-sentence';
            p.setAttribute('lang', 'th');
            sentence.forEach(function (tok) {
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'rw-token';
                btn.textContent = tok.thai;
                btn.addEventListener('click', function () {
                    if (activeToken) { activeToken.classList.remove('is-active'); }
                    activeToken = btn;
                    btn.classList.add('is-active');
                    showGloss(tok);
                });
                p.appendChild(btn);
            });
            mount.appendChild(p);
        });

        var gloss = document.createElement('div');
        gloss.className = 'rw-gloss';
        gloss.setAttribute('aria-live', 'polite');
        gloss.innerHTML = '<span class="rw-gloss-empty">Tap any word above to read it.</span>';
        mount.appendChild(gloss);

        if (story.moral_en) {
            var moral = document.createElement('p');
            moral.className = 'rw-moral';
            moral.textContent = '☸️ ' + story.moral_en;
            mount.appendChild(moral);
        }
        if (story.source) {
            var src = document.createElement('p');
            src.className = 'rw-source';
            src.textContent = story.source;
            mount.appendChild(src);
        }

        function showGloss(tok) {
            var url = audioMap[tok.thai];
            var listen = url
                ? ' <span class="th-audio rw-listen" role="button" tabindex="0"' +
                  ' data-audio="' + url + '">🔊 Listen</span>'
                : '';
            gloss.innerHTML =
                '<span class="rw-gloss-thai" lang="th"></span>' +
                '<span class="rw-gloss-paiboon"></span>' + listen +
                '<span class="rw-gloss-english"></span>';
            gloss.querySelector('.rw-gloss-thai').textContent = tok.thai;
            gloss.querySelector('.rw-gloss-paiboon').textContent = tok.paiboon;
            gloss.querySelector('.rw-gloss-english').textContent = tok.english;
        }
    }

    /* ── Trace canvas ──────────────────────────────────────────
       A faded letter behind a canvas; drawing over it practises the shape. No
       stroke-order data is claimed here — the guide is the whole glyph and the
       principles above the canvas teach where to start. */

    function setupTrace() {
        var consonants = (readJSON('rw-consonants') || []).filter(function (c) {
            return !c.obsolete;   // don't ask people to hand-write letters no one writes
        });
        var canvas = byId('rw-canvas');
        var guide = byId('rw-guide');
        if (!canvas || !guide || !consonants.length) { return; }

        var ctx = canvas.getContext('2d');
        var index = 0;
        var drawing = false;
        var last = null;

        function audioUrlFor(c) {
            var file = (c.audio || '').split('/').pop();
            return file ? (CONFIG.consonantAudioBase || '') + file : '';
        }

        function render() {
            var c = consonants[index];
            guide.textContent = c.char;
            byId('rw-trace-name').textContent = c.name_thai || c.char;
            byId('rw-trace-sound').textContent = c.name || '';
            byId('rw-counter').textContent = (index + 1) + ' / ' + consonants.length;
            byId('rw-listen').setAttribute('data-audio', audioUrlFor(c));
            clear();
        }

        // Size the canvas backing store to its on-screen size, allowing for
        // high-DPI screens so lines are crisp. Called when the Write tab first
        // becomes visible (a hidden panel reports a size of 0) and on resize.
        function sizeCanvas() {
            var rect = canvas.getBoundingClientRect();
            if (!rect.width) { return; }               // still hidden — try later
            var dpr = window.devicePixelRatio || 1;
            canvas.width = Math.round(rect.width * dpr);
            canvas.height = Math.round(rect.height * dpr);
            ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
            ctx.lineWidth = 8;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            ctx.strokeStyle = '#4A1A6B';
        }

        function clear() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        function pointFrom(event) {
            var rect = canvas.getBoundingClientRect();
            return { x: event.clientX - rect.left, y: event.clientY - rect.top };
        }

        canvas.addEventListener('pointerdown', function (event) {
            event.preventDefault();
            drawing = true;
            last = pointFrom(event);
            if (canvas.setPointerCapture) { canvas.setPointerCapture(event.pointerId); }
        });
        canvas.addEventListener('pointermove', function (event) {
            if (!drawing) { return; }
            var p = pointFrom(event);
            ctx.beginPath();
            ctx.moveTo(last.x, last.y);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
            last = p;
        });
        function stop() { drawing = false; last = null; }
        canvas.addEventListener('pointerup', stop);
        canvas.addEventListener('pointercancel', stop);
        canvas.addEventListener('pointerleave', stop);

        byId('rw-clear').addEventListener('click', clear);
        byId('rw-prev').addEventListener('click', function () {
            index = (index - 1 + consonants.length) % consonants.length;
            render();
        });
        byId('rw-next').addEventListener('click', function () {
            index = (index + 1) % consonants.length;
            render();
        });

        var toggle = byId('rw-toggle-guide');
        toggle.addEventListener('click', function () {
            var hidden = guide.classList.toggle('is-hidden');
            toggle.setAttribute('aria-pressed', hidden ? 'false' : 'true');
            toggle.textContent = hidden ? '👁️ Show guide' : '👁️ Hide guide';
        });

        window.addEventListener('resize', sizeCanvas);
        render();

        // Expose a hook so the tab controller can size the canvas the first
        // time the Write panel is shown.
        setupTrace.onWritePanelShown = function () { sizeCanvas(); clear(); };
    }

    /* ── Boot ──────────────────────────────────────────────── */

    document.addEventListener('DOMContentLoaded', function () {
        setupRevealCards();
        setupStory();
        setupTrace();
        setupTabs(function (shownPanel) {
            if (shownPanel === 'panel-write' && setupTrace.onWritePanelShown) {
                setupTrace.onWritePanelShown();
            }
        });
    });
})();
