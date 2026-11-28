# s27 row 27

## Scope
- g 817-837 (first_g 817, 21 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: DEADPAN: near-hold for the first 9 frames, then a slow PUSH 6 % (4.6 -> 4.3 D, 40 mm) with a 0.15 D slide and a 4 deg arc.
- Render: mean 89 s wall per frame per process (2 processes x 2 threads running at the same time; min 83, max 93).

## light_metrics
```
take.mkv (1 fr)                        luma 0.469 p1 0.086 p99 0.974 lc 0.0566 sat 0.435 chroma 28.4 a -1.9 b +3.6 p98 1.00 blue 0.28 warm 0.33 neut 0.09 M 84  PASS  (guides off: p1,p99,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.37
```
## Framing numbers (from the per-frame meta)
- highest head top y 329 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1428 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- tommy_b25 holds the tin cup under the hull tap (feet solved so the cup rim meets the spout tip), a water bead falls into the cup every 15 frames, gaze on the tap, blink g 822, deadpan stare at us from g 828. Colour fix: the hull plate is now calm olive (camo swapped to one plain olive riveted plate, stencil off), no cyan; grade vibrance 2.0, sat x1.5, sky-hue clamp. Hull is 1 D behind him with his shadow on it. Re-rendered.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
