# QA s21 = T21 v2 (render20/v2a)
Cut in at g1431 (4 handle frames), dissolve out (8 handle), g1427-1663, 237 frames, timing / events unchanged.
- Camera: the travel (rise along the wire, summit, swoop, group) is the old knot path low-passed with a gaussian (sigma 8 f) plus a 7-frame lead over g1520-1550 so the hand-over to the group lands as before; the 0.07 D ~9 Hz handheld sway on the group is removed. (A C2 spline through the knots overshot into the cobbles; dropped.)
- Contact shadows on the cobbles (see GROUND.md); ground_check PASS.
- g1575 (52.5 s): the camera is still finishing the swoop, the group is in the lower third and arrives fully by ~g1585 (old take: g1575). Slightly later arrival, declared.
- qa_auto PASS, qa_jitter all <= 1.7 (GROUND.md), frame-diff median 12.40 p90 21.12. sheet_1fps.jpg.

## Round 2 (batch hunter items 1-6, all frames re-rendered)
1+2 stray white / light-blue lines: sig_wire hidden, rings are now concentric around the tip (r max 240 m). 3 pale band: sig_aura, sig_halo and the lattice glow sweep off. 4 hard sky edge: horizon haze + 8x ground. 5 arrival: wider framing at g1575 (whole group in frame, officer included), ease-in to the old framing by ~g1635. 6 ghost rods: removed, pickaxes stay in the hands.
qa_auto PASS, ground_check PASS, qa_jitter all <= 1.7. frame-diff median 11.67 p90 18.86.
