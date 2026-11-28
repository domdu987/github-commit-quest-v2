# s66 row 66

## Scope
- g 1932-1960 (first_g 1932, 29 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: Slow descending tilt + PUSH 8 %: camera (5,-8,34) -> (4.2,-3,27) with lens 28 -> 30.2 mm; the look point rises 1 -> 2.5 D.
- Render: mean 46 s wall per frame per process (2 processes x 2 threads running at the same time; min 43, max 52).

## light_metrics
```
take.mkv (1 fr)                        luma 0.480 p1 0.122 p99 0.852 lc 0.0481 sat 0.473 chroma 33.8 a +5.0 b -0.2 p98 1.00 blue 0.50 warm 0.30 neut 0.04 M 98  PASS  (guides off: p1,p99,blue_frac,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.17
```
## Framing numbers (from the per-frame meta)
- highest head top y 0 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 0 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Wide (W): no DOF, no backdrop, no characters; render at 70 % scale with 14 adaptive samples (small detail only). The tank rolls up the high street (pose_on_ground + set_drive every frame). Brick houses = red, sky blue.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
