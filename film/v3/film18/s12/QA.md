# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 18.1 s wall/frame (median 19.8); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 3.90, p90 4.85** (min 2.84, max 5.13), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.70 %, mean luma 76.

## Re-done for the TAKE gate: no pulses, no wiggles
- Camera: the set's slide-right + tilt up 5.6 D (less bare ground, the wall fills the frame) + steady push 0.05/s + orbit -10 deg/s.
- Envoy 1.5x larger (4.4 D) walking out left of the bridge (x -2.6, clear of the cart wheel at the right), banner 1.5x; he bows at g 978+.
- Folk: 9 figures (old men, women, a child) at 2.1x on the gate-hall ledge and wall crest, clearly visible; gate crack glow (set_gate 0 -> 0.15) left of the fg wheel.
- Caption band max 0.67 % bright.
## Deviations
- Bare ground is ~30 % at the bottom (water of the moat + dark bank); p90 is under 12 (median is just under 4: see numbers above).

