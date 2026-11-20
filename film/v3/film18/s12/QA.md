# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 10.8 s wall/frame (median 10.7); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 2.66, p90 3.04** (min 1.60, max 5.57), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 2.37 %, mean luma 83.

## Round 7
- Spiky blade clumps (set 'tufts'), the red lance (fg cart) and the cloud stickers are hidden; folk on the balcony 2.4x, in frame to the end; the envoy (4.2 D) stays in frame (x -4.4, orbit reduced to -5 deg/s) to the last frame.
## Deviations
- The envoy is partly behind the bridge rail in the middle frames; p90 below the 9 guide.

