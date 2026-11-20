# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 10.9 s wall/frame (median 11.2); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 5.26, p90 5.86** (min 4.63, max 5.99), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.22 %, mean luma 94.

> Set version: Vista round 4 (set3d18 from film18/main 08dc7e0).
## Round 11
- Jimo's red Qi flag (k 0.4) stays fully in frame to g 391 (push 0.06/s + orbit -24 deg/s keeps it in the upper half); the navy plank in Jimo's yard was the town road ribbon (vroad) that starts at Jimo's centre: found by hiding objects one at a time (towns and the road ribbon explain the navy), faces of vroad within 33 D of Jimo are removed (c18.vista_yard_fix).
- Ju visible (fire basket) at the start; caption band max 0.22 %. No pulses.
## Deviations
- p90 5.9 (< 9 guide).

