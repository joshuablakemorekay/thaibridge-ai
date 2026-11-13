// Moved out of templates/meditation.html, where it ran as an inline <script>.
// Values from the server now arrive in a JSON block on the page (a
// data block, which never runs), so the Content-Security-Policy can
// refuse inline scripts (see security_headers.py).

// ── Session Definitions ──────────────────────────────────────────────────
const SESSIONS = {
    // Two minutes, for when you are on the move - a moment of stillness before
    // giving blessings. Phase durations are in minutes, so 0.5 = 30 seconds.
    blessing: {
        label: '🙏 On the Move — Before Giving Blessings',
        totalMinutes: 2,
        type: 'breathing',
        phases: [
            { name: '🌬️ Arriving',   duration: 0.5, instruction: 'Three slow breaths. Feel your feet on the ground. Let the hurry fall away.' },
            { name: '🪷 Metta',      duration: 1,   instruction: '"May you be happy. May you be well. May you be free from suffering." Wish it for the people you are about to bless.' },
            { name: '🙏 Blessing',   duration: 0.5, instruction: 'Rest the mind in goodwill. Carry this calm with you into the blessing.' },
        ]
    },
    samatha: {
        label: '🌊 Samadhi — Concentration',
        totalMinutes: 30,
        type: 'breathing',
        phases: [
            { name: '🌿 Settling',       duration: 5,  instruction: 'Sit comfortably. Let thoughts settle like sediment in still water. Simply be here.' },
            { name: '🌬️ Anapanasati',   duration: 15, instruction: 'Bring full attention to the breath at the nostrils. Notice in-breath and out-breath without control.' },
            { name: '🌊 Deepening',      duration: 10, instruction: 'Rest awareness in the breath continuously. If distracted, return gently without judgment.' },
        ]
    },
    vipassana: {
        label: '👁️ Vipassana — Insight',
        totalMinutes: 30,
        type: 'breathing',
        phases: [
            { name: '🌿 Settling into Stillness', duration: 5,  instruction: 'Begin with breath awareness. Allow the mind to arrive before turning to investigation.' },
            { name: '🔍 Noting Practice',          duration: 15, instruction: 'Observe arising phenomena — thoughts, sensations, emotions. Note each: arising, passing, impermanent.' },
            { name: '🌌 Open Awareness',           duration: 10, instruction: 'Allow awareness to rest openly. Receive whatever arises without clinging or aversion.' },
        ]
    },
    body_scan: {
        label: '🫁 Body Scan',
        totalMinutes: 20,
        type: 'body_scan',
        phases: [
            { name: '🌱 Grounding',          duration: 3,  instruction: 'Lie down or sit. Notice the points of contact between your body and the surface supporting you.' },
            { name: '🫁 Body Scan',          duration: 14, instruction: 'Move attention slowly upward through the body. At each area, simply notice whatever is present.' },
            { name: '🌟 Whole Body Awareness', duration: 3,  instruction: 'Expand awareness to hold the entire body as a whole. Rest here in open presence.' },
        ]
    },
    full: {
        label: '☸ Full Session',
        totalMinutes: 60,
        type: 'breathing',
        phases: [
            { name: '🌿 Settling',             duration: 5,  instruction: 'Sit comfortably. Let thoughts settle. Simply arrive here.' },
            { name: '🌬️ Anapanasati',         duration: 20, instruction: 'Rest attention on the breath at the nostrils. Establish deep concentration.' },
            { name: '🌊 Deepening Samadhi',    duration: 5,  instruction: 'Allow the mind to rest in stillness. The breath becomes subtle and fine.' },
            { name: '🔍 Vipassana — Noting',   duration: 15, instruction: 'Open awareness to all arising phenomena. Note thoughts, sensations, emotions as they arise and pass.' },
            { name: '🌌 Open Awareness',       duration: 10, instruction: 'Rest in open, choiceless awareness. Receive experience without preference.' },
            { name: '🪷 Metta Closing',        duration: 5,  instruction: '"May all beings be happy. May all beings be free from suffering." Radiate loving kindness outward.' },
        ]
    }
};

// ── State ────────────────────────────────────────────────────────────────
let totalSeconds     = 20 * 60;
let remainingSeconds = 20 * 60;
let timerInterval    = null;
let isRunning        = false;
let currentSession   = null;
let currentPhaseIdx  = 0;
let phaseSecondsLeft = 0;
let sessionTotalSecs = 0;
let sessionElapsed   = 0;
let breathCycle      = null;
let bodyScanStepIdx  = 0;

// ── Breath Animation ─────────────────────────────────────────────────────
const BREATH_SEQUENCE = [
    { phase: 'inhale', label: 'Breathe in...', duration: 4000 },
    { phase: 'hold',   label: 'Hold...',       duration: 4000 },
    { phase: 'exhale', label: 'Breathe out...', duration: 6000 },
];
let breathIdx = 0;

function runBreathCycle() {
    const circle = document.getElementById('breathCircle');
    const label  = document.getElementById('breathLabel');
    if (!circle || !isRunning) return;

    const step = BREATH_SEQUENCE[breathIdx % BREATH_SEQUENCE.length];
    circle.className = 'breathing-circle ' + step.phase;
    label.textContent = step.label;
    circle.textContent = step.phase === 'inhale' ? '🌬️' : step.phase === 'hold' ? '🙏' : '😮‍💨';
    breathIdx++;
    breathCycle = setTimeout(runBreathCycle, step.duration);
}

function stopBreathCycle() {
    if (breathCycle) clearTimeout(breathCycle);
    breathCycle = null;
    const circle = document.getElementById('breathCircle');
    const label  = document.getElementById('breathLabel');
    circle.className = 'breathing-circle';
    circle.textContent = '🙏';
    label.textContent = '';
}

// ── Body Scan ─────────────────────────────────────────────────────────────
const BODY_SCAN_STEPS = JSON.parse(document.getElementById('body-scan-steps').textContent);

function highlightBodyScanStep(idx) {
    document.querySelectorAll('.body-scan-step').forEach((el, i) => {
        el.classList.toggle('active', i === idx);
        if (i === idx) el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });
}

function advanceBodyScan() {
    if (bodyScanStepIdx < BODY_SCAN_STEPS.length) {
        highlightBodyScanStep(bodyScanStepIdx);
        document.getElementById('phaseInstruction').textContent = BODY_SCAN_STEPS[bodyScanStepIdx].instruction;
        bodyScanStepIdx++;
    }
}

// ── Session Launch ────────────────────────────────────────────────────────
function launchSession(key) {
    resetTimer();
    currentSession  = SESSIONS[key];
    currentPhaseIdx = 0;
    sessionElapsed  = 0;
    bodyScanStepIdx = 0;

    sessionTotalSecs = currentSession.totalMinutes * 60;
    totalSeconds     = sessionTotalSecs;
    remainingSeconds = sessionTotalSecs;
    phaseSecondsLeft = currentSession.phases[0].duration * 60;

    // UI
    document.getElementById('sessionLabel').style.display = 'block';
    document.getElementById('presetButtons').style.display = 'none';
    document.getElementById('phaseBanner').textContent = currentSession.phases[0].name;
    document.getElementById('phaseInstruction').textContent = currentSession.phases[0].instruction;
    updateDisplay();

    // Body scan panel
    const bsp = document.getElementById('bodyScanPanel');
    bsp.style.display = currentSession.type === 'body_scan' ? 'block' : 'none';

    // Circle colour
    const circle = document.getElementById('breathCircle');
    if (currentSession.type === 'body_scan') {
        circle.className = 'breathing-circle scanning';
        circle.textContent = '🫁';
    } else {
        circle.className = 'breathing-circle';
        circle.textContent = '🙏';
    }

    window.scrollTo({ top: document.querySelector('.timer-card').offsetTop - 20, behavior: 'smooth' });
    startTimer();
}

// ── Timer Core ────────────────────────────────────────────────────────────
function updateDisplay() {
    const mins = String(Math.floor(remainingSeconds / 60)).padStart(2, '0');
    const secs = String(remainingSeconds % 60).padStart(2, '0');
    document.getElementById('timerDisplay').textContent = `${mins}:${secs}`;

    if (sessionTotalSecs > 0) {
        const pct = (sessionElapsed / sessionTotalSecs) * 100;
        document.getElementById('progressBar').style.width = pct + '%';
    }
}

function startTimer() {
    if (isRunning) return;
    isRunning = true;
    document.getElementById('startBtn').disabled = true;
    document.getElementById('pauseBtn').disabled = false;

    if (currentSession && currentSession.type === 'breathing') {
        breathIdx = 0;
        runBreathCycle();
    }
    if (currentSession && currentSession.type === 'body_scan') {
        advanceBodyScan();
    }

    timerInterval = setInterval(tick, 1000);
    startMusic();
}

function tick() {
    if (remainingSeconds <= 0) {
        finishSession();
        return;
    }

    remainingSeconds--;
    sessionElapsed++;
    updateDisplay();

    if (currentSession) {
        phaseSecondsLeft--;
        checkPhaseTransition();
    }

    // Body scan: advance a step every ~76 seconds across 14 min scan phase
    if (currentSession && currentSession.type === 'body_scan' && sessionElapsed > 180) {
        const scanElapsed = sessionElapsed - 180;
        const scanTotal   = 14 * 60;
        const stepEvery   = Math.floor(scanTotal / BODY_SCAN_STEPS.length);
        const expectedStep = Math.floor(scanElapsed / stepEvery);
        if (expectedStep !== bodyScanStepIdx - 1 && expectedStep < BODY_SCAN_STEPS.length) {
            bodyScanStepIdx = expectedStep;
            advanceBodyScan();
        }
    }
}

function checkPhaseTransition() {
    if (phaseSecondsLeft > 0) return;
    currentPhaseIdx++;
    if (currentPhaseIdx >= currentSession.phases.length) return;

    const phase = currentSession.phases[currentPhaseIdx];
    phaseSecondsLeft = phase.duration * 60;

    document.getElementById('phaseBanner').textContent = phase.name;
    document.getElementById('phaseInstruction').textContent = phase.instruction;
    playBell(1);
}

function pauseTimer() {
    if (!isRunning) return;
    clearInterval(timerInterval);
    isRunning = false;
    stopBreathCycle();
    stopMusic();
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
}

function resetTimer() {
    pauseTimer();
    currentSession  = null;
    sessionTotalSecs = 0;
    sessionElapsed  = 0;
    currentPhaseIdx = 0;
    bodyScanStepIdx = 0;
    remainingSeconds = 20 * 60;
    totalSeconds     = 20 * 60;

    updateDisplay();
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('sessionLabel').style.display   = 'none';
    document.getElementById('presetButtons').style.display  = 'flex';
    document.getElementById('bodyScanPanel').style.display  = 'none';
    document.getElementById('phaseInstruction').textContent = 'Select a session above or set a custom time below.';

    const circle = document.getElementById('breathCircle');
    circle.className = 'breathing-circle';
    circle.textContent = '🙏';
    document.getElementById('breathLabel').textContent = '';
    document.querySelectorAll('.body-scan-step').forEach(el => el.classList.remove('active'));
}

function setCustomTimer(minutes) {
    if (isRunning) return;
    currentSession   = null;
    remainingSeconds = minutes * 60;
    totalSeconds     = minutes * 60;
    sessionTotalSecs = 0;
    document.getElementById('progressBar').style.width = '0%';
    document.getElementById('sessionLabel').style.display = 'none';
    updateDisplay();
}

function finishSession() {
    clearInterval(timerInterval);
    isRunning = false;
    stopBreathCycle();
    stopMusic();
    remainingSeconds = 0;
    updateDisplay();
    document.getElementById('progressBar').style.width = '100%';
    document.getElementById('startBtn').disabled = false;
    document.getElementById('pauseBtn').disabled = true;
    document.getElementById('phaseBanner').textContent = '🪷 Session Complete';
    document.getElementById('phaseInstruction').textContent = 'Sādhu sādhu sādhu 🙏 Rest in the stillness before returning to activity.';
    playBell(3);
    setTimeout(() => alert('🔔 Meditation session complete.\nSādhu sādhu sādhu 🙏'), 500);
}

// ── Bell ──────────────────────────────────────────────────────────────────
function playBell(times = 1) {
    try {
        const ctx  = audioCtx();
        let delay  = 0;
        for (let i = 0; i < times; i++) {
            setTimeout(() => {
                const osc  = ctx.createOscillator();
                const gain = ctx.createGain();
                osc.connect(gain);
                gain.connect(ctx.destination);
                osc.frequency.value = 432;
                osc.type = 'sine';
                gain.gain.setValueAtTime(0.6, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 4);
                osc.start(ctx.currentTime);
                osc.stop(ctx.currentTime + 4);
            }, delay);
            delay += 1500;
        }
    } catch(e) { console.log('Audio unavailable'); }
}

// ── Background music ─────────────────────────────────────────────────────
// Generated live by the browser, so there are no audio files to host and no
// licence to check. The one music option (Josh's choice, 2026-10-14) is a
// binaural beat: a C at 131 Hz in the left ear
// and 132.618 Hz in the right, so the brain hears a slow 1.618 Hz pulse - the
// golden number - over a soft C drone. It needs headphones. The note under
// the picker says what it may help with and that the evidence is mixed; no
// stronger claim is made, on purpose (see /policies: no selling with tricks).
let _ctx = null;
let musicMode = 'off';
let music = null;          // { master, nodes, bowlTimer } while playing

function audioCtx() {
    if (!_ctx) _ctx = new (window.AudioContext || window.webkitAudioContext)();
    if (_ctx.state === 'suspended') _ctx.resume();
    return _ctx;
}

function setMusic(mode) {
    musicMode = mode;
    try { localStorage.setItem('meditationMusic', mode); } catch (e) {}
    const sel = document.getElementById('musicSelect');
    sel.classList.toggle('active', mode !== 'off');
    const note = document.getElementById('musicNote');
    note.style.display = mode === 'off' ? 'none' : 'block';
    note.textContent = mode === 'golden'
        ? '🧠 Your left ear hears a C at 131 Hz and your right ear 132.618 Hz, so your brain '
          + 'creates a slow 1.618 Hz pulse - the golden number. A beat this slow is in the delta range, '
          + 'the brainwave rhythm of deep rest and sleep. Studies suggest slow binaural beats can help '
          + 'the brain relax, ease anxiety and quieten busy thoughts, so the mind settles more easily '
          + 'into meditation (the research is still young, so treat it as a gentle aid). '
          + '🎧 Best with headphones; through speakers you\'ll hear it as a gentle slow pulse. '
          + 'On iPhone, turn the silent switch off.'
        : 'On iPhone, turn the silent switch off to hear the music.';
    stopMusic();
    if (isRunning) startMusic();
}

function startMusic() {
    if (musicMode === 'off' || music) return;
    try {
        const ctx = audioCtx();
        const master = ctx.createGain();
        master.gain.setValueAtTime(0.0001, ctx.currentTime);
        master.gain.exponentialRampToValueAtTime(0.35, ctx.currentTime + 4);   // fade in
        master.connect(ctx.destination);

        const soft = ctx.createBiquadFilter();
        soft.type = 'lowpass';
        soft.frequency.value = 900;
        soft.connect(master);

        const nodes = [];
        // A low C chord (C2, G2, E3, G3) under the 131 Hz C, without beating
        // against it - C3 itself is left out for that reason.
        [65.41, 98.00, 164.81, 196.00].forEach((freq, i) => {
            const osc = ctx.createOscillator();
            osc.type = i === 0 ? 'triangle' : 'sine';
            osc.frequency.value = freq;
            const g = ctx.createGain();
            g.gain.value = [0.30, 0.16, 0.12, 0.06][i];
            // each voice swells slowly at its own pace, so the sound breathes
            const lfo = ctx.createOscillator();
            lfo.frequency.value = 0.05 + i * 0.023;
            const depth = ctx.createGain();
            depth.gain.value = g.gain.value * 0.6;
            lfo.connect(depth).connect(g.gain);
            osc.connect(g).connect(soft);
            osc.start(); lfo.start();
            nodes.push(osc, lfo);
        });

        // Two pairs, each 1.618 Hz apart, so both beat at the golden number.
        // 131 / 132.618 Hz is Josh's track. Phone speakers barely play below
        // ~200 Hz, so a quieter pair an octave up (262 / 263.618 Hz - NOT
        // 265.236, which would double the beat to 3.236 Hz) carries the same
        // pulse through a speaker. Without headphones the two sides mix in
        // the air and the 1.618 Hz beat is heard as a slow throb instead.
        {
            [[131, -1, 0.16], [132.618, 1, 0.16],
             [262, -1, 0.07], [263.618, 1, 0.07]].forEach(([freq, pan, level]) => {
                const osc = ctx.createOscillator();
                osc.frequency.value = freq;
                const g = ctx.createGain();
                g.gain.value = level;
                osc.connect(g);
                if (ctx.createStereoPanner) {
                    const p = ctx.createStereoPanner();
                    p.pan.value = pan;
                    g.connect(p).connect(master);
                } else {
                    g.connect(master);   // older browsers: mono, still pulses
                }
                osc.start();
                nodes.push(osc);
            });
        }

        music = { master, nodes, bowlTimer: null };
        const nextBowl = () => {
            music.bowlTimer = setTimeout(() => {
                if (!music) return;
                singingBowl(master);
                nextBowl();
            }, 20000 + Math.random() * 25000);
        };
        nextBowl();
    } catch (e) { console.log('Audio unavailable'); }
}

function stopMusic() {
    if (!music) return;
    const { master, nodes, bowlTimer } = music;
    music = null;
    clearTimeout(bowlTimer);
    try {
        const now = _ctx.currentTime;
        master.gain.cancelScheduledValues(now);
        master.gain.setValueAtTime(master.gain.value, now);
        master.gain.exponentialRampToValueAtTime(0.0001, now + 1.5);   // fade out
        nodes.forEach(n => n.stop(now + 1.6));
        setTimeout(() => master.disconnect(), 1800);
    } catch (e) {}
}

// A struck bowl: a few out-of-tune partials that ring and fade slowly.
function singingBowl(dest) {
    const ctx = audioCtx();
    const now = ctx.currentTime;
    [[392, 0.18], [1052, 0.07], [1987, 0.03]].forEach(([freq, level]) => {
        const osc = ctx.createOscillator();
        osc.frequency.value = freq;
        const g = ctx.createGain();
        g.gain.setValueAtTime(0.0001, now);
        g.gain.exponentialRampToValueAtTime(level, now + 0.02);
        g.gain.exponentialRampToValueAtTime(0.0001, now + 9);
        osc.connect(g).connect(dest);
        osc.start(now);
        osc.stop(now + 9.1);
    });
}

// ── Init ──────────────────────────────────────────────────────────────────
updateDisplay();
try {
    let saved = localStorage.getItem('meditationMusic');
    if (saved === 'alpha' || saved === 'tranquil') saved = 'golden';   // retired options
    if (saved && saved !== 'off') {
        document.getElementById('musicSelect').value = saved;
        setMusic(saved);
    }
} catch (e) {}
