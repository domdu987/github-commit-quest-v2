# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 12.2 s wall/frame (median 14.5); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 6.23, p90 7.34** (min 2.55, max 8.21), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.17 %, mean luma 76.

## TAKE-gate round 2: no pulses; one eased dolly + truck (see s03 history); the blue spike cones (set trees) are hidden, sticker clouds gone (cloudless dusk gradient), flag shadows off, Jimo's Qi flag opaque, halos hidden, caption band clear.
- Camera: flies from (40,-135,70) to (-95,15,70) with the look-at drifting west and tilted down; sky ~33 % and falling; ground_share (J.ground_share tool) 0.01-0.10.
- Pennants pop one by one over g 223..294.
## Deviations
- p90 7.3 < 9 guide (median passes); visible dolly + truck.

