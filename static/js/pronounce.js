/* Pronunciation Analysis — the page half (the 🎤 Say it mode, Pro).

   One word at a time: hear the model, tap 🎤, say it. Then:
     * your pitch line is drawn over the model's, with a score and one plain
       sentence on the biggest difference (pronounce_core.js does the maths);
     * the browser's speech recognition says which Thai word it heard.

   Privacy, as the notice on the page says: the microphone is only opened by a
   tap, for at most RECORD_MS, and switched off straight after. The pitch line
   is worked out here, on the device. The word check uses the browser's own
   speech service (Google in Chrome and Edge, Apple in Safari), which receives
   that short recording; ThaiBridge never receives or stores it. Browsers
   without speech recognition (Firefox) still get the pitch line. */
(function () {
    'use strict';

    var RECORD_MS = 3000;
    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    var audioContext = null;      // created on the first tap (browsers insist)
    var modelCache = {};          // audio url -> decoded model pitch line

    function context() {
        if (!audioContext) {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
        }
        return audioContext;
    }

    function decode(arrayBuffer) {
        // Safari still wants the callback form of decodeAudioData.
        return new Promise(function (resolve, reject) {
            context().decodeAudioData(arrayBuffer, resolve, reject);
        });
    }

    async function modelLine(url) {
        if (!modelCache[url]) {
            var buffer = await decode(await (await fetch(url)).arrayBuffer());
            modelCache[url] = PronounceCore.contour(buffer.getChannelData(0), buffer.sampleRate);
        }
        return modelCache[url];
    }

    /* Record RECORD_MS of the learner, with the word check running alongside.
       Resolves to { line, heard } — heard is null where unsupported. */
    async function record(onTick) {
        // Echo cancelling and noise suppression bend the pitch; turn them off.
        var stream = await navigator.mediaDevices.getUserMedia({
            audio: { echoCancellation: false, noiseSuppression: false, autoGainControl: false }
        });
        var recorder = new MediaRecorder(stream);
        var chunks = [];
        recorder.ondataavailable = function (e) { if (e.data.size) { chunks.push(e.data); } };

        var heard = SpeechRecognition ? listenForWord() : Promise.resolve(null);
        var stopped = new Promise(function (resolve) { recorder.onstop = resolve; });
        recorder.start();

        var left = RECORD_MS / 1000;
        onTick(left);
        var ticker = setInterval(function () { onTick(--left); }, 1000);
        await new Promise(function (resolve) { setTimeout(resolve, RECORD_MS); });
        clearInterval(ticker);
        recorder.stop();
        await stopped;
        stream.getTracks().forEach(function (t) { t.stop(); });   // mic light off

        var buffer = await decode(await new Blob(chunks).arrayBuffer());
        return {
            line: PronounceCore.contour(buffer.getChannelData(0), buffer.sampleRate),
            heard: await heard
        };
    }

    /* The browser's Thai speech recognition: up to five guesses at the word. */
    function listenForWord() {
        return new Promise(function (resolve) {
            var rec = new SpeechRecognition();
            rec.lang = 'th-TH';
            rec.maxAlternatives = 5;
            rec.interimResults = false;
            var guesses = [];
            var done = function () { resolve(guesses); };
            rec.onresult = function (e) {
                for (var i = 0; i < e.results.length; i++) {
                    for (var j = 0; j < e.results[i].length; j++) {
                        guesses.push(e.results[i][j].transcript);
                    }
                }
            };
            rec.onerror = done;
            rec.onend = done;
            try { rec.start(); } catch (err) { resolve(null); return; }
            // Stop listening when the recording stops; give it a moment to answer.
            setTimeout(function () { try { rec.stop(); } catch (err) { /* already ended */ } },
                       RECORD_MS);
            setTimeout(done, RECORD_MS + 4000);
        });
    }

    function el(tag, className, text) {
        var node = document.createElement(tag);
        if (className) { node.className = className; }
        if (text !== undefined) { node.textContent = text; }
        return node;
    }

    /* The two pitch lines, as an SVG chart. Semitones from each speaker's own
       middle, so the height is the SHAPE of the tone, not how deep the voice is. */
    function chart(result) {
        var NS = 'http://www.w3.org/2000/svg';
        var svg = document.createElementNS(NS, 'svg');
        svg.setAttribute('viewBox', '0 0 240 110');
        svg.setAttribute('class', 'pron-chart');
        svg.setAttribute('role', 'img');
        svg.setAttribute('aria-label', 'The model\'s pitch ' + result.modelMove +
                         '; yours ' + result.yourMove + '.');

        var mid = document.createElementNS(NS, 'line');
        mid.setAttribute('x1', 0); mid.setAttribute('x2', 240);
        mid.setAttribute('y1', 55); mid.setAttribute('y2', 55);
        mid.setAttribute('class', 'pron-mid');
        svg.appendChild(mid);

        [['model', 'pron-model'], ['yours', 'pron-yours']].forEach(function (pair) {
            var line = result[pair[0]];
            var points = line.map(function (semis, i) {
                var x = 10 + i * 220 / (line.length - 1);
                var y = 55 - Math.max(-10, Math.min(10, semis)) * 4.5;
                return x.toFixed(1) + ',' + y.toFixed(1);
            }).join(' ');
            var poly = document.createElementNS(NS, 'polyline');
            poly.setAttribute('points', points);
            poly.setAttribute('class', pair[1]);
            svg.appendChild(poly);
        });
        return svg;
    }

    function verdict(score) {
        if (score >= 75) { return '🌟 Very close'; }
        if (score >= 55) { return '👍 Close'; }
        return '🔁 Try again';
    }

    /* Show one word and its controls in `box`. */
    function showWord(box, words, index) {
        var word = words[index];
        box.innerHTML = '';

        var head = el('div', 'pron-word');
        head.appendChild(el('p', 'thai-text pron-thai', word.thai));
        head.appendChild(el('p', 'paiboon', word.paiboon));
        head.appendChild(el('p', 'pron-english', word.english));
        box.appendChild(head);

        var controls = el('p', 'pron-controls');
        var play = el('button', 'btn th-audio', '▶️ Hear the model');
        play.type = 'button';
        play.setAttribute('data-audio', word.audio);
        var mic = el('button', 'btn btn-saffron', '🎤 Say it');
        mic.type = 'button';
        var next = el('button', 'btn btn-secondary', 'Next word →');
        next.type = 'button';
        controls.append(play, mic, next);
        box.appendChild(controls);

        var privacy = el('p', 'pron-privacy');
        privacy.append(
            '🔒 Tapping 🎤 records you for 3 seconds, then the microphone turns off. ' +
            'Your pitch line is worked out on this device. To check the word, your ' +
            'browser\'s speech service (Google in Chrome and Edge, Apple in Safari) ' +
            'hears that recording. ThaiBridge never receives or keeps it. ');
        var more = el('a', '', 'More in the privacy notice.');
        more.href = '/privacy#microphone';
        privacy.appendChild(more);
        box.appendChild(privacy);

        var status = el('p', 'pron-status');
        status.setAttribute('role', 'status');
        var results = el('div', 'pron-results');
        box.append(status, results);

        next.addEventListener('click', function () {
            showWord(box, words, (index + 1) % words.length);
        });

        mic.addEventListener('click', async function () {
            mic.disabled = true;
            results.innerHTML = '';
            try {
                var model = modelLine(word.audio);   // decode while they speak
                var take = await record(function (left) {
                    status.textContent = left > 0 ? '🔴 Listening… ' + left : 'Checking…';
                });
                var result = PronounceCore.compare(await model, take.line);
                status.textContent = '';
                if (!result) {
                    status.textContent = 'No voice heard. Check your microphone and try again, a little louder.';
                } else {
                    results.appendChild(el('p', 'pron-score',
                        verdict(result.score) + ' — tone match ' + result.score + '/100'));
                    results.appendChild(chart(result));
                    var key = el('p', 'pron-key');
                    key.append(el('span', 'pron-key-model', '━ model'), ' ',
                               el('span', 'pron-key-yours', '━ you'));
                    results.appendChild(key);
                    results.appendChild(el('p', 'pron-advice', result.advice));
                }
                results.appendChild(wordCheck(word.thai, take.heard));
            } catch (err) {
                status.textContent = err && err.name === 'NotAllowedError'
                    ? 'The microphone is blocked. Allow it for this site in your browser, then try again.'
                    : 'Something went wrong recording. Please try again.';
            }
            mic.disabled = false;
        });
    }

    function wordCheck(target, heard) {
        if (heard === null) {
            return el('p', 'pron-heard', 'Word check isn\'t available in this browser — try Chrome, Edge or Safari.');
        }
        if (PronounceCore.heardWord(target, heard)) {
            return el('p', 'pron-heard is-right', '✅ The word check heard ' + target + '.');
        }
        return el('p', 'pron-heard', heard.length
            ? '🤔 The word check heard: ' + heard[0] + '. Listen to the model and try again.'
            : '🤔 The word check couldn\'t make out a Thai word. Try again, clearly and a little slower.');
    }

    window.Pronounce = {
        supported: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia &&
                      window.MediaRecorder && (window.AudioContext || window.webkitAudioContext)),
        mount: function (box, words) {
            var start = Math.floor(Math.random() * words.length);
            showWord(box, words, start);
        }
    };
}());
