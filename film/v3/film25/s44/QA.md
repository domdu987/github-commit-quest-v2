# s44 row 44

## Scope
- g 1331-1367 (first_g 1331, 37 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: PUNCH 20 % over g 1347-1354 (5.0 -> 4.2 D, 40 mm), slow +4 % push, 6 deg arc.
- Render: mean 65 s wall per frame per process (2 processes x 2 threads running at the same time; min 58, max 73).

## light_metrics
```
take.mkv (1 fr)                        luma 0.499 p1 0.098 p99 0.963 lc 0.0460 sat 0.397 chroma 27.0 a +2.1 b +4.4 p98 0.90 blue 0.40 warm 0.50 neut 0.06 M 79  MISS  (guides off: p1,p99,chroma)
```
## qa_jitter
```
0s shake   5.5px
overall median jitter px 5.8
```
## Framing numbers (from the per-frame meta)
- highest head top y 248 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1447 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- glasses_laugh with lip-sync in his second quote, pointing hand jabs, squash accent g 1347, plate wall + shadow, sky. Vibrance 2.0 (sat gate).
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
