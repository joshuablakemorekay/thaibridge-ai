/* Thai Alphabet page — chart, flashcards and quiz.
   ================================================

   Plain JavaScript, no build step, no libraries: the page has to work on
   whatever browser a visitor turns up with.

   Four rules this file exists to keep, each learned from a real failure:

     1. No drag and drop. It never worked on a touchscreen.
     2. ONE Audio object for the whole page. A fresh one per letter leaks
        decoders on iOS until sound stops working altogether.
     3. Render one flashcard, not forty-four. The quiz builds four options at a
        time. The DOM stays small however long you study.
     4. Never make content legible only after an animation. requestAnimationFrame
        and CSS transitions both stall in a throttled tab, which once left a
        revealed answer invisible. Everything here shows instantly.
*/

(function () {
    'use strict';

    var CONFIG = window.ABC_CONFIG || {};
    var LETTERS = JSON.parse(document.getElementById('abc-data').textContent);

    function byId(id) { return document.getElementById(id); }

    function shuffled(list) {
        // Fisher-Yates on a copy, so the caller's array is untouched.
        var out = list.slice(), i, j, tmp;
        for (i = out.length - 1; i > 0; i--) {
            j = Math.floor(Math.random() * (i + 1));
            tmp = out[i]; out[i] = out[j]; out[j] = tmp;
        }
        return out;
    }

    /* ── Audio ─────────────────────────────────────────────────
       One element, reused. Every play follows a tap, which is what iOS
       requires — it refuses to play sound nobody asked for. */

    var player = new Audio();
    var playingButton = null;

    function clearPlayingState() {
        if (playingButton) {
            playingButton.classList.remove('is-playing');
            playingButton = null;
        }
    }

    player.addEventListener('ended', clearPlayingState);
    player.addEventListener('error', clearPlayingState);

    function play(letter, button) {
        if (!letter || !letter.audio) { return; }

        clearPlayingState();
        if (button) {
            button.classList.add('is-playing');
            playingButton = button;
        }

        player.src = CONFIG.staticBase + letter.audio;

        // play() rejects if the browser refuses (no gesture yet, or a missing
        // file). Swallow it: a quiet button is a small disappointment, an
        // unhandled rejection in the console is worse.
        var attempt = player.play();
        if (attempt && typeof attempt.catch === 'function') {
            attempt.catch(clearPlayingState);
        }
    }

    /* ── Tabs ──────────────────────────────────────────────── */

    var tabs = [
        { tab: byId('tab-chart'), panel: byId('panel-chart') },
        { tab: byId('tab-cards'), panel: byId('panel-cards') },
        { tab: byId('tab-quiz'),  panel: byId('panel-quiz')  }
    ];

    function selectTab(index) {
        tabs.forEach(function (entry, i) {
            var on = i === index;
            entry.tab.setAttribute('aria-selected', on ? 'true' : 'false');
            entry.panel.hidden = !on;
        });
        // Sound should not follow you into a panel it makes no sense in.
        player.pause();
        clearPlayingState();
    }

    tabs.forEach(function (entry, i) {
        entry.tab.addEventListener('click', function () { selectTab(i); });
        // Arrow keys move between tabs — what a screen-reader user expects of
        // role="tablist".
        entry.tab.addEventListener('keydown', function (event) {
            var next = null;
            if (event.key === 'ArrowRight') { next = (i + 1) % tabs.length; }
            if (event.key === 'ArrowLeft')  { next = (i - 1 + tabs.length) % tabs.length; }
            if (next !== null) {
                event.preventDefault();
                selectTab(next);
                tabs[next].tab.focus();
            }
        });
    });

    /* ── Chart ─────────────────────────────────────────────── */

    function describe(letter) {
        return letter.cls.charAt(0).toUpperCase() + letter.cls.slice(1)
            + ' class · sounds like "' + letter.sound + '"';
    }

    function buildChart() {
        var host = byId('chart-groups');
        var labels = CONFIG.classLabels || {};

        ['middle', 'high', 'low'].forEach(function (cls) {
            var members = LETTERS.filter(function (l) { return l.cls === cls; });
            if (!members.length) { return; }

            var heading = document.createElement('h2');
            heading.className = 'abc-class-heading';
            heading.textContent = (labels[cls] || cls) + ' — ' + members.length + ' letters';
            host.appendChild(heading);

            var grid = document.createElement('div');
            grid.className = 'abc-grid';

            var detail = document.createElement('div');
            detail.className = 'abc-detail';
            detail.hidden = true;

            members.forEach(function (letter) {
                var cell = document.createElement('button');
                cell.type = 'button';
                cell.className = 'abc-cell';
                cell.setAttribute('aria-expanded', 'false');
                cell.setAttribute('aria-label',
                    letter.char + ', ' + letter.name + ', ' + letter.meaning);

                var glyph = document.createElement('span');
                glyph.className = 'abc-cell-letter';
                glyph.lang = 'th';
                glyph.textContent = letter.char;

                var name = document.createElement('span');
                name.className = 'abc-cell-name';
                name.textContent = letter.name;

                cell.appendChild(glyph);
                cell.appendChild(name);

                cell.addEventListener('click', function () {
                    var wasOpen = cell.getAttribute('aria-expanded') === 'true';

                    Array.prototype.forEach.call(
                        grid.querySelectorAll('.abc-cell'),
                        function (other) { other.setAttribute('aria-expanded', 'false'); });

                    if (wasOpen) {
                        detail.hidden = true;
                        return;
                    }

                    cell.setAttribute('aria-expanded', 'true');
                    showDetail(detail, letter);
                    play(letter, detail.querySelector('.abc-audio'));
                });

                grid.appendChild(cell);
            });

            host.appendChild(grid);
            host.appendChild(detail);
        });
    }

    function showDetail(detail, letter) {
        detail.innerHTML = '';
        detail.hidden = false;

        var glyph = document.createElement('div');
        glyph.className = 'abc-detail-letter';
        glyph.lang = 'th';
        glyph.textContent = letter.char;

        var text = document.createElement('div');
        text.className = 'abc-detail-text';

        var name = document.createElement('div');
        name.className = 'abc-detail-name';
        name.textContent = letter.name + ' — ' + letter.meaning;

        var thai = document.createElement('div');
        thai.className = 'abc-detail-thai';
        thai.lang = 'th';
        thai.textContent = letter.name_thai;

        var meta = document.createElement('div');
        meta.className = 'abc-detail-meta';
        meta.textContent = describe(letter);

        text.appendChild(name);
        text.appendChild(thai);
        text.appendChild(meta);

        var audioBtn = document.createElement('button');
        audioBtn.type = 'button';
        audioBtn.className = 'abc-audio';
        audioBtn.textContent = '🔊 Listen';
        audioBtn.setAttribute('aria-label', 'Play ' + letter.name);
        audioBtn.addEventListener('click', function () { play(letter, audioBtn); });

        detail.appendChild(glyph);
        detail.appendChild(text);
        detail.appendChild(audioBtn);
    }

    /* ── Flashcards ────────────────────────────────────────── */

    var deck = LETTERS.slice();
    var cardIndex = 0;

    var cardEl     = byId('flashcard');
    var cardReveal = byId('card-reveal');
    var cardAudio  = byId('card-audio');

    function renderCard() {
        var letter = deck[cardIndex];

        byId('card-letter').textContent = letter.char;
        byId('card-name').textContent = letter.name + ' — ' + letter.meaning;
        byId('card-thai').textContent = letter.name_thai;
        byId('card-meaning').textContent = describe(letter);
        byId('card-counter').textContent = (cardIndex + 1) + ' of ' + deck.length;

        cardAudio.setAttribute('aria-label', 'Play ' + letter.name);

        // Every move returns the card to its front.
        cardEl.classList.remove('is-revealed');
        cardReveal.textContent = 'Reveal';

        byId('card-prev').disabled = cardIndex === 0;
        byId('card-next').disabled = cardIndex === deck.length - 1;
    }

    function toggleReveal() {
        // One class does it all, applied immediately. No requestAnimationFrame
        // and no transition — both stall in a background tab and used to leave
        // the answer invisible after the user had tapped Reveal.
        var nowRevealed = !cardEl.classList.contains('is-revealed');
        cardEl.classList.toggle('is-revealed', nowRevealed);
        cardReveal.textContent = nowRevealed ? 'Hide' : 'Reveal';
    }

    cardReveal.addEventListener('click', toggleReveal);
    cardEl.addEventListener('click', toggleReveal);

    cardAudio.addEventListener('click', function (event) {
        event.stopPropagation();          // the card also toggles on click
        play(deck[cardIndex], cardAudio);
    });

    byId('card-prev').addEventListener('click', function () {
        if (cardIndex > 0) { cardIndex--; renderCard(); }
    });

    byId('card-next').addEventListener('click', function () {
        if (cardIndex < deck.length - 1) { cardIndex++; renderCard(); }
    });

    byId('card-shuffle').addEventListener('click', function () {
        deck = shuffled(LETTERS);
        cardIndex = 0;
        renderCard();
    });

    /* ── Quiz ──────────────────────────────────────────────── */

    var questions = [];
    var qIndex = 0;
    var score = 0;
    var answered = false;

    var quizOptions  = byId('quiz-options');
    var quizFeedback = byId('quiz-feedback');
    var quizNext     = byId('quiz-next');
    var quizAudioBtn = byId('quiz-audio');

    function buildQuestions() {
        // One question per letter, so every consonant is tested exactly once
        // and the pass mark means what it says.
        return shuffled(LETTERS).map(function (letter, i) {
            // Alternate the two question types rather than randomising them,
            // so nobody gets a run of twenty listening questions.
            var mode = (i % 2 === 0) ? 'see' : 'hear';

            // Wrong answers prefer letters of the SAME class, so the question
            // cannot be solved by elimination.
            var sameClass = LETTERS.filter(function (l) {
                return l.char !== letter.char && l.cls === letter.cls;
            });
            var others = LETTERS.filter(function (l) {
                return l.char !== letter.char && l.cls !== letter.cls;
            });
            var distractors = shuffled(sameClass).concat(shuffled(others)).slice(0, 3);

            return {
                letter: letter,
                mode: mode,
                options: shuffled([letter].concat(distractors))
            };
        });
    }

    function startQuiz() {
        questions = buildQuestions();
        qIndex = 0;
        score = 0;
        byId('quiz-intro').hidden = true;
        byId('quiz-result').hidden = true;
        byId('quiz-play').hidden = false;
        renderQuestion();
    }

    function renderQuestion() {
        var q = questions[qIndex];
        answered = false;

        quizFeedback.textContent = '';
        quizFeedback.className = 'abc-feedback';
        quizNext.hidden = true;
        quizOptions.innerHTML = '';

        byId('quiz-counter').textContent = 'Question ' + (qIndex + 1) + ' of '
            + questions.length + ' · ' + score + ' correct so far';
        byId('quiz-bar').style.width =
            ((qIndex / questions.length) * 100) + '%';

        var letterEl = byId('quiz-letter');

        if (q.mode === 'see') {
            byId('quiz-prompt').textContent = 'Which name belongs to this letter?';
            letterEl.textContent = q.letter.char;
            quizAudioBtn.hidden = true;
        } else {
            byId('quiz-prompt').textContent = 'Listen, then choose the letter you heard.';
            letterEl.textContent = '🔊';
            quizAudioBtn.hidden = false;
            quizAudioBtn.setAttribute('aria-label', 'Play the sound again');
            // Try to play at once. If the browser wants a fresh gesture, the
            // Play button is right there.
            play(q.letter, quizAudioBtn);
        }

        q.options.forEach(function (option) {
            var btn = document.createElement('button');
            btn.type = 'button';
            btn.className = 'abc-option';

            if (q.mode === 'see') {
                btn.textContent = option.name + ' (' + option.meaning + ')';
            } else {
                btn.className += ' abc-option-thai';
                btn.lang = 'th';
                btn.textContent = option.char;
                btn.setAttribute('aria-label', 'Letter ' + option.char);
            }

            btn.addEventListener('click', function () { answer(btn, option, q); });
            quizOptions.appendChild(btn);
        });
    }

    function answer(button, chosen, q) {
        if (answered) { return; }        // ignore a second tap
        answered = true;

        var correct = chosen.char === q.letter.char;
        if (correct) { score++; }

        // Mark every option, so the right answer is shown even when the guess
        // was wrong. The ✓/✗ matters as much as the colour — colour alone would
        // leave colour-blind users guessing.
        Array.prototype.forEach.call(
            quizOptions.querySelectorAll('.abc-option'),
            function (btn, i) {
                btn.disabled = true;
                var opt = q.options[i];
                if (opt.char === q.letter.char) {
                    btn.classList.add('is-correct');
                    btn.textContent = '✓ ' + btn.textContent;
                } else if (btn === button) {
                    btn.classList.add('is-wrong');
                    btn.textContent = '✗ ' + btn.textContent;
                }
            });

        quizFeedback.className = 'abc-feedback ' + (correct ? 'is-correct' : 'is-wrong');
        quizFeedback.textContent = correct
            ? 'Correct — ' + q.letter.char + ' is ' + q.letter.name
            : 'Not quite. ' + q.letter.char + ' is ' + q.letter.name
              + ' (' + q.letter.meaning + ')';

        quizNext.hidden = false;
        quizNext.textContent = (qIndex === questions.length - 1)
            ? 'See my result →'
            : 'Next question →';
        quizNext.focus();
    }

    quizNext.addEventListener('click', function () {
        qIndex++;
        if (qIndex >= questions.length) { finishQuiz(); } else { renderQuestion(); }
    });

    quizAudioBtn.addEventListener('click', function () {
        play(questions[qIndex].letter, quizAudioBtn);
    });

    function finishQuiz() {
        byId('quiz-play').hidden = true;
        byId('quiz-result').hidden = false;
        byId('quiz-bar').style.width = '100%';
        byId('result-score').textContent = score + ' / ' + questions.length;

        var passed = score >= CONFIG.passMark;
        var verdict = byId('result-verdict');
        verdict.className = 'abc-result-verdict ' + (passed ? 'is-pass' : 'is-fail');
        verdict.textContent = passed ? '🎉 Passed!' : 'Not passed yet';

        var message = byId('result-message');
        message.textContent = 'Saving your result…';

        // The SERVER decides whether this unlocks the site. The page reports a
        // score; it does not get to declare itself finished.
        fetch('/api/complete_alphabet', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ score: score, total: questions.length })
        })
            .then(function (r) { return r.json(); })
            .then(function (data) {
                message.textContent = data.message || '';
                byId('result-continue').hidden = !data.passed;
                if (data.passed && data.first_time) {
                    // Reload so the nav, the banner and every gated link
                    // re-render as unlocked. Delayed so the message is readable.
                    setTimeout(function () { window.location.reload(); }, 2500);
                }
            })
            .catch(function () {
                message.textContent = passed
                    ? 'You passed, but we could not save it just now. Check your '
                      + 'connection and take the quiz once more.'
                    : 'You need ' + CONFIG.passMark + ' to pass. Have another go.';
            });
    }

    byId('quiz-start').addEventListener('click', startQuiz);
    byId('quiz-retry').addEventListener('click', startQuiz);

    /* ── Go ────────────────────────────────────────────────── */

    buildChart();
    renderCard();
})();
