# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 8.4 s wall/frame (median 8.1); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 5.70, p90 7.45** (min 3.65, max 7.82), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 89.

## Rework after the TAKE gate: NO pulses. Motion = orbit -19 deg/s about the plain (real parallax), the pennants popping, no zoom in/out.
- Pennants pop one by one (set_pennants 0 -> 1 keyed per frame, g 223..294); Jimo's Qi flag is opaque cloth, no halos at all (no bloom); siege tents dimmed, siege fires hidden: caption band clear.
- Clouds: dusk sky repainted at runtime so the cloud base is a rounded underside, no flat bar.
## Deviations
- p90 below the 12 target (median passes). Out handle only 2 frames (s04 is a cut).

