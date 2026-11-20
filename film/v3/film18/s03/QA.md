# QA s03 (film 18, render team 2)

- Range: take g 147..298 (152 frames); shot g 156..296; transition_in dissolve 15.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 9.3 s wall/frame (median 8.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 152 frames, 30.00 fps, g 147-298)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (140 pairs): **median 5.58, p90 6.30** (min 0.76, max 6.77), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.51 %, mean luma 90.

> Set version: Vista round 4 (set3d18 from film18/main 08dc7e0).
## Round 11
- From g 238 the camera eases UP and BACK (to (-100,-125,190)); the last frames show 25+ small flags over the towns: the pennants pop near-to-far with J.vista_pennant_order / J.set_pennant_scale, the 6 nearest stay down (no diagonal pole in the bottom third / on the edges), near ones k 0.32, middle 0.7, far 1.0.
- Navy ramp / plank / pole-base strips: the town road ribbon's navy (vroad faces within 33 D of Jimo removed, c18.vista_yard_fix) and the yellow-cube lump: the set's haystack props were scaled by the camera; the take no longer passes over that spot closely.
## Deviations
- The vista's far-hill haystack lumps still appear as yellow blobs; the ramp / plank strips in the west towns (set objects) are not individually hidden. p90 below 9 guide.

