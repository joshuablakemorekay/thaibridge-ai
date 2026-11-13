// Moved out of templates/exercise.html, where it ran as an inline <script>.
// Values from the server now arrive in a JSON block on the page (a
// data block, which never runs), so the Content-Security-Policy can
// refuse inline scripts (see security_headers.py).

const EXERCISE_DATA = JSON.parse(document.getElementById('exercise-data').textContent);
const category = EXERCISE_DATA.category;
const beginnerMode = EXERCISE_DATA.beginnerMode;

// Tap-to-hear: thai -> MP3 URL for this category's words. wireAudio appends a
// 🔊 (the site-wide .th-audio player) to every .thai-text in `root` that has a
// clip. Called on load for the vocab table, and after each quiz render for the
// dynamically-built card. Guarded so a word is only wired once.
const EXERCISE_AUDIO = EXERCISE_DATA.audio;
function wireAudio(root) {
    (root || document).querySelectorAll('.thai-text').forEach(function (el) {
        if (el.dataset.audioWired) { return; }
        var url = EXERCISE_AUDIO[el.textContent.trim()];
        if (!url) { return; }
        el.dataset.audioWired = '1';
        var b = document.createElement('button');
        b.type = 'button';
        b.className = 'th-audio ex-listen';
        b.setAttribute('data-audio', url);
        b.setAttribute('aria-label', 'Listen');
        b.textContent = '🔊';
        el.appendChild(b);
    });
}
document.addEventListener('DOMContentLoaded', function () { wireAudio(document); });

let currentQuestion = null;
let score = 0;
let total = 0;

async function loadQuiz() {
    listening = false;
    const url = `/api/quiz/${category}${beginnerMode ? '?beginner=true' : ''}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        currentQuestion = data;

        let html = `
            <div style="text-align: center; margin-bottom: 1.5rem;">
                <p style="font-size: 0.9rem; color: #666;">Score: ${score}/${total}</p>
                <p class="thai-text" style="font-size: 2.5rem; margin: 1rem 0;">${data.thai}</p>
                <p style="font-size: 1.2rem; color: #666;">${data.english}</p>
                <p style="margin-top: 1rem; color: var(--royal-purple);">Select the correct ThaiBridge Spelling:</p>
            </div>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; max-width: 500px; margin: 0 auto;">
        `;

        data.options.forEach(option => {
            html += `
                <button class="btn" onclick="checkAnswer('${option}')" style="width: 100%;">
                    ${option}
                </button>
            `;
        });

        html += '</div>';

        document.getElementById('quizContent').innerHTML = html;
        wireAudio(document.getElementById('quizContent'));
    } catch (error) {
        document.getElementById('quizContent').innerHTML = '<p style="color: red;">Error loading quiz. Please try again.</p>';
    }
}

// Listening Quiz: the word is heard, never shown, until it has been answered.
// The options are English meanings, so they can hold apostrophes ("don't") —
// the buttons are built as elements with their own click handler rather than
// as an onclick="..." string, which an apostrophe would break.
let listening = false;
const SLOW_RATE = 0.7;   // the clips are already a touch slow; this is "really slow"

async function loadListening() {
    listening = true;
    const box = document.getElementById('quizContent');
    try {
        const response = await fetch(`/api/quiz/${category}?listen=true`);
        if (!response.ok) { throw new Error('no listening question'); }
        currentQuestion = await response.json();
    } catch (error) {
        box.innerHTML = '<p style="color: red;">Error loading the listening quiz. Please try again.</p>';
        return;
    }

    box.innerHTML = `
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <p style="font-size: 0.9rem; color: #666;">Score: ${score}/${total}</p>
            <p style="margin: 1rem 0;">
                <button type="button" class="btn btn-saffron th-audio" id="listenPlay">▶️ Play</button>
                <button type="button" class="btn th-audio" id="listenSlow"
                        data-audio-rate="${SLOW_RATE}">🐢 Slower</button>
            </p>
            <p style="margin-top: 1rem; color: var(--royal-purple);">What does it mean?</p>
        </div>
        <div id="listenOptions" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; max-width: 500px; margin: 0 auto;"></div>
    `;
    document.getElementById('listenPlay').setAttribute('data-audio', currentQuestion.audio);
    document.getElementById('listenSlow').setAttribute('data-audio', currentQuestion.audio);

    const options = document.getElementById('listenOptions');
    currentQuestion.options.forEach(option => {
        const b = document.createElement('button');
        b.type = 'button';
        b.className = 'btn';
        b.style.width = '100%';
        b.textContent = option;
        b.addEventListener('click', () => checkAnswer(option));
        options.appendChild(b);
    });
}

async function checkAnswer(answer) {
    total++;

    const response = await fetch('/api/check_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        // The question id is what gets marked. The browser is no longer told
        // the answer up front, so it cannot send it back — the server checks
        // against what it issued. Options travel too, so a wrong guess can be
        // shown the right one without the answer ever having been sent early.
        body: JSON.stringify({
            question_id: currentQuestion.question_id,
            answer: answer,
            options: currentQuestion.options
        })
    });

    const result = await response.json();
    if (window.ThaiSounds) ThaiSounds.result(result);

    if (result.correct) {
        score++;
    }

    const resultColor = result.correct ? 'var(--bodhi-green)' : 'var(--temple-red)';
    const resultIcon = result.correct ? '✅' : '❌';

    document.getElementById('quizContent').innerHTML = `
        <div style="text-align: center;">
            <p style="font-size: 0.9rem; color: #666;">Score: ${score}/${total}</p>
            <p style="font-size: 3rem;">${resultIcon}</p>
            <p style="font-size: 1.5rem; color: ${resultColor}; margin: 1rem 0;">
                ${result.message}
            </p>
            <p class="thai-text" style="font-size: 2rem;">${currentQuestion.thai}</p>
            <p class="paiboon" style="font-size: 1.3rem;">${listening ? currentQuestion.paiboon : (result.correct_answer ?? '')}</p>
            ${listening ? `<p style="font-size: 1.2rem; color: #666;">${result.correct_answer ?? ''}</p>` : ''}
            <p style="margin-top: 1.5rem;">
                <button class="btn btn-saffron" onclick="${listening ? 'loadListening()' : 'loadQuiz()'}">Next Question</button>
            </p>
        </div>
    `;
    wireAudio(document.getElementById('quizContent'));
}
