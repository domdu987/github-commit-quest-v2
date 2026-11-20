# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 9.6 s wall/frame (median 9.5); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 4.67, p90 6.32** (min 1.59, max 7.25), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 56.

## Rework after the TAKE gate (QA-tech + QA-art, ALL_TEAMS rules) - all four director fixes applied
1. NO pulses: the plan's tracking pull + the set's one eased push-in that starts on "วิ่งหนีวัว" (g 2068-2069) and holds to the cut. Motion comes from the tracking speed (10 D/s), the run cycle, the gaining oxen and a smooth lateral weave of the camera (+-1.6 D, 0.4 Hz; the subject stays framed).
2. 4 front-3/4 dragon oxen directly BEHIND him, nose toward him, gaining from 9-16 D back to 2.6-7.8 D by g 2085, grey tail smoke wisps (bolder than before), no flame.
3. Panic run: forward lean 15, pumping arms, helmet askew, cup out to the side on a visible arm clear of the face (smaller cup, splash tilt), one look back over the shoulder g 2070-2080 (yaw 0.3 -> 1.0 -> 0.3), closed grimace mouth (no 'o').
4. Rocks, ring discs, pots, baskets, wheels and the dawn cloud stickers are gone (own road dressing = red silk strips + torch stakes only; the dawn sky texture is replaced by its smoothed cloudless gradient).
## Checks
- General head top y ~230-480 (<= 700), chin < 880 (frames_log.jsonl); caption band clear (no props, no bright pixels).
## Deviations / NOT MET
- p90 of the frame diff is below 12 (median passes): without pulses the shot only reaches the figures above.
- No out handle (hard cut at the film end).

