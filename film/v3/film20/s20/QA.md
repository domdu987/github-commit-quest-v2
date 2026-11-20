# s20 QA (render team 8)
Shot 20 (g 1382-1430, cut in/out; handles g 1378-1381 and 1431-1434). 57 frames. Six Morse taps, spark gap flashes on each.

- s/frame: 11.13 wall (2 procs x 2 threads), 21.62 cpu; 8 spp, 720x1280, no DOF, no text.
- Heads: [173, 192] px wide, centre y [502, 521], lowest bottom y 609 (caption band 880).
- Frame-diff in-shot: median 2.16, p90 18.21 (target 4 / 12: BELOW target except s20 p90; small figures + smooth dusk sky).
- Mouths: all still (no quote in these shots). Checked contact sheet at 16 frames, phone sheet, cut edges via handles.
- Set bug worked around at runtime (c20.fix_antenna_wires): tower20._antenna zips 40 points with linspace(...)[1:] (39 pairs), so the last segment of each wire to the anchor post was never built (wires ended in mid-air). s18/s19 add it. Also wire_glow 0.7 in s19 so wires read against the dusk sky.
- Staging deviations: s18 cast marks moved 2-5 m toward the wagon so five heads fit one frame; s19 camera on the avenue at (-4.4,-218,0.5) m (not the board camera) so Eiffel is in frame; s20 soldier seated on the chair (seat_h 0.5) with the aim between him and the spark gap.
- Known weak: bottom third is empty ground (caption zone); s20 plank grooves faintly stripe on floor/ceiling (no visible shimmer at phone size); hands/key of the soldier mostly hidden behind desk and headphones.

## Take-gate revision
Orbit 12 deg/s + slide -40 px/s; ARC chosen so the spark gap stays in the right third for all six taps (x <= 670 at g 1428). A stronger orbit hit median 4.2 but lost the spark from frame.
- Final numbers: s/frame 11.19 wall, frame-diff median 3.03 p90 17.97.

## Take-gate round 2 (TAKE_B + QA_TEAM §G)
TAKE-B: soldier raised 0.15 m so torso, arm and key prop clear the desk (hand on the key on each tap); duplicate FG headphones + FG post removed; the set's arc/forks/halo spheres replaced by our own jagged arc between the two brass balls (3 variants swapped per frame); aim keeps head and spark gap inside both edges; exposure +0.35 (luma 70 -> 76); plank moire only faintly visible on ceiling, floor mostly out of frame (pitch -0.8).
- qa_stats: take.mkv: 1.9s, shots=1, mean shot 1.90s, median 1.90s, shortest 1.90s, shots<1.5s: 0 |    saturation 0.873, brightness 76.1, in-shot motion median 3.95 p90 15.93 |    shot lengths: 1.9
- Own frame-diff (in-shot): median 3.62 p90 15.89; s/frame 10.64 wall.
