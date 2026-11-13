# s14 QA: film 4, shots 14-15 (NIGHT: the quake starts, kenta runs, the townsman mocks), pagoda set v2

Delivered: `take.mkv` = `frames/g_1173.png .. g_1438.png` (266 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 1180..1431 = shots 14-15 ([g0, g1) = [1180, 1432)); g 1173..1179 = 7-frame in-handle (shot 14 camera before its start, 3D) for a
10-frame dissolve from s13 (SUNSET -> NIGHT); g 1432..1438 = 7-frame out-handle (shot 15 c2 continues, 3D; the plan's 15 -> 16 is a
hard cut, the handle is there in case the conform dissolves). Also `meta.json` (first_g 1173, n_frames 266), `cues.json` (24 cues),
`contact.jpg` (16 frames), `compare.jpg` (6 final frames beside ref a t0067 / t0071 / t0075 / t0079 / t0083 / t0087).
Scripts: `shot.py` (the take), `base4.py` (shared take machinery, same file in s13 / s16), `deliver.py` (frames, meta, cues, sheets,
mkv, `work/qa.txt`). Raw renders + per-frame json in `raw/s14`, `raw/s15`.

## Timing (narration_bankky.wav at +0.10 s, captions_bankky.json)
| part | g | what | ref a |
|---|---|---|---|
| 14 A | 1173-1221 | high wide over the street roofs (axial, toward the gate), pagoda + tower, mountains, big moon; slow push. Quake starts on "พื้นดินก็สั่นแรง" (40.02 s = g 1204): strength 0 -> 1 g 1200-1222 (lanterns / bells swing, pagoda sway 0 -> 1.0 at 1.1 Hz, camera shake 0.04 -> 0.6 deg) | t0067-t0071 |
| 14 B | 1222-1261 (cut) | low in the street looking up at the swinging lanterns, hopping roof tiles, moon, gate; tilt up, shake 0.85 deg | t0069 |
| 15 a | 1262-1302 (cut) | side tracking: kenta sprints screen-right down the lantern street (0.22 D/frame, 3 strides/s), cupped hand, shouting drawing | t0075 |
| 15 b | 1303-1344 (cut) | kenta stops, shouts toward the doorways with a beckoning hand ("ตะโกนให้" 43.31 s = g 1302); woman2 laughing in the street behind, the merchant soft in his doorway | t0077-t0081 |
| 15 c1 | 1345-1386 (cut) | LOW ANGLE (pitch 36-38 deg) on the merchant at his doorway, eave + lantern + nobori in the foreground: arms folded, smug; cups his hands g 1374-1381; mouth from g 1383 | t0083-t0087 (guard on the wall) |
| 15 c2 | 1387-1438 (snap) | closer and lower on him, mock-shouting the quote "เจดีย์เมาจะพาพวกข้าตายหรือไง" (46.01-47.73 s = g 1383-1435) | t0085-t0087 |
Framing changes g 1180, 1204 (shake begins), 1222, 1262, 1303, 1345, 1387: gaps 0.8, 0.6, 1.33, 1.37, 1.40, 1.40 s; c2 runs 1.5 s to the cut.

## Staging (`work/qa.txt`)
| part | head | width px | centre x | centre y (H) | head bottom below 880 |
|---|---|---|---|---|---|
| 15 a / b | kenta | 210-241 | 230-316 | 0.47-0.51 | none |
| 15 b | merchant (background, soft) / woman2 (background) | 91 / 82-87 | 185 / 517-554 | 0.47 / 0.48 | none |
| 15 c | merchant | 193-271 | 390-439 | 0.41-0.52 | none |
Near/far in 15 b: 241 / 82 = 2.9. head_flip chosen per camera from the moon key (`Take.head_flip_for`): on for 15 b (key screen-right), off elsewhere.
Nobody's back to the camera. Mouths: only the merchant's moves, and only g 1383-1435 (lip-sync from the narration RMS, a new drawing every
2 frames: flat / talk_a / talk_b / talk_o); kenta's is a fixed shout drawing ("talk_b" from `kenta_run_shout`, never animated), woman2's
the fixed laughing grin. Actor cards tinted `#b8bfe8`, ink `#1e142e` (night). No pinned hands in this take.

## Motion / popcheck
Pops only at the cuts (1221->1222 35.5, 1261->1262 38.2, 1302->1303 37.6, 1344->1345 49.3) plus quake-shake frames (1213, 1226, 1234,
1307, 1320, 1347, 1381-1399, 1421: 4-11 levels; checked at full size: whole-frame shake, no sprite pop). No near-still frames
(median change 4.4 levels); no static runs. No black / magenta frames, no retried frames, no clipped sprites, no warnings in `work/final_log.txt`.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s14 shot 14 (g 1173-1261)                       2.3    3.0    0.0    0.0    0.0   93.0    0.9    0.9  0.68 0.49 0.02
s14 shot 15 (g 1262-1438)                       1.8   16.4    0.0    0.0    0.1   78.9    2.0    0.7  0.63 0.47 0.09
ref a t0067 t0071 t0075 t0079 t0083 t0087       2.0    0.9    0.0    0.0    0.0   85.0    8.0    4.0  0.54 0.58 0.04
```
Night: outside the day band by design, like the reference night (blue 85, red 2). Ours is as blue (79-93), less violet / magenta,
a bit more saturated (0.63-0.68 vs 0.54) and darker (val 0.47-0.49 vs 0.58); warm lantern windows give shot 15 its orange 16.
Shade reads blue, never magenta.

## Seconds per frame
7.83 s wall / 15.3 s CPU mean (2 threads); shot 14 6.6 / 13.0, shot 15 8.5 / 16.5.

## Differences from the plan / the reference
- Shot 14: plan "town_wide -> street_eye": custom cameras instead (A high on the street axis like s01 shot 5, so the moon, pagoda and
  tower are in one frame; B low in the street under the lanterns). No people in shot 14.
- Shot 15: the "townsman" is the merchant (cast4) at the doorway of the east machiya (3.2, -51.2), standing just outside the pent roof
  (under it the eave cut his head at the low angle). The ref's wall is replaced by the eave + lantern + nobori seen from below.
  "Others still laughing": woman2 in the street behind kenta in 15 b; the farmer was dropped (at the c low angle any background head lands
  below y 880).
- Kenta's run is a side tracking shot (cast4's sprint pose runs screen-right), not toward the camera.
- The street floor still carries the set's red runner (set v2).
