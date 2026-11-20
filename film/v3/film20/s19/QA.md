# s19 QA (render team 8)
Shot 19 (g 1302-1381, cut in/out; handles g 1298-1301 and 1382-1385). 88 frames. Whip-tilt g 1343-1352 (planned pops, qa_auto lists them).

- s/frame: 7.6 wall (2 procs x 2 threads), 14.65 cpu; 8 spp, 720x1280, no DOF, no text.
- Heads: [83, 110] px wide, centre y [592, 724], lowest bottom y 773 (caption band 880).
- Frame-diff in-shot: median 1.52, p90 2.82 (target 4 / 12: BELOW target except s20 p90; small figures + smooth dusk sky).
- Mouths: all still (no quote in these shots). Checked contact sheet at 16 frames, phone sheet, cut edges via handles.
- Set bug worked around at runtime (c20.fix_antenna_wires): tower20._antenna zips 40 points with linspace(...)[1:] (39 pairs), so the last segment of each wire to the anchor post was never built (wires ended in mid-air). s18/s19 add it. Also wire_glow 0.7 in s19 so wires read against the dusk sky.
- Staging deviations: s18 cast marks moved 2-5 m toward the wagon so five heads fit one frame; s19 camera on the avenue at (-4.4,-218,0.5) m (not the board camera) so Eiffel is in frame; s20 soldier seated on the chair (seat_h 0.5) with the aim between him and the spark gap.
- Known weak: bottom third is empty ground (caption zone); s20 plank grooves faintly stripe on floor/ceiling (no visible shimmer at phone size); hands/key of the soldier mostly hidden behind desk and headphones.

## Take-gate revision
RE-BLOCKED per TAKE_ART F1-F4: Eiffel's pointing arm is a big foreground silhouette (head 160 px, fully in frame) with the spire + wires above; pitch 28-30 deg, whip g 1343-1352 from pitch 30 to 0 with animated lens shift 0 -> 0.15 (about 48 deg of apparent tilt, yaw follows the wire, peak 1.9); Eiffel leaves frame in the whip and is parked out at g 1349 (fully out afterwards); then push on the hut at ~1.6 m/s. Ground after the whip is ~35 %, not 20 % (the hut base would otherwise fall into the caption zone). Spire top is at y ~250 at the start (not the top edge): head band and summit cannot both fit tighter. Ground desaturation not done.
- Final numbers: s/frame 6.54 wall, frame-diff median 3.04 p90 3.75.

## Take-gate round 2 (TAKE_B + QA_TEAM §G)
TAKE-B: arm now extended up-right at the summit (reads as a point), warm ground + shadows, Eiffel fully in until the whip and parked out after. Wire ends at the post (top 6.2 m) with its lead-in to the hut; the ground end of the wire is the post's guy ropes, not shown separately.
- qa_stats: take.mkv: 2.9s, shots=3, mean shot 0.98s, median 1.20s, shortest 0.13s, shots<1.5s: 2 |    saturation 0.606, brightness 101.2, in-shot motion median 2.66 p90 2.93 |    shot lengths: 1.6 0.1 1.2
- Own frame-diff (in-shot): median 2.33 p90 3.94; s/frame 6.82 wall.
