# QA-tech round 14b s19: FAIL
Checked: all frames at 6 fps (g1427-1514), every frame g1478-1490 (mouth/pot), 2x crops of g1443/1445/1457 (flame gaps), 20 px block ground mask on 15 frames, frame-diff 90x160 (median 11.21, p90 14.19; matches meta). No pulsing, no placeholders, mouths held, no text.

## Blockers
1. Prop crosses a face (§G), repeat from round 13. g1481-1484: the terracotta pot at lower right sits under/in front of the lead ox's jaw. The pot rim covers the chin at g1481-1483 and the lower jaw/tongue at g1484 (mouth bottom ~y815-830, rim at ~y805-830). Fix: move that pot 100+ px right or 120 px lower (rim top >= y860 in g1478-1487), or hide it. The ox mouth itself is now fine (see passed).
2. Ground > 30 %. Block mask (smooth, outline-free 20 px blocks below the wall base): 0.36 g1427, 0.34 g1439, 0.36 g1445, 0.37 g1457, 0.36 g1463, 0.35 g1481, 0.34 g1487/1493, 0.35 g1505; only g1433/1451/1469/1475/1499 are 0.28-0.32. Visually y 830-1280 (about 35 %) is plain dirt in g1427-1470. Team has no real measurement (QA.md says "not done"). Fix: add dark low props (sacks, reed bundles, low jars with outlines) across y 900-1250 at the bottom of frame, or tilt the camera up ~60 px so the horizon sits higher; target <= 28 % on the mask.

## Passed
- Flame gap (rendered pixels, 2x): g1443 ~10 px, g1445 ~12 px, g1457 ~10 px between a far-lane ox's tail flame and the neighbouring far ox's horn tip. Never an overlap, nothing under 5 px. Decision: NOTE, not a blocker (round 12: dense herd, no overlap, >= 15 px target; 10-14 px at 3 frames of 28 px flames on the far lane). The near lane flames are 40+ px clear of every face/horn/blade.
- Ox mouths y <= 860: lowest mouth/tongue edge g1478 ~800, g1480 ~815, g1482 ~822, g1484 hidden by pot, never > 830. PASS (round 13 failure fixed).
- Painted blue rim: reads as a thin clean outline on the upper/right edge of the oxen and Qi, no doubled edges, no glitch. Fine.
- Whip blur g1505+ accepted.
- Subject in frame; props otherwise off faces (helmet now left, x<200, g1445 only).

## Notes
- Herd density (visible oxen per 0.5 s tile): lead + 1 small far ox + 0-1 more, i.e. 2-3 oxen (plus Qi silhouettes) in tiles g1427-1500; 6-7 only from g1507 (whip landing). Team admits 5 per tile not reached. Weak "burst" read; accepted at round 13, still weak.
- Flames are 25-30 px and tiny at phone size; fire-behind idea reads only on the poles.
- Lead ox leaves the right edge g1484-1488 (exit, head cut by edge for ~4 frames); acceptable as an exit, no hold.
- Near pots at g1427-1449 are still lavender-violet, not warm.
