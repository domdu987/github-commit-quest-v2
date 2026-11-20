# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 16.4 s wall/frame (median 16.5); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 6.83, p90 7.46** (min 2.76, max 8.06), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.48 %, mean luma 83.

## Round 6: bare ground
- The set's vista dressing (J.dress_ground over the whole move: 414 hedges, haystacks, tree clumps, field ridges, huts) fills the ground; no pulses; one eased dolly + truck; sticker clouds gone; caption band clear.
## Deviations
- p90 below the 9 guide (median passes).

