// Moved out of templates/tones_classes.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// ── Tab switching (same behaviour as the Vowels page) ──
function showTab(tabName, btn) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    if (btn) btn.classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// The drill pools used to be handed over here — every question WITH its
// answer, rendered straight into the page. That is what made the drills
// unmarkable: the answer key shipped to the browser, so nothing sent back from
// it could be trusted. Questions now come one at a time from /api/drill/<kind>
// and the answer stays on the server. Nothing about the drills belongs in this
// file any more.

/*
 * Reusable drill widget. Draws each question from the server and lets the
 * server mark it, so scoring, XP and quiz stats stay consistent with every
 * other quiz on the site — and so the answer is never in the page.
 *  cfg.kind    -> which drill, i.e. /api/drill/<kind>
 *  cfg.params  -> optional () => query string, e.g. '?level=2'
 */
function makeDrill(rootId, cfg) {
    const root = document.getElementById(rootId);
    const qEl = root.querySelector('.drill-question');
    const optsEl = root.querySelector('.drill-options');
    const fbEl = root.querySelector('.drill-feedback');
    const scoreEl = root.querySelector('.drill-score');
    const nextBtn = root.querySelector('.next-btn');
    let score = 0, total = 0, current = null, locked = false;

    function updateScore() { scoreEl.textContent = `Score: ${score} / ${total}`; }

    async function nextQuestion() {
        locked = true;                       // no answering a question not yet drawn
        fbEl.textContent = '';
        nextBtn.style.display = 'none';
        optsEl.innerHTML = '';
        qEl.textContent = '…';

        try {
            const params = cfg.params ? cfg.params() : '';
            const res = await fetch(`/api/drill/${cfg.kind}${params}`);
            if (!res.ok) { qEl.textContent = 'No questions here yet.'; return; }
            current = await res.json();
        } catch (e) {
            qEl.textContent = 'Could not load a question. Check your connection.';
            return;
        }

        qEl.innerHTML = `${current.thai}<small>${current.sub}</small>`;
        current.options.forEach(opt => {
            const b = document.createElement('button');
            b.className = 'opt-btn';
            b.textContent = opt;
            b.onclick = () => answer(opt, b);
            optsEl.appendChild(b);
        });
        locked = false;
    }

    async function answer(choice, btn) {
        if (locked) return;
        locked = true;
        total++;
        const buttons = optsEl.querySelectorAll('.opt-btn');
        buttons.forEach(b => { b.disabled = true; });

        // The server marks it. The browser is no longer told the answer when the
        // question is drawn, so it has nothing to mark against and nothing to
        // send back — which is what stopped these drills minting XP.
        let result = null;
        try {
            const res = await fetch('/api/check_answer', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    question_id: current.question_id,
                    answer: choice,
                    options: current.options
                })
            });
            result = await res.json();
        } catch (e) {
            fbEl.style.color = 'var(--temple-red)';
            fbEl.textContent = 'Could not reach the server to mark that one.';
            nextBtn.style.display = 'inline-block';
            return;
        }

        if (window.ThaiSounds) ThaiSounds.result(result);
        const correct = result.correct_answer;
        buttons.forEach(b => { if (b.textContent === correct) b.classList.add('correct'); });

        if (result.correct) {
            score++;
            const xp = result.xp_earned || 0;
            fbEl.style.color = 'var(--bodhi-green)';
            fbEl.textContent = xp ? `✅ Correct!  +${xp} XP` : '✅ Correct!';
        } else {
            btn.classList.add('wrong');
            fbEl.style.color = 'var(--temple-red)';
            fbEl.textContent = `❌ Not quite — the answer is ${correct}.`;
        }
        updateScore();
        nextBtn.style.display = 'inline-block';
    }

    nextBtn.addEventListener('click', nextQuestion);
    updateScore();
    nextQuestion();
    return { reset: nextQuestion };
};
}

document.addEventListener('DOMContentLoaded', function () {
    // Drill 1 — class identification
    makeDrill('drill-classid', { kind: 'classid' });

    // Drill 2 — tone calculation, filtered by the selected level
    let toneLevel = 1; // 1=mid, 2=high, 3=low, 0=mixed
    const toneDrill = makeDrill('drill-tonecalc', {
        kind: 'tone_calc',
        params: () => `?level=${toneLevel}`
    });
    document.querySelectorAll('#drill-tonecalc .level-btn').forEach(btn => {
        btn.addEventListener('click', function () {
            document.querySelectorAll('#drill-tonecalc .level-btn').forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            toneLevel = parseInt(this.dataset.level, 10);
            toneDrill.reset();
        });
    });

    // Drill 3 — contrast pairs
    makeDrill('drill-contrast', { kind: 'contrast' });

    // Drill 4 — leading ห
    makeDrill('drill-leadingh', { kind: 'leading_h' });
});
