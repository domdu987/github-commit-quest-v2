# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 13.7 s wall/frame (median 14.3); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 5.72, p90 6.46** (min 2.02, max 7.39), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.59 %, mean luma 88.

## Round 7 (vista round 3)
- Set's round-3 farmland, Ju visible on the horizon, no navy slabs; sticker clouds gone (cloudless dusk gradient); Jimo-side halos and glints off; Qi flag opaque.
- No pulses: dolly (set camera + orbit -14 deg/s, tilt); pennants pop one by one over g 223..294.
## Deviations
- p90 6.5 (< 9 guide).

