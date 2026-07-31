# v1 — Two stages, labelled-text output

> **Status:** verbatim from the Claude Code session, 2026-07-31.

## The brief

```
Can you give me a prompt for Claude.ai chat that consistently and accurately
produces the output I want which will then be pasted as an input in Claude Code
sessions.
```

```
Here is the job step by step: 1. I copy and paste Thai script from an official
chanting book into Claude.ai because apparently it is better quality than Chat
GPT for this sort of work. [...] 2. I then paste the Claude.ai output into
Claude Code and ask Claude Code to add this as a new chant to the Digital
Chanting Book in the app following the same structure and everything as the
first chant I added which currently exists in the app Digital Chanting Book.

So can you give me a prompt for Claude Code as well as to achieve the second
step in the process.
```

The two-surface split came from the brief, not from me: stage 1 does the
language work in a chat window, stage 2 does the file work in an agent. It also
puts a human checkpoint between them, which is where the Pali gets verified
against the physical book.

## The register, researched before any prompt was written

```
It's mostly Central Thai, but it uses a formal literary register that is
traditional in Buddhist scriptures and chanting books. It is not Royal Thai, and
it is not a separate "monk language."

Buddhist literary vocabulary — uses older, formal words common in temples and
scriptures. Examples: บุคคล (person) instead of คน, ตัณหา (craving), ดับสนิท
(completely extinguished), พระอริยเจ้า (Noble One).

Traditional style — the wording is often more elegant or archaic than everyday
conversation. For example: เบื้องบนแต่พื้นเท้าขึ้นมา instead of the more
conversational ตั้งแต่ฝ่าเท้าขึ้นมา.

Overall: Think of it as the Thai equivalent of the language used in an English
Bible or the Book of Common Prayer—recognizably modern English, but more formal,
traditional, and rich in religious vocabulary. which is important.
```

That last clause — *which is important* — is why register is a section of the
prompt rather than a passing note.

## What v1 established, and what survived every later version

- **The five layers are not interchangeable.** A chanting book prints two
  different things that both look like Thai script — Pali *in* Thai script, and
  the Thai translation. Confusing them corrupts the entry.
- **Never reconstruct from memory.** Four OCR errors had already been caught by
  reading chant 1 against the physical book.
- **Flag, don't guess.** Anything unclear gets a `⚠️ CHECK`.
- **Hold the register.** No modernising, in Thai or in English.

## Output format

Labelled plain text — `TITLE_THAI:`, `VERSE 1`, `pali:`. Readable by a human,
but stage 2 had to parse it by eye. That became the reason for v3.

## Caught immediately

The sample output supplied as a layout example used a different romanisation
from the app's Paiboon+ — `sangkhaan` where the app has `sǎŋ-kǎan`. v1 pinned
the convention to a consonant table to stop it leaking in.
