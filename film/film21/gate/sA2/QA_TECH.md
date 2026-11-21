# film-13 QA, QA-tech: sA2 v3 (team5 92c6c9a), TAKE gate

**Verdict: FAIL** (4 blocking issues).

Inputs: take.mkv (83 frames, g77-159, 720x1280, 30 fps), QA.md, meta.json, GROUND.md, QA_AUTO.md, shot.py, cues.json, sheet1fps.jpg, f6/. All frames extracted full size; A1 g77-83 against A2 g77-83 side by side; consecutive strips g100-127 and g120-126; full-size g104, g150; crops of the bridge (g114, g140). Farneback flow and Laplacian on every frame.

## qa_auto blur flags (g98-108, g122) and qa_jitter 8.1 px (g107-136)
- **Geometry is sharp:** no DOF (`dof.use_dof=False`), edges of rocks, pines and the blue Scots are crisp at full size in g98-108.
- **But the flag is not a false positive in what the viewer sees:** g77-118 the "light shafts" are flat, opaque yellow slabs with smeared edges laid across the crag; in g98-108 they fill a third of the frame and read as motion streaks / smear (client: motion streak only 1-3 frames on whip moves). See blocking 2.
- **g100-118 (the arc over the summit):** fast but continuous. Flow rises 20 -> 60 px/frame at g105 and stays 25-35 px/frame to g118; consecutive frames connect, no random keys, no shake. qa_jitter's 8.1 px is the estimator failing at this flow. Acceptable as camera motion.
- **g119-126 is a real defect**, not blur: see blocking 3.

## Blocking issues
1. **g77-83 (D6 at P_A): content mismatch with A1.** Camera geometry matches A1 exactly, but A1's 5 saltire banners are gone in A2 (`hide_near_banners(W, 32 m)` hides them, and the line is placed with `toward=(-60,-260)` and default scale instead of A1's `toward=(120.0,-300.0), scale=2.2`). Through the dissolve the hook's subject (the banners) fades out and yellow slabs fade in. **Fix:** use A1's exact call `K.scots_wide_line(n=26, banners=5, scale=2.2, toward=(120.0,-300.0))`; do not hide banners before the camera has passed them: key the hide (hide_render) from about g112, or hide only the cloth(s) that block the g125-159 view.
2. **g77-118: flat yellow light-shaft slabs.** Opaque yellow bars with smeared ends across the crag and the Scots line (worst g98-108, they cause the qa_auto blur flag); they also differ from A1 (none) at the D6. This was a fixed item in A1 (v2 QA item 3). **Fix:** `shafts=False` for g77-110, or thin, soft volumetric shafts at low opacity that do not cover the Scots; start them after g90 so the dissolve matches A1.
3. **g119-126: crash dive and dead stop.** In 5 frames the camera drops from a high view of the valley (g120) through rock at near-ground (g121), a half-frame lemon flash (g122), near-black pine trunks a few metres from the lens (g123), to the medium shot (g124-125); then flow falls from 32-37 px/frame (g124-125) to 1.2 px/frame (g126) in one frame. It reads as a stutter plus a jolt. **Fix:** re-time the end of the path (the team's offered 25-frame re-render g98-125 is the right scope): arrive at the medium pose with an ease-out over about 8-10 frames so the speed into g125 matches the push start, keep the camera at least 3 m from trunks and the slope, and keep the Scots line in frame during the last 6 frames of the dive.
4. **g111-159: bridge column continuity.** A2 shows the set's sparse placeholder column (a few riders spaced along the deck, crop g140) where A1 shows the deck and causeways full of crimson/white knight pairs. The bridge is clearly in view behind the Scots at g125-159 while "ทีละสองคน ... ไม่ทำอะไรเลยสักอย่าง" plays. **Fix:** build A1's knight-pair column (same code/positions, walking north at 1.3 m/s from the same start) in A2.

## Non-blocking notes
1. Heads y 540-700 at g125-159, all above 880. Chewer stalk and Wallace's folded arms read at g140-159; no mouths move. GROUND PASS (SUNK warnings are card canvas margins).
2. g141-159: drift is 0.7 px/frame, slow but not frozen. OK.
3. g159: right-hand Scot clipped by the frame edge after the push; move him 0.3 m left.
4. g125-159: the Scots shelf is in deep shadow (ground near black); a warm fill on the shelf would help the conform.
5. g90-105 ("ทีละสองคน"): the bridge is out of frame; acceptable by the plan, noted for the FINAL blind-viewer test.
6. A1's crag-foot confetti mini-crowd is in A2 too (g87-110); if A1 removes it, A2 must too.
