# Monk Mode — Syllabus (DRAFT for approval)

Content written **specifically for monastics**, serving both directions from the
same lessons:

- **Thai Buddhist monks learning English**
- **Western Buddhist monks learning Thai**

Every entry holds both languages, so one lesson works both ways — the direction
switch just decides which language is the *prompt* and which is the *answer*.

> 🙏 **Josh — please correct freely.** You are the monastic; I have drafted the
> Thai script, romanization and register as best I can, but treat every line as a
> draft to fix. Reorder, rename, add or cut topics as you see fit.

## Proposed topics (a gentle progression)

| # | Topic | Pāli | Why it matters |
|---|-------|------|----------------|
| 01 | **The Alms Round** | piṇḍapāta | Daily contact between saṅgha and laity — the first words a monk needs |
| 02 | **The Monastery & Requisites** | senāsana / parikkhāra | Names of places and objects: kuṭi, sālā, bowl, robe, the four requisites |
| 03 | **Respectful Address & Register** | — | How monks and laypeople address one another; titles (Ajahn, Luang Por, Bhante, Venerable) |
| 04 | **The Daily Routine** | — | Chanting, meditation, sweeping, meal time, observance (Uposatha) days |
| 05 | **Offering & Anumodanā** | dāna / anumodanā | Receiving offerings, giving blessings, making merit |
| 06 | **Greetings & Courtesies** | — | Meeting laypeople, añjali/wai, thanks, well-wishes |
| 07 | **Health & the Body** | gilāna-paccaya | Seeing a doctor, describing illness, medicine and what's allowable |
| 08 | **Dhamma & Teaching** | dhamma-desanā | Giving and receiving teachings; core Dhamma vocabulary |
| 09 | **Precepts & Allowables** | sīla / kappiya | Talking about precepts; what is offered and made allowable |
| 10 | **Travel & Life Abroad** | — | For Thai monks overseas: airport, immigration, being hosted |
| 11 | **Pronunciation Practice: L and R** | — | Tongue twisters from Josh's Thai teacher — the rice/lice problem; drills for both sounds |
| 12 | **Dhamma Reading: Ajahn Sumedho** | — | Three passages from *Direct Realization* with key teaching vocabulary and full-passage audio |
| 13 | **Pronunciation Practice: V, F and TH** | — | The other sounds the teacher flagged: V→W, final F→P, and TH→T/D/S |

Topics 11–13 add four optional sections beyond `vocab`/`phrases`:

- `drill_sections` — groups of English-only drill lines (`english`, `english_respell`,
  `english_ipa`, optional `english_tip_th`, `meaning_th`). No Thai prompt side —
  the point is saying the English sound.
- `passages` — whole readings (`id`, `title`, `intro_th`, `source`, `text`).
  Passage audio is keyed `passage <id>` (see scripts/generate_english_audio.py).
- `reading_guide` — how to read a passage rather than what to say: pause at the
  punctuation, read for meaning, then read again with vocal variety.
  (`title`, `intro_th`, `intro_en`, `tips[{en, th}]`.)
- `word_choices` — one idea, several English words, each with the shade of
  meaning it carries. (`title`, `intro_th`, `intro_en`, `sets[{concept, pali,
  options[{english, english_respell, english_ipa, nuance_th}]}]`.) Options get
  their own audio like any other entry.

### The teacher's principle behind topics 11–13

A word pronounced perfectly on its own slips straight back to the old habit once
it sits inside a sentence. So every pronunciation topic ends with a **From word
to sentence** drill section: the same sounds, now embedded in real sentences, as
the test of whether the sound is really learned.

## File format (one JSON file per topic)

```
content/monk/01_alms_round.json  → topic 01, and so on
```

Each file has a title/description in both languages, then `vocab` (single words)
and `phrases` (whole sentences). Every item carries:

- `thai` — Thai script
- `paiboon` — romanization in the app's **existing Paiboon+ system** *(helps the Western monk **say the Thai**)*. Must match the spellings already used across the app and its romanized dictionary — e.g. aspirated stops are written **without** an `h` (พ = `p`, ข = `k`, ถ/ท/ธ = `t`), ป = `bp`, ต = `dt`, ก = `g`, ง = `ŋ`, and vowels like ออ = `ɔɔ`, เออ = `əə`. Tones by diacritic: mid `a`, low `à`, falling `â`, high `á`, rising `ǎ`.
- `english` — the English meaning/equivalent
- `english_ipa` — **IPA** transcription *(helps the Thai monk **say the English**, e.g. `/mʌŋk/`)*. British/RP, non-rhotic.
- `pali` — the Pāli term, where one applies (blank otherwise)
- `note` / `context` — optional usage guidance

Who reads what:

| Reader | Prompt they see | Help they use |
|--------|-----------------|---------------|
| Western monk learning Thai | English | `thai` + `paiboon` |
| Thai monk learning English | Thai | `english` + `english_ipa` |

See `01_alms_round.json` for a worked example.

## Status

- [x] Syllabus approved
- [x] Format approved (thai · paiboon · english · english_ipa · pali · note)
- [x] **All 10 topics drafted** (100 vocab + 40 phrases) → **awaiting Josh's content review**
- [ ] Romanization / register / Pāli verified by Josh
- [ ] Wired into Monk Mode
- [ ] Committed
