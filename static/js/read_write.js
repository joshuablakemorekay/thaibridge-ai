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
       Render a story as tappable word tokens. Tapping a word fills the gloss
       panel with its Thai, romanisation and meaning, and (if a recording exists)
       turns the gloss into a play button via the shared th-audio class.

       thai_reading.STORIES holds more than one tale, so a picker sits above the
       text and re-renders on switch. With only one story the picker is left out
       entirely rather than shown as a single dead button. */

    function setupStory() {
        var stories = readJSON('rw-stories') || [];
        var audioMap = readJSON('rw-audio-map') || {};
        var mount = byId('rw-story-mount');
        if (!mount || !stories.length) { return; }

        // Two containers: the picker is built once, the story is rebuilt on
        // every switch. Keeping them apart means a switch cannot wipe the picker.
        var picker = null;
        if (stories.length > 1) {
            picker = document.createElement('div');
            picker.className = 'rw-story-picker';
            picker.setAttribute('role', 'tablist');
            picker.setAttribute('aria-label', 'Choose a story');
            mount.appendChild(picker);
        }

        var body = document.createElement('div');
        mount.appendChild(body);

        var buttons = [];
        if (picker) {
            stories.forEach(function (story, i) {
                var btn = document.createElement('button');
                btn.type = 'button';
                btn.className = 'rw-story-choice';
                btn.setAttribute('role', 'tab');
                btn.innerHTML =
                    '<span class="rw-story-choice-th" lang="th"></span>' +
                    '<span class="rw-story-choice-en"></span>' +
                    '<span class="rw-story-choice-len"></span>';
                btn.querySelector('.rw-story-choice-th').textContent = story.title_th || '';
                btn.querySelector('.rw-story-choice-en').textContent = story.title_en || '';
                btn.querySelector('.rw-story-choice-len').textContent =
                    (story.sentences || []).length + ' sentences';
                btn.addEventListener('click', function () { select(i); });
                buttons.push(btn);
                picker.appendChild(btn);
            });
        }

        function select(index) {
            buttons.forEach(function (b, i) {
                b.setAttribute('aria-selected', i === index ? 'true' : 'false');
            });
            renderStory(stories[index]);
        }

        function renderStory(story) {
            body.textContent = '';               // clear the previous story
            var activeToken = null;

            var head = document.createElement('div');
            head.className = 'rw-story-head';
            head.innerHTML =
                '<h2 class="rw-story-title-th" lang="th"></h2>' +
                '<p class="rw-story-subtitle-th" lang="th"></p>' +
                '<p class="rw-story-title-en"></p>' +
                '<p class="rw-story-instruction"></p>';
            head.querySelector('.rw-story-title-th').textContent = story.title_th || '';
            head.querySelector('.rw-story-title-en').textContent = story.title_en || '';
            setOrHide(head, '.rw-story-subtitle-th', story.subtitle_th);
            setOrHide(head, '.rw-story-instruction', story.instruction);
            body.appendChild(head);

            // Real-Thai stories read as whole paragraphs with the English hidden
            // underneath; graded stories read one tappable word at a time.
            if (story.format === 'passages') {
                renderPassages(story);
                renderExtras(story);
                return;
            }

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
                body.appendChild(p);
            });

            var gloss = document.createElement('div');
            gloss.className = 'rw-gloss';
            gloss.setAttribute('aria-live', 'polite');
            gloss.innerHTML = '<span class="rw-gloss-empty">Tap any word above to read it.</span>';
            body.appendChild(gloss);

            renderExtras(story);

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

        /* Fill an element's text, or remove it entirely when there is nothing to
           say — so a story without a subtitle leaves no empty gap behind. */
        function setOrHide(root, selector, text) {
            var el = root.querySelector(selector);
            if (!el) { return; }
            if (text) { el.textContent = text; } else { el.remove(); }
        }

        function el(tag, className, text) {
            var node = document.createElement(tag);
            if (className) { node.className = className; }
            if (text) { node.textContent = text; }
            return node;
        }

        /* Real-Thai passages: a numbered Thai paragraph, then the English behind
           a button. Hidden by default on purpose — the whole instruction is to
           read the Thai aloud FIRST and only then check yourself. */
        function renderPassages(story) {
            (story.passages || []).forEach(function (passage) {
                var wrap = el('div', 'rw-passage');

                var thai = el('p', 'rw-passage-thai');
                thai.setAttribute('lang', 'th');
                thai.appendChild(el('span', 'rw-passage-number', passage.number || ''));
                thai.appendChild(document.createTextNode(passage.thai || ''));
                wrap.appendChild(thai);

                var english = el('p', 'rw-passage-en', passage.english || '');
                english.hidden = true;

                var toggle = el('button', 'rw-passage-toggle', 'Check the English');
                toggle.type = 'button';
                toggle.setAttribute('aria-expanded', 'false');
                toggle.addEventListener('click', function () {
                    var open = toggle.getAttribute('aria-expanded') === 'true';
                    toggle.setAttribute('aria-expanded', open ? 'false' : 'true');
                    toggle.textContent = open ? 'Check the English' : 'Hide the English';
                    english.hidden = open;
                });

                var controls = el('div', 'rw-passage-controls');

                // The whole paragraph read aloud — a model to read along with,
                // or to check your own reading against. Only drawn once the clip
                // exists, the same rule as every other play button on the site.
                var url = audioMap[(passage.thai || '').trim()];
                if (url) {
                    var play = el('button', 'th-audio rw-passage-audio',
                                  '🔊 Listen to this paragraph');
                    play.type = 'button';
                    play.setAttribute('data-audio', url);
                    // Long clip: tapping again must STOP it, not restart it.
                    play.setAttribute('data-audio-toggle', '');
                    controls.appendChild(play);
                }

                controls.appendChild(toggle);
                wrap.appendChild(controls);
                wrap.appendChild(english);
                body.appendChild(wrap);
            });
        }

        /* Everything that sits under the story itself: the scripture note, the
           virtues table, the vocabulary list, the moral and the source. Shared by
           both formats — each part renders only if that story carries it. */
        function renderExtras(story) {
            var note = story.scripture_note;
            if (note) {
                var box = el('section', 'rw-note');
                var h = el('h3', 'rw-note-head');
                h.appendChild(el('span', 'rw-note-head-th', note.heading_th || ''));
                h.appendChild(el('span', 'rw-note-head-en', note.heading_en || ''));
                box.appendChild(h);
                var nt = el('p', 'rw-note-thai', note.thai || '');
                nt.setAttribute('lang', 'th');
                box.appendChild(nt);
                box.appendChild(el('p', 'rw-note-en', note.english || ''));

                var list = el('ul', 'rw-note-list');
                (note.identifications || []).forEach(function (item) {
                    var li = el('li');
                    var t = el('span', 'rw-note-item-th', item.thai || '');
                    t.setAttribute('lang', 'th');
                    li.appendChild(t);
                    li.appendChild(el('span', 'rw-note-item-en', item.english || ''));
                    list.appendChild(li);
                });
                box.appendChild(list);
                body.appendChild(box);
            }

            if ((story.virtues || []).length) {
                var vsec = el('section', 'rw-virtues');
                vsec.appendChild(el('h3', 'rw-note-head', '☸️ คุณธรรมในเรื่องนี้ — the virtues in this story'));
                var ul = el('ul', 'rw-virtue-list');
                story.virtues.forEach(function (v) {
                    var li = el('li', 'rw-virtue');
                    var term = el('div', 'rw-virtue-term');
                    var vth = el('span', 'thai-text rw-virtue-th', v.thai || '');
                    vth.setAttribute('lang', 'th');
                    term.appendChild(vth);
                    term.appendChild(el('span', 'rw-virtue-paiboon', v.paiboon || ''));
                    term.appendChild(el('span', 'rw-virtue-en', v.english || ''));
                    li.appendChild(term);
                    var wth = el('p', 'rw-virtue-story-th', v.in_story_th || '');
                    wth.setAttribute('lang', 'th');
                    li.appendChild(wth);
                    li.appendChild(el('p', 'rw-virtue-story-en', v.in_story_en || ''));
                    ul.appendChild(li);
                });
                vsec.appendChild(ul);
                body.appendChild(vsec);
            }

            if ((story.vocabulary || []).length) {
                var vocab = el('section', 'rw-vocab');
                vocab.appendChild(el('h3', 'rw-note-head', '📕 คำศัพท์ — vocabulary'));
                var vlist = el('ul', 'rw-vocab-list');
                story.vocabulary.forEach(function (w) {
                    var li = el('li', 'rw-vocab-item');
                    var wt = el('span', 'thai-text rw-vocab-thai', w.thai);
                    wt.setAttribute('lang', 'th');
                    li.appendChild(wt);
                    var url = audioMap[w.thai];
                    if (url) {
                        var play = el('span', 'th-audio rw-listen', '🔊');
                        play.setAttribute('role', 'button');
                        play.setAttribute('tabindex', '0');
                        play.setAttribute('data-audio', url);
                        play.setAttribute('aria-label', 'Listen');
                        li.appendChild(play);
                    }
                    li.appendChild(el('span', 'rw-vocab-paiboon', w.paiboon));
                    li.appendChild(el('span', 'rw-vocab-en', '— ' + w.english));
                    vlist.appendChild(li);
                });
                vocab.appendChild(vlist);
                body.appendChild(vocab);
            }

            if (story.moral_en) {
                body.appendChild(el('p', 'rw-moral', '☸️ ' + story.moral_en));
            }
            if (story.source) {
                body.appendChild(el('p', 'rw-source', story.source));
            }
        }

        select(0);
    }

    /* ── Trace canvas ──────────────────────────────────────────
       A faded letter behind a canvas; drawing over it practises the shape,
       and is checked as you go (trace_check.js):
         * each bit of line is purple on the letter and ORANGE the moment it
           leaves it — the instant correction;
         * after each stroke, how much of the letter is covered, and which
           part still isn't;
         * with the guide hidden, "Check" compares the SHAPE written from
           memory, wherever and however big it was written.
       No stroke-order data is claimed here — the app has none, so the check
       is about shape and coverage only, and the principles above the canvas
       teach where to start. */

    var GRID = 48;                     // the letter and the ink are compared on a 48×48 grid
    var INK = '#4A1A6B';               // royal purple: on the letter
    // Off the letter: a BRIGHT orange, not red. Red and dark purple are both
    // dark, so to a colour-blind learner they can look the same; light against
    // dark still reads when the hue doesn't.
    var STRAY = '#F57C00';

    /* Draw `char` centred in a w×h box. Used for BOTH the visible guide and
       the hidden grid it is checked against, so the two can never disagree.
       Centred on the ink itself (measureText's bounding box), not the font's
       line box, because Thai letters sit at very different heights in it. */
    function drawGlyph(g, char, w, h, family) {
        var size = Math.min(w, h) * 0.7;
        g.font = size + 'px ' + family;
        g.textAlign = 'left';
        g.textBaseline = 'alphabetic';
        var m = g.measureText(char);
        var left = m.actualBoundingBoxLeft || 0, right = m.actualBoundingBoxRight || m.width;
        var up = m.actualBoundingBoxAscent || size * 0.7, down = m.actualBoundingBoxDescent || 0;
        g.fillText(char, w / 2 - (right - left) / 2, h / 2 + (up - down) / 2);
    }

    function setupTrace() {
        var consonants = (readJSON('rw-consonants') || []).filter(function (c) {
            return !c.obsolete;   // don't ask people to hand-write letters no one writes
        });
        var canvas = byId('rw-canvas');
        var guide = byId('rw-guide');
        if (!canvas || !guide || !consonants.length) { return; }

        var ctx = canvas.getContext('2d');
        var guideCtx = guide.getContext('2d');
        var checking = !!window.TraceCheck;     // drawing still works without it
        var index = 0;
        var drawing = false;
        var last = null;
        var letterGrid = null;                  // the letter, as GRID×GRID cells
        var nearGrid = null;                    // the letter plus a pen's width
        var inkGrid = new Array(GRID * GRID).fill(false);
        var cssW = 0, cssH = 0;

        function audioUrlFor(c) {
            var file = (c.audio || '').split('/').pop();
            return file ? (CONFIG.consonantAudioBase || '') + file : '';
        }

        function guideHidden() { return guide.classList.contains('is-hidden'); }

        function render() {
            var c = consonants[index];
            byId('rw-trace-name').textContent = c.name_thai || c.char;
            byId('rw-trace-sound').textContent = c.name || '';
            byId('rw-counter').textContent = (index + 1) + ' / ' + consonants.length;
            byId('rw-listen').setAttribute('data-audio', audioUrlFor(c));
            drawGuide();
            clear();
        }

        /* The faded guide on screen, and the same letter as a grid to check
           against. Redrawn on every letter change and resize. */
        function drawGuide() {
            if (!cssW) { return; }
            var c = consonants[index];
            var style = getComputedStyle(guide);
            guideCtx.clearRect(0, 0, cssW, cssH);
            guideCtx.fillStyle = style.color;
            drawGlyph(guideCtx, c.char, cssW, cssH, style.fontFamily);

            var grid = document.createElement('canvas');
            grid.width = grid.height = GRID;
            var g = grid.getContext('2d');
            g.scale(GRID / cssW, GRID / cssH);
            g.fillStyle = '#000';
            drawGlyph(g, c.char, cssW, cssH, style.fontFamily);
            var pixels = g.getImageData(0, 0, GRID, GRID).data;
            letterGrid = [];
            for (var i = 3; i < pixels.length; i += 4) { letterGrid.push(pixels[i] > 96); }
            nearGrid = checking ? TraceCheck.zone(letterGrid, GRID) : null;
        }

        // Size both canvases' backing stores to their on-screen size, allowing
        // for high-DPI screens so lines are crisp. Called when the Write tab
        // first becomes visible (a hidden panel reports a size of 0) and on resize.
        function sizeCanvas() {
            var rect = canvas.getBoundingClientRect();
            if (!rect.width) { return; }               // still hidden — try later
            var dpr = window.devicePixelRatio || 1;
            cssW = rect.width;
            cssH = rect.height;
            [canvas, guide].forEach(function (c) {
                c.width = Math.round(cssW * dpr);
                c.height = Math.round(cssH * dpr);
                c.getContext('2d').setTransform(dpr, 0, 0, dpr, 0, 0);
            });
            ctx.lineWidth = 8;
            ctx.lineCap = 'round';
            ctx.lineJoin = 'round';
            drawGuide();
        }

        function clear() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            inkGrid = new Array(GRID * GRID).fill(false);
            showFeedback(null);
        }

        function pointFrom(event) {
            var rect = canvas.getBoundingClientRect();
            return { x: event.clientX - rect.left, y: event.clientY - rect.top };
        }

        function cellOf(p) {
            var x = Math.min(GRID - 1, Math.max(0, Math.floor(p.x * GRID / cssW)));
            var y = Math.min(GRID - 1, Math.max(0, Math.floor(p.y * GRID / cssH)));
            return y * GRID + x;
        }

        // Mark every grid cell the segment passes through, stepping finely
        // enough that a fast stroke leaves no gaps.
        function inkSegment(a, b) {
            var steps = Math.max(1, Math.ceil(Math.hypot(b.x - a.x, b.y - a.y) / 2));
            for (var s = 0; s <= steps; s++) {
                inkGrid[cellOf({ x: a.x + (b.x - a.x) * s / steps,
                                 y: a.y + (b.y - a.y) * s / steps })] = true;
            }
        }

        function showFeedback(result) {
            var fill = byId('rw-cover-fill'), pct = byId('rw-cover-pct'), msg = byId('rw-feedback-msg');
            if (!fill) { return; }
            var covered = result ? Math.round(result.covered * 100) : 0;
            fill.style.width = covered + '%';
            fill.classList.toggle('is-done', !!(result && result.done));
            pct.textContent = covered + '%';
            msg.textContent = result ? result.message
                : (guideHidden() ? 'Write the letter from memory, then tap Check.'
                                 : 'Trace over the faded letter with your finger or mouse.');
        }

        canvas.addEventListener('pointerdown', function (event) {
            event.preventDefault();
            drawing = true;
            last = pointFrom(event);
            inkSegment(last, last);
            if (canvas.setPointerCapture) { canvas.setPointerCapture(event.pointerId); }
        });
        canvas.addEventListener('pointermove', function (event) {
            if (!drawing) { return; }
            var p = pointFrom(event);
            // Orange only while tracing: with the guide hidden the learner is
            // writing from memory, and colouring the line would give it away.
            var stray = nearGrid && !guideHidden() && !nearGrid[cellOf(p)];
            ctx.strokeStyle = stray ? STRAY : INK;
            ctx.beginPath();
            ctx.moveTo(last.x, last.y);
            ctx.lineTo(p.x, p.y);
            ctx.stroke();
            inkSegment(last, p);
            last = p;
        });
        function stop() {
            if (!drawing) { return; }
            drawing = false;
            last = null;
            if (checking && letterGrid && !guideHidden()) {
                showFeedback(TraceCheck.assess(letterGrid, inkGrid, GRID));
            }
        }
        canvas.addEventListener('pointerup', stop);
        canvas.addEventListener('pointercancel', stop);
        canvas.addEventListener('pointerleave', stop);

        var check = byId('rw-check');
        check.addEventListener('click', function () {
            if (checking && letterGrid) {
                showFeedback(TraceCheck.assessFromMemory(letterGrid, inkGrid, GRID));
            }
        });

        // The guide letter depends on the Thai web font; redraw once it has
        // loaded, or the first letter would be drawn in a fallback face.
        if (document.fonts && document.fonts.ready) {
            document.fonts.ready.then(drawGuide);
        }

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
            check.hidden = !hidden || !checking;
            clear();
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
