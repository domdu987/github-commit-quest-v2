# QA — film 15 reveal, takes s25 / s28 / s29 (shots 25-31)
Takes (one script, `s25/shot.py`, `s25/c15.py`): **s25** = shots 25-27, B TENSE, g 1329-1509 (+6 in / +8 out handle, first_g 1323, 195 frames);
**s28** = shot 28 straddle contrast, B EVE, g 1510-1585 (first_g 1502, 92 frames, dissolve in 11); **s29** = shots 29-31, B TENSE -> EVE, g 1586-1803
(first_g 1578, 234 frames, dissolve in 11, out handle 8 for the dissolve into shot 32). Split from the plan's two takes into three because 27 -> 28 -> 29 are
dissolves between TENSE and EVE (one process = one light preset). Final 720x1280, 12 samples, OIDN, no DOF, cast15 emission cards in the set3d15 scene.
Cost about 13.4 s wall per frame (two processes x 2 threads).
## Reveal checks
- Flop part by part: head over g1392 (46.4 s), back g1416 (47.2), legs g1434 (47.8); arch held to g1586; flick g1586-1603, fall, lands on the foam g1626, lies, sits up g1666-1696 (shot 30).
- Arch >= 50 % of the frame width in 26/27/29 (camera 2.0-2.6 m from the bar, orbiting the body); bar against the dark upper stand; head and legs hang below the bar; card 0.3 D in front of the bar; TENSE pool spots dimmed x0.55 so the bar is not blown out.
- Shot 28: rival1 straddle_a -> b, belly down, whole body 1.6 D above the bar. Shot 30: bar does not move; light pops TENSE -> EVE at g1698 (56.6 s). Shot 31: podium (dick_olympic medal, official1, rival2), crowd cheer + stand flashes + flash bulbs from g1773 (59.1 s); coach_stands (jaw drop) in the stands at scale 3.2 (he is ~95 D from the camera).
- No mouths move (no coach quote in 25-31). Heads: Dick/rival head y < 880 in every frame (lying Dick g1626-1651 head y about 620; see work logs `work/log_*.jsonl`). No text, digits or flags on cards.
## Motion (python3 film15/motion_check.py take.mkv --first_g G --cuts ...)
| take | median | p90 | per shot (median / p90) |
|---|---|---|---|
| s25 | 4.2 | 6.0 | 25: 5.0/6.1, 26: 3.9/5.0, 27: 4.7/7.3, out handle: 3.8/4.1 |
| s28 | 4.1 | 6.6 | 28: 4.0/7.4 |
| s29 | 5.3 | 12.1 | 29: 5.2/25.2, 30: 5.4/6.4, 31: 4.2/16.9 |
Median passes in all three; **p90 >= 12 is met only by s29** (s25 6.0, s28 6.6). The hanging flop / straddle are slow by nature (the figure is held in the picture,
the camera orbits 25-50 degrees around it with a quick 0.4 s push-in at the punch beats, FG standards ride the lens); a faster orbit or a whip in 26-28 would lift p90 if the director wants it.
## Known points
- A camera sliding sideways moved almost nothing (distant stands), so 26/27/28/30/31 orbit the figure instead (first versions measured median 1.4-1.9).
- Dissolve handle frames come from this take's own set-up (s25 out = shot 27 look, s28 in/out = shot 28 look, s29 in = shot 29 look, s29 out = shot 31 look).
- Dick pose tween between presets is numeric (legs presets switch at the midpoint); the run uses run_curved (16 frames/cycle) and plant/takeoff presets, x travel 5.6 D in 35 frames.
- Rival2 on the podium is cropped by the right edge in the last frames of shot 31 (orbit + cheer); coach in the stands is small.
