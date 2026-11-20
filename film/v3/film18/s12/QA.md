# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 12.1 s wall/frame (median 11.8); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 4.12, p90 4.99** (min 2.33, max 8.23), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 5.40 %, mean luma 89.

## Round 7
- Spiky blade clumps ('tufts'), red lance (fg cart), cloud stickers hidden. Folk 2.4x on the balcony, envoy (4.2 D) kept in frame to the end (x -7.4; orbit -10, push 0.10/s) and large; banner clipped at the right edge in the last frames.
## Deviations
- p90 5.0 (< 9 guide); the envoy is partly behind the rail posts mid-shot.

