# QA-tech round 11 s19: FAIL
Checked: 33 frames (6 fps g1427-1514 + the whole g1500-1514 whip-landing run at every frame), phone strips with y 860/880 lines, full-size crops g1457/1477/1482/1487 with a drawn y 860 line. Director 11.21/15.38: OK, no pulsing. NIGHT, no text. Purple/indigo strip: GONE. Flames are red teardrops on tail tips trailing backward.

## Blur decision (qa_auto "suspected blur" g1505-1514): NOT a defect, accepted.
Measured Laplacian variance of the herd/pot band (y 580-900) is 330-410 for g1497-1514, equal to the pre-whip frames (340-380); the global value falls from ~210 to ~130 only because the frame becomes 55 % smooth night sky. Visual check at full size (g1510): outlines, horns, pots and the herd are crisp, no smear, no ghosting, no double image. The camera is a held, static landing from g1507 on. The auto test is a false positive on a low-detail sky; nothing to fix.

## Previous blocking notes
1. Oxen faces below y 860: NOT FIXED. Measured on the rendered frames (lowest mouth/chin pixel): g1457 y ~895, g1477 y ~925, g1482 y ~905, g1487 y ~1025 (the lead ox's mouth is at y 940-1025 at g1487), g1462 y ~860-870, g1432 ~857 (ok). The team's "790-860" is not what the pixels show.
2. Flame within 60 px of a face: NOT FIXED at g1452-1462: at g1457 a big flame (x 470-720, y 730-830) touches the lead ox's horn and is ~15-30 px from its face (x 360-520, y 780-900), reading as fire at the head. (g1467-1482 is OK, > 150 px.)
3. Bare ground > 30 %: NOT FIXED (see blocking 2).

## Blocking
1. g1457-1497 - ox mouths/chins below the caption line: lowest mouth pixel y ~895 (g1457), ~925 (g1477), ~905 (g1482), ~1025 (g1487), ~960 (g1492/1497). Fix: raise the camera by ~0.5 D and pitch it down a further 6-7 degrees so the herd sits at y 0.40-0.62 (the lowest mouth pixel must reach <= 860), or push the lead ox back 1.5 D at g1480-1500; measure the lowest mouth pixel of every ox <= 860 on g1457, 1477, 1482, 1487, 1492, 1497.
2. g1427-1452 and g1487-1503 - bare ground: below the herd (y > 0.68) the frame is 32-40 % plain gravel with no prop (g1427-1452 almost fully plain, pure purple; g1492-1503 ~35 %, only faint warm pools). Fix: the pots/jars that appear at g1505 must be in the lower corners from g1427, sliding across, or tilt up so the ground is <= 25 %.
3. g1452-1462 - flame near the lead ox's face (see above). Fix: delay the rear ox's flame by 8 frames or shorten that flame card and offset it >= 60 px from the lead ox's head.

## Notes
- g1505-1514 landing is good: pots in fg, herd at the horizon, lead mouths at y ~790-820, sharp.
- Qi silhouettes are only 1-2, black, fine.
- Mouths of the oxen are open roars, no lip-sync question (outside the quote windows these are held roars).
