# QA_TECH s17 - FAIL
Checked: qa_auto PASS (planned cut g1280 not visible, expected: continuous handle), 6 fps + cut sheet g1271-1391, meta g0 1280 / g1 1383 (plan 42.65-46.12 -> 1280/1383 OK), CUT in + 9 f out-handle for DIS 11 OK. No actors, no text, no blur, no black/magenta, ship intact (all sails set), NOON.
Issues:
1. Whole shot: frame-diff median 1.88 / p90 2.73 (limit >= 4 / >= 12). The shot reads as near-static: ship stays centred, sea scrolls slowly, snap g1368-1384 only a mild scale change. Fix: stronger pull + slide/orbit, bigger snap-back (x0.55 does not read), add moving foreground (gulls/spray) or a faster sea.
2. g1271-1391 (plan coverage): "V-wake lengthening behind it" is not visible; the wake is a short spray fan at the stern of constant length, no trailing V on the sea. Fix: add a long trailing wake ribbon that grows with the pull-back.
3. g1271-1391: bottom ~55 % of frame is flat empty teal water (no reflections or detail), subject sits in the upper half; weak on phone. Fix: tilt/crane so the ship sits at y ~ 450-700 or add wake/foam trail in the lower half.
4. g1321-1371: gull at the right edge is clipped by the frame (x ~ 720, y ~ 1000-1100). Minor.
