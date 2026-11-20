# QA s09 (film 17, shots 22-23, narration 39.76-44.65 s) - round 3
Take g 1190..1348 (159 frames; g0 1196, g1 1342, 6 handle frames each side), 720x1280, 12 samples + OIDN. take.mkv is split: `cat take.mkv.part* > take.mkv`.
Set measure / DAY_INT. Shot 22 g1190-1274: gendarmes march dupont in (hands on his arms), the inspector walks in behind and to the right from the first frame (never pops in). Shot 23 g1275-1348: dupont seated, shrug + two head shakes, inspector at the left turned to Bertillon with a smile-eyes grin, Bertillon calm at the right.

## Numbers
- rhythm.py --first_g 1190 --cuts 1275: in-shot median **7.50**, p90 **14.36** (>= 4 / >= 12).
- qa_auto: **PASS**, magenta 0.0 %.

## Round-2 fixes (QA_TECH_R2)
1. grin: expression `happy` (smile arcs), head yaw 0.7, tilt -10 deg, gaze to Bertillon; moustache tips already curl up (cast not editable). Placed at (0.1, 2.0), fully left of dupont's head (small overlap of the moustache tip with his beret edge only).
2. entrance: inspector visible and walking (march cycle) from g1190, trailing the group (lag grows 0.25 -> 0.9 m).
3. gendarmes: camera look shifted so the blue gendarme stays fully in frame to g1274; camera pull-back limited to stay inside the room.
4. ring with blue dot = leftover steel ring of the loose spreading calipers; the rod with square clip = a second quill in the cream pen set. Both deleted once at build (before any keyframe), so nothing toggles per frame. Dust fully off (0).
5. dupont's face built once and reused (silent, flat mouth, expr worried); only yaw / head_roll / blink change.
6. head shakes: yaw 0.1 +-0.42 and roll +-8 deg at 2.5 Hz, two bursts of 0.7 s (g1290-1310, g1318-1338).
7. dust off (no dots).

## Self-check (full-res frames viewed)
g1212, g1265, g1300, g1310, g1330 checked at 360x640 from the 720x1280 frames: no rods, no ring, no clip, inspector present/grinning, gendarmes in frame, Bertillon in frame, no dust dots. Plus contact sheet of 12 frames across both shots, the cuts g1196 / g1275 +-3, and a decode check of all 159 PNGs. Not every frame was inspected at 6 fps. Legs of dupont still read as thin stubs under the coat (minor, accepted in R2).
