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
