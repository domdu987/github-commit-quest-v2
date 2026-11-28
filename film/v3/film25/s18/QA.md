# s18 row 18

## Scope
- g 485-521 (first_g 485, 37 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: FOLLOW: the camera pans with the group, leading (about 0.12 D/frame, roughly 24 % of the frame width per second), dolly 13.5 -> 11.5 D at 26 mm.
- Render: mean 43 s wall per frame per process (2 processes x 2 threads running at the same time; min 39, max 57).

## light_metrics
```
take.mkv (1 fr)                        luma 0.513 p1 0.123 p99 0.879 lc 0.0303 sat 0.456 chroma 36.1 a -0.9 b +1.1 p98 0.98 blue 0.41 warm 0.14 neut 0.08 M 80  PASS  (guides off: p1,p99,lc,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.41
```
## Framing numbers (from the per-frame meta)
- highest head top y 584 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 825 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Wide (W): the general (walk cycle, smug, mouth flat) marches in with two staff officers (tommy_a25 / tommy_d25 stand-ins, a step behind) toward the Mark I standing beside the test trench. 70 % scale, 14 samples, no DOF, no backdrop. Graded vibrance 1.8, wb a* -3 b* +4 (green park).\n- Deviation: heads are 0.09-0.10 of the width (W shot), no shading pass (characters small).
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
