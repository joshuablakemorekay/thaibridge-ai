# Reasoning: Paiboon+ Romanization System

## Goal

The romanization in this app is a **uniquely designed Paiboon+ system**, derived from the Paiboon transliteration system **used by Benjawan Poomsan Becker in her *Thai–English and English–Thai Three-Way Dictionary***. A good friend of mine, **Douglas J. Alford**, and I are **still actively developing and improving it** inside the app — it's a living part of the project, not a fixed import. The aim is to make Thai pronunciation genuinely learnable for English speakers: every Thai vowel gets a consistent character, and tone and vowel-length are marked accurately — the things the official RTGS romanization leaves out. Two practical build threads grew out of this: a **beginner mode** to remove a common misreading, and **display consistency** so the special characters render identically everywhere, including in the AI tutor.

## The vowel system (the heart of it)

The app represents the full set of Thai vowels with dedicated characters — short and long pairs — so the sound and length are unambiguous:

| Thai | Paiboon+ | Sound guide |
|------|----------|-------------|
| อะ | `a` | short "a" as in *bat* |
| อา | `aa` | long "aa" as in *naa* (น้า) |
| อิ | `i` | short "i" as in *bit* |
| อี | `ii` | long "ee" as in *see* |
| อึ | `ʉ` | short "er" — bite molar teeth & exaggerate saying "er" |
| อื | `ʉʉ` | long "churrr" / Thai *chʉʉ* — bite molars & exaggerate "churrr" |
| อุ | `u` | short "u" as in *tuk tuk* |
| อู | `uu` | long "oo" as in *moon* — pronounced "muuun" |
| เอะ | `e` | short "e" as in *ed* |
| เอ | `ee` | long "ay" as in *day* |
| แอะ | `ɛ` | short "e" as in *bed* — stretch mouth wide like a smile, open slightly, tongue on bottom lip, more exaggerated than "e" |
| แอ | `ɛɛ` | long "ɛɛ" as in *mɛɛ* (mother), or how a sheep goes "mɛɛ!" |
| โอะ | `o` | short "o" |
| โอ | `oo` | long "o" as in *go* |
| เอาะ | `ɔ` | short "aw" |
| ออ | `ɔɔ` | long "aw" as in *awwww* |
| เออะ | `ə` | short "er" as in *bird* |
| เออ | `əə` | long "errr" as in *birrrd* |

## Iteration history (the build threads on top of the system)

- **Beginner mode:** swap word-final single `i`→`y` and `o`→`w` (e.g. `bpai`→`bpay`, `gao`→`gaw`) so beginners don't read them as "ee"/"oh" — but **not** vowel combos (`chái`, `sǎao`) or double vowels (`dii`). Added as a toggle.
- **The `ɔ̌ɔ` display problem:** the two `ɔ` characters rendered at different sizes because of the combining tone mark. Tried line-height, font-weight, `geometricPrecision`, disabling ligatures — none fully worked.
- **The honest workaround:** it's fundamentally how computers combine accent characters, so I switched all romanization to a **monospace font (Roboto Mono)** to force equal character widths. Pragmatic, not perfect.
- **Make the AI tutor match:** *"Remove h in khâ & thîi. Replace ng with ŋ..."* — pinned the tutor's output to the app's house style (`khâ`→`kâ`, `ng`→`ŋ`, `thai`→`tai`).

## Failure modes the final version handles

- **Over-eager conversion** — beginner mode must *not* touch vowel combos (`ái`, `ao`) or double vowels (`dii`).
- **Uneven diacritics** — browsers' "smart" font rendering made combining tone marks inconsistent; monospace fixed the width.
- **Tutor drift** — the AI used a different romanization than the app until its instructions were pinned to this system.

## Outcome

A consistent, custom Paiboon+ vowel system running across the app, a working beginner-mode toggle, monospace rendering that keeps the special characters even, and an AI tutor that matches. Honest caveat: the `ɔ̌ɔ` consistency is a *workaround* (monospace), not a true typographic fix — and the system itself is still being refined.

## What I'd change next

This system is **still in active development** with my friend Douglas J. Alford — the next work is on the system itself: refining how a few vowels and tones are represented, and revisiting whether a better font or pre-composed Unicode could keep a nicer proportional look while staying perfectly consistent.

## Tags

`romanization` `paiboon` `language-design` `internationalization` `css` `work-in-progress`
