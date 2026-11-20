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
