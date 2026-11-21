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
- Camera: the set's 3-key BIGZOOM path put both cyclists out of frame mid-move (x -600 .. -80, head y up to 1175). Re-keyed at runtime (`CAM_KEYS`): same start idea (4.7-6 D from
  their faces), a mid key from the south-east, the same wide end (5.5, -59, 7.4); the end look-at is lowered so the cyclists' heads stay above the caption band.
  Cyclists: head centre y 662-789 (head width up to 152 px at the close start, bottom <= 865), x 138-685 on every frame (inside the frame the whole move).
- The four lifters are on screen from g 1319 (they are behind / beside the camera while it swings past, g 1298-1312: the stage's head report gives garbage there, QA_NUMBERS.json `lf*`).
  From g 1319 on their heads are at y ~ 565-660 (head width 25-45 px: it is the wide reveal), well above y 880.
- Deviation: none against the plan; rhythm numbers meet the rule (median 5.83, p90 15.14).
