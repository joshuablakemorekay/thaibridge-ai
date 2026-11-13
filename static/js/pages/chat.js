// Moved out of templates/chat.html, where it ran as an inline <script>.
// Values from the server now arrive in a JSON block on the page (a
// data block, which never runs), so the Content-Security-Policy can
// refuse inline scripts (see security_headers.py).

// Injected by the /chat route — tells the UI this visitor's AI access.
const CHAT_DATA = JSON.parse(document.getElementById('chat-data').textContent);
const AI_LIMITS = CHAT_DATA.aiLimits;
// Pro starts on Conversation; free & basic start on the one mode they can use.
let currentMode = AI_LIMITS.unlimited ? 'conversation' : 'tutor';
let sessionId = 'session_' + Date.now();
let totalTokens = 0;
let currentScenario = null;   // active roleplay scenario id, or null
const DHAMMA_LENSES = CHAT_DATA.dhammaLenses;
let currentLens = CHAT_DATA.defaultLens;   // Buddhist mode only

// The conversation lives here, in this browser tab, not on the server.
// Each question sends the recent part of it back (the server caps it; see
// _history_from_browser in ai_agent.py). Kept here because the server
// forgot every chat on each deploy, and because storing it there would
// break the promise in app.py's AiUsage that message text is never kept.
// sessionStorage: it survives a refresh, and closing the tab ends it.
const HISTORY_KEY = 'thaibridge-chat-history';
let chatHistory = loadHistory();

function loadHistory() {
    try {
        const saved = JSON.parse(sessionStorage.getItem(HISTORY_KEY) || '[]');
        return Array.isArray(saved) ? saved : [];
    } catch (e) {
        return [];
    }
}

function saveHistory() {
    try {
        sessionStorage.setItem(HISTORY_KEY, JSON.stringify(chatHistory.slice(-40)));
    } catch (e) { /* private browsing or storage full: the chat still works */ }
}

function resetHistory() {
    chatHistory = [];
    saveHistory();
}

// `hidden` marks the roleplay kickoff, which the tutor saw but the learner
// never typed, so it is sent again but not redrawn after a refresh.
function rememberTurn(question, reply, hidden) {
    chatHistory.push({ role: 'user', content: question, hidden: !!hidden });
    chatHistory.push({ role: 'assistant', content: reply });
    saveHistory();
}

// After a refresh, put the conversation back on screen, so what the page
// shows and what the tutor remembers are the same thing.
function restoreChat() {
    if (!chatHistory.length) return;
    const welcome = document.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    const placeholder = document.getElementById('chat-placeholder');
    if (placeholder) placeholder.remove();
    chatHistory.forEach(turn => {
        if (!turn.hidden) addMessage(turn.role, turn.content);
    });
}
document.addEventListener('DOMContentLoaded', restoreChat);

// Shows the lens bar in Buddhist mode and marks the chosen lens.
function showLensBar() {
    const bar = document.getElementById('lens-bar');
    if (!bar) return;
    bar.hidden = currentMode !== 'buddhist';
    document.querySelectorAll('.lens-chip').forEach(c =>
        c.classList.toggle('active', c.dataset.lens === currentLens));
}

function setLens(id) {
    if (!DHAMMA_LENSES[id] || id === currentLens) return;
    currentLens = id;
    showLensBar();
    // The tutor is sent the conversation so far, and answers written in
    // the old approach pull the next few back towards it. Start its memory
    // afresh; the messages stay on screen so nothing is lost to read.
    resetHistory();
    addMessage('system', `Approach: ${DHAMMA_LENSES[id].icon} ${DHAMMA_LENSES[id].title}. ${DHAMMA_LENSES[id].blurb} The tutor starts fresh from here.`);
}

function switchMode(mode) {
    // Free & Basic can only use the allowed mode(s); the rest are Pro-only.
    if (!AI_LIMITS.unlimited && !AI_LIMITS.allowed_modes.includes(mode)) {
        showUpgradeNote("🔒 That AI mode is a Pro feature. Upgrade to unlock "
            + "Conversation, Culture, the Translator and the Exercise Generator.");
        return;
    }
    // Leaving conversation mode ends any roleplay in progress.
    if (mode !== 'conversation' && currentScenario) { exitScenario(); }
    currentMode = mode;

    // Update button states
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-mode="${mode}"]`).classList.add('active');
    showLensBar();
    document.getElementById('translator-note').hidden = mode !== 'translator';
    document.getElementById('photo-btn').hidden = mode !== 'translator';
    if (mode !== 'translator') clearPhoto();

    // The two modes have separate allowances, so the hint has to be redrawn
    // on every switch — not just after a message is sent.
    updateLimitHint();

    // Show mode change message
    const modeNames = {
        'conversation': '🗣️ Conversation Mode - Practice Thai dialogue',
        'tutor': '🎓 Tutor Mode - Get explanations and answers',
        'cultural': '🌏 Cultural Guide - Learn Thai customs',
        'buddhist': '☸️ Buddhist Guide - Explore the Dhamma. Choose your approach above',
        'generator': '📝 Generator Mode - Create custom exercises',
        'helper': '💡 Helper Mode - Get smart hints',
        'translator': '🔤 Translator - Type English or Thai, or tap 📷 for a photo of a menu or sign'
    };

    addMessage('system', `Switched to ${modeNames[mode]}`);
}

function quickStart(message) {
    document.getElementById('user-input').value = message;
    sendMessage();
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const photo = pendingPhoto;
    // A photo on its own is fine: the server asks for it to be read.
    const message = input.value.trim() || (photo ? 'Please read the Thai in this photo and translate it.' : '');
    if (!message) return;
    input.value = '';
    clearPhoto();
    await callAI(message, { showUser: true, photo: photo });
}

// ── Photo for the Translator ───────────────────────────────
// The photo is shrunk here, before it is sent: a phone photo is several
// megabytes, but Claude reads text just as well at 1568px on the long
// side, and a smaller image costs less to read and uploads faster on a
// mobile connection. Redrawing it as a JPEG also turns any odd format
// the phone hands over into one the server accepts.
const PHOTO_MAX_SIDE = 1568;
let pendingPhoto = null;   // { media_type, data, preview } or null

function onPhotoChosen(file) {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
        addMessage('system', 'That file is not a photo. Please choose an image.');
        return;
    }
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => {
        const scale = Math.min(1, PHOTO_MAX_SIDE / Math.max(img.width, img.height));
        const canvas = document.createElement('canvas');
        canvas.width = Math.round(img.width * scale);
        canvas.height = Math.round(img.height * scale);
        canvas.getContext('2d').drawImage(img, 0, 0, canvas.width, canvas.height);
        URL.revokeObjectURL(url);
        const dataUrl = canvas.toDataURL('image/jpeg', 0.85);
        pendingPhoto = {
            media_type: 'image/jpeg',
            data: dataUrl.split(',')[1],
            preview: dataUrl
        };
        document.getElementById('photo-preview-img').src = dataUrl;
        document.getElementById('photo-preview').hidden = false;
        document.getElementById('user-input').focus();
    };
    img.onerror = () => {
        URL.revokeObjectURL(url);
        addMessage('system', "That photo couldn't be opened. Please try a JPEG or PNG.");
    };
    img.src = url;
}

function clearPhoto() {
    pendingPhoto = null;
    document.getElementById('photo-preview').hidden = true;
    document.getElementById('photo-preview-img').removeAttribute('src');
}

// Shared network + response handling. Used by a typed message (showUser
// true) and by a scenario kickoff, which sends a hidden control message
// (showUser false) so the AI opens the scene without a stray user bubble.
async function callAI(message, opts) {
    opts = opts || {};
    const showUser = opts.showUser !== false;

    const photo = opts.photo || null;
    // The chat is kept as text (see chatHistory), so a photo is sent with
    // this message only and remembered as a marker in front of it.
    const remembered = photo ? '📷 ' + message : message;

    const input = document.getElementById('user-input');
    input.disabled = true;
    document.getElementById('send-btn').disabled = true;
    document.getElementById('photo-btn').disabled = true;

    // Remove welcome message and placeholder if present
    const welcome = document.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    const placeholder = document.getElementById('chat-placeholder');
    if (placeholder) placeholder.remove();

    if (showUser) {
        const bubble = addMessage('user', message);
        if (photo && bubble) {
            const img = document.createElement('img');
            img.className = 'message-photo';
            img.src = photo.preview;
            img.alt = 'Your photo';
            bubble.prepend(img);
        }
    }

    document.getElementById('thinking').classList.add('active');

    try {
        const response = await fetch('/api/ai/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                mode: currentMode,
                session_id: sessionId,
                scenario: currentScenario,
                lens: currentLens,
                stream: true,
                // The conversation so far. Only role and text: the
                // `hidden` flag is this page's own business.
                history: chatHistory.slice(-20).map(t => ({ role: t.role, content: t.content })),
                photo: photo ? { media_type: photo.media_type, data: photo.data } : null
            })
        });

        // A reply being written arrives as lines; a gate, an error or an
        // empty budget still arrives as one ordinary JSON answer below.
        const contentType = response.headers.get('Content-Type') || '';
        if (contentType.includes('application/x-ndjson')) {
            const reply = await readStreamedReply(response);
            if (reply !== null) rememberTurn(remembered, reply, !showUser);
            return;
        }

        const data = await response.json();

        if (data.success) {
            addMessage('assistant', data.response);
            rememberTurn(remembered, data.response, !showUser);

            if (data.tokens_used) {
                totalTokens += data.tokens_used.input + data.tokens_used.output;
                document.getElementById('token-display').textContent =
                    `Session tokens: ${totalTokens.toLocaleString()}`;
            }
            // The server sends both pools back, so the other allowance stays
            // accurate without asking for it again.
            if (data.pools) {
                AI_LIMITS.pools = data.pools;
                updateLimitHint();
            }
        } else if (data.gate) {
            showUpgradeNote(data.message, data.gate !== 'ai_resting');
            if (data.gate === 'daily_limit' && AI_LIMITS.pools) {
                // Zero only the pool that was actually refused.
                const pool = data.pool || currentPool();
                AI_LIMITS.pools[pool].remaining = 0;
                updateLimitHint();
            }
        } else {
            addMessage('system', `Error: ${data.message}`);
        }
    } catch (error) {
        addMessage('system', `Error: ${error.message}`);
    } finally {
        input.disabled = false;
        document.getElementById('send-btn').disabled = false;
        document.getElementById('photo-btn').disabled = false;
        document.getElementById('thinking').classList.remove('active');
        input.focus();
    }
}

// The reply as it is written: one JSON line per piece (see _stream_ai_reply
// in app.py). The bubble appears with the first words and is redrawn as the
// text grows, instead of the page sitting on "AI is thinking" throughout.
async function readStreamedReply(response) {
    const chatBody = document.getElementById('chat-messages');
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let text = '';
    let bubble = null;
    let finished = false;   // only a reply that reached 'done' is remembered

    while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop();   // a half-received line waits for the rest
        for (const line of lines) {
            if (!line.trim()) continue;
            const event = JSON.parse(line);
            if (event.type === 'text') {
                if (!bubble) {
                    document.getElementById('thinking').classList.remove('active');
                    bubble = addMessage('assistant', '');
                }
                text += event.text;
                bubble.innerHTML = formatMessage(text);
                chatBody.scrollTop = chatBody.scrollHeight;
            } else if (event.type === 'replace') {
                // The finished answer differs from what was shown: a
                // spelling corrected against the lessons. Show the
                // corrected one, and remember that one too.
                if (!bubble) {
                    document.getElementById('thinking').classList.remove('active');
                    bubble = addMessage('assistant', '');
                }
                text = event.text;
                bubble.innerHTML = formatMessage(text);
            } else if (event.type === 'done') {
                finished = true;
                if (event.tokens_used) {
                    totalTokens += event.tokens_used.input + event.tokens_used.output;
                    document.getElementById('token-display').textContent =
                        `Session tokens: ${totalTokens.toLocaleString()}`;
                }
                if (event.pools) {
                    AI_LIMITS.pools = event.pools;
                    updateLimitHint();
                }
            } else if (event.type === 'error') {
                addMessage('system', `Error: ${event.message}`);
            }
        }
    }
    // The full reply, or null if it broke off before finishing: half an
    // answer is not something the tutor should be shown as its own words.
    return finished ? text : null;
}

// ── Roleplay scenarios (conversation partner) ───────────────
function startScenario(id, title) {
    if (!AI_LIMITS.unlimited) {
        showUpgradeNote("🔒 Roleplay is part of Conversation mode, a Pro feature. "
            + "Upgrade to practise real Thai conversations with the AI partner.");
        return;
    }
    // Roleplay runs in conversation mode; select it and reset for a fresh scene.
    currentMode = 'conversation';
    document.getElementById('photo-btn').hidden = true;
    clearPhoto();
    document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
    const convBtn = document.querySelector('[data-mode="conversation"]');
    if (convBtn) convBtn.classList.add('active');
    showLensBar();

    currentScenario = id;
    sessionId = 'session_' + Date.now();   // fresh history per scene
    resetHistory();

    document.querySelectorAll('.scenario-chip').forEach(c => c.classList.remove('active'));
    const chip = document.querySelector(`.scenario-chip[data-scenario="${id}"]`);
    if (chip) chip.classList.add('active');
    const exit = document.getElementById('scenario-exit');
    if (exit) exit.hidden = false;

    const welcome = document.querySelector('.welcome-message');
    if (welcome) welcome.remove();
    addMessage('system', `🎭 Roleplay started: ${title}. Reply in Thai — the other person will begin.`);

    // Let the AI open the scene in character (hidden control message).
    callAI('(The learner is ready. Please begin the scene in character.)', { showUser: false });
}

// /chat?scenario=<id> opens straight into that roleplay. The Tour Guide
// trips and the Sentences page conversations link here. Only ids that have
// a chip on the page are honoured (the chips come from the server's
// ROLEPLAY_SCENARIOS), and startScenario still applies the Pro check, so
// the link grants nothing. The parameter is then dropped from the URL so a
// refresh doesn't spend another message restarting the scene.
document.addEventListener('DOMContentLoaded', function () {
    const wanted = new URLSearchParams(window.location.search).get('scenario');
    if (!wanted) return;
    history.replaceState(null, '', window.location.pathname);
    const chip = Array.from(document.querySelectorAll('.scenario-chip[data-scenario]'))
        .find(c => c.dataset.scenario === wanted);
    if (chip) chip.click();
});

function exitScenario() {
    currentScenario = null;
    document.querySelectorAll('.scenario-chip').forEach(c => c.classList.remove('active'));
    const exit = document.getElementById('scenario-exit');
    if (exit) exit.hidden = true;
    addMessage('system', '🎭 Roleplay ended. Back to open conversation.');
}

function addMessage(type, content) {
    const chatBody = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');

    if (type === 'system') {
        messageDiv.style.textAlign = 'center';
        messageDiv.style.padding = '0.5rem';
        messageDiv.style.color = 'var(--monsoon-grey)';
        messageDiv.style.fontStyle = 'italic';
        messageDiv.style.fontSize = '0.9rem';
        messageDiv.textContent = content;
    } else {
        messageDiv.className = `message ${type}`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.textContent = type === 'user' ? '👤' : '🤖';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        // Parse content for Thai text (simple detection)
        contentDiv.innerHTML = formatMessage(content);

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(contentDiv);
    }

    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
    // The text area, so a streamed reply can keep filling it in.
    return messageDiv.querySelector('.message-content');
}

function formatMessage(content) {
    // Simple formatting - detect Thai script and romanization patterns
    // This is a basic implementation - can be enhanced
    // Escaped first: this goes into innerHTML, and a reply (or a message
    // read back from sessionStorage) holding HTML would otherwise run as it.
    return content
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function clearChat() {
    if (!confirm('Clear entire conversation?')) return;

    const chatBody = document.getElementById('chat-messages');
    chatBody.innerHTML = `
        <div class="welcome-message">
            <h2>🪷 Chat Cleared!</h2>
            <p>Start a new conversation below.</p>
        </div>
        <div id="chat-placeholder">
            <span class="placeholder-icon">🪷</span>
            <span class="placeholder-text">Your conversation will appear here...</span>
        </div>
        <div class="thinking-indicator" id="thinking">AI is thinking</div>
    `;

    // Reset session
    sessionId = 'session_' + Date.now();
    totalTokens = 0;
    document.getElementById('token-display').textContent = 'Session tokens: 0';

    // The conversation is kept in this tab, so this is the whole clear.
    resetHistory();
}

function exportChat() {
    const messages = document.querySelectorAll('.message');
    let transcript = `ThaiBridge AI Chat - ${new Date().toLocaleDateString()}\n`;
    transcript += `Mode: ${currentMode}\n`;
    transcript += '='.repeat(60) + '\n\n';

    messages.forEach(msg => {
        const role = msg.classList.contains('user') ? 'You' : 'AI';
        const content = msg.querySelector('.message-content').textContent;
        transcript += `${role}: ${content}\n\n`;
    });

    // Download as text file
    const blob = new Blob([transcript], {type: 'text/plain'});
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `thai-chat-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// ---- Freemium UI helpers ----
// Which allowance the chosen mode spends from. Dhamma questions have their
// own daily pool, so the hint has to follow the mode rather than show one
// number for both — otherwise switching to Dhamma looks like it costs the
// Thai tutor's messages, which is exactly what the split fixed.
function currentPool() {
    return (AI_LIMITS.dhamma_modes || []).includes(currentMode) ? 'dhamma' : 'tutor';
}

function updateLimitHint() {
    const hint = document.getElementById('limit-hint');
    if (!hint || AI_LIMITS.unlimited || !AI_LIMITS.pools) return;
    const pool = currentPool();
    const left = AI_LIMITS.pools[pool].remaining;
    // The Dhamma line carries no upsell in EITHER state. A "go Pro" beside
    // the day's remaining Dhamma questions turns the teaching into a sales
    // surface, which is the same objection as charging for it — just
    // quieter. The tutor line keeps its link; that one really is a product.
    if (left > 0 && pool === 'dhamma') {
        hint.innerHTML = `🪷 <strong>${left}</strong> Dhamma question${left === 1 ? '' : 's'} left today`;
    } else if (left > 0) {
        hint.innerHTML = `🎁 FREE taste: <strong>${left}</strong> AI message${left === 1 ? '' : 's'} left today · `
            + `<a href="/premium">Go Pro for unlimited →</a>`;
    } else if (pool === 'dhamma') {
        // No upsell: the teaching is free, and the cap is a running cost.
        hint.innerHTML = `🪷 That’s today’s Dhamma questions — the teaching is free, `
            + `the model isn’t. Back tomorrow.`;
    } else {
        hint.innerHTML = `🔒 You’ve used today’s free AI messages · `
            + `<a href="/premium">Upgrade to Pro for unlimited →</a>`;
    }
    hint.style.display = 'block';
}

// withPlansLink is false when paying would not help: when the AI budget
// has run out ('ai_resting'), Pro is resting too.
function showUpgradeNote(text, withPlansLink = true) {
    const chatBody = document.getElementById('chat-messages');
    const note = document.createElement('div');
    note.className = 'upgrade-note';
    note.innerHTML = withPlansLink
        ? `${text} <a href="/premium">See Pro plans →</a>`
        : text;
    chatBody.appendChild(note);
    chatBody.scrollTop = chatBody.scrollHeight;
}

function initAiLimits() {
    if (AI_LIMITS.unlimited) return;
    // Visually lock the Pro-only mode buttons. Free & Basic have more than one
    // mode now, so highlight the one we actually start in rather than all of
    // them — otherwise every allowed button looks active at once.
    document.querySelectorAll('.mode-btn').forEach(btn => {
        const m = btn.getAttribute('data-mode');
        btn.classList.remove('active');
        if (!AI_LIMITS.allowed_modes.includes(m)) {
            btn.classList.add('mode-locked');
        }
    });
    const startBtn = document.querySelector(`[data-mode="${currentMode}"]`);
    if (startBtn) startBtn.classList.add('active');
    updateLimitHint();
}

// Focus input on load + apply freemium limits. preventScroll: a plain
// focus() scrolled the page down to the box, past the mode buttons and the
// approach picker, so a first visit opened on an empty chat with no
// choices in sight. The cursor is still in the box, ready to type.
window.addEventListener('load', () => {
    document.getElementById('user-input').focus({ preventScroll: true });
    initAiLimits();
});
