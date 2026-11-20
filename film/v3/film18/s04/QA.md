# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 17.3 s wall/frame (median 17.2); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 11.65, p90 13.86** (min 3.13, max 14.29), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.03 %, mean luma 75.

## TAKE-gate round 2: no pulses; the take continues the s03 camera and makes one eased dolly + pan to Jimo with ONE held +16 % punch-in on "จี๋โม่" (g ~352).
- **Ju is visible and lit** at the start (Qi flag on a beacon tower with a live flame, top left; a stand-in on Ju's spot because the set's own Ju is lost in the haze).
- Flat navy shadow polygons gone (flag shadows off), blue spike cones (trees) hidden, flag is opaque crimson with a dark-gold trim (no pale patch), caption band bright max 0.03 % (limit 1 %).
- ground_share 0.10.
## Deviations
- Delivered as a CUT in (continues the s03 camera, so the director may make it a plain continuation).

