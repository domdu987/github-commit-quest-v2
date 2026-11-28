# s27 row 27 GAG tap and tin cup (g 817-837)

## Scope
- g 817-837 (first_g 817, 21 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: DEADPAN: near-hold for the first 9 frames (only the 2 cm eased drift), then a slow PUSH 6 % (4.6 -> 4.3 D, 40 mm) with a 0.15 D slide and a 4 deg arc.
- Render: mean 109 s wall per frame per process (2 processes x 2 threads running at the same time; min 93, max 127).

## light_metrics
```
take.mkv (1 fr)                        luma 0.498 p1 0.098 p99 0.974 lc 0.0585 sat 0.420 chroma 24.8 a +2.0 b +4.1 p98 1.00 blue 0.43 warm 0.49 neut 0.19 M 89  PASS  (guides off: p1,p99,chroma)
```
## qa_jitter
```
overall median jitter px 0.33
```
## Framing numbers (from the per-frame meta)
- highest head top y 329 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1428 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- tommy_b25 holds the tin cup (scale 1.3) under the hull tap: his feet are solved so that the cup rim sits at the spout tip (anchor tin_cup_r vs the tap world point, residual < 25 px); a water bead falls from the spout into the cup every 15 frames; gaze on the tap, blink g 822, then the deadpan stare at us from g 828.\n- Backdrop = the tank hull side, runtime-dressed to one calm riveted teal-steel plate (camo material swapped, stencil off); hull plate 1 D behind him, his shadow lands on it; hatch + tap stay beside his head.\n- Deviations: hull is teal (saturated pure hue) rather than grey-olive because grey gave sat 0.26; the cup rim is about 0.17 D above the spout tip (arm reach limit), the bead falls into the cup. Vibrance 2.05 for this take.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
