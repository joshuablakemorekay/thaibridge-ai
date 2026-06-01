# v2 — Getting it actually running

> **Status:** close reconstruction (this thread was a back-and-forth of setup errors and fixes, not a single prompt).

Phase 1's code was correct, but getting it to run as a complete beginner on Windows took several fixes, in order:

1. **Python wasn't installed** — installed it (and ticked "Add Python to PATH").
2. **Flask wasn't installed** — `pip install flask`, then `anthropic`.
3. **API key only set for one terminal session** — it vanished when the terminal changed.
4. **Missing quote marks around the key** — Python read the raw `sk-ant-...` key as code and threw `NameError`. Wrapping it in quotes fixed that.
5. **Env var not reaching Flask's child process** — Flask's debug reloader spawns a second process that didn't inherit the key. Setting `os.environ['ANTHROPIC_API_KEY']` at the **very top of the file** (before other imports) made it work everywhere.

**A false "it works":** the server logs reported the AI as active while the browser still errored. I had to push back on the "it works!" claim and test it myself before it was genuinely working.

**The lesson:** small setup details (a missing pair of quotes, where you set an environment variable) break everything — and don't trust "done" until you've tested it yourself.
