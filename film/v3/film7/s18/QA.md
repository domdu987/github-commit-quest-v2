# s18 QA: film 7, shot 18 (58.80-62.62 s): Notre-Dame's towers still standing -> hard cut to the director at the empty wall

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps) = g 1758..1884 (first_g 1758, 127 frames): in-handle g 1758..1763, shot 18 g 1764..1878,
out-handle g 1879..1884, all rendered in 3D (720x1280, 12 samples, 2 threads, denoise FAST). Also `meta.json`, `cues.json`, `contact.jpg`,
`compare.jpg`. Scripts: `engine.py` (same as s16), `shot.py`, `deliver.py`. Numbers: `work/qa.txt`, `work/hue.txt` (not in git).

| set-up | g | framing | action | caption |
|---|---|---|---|---|
| 1 | 1758-1801 | paris notre_dame_view, STREET_DUSK, 22 mm, slow push | the quai at dusk, Notre-Dame's two towers at the end, gas lamps lit; a lady strolls, a gentleman crosses | "ภาพไปไหน หอคอยนอเทรอ" |
| 2 | 1802-1835 | CUT low angle, 40 mm, tilt up | from the rose window up to the two towers, standing against the dusk sky | "ดามยังอยู่ครบ" 60.17 |
| 3 | 1836-1884 | HARD CUT, louvre wall_eye, low angle 22 -> 24 mm with a punch-in on the turn | the director stares, stunned, at the empty wall (four hooks), then whips round (g 1847-1851) pale, sweating, hands to his head, trembling | "แต่โมนาลิซ่า" 61.11 / "หายไปแล้ว" 61.89 |

## Client rules
- No depth of field; sharp throughout. Mouths: static (the director's shocked 'O' is the expression's own mouth, it does not move).
- Heads above y 880 in every frame. The director (main head) 0.38-0.51 H; set-up 1 is a wide (strollers 0.61-0.66 H, small, exempt).
- Dense: Haussmann facades, lamps, quai, roof ring; the salon hang behind the director. set_papers(24) keyed (theft known from shot 18),
  set_mona(False) keyed every frame in set-up 3.

## QA numbers (work/qa.txt)
```
set-up 1 gent    head w   47..  57 px, x   410..  558, centre y  787.. 815 (0.61..0.64 H); bottom below 880: none
set-up 1 lady    head w   54..  68 px, x   129..  214, centre y  809.. 842 (0.63..0.66 H); bottom below 880: none
set-up 3 dir     head w  178.. 276 px, x   445..  513, centre y  486.. 648 (0.38..0.51 H); bottom below 880: none
render: wall 14.86 s, cpu 24.00 s per frame (mean); by set-up {'1': {'wall': 11.54, 'cpu': 23.08}, '2': {'wall': 10.89, 'cpu': 22.1}, '3': {'wall': 20.6, 'cpu': 26.14}}; retried: []
popcheck (g -> g+1, change): [(1801, 1802, 39.4), (1835, 1836, 73.9), (1853, 1854, 4.6), (1855, 1856, 4.5), (1864, 1865, 4.6), (1866, 1867, 4.6), (1877, 1878, 4.7), (1879, 1880, 4.3)]   planned cuts: [1764, 1802, 1836]
near-still transitions (< 0.35 levels): []
frame change median 3.75, max 73.93 levels
magenta / black frames: []
```
Pops: the planned cuts at 1802 / 1836; the ~4.5-level steps in set-up 3 are the director's trembling (head roll + lean jitter), intended.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s18 notre-dame (g 1764-1835)                   22.1   59.2    2.1    0.0    0.0    8.2    4.1    4.3  0.34 0.63 0.02   OUT: red,orange,blue,sat,val,dark
s18 director (g 1836-1878)                     63.3   28.2    1.1    0.4    0.0    0.8    3.1    3.1  0.48 0.55 0.12   OUT: red,blue,sat
ref a t0063 t0065 (dusk exteriors)             48.5   41.9    2.1    0.0    0.0    0.3    0.2    7.1  0.49 0.70 0.12   OUT: red,orange,blue,sat,val
ref a t0013 (red interior)                     47.4   33.7    0.2    0.1    0.0    9.2    5.1    4.3  0.52 0.48 0.14   OUT: red,blue,violet,sat
```
Dusk exterior is orange-dominant with low saturation (0.34) — the set's STREET_DUSK look (louvre_API section 7); magenta 4.3 (< 10).

## Fixed after looking at the first final
- Set-up 1's first 18 frames were washed by the street's camera-only haze sheet: the push crossed it at y ~40 (a visible jump at g 1775).
  The camera now stays beyond it (y 40.8 -> 43.6); set-ups 1-2 re-rendered.
- The first tilt (48 mm) ended with the towers' tops cut off; now 40 mm, tilting to the tower tops and the sky.

## Differences from the plan
- Shot 18 = three set-ups (wide / tilt / director) for the 1-2 s framing rhythm; the hard cut lands on "แต่โมนาลิซ่า".
- Notre-Dame is the set's painted plate (flat, as the set documents).
