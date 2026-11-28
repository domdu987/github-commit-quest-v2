# s68 rows 68-70 FINAL CALLBACK (g 2009-2092)

## Scope
- g 2009-2092 (first_g 2009, 84 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: Behind-right, low camera (cz 1.45) dollies in from 10.4 to 4.6 D (lens 34 -> 40 mm) past four cheering Tommies, who leave the frame at the sides; the general's head grows from about 140 px to 302 px of the 720 px width (x2.1, an eased calm() curve), the group itself rolls +y at 0.06 D per frame with the tank, so the pan follows at 10-25 % of the width per second. No whip, the take ends exactly on g 2092.
- Render: mean 148 s wall per frame per process (2 processes x 2 threads running at the same time; min 110, max 237).

## light_metrics
```
take.mkv (3 fr)                        luma 0.522 p1 0.103 p99 0.941 lc 0.0540 sat 0.410 chroma 26.9 a +2.1 b +4.8 p98 0.91 blue 0.37 warm 0.54 neut 0.13 M 84  PASS  (guides off: p1,chroma)
```
## qa_jitter
```
overall median jitter px 0.58
```
## Framing numbers (from the per-frame meta)
- highest head top y -2249 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 4744 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Tank rolls up the cobbled high street (pose_on_ground + set_drive every frame, tail wheels turn); tommy_c25 / tommy_a25 / tommy_d25 / tommy_b25 march (cast25.cycle march) with cheer arms, mouths open and varied, the general marches knees-up with the flag (march_flag25, flag wave t), expression excited, then happy with blush and sweat (sheepish) from g 2062.\n- Backdrop = red brick houses and blue sky; the sun is aimed from camera-left, el 42 deg.\n- Deviation: by g 2092 the tank's tail wheel is at the right edge of the frame, the tank rear is mostly out of frame (the general is 'right behind' the tail wheels in the world, GAP 2.4 D). 4 Tommies are in the first 55 % of the take only.\n- No out-handle (g 2092 is the last film frame); no in-handle frames were rendered (see T3_STATUS).
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
