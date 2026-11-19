# QA s12 (film 18, render team 2)

- Range: take g 937..1010 (74 frames); shot g 944..1002; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 14.8 s wall/frame (median 14.5); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 74 frames, 30.00 fps, g 937-1010)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (58 pairs): **median 11.01, p90 16.90** (min 0.86, max 18.81), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 44.

## Checks (every 5th frame at 6 fps + phone_sheet.jpg)
- Gate: set_gate 0 -> 0.15 over g 948..990, keyed per frame; the warm crack glow shows left of the fg wheel (the fg wheel was slid left, out of the gate).
- Envoy (cast18 envoy_walk with the plain banner, then bow with the banner) walks out from the gate over the bridge (y -14 -> -28.5) and bows from g 978; 7 wall-walk folk (old men, women, a child) stand in the crenel gaps at 1.7x scale (the wall is 16 D high and 30+ D from the lens, so they must be oversized to read).
- Heads in frames_log.jsonl: all rows y <= 700 (envoy top ~650, folk 290-400); nobody speaks.
- Camera: the set's low slide-right move plus whip-pan wiggles (pure rotation, every 11 frames); push punches and extra slide were dropped because they drove the lens through the cart.
## Deviations
- The cart wheel still sweeps in at the right edge near the end (the set's own cart on the camera's slide path).

