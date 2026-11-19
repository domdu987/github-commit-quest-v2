# Phase 2: story and script

The user judges the story against the reference as closely as the picture. "Is the story like the clips I sent?" was asked directly, and the honest answer for the first script was "7 of 12 elements".

## Extract the formula from the reference transcripts

Write each reference's beat sheet, then list the elements they share. The two first references shared these twelve:

1. Cold-open hook: "He" plus a strange physical act, one sentence.
2. A spoken pivot ("You see, ...") that sets the world and the stakes.
3. The hero is the youngest or smallest person in the room.
4. The authority mocks him in a quoted line.
5. The hero persists and keeps acting.
6. A mocking nickname for his odd thing, used as a running thread.
7. A false defeat: the world seems to prove him wrong.
8. A second mocking quote at the false defeat.
9. The turn: "Meanwhile, ..." or "Then one night, ...".
10. The disaster lands on the doubters, shown as one physical image, no casualty count, no aftermath.
11. The mechanism reveal: a simple physical explanation of why his odd thing was right.
12. It ends on an image or on the last line of the reveal. No moral.

Texture to copy as well: short spoken sentences, countable concrete details, a running object the viewer watches change, wry understatement, a hero who almost never speaks, a narrator who never judges, about 200 to 216 English words per minute.

A new reference style needs its own list. Do not assume these twelve.

## Where each element lands (timing)

Sentence start times in seconds (share of the runtime in brackets). Reference: from the speech-to-text word times of the two clips (`__PROJ__/audio/refaudio/a.asr_events.json`, `b.asr_events.json`; the reference text is not quoted here); both run about 65 s. Film 1: the sentence starts of `narration_timing.json` with the `beat` of each sentence in `script_th_v2/script_th.json` (65.4 s).

| Element | Reference A | Reference B | Film 1 |
|---|---|---|---|
| 1 hook (one sentence) | 0.1-3.4 (3.3 s) | 0.1-7.3 (7.2 s, with a quoted dare) | 0.0-4.3 (21 syllables) |
| 2 pivot "You see" | 3.4 (5 %) | 7.3 (11 %) | 4.3 (7 %) |
| setup / authority | 3.4-11.7 | 13.5 (21 %) | 9.0 and 13.4 |
| 3 youngest hero and the boss's reaction | 11.7 (18 %) | | 16.8 (26 %) |
| 4 first mocking quote | 18.2 (28 %) | | 20.3 (31 %) |
| 5 persists | 18.2-21.7 | 17.8 (false defeat comes first) | 23.1 (35 %) |
| rivals win / they laugh harder | 21.7-31.3 | 22.4 (34 %) | |
| 6 nickname given | 31.3 (48 %) | 24.2 (37 %) | 26.4 (40 %) |
| hero alone | | 29.5 (45 %) | |
| 7 false defeat / "something weird" | 36.1-45.7 (56-70 %) | 17.8 (27 %) | 31.9 (49 %) |
| 8 second mocking quote | 45.7 (70 %) | 40.5 (62 %) | 36.2 (55 %) |
| 9 the turn ("Meanwhile" / "Then one night") | 46.3 (71 %) | 32.9 (51 %) | 39.6 (61 %) |
| build to the peak | 54.4 (84 %) | 37.1 (57 %) | 44.2-54.2 (mechanism, 68-83 %) |
| 10 disaster image | 59.4-65.0 (91 %) | 45.9 (71 %) | 54.2 (83 %) |
| 11 mechanism reveal | inside the build (46-59) | 48.6-58.4 (75-90 %) | 44.2-54.2, before the disaster |
| 12 last line or image | 59.4 | 58.4-64.8 | 59.6-65.4 |

Rules of thumb from these numbers:
- The hook is one sentence of 3 to 7 s; the pivot follows at once (5-11 %).
- The first quote by about 30 %; the nickname at 37-48 %; the turn at 51-71 %; the disaster at 71-91 %.
- After the disaster: either end within about 6 s on the disaster image (A), or reveal the mechanism and end on its last line (B, 19 s). Film 1 put the mechanism before the disaster and ended 11 s after it.
- Nickname: the references say it 2 times (A: the name once, B: the naming and the second quote); film 1 used it 4 times (`nickname_uses`). Use it at least at the naming and in the second quote.
- Size: reference 214 (A) and 235 (B) English words in 65 s; film 1 313 Thai syllables in 65.4 s (speed 1.2, tempo 1.19). For a 60 s Thai film plan about 290 syllables (inferred, pro rata).
- Only the quoted lines move a mouth; no casualty figure; no moral; end on an image.

## Choosing the story

Pick a true story that has an odd visible object, a doubting authority, a false defeat and a physical mechanism to reveal. Keep a fact list and a separate list of allowed dramatisations (the references dramatise freely: invented quotes, a nickname, a repeated gag). Tell the user which parts are fact and which are dramatised.

## Writing it

Template: `workflows/05_script_by_formula.js`.
- Three writers: mirror reference A beat for beat, mirror reference B beat for beat, best of both in the target language.
- Three judges: formula match element by element with the exact sentence quoted for each element; native ear (read aloud at speed, flag anything that sounds translated); facts, length and captions.
- One editor merges; one adversarial checker re-derives the beat sheets and re-checks all elements, facts, length and spelling, and repairs.
- Write directly in the target language. Translating an approved English script gave correct but translated-sounding Thai.

## What to deliver per sentence

- `tts`: exactly what the voice says, written for a speech engine: no digits, no Latin letters, numbers and years spelled the way a narrator says them, a space where the narrator pauses.
- `captions`: the same sentence cut into on-screen phrases, each one short breath unit (4 to 14 Thai characters, or 1 to 3 English words), never splitting a word, digits allowed where a viewer expects them.
- `beat` and the formula elements it carries.

Length: count syllables with a tool (pythainlp for Thai) and measure one real read before locking the picture; speech engines read slower than estimates. 313 Thai syllables needed speed 1.2 plus a tempo of 1.19 to land in 65 seconds.

Adapt for the audience: local units (kilometres per hour), local spellings of place names, but keep on-screen text in the story's own language when the setting is foreign.
