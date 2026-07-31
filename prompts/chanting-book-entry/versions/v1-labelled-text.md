# v1 — Two stages, labelled-text output

> **Status:** verbatim from the Claude Code session, 2026-07-31.

```
Can you give me a prompt for Claude.ai chat that consistently and accurately
produces the output I want which will then be pasted as an input in Claude Code
sessions. [...] So can you give me a prompt for Claude Code as well as to
achieve the second step in the process.
```

**The two-surface split.** Stage 1 in Claude.ai does the language work —
transliteration, romanisation, translation, background. Stage 2 in Claude Code
writes it into `chanting.py` and verifies it renders. The split is deliberate:
it puts a human checkpoint in the middle, which is where the Pali gets verified
against the physical book.

**What v1 established, and what survived every later version:**

- **The five layers are not interchangeable.** A chanting book prints two
  different things that both look like Thai script — Pali *in* Thai script, and
  the Thai translation. Confusing them corrupts the entry.
- **Never reconstruct from memory.** Four OCR errors had been caught by reading
  chant 1 against the physical book; a model asked to tidy those would have
  rewritten the text into something plausible and wrong.
- **Flag, don't guess.** Anything unclear gets a `⚠️ CHECK` rather than a
  confident invention.
- **The register.** Formal literary Buddhist Thai, "the Thai equivalent of the
  language used in an English Bible or the Book of Common Prayer".

**Output format:** labelled plain text — `TITLE_THAI:`, `VERSE 1`, `pali:` and
so on. Readable by a human, but stage 2 had to parse it by eye.

**Caught immediately:** the sample output supplied as a layout example used a
different romanisation from the app's Paiboon+ — `sangkhaan` where the app has
`sǎŋ-kǎan`. v1 pinned the convention to a consonant table to stop it leaking in.
