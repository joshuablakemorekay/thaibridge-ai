# v2 — Option B: enhanced CSS

> **Status:** verbatim from the saved chat.

```
Yes. Create Option B. Create Options C, D later
```

**What improved:** styling moved out of inline `<style>` blocks into external CSS files (`main.css`, `animations.css`, plus page-specific files), with a CSS-variable theming system and 50+ animations. `base.html` and `index.html` were updated to link the external stylesheets.

**Why it changed:** inline styles were hard to maintain — a variable-based system let me change the whole colour scheme in one place instead of editing every page.
