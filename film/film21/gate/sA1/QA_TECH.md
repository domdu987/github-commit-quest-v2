# film-13 QA, QA-tech: sA1 v3 (team1 3cfad63), TAKE gate

**Verdict: PASS** (no blocking issue in the take; the D6 defect at P_A belongs to A2, see gate/sA2/QA_TECH.md).

Inputs: take.mkv (84 frames, g0-83, 720x1280, 30 fps), QA.md, meta.json, GROUND.md, QA_AUTO.md, sheet1fps.jpg, phone_sheet.jpg, f6/. All 84 frames extracted full size; full-size views of g0, g40, g80; 3x crops of the crag (g0, g80) and the bridge (g0); 360x640 downscales of g0 and g30. Optical flow and Laplacian on every frame. Shot plan rows A, A split, P_HOOK, P_A.

## Old items
| old item | status |
|---|---|
| Scots not findable at g0-40 (shadow, confetti colours) | FIXED. 26 blue/white Scots and 5 saltire banners stand on the lit grey middle of the crag face, not in the crag shadow. At 360x640 g0 they are a small blue-white bar with white X glints, under 5 % of frame height as planned; clear from g30 on. |
| Knights two by two | FIXED. Crimson/white pairs fill the whole deck and both causeways; at g0 (3x crop) a clean double red-white column, on the phone sheet a dotted double line from about g15. |
| Flat yellow light-shaft slabs | Still absent in A1. |

## Checks
- **Camera:** one continuous eased move, P_HOOK at g0 to P_A at g80 (probed), handles g81-83 continue it. Flow 3.0 px/frame at g0, peak 4.9 at g33-39, 3.3 at g70, 4.4-5.4 at g81-83: smooth, no spike, no shake. rhythm median 9.57 / p90 11.88.
- **Sharpness:** Laplacian 596-700 (g0-50) falling to 290-300 (g60-83) as the frame fills with smooth crag rock and river; no DOF, no streaks. qa_auto PASS.
- **Frozen / black / magenta / pops:** none (0 % still, magenta 0 %, cuts_detected 0).
- **Caption band / cast cards:** no cards. The Scots line is at y 480-510 (g0) and y 520-600 (g80), above 880.
- **Ground:** GROUND.md PASS (54 horse support points, FAIL 0). No floating seen in the crops.
- **Continuity into A2 (g77-83 overlap):** camera geometry matches A2 frame for frame (crag, river and trees line up at g77, g80, g83). Content does not: see A2 blocking items 1-2.
- **Mouths / Thai text:** none in shot.

## Blocking issues
None.

## Non-blocking notes
1. **meta.json `world` string is stale.** It says `scots_wide_line(toward=(-60,-260))`; the real call (QA.md, meta `scots_wide_line_call`) is `toward=(120.0,-300.0), scale=2.2`. Team 5 copied the stale value. Fix the string so the next re-render of A2 uses the right call.
2. **g40-83, crag foot:** a second, old crowd of tiny multicoloured figures (orange, yellow, red, green, with small saltire flags) still stands on the lower slope below the new blue line (3x crop g80, x 150-500, y 650-760). At phone size it reads as speckle, not soldiers, but it is the old "confetti" look and A2 inherits it. Remove it or recolour it blue/white.
3. **g0-50:** pier wakes are still long straight white spikes beside the bridge.
