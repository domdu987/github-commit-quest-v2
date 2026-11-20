# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 7.4 s wall/frame (median 7.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 5.96, p90 7.27** (min 2.27, max 8.48), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 70.

## Round 9 fixes (set/cast film18/main 5da0649)
1. Cup and fist inside the left edge to the last frame: the general moved 0.25 D to screen-right (x 1.35 + 0.3 sin); the cup shrunk to 62 % of the scream pose's size (scale 0.93).
2. Lead ox: whole head above y 860 for g 2080-2111: max chin measured 757 (camera look-at lowered to z 2.5, which lifts the oxen in frame).
3. Sky: a smooth warm gradient (pink at the horizon -> peach -> pale gold at the top), no arc.
- Kept: scream run with fist-gripped cup, look-back g 2070-2080, rage oxen with the nearest at his shoulder, smoke on the tails, +19 % held push from g 2068.
## Deviations
- p90 7.3 (< 9 guide). Not measured on a pixel basis: the cup's exact margin (visually about 50 px at the last frame).

