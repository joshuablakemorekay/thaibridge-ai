# Task — Refactor signup fetch to async/await

> **Status:** verbatim from the Claude Code session.

```
refactor the authentication module to use async/await instead of callbacks
```

**The change:** the only callback-style code in the auth flow was the `fetch` chain in `signup.html`. Claude Code converted it:

- `addEventListener('submit', function ...)` → `addEventListener('submit', async function ...)`
- `.then().then().catch()` → `await` inside a `try/catch`

The Flask backend is synchronous Python and had no callbacks to refactor. Same behaviour, cleaner and more readable code.
