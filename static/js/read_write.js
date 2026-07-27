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
