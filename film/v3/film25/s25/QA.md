# s25 row 25

## Scope
- g 760-784 (first_g 760, 25 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: Lateral slide (camera x -17 -> -23 with the look point), about 25 % of the width per second, lens 24 mm.
- Render: mean 49 s wall per frame per process (2 processes x 2 threads running at the same time; min 42, max 55).

## light_metrics
```
take.mkv (1 fr)                        luma 0.501 p1 0.111 p99 0.773 lc 0.0441 sat 0.422 chroma 31.9 a -3.1 b +3.9 p98 0.83 blue 0.40 warm 0.21 neut 0.07 M 70  PASS  (guides off: p1,p99,sat_p98,warm_frac)
```
## qa_jitter
```
overall median jitter px 1.03
```
## Framing numbers (from the per-frame meta)
- highest head top y 569 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 922 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Wide (W) camp: six soldiers (tommy_a25 x2 with different pose / size / mirror, tommy_b25, tommy_c25 x2, tommy_d25 as listed in shot.py) laugh / cheer at the Mark I; varied member, pose, scale 0.9-1.05, mirroring. Tents behind. 70 % scale, 14 samples, no DOF / backdrop / shading pass. Graded vibrance 1.4, wb a* -3 b* +4.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
