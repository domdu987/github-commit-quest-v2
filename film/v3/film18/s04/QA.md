# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 13.4 s wall/frame (median 14.0); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 11.39, p90 13.81** (min 3.23, max 14.28), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.82 %, mean luma 97.

## Round 6 fixes
- **Ju**: a small walled town with 6 houses, warm lit windows, gate fires and a ground pool, built at (-112,125) as a stand-in for Ju (the real one is lost in the haze), separate from Jimo, visible from the first frame and passed on the way.
- Flame-flag removed (no beacon / flag on Ju any more). Flat navy shadow slabs: shadows of towns, roofs, tents and the Ju stand-in switched off.
- No pulses: one dolly + pan to Jimo with one held +16 % punch-in on "จี๋โม่".
## Deviations
- Ju's roofs read dark navy at phone size; only its windows glow warm.

