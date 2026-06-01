# v3 — Option C: JavaScript interactivity

> **Status:** verbatim from the saved chat.

```
Yes, lets do Option C now. Do Option D later
```

**What improved:** added the interactive layer — `app.js` and `quiz.js` plus `interactive.css` — bringing flashcards with flip animations, progress saving to LocalStorage, confetti celebrations, sound effects, keyboard navigation (1–4 to answer), toast notifications, and a stats dashboard.

**What I learned later:** this layer is also where the front-end bugs lived — a broken `exercise.html` (CSS leaked outside its block) caused an "Internal Server Error" on the practice pages, which I had to fix before the interactivity worked.
