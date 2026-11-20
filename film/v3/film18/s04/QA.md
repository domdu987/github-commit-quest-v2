# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 8.0 s wall/frame (median 8.1); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 4.87, p90 5.27** (min 3.15, max 5.39), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.16 %, mean luma 97.

> Set version: Vista round 4 (set3d18 from film18/main 0cdc3e8).
## Round 10
- Silk pennants on all towns at 0.4 / 0.55; the near Jimo Qi flag at scale 0.45 (set_pennant_scale), opaque, no bloom; Ju visible as a warm-lit town with a fire basket for the first ~2 s; moat water, warm timber gate; caption band max shown above; no pulses (push 0.14/s + orbit -12).
## Deviations
- The Jimo flag at 0.45 still reaches the top third in the last third of the shot (camera closes on it); p90 5.3 (< 9 guide).

