# Reasoning: Translator Mode

## The decision that shaped everything: a mode, not a page

The tutor in `ai_agent.py` builds every reply from a shared prompt (ThaiBridge
Spelling, the politeness rules from `thai_registers.py`, the consonant classes)
plus one block per mode. Adding a `translator` block meant the translator got all
of that on day one, and `app.py` needed no new gate at all: any mode not on
`FREE_AI_ALLOWED_MODES` is already Pro-only. The change to `app.py` is two lines
of wording.

## What the translator prompt asks for, and why

- **Neutral politeness by default, "I" dropped.** That is the teacher's own
  example from the same day (จะทำทีหลังนะคะ/ครับ, "Will do it later"), and the
  safe level with anyone.
- **ครับ/ค่ะ both shown.** The tutor does not know the speaker's gender, and
  guessing would be wrong half the time.
- **The monk swap by reference, not by copy.** The first draft listed ถวาย and
  นิมนต์ in the translator prompt. An existing test,
  `test_rules_read_from_one_place_only`, failed it: monk vocabulary lives in
  `thai_registers.py` alone so two copies cannot drift. The prompt now points at
  those rules instead.
- **"Never invent a word you are unsure of."** A learner cannot check the Thai,
  so a confident wrong answer is the worst failure.

## How it was checked

Four new cases in `evals/tutor_accuracy.yaml`, asked of the real model:

1. Offering food to a monk must use ถวาย, not ให้.
2. "Will do it later" must keep ครับ/ค่ะ.
3. "Are you hungry?" must use มั๊ย, the app's spelling.
4. กินข้าวรึยัง must come back in English, not be answered in Thai.

The first run scored 3/4, and the failure was **the check's fault**: the answer
translated with มั๊ย and then said "books write ไหม", exactly as the rules ask,
and the check banned ไหม anywhere. The check was narrowed to the translation
itself (หิวไหม). The same answer also spelt the particle ค๊ะ instead of คะ, a
real mistake, so that is now checked too. The rerun passed.

## The bug the fixture found

Recording a real answer for the CI fixture turned up something the exam had
missed. Asked to offer food to a monk, the translator began ผมอยากถวาย...,
wrote "no wait, here is the clean version" and started again. Repeated runs
did it about one time in three, with "Actually, the clean version is" too.

The shared prompt already says never to correct yourself partway through.
Translator mode needed it as a shape, not just a rule: the first line must be
the one finished Thai sentence in bold, and a second good wording goes after
it as an alternative rather than replacing it. Streaming makes this matter
more, because the learner watches every word arrive. The monk case now fails on
"no wait", "clean version" or "actually,", and passed six runs out of six, then
all four cases together.

Turning thinking on for this mode would fix the cause more surely, but it costs
more per message and changes the request every mode shares, so it was left as a
decision for later rather than slipped in here.

## What it does not do

- **No audio.** The phrase-audio system plays recorded phrases; spoken
  translations would need a text-to-speech service. Left for later.
- **No review.** Its Thai has not been checked by the teacher, so the chat shows
  "AI translation, may not be perfect" whenever Translator mode is on.
