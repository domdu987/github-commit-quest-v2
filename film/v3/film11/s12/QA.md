# s12 QA: film 11 shot 12 (24.10-25.86 s, g 723..775; file g 717..781)
room_day / A. James on the bed edge (mirrored, stool=0) rubs the armpit under his sore arm with the other hand (small circles), wince (worried eyes, frown, head roll 6 deg),
the blister card sits on his front arm; mother stands worried to the right (wringing hands). Jenner not shown (plan lists only James + mother). Heads 115-135 px, centres y 545-625, nothing below 880.
Weakness: the rubbing is a small hand motion at 6 fps scale (readable on the full-size frame, subtle on the phone sheet). Mouths still. 14 % push. 6 fps contact checked.

## Gate-1 fix round (2026-11-18)
- The hanging green 'lamp' on James's head was a herb bundle merged into the room mesh: `Take.cut_boxes` collapses its vertices at runtime; re-rendered, nothing hangs over James.
- James is now NOT mirrored (faces the camera, yaw +0.15): blister card on his viewer-left arm (`upper_arm_l`), same arm as s02/s07/s08; the right hand rubs under it (circles).
