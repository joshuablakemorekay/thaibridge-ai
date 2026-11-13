// Moved out of templates/partials/thai_audio_wiring.html, where it ran as an inline
// <script>. Kept in a file so the Content-Security-Policy can refuse
// inline scripts (see security_headers.py).

(function () {
  var map = JSON.parse(document.getElementById('ta-audio-map').textContent);
  function wire(root) {
    (root || document).querySelectorAll('.thai-text').forEach(function (el) {
      if (el.dataset.audioWired) { return; }
      var url = map[el.textContent.trim()];   // exact match — pure-Thai cells only
      if (!url) { return; }
      el.dataset.audioWired = '1';
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'th-audio ta-listen';
      b.setAttribute('data-audio', url);
      b.setAttribute('aria-label', 'Listen');
      b.textContent = '🔊';
      el.appendChild(b);
    });
  }
  window.wireThaiAudio = wire;   // for pages that add .thai-text after load
  document.addEventListener('DOMContentLoaded', function () { wire(document); });
})();
