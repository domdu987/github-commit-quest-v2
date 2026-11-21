# Film 23 set (r1): builder notes and numbers

Rebuild: `python3 ghost.py sheet` (19 shots x first / mid / last, 360x640, 6 samples -> `set_sheet.jpg`), `python3 ghost.py finals` (S01 S07 S09 S12 S14 S17
first frame, 720x1280, 12 samples, OIDN -> `set_work/final/`, `set_finals.jpg`, `set_work/numbers.json`), `python3 ghost.py ground` (-> `GROUND_SET.md`).
One bpy process per shot, one render at a time, Cycles CPU 4 threads, no DOF. API: `API.md`. Style board kept in `board/`.

## Finals (first frame of the take, 720x1280, 12 samples) — ghost_hue.py
| shot | location / light | sat (>= 0.47) | luma (day 85-110, night 70-95) | shade hue (240-260) | magenta % | vivid % | render wall s | cpu s | build s |
|---|---|---|---|---|---|---|---|---|---|
| S01 | FIELDS DAWN | 0.898 | 103.6 | 215.7 | 0.0 | 98.4 | 6.8 | 25.1 | 9.5 |
| S07 | LANE MORNING | 0.637 | 104.1 | 243.3 | 0.2 | 71.7 | 6.3 | 23.1 | 7.4 |
| S09 | CAMP NIGHT | 0.484 | 80.6 | 242.9 | 1.6 | 22.8 | 9.7 | 37.1 | 3.1 |
| S12 | LANE DAY | 0.604 | 109.6 | 233.4 | 0.1 | 75.2 | 5.6 | 20.5 | 7.5 |
| S14 | RHINE NIGHT_R | 0.574 | 81.3 | 237.5 | 0.6 | 44.3 | 7.8 | 29.3 | 10.1 |
| S17 | RHINE NIGHT_R | 0.661 | 76.3 | 242.9 | 2.0 | 52.0 | 6.5 | 24.3 | 9.9 |

Render time per final frame: 5.6-9.7 s wall (mean 7.1; 20-37 CPU s, 4 threads), plus a 3-10 s build per process.

## Sheet drafts (mid frame of every shot, 360x640, 6 samples)
| shot | loc / light | sat | luma | shade hue | magenta % | heads in band 880-950 (first/mid/last) |
|---|---|---|---|---|---|---|
| S01 | FIELDS DAWN | 0.658 | 99.4 | 245.1 | 0.2 | none |
| S02 | LANE MORNING | 0.653 | 102.3 | 246.2 | 0.1 | none |
| S03 | LANE MORNING | 0.560 | 115.0 | 248.2 | 0.2 | none |
| S04 | LANE MORNING | 0.592 | 101.9 | 251.7 | 0.6 | none |
| S05 | LANE MORNING | 0.609 | 106.5 | 256.9 | 0.6 | none |
| S06 | LANE MORNING | 0.571 | 109.8 | 254.6 | 0.0 | none |
| S07 | LANE MORNING | 0.660 | 108.5 | 236.0 | 0.1 | none |
| S08 | LANE MORNING | 0.551 | 101.7 | 250.4 | 0.7 | none |
| S09 | CAMP NIGHT | 0.531 | 78.2 | 240.3 | 0.3 | 1 |
| S10 | CAMP NIGHT | 0.556 | 96.8 | 244.3 | 1.9 | none |
| S11 | LANE DAY | 0.537 | 103.9 | 241.8 | 0.1 | none |
| S12 | LANE DAY | 0.588 | 111.1 | 264.3 | 0.2 | none |
| S13 | LANE DAY | 0.607 | 106.3 | 243.7 | 0.2 | none |
| S14 | RHINE NIGHT_R | 0.598 | 80.2 | 236.9 | 0.4 | none |
| S15 | RHINE NIGHT_R | 0.569 | 85.5 | 235.7 | 1.0 | none |
| S16 | RHINE NIGHT_R | 0.660 | 73.4 | 235.6 | 0.4 | none |
| S17 | RHINE NIGHT_R | 0.655 | 79.2 | 245.7 | 2.1 | none |
| S18 | RHINE PREDAWN | 0.561 | 92.6 | 231.4 | 0.0 | none |
| S19 | LANE DAY | 0.598 | 98.7 | 273.3 | 3.0 | none |

## What changed from the board
- One `build(location, shot)` for four locations in one world frame (FIELDS at the origin, LANE 700 D west and CAMP 760 D east inside the FIELDS far
  patchwork ring, RHINE 9000 D north); the board's camera-relative layout was frozen into world positions.
- Every prop is its own object (prop groups), ground-snapped by ray cast and given a contact blob; tanks are shape-keyed (inflate / sag / elev).
- CAMP: tank rows broadside with turret + barrel, darker rubber with a thin cold moon rim (rim 1.25, power 3.2), only two nets, lantern halos 0.75 D,
  crisp pools, no fog; the soldier is off the lantern pole and the foreground figure is gone. Night grade moved from cyan-blue to blue-violet (sky_night2).
- RHINE is new: glossy rippled river with real reflections (one glossy bounce), a painted current layer and glint dashes; decoy field (42 tanks, 24
  lanterns, sound truck, radio tent, 30th / 79th INF DIV crates, unloading trucks, RHINE sign); pontoon bridge + boats (PREDAWN); German OP.

## Misses (honest)
- Shade hue: S12 233 and S14 237 (target 240-260): the shaded pixels are lane dirt under the cyclists (S12) and the moonlit night fields (S14).
  S01's first frame is a sun-lit top-down patchwork (1 % shaded pixels), so its 216 is not meaningful; its mid frame measures 245.
- S09 vivid share is low (23 %) though mean saturation passes (0.48).
- Sheet mid frames outside the bands: shade hue S07 236, S14-S16 235-237, S18 231 (pre-dawn blue), S12 264 and S19 273 (balloon reds / violet shadow
  on the pile); luma S03 115 and S12 111 (day band 85-110). S09 / S15 each have one placeholder chin touching y 880 at one sampled frame (a
  background card at the edge of a crane move).

## Ground
`GROUND_SET.md`: 18 537 checks over the 19 takes (every 10th frame, action states keyed in) + the four bare locations: 0 FAIL.
