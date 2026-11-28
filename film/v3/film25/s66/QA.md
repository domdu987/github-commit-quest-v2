# s66 row 66

## Scope
- g 1932-1960 (first_g 1932, 29 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: Slow descending tilt + PUSH 8 %: camera (5,-8,34) -> (4.2,-3,27), lens 28 -> 30.2 mm.
- Render: mean 49 s wall per frame per process (2 processes x 2 threads running at the same time; min 42, max 67).

## light_metrics
```
take.mkv (1 fr)                        luma 0.486 p1 0.139 p99 0.834 lc 0.0466 sat 0.460 chroma 30.2 a -3.2 b +3.5 p98 1.00 blue 0.50 warm 0.28 neut 0.02 M 95  PASS  (guides off: p1,p99,blue_frac,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.16
```
## Framing numbers (from the per-frame meta)
- highest head top y 0 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 0 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Wide (W), no DOF/backdrop/characters, 70 % scale, 14 samples. Colour-bug fix: the tail A-frame and wheels (blue-grey in the set) are re-materialled dark olive at runtime; grade now vibrance 1.8, wb a* -3 b* +3.5, sat x1.1, gamma 0.95, sky-hue clamp: roofs read brick red, tank olive. Re-rendered.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
