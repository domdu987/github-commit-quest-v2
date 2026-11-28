# s26 row 26

## Scope
- g 785-816 (first_g 785, 32 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: PUSH 10 % (4.5 -> 4.1 D at 40 mm) with a 5 deg arc and a 0.2 D slide.
- Render: mean 84 s wall per frame per process (2 processes x 2 threads running at the same time; min 79, max 99).

## light_metrics
```
take.mkv (1 fr)                        luma 0.495 p1 0.097 p99 0.974 lc 0.0547 sat 0.429 chroma 26.7 a +2.2 b +3.9 p98 0.95 blue 0.36 warm 0.45 neut 0.06 M 85  PASS  (guides off: p1,p99,chroma)
```
## qa_jitter
```
overall median jitter px 0.35
```
## Framing numbers (from the per-frame meta)
- highest head top y 340 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1302 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- tommy_c25_ladle_tap: ladle swings back and strikes the hull plate every 8 frames (arm hand + prop angle), squash on each strike, laughing tears loop, blinks. Hull side (camo swapped to one calm teal-steel plate, stencil off) 0.7 D behind him is the backdrop, his shadow on it. The tank's sloped nose track shows top left.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
