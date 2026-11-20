# QA_TECH s15

## Round 2 - FAIL
Checked: qa_auto PASS (g1190 cut not visible in range: continuous handle, expected), meta g0 1096/g1 1190 handles 10/9 DIS 15 OK, framediff 5.08 / 13.96 OK. Cards and camera ride the ship: horizon, rail and deck shadows stay locked to the cards, no sliding found. Sun overhead: the mast shadow shrinks and curls in over g1096-1180, reads OK. Mouths fixed (frown). Contact shadows under shoes present. Snap g1168-1184 on อยู่ตรงหัว (g1172) OK.
1. g1184-1190: William's hat brim and head touch/clip at the LEFT frame edge during the final hold (head x ~0). Fix: recentre the final settle ~0.15 m right.
2. g1160-1176: the captain is cut by the left edge (arm/body) during the snap. Fix: shift the captain mark right or loosen the push.
3. NOTE: William looks at the lens, not up at the sun; the quadrant is raised at the forehead tilted aside rather than aimed straight up. Not blocking at phone size.

## Round 4: PASS
Checked 6 fps (take g1086-1198), qa_auto PASS. No text, black/magenta, frozen, blur, mouths closed (frown). Frame-diff g1097-1189 median 4.54 / p90 12.27 OK. Ship ride (deck, rail, cards) consistent; sun overhead and the glare disc appear after the snap on "อยู่ตรงหัว".
Earlier issues: R2-1 (William hat at left edge at the end) FIXED, William now at right with face inside; R2-2 (captain cut by left edge) FIXED: captain fully inside until g1160; at g1176-1189 his hat brim touches the left edge (face and body inside) = NOTE; R2-3 NOTE: William now squints up with the quadrant raised, OK.
Notes: William's quadrant tip / hat brim touches the right edge g1181-1189 (face intact). Captain feet shadows present.

## Round 8 (director QA-tech): FAIL
Checked: merged take s15 (203 frames, g1086-1288, in-shot g1096-1279) at 6 fps plus every frame g1160-1230 (frames in /tmp/qa19_r8/s15/, name = g-1086). No black/magenta frames, no pops, no mouth movement (William and captain frowning or smiling with closed mouths; none moving). Heads max y 835 (<880), faces about 19 % of frame height (<35 %), contact shadows under shoes present throughout.
Frame-diff (90x160 grey, bilinear, in-shot pairs g1097-1279, n=183): median 4.08, p90 10.70, min 2.76, max 13.50. Numeric target (median >=4, p90 >=10) met, but only just, and the number is made by camera and light motion, not by acting (see 1, 2).
1. g1229-1279 (last ~2 s, diff 3.5 falling to 2.8): NOT frozen at the pixel level (min 2.76; the camera drifts, the deck roll and sea move, and the mast and rigging shift), but the characters are held in the same pose: the diff over the character region is about the same as over the plain deck. William's H4 pose and the captain's idle pose do not change. It is a camera-only run, near-frozen as acting. FAIL under §I5.
2. g1096-1160 and g1189-1279: both characters hold fixed idle or pose cycles on one spot (about 2 s at the start, 3 s at the end with no body motion): "nobody still for more than 1.5 s" is broken. Only g1160-1188 (snap) and g1190-1226 (lower, turn to H4) show body motion.
3. Plan coverage g1230-1279: the captain does NOT step in and lean to look at the H4. He stays on his mark at left, upright, looking at the lens, for the whole take. The sailors are tiny in the background (g1210-1279), the right one jiggles in place and no rope is visible or hauled; at g1270-1279 the sailors are cut by the left and right frame edges. Plan beat missing. Fix: key the captain from his mark to William's side, with a lean toward the watch, g1200-1250; show rope and haul loop for the sailors, keep them inside the frame.
4. Captain "glide 0.6 D" during the pull-back (g1190-1226): on screen he drifts from the left edge toward centre (x about 60 -> 85 px of 250, while the camera moves back and he shrinks), feet in contact with the deck and the shadow, no walk cycle. Because he is parented to the ship and the camera moves, he does not slide against the deck planks or the mast shadow; he looks planted and the crane reads as a camera move. I do not rate it as floating/sliding. But the drift is not a mark move, so the team's "0.6 D glide" is camera parallax, not captain motion.
5. g1160-1178 (William quadrant up): William's quadrant tip and the captain's hat brim touch the left frame edge (g1170-1182). NOTE, not blocking (faces inside).
6. NOTE: the sun disc appears at g1176 and is a flat white disc; at g1218 it sits beside the rigging, fine.
Verdict: FAIL (issues 1, 2, 3).
