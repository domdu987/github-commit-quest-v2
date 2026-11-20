# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 8.0 s wall/frame (median 8.0); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 5.78, p90 6.46** (min 2.07, max 6.63), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.59 %, mean luma 89.

> Set version: Vista round 4 (set3d18 from film18/main 0cdc3e8; silk pennants, water moat, warm timber gate).
## Round 10
- All 51 ordinary towns' Yan pennants pop near-to-far through g 222-296 with J.vista_pennant_order + J.set_pennant_scale (cloth grows from the pole top; cap 0.4 for the nearest 20, 0.55 for the rest, never near the lens); Jimo's Qi flag at 0.45; no cloud base bars (cloudless gradient); no pulses (orbit dolly).
## Deviations
- p90 6.5 (< 9 guide). Few pennants are up before ~g 255 because the near ones pop first (all 51 are up by g 296).

