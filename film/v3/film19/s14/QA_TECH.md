# QA_TECH s14

## Round 2 - FAIL
Checked: qa_auto PASS, meta g0 1016/g1 1096 handles 9/9 DIS 11 OK, default look OK, DAY, no text, mouths fixed (closed-eye smile), snap g1071-1091 on เท่าจานรอง (g1079) present, push-in visible, no black/magenta/frozen.
1. framediff median 3.44 (limit 4) / p90 13.86: median fails. Fix: more drift or a live fore element before the snap.
2. g1075-1096: the snap target is badly framed: the H4 watch and its red cloth are cut by the LEFT frame edge, and Harrison's head is cut by the RIGHT edge (last ~20 frames). Fix: aim the snap pan at the H4 centre and pull back to keep H4 + Harrison head inside the frame (or pan more to the right so the H4 is centred).
3. g1039-1096: his open palm points to screen right, away from the H4 (which is at screen left). Eye-line is closed eyes. Fix: flip the arm toward the H4 or aim the pan so the gesture reads at the watch.
4. g1075-1096: bottom ~45 % of frame is blurry orange hot-patch smear (shop_clock DAY hot patches y 990-1150, WORKER19 s6). Fix: tilt up or frame above the bench.
5. No feet visible (behind bench), NOTE.

## Round 3: FAIL
Checked 6 fps (take g1007-1104), qa_auto PASS (no planned cuts: dissolve in). No text, no black/magenta, no frozen, no blur. Mouth: closed-eye smile. Default look, DAY. Head centre y ~ 500-540. Snap on เท่าจานรอง (g1079) present.
Earlier issues: R2-1 NOT FIXED; R2-2 FIXED (H4 on its cloth, H1 frame/wheel/balls at left, Harrison inside; hair only tangent at the right edge g1088-1095); R2-3 FIXED (arm reaches across to the H4 from g1047); R2-4 mostly FIXED (bottom 40 % is bench front and floor with wood grain and orange patches, no longer a flat smear; NOTE). QA_ART fixes (round 3 PASS 7.4): 1 FIXED, 2 partly (accepted by QA-art), 3 FIXED, 4 FIXED; the QA_ART tangent note (H1 frame upright on the H4 crown at g1087-1097) is still there.
1. g1017-1095 (R2-1): frame-diff (take.mkv, g1017-1095) median 3.73 (< 4), p90 11.91 (>= 10 OK); deliver framediff.json says median 3.43 / p90 11.18. Median fails the director's rule. Fix: more continuous drift in g1017-1075 (the wide is nearly static: pair diffs ~ 2-3), e.g. push 0.20 -> 0.28 or a lateral sway, without changing the snap framing.
Notes: Harrison hair tangent on the right edge g1088-1095 (nudge SNAPSX -0.05); H1/H4 tangent as per QA-art; no feet visible.

## Round 4: FAIL
Checked 6 fps + g1090-1095 at full size (take g1007-1104), qa_auto PASS. No text, black/magenta, frozen, blur. Mouth: closed-eye smile. Frame-diff g1017-1095 median 4.15 / p90 11.29: R3-1 FIXED (>= 4 / >= 10). H1 + H4 on red cloth, palm toward the H4 read.
1. g1084-1095 (new, clipping): during the snap settle Harrison drifts to the right and his head is cut by the RIGHT frame edge: ~20 % of the face (cheek, ear, hair) off at g1086, ~30 % at g1090-1095. Round 3 listed it as a tangent; it is now a face clip. Fix: shift SNAPSX by about -0.10 (or stop the slide) so his whole head stays inside x <= 700 through g1095; this also clears the H1/H4 tangent.

## Round 5: PASS
Checked 6 fps + g1084-1096 at full size (take g1007-1104), qa_auto PASS, no text/black/magenta/frozen/blur. Closed-eye smile mouth. Frame-diff g1017-1095: median 4.83 / p90 13.74 OK. Heads centre y ~ 510-600 (< 880).
Earlier: R4-1 FIXED: Harrison's whole face stays inside x <= 700 through g1095 (ponytail ends at the edge g1090-1095, face intact; at g1100+ in the out-handle the wig tip touches the edge, handle only).
NOTES: H1 + H4 on red cloth read; gears lower-left dominate the frame.

## Round 8 (director QA-tech): PASS (one spec reading flagged)
Checked 6 fps + g1063, 1070, 1080, 1086, 1090, 1095 at full size (take g1007-1104), frames in /tmp/qa19_r8/s14. Frame-diff g1017-1095: median 5.20 / p90 11.62 OK. No text, black or frozen frames. Mouth: a closed-eye smile / small grin, no mouth movement. Heads centre y ~ 480-600, face ~ 16 % of frame height.
Fixes: palm VERIFIED: the open (dark) hand is raised above the red cloth top edge, pointing over the H4, from g1039 through g1095. Expressions change: neutral smile g1016-1050, bigger smile g1056, closed-eye beam g1061-1075, open eyes grin g1081-1095; nobody is still for more than ~1.2 s. Harrison fully in frame at 36.1-36.5 s (g1083-1095): head right edge ~ 25 px inside, ponytail and sleeve inside, no clip.
FLAG for the director (H1-post / H4 gap >= 15 px at g1063-1095): the gap is NOT a clean clearance: the red cloth and watch sit IN FRONT of the H1 gear box (the box's right post is behind the cloth, overlap ~ 40 px at g1063 and ~ 150 px at g1090-1095). There is no edge tangent or kiss (overlap, not touching), so I call it a pass; if the director meant a literal visible gap, this is not met.
Notes: a dark rear arm with a small hand reads as a shadow arm beside his head g1056-1095; the gear/pendulum clutter is dense and bright left of the watch.
