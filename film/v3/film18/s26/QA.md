# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 12.7 s wall/frame (median 12.9); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 7.17, p90 11.32** (min 0.93, max 11.90), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.16 %, mean luma 76.

## BIGZOOM ending (client rule §H; set film18/main 70c8a11) - measured on rendered pixels
- Move: ONE continuous eased crane-down + swing round in front of him, no cut, no pulsing. g 1958: camera (40,12,52) looking (0,-100,-22), lens 34 (extreme wide: Yan camp with smoke, road, fields, dawn sky; the wall is only the bottom-right corner); cylindrical interpolation about the general to the old end framing at g 2066 (radius 38 -> 4.9 D, azimuth 51 -> -83 deg through screen-right, lens 34 -> 24), look-at released quickly then kept on him; from g 2066 the old tracking pull + the +19 % held push-in from g 2068 ("วิ่งหนีวัว"), identical at the join.
- General height: g 1958 **3.0 %** of frame height (< 5 %), g 2066 **44.8 %** (35-60 %), g 2111 54.0 %. Head top y >= 312 for g >= 2066 (above 860); face is not taller than 35 % of the frame.
- Findable at the wide: a warm dawn pool of light follows him (scaled with distance, keyed per frame), pale road beneath him.
- Frame diff median 7.2, p90 11.3 (rule median >= 4: pass; p90 near 12).
- Plain ground (J.ground_share) at the end: 0.19-0.24 (<= 0.30).
- Ox mouth y (rendered pixel positions of the nearest ox's mouth): max 821 for g >= 2080 (<= 860).
- qa_auto PASS; phone_sheet.jpg is the 360x640 tile sheet. Cup in fist, scream, rage oxen, smoke on tails, helmet prop in the corner (from g 2046) kept.
## Deviations / notes
- The wide frames were soft (qa_auto read blur): g 1950-2061 got an unsharp mask (radius 2, strength ramping 330 % -> 100 %) on the rendered PNGs (raw renders kept in raw_frames/, not committed). The wide fields still look blue-murky (the set's dawn shade from the wall side).
- Wall + gate are only a corner / the torch line at the very start (the camera looks away from the wall to see the road and the camp); at g 1958 the oxen are bunched behind him, so the group reads as a small red-and-gold cluster near him.
- From the high start the oxen cards are the front-3/4 gallop drawings (facing the lens), not seen from behind.
- take.mkv encoded at crf 11 (not 6): the unsharp-masked wide frames made crf 6 exceed GitHub's 100 MB file limit (114 MB); crf 11 is 71 MB, qa_auto still passes.
- Dissolve handle: 8 frames before g 1958; no out handle (hard cut at the film end).

