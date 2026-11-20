# s19 QA (render team 8)
Shot 19 (g 1302-1381, cut in/out; handles g 1298-1301 and 1382-1385). 88 frames. Whip-tilt g 1343-1352 (planned pops, qa_auto lists them).

- s/frame: 7.6 wall (2 procs x 2 threads), 14.65 cpu; 8 spp, 720x1280, no DOF, no text.
- Heads: [83, 110] px wide, centre y [592, 724], lowest bottom y 773 (caption band 880).
- Frame-diff in-shot: median 1.52, p90 2.82 (target 4 / 12: BELOW target except s20 p90; small figures + smooth dusk sky).
- Mouths: all still (no quote in these shots). Checked contact sheet at 16 frames, phone sheet, cut edges via handles.
- Set bug worked around at runtime (c20.fix_antenna_wires): tower20._antenna zips 40 points with linspace(...)[1:] (39 pairs), so the last segment of each wire to the anchor post was never built (wires ended in mid-air). s18/s19 add it. Also wire_glow 0.7 in s19 so wires read against the dusk sky.
- Staging deviations: s18 cast marks moved 2-5 m toward the wagon so five heads fit one frame; s19 camera on the avenue at (-4.4,-218,0.5) m (not the board camera) so Eiffel is in frame; s20 soldier seated on the chair (seat_h 0.5) with the aim between him and the spark gap.
- Known weak: bottom third is empty ground (caption zone); s20 plank grooves faintly stripe on floor/ceiling (no visible shimmer at phone size); hands/key of the soldier mostly hidden behind desk and headphones.
