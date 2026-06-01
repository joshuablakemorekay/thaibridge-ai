# v2 — Integrated into a single app.py

> **Status:** close reconstruction (the follow-up was "yes" to "shall I create the complete merged app.py for you").

After the snippet failed to run on its own, I asked for everything merged into one ready-to-run file:

```
yes
```

**What improved:** the gamification was integrated directly into `app.py`, so there was nothing to paste — just run the one file.

**What went wrong:** it crashed on startup with `AssertionError: View function mapping is overwriting an existing endpoint function: formality_guide` — there were **two `/formality` routes**. Removing the duplicate fixed it.
