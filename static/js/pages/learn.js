// Moved out of templates/learn.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

function updateLinks() {
    const isBeginnerMode = document.getElementById('beginnerToggle').checked;
    const links = document.querySelectorAll('.category-link');

    links.forEach(link => {
        const category = link.dataset.category;
        if (isBeginnerMode) {
            link.href = `/exercise/${category}?beginner=true`;
        } else {
            link.href = `/exercise/${category}`;
        }
    });
}
