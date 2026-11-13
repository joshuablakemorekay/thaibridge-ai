// Moved out of templates/chanting.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

// A closed <details> prints as just its heading, which would leave the
// background and meaning missing from a printed chant. So open every context
// section before printing, and put them back afterwards — the printed page and
// the screen stay the same book. Chants themselves are left alone: printing
// only what you opened is deliberate.
(function () {
    var reopened = [];

    function expand() {
        reopened = [];
        document.querySelectorAll('.chant-section:not([open])').forEach(function (section) {
            section.open = true;
            reopened.push(section);
        });
    }

    function restore() {
        reopened.forEach(function (section) { section.open = false; });
        reopened = [];
    }

    window.addEventListener('beforeprint', expand);
    window.addEventListener('afterprint', restore);

    // Safari and older browsers fire no print events, but they do flip this
    // media query around the print dialogue.
    if (window.matchMedia) {
        var printing = window.matchMedia('print');
        var onChange = function (event) { event.matches ? expand() : restore(); };
        if (printing.addEventListener) {
            printing.addEventListener('change', onChange);
        } else if (printing.addListener) {
            printing.addListener(onChange);
        }
    }
})();

// ── A chant arrives when its card is opened ─────────────────────────────
// The index used to carry all 305 chants in full, opened or not, which made
// it a 4.9MB page to read one chant on temple wifi. Now each card holds the
// address of its chant and fetches the words the first time it is opened.
//
// Nothing here is required for the page to work: without fetch, or if a
// request fails, the card shows a link to the chant's own page, which is the
// same chant from the same template.
// The same loader serves both grids: the temple book's and Ajarn Owen's.
['chant-book', 'owen-book'].forEach(function (gridId) {
    var grid = document.getElementById(gridId);
    if (!grid || !window.fetch) return;

    function load(card) {
        var pending = card.querySelector('.chant-pending');
        if (!pending || pending.getAttribute('data-loading')) return;
        pending.setAttribute('data-loading', '1');
        pending.classList.add('is-loading');
        pending.classList.remove('is-failed');

        fetch(pending.getAttribute('data-chant-url'), {
            credentials: 'same-origin',
            headers: { 'X-Requested-With': 'fetch' }
        }).then(function (response) {
            if (!response.ok) throw new Error(response.status);
            return response.text();
        }).then(function (html) {
            // A gate that has lapsed answers with a whole page rather than a
            // chant. Dropping that into the card would put a second copy of
            // the site inside it, so check it is a chant before trusting it.
            if (html.indexOf('chant-body') === -1) throw new Error('not a chant');
            pending.outerHTML = html;
        }).catch(function () {
            pending.removeAttribute('data-loading');
            pending.classList.remove('is-loading');
            pending.classList.add('is-failed');
        });
    }

    // `toggle` does not bubble, so it is caught on the way down instead.
    grid.addEventListener('toggle', function (event) {
        var card = event.target;
        // Every context section inside a chant is a <details> too — only the
        // cards themselves are asking for anything.
        if (card.classList && card.classList.contains('chant-card') && card.open) {
            load(card);
        }
    }, true);

    // Printing opens every chant it is given; the ones never opened have no
    // words to print, and waiting on the network mid-print is not an option.
    // So fetch anything already open before the print dialogue is drawn.
    window.addEventListener('beforeprint', function () {
        [].slice.call(grid.querySelectorAll('.chant-card[open]')).forEach(load);
    });
});

// ── Find a chant by name ────────────────────────────────────────────────
// Pure front end. The whole index is already in the page, so filtering it
// here is instant and asks the server for nothing — same approach as the
// layer toggles, and it keeps working on a phone with a bad signal in the
// middle of a service.
(function () {
    var panel = document.getElementById('chant-search');
    var box = document.getElementById('chant-find');
    var clear = document.getElementById('chant-find-clear');
    var count = document.getElementById('chant-search-count');
    var empty = document.getElementById('chant-search-empty');
    var grid = document.getElementById('chant-book');
    if (!panel || !box || !grid) return;

    var cards = [].slice.call(grid.querySelectorAll('.chant-card'));
    if (!cards.length) return;

    // Fold a name down to what a reader can actually type: lower case, no
    // accents — so "Khemakhema" finds "Khemākhema" — and no spaces, hyphens
    // or punctuation, so "saranadipika gatha" finds "saraṇadīpikā-gāthā".
    // Thai script passes through untouched: its vowels and tone marks are
    // letters in their own right, not accents to be stripped.
    function fold(text) {
        return (text || '').toLowerCase().normalize('NFD')
            .replace(/[̀-ͯ]/g, '')
            .replace(/[^0-9a-z฀-๿]+/g, '');
    }

    function textOf(card, selector) {
        return [].slice.call(card.querySelectorAll(selector))
            .map(function (el) { return el.textContent; }).join(' ');
    }

    // Every page the chant runs across, ranges opened out. The card says
    // "pages 47–49"; someone who was called to 48 must still find it.
    function pagesOf(card) {
        var pages = [];
        textOf(card, '.card-page').replace(
            /(\d+)\s*[–—-]\s*(\d+)|(\d+)/g,
            function (whole, from, to, one) {
                if (one) {
                    pages.push(Number(one));
                } else {
                    for (var n = Number(from); n <= Number(to); n++) pages.push(n);
                }
                return whole;
            });
        return pages;
    }

    var index = cards.map(function (card) {
        return {
            card: card,
            // Tier one: the names. This is what "find a chant" means, and it
            // includes the card's own id — a plain romanisation that is the
            // only typeable name some of the Pali-only chants have.
            name: fold(textOf(card, '.card-thai, .card-pali, .card-english')
                       + ' ' + card.id),
            // Tier two: the rest of what the closed card says — when it is
            // chanted, where it comes from, what it is about. Searched only
            // when nothing matched by name, so that a common word like
            // "refuge" cannot bury the chant actually called Refuge.
            about: fold(textOf(card, '.card-when, .chant-source, .card-summary')),
            pages: pagesOf(card)
        };
    });

    function openCard(card) {
        card.open = true;
        // Straight there, not a smooth glide. Opening a chant adds thousands
        // of pixels of verses to the page, and a smooth scroll that is still
        // animating while the page grows under it lands somewhere else
        // entirely — measured at 3,600px past the chant asked for. A jump is
        // what was asked for anyway.
        if (card.scrollIntoView) {
            card.scrollIntoView({ block: 'start' });
        }
    }

    var showing = index;

    function filterToQuery() {
        var raw = box.value.trim();
        var terms = raw.split(/\s+/).map(fold).filter(Boolean);
        var number = /^\d+$/.test(raw) ? Number(raw) : null;

        if (!terms.length) {
            showing = index;
            index.forEach(function (entry) { entry.card.hidden = false; });
            count.textContent = cards.length + ' chants, in book order.';
            empty.hidden = true;
            return;
        }

        function holdsAll(haystack) {
            return terms.every(function (term) {
                return haystack.indexOf(term) !== -1;
            });
        }

        var byName = index.filter(function (entry) {
            return holdsAll(entry.name)
                || (number !== null && entry.pages.indexOf(number) !== -1);
        });
        var found = byName;
        if (!found.length) {
            found = index.filter(function (entry) { return holdsAll(entry.about); });
        }

        showing = found;
        index.forEach(function (entry) {
            entry.card.hidden = found.indexOf(entry) === -1;
        });

        if (!found.length) {
            count.textContent = 'No chant found.';
            empty.hidden = false;
            return;
        }
        empty.hidden = true;
        // "Press Enter" is only worth saying when there is one thing to open.
        var opener = found.length === 1 ? ' — press Enter to open it.' : '.';
        if (byName.length) {
            count.textContent = (found.length === 1 ? '1 chant'
                                 : found.length + ' chants') + opener;
        } else {
            // Said plainly, because it changes what the reader is looking at:
            // these are not chants of that name, they are chants that talk
            // about it. Leaving that unsaid reads as a wrong answer.
            count.textContent = 'No name matches. '
                + (found.length === 1 ? '1 chant mentions it'
                   : found.length + ' chants mention it') + opener;
        }
    }

    function run() {
        filterToQuery();
        // The box grows and shrinks with the message it is showing, so where
        // a jumped-to chant has to land moves with it.
        placeUnderNav();
    }

    box.addEventListener('input', run);
    box.addEventListener('keydown', function (event) {
        if (event.key !== 'Enter') return;
        event.preventDefault();          // it is not in a form; make that plain
        if (showing.length) openCard(showing[0].card);
    });
    clear.addEventListener('click', function () {
        box.value = '';
        run();
        box.focus();
    });

    // A link from the contents page or from a page of the book ends in
    // #<chant id>. The browser scrolls to the card but leaves it SHUT, because
    // the id sits on the <details> itself rather than on something inside it —
    // so the reader arrived at the chant they asked for and saw it closed.
    function openFromHash() {
        var id = (window.location.hash || '').slice(1);
        if (!id) return;
        try { id = decodeURIComponent(id); } catch (e) { /* leave it as typed */ }
        var card = document.getElementById(id);
        if (card && card.classList.contains('chant-card')) {
            card.hidden = false;
            openCard(card);
        }
    }
    window.addEventListener('hashchange', openFromHash);

    // Shown only now that it works.
    panel.hidden = false;

    // The nav is sticky, and how tall it is depends on the width of the
    // window — two rows on a laptop, three on a phone. So measure it rather
    // than assume: a hard-coded offset parked this box behind the nav, and a
    // jumped-to chant behind both of them.
    var nav = document.querySelector('nav');
    function placeUnderNav() {
        var navHeight = nav ? Math.round(nav.getBoundingClientRect().height) : 80;
        var sticky = window.getComputedStyle(panel).position === 'sticky';
        if (sticky) {
            panel.style.top = (navHeight + 6) + 'px';
        } else {
            panel.style.top = '';
        }
        document.documentElement.style.setProperty(
            '--chant-jump-offset',
            (navHeight + (sticky ? panel.offsetHeight + 16 : 16)) + 'px');
    }
    window.addEventListener('resize', placeUnderNav);
    window.addEventListener('orientationchange', placeUnderNav);

    // ?q=metta opens the book already filtered, so a search can be bookmarked
    // or passed to someone else.
    var query = /[?&]q=([^&]*)/.exec(window.location.search);
    if (query) {
        try { box.value = decodeURIComponent(query[1].replace(/\+/g, ' ')); }
        catch (e) { /* a mangled link is not worth failing over */ }
    }
    run();
    openFromHash();
})();
