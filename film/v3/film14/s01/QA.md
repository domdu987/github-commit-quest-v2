# s01 v4 QA (render team 6), answers s01v3_QA_RECHECK
- qa_auto PASS (QA_AUTO.md, phone_sheet.jpg). 12 samples, ~45-60 s/frame, 2 procs x 2 threads. Per-frame L1 diff (180x320): median 2.3; cuts g65->66 (56) and g122->123 (53) on plan; g0->g1 3.1 (was 6.9-9.0); hang frames g29-40 about 5-7 (a continuous move, no single spike).
- 1. g0 pop: cause found = both render processes wrote sprites with the same file names in a shared folder (g0 of one process picked up the other process's bigger shot-2 farmer sprite). Fixed with a per-process sprite folder; g0 re-rendered, g0=g1 pose/size.
- 2. Hang: farmer now stands on the ladder rung (z 0.64/y 3.85, soles on the rung); same hive from g0, hands on the bar until it hooks: carry g0-30, travel onto the hanger g30-44 (14 frames), arm relaxes g46-58. Camera pitched down/left so the hung hive lands left-centre, fully in frame (x ~100-460 of 720, y <= ~830), under the roof; bar un-squashes as it hooks; bees follow.
- 3. Shot 3: arm sweep = 3 keyed hand poses over 16 frames (g148-164) then HELD g164-186 with the full arm up toward the peak (card mirrored so the mountain is on his pointing side), camera pans toward it; ground about 25 %; contact shadow under him enlarged; ladder out of the hive's way.
- Shot 2: villagers back to laugh-with-tears expressions (eyes squeezed, open grin); kid chin above y 830; farmer on the rung.
- Weak: farmer's raised arm in shot 3 is more "arm up" than a long point; sky is ~35 % in shot 3 (mountain/acacias fill it); shot 2 villagers are small side groups.

## v5 (shot 3 re-rendered, g123-186; shots 1-2 identical to v4)
- Arm: 3 keyed hand poses (low -> out front -> (1.75,-0.6)), tweened g148-164, then HELD g164-186; the card is mirrored so the peak is on his pointing side and the arm extends out and up diagonally, clear of his head and hat; camera nearly static (look x -5.3 -> -5.4) so he stays well inside the right edge (no drift); hung hive no longer cut by the left edge. Whole shot re-rendered (camera path changed) so there is no cut at g148.
- qa_auto PASS; frame diffs: median 2.3, only cuts g65/g122 and the hang (g29-40) above 2.2 x median.
