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
