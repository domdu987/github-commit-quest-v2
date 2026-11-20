# QA_TECH s17 - FAIL
Checked: qa_auto PASS (planned cut g1280 not visible, expected: continuous handle), 6 fps + cut sheet g1271-1391, meta g0 1280 / g1 1383 (plan 42.65-46.12 -> 1280/1383 OK), CUT in + 9 f out-handle for DIS 11 OK. No actors, no text, no blur, no black/magenta, ship intact (all sails set), NOON.
Issues:
1. Whole shot: frame-diff median 1.88 / p90 2.73 (limit >= 4 / >= 12). The shot reads as near-static: ship stays centred, sea scrolls slowly, snap g1368-1384 only a mild scale change. Fix: stronger pull + slide/orbit, bigger snap-back (x0.55 does not read), add moving foreground (gulls/spray) or a faster sea.
2. g1271-1391 (plan coverage): "V-wake lengthening behind it" is not visible; the wake is a short spray fan at the stern of constant length, no trailing V on the sea. Fix: add a long trailing wake ribbon that grows with the pull-back.
3. g1271-1391: bottom ~55 % of frame is flat empty teal water (no reflections or detail), subject sits in the upper half; weak on phone. Fix: tilt/crane so the ship sits at y ~ 450-700 or add wake/foam trail in the lower half.
4. g1321-1371: gull at the right edge is clipped by the frame (x ~ 720, y ~ 1000-1100). Minor.

## Round 2 - FAIL
Checked: qa_auto PASS, meta g0 1280/g1 1383 handles OK, CUT in, no actors, no text, NOON, ship intact.
1. Earlier 1 (frame-diff) improved but NOT fixed: median 3.99 (limit 4) / p90 5.03 (limit 12). p90 fails by a wide margin: the middle of the shot is a slow drift. Fix: stronger slide/crane in the middle and a bigger snap-back.
2. Earlier 2 (V-wake lengthening) NOT fixed: only a short white spray fan at the stern and a ring ripple round the hull, no long trailing V. Fix: long wake ribbons that grow with the pull-back.
3. Earlier 3 (empty teal lower half) improved, the ship now sits lower from g1310; NOTE.
4. Earlier 4 (gull clipped at the right edge) gone, but NEW g1310-1350: the ship's hull and stern are clipped by the LEFT frame edge and a large foreground gull is clipped at the left edge (g ~1340-1360), then the ship is cut at the bottom. Fix: keep the crane/slide from dragging the ship off-frame; keep the ship x 150-570.

## Round 5: FAIL
Checked 6 fps + cut g1280/g1384 +-3 (take g1271-1392), qa_auto PASS (soft g1387-1392 = dissolve handle). No actors, no text/black/magenta/frozen. Frame-diff g1281-1383: median 3.54 / p90 4.49 (rule 4 / 10): worse than round 2 (3.99 / 5.03).
Earlier: R2-1 NOT FIXED; R2-4 ship clipping FIXED (ship stays inside x 60-560 through the crane); R2-2 V-wake: a long wake ribbon now trails, FIXED.
1. g1281-1383 (frame-diff): median 3.54 < 4 and p90 4.49 < 10; the move is a uniform slow drift. Fix: add a clear eased push/slide accent (about 1.3x over 12 f around g1340-1355) and raise the base speed so the median >= 4.5 and p90 >= 10; re-measure.
NOTES: g1271-1290 white glare patches at the left of the wake read as holes.

## Round 10 (director QA-tech): PASS
Take g1271-1392 (joined parts -> /tmp/s17q.mkv, 122 frames). Frames /tmp/qa19_r10c/s17/. 6 fps sheet plus the snap g1368-1384 checked. Frame-diff (90x160 grey bilinear, pairs g1281..g1383): median 4.71, p90 10.65 (limits 4 / 10: OK), max 25.7 at g1377 (the pan snap, eases in from g1370 and out by g1383). Colour sat 0.712, luma 108.0. No actors, no text, no black/magenta/frozen frames (min diff 2.36), no pop, ship intact in frame all through, no edge of the world or bare plane (horizon and sky only), whitecaps now visible, V-wake lengthens as the camera pulls back and rises.
Notes (not blocking):
- g1340-1369 the move is slow (diff 2-3, about 1 s) before the snap; the median clears only because of the snap.
- g1271-1310 big white glint patches left of the ship read as holes (g1271-1290 most).
- Sails are grey in the backlit first half and cream later (lighting angle, plausible).
