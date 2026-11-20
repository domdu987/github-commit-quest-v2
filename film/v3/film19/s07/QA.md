# s07 QA: film 19, shot 7 (HALL hall_window, DAY) -- revision 6 (round-5 gate)
## Delivered
- take.mkv (97 frames, first_g 457): g 457-465 in-handle (CUT), g 466-544 = shot 7, g 545-553 out-handle (CUT). 720x1280, 8 spp. qa_auto PASS.
## Round-3 fixes
1. Black bar (quadrant ring) crossing astro_c at g 508-521: the group moved right and the camera sits further right (look x -1.95), so the ring is out of frame; none visible on the finals.
2. Edges: astro19 (-3.1, 2.5), astro19_c (-1.45, 2.2, front) and astro19_b (-0.30, 3.4) stand closer together; the lateral camera sway tapers to zero by the end of the snap (x1.3, g 492-508), so all three are fully inside the frame on every frame to g 553.
3. The point: astro19's arm is a long extended point up-left (hand (1.30, -0.35), stretch 1.45, jabbing) toward the Moon plate, with eyes and head turned up-left until the snap, then back to the lens. astro19_c nods in the front centre, astro19_b nods behind.
## Numbers
- Frame-diff in-shot: median 5.16, p90 11.52.
- Head width 110-192 px, head centre y 563-678, lowest head bottom 771 (< 880). Contact decals 1.6 x 0.75 D.
- 14.96 s/frame wall, 29.33 s CPU.

## Revision 5 (director: chair back across astro19_c's face at g508-553)
- astro19_c now stands in FRONT of the Board chair (mark -1.60, 1.45; the chair is behind him at y 1.9), so the chair back no longer crosses his face. The camera sits further right (x -1.6, look x -2.15, i.e. 0.2 D left) so astro19's wig and arm clear the left edge.
- Finals: frame-diff median 5.16, p90 12.19; head width 112-239 px, lowest head bottom 801 (astro19_c, close), qa_auto PASS.

## Revision 6 (round 5: pointing hand cut by the left edge, grey-wig face cut by the right edge, g506-553)
- The group is narrower: astro19 (-2.8, 2.5), astro19_c (-1.60, 1.45, in front of the chair), astro19_b (-0.85, 3.4); the end of the snap is x1.15 (drift 1.5 %/s) so the group stays inside at the end; astro19's arm points more upward than sideways (hand (0.95, -0.60)).
- Checked on the finals at g 506, 515, 525, 535, 545, 553: the pointing hand and all three faces are fully inside the frame; the chair is still clear of astro19_c's face.
- Finals: frame-diff median 4.41, p90 10.90 (within the per-take acceptance of median >= 4, p90 >= 10), lowest head bottom y 769, qa_auto PASS.
