# Film 23 set (r1): builder notes and numbers

Rebuild: `python3 ghost.py sheet` (19 shots x first / mid / last, 360x640, 6 samples -> `set_sheet.jpg`), `python3 ghost.py finals` (S01 S07 S09 S12 S14 S17
first frame, 720x1280, 12 samples, OIDN -> `set_work/final/`, `set_finals.jpg`, `set_work/numbers.json`), `python3 ghost.py ground` (-> `GROUND_SET.md`).
One bpy process per shot, one render at a time, Cycles CPU 4 threads, no DOF. API: `API.md`. Style board kept in `board/`.

## Finals (first frame of the take, 720x1280, 12 samples; r2: S01 S14 S17 S18 re-rendered after the QA_ART_SET fixes, S07 S09 S12 unchanged from r1) — ghost_hue.py
| shot | location / light | sat (>= 0.47) | luma (day 85-110, night 70-95) | shade hue (240-260) | magenta % | vivid % | render wall s | cpu s | build s |
|---|---|---|---|---|---|---|---|---|---|
| S01 | FIELDS DAWN | 0.661 | 100.6 | 241.3 | 0.1 | 67.4 | 6.9 | 25.6 | 9.1 |
| S07 | LANE MORNING | 0.637 | 104.1 | 243.3 | 0.2 | 71.7 | 6.3 | 23.1 | 7.4 |
| S09 | CAMP NIGHT | 0.484 | 80.6 | 242.9 | 1.6 | 22.8 | 9.7 | 37.1 | 3.1 |
| S12 | LANE DAY | 0.604 | 109.6 | 233.4 | 0.1 | 75.2 | 5.6 | 20.5 | 7.5 |
| S14 | RHINE NIGHT_R | 0.575 | 76.0 | 227.2 | 0.3 | 48.3 | 12.8 | 33.9 | 15.0 |
| S17 | RHINE NIGHT_R | 0.643 | 70.1 | 233.5 | 0.1 | 52.0 | 10.3 | 27.1 | 15.4 |
| S18 | RHINE PREDAWN | 0.568 | 85.5 | 231.3 | 0.8 | 73.8 | 6.9 | 25.4 | 15.5 |

Render time per final frame: 5.6-9.7 s wall on an idle machine (r1); the r2 S14 / S17 renders read 10-13 s because the ground sweep ran beside them. CPU 20-37 s, 4 threads; plus a 3-15 s build per process (RHINE r2 builds take ~15 s).

## Sheet drafts (mid frame of every shot, 360x640, 6 samples; S01 + S14-S18 re-rendered in r2)
| shot | loc / light | sat | luma | shade hue | magenta % | dark V<0.25 | heads in band 880-950 |
|---|---|---|---|---|---|---|---|
| S01 | FIELDS DAWN | 0.639 | 94.5 | 245.3 | 0.2 | 0.01 | none |
| S02 | LANE MORNING | 0.653 | 102.3 | 246.2 | 0.1 | 0.08 | none |
| S03 | LANE MORNING | 0.560 | 115.0 | 248.2 | 0.2 | 0.04 | none |
| S04 | LANE MORNING | 0.592 | 101.9 | 251.7 | 0.6 | 0.02 | none |
| S05 | LANE MORNING | 0.609 | 106.5 | 256.9 | 0.6 | 0.04 | none |
| S06 | LANE MORNING | 0.571 | 109.8 | 254.6 | 0.0 | 0.07 | none |
| S07 | LANE MORNING | 0.660 | 108.5 | 236.0 | 0.1 | 0.03 | none |
| S08 | LANE MORNING | 0.551 | 101.7 | 250.4 | 0.7 | 0.04 | none |
| S09 | CAMP NIGHT | 0.531 | 78.2 | 240.3 | 0.3 | 0.01 | 1 |
| S10 | CAMP NIGHT | 0.556 | 96.8 | 244.3 | 1.9 | 0.02 | none |
| S11 | LANE DAY | 0.537 | 103.9 | 241.8 | 0.1 | 0.06 | none |
| S12 | LANE DAY | 0.588 | 111.1 | 264.3 | 0.2 | 0.03 | none |
| S13 | LANE DAY | 0.607 | 106.3 | 243.7 | 0.2 | 0.03 | none |
| S14 | RHINE NIGHT_R | 0.608 | 75.3 | 231.5 | 0.3 | 0.00 | none |
| S15 | RHINE NIGHT_R | 0.600 | 71.3 | 231.5 | 0.6 | 0.00 | none |
| S16 | RHINE NIGHT_R | 0.690 | 62.0 | 234.5 | 0.2 | 0.00 | none |
| S17 | RHINE NIGHT_R | 0.638 | 72.7 | 233.8 | 0.1 | 0.00 | none |
| S18 | RHINE PREDAWN | 0.571 | 86.5 | 231.3 | 0.8 | 0.00 | none |
| S19 | LANE DAY | 0.598 | 98.7 | 273.3 | 3.0 | 0.02 | none |

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

## r2 (QA_ART_SET.md: FIELDS + RHINE fixes; LANE / CAMP code, cameras and marks untouched)
- S01: starts as a high OBLIQUE view (120 D up, 37 deg down, lens 18) along the lane over the detailed bocage with the dawn horizon in the top ~15 %;
  the column is a findable string of olive dots on the lane; the descent stays inside the detailed square (its edge only at the far horizon); the
  end is 3/4 on the lead tank from the lane, no hedge wall, the waving rider's head at ~0.45 of the frame height. First-frame shade hue 241.
- RHINE lights: moon moved to the north-east and low (path on the river), ambient cut where the moon lands (no lavender), navy shade, sky_night3r;
  24 field lanterns at 2400 W with 1.8 D warm pools, 7 bank lanterns (warm streaks on the water), lit truck cabs, tent glow.
- River: deep navy flat body, low-frequency swell + fine ripple noise, real glossy reflections; the glint dashes ("blue static") are gone.
- Foregrounds: a lit supply dump fills the lower S14 frame; `bankdress` groups (crate stack, rubber bundle, rope coil, pump, small lantern) 1.8-2 D
  from the lens in S15 / S16 (+ more dressing at 6-10 D in S16); the pink reed sticks are gone from S15.
- S17: re-aimed, all three observers whole in frame, the glowing field and its reflection behind them.
- S18 rebuilt: low oblique 2.4 D over the water at the west end of the pontoon bridge looking ENE into a warm orange pre-dawn band; boat3 with two
  paddlers and the dog ~7 D from the lens; troops on the bridge and the far bank, trees and a truck there.

### Still missing (honest)
- RHINE shade hue stays 227-234 (target 240-260): the moonlit grass reads hue 205-210 (QA asked 215-230 for lit ground), the sky and shade are
  ~246; pushing the moon key toward red turned sandbags and crates pink again, so I kept the blue key.
- RHINE dark share (V < 0.25) is ~0 % (target 8-15 %): raising luma into the night band and keeping deep darks did not both fit.
- S18: the bridge reads as a thin diagonal strip at the horizon (camera 2.4 D over the water), water fills ~45 % (target <= 35 %), the paddlers are
  ~7 D away (asked 3-5: at 5 D the cards fill the frame).
- S14's moon path is glitter rather than a crisp column.
- Night luma: S16 mid frame 62 (band 70-95); S14 / S15 / S17 sit at 71-75, just inside.

## Ground
`GROUND_SET.md`: 21 453 checks over the 19 takes (every 10th frame, action states keyed in) + the four bare locations: 0 FAIL (r2 re-run on
FIELDS, RHINE and S01, S14-S18).
