# s24 row 24

## Scope
- g 712-759 (first_g 712, 48 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: PUSH 12 % with an 8 deg arc (4.7 -> 4.2 D at 40 mm, +0.15 D slide).
- Render: mean 71 s wall per frame per process (2 processes x 2 threads running at the same time; min 66, max 83).

## light_metrics
```
take.mkv (2 fr)                        luma 0.490 p1 0.093 p99 0.974 lc 0.0553 sat 0.465 chroma 33.2 a +2.5 b +4.9 p98 0.90 blue 0.31 warm 0.52 neut 0.10 M 91  PASS  (guides off: p1,p99)
```
## qa_jitter
```
overall median jitter px 0.84
```
## Framing numbers (from the per-frame meta)
- highest head top y 256 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1407 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- general25_finger_wag with lip-sync (his quote to g 760), finger wag every 7 frames, squash accent g 728, blinks. Two staff officers (tommy_a25 mirrored and tommy_d25, stand-in staff: cast25 has no staff members) snigger behind him in laugh_point with a shaking squash / head roll. Plate wall 3.2 D behind.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
