# QA-tech round 13 s19: FAIL
Checked: all frames g1427-1514 at 6 fps; every 2nd frame g1427-1499 (band y650-850, 1:1); mouth crops g1477-1488 at 2x with y860/880 lines; frame-diff re-measured 90x160 (median 10.97, p90 13.72, OK, no pulsing); ground colour-mask estimate on 10 frames.

## Blockers
1. Ox mouth below y 860 (hard check; QA.md claims worst 857). Measured on 2x crops of the lowest edge of the mouth/tongue: g1479 ~856, g1480 ~868, g1481 ~877, g1482 ~882, g1483 ~878, g1484 ~880 (g1485 head leaves frame bottom/cut by pot). So g1480-1484 are 8-22 px over the limit, touching the caption line y880. Fix: tilt the camera up ~30 px or lift the lead ox / move its lane 0.3 D deeper in g1478-1485 so the mouth stays <= 850; re-measure the mouth, not the head box.
2. Prop through a face: at g1483-1485 the terracotta pot at lower right sits in front of the lead ox's mouth/chin (the pot rim covers the lower jaw, g1484 the tongue is cut by the rim). Fix: move that pot 80-100 px right or lower it out of the ox's face band (y < 880) in g1480-1486.

## Checked and passed
- Flame vs face/horn/blade, g1427-1499 (every 2nd frame, plus 1:1 crops): no overlap. Nearest approaches I can see: g1451 flame to left ox horn about 80 px, g1455 about 130, g1469 about 110, g1481 about 90. I could not find anything below the claimed 38 px; the team's 38 px figure is plausible and the 15 px gap holds. Each flame sits on its own ox's tail torch (a stick with a ~25-30 px flame at the end, trailing behind). g1500-1514 whip frames: flames far from faces.
- Placeholders: none (wall stones textured, pots terracotta/striped, helmet fan warm). Pots read lavender at g1427-1447 (note).
- Subject in frame: yes. No zoom pulsing (eased dolly/truck). Mouths held. No text. Blur g1505+ accepted as whip.
- Frame-diff: 10.97 / 13.72.

## Notes
- Ground (colour-mask estimate, props included in the mask): 0.35 g1430, 0.37 g1441, 0.36 g1451, 0.34 g1461, 0.28 g1469, 0.26 g1476, 0.35 g1483, 0.35 g1491. Team figure 0.15-0.28 does not reproduce; with pots subtracted I read about 0.28-0.33, i.e. on the 30 % edge. Add one low dark prop at lower left in g1427-1465 and g1483-1500 to be safe. Not blocking alone.
- Herd read: 1-2 oxen are visible at a time (one big, one small behind) plus black Qi silhouettes. It reads as a few oxen trotting out, not a herd pouring out. The only herd read is the g1507-1514 landing (6-7 small oxen in a row at the horizon). Accepted under round 12 decisions, but weak.
- Oxen are small (head about 100 px), flames about 25-30 px: the film's key idea (fire behind the oxen) reads only on the pole, not as a big flame.
- Black Qi silhouette at g1427-1449 overlaps the lead ox's tail torch slightly (silhouette only).
