# QA-tech TAKE gate round 6, film 20: s24 (BIGZOOM 2, plan g1732-1852, take g1724-1858)
Verdict: **PASS with notes** (the round-5 failures are fixed; one small new defect, one soft spec note).
Note: take.mkv is the round-5 re-render commit f78682c (stats identical to its QA.md); frames extracted 135, viewed every 5th at 360x640 and g1781/1784/1804/1830/1858 at 720x1280.

## Round-5 failures
1. Orange wedge / X wall bands behind his head g1804-1858: FIXED. Behind him is now a plain panelled back wall, carpet, tables and diners; only the top ~25 % of the frame is the dark-red ceiling truss with chandeliers, clear of his head (head y ~0.36-0.52 H).
2. Thin black vertical seam chair -> bottom edge g1799-1858: FIXED (bottom 180 px column scan has no dark outlier line at g1799/1815/1830/1858; chair, blue seat, carpet read clean). Flat orange floor strip: GONE (parquet floor + carpet).

## Numbers
qa_stats sat 0.636, luma 93.1, motion median 4.36 / p90 13.21. qa_stats2 vivid 64.8 %, warm 61.6 / cool 21.7. qa_auto PASS. All inside spec (sat >= 0.50, vivid >= 45, luma 85-110).
Own frame diff (90x160 grey): smooth ramp, peak 43.6 at g1795, no step; no hard cut. The 3 "shots" in qa_stats are the whip (g1778-1800, ~0.7 s of diff 30-44, longer than the ~6 frames in QA.md but continuous) = false positive.

## Spec
- BIGZOOM: g1724 wide, tower + Paris, he is a speck (<5 %); lands medium g~1819 = 3.2 s, ease in/out, passes lattice girders and the RESTAURANT sign. OK.
- First bite: forkful at the mouth g1810-1820 (and again g1857), fork lowers, cheek chew. OK, reads clearly.
- Faces: head 201 px max = 16 % H (<= 35 %). Ground (floor/carpet) ~15-20 % (<= 25 %). OK.
- Join to s25: plain 9-frame dissolve, accepted in the TAKE5 section E ruling; head position stays ~0.45 W / 0.45-0.5 H.

## Notes (do not block)
- N1 (new, minor): thin green slanted sticks poke out behind the diners at the left (x 0-90) and right (x 570-720) of the room, y ~0.43-0.5 H, g1804-1858 (crop at 720x1280 in g1804). They read as tilted stray members / plants intersecting chairs and heads. Fix if cheap: hide the green objects (tower plant/lattice leftovers) in the room box at runtime; else leave.
- N2: visible figure (hair to tablecloth) is ~27 % of frame H, below the 35-60 % medium band (head 16 %, the table hides the rest). Round-4 text claimed ~35 %. Acceptable as a seated medium at this table height, but if a re-render happens, push in ~15 % at the landing.
- N3: upper ~25 % is a heavy dark-red truss (not orange wedge); acceptable as the room ceiling.
