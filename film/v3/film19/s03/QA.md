# s03 QA: film 19, shot 3 (HALL hall_window, DAY) -- revision 2 (after QA_TECH FAIL)
## Delivered
- take.mkv (99 frames, first_g 101): g 101-109 in-handle (CUT), g 110-190 = shot 3, g 191-199 out-handle (DIS 13). 720x1280, 8 spp. qa_auto PASS.
## Fixes for QA_TECH s03
1. Black tripod wedge g190-199: the camera no longer swings across the left foreground (arc -13 deg/s, slide -40 px/s; the earlier -21 deg/s arc is gone). Only a thin dark tripod leg remains at the far left edge.
2. astro_b clipped: both astronomers are fully inside the frame to g 199 (snap x1.9 with shift +0.3).
3. Peering: astro_b's mark is at the eyepiece depth (mark -3.80, 3.45); he bends (lean 23, crouch 0.30) so his face is at the eyepiece (eyepiece px 246,666 vs head 248,680 at g 110), then straightens with a frown on the snap.
4. Contact shadows: decal widened and darkened for both (1.6 x 0.75 D, #1a1626, opacity 0.9).
5. astro19 moved off the chair (mark -2.10, 4.00).
## Numbers
- Frame-diff in-shot: median 2.98, p90 10.99. **Both are below the first delivery (4.75 / 15.6): median < 4 and p90 < 12 now.** Cause: the strong left arc that made the median is what swung the camera across the tripod / black quadrant arc; stronger slide or arc brought the black arc back into frame (checked at slide -55/-65). Kept the clean framing.
- Head width 100-228 px, head centre y 598-695, lowest head bottom 764 (< 880).
- 9.87 s/frame wall, 19.45 s CPU.
## Known
- The sprite crouch makes astro_b's legs look bent as he leans; it reads as bending to the eyepiece at phone size.
