# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 7.1 s wall/frame (median 7.1); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 6.30, p90 7.56** (min 2.19, max 9.02), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 61.

## Round 8 (set/cast from film18/main 5da0649)
- General: cast18.general_run_scream_frame (big open screaming mouth, brows raised, sweat drops, drawn fist gripping the jue cup via cup_grip), lean 22, look-back variant (lookback=True) g 2070-2080; cup stays in frame to g 2111.
- Sky: the curved lavender band replaced by a smoothed gradient (everything above v 0.5 eased into one colour); road: warm dawn dirt with verge props, ground_share 0.16-0.18; lead ox chin max 821 (< 860), ox faces use face='rage', the nearest drifts to screen-right so its face shows at his shoulder at the cut; four oxen gaining on him; held +19 % push from g 2068; no pulses.
## Deviations
- p90 7.6 (< 9 guide). The upper sky is now a flat beige-grey (smooth, but dull). No out handle (hard cut at the film end).

