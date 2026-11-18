# s10 QA: film 11 shot 10 (20.71-22.40 s, g 621..671; file g 615..677), dissolve in 8 (6 handle frames before g 621 rendered)
room_day / A. James sits on the bed edge (mirrored, faces screen-right, stool=0, seat on the quilt top; contact decal off), small red dot card on his front arm
(anchor `upper_arm_r` because mirrored anchors are named by screen side); Jenner (neutral, leans in 9 deg) and mother (stand_worried) look at it. Heads 100-130 px, centres y 550-620, no head under 880.
Deviation: the plan says "mother and Jenner look at James's arm" and the set has the boy in bed (lying); I seat him on the bed edge so the sore is visible (sleeve rolled), the quilt hides his legs.
Mouths still. Slow 12 % push. 6 fps contact checked.

## Gate-1 fix round (2026-11-18)
- The hanging green 'lamp' on James's head was one of the room's herb bundles (merged into the room mesh): `Take.cut_boxes` collapses its vertices (and the one at (0,5.2)) at runtime; re-rendered.
- James is now NOT mirrored (faces screen-right via yaw +0.45): the sore card sits on his viewer-left arm (`upper_arm_l`), same arm as s02/s07/s08.
- Eye-lines: Jenner and mother look down-left at James's arm (gaze (-0.9, 0.7) / (-0.9, 0.5)).
