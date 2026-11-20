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

## Round 9 (director QA-tech): FAIL
Take: take.mkv.partaa+partab, 203 frames 720x1280. Frames: /tmp/qa19_r9/s15/ (six/ = 6 fps, all/ = every frame, i = g-1086). Checked 6 fps plus every frame g1160-1280. No black frames (min luma 91), no frozen runs (min diff 1.64), no magenta/text, no character cut in half, nothing floating (contact shadows under all feet), no prop through a face.

Frame-diff (own run, 90x160 grey, bilinear, g1097-1279): median 4.84 (>=4 OK), p90 11.18 (>=10 OK), min 1.64, max 19.7. Caveat: p90 is carried by the camera tilt at g1166-1184 (diff 8-20). Last 2 s (g1220-1279) mean 4.04; the "2.4" belongs to g1187-1190 only.

Issues
1. g1207-1229 SUN DISC BLINKS OUT: the disc fades 255 -> 91 in 3 frames (g1207-1210), is replaced by a dull grey patch (about 165, the sail colour) until g1226 and snaps back g1227-1229. About 22 frames (0.7 s) with no sun during snap2 and the dial push-in. Unintended pop. Fix: keep the disc and halo at constant strength through g1196-1240, or fade over at least 12 frames.
2. g1238-1262 William's glance is NOT visible: eyes stay closed-smile in every frame (g1236, 1248, 1258, 1268, 1279). Fix: add open eyes with a glance up and back.
3. g1248-1279 (1.0 s): both principals hold the same pose. Only the captain's face and the watch sway change, and the crane moves slowly. Under 1.5 s so not a hard fail, but it reads static. Only the sailors move (striped sailor hauls, red-bandana sailor appears behind the captain's head from g1244).
4. g1218-1242 captain's hat brim touches or clips the LEFT frame edge during the peak push (face inside, skin x >= 25). The dial at the peak is about 170-190 px: OK. Fix: nudge the captain 40 px right or ease the push.
5. Claim 1 only partly true. The diagonal sail shadow does NOT disappear at g1171. It stays on the lower left to g1279 (g1171-1174 still a big dark diagonal). The change is smooth with no pop at g1171 (diff 19.5 vs 17.9 and 19.7 neighbours, continuous). The deck is 25-28 % of the frame (orange mask) from g1172, a hair over the claimed 25 %. The sun is top-centre at (359,124) from g1166, camera-parented.
6. Claim 2 only partly confirmed. Hands read 8:00 and the dial is about 170-190 px. I could NOT reproduce "face = 37 %": measured face-only max 188 px = 14.7 % of 1280 (g1230-1232); hat-top to chin about 330 px = 26 %. Frames over 35 %: 0 (peak margin about 9 points under). Close-ups under §I.6: 1 push (g1212-1240), within the limit of 3.
7. Note: from g1236 the captain's mouth is an open "O" (shock) held to g1279 with one blink at g1268. It reads as an expression, not talking. Mouth flapping outside the quote window: none seen.

Claim 3 (sun top, watch bottom in the last 2 s, slow crane up): CONFIRMED (sun top-centre and constant, watch at y about 800-900, deck about 25 %). Claim 4: captain shock from g1236 CONFIRMED, William glance MISSING (issue 2), sailors stay in frame CONFIRMED. Claim 5: deck dressed (lamps, rope coils, rails, sailors): OK.
Fix items 1 and 2 are blocking; 3-4 should be fixed in the same re-render.
