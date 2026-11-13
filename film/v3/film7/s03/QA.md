# s03 QA: film 7, shot 3 (the kiosk fills with Mona Lisa front pages, the newsboy shouting)

Delivered: `frames/` (g 132..239, 108 frames, 720x1280, 12 samples, 2 threads, denoise FAST) and `take.mkv` (libx264rgb crf 6, 30 fps,
**first_g 132, n_frames 108**). g 138..233 = shot 3 (plan 4.60-7.80 s); g 132..137 in-handle, g 234..239 out-handle (rendered in 3D).
transition_in = cut; out = dissolve (shot 4 dissolves in per plan; the 6-frame out-handle covers a dissolve up to 12 frames).
Also `meta.json`, `cues.json`, `contact.jpg` (cyan line y 880), `compare.jpg` (g 170 beside ref a t0056, a sunny street of stalls; g 215
beside ref a t0085, a character close to the lens in a street). Scripts `shot.py`, `deliver.py`, `qa.py`; `../common.py` untouched.
Drafts `work/d1..d4.jpg`.

## Set-ups (framing change at g 186 = 6.20 s, 1.6 s into the shot)
| id | g | what |
|---|---|---|
| 1 | 132..185 | the sunlit "JOURNAUX" kiosk front: `set_papers` keyed 0 until g 141, then 1 -> 24 one every ~2.3 frames (g 142..196: kiosk front 8, sides 4, Morris column 6, shop walls 6); the newsboy right of the kiosk waving the front page and shouting; push in (22 mm) |
| 2 | 186..239 | closer and a little low (camera z 1.85) on the newsboy: front page held high, the kiosk wall of front pages and the column behind; slow push (24 mm) |
Flash-forward: this is the one shot before 17 that may show the theft headlines (common.py gotcha), so papers go 0 -> 24 here.
Captions: "และการขโมย" 4.24 s, "ครั้งนั้นแหละ" 4.93 s (g 151, papers filling), "คือเหตุผลที่" 5.79 s, "มันดังที่สุด" 6.63 s (g 202: close on
the shouting boy, all 24 papers up), "ในโลก" 7.37 s.

## Client rules
- **No depth of field** (C.Take). Every front page, the masthead lettering, the facades: sharp.
- **Heads**: id 1 head centre y 657..664 (0.51-0.52 H), id 2 692..697 (0.54 H); no head bottom below 880.
- **Mouths**: the newsboy's shout is a HELD open mouth (`("open", 0.17, 0.20)` every frame), no lip-sync, as the plan asks.
- **Dense set**: kiosk with 8+4 front pages, gas lamp, Morris column, shop fronts (TABAC, LIBRAIRIE), balconies, trees.
- The kerb gas lamps are keyed low (`set_flames(0.3)`, daytime) -- the kiosk lamp globe still reads as a lit yellow globe at the top of frame.

## Checks (`work/qa.txt`)
Popcheck: one jump, the planned framing change 185 -> 186. No near-still pairs, no black / magenta frames, no retried frames.
Late in id 1 (g ~175-185) the push brings the newsboy's head to x 653 +- 76 px: its right edge touches the frame edge (a few px cut).

## Colour (hue_report rows)
```
s03 id 1 (g 132-185)   red 35.9 orange 30.0 blue 20.1 violet 2.8 magenta 3.0  sat 0.37 val 0.46 dark 0.25
s03 id 2 (g 186-239)   red 35.8 orange 28.0 blue 26.4 violet 3.4 magenta 3.1  sat 0.35 val 0.48 dark 0.17
```
Warm sun on the kiosk side, blue shade on the facades (hue ~225, no magenta). Saturation slightly under the ref band, like every louvre.py
preset (louvre_API 7); dark 0.25 in id 1 is the kiosk's dark green body in shade. Not graded here.

## Seconds per frame
13.7 s wall / 26.3 s CPU mean (2 threads, two render processes at once).

## Differences from the plan / notes
- A passing lady was tried in id 2 and dropped (she hid behind his raised front page or left frame at once): `WITH_LADY = False` in shot.py.
- The newsboy is a `newsboy_shout` pose with a small wave of the paper arm, lean and head roll (no walk).
