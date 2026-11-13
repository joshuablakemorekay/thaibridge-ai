// Sends any <form data-json-post> as JSON instead of as an ordinary form.
//
// Every POST to ThaiBridge must be JSON (see json_only.py): a form on another
// website can't send JSON without the browser asking ThaiBridge first, so this
// shuts out forged requests. The older forms (Monk Mode, dāna, claiming the
// earned unlock, cancelling a subscription) keep their plain HTML and gain the
// one attribute:
//
//   <form data-json-post action="/monk-mode">
//       ...fields...
//       <p data-form-message role="alert"></p>
//   </form>
//
// The fields become a JSON object. A name used more than once becomes a list,
// and the clicked submit button's own name and value are included, as a normal
// form would. The server answers with either:
//   {"redirect": "/somewhere"}            the page goes there, or
//   {"success": false, "message": "..."}  the message shows in [data-form-message].
//
// data-confirm="..." on the form is asked first (by actions.js, which is loaded
// before this file, so its answer is already known here).

(function () {
    'use strict';

    function add(data, name, value) {
        if (!Object.prototype.hasOwnProperty.call(data, name)) {
            data[name] = value;
        } else if (Array.isArray(data[name])) {
            data[name].push(value);
        } else {
            data[name] = [data[name], value];
        }
    }

    function fieldsOf(form, submitter) {
        var data = {};
        // FormData leaves out the button that was clicked. The dāna presets are
        // buttons carrying the amount, so add it by hand (older browsers don't
        // support FormData's own option for this). It goes FIRST, so a clicked
        // £5 wins over anything left typed in the "other" box, as before.
        if (submitter && submitter.name) { add(data, submitter.name, submitter.value); }
        new FormData(form).forEach(function (value, name) { add(data, name, value); });
        return data;
    }

    function show(form, text) {
        var box = form.querySelector('[data-form-message]');
        if (!box) {
            box = document.createElement('p');
            box.setAttribute('data-form-message', '');
            box.setAttribute('role', 'alert');
            form.appendChild(box);
        }
        box.textContent = text;
    }

    document.addEventListener('submit', async function (event) {
        var form = event.target;
        if (!form.matches || !form.matches('form[data-json-post]')) { return; }
        // Already cancelled, e.g. "Cancel" on the data-confirm question.
        if (event.defaultPrevented) { return; }
        event.preventDefault();

        var buttons = form.querySelectorAll('button, input[type="submit"]');
        buttons.forEach(function (b) { b.disabled = true; });
        show(form, '');
        try {
            var response = await fetch(form.getAttribute('action'), {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(fieldsOf(form, event.submitter))
            });
            // A page that needs signing in answers with the log-in page rather
            // than JSON. Follow it, as an ordinary form would have.
            var isJson = (response.headers.get('Content-Type') || '').indexOf('application/json') !== -1;
            if (!isJson) {
                window.location.assign(response.redirected ? response.url : form.getAttribute('action'));
                return;
            }
            var result = await response.json();
            if (result.redirect) {
                window.location.assign(result.redirect);
                return;
            }
            show(form, result.message || 'Something went wrong. Please try again.');
        } catch (err) {
            show(form, 'A network error occurred. Please try again.');
        }
        buttons.forEach(function (b) { b.disabled = false; });
    });
}());
