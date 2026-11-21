# film-13 QA, QA-tech sD1 v4 (team2 8110474)

**Verdict: FAIL** (1 blocking: a one-frame camera hitch at the g603/g604 splice)

Checked: all 101 frames extracted from `take.mkv` (g542-642) at full size, every 5th frame (f6/), 1 fps sheet, background motion per frame (phase correlation on hills/bridge/river and LK flow), frame-difference triads at every splice (g559/560, g592/593, g603/604), face tracking g600-636, QA.md, meta.json, GROUND.md, QA_AUTO.md, plan row D1. Colour and exposure are left to the grade.

## Old blocking items
- Head cut by the RIGHT edge g562-582: still fixed.
- Head cut by the LEFT edge g622-636: **fixed.** The face stays at x >= 209 (hat well inside) through g636; head is centred-left during the laugh, and leaves frame only in the whip g637-642.
- qa_jitter 7.5 px in second 2 (g602-631): **not shake.** Background (hills, bridge) moves smoothly: dx ramps 3.4 -> 14.4 -> 4.5 px/frame (the planned aim ease), dy <= 1.9 px, no oscillation. The +-25 px vertical swing is the head card's 3 Hz laugh bounce (face cy 683-750, period ~10 frames). Planned.

## Blocking
1. **g604: one-frame backward camera jump at the splice (g593-603 kept, g604+ re-rendered).** The background drifts steadily +4.6 px/frame g599-603, then jumps **-6.9 px** at g603->g604 and resumes +3.4/+4.7 (an ~11 px jolt against the move; right pole x 624 -> 620 -> 623, face left edge 443 -> 436 -> 439, i.e. g604-606 repeat the positions of g601-603). It is a visible hitch on the slow look-up, which the client reads as shake.
   Fix: re-render g593-603 with the v4 camera path (aim ease from g604 included), or start the new aim ease at g593 so the path is continuous; check that background dx has no sign flip over g596-608.

## Notes (not blocking)
- g598->g599: the drift starts at full speed (0.3 -> 4.7 px/frame in one frame, no ease-in). Fix it in the same g593-603 re-render (ease in over 4-5 frames).
- Splices g559/560 and g592/593: continuous (no position or colour step). The set is consistent across the take (warm tent, crimson/gold canopy, gold coins, lantern).
- Blur: only the planned whip g637-642. Heads: lowest chin about y 820 (< 880). No black/magenta/frozen frames. Ground PASS.
- Mouth: closed g542-611; open laugh drawing from g612 (no lip-sync), per plan. Eye-line up toward the river g602-611.
- Plan coverage: sign readable g542-~570, counting with pinched coin g592-602, look-up, laugh bounce at g612, whip right g637-642. All present. Sign cropped g570-590 as it leaves frame (transition, OK).
