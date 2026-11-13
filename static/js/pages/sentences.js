// Moved out of templates/sentences.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// Conversation practice mode. Toggling a conversation redacts its Thai lines
// so the learner produces them from the English prompt; tapping a line
// reveals it to check. Global functions because the buttons use inline
// onclick, the same pattern as the rest of this app's pages.
function toggleConvPractice(button) {
    var card = button.closest('.conv-card');
    var on = card.classList.toggle('practice-on');
    card.querySelector('.practice-state').textContent = on ? 'on' : 'off';
    var hint = card.querySelector('.practice-hint');
    if (hint) { hint.hidden = !on; }
    // Turning practice off (or back on) starts every line hidden again.
    card.querySelectorAll('.answer.revealed').forEach(function (a) {
        a.classList.remove('revealed');
    });
}

// ── Listen & answer ─────────────────────────────────────────────
// Hides a conversation's lines, plays it as one sequence through the
// site-wide player (base.js, data-audio-sequence), and asks comprehension
// questions the server deals and marks. The chosen speed is remembered on
// this device for every conversation.
var LISTEN_RATE_KEY = 'listenRate';

function toggleConvListening(button, convId) {
    var card = button.closest('.conv-card');
    var on = card.classList.toggle('listen-on');
    card.classList.remove('listen-revealed');
    card.querySelector('.listen-state').textContent = on ? 'on' : 'off';
    card.querySelector('.listen-panel').hidden = !on;
    if (on && !card.dataset.listenLoaded) { loadListening(card, convId); }
}

function revealConversation(button) {
    button.closest('.conv-card').classList.add('listen-revealed');
}

function setListenRate(card, rate) {
    card.querySelector('.listen-play').setAttribute('data-audio-rate', rate);
    card.querySelectorAll('.listen-rate').forEach(function (b) {
        b.setAttribute('aria-pressed', b.dataset.rate === rate ? 'true' : 'false');
    });
}

document.addEventListener('click', function (event) {
    var b = event.target.closest('.listen-rate');
    if (!b) { return; }
    setListenRate(b.closest('.conv-card'), b.dataset.rate);
    try { localStorage.setItem(LISTEN_RATE_KEY, b.dataset.rate); } catch (e) { /* private window */ }
});

async function loadListening(card, convId) {
    var box = card.querySelector('.listen-questions');
    var saved = null;
    try { saved = localStorage.getItem(LISTEN_RATE_KEY); } catch (e) { /* private window */ }
    if (saved) { setListenRate(card, saved); }

    var data;
    try {
        var response = await fetch('/api/listening/' + encodeURIComponent(convId));
        data = await response.json();
        if (!response.ok) { throw new Error(data.error); }
    } catch (err) {
        box.textContent = 'Could not load the questions. Please try again.';
        return;
    }
    card.dataset.listenLoaded = '1';
    box.innerHTML = '';

    var right = 0, answered = 0;
    var score = document.createElement('p');
    score.className = 'listen-score';

    // Built from elements, not an HTML string: the options are English
    // and may contain apostrophes.
    data.questions.forEach(function (q, i) {
        var block = document.createElement('div');
        block.className = 'listen-q';
        var title = document.createElement('p');
        title.className = 'listen-q-title';
        title.textContent = (i + 1) + '. ' + q.question;
        block.appendChild(title);

        var grid = document.createElement('div');
        grid.className = 'listen-options';
        q.options.forEach(function (option) {
            var b = document.createElement('button');
            b.type = 'button';
            b.className = 'listen-option';
            b.textContent = option;
            b.addEventListener('click', async function () {
                grid.querySelectorAll('button').forEach(function (x) { x.disabled = true; });
                var response = await fetch('/api/check_answer', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ question_id: q.question_id, answer: option, options: q.options })
                });
                var result = await response.json();
                if (window.ThaiSounds) { ThaiSounds.result(result); }
                grid.querySelectorAll('button').forEach(function (x) {
                    if (x.textContent === result.correct_answer) { x.classList.add('is-right'); }
                });
                if (!result.correct) { b.classList.add('is-wrong'); }
                answered++;
                if (result.correct) { right++; }
                score.textContent = right + ' of ' + answered + ' right' +
                    (answered === data.questions.length ? ' — now show the conversation to check.' : '');
            });
            grid.appendChild(b);
        });
        block.appendChild(grid);
        box.appendChild(block);
    });
    box.appendChild(score);
}

function revealAnswer(answer) {
    // Only meaningful while practising; a plain read-through ignores taps.
    if (answer.closest('.conv-card').classList.contains('practice-on')) {
        answer.classList.add('revealed');
    }
}

// ── Build the Sentence ──────────────────────────────────────────
// The server deals the tiles shuffled and keeps the right order to
// itself; the page only ever sends back the order the learner chose.
var sbQuestion = null;
var sbLevel = 'starter';
var SB_LEVEL_NOTES = {
    starter: 'Short sentences, with the romanisation on every word.',
    challenge: 'Longer sentences that join ideas — and no romanisation. Read the Thai! '
        + 'Some can be said more than one way round; any right order counts.'
};

function sbSetLevel(level) {
    sbLevel = level;
    document.querySelectorAll('.sb-level').forEach(function (b) {
        var on = b.dataset.level === level;
        b.classList.toggle('active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
    document.getElementById('sb-level-note').textContent = SB_LEVEL_NOTES[level];
    document.getElementById('sb-drill').classList.toggle('challenge', level === 'challenge');
    try { localStorage.setItem('sbLevel', level); } catch (e) { /* private window */ }
    sbNext();
}

function sbTile(tile, onTap) {
    var b = document.createElement(onTap ? 'button' : 'span');
    b.className = 'sb-tile' + (onTap ? '' : ' static');
    if (onTap) { b.type = 'button'; b.onclick = onTap; }
    var th = document.createElement('span');
    th.className = 'thai-text';
    th.textContent = tile.thai;
    var ro = document.createElement('span');
    ro.className = 'sb-roman';
    ro.textContent = tile.roman;
    b.append(th, ro);
    return b;
}

function sbMove(button, toRow) {
    if (sbQuestion && sbQuestion.done) { return; }
    document.getElementById(toRow).appendChild(button);
    document.getElementById('sb-check').disabled =
        document.getElementById('sb-pool').children.length > 0;
}

function sbRender() {
    var pool = document.getElementById('sb-pool');
    var answer = document.getElementById('sb-answer');
    pool.replaceChildren();
    answer.replaceChildren();
    sbQuestion.tiles.forEach(function (tile) {
        var b = sbTile(tile, function () {
            sbMove(b, b.parentNode.id === 'sb-pool' ? 'sb-answer' : 'sb-pool');
        });
        b.dataset.thai = tile.thai;
        pool.appendChild(b);
    });
    var speaker = document.getElementById('sb-speaker');
    speaker.className = 'sb-speaker ' + sbQuestion.speaker;
    speaker.textContent = sbQuestion.speaker === 'male' ? '👨 said by a man' : '👩 said by a woman';
    document.getElementById('sb-english').textContent = sbQuestion.english;
    document.getElementById('sb-check').disabled = true;
    document.getElementById('sb-result').hidden = true;
}

var sbRequest = 0;

function sbNext() {
    // Switching level quickly can leave an older request still in flight;
    // only the newest one is allowed to draw.
    var mine = ++sbRequest;
    fetch('/api/sentence-builder?level=' + encodeURIComponent(sbLevel))
        .then(function (r) { return r.json(); })
        .then(function (q) {
            if (mine !== sbRequest) { return; }
            if (q.error) {
                document.getElementById('sb-english').textContent = q.error;
                return;
            }
            sbQuestion = q;
            sbRender();
        })
        .catch(function () {
            document.getElementById('sb-english').textContent =
                'Could not load a sentence — check your connection and press Next.';
        });
}

function sbClear() {
    if (!sbQuestion) { return; }
    // A checked question can't be marked twice, so start a fresh one.
    if (sbQuestion.done) { sbNext(); } else { sbRender(); }
}

function sbCheck() {
    if (!sbQuestion || sbQuestion.done) { return; }
    var chosen = Array.from(document.getElementById('sb-answer').children)
        .map(function (b) { return b.dataset.thai; });
    sbQuestion.done = true;
    document.getElementById('sb-check').disabled = true;
    fetch('/api/sentence-builder/check', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question_id: sbQuestion.question_id, tiles: chosen })
    })
        .then(function (r) { return r.json(); })
        .then(function (res) {
            var box = document.getElementById('sb-result');
            box.replaceChildren();
            box.hidden = false;
            if (res.expired || res.error) {
                box.className = 'sb-result wrong';
                box.textContent = res.error;
                if (res.expired) { sbNext(); }
                return;
            }
            box.className = 'sb-result ' + (res.correct ? 'right' : 'wrong');
            if (window.ThaiSounds) ThaiSounds.result(res);
            var head = document.createElement('div');
            head.style.fontWeight = '600';
            head.textContent = res.correct
                ? 'ถูกต้อง! Correct!' + (res.xp_earned ? ' +' + res.xp_earned + ' XP' : '')
                : 'Not quite. The right order is:';
            box.appendChild(head);
            if (!res.correct) {
                var row = document.createElement('div');
                row.className = 'sb-row';
                res.correct_tiles.forEach(function (t) { row.appendChild(sbTile(t, null)); });
                box.appendChild(row);
            }
            if (res.tip) {
                var tip = document.createElement('div');
                tip.style.marginTop = '0.5rem';
                tip.textContent = '💡 ' + res.tip;
                box.appendChild(tip);
            }
        })
        .catch(function () {
            sbQuestion.done = false;
            document.getElementById('sb-check').disabled = false;
        });
}

document.addEventListener('DOMContentLoaded', function () {
    if (!document.getElementById('sb-drill')) { return; }
    // Come back to the level the learner last chose (a convenience only).
    var saved = null;
    try { saved = localStorage.getItem('sbLevel'); } catch (e) { /* private window */ }
    if (saved === 'challenge') { sbSetLevel('challenge'); } else { sbNext(); }
});
