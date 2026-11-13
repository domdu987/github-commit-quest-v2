# s16 QA: film 7, shots 16-17 (51.19-58.80 s): the empty wall all day; next morning the painter points at the hooks

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps) = g 1530..1769 (first_g 1530, 240 frames): 6-frame in-handle g 1530..1535, shot 16
g 1536..1663, shot 17 g 1664..1763, 6-frame out-handle g 1764..1769, all rendered in 3D (720x1280, 12 samples, 2 threads, denoise FAST).
Also `meta.json`, `cues.json`, `contact.jpg` (16 frames, cyan = y 880), `compare.jpg`. Scripts: `engine.py` (spec-driven take runner on
`../common.py`, identical copy in s18 / s19), `shot.py` (the five set-ups), `deliver.py`. Numbers: `work/qa.txt`, `work/hue.txt` (not in git).

| set-up | g | framing | action | caption |
|---|---|---|---|---|
| 1 | 1530-1576 | wide on the empty wall, 21 mm, slow push | two ladies + a gentleman stride past in time-lapse, nobody looks; guard at ease by the wall | "ทั้งวันไม่มีใครสังเกต" |
| 2 | 1577-1617 | CUT medium on the guard + the four hooks, 24 mm | he turns his head to the empty spot, unimpressed | "ยามเห็นผนังว่าง" 52.48 |
| 3 | 1618-1663 | CUT punch-in, 26 mm | he turns to us and shrugs (the photographers took it) | "ก็นึกว่าช่างภาพยืมไปถ่ายรูป" 53.48 |
| 4 | 1664-1712 | CUT, next morning, 22 mm | the copyist painter (beret, palette) walks in to his easel before the empty wall | "วันรุ่งขึ้น จิตรกรคนหนึ่งมา" 55.43 |
| 5 | 1713-1769 | CUT closer, 22 mm | he dabs at the easel, looks up (g 1732), points at the empty hooks, shocked (g 1745) | "วาดรูปตรงนั้น แล้วถามว่า" 57.17 / 58.13 |

Time passing (shot 16): the gallery sun is keyed per frame from GALLERY_DAY (57 deg, cream) to a low gold sunset (24 deg, swung west),
the skylight fills dim and warm (x1.0 -> 0.35), the gas torcheres rise (set_flames 1.0 -> 1.9) and the compositor CDL slope goes
(1, 0.985, 0.97) -> (0.98, 0.76, 0.56). The camera-only shaft sheets follow the built sun only, so they are hidden in shot 16. Shot 17 is
plain GALLERY_DAY (morning), shafts on.

## Client rules
- No depth of field anywhere (common.Take: dof off at build and before every render); everything sharp.
- Mouths: no quoted line here: static expression mouths only (the STORY7 'mouth' talk shapes are dropped by engine.story()).
- Heads above y 880: every frame, every actor (set-up 3 was re-rendered with a looser punch-in after the first final put the guard's
  chin at y 885 on g 1654-1663). Main head centre: set-up 2 0.56-0.57 H, set-up 3 0.51-0.52, set-up 4 0.53-0.55, set-up 5 0.53-0.54;
  set-up 1 is a wide (passers 0.57-0.60, exempt).
- Dense set: salon hang, damask, stanchions + rope, torcheres; the easel card (cast7.easel_svg with a faint sketch of her) added at runtime.
- Continuity: set_mona(False) keyed on every frame (the four hooks + the unfaded patch + plaque); no paris / papers in this take.

## QA numbers (work/qa.txt)
```
set-up 1 gent    head w  208.. 218 px, x   -84..  783, centre y  724.. 740 (0.57..0.58 H); bottom below 880: none
set-up 1 guard   head w   90..  98 px, x   497..  520, centre y  697.. 702 (0.54..0.55 H); bottom below 880: none
set-up 1 lady    head w  145.. 179 px, x   -51..  779, centre y  747.. 774 (0.58..0.60 H); bottom below 880: none
set-up 1 lady2   head w  120.. 127 px, x   -19..  706, centre y  736.. 749 (0.57..0.59 H); bottom below 880: none
set-up 2 guard   head w  182.. 205 px, x   566..  569, centre y  717.. 726 (0.56..0.57 H); bottom below 880: none
set-up 3 guard   head w  264.. 294 px, x   457..  462, centre y  654.. 671 (0.51..0.52 H); bottom below 880: none
set-up 4 painter head w  140.. 155 px, x   -62..  242, centre y  682.. 700 (0.53..0.55 H); bottom below 880: none
set-up 5 painter head w  225.. 276 px, x   221..  256, centre y  676.. 685 (0.53..0.54 H); bottom below 880: none
render: wall 14.89 s, cpu 28.38 s per frame (mean); by set-up {'1': {'wall': 15.21, 'cpu': 28.17}, '2': {'wall': 13.45, 'cpu': 26.45}, '3': {'wall': 14.22, 'cpu': 27.01}, '4': {'wall': 14.83, 'cpu': 27.49}, '5': {'wall': 16.23, 'cpu': 31.8}}; retried: []
popcheck (g -> g+1, change): [(1576, 1577, 52.6), (1617, 1618, 33.7), (1663, 1664, 70.6), (1712, 1713, 55.4), (1744, 1745, 8.5)]   planned cuts: [1536, 1577, 1618, 1664, 1713]
near-still transitions (< 0.35 levels): [1662, 1711, 1768]
frame change median 3.24, max 70.60 levels
magenta / black frames: []
```
Pops are the planned cuts, plus g 1744 -> 1745 (8.5 levels): the painter's point snaps in over 5 frames (an accent on "แล้วถามว่า").

## Colour (hue_report, every 2nd frame)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s16 shot 16 (g 1536-1663)                      67.3   27.5    0.6    1.3    0.0    0.5    0.1    2.7  0.57 0.50 0.08   OUT: red,blue,sat,dark
s16 shot 17 (g 1664-1763)                      46.8   48.6    2.5    0.3    0.0    0.8    0.1    0.8  0.54 0.66 0.02   OUT: red,orange,blue,sat,val,dark
ref a t0013 t0049 (red interiors)              50.8   33.2    0.5    0.1    0.0    8.9    3.0    3.6  0.54 0.44 0.17   OUT: red,blue,sat,val,dark
ref a t0063 (sunset)                           56.3   31.1    2.5    0.0    0.0    0.0    0.0   10.0  0.48 0.73 0.24   OUT: red,blue,sat,val,dark
```
Red-dominant like the ref's red interiors (red 67 / 47 vs ref 51); magenta 2.7 / 0.8 (limit 10). Saturation 0.54-0.58 matches the ref.

## Differences from the plan / known issues
- Shot 16 is three set-ups (wide / medium / punch-in) to keep a framing change every 1.3-1.6 s; shot 17 two.
- Shot 17's painter does not carry the easel in: it already stands before the wall (the easel is a 2D card), he walks in with his palette.
- The guard stands inside the rope: the red rope crosses his chest in set-ups 2-3, so the shrug reads mostly from the head tilt and the
  raised shoulders / short forearms, not open palms.
- Set-up 1 uses the cast7 'lady' twice (same costume) for the second passer.
