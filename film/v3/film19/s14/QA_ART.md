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

## Round 4 (re-render 11:19, after QA_TECH R4 face clip): FIX-FIRST, 6.6

Frames checked (g): 1047, 1062, 1086, 1095 at full size. I also checked crops of the right edge (x 440-720, y 250-750) for every frame from g 1080 to 1104, with a guide at x 700, and an overview of every 6th frame from g 1007 to 1103.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey7/s14/f*.png (frame index = g - 1007), /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey7/s14_right_edge.png, /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey7/s14_overview.png

Change: Harrison's mark is 1.1 D further left. The snap is unchanged (x1.65, shift (0.7, -0.35), peak 2.5). Push 24, slide -35, arc 14.

| Check | Status |
|---|---|
| QA_TECH R4: face cut by the right edge, g 1084-1095 | FIXED. The face disc ends at about x 690 at its widest, and the whole face, brows, eyes and smile are inside at g 1084-1095. Only the grey ponytail and bow touch x ~700-715 at g 1088-1097. That is a tangent, not a clip. In the out-handle (g 1098-1104) his hand reaches the edge, which is acceptable in the handle. |
| Round 3 fix 4: palm toward the H4 | **REGRESSED.** With the new mark, Harrison stands directly behind the H4 and its red cloth (g 1039-1078). His arms and open palm are hidden behind the cloth, so in the wide there is no gesture: only a head over the watch. In the snap (g 1085-1095), his visible hand hangs at his apron on screen right, pointing away from the H4. The "proud palm presents the H4" beat is gone. |
| Round 3 fix 1: two-object reveal | HOLDS. The H1 frame, wheels and balls fill the left ~40 %, and the H4 on its cloth is at centre. |
| New overlaps in the snap | The red cloth's top corner now sits on his chin and mouth corner (g 1085-1095). The H1 front upright no longer only touches the H4's crown: it now cuts into the dial's top-left (x ~250-300, y ~540-590), so the two clocks merge at the key word. |

Composition 6.5, Acting 5.5, Key moment 6.5. **Overall 6.6. FIX-FIRST.**

Fixes (shot.py):
1. Undo most of the mark move: keep Harrison about 0.4-0.5 D left of the round-3 mark, not 1.1 D, so that he stands right of the cloth, not behind it. Then get the face margin from the camera, as QA_TECH asked: SNAPSX 0.70 -> about 0.60, or slide -35 -> about -25, during g 1071-1095. Target: face right edge <= 690 and ponytail <= 705 through g 1095.
2. The palm must again be visible in the wide (g 1039-1070), reaching left over the cloth toward the H4 (hand x 0.95, stretch 1.25, layer front if needed), and must still read after the snap.
3. Check that at g 1085-1095 the H1 upright clears the H4 dial (a gap of >= 15 px), and that the cloth corner is below his chin.
Keep the frame-diff gain (median 4.43). It must not drop below 4 after these changes.

## Round 7 (director QA-art): FIX, 6.8

Take checked: take.mkv 13:25 (round-5 render: mark 0.3 D left, snap x1.65, SNAPSX 0.6, handheld sway). Frames: 3 fps plus every frame g 1071-1098, at full size and 360x640. Crops of the palm area (g 1039-1079) and the right edge (g 1083-1098).
Frames: /tmp/qa19_r7art/s14/all_NNN.png (NNN = g - 1007 + 1), f3_*.png; sheets /tmp/qa19_r7art/s14_key.jpg, s14_edge.jpg, s14_palm_crops.jpg, s14_rightedge_crops.jpg, s14_phone.jpg

| Check | Status |
|---|---|
| Right edge, 36.1-36.5 s (g 1083-1095) | OK. The face disc ends at x ~685 or less. The grey ponytail reaches x ~710-715 at g 1093-1098: a tangent, not a clip. The whole face, both eyes and the smile are inside. Not cut in half. |
| Size contrast on a phone | Reads in the wide (g 1016-1078): the H1 is about 180 px wide at 360 px and the H4 is about 50 px, roughly 1:4. After the snap the H1 is cropped to its left part and one post, so the H4 dial is the largest object. The "tiny next to giant" idea depends on the 2 s of wide before it. That works in the cut, but it is not instant. |
| Palm toward the H4, wide (g 1039-1078) | **NOT VISIBLE.** The red cloth is propped upright and covers his near arm. His far arm hangs at his apron. For about 2 s there is a smiling head over a watch, with no gesture. The palm only reads from g 1083, inside the snap. Round 5's "palm reaches across" is true only for the snap frames. |
| Palm, snap (g 1083-1095) | OK. His open hand points left at the H4, about 100 px right of the dial, and reads at 360x640. |
| H1 post vs H4 dial | **NOT FIXED** (the round-4 ask was a gap of 15 px or more). From g 1063 to g 1095 the gold H1 corner post comes down onto the H4's crown and the dial's top-left (x ~150-185, y ~540-600 at g 1088). The two clocks merge at the key word. |
| Cloth vs chin | OK. The cloth is below his chin in the snap. |
| Snap | It is there, but soft: x1.65 over 20 f with a smooth ease. It reads as a fast push, not a snap. Acceptable. |
| Characters act | Weak. The same eyes-closed smile and pose run from g 1016 to g 1080 (2.1 s), with only the handheld sway. That breaks §I.5 (still for no more than 1.5 s). |
| Grounding / floating | OK. No pole through a face. Harrison stands behind the bench, so his feet are hidden. |
| Lower frame in the snap | y ~800-1280 is bench front and floor in warm blur. It is the caption zone, so it is acceptable, but it is 40 % of the image with nothing in it. |

| Criterion | Score |
|---|---|
| Set | 8.5 |
| Light & colour | 7.5 (sunlit shaft, candle, red cloth against brass; warm-only, no cool accent) |
| Composition / phone | 6.5 |
| Acting | 5.5 |
| Key moment (reveal) | 6.5 |
| Match to refs (R4/R5) | 7 |
| **Overall** | **6.8 - FIX** |

The reveal is close. Two concrete problems block it: the proud gesture is hidden for the whole wide, and the H1 and H4 merge at "เท่าจานรอง".

Fixes (shot.py / set, small; keep the mark, snap and drift as they are):
1. **Palm in the wide.** Lay the red cloth flat, or tilt it back to 15 degrees or less, so it no longer stands up like an envelope. Or put the palm arm on a layer in front of the cloth. From g 1039 the open palm must be over the bench just right of the H4, visible at 360x640. Add a presenting beat: the palm sweeps out over g 1039-1050, settles, then makes a small "ta-da" bounce on the snap (g 1079-1085).
2. **Acting in the wide.** Change the expression at least once: eyes to the H4 (looking down) over g 1016-1045, then a proud smile to the lens from about g 1060. Add a small chest-puff or a 2-3 % squash bounce so he is not frozen for 2 s.
3. **Separate the H1 post from the H4.** Move the H1 0.12-0.15 D to the left (away from the H4), or move the H4 and cloth 0.1 D forward toward the lens. Do not move Harrison or SNAPSX. Target: a gap of 15 px or more between the post and the dial's rim over g 1079-1095. Recheck that the ponytail stays at x 715 or less.
4. Optional, for "instant" size contrast after the snap: tilt the snap 0.1-0.15 D up so the H1's full top bar and both balls stay above the H4. The giant clock then towers over the small watch in the held frame, instead of only one cropped post.
Keep frame-diff median at 4 or more.
