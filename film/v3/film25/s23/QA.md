# s23 row 23 GAG imagined march (g 676-711)

## Scope
- g 676-711 (first_g 676, 36 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: FOLLOW: the camera travels with the pair (V 0.10 D/frame, 3 D/s, about 20-25 % of the width per second on the ground), behind-right of the travel direction, slow push 9.4 -> 8.0 D (lens 32 mm), look point leads.
- Render: mean 73 s wall per frame per process (2 processes x 2 threads running at the same time; min 64, max 104).

## light_metrics
```
take.mkv (1 fr)                        luma 0.497 p1 0.097 p99 0.846 lc 0.0255 sat 0.404 chroma 34.4 a +5.6 b -3.7 p98 0.88 blue 0.36 warm 0.26 neut 0.02 M 78  PASS  (guides off: p1,p99,lc,warm_frac)
```
## qa_jitter
```
overall median jitter px 0.79
```
## Framing numbers (from the per-frame meta)
- highest head top y 560 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1030 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- The Mark I rolls (pose_on_ground + set_drive per frame) with a bum-wiggle: its heading sways +-2.2 deg every 12 frames; the general marches knees-up behind its tail wheels waving the flag (march_flag25, t wave every frame), mouth open cheer, no lip-sync.\n- Plain grey-olive plate wall 5 D left of the tank axis catches the cast shadows (sun from camera-right here, light25 +1). Blue sky above.\n- Deviation: the grade is the 'warm brighter' one only partly: green park scene needed vibrance 2.16 / wb a* -1, b* +5 / gamma 0.9 to reach sat 0.40; the result reads slightly cool (a +5.6, b -3.7 inside the hard gate). Frames are M (head 0.15-0.19 of the width), the tank body is mostly out of frame (wheels and axle show).
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
