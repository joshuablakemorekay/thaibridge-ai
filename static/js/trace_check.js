/* Writing Practice — checking a traced or written letter. No DOM.

   Both the real letter and the learner's ink arrive as GRIDS: a flat array
   of true/false cells, `size` cells square, true where there is ink. The page
   (read_write.js) makes the letter's grid by drawing the same glyph it shows
   as the guide, and the learner's grid from their canvas, so the two line up
   exactly. Everything here is just counting cells.

   What it can honestly check: how much of the letter the learner covered,
   how much of their ink strays off it, and where the gaps are. What it can't:
   stroke order or direction — the app has no stroke-order data for Thai
   letters, so it never pretends to.

   Kept apart from the page so tests/test_trace_check.py can run it in Node. */
(function (root, factory) {
    var api = factory();
    if (typeof module === 'object' && module.exports) { module.exports = api; }
    else { root.TraceCheck = api; }
}(this, function () {
    'use strict';

    var REACH = 2;            // cells: how close ink must be to count as "on" a part
    var DONE_COVER = 0.85;    // share of the letter covered to call it done
    var DONE_OFF = 0.12;      // ...with no more than this share of ink off it
    var OFF_WARN = 0.2;       // more ink off the letter than this earns a warning

    /* Every cell within `r` cells (a square around it) of an inked cell. */
    function dilate(grid, size, r) {
        var out = new Array(grid.length).fill(false);
        for (var y = 0; y < size; y++) {
            for (var x = 0; x < size; x++) {
                if (!grid[y * size + x]) { continue; }
                for (var dy = -r; dy <= r; dy++) {
                    for (var dx = -r; dx <= r; dx++) {
                        var nx = x + dx, ny = y + dy;
                        if (nx >= 0 && ny >= 0 && nx < size && ny < size) {
                            out[ny * size + nx] = true;
                        }
                    }
                }
            }
        }
        return out;
    }

    function count(grid) {
        var n = 0;
        for (var i = 0; i < grid.length; i++) { if (grid[i]) { n++; } }
        return n;
    }

    /* The near-the-letter zone: the page uses it to colour ink orange the
       moment it leaves the letter. */
    function zone(letter, size) {
        return dilate(letter, size, REACH);
    }

    /* Where on the letter the biggest uncovered patch sits, in words. */
    function whereMissing(letter, inkNear, size) {
        var sx = 0, sy = 0, n = 0;
        for (var y = 0; y < size; y++) {
            for (var x = 0; x < size; x++) {
                var i = y * size + x;
                if (letter[i] && !inkNear[i]) { sx += x; sy += y; n++; }
            }
        }
        if (!n) { return ''; }
        var cx = sx / n / size, cy = sy / n / size;
        var v = cy < 0.4 ? 'top' : (cy > 0.6 ? 'bottom' : '');
        var h = cx < 0.4 ? 'left' : (cx > 0.6 ? 'right' : '');
        return (v && h) ? v + '-' + h : (v || h || 'middle');
    }

    /* Compare ink with the letter, cell for cell, where they sit.

       Returns { covered, off, done, message }:
         covered  share of the letter's cells with ink within REACH
         off      share of the ink's cells further than REACH from the letter */
    function assess(letter, ink, size) {
        var letterCells = count(letter), inkCells = count(ink);
        if (!inkCells) {
            return { covered: 0, off: 0, done: false,
                     message: 'Trace over the faded letter with your finger or mouse.' };
        }
        var inkNear = dilate(ink, size, REACH);
        var near = zone(letter, size);
        var covered = 0, off = 0;
        for (var i = 0; i < letter.length; i++) {
            if (letter[i] && inkNear[i]) { covered++; }
            if (ink[i] && !near[i]) { off++; }
        }
        var share = letterCells ? covered / letterCells : 0;
        var offShare = off / inkCells;
        var missing = whereMissing(letter, inkNear, size);
        var done = share >= DONE_COVER && offShare <= DONE_OFF;

        var message;
        if (done) {
            message = '✅ Well done — that\'s the whole letter, neatly on the line.';
        } else if (offShare > OFF_WARN) {
            message = 'Some of your lines wander off the letter (shown in orange). ' +
                      'Slow down and stay on the guide.';
        } else if (share >= DONE_COVER) {
            message = 'All of it is covered, but a little ink strays off the line. ' +
                      'Clear and try once more, a bit slower.';
        } else {
            message = 'Keep going — the ' + missing + ' part of the letter isn\'t traced yet.';
        }
        return { covered: share, off: offShare, done: done, missing: missing, message: message };
    }

    /* Crop a grid to its ink and stretch it to fill `size` × `size`, so a
       letter written smaller, bigger or off to one side can still be compared
       by its SHAPE. Used when the guide is hidden (writing from memory). */
    function normalise(grid, size) {
        var minX = size, minY = size, maxX = -1, maxY = -1;
        for (var y = 0; y < size; y++) {
            for (var x = 0; x < size; x++) {
                if (grid[y * size + x]) {
                    if (x < minX) { minX = x; }
                    if (y < minY) { minY = y; }
                    if (x > maxX) { maxX = x; }
                    if (y > maxY) { maxY = y; }
                }
            }
        }
        var out = new Array(size * size).fill(false);
        if (maxX < 0) { return out; }
        // Keep the shape's proportions: scale by the longer side, and centre.
        var span = Math.max(maxX - minX, maxY - minY) + 1;
        var offX = (span - (maxX - minX + 1)) / 2, offY = (span - (maxY - minY + 1)) / 2;
        for (var yy = minY; yy <= maxY; yy++) {
            for (var xx = minX; xx <= maxX; xx++) {
                if (!grid[yy * size + xx]) { continue; }
                var nx = Math.floor((xx - minX + offX) * size / span);
                var ny = Math.floor((yy - minY + offY) * size / span);
                out[Math.min(size - 1, ny) * size + Math.min(size - 1, nx)] = true;
            }
        }
        // Stretching spreads ink thinly; thicken it back into joined strokes.
        return dilate(out, size, 1);
    }

    /* Writing from memory: compare shapes, wherever and however big it was
       written. Same result shape as assess(), with gentler pass marks — a
       hand-written letter never matches a printed one cell for cell. */
    function assessFromMemory(letter, ink, size) {
        if (!count(ink)) {
            return { covered: 0, off: 0, done: false,
                     message: 'Write the letter in the box, then tap Check.' };
        }
        var result = assess(normalise(letter, size), normalise(ink, size), size);
        result.done = result.covered >= 0.7 && result.off <= 0.25;
        if (result.done) {
            result.message = '✅ That\'s the right shape. Show the guide to compare.';
        } else if (result.off > 0.25 || !result.missing) {
            result.message = 'That doesn\'t quite match the letter\'s shape yet. ' +
                             'Show the guide, trace it a few times, then try again.';
        } else {
            result.message = 'Close — but the ' + result.missing + ' part is missing or ' +
                             'a different shape. Show the guide to compare.';
        }
        return result;
    }

    return { dilate: dilate, zone: zone, assess: assess, normalise: normalise,
             assessFromMemory: assessFromMemory };
}));
