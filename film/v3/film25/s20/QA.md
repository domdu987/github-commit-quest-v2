# s20 row 20

## Scope
- g 552-601 (first_g 552, 50 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: eased PUSH 10 % (4.5 -> 4.1 D at 40 mm) with a 6 deg arc and a 0.2 D slide.
- Render: mean 77 s wall per frame per process (2 processes x 2 threads running at the same time; min 62, max 95).

## light_metrics
```
take.mkv (2 fr)                        luma 0.497 p1 0.095 p99 0.973 lc 0.0484 sat 0.454 chroma 33.2 a +2.3 b +4.7 p98 0.90 blue 0.34 warm 0.50 neut 0.16 M 96  PASS  (guides off: p1,p99)
```
## qa_jitter
```
overall median jitter px 0.58
```
## Framing numbers (from the per-frame meta)
- highest head top y 212 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1395 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- point_stick with lip-sync in his quote: head to the tank + stick jab on the first noun (g 558), turns to us scoffing at g 574 (expr smug -> smirk), stick wag, squash accent g 594, blinks. Narrow plate wall (9 D) behind; shadow on it; sky above.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
