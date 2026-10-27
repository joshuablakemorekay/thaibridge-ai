/* Pronunciation Analysis — the measuring half. No DOM, no microphone.

   Given raw audio samples, this finds the pitch line (how high the voice is,
   moment by moment) and compares a learner's line with the model clip's.
   Thai tones ARE pitch lines — mid, low, falling, high, rising — so the shape
   of the line is what tells a right tone from a wrong one.

   Both lines go through exactly the same code: the model MP3 is decoded and
   measured here too, not described by hand. So a quirk of the measuring hits
   both sides equally, and the comparison stays fair.

   Kept apart from pronounce.js (the page side) so tests can run it in Node:
   tests/test_pronounce_core.py feeds it made-up tones with a known shape.

   Everything runs on the learner's own device. No audio leaves it from here. */
(function (root, factory) {
    var api = factory();
    if (typeof module === 'object' && module.exports) { module.exports = api; }
    else { root.PronounceCore = api; }
}(this, function () {
    'use strict';

    var MIN_HZ = 70;          // below a deep man's speaking voice
    var MAX_HZ = 500;         // above a high woman's
    var FRAME = 1024;         // samples per measurement (~21 ms at 48 kHz)
    var HOP = 512;            // step between measurements: half a frame
    var CLARITY = 0.6;        // how periodic a frame must be to count as voiced
    var QUIET = 0.08;         // frames under 8% of the loudest are silence
    var POINTS = 24;          // both lines are resampled to this many points
    var MOVE = 1.5;           // semitones of change that count as "rises"/"falls"
    var MIN_VOICED = 5;       // fewer voiced frames than this = nothing heard
    var WRONG_WAY_CAP = 45;   // best possible score when the direction is wrong
    var OCTAVE = 12;          // semitones

    function rms(frame) {
        var sum = 0;
        for (var i = 0; i < frame.length; i++) { sum += frame[i] * frame[i]; }
        return Math.sqrt(sum / frame.length);
    }

    /* Pitch of one frame in Hz, or null if it is not a voiced sound.

       Normalised autocorrelation: slide the frame against itself and find the
       lag where it matches best — that lag is one cycle of the voice. Taking
       the FIRST strong peak (not just the biggest) avoids the classic mistake
       of reporting half the real pitch, a whole octave too low. */
    function framePitch(frame, sampleRate) {
        var minLag = Math.floor(sampleRate / MAX_HZ);
        var maxLag = Math.min(Math.floor(sampleRate / MIN_HZ), frame.length - 1);
        var n = frame.length;
        var scores = new Array(maxLag + 1);
        var best = 0;

        for (var lag = minLag; lag <= maxLag; lag++) {
            var cross = 0, e1 = 0, e2 = 0;
            for (var i = 0; i + lag < n; i++) {
                cross += frame[i] * frame[i + lag];
                e1 += frame[i] * frame[i];
                e2 += frame[i + lag] * frame[i + lag];
            }
            var s = (e1 && e2) ? cross / Math.sqrt(e1 * e2) : 0;
            scores[lag] = s;
            if (s > best) { best = s; }
        }
        if (best < CLARITY) { return null; }

        for (var l = minLag + 1; l < maxLag; l++) {
            if (scores[l] >= 0.9 * best && scores[l] >= scores[l - 1] && scores[l] >= scores[l + 1]) {
                // Parabolic interpolation between neighbouring lags for a
                // finer answer than whole samples allow.
                var a = scores[l - 1], b = scores[l], c = scores[l + 1];
                var shift = (a - 2 * b + c) ? 0.5 * (a - c) / (a - 2 * b + c) : 0;
                return sampleRate / (l + shift);
            }
        }
        return null;
    }

    /* The pitch line of a whole recording: Hz per frame, null where silent
       or unvoiced (Thai stops like ก ป ต make gaps, and that is fine). */
    function contour(samples, sampleRate) {
        var frames = [], loudest = 0;
        for (var start = 0; start + FRAME <= samples.length; start += HOP) {
            var frame = samples.subarray ? samples.subarray(start, start + FRAME)
                                         : samples.slice(start, start + FRAME);
            var level = rms(frame);
            frames.push({ frame: frame, level: level });
            if (level > loudest) { loudest = level; }
        }
        return frames.map(function (f) {
            if (!loudest || f.level < QUIET * loudest) { return null; }
            return framePitch(f.frame, sampleRate);
        });
    }

    function median(values) {
        var sorted = values.slice().sort(function (a, b) { return a - b; });
        var mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 ? sorted[mid] : (sorted[mid - 1] + sorted[mid]) / 2;
    }

    /* Voiced points only, in semitones above/below the speaker's own middle.

       Semitones, because pitch is heard as ratios: a man and a woman saying
       the same falling tone fall by about the same number of semitones even
       though their Hz are far apart. Measuring from each speaker's own median
       is what lets a learner's voice be compared with any model voice. A light
       median filter then removes one-frame glitches. */
    function shape(hzLine) {
        var voiced = hzLine.filter(function (hz) { return hz; });
        if (voiced.length < MIN_VOICED) { return null; }
        var centre = median(voiced);
        // One word never spans more than an octave either side of its middle;
        // a frame that does is a tracking slip (often an octave jump on a
        // breathy start or a creaky end), so it is dropped, not drawn.
        var semis = voiced.map(function (hz) { return 12 * Math.log2(hz / centre); })
            .filter(function (s) { return Math.abs(s) <= OCTAVE; });
        if (semis.length < MIN_VOICED) { return null; }
        return semis.map(function (_, i) {
            return median(semis.slice(Math.max(0, i - 2), i + 3));
        });
    }

    /* Stretch or squash a line to `count` evenly spaced points, so a quick
       learner and a slow model can be laid side by side. */
    function resample(line, count) {
        count = count || POINTS;
        if (line.length === 1) {
            return new Array(count).fill(line[0]);
        }
        var out = [];
        for (var i = 0; i < count; i++) {
            var pos = i * (line.length - 1) / (count - 1);
            var lo = Math.floor(pos), hi = Math.min(lo + 1, line.length - 1);
            out.push(line[lo] + (line[hi] - line[lo]) * (pos - lo));
        }
        return out;
    }

    function mean(values) {
        return values.reduce(function (s, v) { return s + v; }, 0) / values.length;
    }

    /* 'rises', 'falls' or 'level' — what the line does from its middle to its
       end. Not from the very start: the first moments of a word are the
       consonant letting go, which bends the pitch on its own. And Thai's
       rising tone dips before it climbs, so start-to-end can read it as level
       when middle-to-end clearly rises. */
    function movement(line) {
        var third = Math.max(1, Math.floor(line.length / 3));
        var middle = line.slice(third, Math.max(third + 1, line.length - third));
        var change = mean(line.slice(-third)) - mean(middle);
        return change > MOVE ? 'rises' : (change < -MOVE ? 'falls' : 'level');
    }

    /* Compare a learner's pitch line with the model's.

       Returns null if no voice was heard, else:
         score   0–100, from the average gap between the two lines in semitones
         model / yours   the two lines, resampled, for drawing
         modelMove / yourMove   'rises' | 'falls' | 'level'
         advice  one plain sentence on the biggest difference */
    function compare(modelHz, learnerHz) {
        var model = shape(modelHz), yours = shape(learnerHz);
        if (!model || !yours) { return null; }
        model = resample(model);
        yours = resample(yours);

        var gap = Math.sqrt(mean(model.map(function (m, i) {
            return (m - yours[i]) * (m - yours[i]);
        })));
        // 1 semitone apart on average is close (85); 4 apart is a different tone (40).
        var score = Math.max(0, Math.min(100, Math.round(100 - gap * 15)));

        var modelMove = movement(model), yourMove = movement(yours);
        // Going the wrong way IS a different tone in Thai (ไม้ — falling — is
        // not ไม — rising), however close the lines sit, so it can never pass.
        if (modelMove !== yourMove) { score = Math.min(score, WRONG_WAY_CAP); }
        var advice;
        if (modelMove !== yourMove) {
            advice = 'Towards the end, the model\'s pitch ' +
                     (modelMove === 'level' ? 'stays level' : modelMove) +
                     ', but yours ' + (yourMove === 'level' ? 'stays level' : yourMove) +
                     '. Listen again and copy the direction.';
        } else if (score >= 75) {
            advice = 'Your pitch follows the same shape as the model. Well done!';
        } else {
            advice = 'The direction is right (it ' + (modelMove === 'level' ? 'stays level' : modelMove) +
                     '), but the shape differs along the way. Compare the two lines.';
        }
        return { score: score, model: model, yours: yours,
                 modelMove: modelMove, yourMove: yourMove, advice: advice };
    }

    /* Did speech recognition hear the target word? Thai is written without
       spaces between words, so spaces and punctuation are ignored, and the
       polite particles ครับ/ค่ะ/คะ are allowed on either side. */
    function heardWord(target, alternatives) {
        function clean(text) {
            return (text || '').replace(/[\s.,!?'"]/g, '')
                .replace(/(ครับ|ค่ะ|คะ)$/, '');
        }
        var want = clean(target);
        if (!want) { return false; }
        return alternatives.some(function (alt) {
            var got = clean(alt);
            return got === want || (got.length > 0 && got.indexOf(want) !== -1);
        });
    }

    return {
        framePitch: framePitch, contour: contour, shape: shape, resample: resample,
        movement: movement, compare: compare, heardWord: heardWord,
        POINTS: POINTS
    };
}));
