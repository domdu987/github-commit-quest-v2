# s12 QA: film 23, shot S12 (LANE, DAY)

## What is in the take
S12 "bikes (ยกรถถังสี่สิบตัน)", LANE day, cut in. BIGZOOM 2 / reveal: the camera starts close on the two cyclists' faces (they ride up the lane and BRAKE to a stop by g 1308:
`ride_frame` state `brake`, stunned faces with a sweat drop, held open mouths), then pulls back and up to a wide that shows four GIs holding the rubber tank over their heads.
Real cast23 cards: French cyclists (`fr_beret` green bike with baguette basket, `fr_cap` maroon bike), four lifters (`lift_pose`, arms straight up, hands exactly at the tank
belly, wobble + strain; the faces are the S13 cast: `gi_smile` nearest the S13 camera, then `gi_driver`, `gi_pump`, `gi_designer`).
**The 4-man lift is the only airborne tank:** `tank_lift` is keyed per frame by `GH.set_lift` (0 -> 1 over g 1290-1328, out of frame while the camera is still on the cyclists),
flagged `airborne`; every field decoy stays on the grass. Mouths: held drawings only (no quote in this shot).

## QA_ART_SET per-shot note for S12 (lane-dirt shade hue)
- Per-surface ambient on the dirt: `tint_dirt()` multiplies the shade colour of the ground / dirt / rut materials by a per-channel factor (`DIRT_K`). I measured both ways on the
  draft frames (g 1284 / 1329 / 1389): with a blue-green push (0.88, 1.28, 1.0) the shade hue went DOWN to 237 / 249 / 244; with the unchanged set 243 / 254 / 251. The QA's
  233 / 264 were measured on the set's own camera; with the re-keyed camera (below) the untouched ambient already lands in 240-260, and the pushed one left it on the wrong
  side (the pixels are brown dirt x violet shade). So `DIRT_K = (1, 1, 1)` ships (the hook is in the script). **Final render numbers: first g 1284 = 243.1, mid g 1326 = 259.4,
  last g 1389 = 251.8** (all in 240-260; the shaded share of pixels is only 3-4 % in this shot, so the hue is a small-sample measure).
- **Redo after the director's review (first version: tank small at the top-right, a hedge over the right third, lifters specks).** Camera re-keyed again (`CAM_KEYS`): start at the west
  side, 5.5 D from the cyclists' faces in profile; a mid key swinging south; END (-4.8,-45,3.4) -> look (-5.2,-30,3.0), 22 mm, eased stop on the tank: the lifted tank is centred
  (about 40-45 % of the width), the four lifters are visible under it (heads 52-80 px at the end), the cyclists are braking and staring in the left foreground (marks moved to
  (-7.9,-35.3) / (-6.5,-36.6), heads y 727-796, bottoms <= 866), and the east hedge no longer enters the frame. All heads above y 880. The lifters are on screen from g ~1326.
- Shade hue of the redo: first g 1284 = 230.9 (below the 240-260 rule; only 4.7 % of the pixels are shaded, brown dirt in the close-up), mid g 1326 = 254.1, last g 1389 = 259.2.
- S13 does NOT continue from this staging: S13's cyclists stand at other marks and its camera is its own set-up (not re-rendered).
- Deviation: rhythm median 4.87 (rule >= 4) but p90 7.75 (rule >= 12).


## Frame budget
g0 1284, g1 (planned) 1368, g1_render 1389 (planned x 1.25 tail), first_g 1284 (in-handle 0), n_frames 106, transition_in cut 0 f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (44.9 MB).
Render cost: 12.7 s wall / frame (2 threads, two renders at once), 25.6 CPU s / frame.

## Automatic QA (all run on take.mkv)
- `ground_check --every 10`: checked objects: 44   rows: 528   FAIL rows: 0   **result: PASS** -> GROUND.md
  - checked objects: 44   rows: 528   FAIL rows: 0   **result: PASS**
- `qa_auto.py take.mkv --first_g 1284`: QA_AUTO PASS  (take.mkv, 106 frames, 30.00 fps, g 1284-1389) (QA_AUTO.md, phone_sheet.jpg)
- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `overall median jitter px 0.29`
- frame diff on 90x160 grey, in-shot frames: median 4.87, p90 7.75 (rule: >= 4 / >= 12), min 3.31
- shade hue (ghost_hue.shade_hue, rule 240-260): first g1284 = 230.9 (shaded share 0.05), mid g1326 = 254.1 (shaded share 0.04), last g1389 = 259.2 (shaded share 0.08)
- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):
  - cya: centre y 726 .. 796, x 89 .. 284, head width <= 154 px  (bottom of the head <= 873)
  - cyb: centre y 735 .. 781, x 212 .. 541, head width <= 138 px  (bottom of the head <= 851)
  - lf0: centre y 678 .. 766, x -322 .. 283, head width <= 79 px  (bottom of the head <= 805)
  - lf1: centre y 713 .. 804, x -28 .. 299, head width <= 101 px  (bottom of the head <= 854)
  - lf2: centre y 670 .. 724, x -52 .. 468, head width <= 59 px  (bottom of the head <= 753)
  - lf3: centre y 701 .. 756, x 208 .. 531, head width <= 80 px  (bottom of the head <= 797)

Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`.
