# QA s16 (render team 5, film 18) round 4 - frames g1205-1308 (+10 / +6 handles: take.mkv g1195-1314, 120 frames), jimo_in NIGHT
Frame-diff in-shot (n=103): median **8.52**, p90 **9.53**. qa_auto PASS.
- First 10 frames (g1195-1209) are no longer frozen: the handle frames now move (the earlier clamp of t at 0 froze them); no framing pop at g1206-1208 (continuous camera, the first hole opens from g1210).
- Camera tilted up (look z 6.6), so bare ground is about 28-30 %; furrows/streaks/tufts hidden (the pale needles). The navy slab at the left is out of frame except a sliver at g1195.
- Breaches open x41 first, one after another, each warm-lit; diggers swing at the wall.

## Round 6: ground dressing
Re-rendered with `J.dress_ground` (density 0.45, keep-clear round the diggers): `J.ground_share` 0.05 / 0.02 / 0.05 / 0.02 at g1215 / 1250 / 1280 / 1300. Frame-diff median 11.28, p90 12.59. qa_auto PASS. The dressing is dense in the foreground (props near the lens); check by eye that none covers a digger (g1285-1300 one pot passes in front of the child).

## FINAL-gate fix B3 (face in the caption band, g1268-1292)
Base = the take that PASSED the TAKE gate (round 4, git blob 39fb2c7f17, commit 24a9b22: shot.py/c18.py/set3d18 restored from that commit and rendered in a worktree), only the girl changed: she is now placed 5.5 D to the left and 3.3 D deeper along the wall and scaled 2.0 -> 1.6, so she stands small between/behind the diggers and her bun tops sit at y <= ~835 on rendered frames g1250-1300 (her face is mostly hidden behind the baskets). Everything else (hole sequence, glow, camera) unchanged; `scene.cycles.transparent_max_bounces = 64` set. Frame-diff g1205-1308: median 8.24, p90 9.55. qa_auto PASS. Note: shot.py/c18.py in this folder are now the round-4 versions (round-6 ground dressing is not part of this take).
