# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 21.4 s wall/frame (median 22.2); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 4.29, p90 6.73** (min 3.15, max 6.91), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.33 %, mean luma 53.

## Rework after the TAKE gate: NO pulses. Motion = the set's low slide-right + orbit -10 deg/s + steady push 0.05/s (orbit the other way and any stronger push drive the lens through the cart).
- Gate crack glow (set_gate 0 -> 0.15 over g 948..990) left of the fg wheel (slid left); envoy walks out over the bridge with the plain banner and bows (g 978+); 7 wall-walk folk in the crenel gaps at 1.7x scale.
- Heads: envoy top ~650, folk 290-400 (all < 880); nobody speaks.
## Deviations
- p90 below 12 (median passes). The cart wheel still sweeps in at the right edge near the end.

