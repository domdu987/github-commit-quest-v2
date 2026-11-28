# s22 row 22

## Scope
- g 626-675 (first_g 626, 50 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: Over-the-shoulder PUSH 8 % (3.9 -> 3.6 D, lens 24 mm) with a 0.25 D slide; the camera is fixed at azimuth 304 deg behind-left of him, look point on the trench.
- Render: mean 82 s wall per frame per process (2 processes x 2 threads running at the same time; min 67, max 109).

## light_metrics
```
take.mkv (2 fr)                        luma 0.498 p1 0.108 p99 0.948 lc 0.0347 sat 0.504 chroma 40.7 a +2.5 b +3.8 p98 0.95 blue 0.30 warm 0.23 neut 0.03 M 88  MISS  (guides off: p1,lc,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.3
```
## Framing numbers (from the per-frame meta)
- highest head top y 450 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1195 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- point_stick with lip-sync: looks out at the trench, stick jab on 'สนามเพลาะ' (g 646), turns back to us (g 656-663), expression smug -> smirk, lean sway, blinks. The tank hull (camo swapped to the calm teal-steel plate, stencil off) is the near backdrop, mild DOF f/2.2.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
