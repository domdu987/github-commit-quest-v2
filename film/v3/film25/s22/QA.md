# s22 row 22

## Scope
- g 626-675 (first_g 626, 50 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: Over-the-shoulder PUSH 8 % (3.2 -> 3.0 D, lens 24 mm) with a 0.25 D slide; fixed azimuth 304 deg behind-left of him.
- Render: mean 60 s wall per frame per process (2 processes x 2 threads running at the same time; min 56, max 65).

## light_metrics
```
take.mkv (2 fr)                        luma 0.500 p1 0.104 p99 0.961 lc 0.0389 sat 0.457 chroma 36.1 a +2.1 b +4.5 p98 0.91 blue 0.35 warm 0.34 neut 0.21 M 92  PASS  (guides off: p1,p99,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.36
```
## Framing numbers (from the per-frame meta)
- highest head top y 339 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1258 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- point_stick with lip-sync: looks out at the trench, stick jab on 'สนามเพลาะ' (g 646), turns back to us (g 656-663), expression smug -> smirk, lean sway, blinks. Plate wall 3 D behind him (shadow on it), sky above, mild DOF f/2.2. M framing: boots in the frame bottom (below the caption band). Re-rendered once (first version had no near backdrop).
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
