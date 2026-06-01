# v3 — Make the AI tutor's romanization match the app

> **Status:** verbatim from the saved chat.

```
In AI Chat: Remove h in khâ & thîi. Replace ng with ŋ in yang-ngai...
Fix the IPA characters so they are same font + size.
```

**The problem:** the AI tutor was producing a *different* romanization than the rest of the app (e.g. `khráp`, `yang-ngai`, `thai`), which confused the consistency the system is built on.

**The fix:** the tutor's system prompt was pinned to the app's house style:
- drop the `h` after consonants — `khâ` → `kâ`, `khráp` → `kráp`
- use `ŋ` instead of `ng` — `yang-ngai` → `yaŋ-ŋai`
- `thai` → `tai`

**Why it mattered:** a learner should see *one* romanization everywhere. If the tutor spells a word differently from the lesson, the system stops being trustworthy.
