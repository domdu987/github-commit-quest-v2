# s19 row 19 belly laugh (g 522-551)

## Scope
- g 522-551 (first_g 522, 30 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: PUNCH 20 % over g 522-529 (camera 5.0 -> 4.2 D at 40 mm), then a slow +4 % push with a 0.35 D slide; head width 279 -> 337 px.
- Render: mean 68 s wall per frame per process (2 processes x 2 threads running at the same time; min 60, max 96).

## light_metrics
```
take.mkv (1 fr)                        luma 0.500 p1 0.095 p99 0.972 lc 0.0461 sat 0.407 chroma 27.6 a +2.3 b +4.8 p98 0.90 blue 0.36 warm 0.54 neut 0.23 M 83  PASS  (guides off: p1,p99,chroma)
```
## qa_jitter
```
overall median jitter px 26.49
```
## Framing numbers (from the per-frame meta)
- highest head top y 249 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1453 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- laugh / laugh_b every 3-4 frames with a lerp_pose in-between on each swap, head roll, lean, tears loop, winds down to a smug pitch from g 545. Plate wall 2 D behind, sky above, mild DOF f/2. Mouth = the laughing expression (no lip-sync before g 552).\n- Tight crop (head 0.39-0.47 of the width), boots at the frame bottom.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
