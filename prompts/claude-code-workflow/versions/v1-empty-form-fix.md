# Task — Fix the empty-form submission bug

> **Status:** verbatim from the Claude Code session.

```
there's a bug where users can submit empty forms - fix it
```

**The fix:** the signup `<form>` had `novalidate` on it (which disables the browser's built-in validation), and none of the inputs had `required`. Claude Code removed `novalidate` and added `required` to all four fields — giving two independent validation layers:

1. **Browser (HTML5):** blocks empty fields natively, before JavaScript runs.
2. **JavaScript:** still handles the complex rules (username format, email regex, password strength, matching passwords).

**Lesson:** never rely on a single validation layer — defence in depth.
