# film-13 QA, QA-tech sF v5 (team1 4277f66)

**Verdict: PASS** (0 blocking, notes below). Take `take.mkv`, 98 frames, 720x1280, g1044-1141. Checked: all frames extracted at full size, every 5th frame, 1 fps sheet, every frame g1084-1096 (mouth start), per-frame difference over all 98 frames, camera motion per frame (LK flow on the foreground grass, phase correlation on hills and sky). Colour and exposure are left to the grade.

## Checks
- Camera never freezes: foreground grass moves from g1045 on (ease-in 0.1 -> 2.5 px/frame by g1066, scale grows every frame), then the CU2 push (hills up to 13 px/frame at g1121), settling to ~1 px/frame at g1141. No still run of 1 s or more; the slow dolly g1044-1078 is why rhythm median is 3.2. No shake (smooth monotone paths, no sign flips).
- Pops / frozen / black: frame diff 1.6-12.4, no spike outside the push. qa_auto PASS, magenta 0 %.
- Mouth: Cressingham closed through g1092, open from g1093 (window g1093-1140). Laughers' mouths open only for the laugh. OK.
- Heads all above y 880 (CU2 face about y 300-650). Ground PASS, contact shadows on all cards. No Thai text in frame. Bloodless.
- Plan: English laughing on the south bank, bouncing out of phase, camera moving, CU2 push into the smug face with the line. Covered.

## Notes (not blocking)
- N1: the dark banner fragment cut by the top-right edge is still there and bigger (x 650-720, y 100-340, g1044-~1098). Hide it like the smoke.
- N2: the only pointing arm (front-left laugher) leaves the frame by the left edge, hand off-screen (g1044-1100). See QA_ART B1.
- N3: a dark sack is cut by the right edge at y 780-850 (g1044-1090), and the side laughers are cut while leaving in the push (g1105-1135, documented).
- N4: the bridge is not readable (a sliver at the right, y ~650). Judged in QA_ART.
