# s67 row 67

## Scope
- g 1961-2008 (first_g 1961, 48 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: FOLLOW: the camera backs away at 0.085 D/frame while the tank closes at 0.11 D/frame, lateral drift 3.2 -> 0.2 D, lens 24 mm (the tank grows from a small shape at the end of the street to filling the middle third).
- Render: mean 46 s wall per frame per process (2 processes x 2 threads running at the same time; min 38, max 55).

## light_metrics
```
take.mkv (2 fr)                        luma 0.608 p1 0.102 p99 0.832 lc 0.0439 sat 0.334 chroma 25.1 a +5.8 b -2.1 p98 0.99 blue 0.47 warm 0.45 neut 0.11 M 72  MISS  (guides off: p1,p99,chroma,blue_frac)
```
## qa_jitter
```
overall median jitter px 0.29
```
## Framing numbers (from the per-frame meta)
- highest head top y 0 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 0 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Wide (W) street shot: the Mark I rolls toward the camera up the cobbled street of Flers (pose_on_ground yaw 270, set_drive every frame), brick houses both sides, blue sky. No DOF, no backdrop, 70 % scale / 14 samples. Graded vibrance 1.8, wb a* +1 b* +4.5.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
