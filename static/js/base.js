        // Dropdown menu functionality
        function toggleDropdown(button) {
            const dropdown = button.parentElement;
            const allDropdowns = document.querySelectorAll('.dropdown');
            
            // Close other dropdowns
            allDropdowns.forEach(d => {
                if (d !== dropdown) {
                    d.classList.remove('active');
                }
            });
            
            // Toggle current dropdown
            dropdown.classList.toggle('active');
        }
        
        // Close dropdowns when clicking outside
        document.addEventListener('click', function(event) {
            if (!event.target.closest('.dropdown')) {
                document.querySelectorAll('.dropdown').forEach(d => {
                    d.classList.remove('active');
                });
            }
        });
        
        // Mobile menu toggle
        function toggleMobileMenu() {
            const nav = document.getElementById('main-nav');
            nav.classList.toggle('active');
        }
        
        // Collapsible section functionality
        function toggleSection(element) {
            const section = element.closest('.collapsible-section');
            section.classList.toggle('active');
        }
        
        // Initialize all collapsible sections
        document.addEventListener('DOMContentLoaded', function() {
            // Add click handlers to all section headers
            document.querySelectorAll('.section-header').forEach(header => {
                header.addEventListener('click', function() {
                    toggleSection(this);
                });
            });
            
            // Open first section by default on each page
            const firstSection = document.querySelector('.collapsible-section');
            if (firstSection) {
                firstSection.classList.add('active');
            }
        });
        
        // Gender selection functionality
        function setGender(gender) {
            // Update button states
            document.querySelectorAll('.gender-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(gender + '-btn').classList.add('active');
            
            // Save to session via AJAX
            fetch('/set-gender/' + gender)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Reload page to update gendered content
                        location.reload();
                    }
                })
                .catch(error => console.error('Error setting gender:', error));
        }
        
        // Set initial active state based on current gender
        document.addEventListener('DOMContentLoaded', function() {
            const currentGender = window.CURRENT_GENDER || 'neutral';
            if (currentGender) {
                document.querySelectorAll('.gender-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                const activeBtn = document.getElementById(currentGender + '-btn');
                if (activeBtn) {
                    activeBtn.classList.add('active');
                }
            }
        });

        // Wrap each content table in a horizontal-scroll container. The table
        // keeps width:100% so it fills the column when there's room (and grows
        // to fill as you zoom out); the wrapper only shows a sideways scrollbar
        // when the content is genuinely wider than the available space.
        document.addEventListener('DOMContentLoaded', function() {
            document.querySelectorAll('main table').forEach(function(table) {
                if (table.parentElement.classList.contains('table-scroll')) return;
                const wrapper = document.createElement('div');
                wrapper.className = 'table-scroll';
                table.parentNode.insertBefore(wrapper, table);
                wrapper.appendChild(table);
            });
        });

        // Site-wide 🔊 audio buttons.
        // =============================
        // Any element with class "th-audio" and a data-audio="<url>" plays that
        // clip when tapped. This is delegated on the document, so it works for
        // buttons added to any page (present now or rendered later) without each
        // page wiring up its own player.
        //
        // Rules borrowed from the alphabet page, each learned from a real iOS
        // failure: ONE Audio object for the whole page (a fresh one per play
        // leaks decoders on iOS until sound dies), and every play follows a tap
        // (iOS refuses to play sound nobody asked for). A rejected play() is
        // swallowed — a quiet button beats an unhandled console error.
        (function () {
            var player = null;            // created on first tap, then reused
            var playingButton = null;

            function clearPlaying() {
                if (playingButton) {
                    playingButton.classList.remove('is-playing');
                    playingButton = null;
                }
            }

            document.addEventListener('click', function (event) {
                var button = event.target.closest('.th-audio');
                if (!button) return;

                var url = button.getAttribute('data-audio');
                if (!url) return;

                event.preventDefault();

                if (!player) {
                    player = new Audio();
                    player.addEventListener('ended', clearPlaying);
                    player.addEventListener('error', clearPlaying);
                }

                clearPlaying();
                button.classList.add('is-playing');
                playingButton = button;

                player.src = url;
                var attempt = player.play();
                if (attempt && typeof attempt.catch === 'function') {
                    attempt.catch(clearPlaying);
                }
            });
        })();

        // Reading Support (accessibility settings)
        // ========================================
        // Three independent toggles that make text easier to read for learners
        // who struggle with it (e.g. dyslexia): an easy-to-read font, bigger
        // text, and extra spacing. Each just adds or removes an "rs-<name>"
        // class on the <html> element, which the CSS reacts to. Choices are
        // stored in localStorage so they persist across pages and visits on
        // this device — no server, no login needed.
        //
        // Note: the <head> script in base.html already applies saved choices
        // before first paint (to avoid a flash). This block handles the
        // interactive part: reflecting saved state in the checkboxes and saving
        // changes as the user toggles them.
        (function () {
            var KEY = 'tb-reading-support';
            var OPTIONS = ['font', 'large', 'spacing'];

            function load() {
                try { return JSON.parse(localStorage.getItem(KEY) || '{}'); }
                catch (e) { return {}; }
            }
            function save(settings) {
                try { localStorage.setItem(KEY, JSON.stringify(settings)); }
                catch (e) { /* storage off: choices just won't persist */ }
            }
            function apply(settings) {
                var el = document.documentElement;
                OPTIONS.forEach(function (name) {
                    el.classList.toggle('rs-' + name, !!settings[name]);
                });
            }

            document.addEventListener('DOMContentLoaded', function () {
                var settings = load();
                apply(settings);

                OPTIONS.forEach(function (name) {
                    var box = document.getElementById('rs-' + name);
                    if (!box) return;
                    box.checked = !!settings[name];
                    box.addEventListener('change', function () {
                        settings[name] = box.checked;
                        save(settings);
                        apply(settings);
                    });
                });

                var reset = document.getElementById('rs-reset');
                if (reset) {
                    reset.addEventListener('click', function () {
                        settings = {};
                        save(settings);
                        apply(settings);
                        OPTIONS.forEach(function (name) {
                            var box = document.getElementById('rs-' + name);
                            if (box) box.checked = false;
                        });
                    });
                }
            });
        })();

        // Read aloud (text-to-speech)
        // ===========================
        // Reads ENGLISH text aloud using the browser's built-in voice (the Web
        // Speech API) — no server, no cost. Helps dyslexic, low-vision and
        // tired readers.
        //
        // The learner chooses WHAT gets read from the dropdown next to the
        // button, so they are never stuck listening to a whole page:
        //   page      — everything in <main>, top to bottom
        //   section   — they click one paragraph/heading/list on the page and
        //               only that is read ("pick mode")
        //   selection — whatever text they have highlighted
        // The choice is remembered on this device.
        //
        // Three deliberate choices:
        //  - Thai characters are stripped out before speaking. Browser voices
        //    read Thai poorly, and Thai already has its own native-recorded
        //    audio buttons elsewhere, so we keep this to clean English.
        //  - Text is split into sentence-sized chunks and queued. Chrome cuts a
        //    single long utterance off after a few seconds; short queued chunks
        //    are the standard way around that.
        //  - The last highlight is remembered as it happens, because clicking
        //    the button clears the page selection in most browsers.
        (function () {
            var synth = window.speechSynthesis;
            var SCOPE_KEY = 'tb-read-scope';
            // Blocks a learner can click on in "pick mode". Kept to things that
            // hold a readable chunk of text on their own.
            var READABLE = 'p, li, h1, h2, h3, h4, h5, h6, blockquote, td, th, dd, dt, figcaption';
            // The hint line under the button always tells the learner what to do
            // next for the choice they are on — no need to read a manual first.
            var HINTS = {
                page: 'Press the button to hear the whole page. English only — Thai has its own audio buttons.',
                section: 'Press the button, then click the paragraph or heading you want to hear.',
                selection: 'Highlight the text you want on the page, then press the button.'
            };

            var button = null;
            var scopeSelect = null;
            var hint = null;
            var lastSelection = '';
            var picking = false;

            function setHint(message) {
                if (hint) hint.textContent = message;
            }
            function setSpeaking(on) {
                if (!button) return;
                button.textContent = on ? '⏹ Stop reading' : '🔊 Read aloud';
                button.classList.toggle('is-speaking', on);
            }
            function stripThai(text) {
                return text.replace(/[฀-๿]+/g, ' ').replace(/\s+/g, ' ').trim();
            }
            function stop() {
                if (synth) synth.cancel();
                setSpeaking(false);
            }
            function mainEl() {
                return document.querySelector('main') || document.body;
            }
            function scope() {
                return scopeSelect ? scopeSelect.value : 'page';
            }
            function resetHint() {
                setHint(HINTS[scope()] || HINTS.page);
            }

            function speak(source) {
                var text = stripThai(source || '');
                if (!text) {
                    setHint('There was no English text to read there.');
                    return;
                }
                var chunks = text.match(/[^.!?]+[.!?]*/g) || [text];
                setSpeaking(true);
                chunks.forEach(function (chunk, i) {
                    var part = chunk.trim();
                    if (!part) return;
                    var u = new SpeechSynthesisUtterance(part);
                    u.lang = 'en-GB';
                    u.rate = 0.95;
                    if (i === chunks.length - 1) u.onend = function () { setSpeaking(false); };
                    u.onerror = function () { setSpeaking(false); };
                    synth.speak(u);
                });
            }

            // --- Pick mode: click any part of the page to hear just that part ---
            function closeMenus() {
                document.querySelectorAll('.dropdown').forEach(function (d) {
                    d.classList.remove('active');
                });
                var nav = document.getElementById('main-nav');
                if (nav) nav.classList.remove('active');
            }
            function onPick(event) {
                if (event.target.closest('.reading-support')) return;   // panel clicks pass through
                event.preventDefault();                                 // don't follow links mid-pick
                event.stopPropagation();

                var inMain = mainEl().contains(event.target);
                var block = inMain ? event.target.closest(READABLE) : null;
                exitPickMode();
                if (!block) {
                    setHint('That part has no text — press Read aloud and try again.');
                    return;
                }
                speak(block.innerText);
            }
            function onPickKey(event) {
                if (event.key === 'Escape') {
                    exitPickMode();
                    setHint('Cancelled.');
                }
            }
            function enterPickMode() {
                picking = true;
                document.documentElement.classList.add('rs-picking');
                document.addEventListener('click', onPick, true);
                document.addEventListener('keydown', onPickKey, true);
                if (button) button.textContent = '👆 Click a part of the page';
                setHint('Click the paragraph or heading you want. Esc to cancel.');
                closeMenus();
            }
            function exitPickMode() {
                picking = false;
                document.documentElement.classList.remove('rs-picking');
                document.removeEventListener('click', onPick, true);
                document.removeEventListener('keydown', onPickKey, true);
                setSpeaking(false);
            }

            function readAloud() {
                if (!synth) return;                 // very old browser: no voice
                if (picking) { exitPickMode(); setHint('Cancelled.'); return; }
                if (synth.speaking || synth.pending) { stop(); return; }

                if (scope() === 'section') { enterPickMode(); return; }

                if (scope() === 'selection') {
                    var live = window.getSelection ? String(window.getSelection()) : '';
                    var chosen = (live && live.trim()) ? live : lastSelection;
                    if (!chosen.trim()) {
                        setHint('Highlight some text on the page first, then press this again.');
                        return;
                    }
                    speak(chosen);
                    return;
                }

                speak(mainEl().innerText);
            }

            // Remember highlights as they happen — clicking the button afterwards
            // clears the selection in most browsers.
            document.addEventListener('selectionchange', function () {
                var text = window.getSelection ? String(window.getSelection()) : '';
                if (text && text.trim()) lastSelection = text;
            });

            document.addEventListener('DOMContentLoaded', function () {
                button = document.getElementById('rs-read');
                scopeSelect = document.getElementById('rs-read-scope');
                hint = document.getElementById('rs-read-hint');
                if (!button) return;

                var group = button.closest('.rs-read-group');
                if (!window.speechSynthesis) {       // no support: hide the whole thing
                    if (group) group.style.display = 'none';
                    return;
                }

                if (scopeSelect) {
                    try {
                        var saved = localStorage.getItem(SCOPE_KEY);
                        if (saved) scopeSelect.value = saved;
                    } catch (e) { /* storage off: just use the default */ }

                    scopeSelect.addEventListener('change', function () {
                        try { localStorage.setItem(SCOPE_KEY, scopeSelect.value); }
                        catch (e) { /* storage off: choice just won't persist */ }
                        if (picking) exitPickMode();
                        stop();
                        resetHint();
                    });
                }
                resetHint();     // match the choice restored from last time

                button.addEventListener('click', readAloud);

                // "Turn all off" should also silence the voice and drop out of
                // pick mode, not just clear the visual toggles.
                var reset = document.getElementById('rs-reset');
                if (reset) {
                    reset.addEventListener('click', function () {
                        if (picking) exitPickMode();
                        stop();
                        resetHint();
                    });
                }
            });

            // Never keep talking after the user leaves the page.
            window.addEventListener('beforeunload', function () {
                if (synth) synth.cancel();
            });
        })();
