# s43 row 43

## Scope
- g 1301-1330 (first_g 1301, 30 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: PUSH 12 % (4.7 -> 4.2 D, 40 mm) with a 7 deg arc and a 0.15 D slide.
- Render: mean 65 s wall per frame per process (2 processes x 2 threads running at the same time; min 57, max 71).

## light_metrics
```
take.mkv (1 fr)                        luma 0.499 p1 0.096 p99 0.974 lc 0.0463 sat 0.419 chroma 27.4 a +2.3 b +4.7 p98 0.90 blue 0.48 warm 0.47 neut 0.05 M 82  PASS  (guides off: p1,p99,chroma,blue_frac)
```
## qa_jitter
```
overall median jitter px 1.47
```
## Framing numbers (from the per-frame meta)
- highest head top y 252 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1394 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- general25 in the op_close_general mark (OP roof beams hidden at runtime): field glasses sweep (yaw/pitch/lean swing), g 1314-1317 double-take (lerp_pose glasses->laugh, cap pops up with hat_up25, expression shocked->laughing), then laugh / laugh_b bounce with lerp in-betweens. No lip-sync (quote starts g 1331). Plate wall 2 D behind him (sky above), sandbag parapet at the bottom.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
