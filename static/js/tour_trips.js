// Tour Guide trip player. Walks through the trips in tour_trips.py, which
// the page hands over as JSON in #tour-trips-data. Needs base.js (the
// .th-audio player) and thai_audio_wiring.html (window.wireThaiAudio).
(function () {
    // The trip player. Trips come from tour_trips.py; this only walks through
    // them. Stamps and the chosen polite ending are remembered in this browser
    // only. They are a convenience, not progress, so no points are awarded here.
    var data = JSON.parse(document.getElementById('tour-trips-data').textContent);
    var byKey = {};
    data.trips.forEach(function (t) { byKey[t.key] = t; });

    var picker = document.getElementById('trip-picker');
    var player = document.getElementById('trip-player');
    var STAMPS_KEY = 'tb-tour-stamps', VOICE_KEY = 'tb-tour-voice';

    function load(key, fallback) {
        try { var v = localStorage.getItem(key); return v ? JSON.parse(v) : fallback; }
        catch (e) { return fallback; }
    }
    function save(key, value) {
        try { localStorage.setItem(key, JSON.stringify(value)); } catch (e) { /* private window: fine */ }
    }

    var state = null;   // {trip, voice, i, picked, tried, firsts, showEn}

    function esc(s) {
        return String(s).replace(/[&<>"]/g, function (c) {
            return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
        });
    }
    function fill(text, paiboon) {
        var forms = data.particles[state.voice], i = paiboon ? 1 : 0;
        return text.split('{s}').join(forms.s[i]).split('{q}').join(forms.q[i]);
    }

    function showStamps() {
        var got = load(STAMPS_KEY, []);
        document.querySelectorAll('[data-stamp-for]').forEach(function (el) {
            el.hidden = got.indexOf(el.getAttribute('data-stamp-for')) === -1;
        });
    }

    function route(trip, current) {
        return '<div class="tp-route" aria-label="Your route" style="--stops: ' + trip.stops.length + '">' + trip.stops.map(function (s, k) {
            var cls = k < current ? 'done' : (k === current ? 'here' : '');
            return '<div class="tp-stop ' + cls + '"><span class="tp-dot"></span><span>' + esc(s) + '</span></div>';
        }).join('') + '</div>';
    }

    function top(trip) {
        return '<div class="tp-top"><button type="button" class="tp-back" data-act="exit">← All trips</button>' +
            '<span class="tp-trip-name">' + esc(trip.region) + ' · ' + esc(trip.title) +
            (state.started ? ' · <button type="button" class="tp-back" data-act="voice">speaking as ' +
                (state.voice === 'male' ? 'ครับ' : 'ค่ะ') + '</button>' : '') + '</span></div>';
    }

    function renderIntro() {
        var t = state.trip;
        var ph = t.photo;
        player.innerHTML = top(t) + '<div class="tp-card">' +
            '<figure class="tp-hero"><img src="' + esc(data.static + ph.file) + '" alt="' + esc(ph.alt) + '" width="1000" height="667">' +
            '<figcaption>Photo: <a href="' + esc(ph.source) + '" target="_blank" rel="noopener">' + esc(ph.artist) + '</a>, ' +
            '<a href="' + esc(ph.license_url) + '" target="_blank" rel="noopener">' + esc(ph.license) + '</a>, via Wikimedia Commons</figcaption></figure>' +
            '<span class="tp-place">' + esc(t.place) + '</span>' +
            '<h3 class="tp-title">' + esc(t.title) + '</h3>' +
            '<p>' + esc(t.blurb) + '</p>' +
            '<div class="tp-bubble"><span class="tp-intro-thai thai-text">' + esc(t.place_thai) + '</span>' +
            '<span class="tp-pb">' + esc(t.place_paiboon) + '</span><span class="tp-en">' + esc(t.place_english) + '</span></div>' +
            '<p class="tp-prompt">' + (state.voice ? 'Ready? Tap how you speak to set off.' : 'How do you speak? Thai polite endings depend on who is talking.') + '</p>' +
            '<div class="tp-voice">' +
            '<button type="button" data-voice="male"' + (state.voice === 'male' ? ' class="chosen"' : '') + '><span class="thai">ครับ</span><span class="tp-pb">kráp</span><small>I speak as a man</small></button>' +
            '<button type="button" data-voice="female"' + (state.voice === 'female' ? ' class="chosen"' : '') + '><span class="thai">ค่ะ / คะ</span><span class="tp-pb">kâ / ká</span><small>I speak as a woman</small></button>' +
            '</div></div>';
    }

    function renderScene() {
        var t = state.trip, sc = t.scenes[state.i], p = state.picked;
        var html = top(t) + route(t, sc.stop) + '<div class="tp-card">' +
            '<span class="tp-place">' + esc(sc.place) + '</span>' +
            '<h3 class="tp-title">' + esc(sc.title) + '</h3>' +
            '<p>' + esc(sc.narration) + '</p>';
        if (sc.thai) {
            html += '<div class="tp-bubble"><span class="tp-who">' + esc(sc.who) + ' says</span>' +
                '<span class="tp-said thai-text">' + esc(sc.thai) + '</span>' +
                '<span class="tp-pb">' + esc(sc.paiboon) + '</span><span class="tp-en">' + esc(sc.english) + '</span></div>';
        }
        html += '<div class="tp-prompt-row"><span class="tp-prompt">' + esc(sc.prompt) + '</span>' +
            (p === null ? '<button type="button" class="tp-hint" data-act="hint">' + (state.showEn ? 'Hide' : 'Show') + ' English</button>' : '') +
            '</div><div class="tp-choices' + (p !== null || state.showEn ? ' show-en' : '') + '">';
        sc.choices.forEach(function (c, k) {
            var cls = (p !== null && k === p) ? ' picked ' + c.verdict : '';
            html += '<button type="button" class="tp-choice' + cls + '" data-pick="' + k + '"' + (p !== null ? ' disabled' : '') + '>' +
                '<span class="thai">' + esc(fill(c.thai)) + '</span><span class="tp-pb">' + esc(fill(c.paiboon, true)) + '</span>' +
                '<span class="tp-en">' + esc(c.english) + '</span></button>';
        });
        html += '</div>';
        if (p !== null) {
            var c = sc.choices[p];
            var label = { good: 'Nice', ok: 'That works, mostly', miss: 'Not quite' }[c.verdict];
            var last = state.i === t.scenes.length - 1;
            html += '<div class="tp-feedback ' + c.verdict + '" role="status"><span class="tp-verdict">' + label + '</span>' +
                '<span class="tp-you-said">You said <span class="thai-text">' + esc(fill(c.thai)) + '</span></span>' +
                '<p>' + esc(c.reply) + '</p></div>' +
                '<div class="tp-tip"><strong>' + esc(sc.tip.title) + '</strong>' + esc(sc.tip.text) + '</div>' +
                '<div class="tp-actions">' + (c.verdict === 'miss'
                    ? '<button type="button" class="tp-btn ghost" data-act="retry">Try again</button>'
                    : '<button type="button" class="tp-btn primary" data-act="next">' + (last ? 'Get your stamp' : 'Continue') + '</button>') +
                '</div>';
        }
        player.innerHTML = html + '</div>';
    }

    function renderEnd() {
        var t = state.trip;
        var date = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' }).toUpperCase();
        var got = load(STAMPS_KEY, []);
        if (got.indexOf(t.key) === -1) { got.push(t.key); save(STAMPS_KEY, got); }
        player.innerHTML = top(t) + route(t, t.stops.length) +
            '<div class="tp-stamp-wrap"><div class="tp-stamp"><div><small>' + esc(t.place.toUpperCase()) + '</small>' +
            '<span class="thai">' + esc(t.stamp) + '</span><small>' + esc(date) + '</small></div></div></div>' +
            '<div class="tp-card"><h3 class="tp-title">Trip complete</h3>' +
            '<p>You got ' + state.firsts + ' of ' + t.scenes.length + ' stops right first time. ' +
            got.length + ' of ' + data.trips.length + ' stamps collected.</p>' +
            '<div class="tp-tip"><strong>Talk to a local</strong>' + esc(t.tutor_line) + '</div>' +
            '<div class="tp-actions">' +
            '<button type="button" class="tp-btn ghost" data-act="exit">All trips</button>' +
            '<a class="tp-btn primary" href="/chat?scenario=' + encodeURIComponent(t.tutor) + '">Practise with the AI tutor</a>' +
            '</div><p class="tp-draft">The Thai in these trips is a first draft awaiting a teacher’s review.</p></div>';
    }

    // Each render replaces the player's HTML, so the button that was just
    // pressed no longer exists and keyboard focus would fall back to the top of
    // the page. Put it somewhere useful instead: on the answer's feedback once
    // one is picked (Continue is the next Tab), otherwise on the new heading,
    // so a screen reader starts reading the new scene.
    function moveFocus(el) {
        if (!el) return;
        if (!el.matches('button, a')) el.setAttribute('tabindex', '-1');
        el.focus({ preventScroll: true });
    }

    function render(focusSelector) {
        if (!state.started) renderIntro();
        else if (state.i >= state.trip.scenes.length) renderEnd();
        else renderScene();
        if (window.wireThaiAudio) window.wireThaiAudio(player);
        document.getElementById('trips').scrollIntoView({ block: 'start' });
        var target = focusSelector || (state.picked !== null ? '.tp-feedback' : '.tp-title');
        moveFocus(player.querySelector(target));
    }

    function startTrip(key) {
        // Every trip opens on its photo and the ครับ / ค่ะ choice, with the last
        // choice highlighted, so a returning learner sets off in one tap.
        state = { trip: byKey[key], voice: load(VOICE_KEY, null), started: false, i: 0, picked: null,
                  tried: false, firsts: 0, showEn: false };
        picker.hidden = true;
        player.hidden = false;
        render();
    }

    function exitTrip() {
        var key = state.trip.key;
        state = null;
        player.hidden = true;
        player.innerHTML = '';
        picker.hidden = false;
        showStamps();
        moveFocus(picker.querySelector('[data-trip="' + key + '"]'));   // back where they came from
    }

    picker.addEventListener('click', function (e) {
        var card = e.target.closest('[data-trip]');
        if (card) startTrip(card.getAttribute('data-trip'));
    });

    player.addEventListener('click', function (e) {
        var b = e.target.closest('button');
        if (!b || b.classList.contains('th-audio')) return;   // 🔊 buttons belong to base.js
        if (b.dataset.voice) { state.voice = b.dataset.voice; state.started = true; save(VOICE_KEY, state.voice); return render(); }
        if (b.dataset.pick) {
            var k = +b.dataset.pick;
            if (!state.tried && state.trip.scenes[state.i].choices[k].verdict !== 'miss') state.firsts++;
            state.tried = true;
            state.picked = k;
            return render();
        }
        var act = b.dataset.act;
        if (act === 'exit') exitTrip();
        else if (act === 'voice') { state.started = false; render(); }
        else if (act === 'hint') { state.showEn = !state.showEn; render('[data-act="hint"]'); }
        else if (act === 'retry') { state.picked = null; render(); }
        else if (act === 'next') { state.i++; state.picked = null; state.tried = false; render(); }
    });

    showStamps();
})();
