# s11 QA: film 2, shot 11 (the town laughs: "ไม้จิ้มฟ้า"), tower set DAY, square_low

Delivered: `take.mkv` (g 792..888, 97 frames, first_g 792, 720x1280, 12 samples, 2 threads, libx264rgb crf 6) from `frames/` (not in git). g 799..882 = shot 11 ([g0, g1) = [799, 883)); g 792..798 = 7-frame in-handle (10-frame dissolve from shot 10), g 883..888 = 6-frame out-handle (9-frame dissolve into shot 12), both in 3D. `meta.json`, `cues.json` (8 cues), `contact.jpg`. Scripts: `shot.py`, `deliver.py`.

## Timing
| event | g | s |
|---|---|---|
| low wide: woman, old man and baker point up at the tower and laugh (bouncing, jabbing fingers, tears), slow creep + rise ("จนคนทั้งเมือง" 802) | 792-826 | |
| snap reframe closer on the three ("เรียกแท่งเหล็กนั้นว่า" 828 / 836) | 826-834 | 27.53-27.80 |
| punch-in on the rod far above: tilt up + snap zoom 22 -> 420 mm (quint, geometric lens), lands "ไม้จิ้มฟ้า" g 856 | 846-856 | 28.20-28.53 |
| rod against the sky, drift and zoom 420 -> 440 mm into the out-handle | 856-888 | |
Framing changes: 792, 826-834, 846-856, then the drift: gaps 1.13, 0.4, 1.07 s. Frame change min 0.17 / median 5.3: two 2-frame near-still runs (g 856-858, 886-888, the telephoto drift against a flat sky), none longer; no pops.

## Staging (heads, g 792-845; after the punch only the rod is in frame)
| head | width px | centre x | centre y | head bottom max |
|---|---|---|---|---|
| woman (left) | 165-205 | 175-259 | 608-713 | 799 |
| old (middle, deeper) | 137-164 | 364-403 | 699-775 | 850 |
| baker (right) | 168-208 | 531-551 | 542-671 | 756 |
Whole heads above y 880 in every frame. Camera 0.55 D above the cobbles (worm's eye) so the heads sit high enough while the whole tower with the rod stays in frame above them (rod tip y 268-278 in the wide). After the punch the rod spans y 409 (tip) .. 780-808 (base), centre 0.46 H. A stone pier in true shadow at the left edge (as s01 shot 2) for darks. head_flip False.

## Colour (hue_report.row on the 97 final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s11 g 792-888                                  15.3    8.3    0.0    0.8    1.9   72.4    0.4    0.9  0.55 0.60 0.03   OUT: red,orange,blue,sat,dark
ref a t0062 t0040                              46.1   30.0    2.6    0.2    0.0    8.9    2.1   10.1  0.40 0.58 0.16
```
Day exterior looking up: the sky fills about half of the wide and most of the rod close-up (the punch-in shows the rod against the sky by the plan's design), so blue is far above band. Violet and magenta in band; shade on the pier and cobbles blue-violet. The wide part alone is close to s01 shot 2.
Seconds per frame: 9.48 s wall / 18.04 s CPU mean.

## Differences from the plan
- Townspeople: woman, old man and baker (no padre, no nico). Market stall hidden (as s01).
- The punch-in on the rod is a lens zoom (22 -> 420 mm) with a tilt-up from the same low position, not a dolly: the rod is 28 D up and a physical move would leave the square. The 22 mm rule is broken on purpose for this comic snap zoom.
