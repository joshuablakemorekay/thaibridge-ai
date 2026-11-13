// Moved out of templates/grammar.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
  var map = JSON.parse(document.getElementById('gr-audio-map').textContent);
  document.querySelectorAll('.thai-text').forEach(function (el) {
    if (el.dataset.audioWired) { return; }
    var url = map[el.textContent.trim()];   // exact match — pure-Thai cells only
    if (!url) { return; }
    el.dataset.audioWired = '1';
    var b = document.createElement('button');
    b.type = 'button';
    b.className = 'th-audio gr-listen';
    b.setAttribute('data-audio', url);
    b.setAttribute('aria-label', 'Listen');
    b.textContent = '🔊';
    el.appendChild(b);
  });
})();
