# s11 QA: film 11 shot 11 (22.40-24.10 s, g 672..722; file g 666..728)
room_day / A, new angle (closer, from the foot of the bed): James on the bed edge, pale blister with a red ring on his front arm (card), Jenner writes in his notebook
(jenner_write, mirrored, quill). Heads 160-170 px, centres y 530-600. Mother stands just off screen right (deviation, framing too tight for three). Mouths still. 12 % push. 6 fps contact checked.

## Gate-1 fix round (2026-11-18)
- The hanging green 'lamp' on James's head was one of the room's herb bundles (merged into the room mesh): `Take.cut_boxes` collapses its vertices (and the one at (0,5.2)) at runtime; re-rendered.
- James is now NOT mirrored (faces screen-right via yaw +0.45): the sore card sits on his viewer-left arm (`upper_arm_l`), same arm as s02/s07/s08.
- s11: James sits close to the left frame edge (head x ~ 40-90 px of 180 in the sheet); mother still off screen.
