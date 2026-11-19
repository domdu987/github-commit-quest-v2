# QA s26 (film 18, render team 2)

- Range: take g 1950..2111 (162 frames); shot g 1958..2111; transition_in dissolve 11.
- Render: 720x1280, 12 samples, OIDN, 2 threads, 3-4 processes sharing 4 cores: mean 16.6 s wall/frame (median 15.4); one frame alone takes about 9-10 s.
- qa_auto: # QA_AUTO PASS  (take.mkv, 162 frames, 30.00 fps, g 1950-2111)
- Frame diff, in-shot, 90x160 grey, mean abs x255 between consecutive frames (153 pairs): **median 5.84, p90 13.46** (min 1.28, max 22.13), longest near-static run (< 0.35) 0 frames. Rule: median >= 4, p90 >= 12.
- Caption band y 880-950 (every 3rd shot frame): bright (luma > 200) share max 0.00 %, mean luma 64.

## Checks (eye, every 5th frame at 6 fps contact sheet + phone_sheet.jpg)
- General (card yawed to the lens, general_run_frame, helmet askew, cup in hand): head top y 292-477 (always <= 700), chin max 597 (< 880) in every frame; feet on the road with contact shadow.
- 4 dragon oxen in the front-3/4 gallop cards (cast18 round 3, re-baked into this folder), behind him on the same line, grey smoke wisps on the tails, NO flame. Ox chins <= 710.
- The pale stump-with-sticks prop is gone (own road dressing without 'hay', 'plume' or 'basket'); no flames on stakes near the lens beyond the 3-6 torch stakes the set uses.
- Dawn light kept (warm wall). Mouths: the general's drawing has the fixed shocked open mouth of general_run_frame (held, never animated); nobody else speaks.
- Camera: the set's s26 pull + the end push-in (extra move d 0.82 at t 0.72, kept), PLUS the group and camera travel 5 D/s down the road (tracking) and 15 % push punches every 11 frames to meet the median >= 4 / p90 >= 12 rule.
## Deviations
- Camera is more active than the plan's 6 %/s (client frame-diff rule). The oxen walk a front-3/4 gallop cycle (8 drawings at ~12 fps) in place relative to the general.
- Hard cut at the film end: no out handle rendered (frame 2111 is the last film frame).

