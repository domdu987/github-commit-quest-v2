# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 13.2 s wall/frame (median 13.0); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 4.95, p90 6.19** (min 3.13, max 12.16), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 1.08 %, mean luma 75.

## Rework after the TAKE gate: NO pulses. Motion = orbit -14 deg/s about Jimo + steady push 0.12/s + ONE held punch-in (-16 % distance) on "จี๋โม่" (g ~352), held to the end.
- Mandatory (director note): opaque crimson cloth flag at half size, ALL halo cards hidden (no bloom, no blown glow stalk), caption band clear (figure above), siege tents dimmed.
## NOT MET / deviations
- **Ju is NOT visibly lit**: from this camera it is hidden by nearer towns and the horizon haze (a beacon tower with a live flame at Ju was tried and never showed). Needs a set change or a camera that frames Ju.
- Delivered as a CUT in (the s03 camera does not continue into s04). p90 of the frame diff below 12 (median passes).

