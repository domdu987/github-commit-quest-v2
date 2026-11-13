# s17 QA: film 4, shot 17 (NIGHT, the pagoda sways like a snake but stands), pagoda set v2, render worker 4

Delivered: `take.mkv` = `frames/g_1515.png .. g_1606.png` (92 frames, 720x1280, 12 samples, 2 threads; meta.json first_g 1515, n_frames 92).
g 1522..1599 = shot 17 ([50.73, 53.32) s); g 1515..1521 = 7-frame in-handle (dissolve from shot 16), g 1600..1606 = 7-frame out-handle,
both rendered in 3D (camera, sway and quake continue). Also `meta.json`, `cues.json` (5 cues), `contact.jpg`, `compare.jpg`, `work/hue.txt`.
Scripts: `shot.py` (one engine for shots 17-20, the same file in s17 / s18 / s20), `deliver.py`. Drafts: `work/d1..d5`.

## Timing
| part | g | what | ref a |
|---|---|---|---|
| A | 1515-1553 | low wide from the runner between two street banners (foreground framing like the ref's branch): the whole pagoda against the moon, storeys sliding opposite ways (set_sway amp 1.1, 0.8 Hz), lanterns + bells swinging (set_quake 0.9), camera shake 0.05 D, slow push | t0121 |
| B | 1554-1606 (cut, 1.07 s after the start) | low at the open base: kenta, woman2, merchant huddled inside (farmer behind them), ground + first storey swaying above them, push + tilt up; "แต่ไม่ล้ม" g 1569 lands 15 frames in | t0123 |
Events: "ส่ายเหมือนงู" g 1546 inside the sway of A, "แต่ไม่ล้ม" g 1569 on B. Framing changes g 1515 (in), 1554, 1600 (out): 1.3 s / 1.53 s.

## State
NIGHT, cutaway off, collapse 1 (tower already down, dust off, settle 0.35: it is outside both frames), sway / quake keyed on every frame,
`soseki_shade` hidden (fixed contact shade would show beside the swinging foot). DOF: A focus (0, -2, 3) f 5; B (0, -2.2, 3) f 3.5.
head_flip False (moon key from the south-west: screen-left). Mouths closed (no quoted line here).

## Staging (head centre px at 720x1280, from raw/*.json)
| part | head | width | x | y |
|---|---|---|---|---|
| A (wide) | 4 tiny figures in the base | 35-39 | 327-400 | 833-870 (bottoms up to ~889: wide-shot extras, 4 % of their height into the caption band) |
| B | kenta / merchant / woman2 / farmer | 104-116 / 97-107 / 100-110 / 93-103 | 272-467 | 709-812 (0.55-0.63 H; all head bottoms above 880) |

## Colour (`work/hue.txt`)
red 9.4, orange 2.4, blue 77.8, violet 5.9, magenta 3.7; sat 0.57, val 0.47, dark 0.04. NIGHT: blue-dominant as expected, no magenta cast.
Dark share 0.04 is below the day band (moonlit set, same as the set's NIGHT stills).

## Differs from the plan / reference
- Ref t0121 is a golden sunset; the plan asks NIGHT, kept NIGHT. Our wide is lower and the pagoda taller in frame than the jar.
- The farmer is mostly hidden behind woman2 in B (four cards in a 2 D opening between the drapes).
