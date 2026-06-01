# Reasoning: AI Tutor Integration (Claude API, 6 Modes)

## Goal

Add an AI tutor to the app powered by the **Claude API**, with multiple specialist modes — conversation practice, grammar tutoring, quiz generation, cultural context, Buddhist teachings, and smart hints. I wanted it built in **phases**, starting with the core chat system.

## Iteration history

**v1 — Phase 1 core system:** `ai_agent.py` (6 modes), a `chat.html` interface, and the integration routes for `app.py`.

**Then the setup struggle (the real story):** Python wasn't installed → then Flask wasn't installed → then my API key vanished because I'd only set it for one terminal session → then it broke because I'd **forgotten the quote marks** around the key in Python (so it was read as code, not text) → it finally worked when the key was loaded **at the very top of the file**, before other imports.

**A false "it works":** at one point the server logs said the AI was active, but the browser still errored — I had to correct the claim that it worked and test it properly.

**Romanization alignment:** the tutor's output was later pinned to the app's house style (cross-referenced in [`romanization-system`](../romanization-system/)).

## Failure modes the final version handles

- **Env var not inheriting** — Flask's debug reloader spawns a child process that didn't see the key set only in the terminal; fixed by setting it at the top of the file.
- **Missing quotes around the key** — Python treated the raw key as code (`NameError: sk... is not defined`).
- **Trusting "it works"** — the biggest lesson: don't trust "done" (even from an AI); test it yourself.

## Outcome

A working 6-mode AI tutor at `/chat`, powered by Claude. Building it cost nothing (versus the ~£/$20,000 a hired build was quoted at); the only running cost is API usage (~$10–50/month).

## What I'd change next

Move the API key out of the source — it ended up hardcoded at the top of `app.py` just to make it run, which isn't safe. And add the Phase 4 feature I deferred: pronunciation feedback (needs speech-to-text).

> **Note:** this tutor is a first working version. It may be further revised, developed, improved, or rebuilt as the app matures — the modes, prompts, and integration are all open to change.

## Tags

`claude-api` `agent-workflow` `tool-use` `integration` `prompt-engineering`
