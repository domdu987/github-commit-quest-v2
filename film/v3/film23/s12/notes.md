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
