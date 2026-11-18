# s28 QA (shots 28-30, g1908-2104, head handle 1908-1913)
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg). Own 6 fps + cuts g1962/2032 checked.
- Shot 28: edge_* kitchen-garden clutter cut at runtime (clutter-free foreground), contact shadows, sky ~17%, held mouths only. Soil fills lower third (people ppd 128 are small at this framing).
- Shot 29: uncle parented to the stool card (one sprite, no sliding); bee darts to nose at g1990.
- Shot 30: nose_swell 0.15 -> 1 over g2045-2088; nose tip and head above y880.
- No lip-sync anywhere. Frame times ~45 s wall (2 procs); render resumed after a container restart (frames on disk reused).

## v2 (director fixes)
- Shot 28: uncle 3/4 toward farmer holding the empty hive box in both hands at chest height, sad brows + wavy mouth + downcast gaze, shrug/head tilt; farmer grin and hat-tip; camera lower/tilted up and pushed in (ground ~35 %, sky ~22 %); both fully in frame.
- Shot 29: visible lift of the hive onto the bar g1962-1985; bee flies from the hive and touches the nose at g1990, red nose g1990-1991; camera lowered so stool/grass end near y 880.
- Shot 30: closer (about 1.3x), no stool continuity break, hive and hook in frame, trunk tip curl g2086+ and blink g2095-2099; trunk tip stays above y 880.

## v3 (director re-check)
Shot 30 only re-rendered: he stands on the same stool as in shot 29 (stool=1, CANVAS14_STOOL), so the cut 29->30 no longer drops him by the stool height. Deviation: "bottom edge above his knees" is incompatible with the full-length trunk tip staying above y 880 at this head size (knees at about y 900), so the stool and feet remain visible in the lower frame (stool top ~y 985). Shots 28-29 unchanged.

## v4
Shot 30 only: nose_swell starts at 0.40 (matches the end of shot 29), held to g2044, eased 0.40 -> 1.0 over g2045-2088; trunk curl + blink kept; camera nudged so the cap top is inside the frame; trunk tip ~y 840 (< 880). qa_auto PASS.
