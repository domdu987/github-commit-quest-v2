# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 13.4 s wall/frame (median 13.0); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 7.61, p90 10.11** (min 1.44, max 11.83), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 5.44 %, mean luma 74.

## BIGZOOM ending (client rule §H; set film18/main 70c8a11) - measured on rendered pixels
- **§I additions (rim, plaque, action):** warm dawn key as before plus a cool sky-blue rim: a blue emissive copy of every general / ox card 4.5 % larger, 0.07 D behind it (shows as an outline); a sharp gold-on-dark plaque 即墨 (12 x 4.5 D, drawn with a CJK font) over the INNER face of Jimo's gate, readable in the first ~1 s of the extreme wide (about 160 px wide on the 720 frame); the start camera moved to (22,60,62) looking (0,-75,-10) so the gate hall is in frame; the general's helmet wobbles (hat_askew 24 +- 20) and the cup sloshes (cup_tilt +- 88 deg quantised) every few frames; panic look-back g 2070-2080 kept.
- Move: ONE continuous eased crane-down + swing round in front of him, no cut, no pulsing. g 1958: camera (22,60,62) looking (0,-75,-10), lens 34 (extreme wide: gate hall with the plaque, road, fields, Yan camp, dawn sky); cylindrical interpolation about the general to the old end framing at g 2066 (radius 38 -> 4.9 D, azimuth 51 -> -83 deg through screen-right, lens 34 -> 24), look-at released quickly then kept on him; from g 2066 the old tracking pull + the +19 % held push-in from g 2068 ("วิ่งหนีวัว"), identical at the join.
- General height: g 1958 **2.2 %** of frame height (< 5 %), g 2066 **44.8 %** (35-60 %), g 2111 54.0 %. Head top y >= 312 for g >= 2066 (above 860); face is not taller than 35 % of the frame.
- Findable at the wide: a warm dawn pool of light follows him (scaled with distance, keyed per frame), pale road beneath him.
- Frame diff median 7.2, p90 11.3 (rule median >= 4: pass; p90 near 12).
- Plain ground (J.ground_share) at the end: 0.22-0.26 (<= 0.30).
- Ox mouth y (rendered pixel positions of the nearest ox's mouth): max 821 for g >= 2080 (<= 860).
- qa_auto PASS; phone_sheet.jpg is the 360x640 tile sheet. Cup in fist, scream, rage oxen, smoke on tails, helmet prop in the corner (from g 2046) kept.
## Deviations / notes
- The wide frames were soft (qa_auto read blur): g 1950-2061 got an unsharp mask (radius 2, strength ramping 330 % -> 100 %) on the rendered PNGs (raw renders kept in raw_frames/, not committed). The wide fields still look blue-murky (the set's dawn shade from the wall side).
- At g 1958 the oxen are bunched behind him, so the group reads as a small red-and-gold cluster near him. Saturation: the wide's fields are still blue-murky; the director's conform grade handles the global saturation.
- From the high start the oxen cards are the front-3/4 gallop drawings (facing the lens), not seen from behind.
- Dissolve handle: 8 frames before g 1958; no out handle (hard cut at the film end).

