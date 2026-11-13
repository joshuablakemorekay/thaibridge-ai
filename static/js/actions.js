// One listener for the whole site, in place of onclick="..." attributes.
//
// The Content-Security-Policy refuses inline JavaScript, and that includes
// onclick="..." written into the HTML. So buttons now say what they do with
// data attributes, and this file runs the matching function:
//
//   <button data-on-click="setGender" data-args='["female"]'>
//       runs setGender("female") when clicked.
//
//   data-on-click / data-on-change / data-on-keydown / data-on-submit
//       name a global function (one defined at the top level of a page script).
//   data-args
//       a JSON list of arguments. Four special words stand for live values:
//         "$this"  the element itself        "$event" the browser event
//         "$value" the element's value       "$file"  the first chosen file
//   data-key="Enter"
//       on keydown, only run for that key.
//   data-confirm="Are you sure?"
//       on submit or click, ask first and stop if the answer is Cancel.
//   data-clicks="photo-input"
//       on click, click the element with that id instead (e.g. a hidden
//       file picker opened by a nicer-looking button).
//   data-reset-value
//       on change, clear the field after the function runs, so choosing the
//       same file again still counts as a change.
//
// A link with href="#" never jumps to the top of the page, and a function that
// returns false cancels the browser's default action, as onclick did.

(function () {
    'use strict';

    function argsFor(el, event) {
        var raw = el.getAttribute('data-args');
        if (!raw) { return []; }
        var list;
        try { list = JSON.parse(raw); } catch (e) { return []; }
        return list.map(function (arg) {
            if (arg === '$this') { return el; }
            if (arg === '$event') { return event; }
            if (arg === '$value') { return el.value; }
            if (arg === '$file') { return el.files && el.files[0]; }
            return arg;
        });
    }

    function handle(type, event) {
        var attr = 'data-on-' + type;
        var el = event.target.closest && event.target.closest(
            '[' + attr + '], [data-clicks]' + (type === 'submit' ? ', form[data-confirm]' : ''));
        if (!el) { return; }

        var question = el.getAttribute('data-confirm');
        if (question && (type === 'submit' || type === 'click') && !window.confirm(question)) {
            event.preventDefault();
            return;
        }

        if (type === 'click' && el.hasAttribute('data-clicks')) {
            var target = document.getElementById(el.getAttribute('data-clicks'));
            if (target) { target.click(); }
            return;
        }

        var name = el.getAttribute(attr);
        if (!name) { return; }
        var key = el.getAttribute('data-key');
        if (type === 'keydown' && key && event.key !== key) { return; }

        var fn = window[name];
        if (typeof fn !== 'function') {
            if (window.console) { console.warn('actions.js: no function called ' + name); }
            return;
        }
        if (el.tagName === 'A' && el.getAttribute('href') === '#') { event.preventDefault(); }

        var result = fn.apply(el, argsFor(el, event));
        if (result === false) { event.preventDefault(); }
        if (type === 'change' && el.hasAttribute('data-reset-value')) { el.value = ''; }
    }

    ['click', 'change', 'keydown', 'submit'].forEach(function (type) {
        document.addEventListener(type, function (event) { handle(type, event); });
    });
}());
