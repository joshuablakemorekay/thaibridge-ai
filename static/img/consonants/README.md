# Consonant pictures

Pictures for the 44 Thai consonants, used on the **Alphabet** page — the detail
strip under the chart, the flashcard's reveal side, and the quiz's picture round.

**The 44-tile chart uses emoji, not these** — all 44 are on screen at once,
emoji cost nothing to load, and they are built to be legible at that size.

The exception is any letter flagged **`no_emoji`** in `thai_consonants.py`,
where no emoji exists for the meaning at all and the nearest one says something
actively wrong. Those tiles show the drawing instead. Currently two:

| Letter | Meaning | Why |
|--------|---------|-----|
| ฉ | ฉิ่ง hand cymbals | Unicode has no cymbals — 🥁 is a different instrument |
| พ | พาน offering tray | Unicode has no tray — 🏆 reads as a prize |

To add another, set `no_emoji=True` on that letter. No JavaScript to change.

Nothing in here is required. Every letter already has an emoji in
`thai_consonants.py`, and that emoji is what shows when there is no picture
file. Pictures are an upgrade, one letter at a time.

## Adding a picture

Name the file after the letter's **slug** and drop it in this folder. That's it —
no code to edit, no list to update. The page picks it up on the next page load.

The slug is the last string in each letter's row in `thai_consonants.py`, and it
is also the name of that letter's audio file:

| Letter | Meaning | Filename to use            |
|--------|---------|----------------------------|
| ก      | chicken | `kor-kai.webp`             |
| ข      | egg     | `khor-khai.webp`           |
| ค      | buffalo | `khor-khwai.webp`          |
| …      | …       | `<slug>.webp`              |

Accepted extensions, tried in this order: `.webp`, `.png`, `.jpg`, `.jpeg`,
`.svg`. So if both `kor-kai.webp` and `kor-kai.png` exist, the `.webp` wins —
handy for replacing a heavy PNG without deleting anything.

## What makes a good picture here

* **Square-ish**, and no bigger than about **400×400** — it is displayed at
  roughly 96–128px, so anything larger is wasted download on a phone.
* **`.webp` if you can**, for the file size. Any of the extensions above work.
* **Obvious at a glance.** A learner has to recognise it in a fraction of a
  second, with no caption, in the quiz.
* **Licensed for use.** Your own photo, or something clearly free to use
  commercially. If a picture needs crediting, add the credit line to the page
  before you add the file.

## The quiz round

The quiz's picture round only asks letters whose picture is unambiguous. Twelve
letters have emoji that are only *approximate* (ฝ "lid" falls back to 🍲, ฏ
"goad" to 🔱 — see the `emoji_approx` flags in `thai_consonants.py`), and those
are asked by letter or by sound instead, because naming a letter from 🍲 would
be an unfair question.

Dropping a **real** picture in here for one of those twelve fixes that
automatically: a genuine photo of a pot lid is unambiguous, so the letter joins
the picture round with no code change.
