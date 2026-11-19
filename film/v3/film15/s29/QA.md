# QA — film 15 reveal, takes s25 / s28 / s29 (shots 25-31)
Takes (one script, `s25/shot.py`, `s25/c15.py`): **s25** = shots 25-27, B TENSE, g 1329-1509 (+6 in / +8 out handle, first_g 1323, 195 frames);
**s28** = shot 28 straddle contrast, B EVE, g 1510-1585 (first_g 1502, 92 frames, dissolve in 11); **s29** = shots 29-31, B TENSE -> EVE, g 1586-1803
(first_g 1578, 234 frames, dissolve in 11, out handle 8 for the dissolve into shot 32). Split from the plan's two takes into three because 27 -> 28 -> 29 are
dissolves between TENSE and EVE (one process = one light preset). Final 720x1280, 12 samples, OIDN, no DOF, cast15 emission cards in the set3d15 scene.
Cost about 13.4 s wall per frame (two processes x 2 threads).
## Reveal checks (take 2, after the director review)
- The body now TRAVELS across the bar: the card (parallel to the bar, 0.3 D in front, so the bar never crosses the body) moves along the bar with the pose tween: head and shoulders over g1392 (flop_head, hips still below the bar), back/hips at the apex g1416-1419 (flop_back -> flop), thighs up and shins hanging g1434-1437 (flop, z +0.12 D), then a slow travel with sway between flop / flop_back / flop_flick through shot 27 (g1470-1517); head-and-legs-below arch about 65-85 % of the width. Quick push-in at g1472-1484 (shot 27); camera snaps (15-20 deg in 6 frames) on every beat.
- Shot 25: J-curve run from the left (y 18.4 -> 19.9 D), plant, take-off, back to the bar (flop_rise), card in front of the bar, no bar across the chest. Shot 28: real straddle jump: approach, rise, belly-down FLAT apex about 0.7 D above the bar at g1540-1558 (leg kick a -> b at the pop g1545-1557), then down; raised leg inside the frame. Shot 29: drop keeps the card in front of the bar plane until below it (bar not across his face). Shot 30: looks up at the bar (pitch -0.6, gaze up), light pops TENSE -> EVE at g1698; the bar does not move.
- Shot 31: podium, medal, crowd cheer + more flashes from g1773 (59.1 s); coach_stands is now on the track right of the podium at normal size (about 15 % of the frame height, in a clear gap) with his mouth dropping open from g1774-1782 (jaw drop at about 59.2 s); he is no longer "in the stands" (the stands are 95 D away, he would be 14 px).
- No mouths move (no coach quote in 25-31) other than the jaw drop. Heads y < 880 (see work/log_*.jsonl). No text, digits or flags on cards.
## Motion (python3 film15/motion_check.py take.mkv --first_g G --cuts ...)
| take | median | p90 | per shot (median / p90) |
|---|---|---|---|
| s25 | 5.2 | 8.4 | 25: 5.5/6.4, 26: 3.6/8.9, 27: 6.6/8.8, out handle: 4.7/6.1 |
| s28 | 4.9 | 9.5 | 28: 5.0/9.7 |
| s29 | 6.4 | 12.1 | 29: 6.8/20.7, 30: 6.7/10.0, 31: 3.5/13.1 |
Medians pass everywhere. p90 >= 12 holds only for s29; s25 (8.4) and s28 (9.5) are short. The figures now move all the time; the remaining gap is the slow parts between the camera snaps. More snaps would make the shots jittery; the director can decide.
## Known points
- A camera sliding sideways moved almost nothing (distant stands), so 26/27/28/30/31 orbit the figure instead (first versions measured median 1.4-1.9).
- Dissolve handle frames come from this take's own set-up (s25 out = shot 27 look, s28 in/out = shot 28 look, s29 in = shot 29 look, s29 out = shot 31 look).
- Dick pose tween between presets is numeric (legs presets switch at the midpoint); the run uses run_curved (16 frames/cycle) and plant/takeoff presets, x travel 5.6 D in 35 frames.
- Rival2 on the podium is cropped by the right edge in the last frames of shot 31 (orbit + cheer); coach in the stands is small.
