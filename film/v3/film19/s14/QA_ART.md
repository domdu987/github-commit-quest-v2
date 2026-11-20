# QA-art, TAKE gate: s14 (REVEAL IMAGE, WORKSHOP shop_clock DAY): FIX-FIRST, 6.5

Frames checked (take index): 12, 35, 55, 72, 80, 90 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s14_*.png

| Criterion | Score |
|---|---|
| Set density / ornament | 9 |
| Lighting & colour | 7 |
| Composition / phone legibility | 5 |
| Acting (proud palm) | 6 |
| Key moment (H4 "the size of a saucer" beside the H1) | 5 |
| Match to refs / client taste | 7 |
| **Overall** | **6.5** |

## What works
- The wide (f 0-60) is the best image in the film so far. The brass H1 is big at left, the white-dial H4 sits on red cloth beside it, Harrison is behind them, and the shop is dense and lit. At 360x640 the H1 vs H4 size contrast reads at once. No text, heads at y 507-583.

## Why FIX-FIRST
1. **The snap throws away the comparison on the key word.** From g 1085 on, "เท่าจานรอง" lands on an H4 close-up. The H1 is reduced to a corner of frame plus two balls, so the image says "a clock", not "small next to the giant". The reveal has to stay a two-object image.
2. **Lower 40-45 % of every snap and hold frame is dead.** From take index 80 to 97 the bench front and the space under it fill y 750-1280 as a washed-out, hazy orange blur. The camera sits low (z 2.5) and the snap's 2x zoom points it at the bench apron. In the wide, the lower third is floor, shavings and stool, which is acceptable but busy.
3. Harrison is small (100-130 px) during the palm gesture, and the open palm is about 25 px at phone size, so the "proud" beat only lands after the snap.

## Fixes (shot.py)
1. Snap: SNAPK 2.0 to about 1.45, SNAPSX 1.3 to about 0.7, and give the shift a downward tilt (shift=(0.7, -0.35)). At g 1085-1095 the full H4 and cloth must sit right of centre, the H1 frame and gears must fill the left 40 %, and Harrison's face and palm must be in frame. SNAPPEAK 2.8 to 2.0.
2. Camera height: CAM_LOC0 z from 2.5 to about 2.9 and CAM_LOOK0 z from 2.2 to about 1.9, so the camera looks slightly down onto the bench top. The bench top and the cloth then fill y 750-1000 instead of the apron. Add RISE=10 so the camera keeps climbing over the bench during the push.
3. Keep PUSH 0.15, SLIDE -30, ARC 10. The frame-diff loss from the smaller snap can be made up with arc 14.
4. Harrison: make the palm bigger in the wide. Push the palm hand out to x 0.95 with stretch 1.25 for g 1039-1070, so his hand points at the H4 across the cloth.

## Round 3 (re-render 09:17): PASS, 7.4

Frames checked (take index / g): 12/1019, 40/1047, 62/1069, 72/1079, 80/1087, 90/1097 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey3/s14_*.png

| Earlier fix | Status |
|---|---|
| 1. Smaller snap that keeps the H1 beside the H4 | FIXED (mostly). Snap x1.65, shift (0.65, -0.35). At g 1085-1097 the H1 frame, wheel and both balls fill the left ~35 %, the H4 on its cloth sits left of centre, Harrison and his palm are in frame. It is a two-object image now. The H4 is still drawn about as big as the visible part of the H1, so the "tiny" reading relies on the wide before it. That works in the cut. |
| 2. Camera higher, lower frame not a dead apron blur | PARTLY FIXED. The wide (g 1016-1078) is good: bench top, cloth, floor, shavings. In the snap, y 780-1280 is still bench front, under-bench glow and floor. It is no longer a washed haze: it has wood grain, warm light patches and shavings. That band is the caption zone, so it is acceptable. Not a blocker. |
| 3. Keep push / slide / arc | FIXED (push 0.20, slide -10, rise 25, arc 8). |
| 4. Bigger palm toward the H4 | FIXED. From g 1047 the arm reaches across to the H4 and reads at 360x640. It reads clearly after the snap. |

| Criterion | Score |
|---|---|
| Set density / ornament | 9 |
| Lighting & colour | 7.5 |
| Composition / phone legibility | 7 |
| Acting (proud palm) | 7 |
| Key moment | 7 |
| Match to refs / client taste | 7.5 |
| **Overall** | **7.4** |

Notes (not blockers): the H1 frame upright ends exactly on the H4's crown at g 1087-1097, a tangent. Nudging SNAPSX by about +0.05 would separate them. Frame-diff median 3.43 is a TECH matter.
