// Moved out of templates/progress.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
    'use strict';
    var box = document.getElementById('path');
    var message = box.querySelector('.path-message');

    async function post(url, body) {
        var response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(body || {})
        });
        var result = await response.json();
        if (!response.ok) { throw new Error(result.error || 'Something went wrong.'); }
        return result;
    }

    function reloadAtPath() {
        window.location.hash = 'path';
        window.location.reload();
    }

    async function run(action) {
        try { await action(); reloadAtPath(); }
        catch (err) { if (message) { message.textContent = err.message; } }
    }

    var form = document.getElementById('path-start');
    if (form) {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            var data = new FormData(form);
            run(function () {
                return post('/api/path/start', {
                    goal: data.get('goal'),
                    practice: data.get('practice'),
                    minutes: data.get('minutes')
                });
            });
        });
    }

    var review = document.getElementById('path-review');
    if (review) {
        review.addEventListener('click', function () { run(function () { return post('/api/path/review'); }); });
    }

    var reset = document.getElementById('path-reset');
    if (reset) {
        reset.addEventListener('click', function () { run(function () { return post('/api/path/reset'); }); });
    }

    // The starting check: all six questions are fetched at once and
    // answered one at a time, then marked together in a single POST.
    var go = document.getElementById('placement-go');
    if (go) {
        var skip = document.getElementById('placement-skip');
        var quiz = document.getElementById('placement-quiz');
        var questions = [], answers = [];

        skip.addEventListener('click', function () {
            run(function () { return post('/api/path/placement', { answers: [] }); });
        });

        go.addEventListener('click', async function () {
            go.disabled = true;
            try {
                var response = await fetch('/api/path/placement');
                var result = await response.json();
                if (!response.ok) { throw new Error(result.error); }
                questions = result.questions;
            } catch (err) {
                message.textContent = err.message || 'Could not load the check. Please try again.';
                go.disabled = false;
                return;
            }
            show(0);
        });

        // Built from elements, not an HTML string: the options are English
        // meanings and may contain apostrophes or other characters.
        function show(i) {
            if (i >= questions.length) {
                quiz.textContent = 'Marking…';
                run(function () { return post('/api/path/placement', { answers: answers }); });
                return;
            }
            var q = questions[i];
            quiz.innerHTML = '';

            var count = document.createElement('p');
            count.className = 'path-note';
            count.textContent = 'Question ' + (i + 1) + ' of ' + questions.length + ' · ' + q.topic;
            quiz.appendChild(count);

            var word = document.createElement('p');
            word.className = 'thai-text path-word';
            word.textContent = q.thai + ' ';
            if (q.audio) {
                var play = document.createElement('button');
                play.type = 'button';
                play.className = 'th-audio';
                play.setAttribute('data-audio', q.audio);
                play.setAttribute('aria-label', 'Listen');
                play.textContent = '🔊';
                word.appendChild(play);
            }
            quiz.appendChild(word);

            var spelling = document.createElement('p');
            spelling.className = 'paiboon';
            spelling.textContent = q.paiboon;
            quiz.appendChild(spelling);

            var grid = document.createElement('div');
            grid.className = 'path-options';
            q.options.concat(["I don't know"]).forEach(function (option) {
                var b = document.createElement('button');
                b.type = 'button';
                b.className = 'btn';
                b.textContent = option;
                b.addEventListener('click', function () {
                    answers.push({ question_id: q.question_id, answer: option });
                    show(i + 1);
                });
                grid.appendChild(b);
            });
            quiz.appendChild(grid);
        }
    }
}());
