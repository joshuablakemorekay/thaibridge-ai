# v2 — Vowel display consistency (the ɔ̌ɔ saga)

> **Status:** verbatim from the saved chat.

```
Can you fix the problem with this vowel - ɔ̌ɔ? The symbols don't match for all
ɔɔ long vowel combinations. They should be the exact same size & shape
throughout.
```

and, to apply it everywhere:

```
Can you implement the fix for this vowel combination for the entire web app?
```

**The problem:** in `ɔ̌ɔ`, the first `ɔ` carries a combining tone mark, so the two characters rendered at different sizes.

**What didn't work:** increasing line-height, changing font-weight, `text-rendering: geometricPrecision`, disabling ligatures, switching proportional fonts. The user reported repeatedly that the vowels still looked different.

**The honest workaround:** combining diacritics in a *proportional* font will always vary in width — so all romanization was switched to a **monospace font (Roboto Mono)**, which gives every character the same width. Not a true typographic fix, but it makes the characters line up consistently across the whole app.
