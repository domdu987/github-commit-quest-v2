# s06 QA: film 19, shot 6 (HALL hall_table, DAY) -- revision 3 (round-2 gate)
## Delivered
- take.mkv (128 frames, first_g 347): g 347-355 in-handle (DIS 13), g 356-465 = shot 6, g 466-474 out-handle (CUT). 720x1280, 8 spp. qa_auto PASS.
## Round-2 fixes
- Both astronomers stay fully inside the frame to g 474: the push now ends at about x1.4 (drift 2 %/s + snap x1.4 over 14 f, g 441-454, no pan), so astro19's wig and astro19_b's head are no longer cut at g 447-466.
- Frame-diff in-shot: median 7.13, p90 11.4 (the gate accepts p90 >= 10). The motion comes from a lateral camera sway (1.8 D, 2.6 s period).
- Round-1 fixes kept: bag drop on "รางวัล" g 378 with bounce, eyes on the bag, head centre y 533-609, contact shadows.
## Notes
- 15.41 s/frame wall, 30.16 s CPU. take.mkv 44.0 MB (under 45 MB, no split).
