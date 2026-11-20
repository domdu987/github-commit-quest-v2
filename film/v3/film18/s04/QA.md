# QA s04 (film 18, render team 2)

- Range: take g 295..391 (97 frames); shot g 297..383; transition_in cut 0.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 14.2 s wall/frame (median 14.6); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 97 frames, 30.00 fps, g 295-391)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (86 pairs): **median 4.74, p90 5.07** (min 3.09, max 5.24), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.01 %, mean luma 97.

## Round 7 (vista round 3)
- Uses the set's vista round 3 (farmland, no navy slabs, Ju second warm-lit town on the horizon with a fire basket, smooth siege tents). My own Ju stand-in and the shadow hacks are removed.
- Ju is visible top-left (fire basket + warm glow) in the first ~1.5 s, then the camera moves on to Jimo; it reads at phone size as a glow, its walls are small. Caption band bright max 0.01 %. Jimo's flag is opaque, half size, no bloom (Jimo-side halo cards removed, glints off).
- No pulses: set camera + push 0.14/s + orbit -12 deg/s.
## Deviations
- p90 5.1 (< 9 guide), no held punch this time (the push-in is steady).

