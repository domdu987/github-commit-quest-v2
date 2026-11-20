# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 15.5 s wall/frame (median 15.3); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 4.60, p90 5.65** (min 3.31, max 6.66), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.51 %, mean luma 83.

## TAKE-gate round 2: no whip-wiggles. Camera: the set's slide-right, tilt up 5.6 D, steady push 0.10/s and orbit -13 deg/s.
- The red lance / plank (fgwood.001 of the fg cart), the fg wheel, grey rocks and the dr_* dressing are hidden.
- Envoy 4.2 D tall, in frame to the end (x -2.6, bridge to y -27), banner 1.5x; 9 wall folk (old men, women, a child) on the gate-hall ledge and wall crest; gate crack glow.
- ground_share 0.04.
## Deviations
- The envoy is still partly behind the bridge rail posts in the middle frames (the rail is 1.3 D high; he stands behind it).

