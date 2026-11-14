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
