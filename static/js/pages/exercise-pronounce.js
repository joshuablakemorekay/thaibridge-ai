// Moved out of templates/exercise.html, where it ran as an inline <script>.
// Values from the server now arrive in a JSON block on the page (a
// data block, which never runs), so the Content-Security-Policy can
// refuse inline scripts (see security_headers.py).

// Pronunciation Analysis (Pro). The words are the ones with a model clip.
const PRON_WORDS = JSON.parse(document.getElementById('pron-words').textContent);
function loadPronounce() {
    const box = document.getElementById('quizContent');
    if (!window.Pronounce || !Pronounce.supported) {
        box.innerHTML = '<p style="text-align: center;">Pronunciation practice needs a microphone and a current browser (Chrome, Edge, Safari or Firefox).</p>';
        return;
    }
    Pronounce.mount(box, PRON_WORDS);
}
