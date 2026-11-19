# QA-art RE-CHECK, film 14, s28 v4 (ENDING, shots 28-30, g1908-2104): PASS
What I reviewed: all 197 frames extracted. g2020-2050 frame by frame in a 240x427 (phone-size) grid. Shot 30 every 4th frame (g2032-2104, plus g2104) in a 180x320 grid. Full 720x1280 frames at g2031/2032, g2060/2088 and g2100/2104. Crops of the trunk tip (g2101) and the top edge (g2104). Pixel measurements for the trunk fill, the trunk's navy outline and the cap. A frame-by-frame md5 and pixel diff against v3 (takes/r5).

How v4 differs from v3: g1908-2031 differ only by encode noise (mean abs diff below 0.67/255, nothing visible). shot.py changes only two lines in shot 30: `base = 0.40` in pose30, and the camera head-height target 230 -> 248. c14.py is identical.

## v3 blocker
| item | status | note |
|---|---|---|
| Nose continuity, cut 29 -> 30 | FIXED | At g2031 the nose is the long ridged orange nose hanging to the chest. At g2032 it is the same long nose (larger only because of the closer framing), held through g2044, then swelling from g2045 on. There is no shrink and no second "grow from a bulb". This reads correctly both at phone size and at full size. |

## The other checks
| check | status | note |
|---|---|---|
| Swell to full trunk by ~g2088 | PASS | Trunk fill bottom: 490 (g2044), 637 (g2052), 758 (g2060), 809 (g2068), 848 (g2076), 856 (g2080). It plateaus by g2080 to g2088, then the tip curls and wiggles. |
| Trunk tip above y 880 | PASS (slim margin) | Lowest trunk fill row is y 868 and the lowest navy outline row is y 874 (g2101). It clears the band by about 6 px. Note that QA.md's "~y 840" is optimistic. The camera nudge moved the tip down about 20 px compared with v3's y 852. Do not lower the framing any further. |
| Stool continuity | PASS | Same trestle stool as in shot 29. Feet stay planted on the top bar throughout the shot, with no slide and no height drop at the cut. |
| Cap inside frame | FIXED | The cap outline's first row goes from y 27 (g2032) to y 5 (g2101). Row 0 has no cap pixels in any shot-30 frame. It is tight at the end, but it is inside the frame. |
| Last frame g2104 clean | PASS | Sharp, eyes open (the blink is g2095-2099), trunk tip mid-curl, nothing stray. Fine for the hard cut to black. |
| Anything new broken | none | Shots 28-29 are untouched. The stool legs reach into the caption band, which is the same accepted minor item as before. |

## Verdict: PASS
The nose now carries across the 29 -> 30 cut and keeps swelling to the full trunk. All earlier fixes hold. Non-blocking: the trunk tip clears y 880 by only about 6 px, and the cap clears the top edge by about 5 px at the end.
