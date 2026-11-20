# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 10.8 s wall/frame (median 11.6); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 6.24, p90 7.16** (min 2.44, max 7.67), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.17 %, mean luma 73.

## Re-done for the TAKE gate (camera recipe): no pulses, no wiggles
- One eased DOLLY + TRUCK: the camera flies from (40,-135,70) to (-95,15,70) while the look-at drifts west (tilted down), so towns fill the frame from the first frame (sky is about 33 % and falling, bare ground well under the old 40-50 %). The camera ends in the western towns, where the pennants are densest (and Ju's beacon + Qi flag show at the top).
- Sticker clouds gone (the dusk sky is replaced by its smoothed cloudless gradient); halos hidden, siege tents dimmed, caption band clear; Jimo's Qi flag is opaque cloth.
- Pennants pop one by one over g 223..294 (set_pennants keyed per frame).
## Deviations
- p90 is under the 12 target but above the 'visible dolly' guide; median passes.

