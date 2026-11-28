# s67 row 67

## Scope
- g 1961-2008 (first_g 1961, 48 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: FOLLOW: the camera backs away at 0.06 D/frame while the tank closes at 0.11 D/frame, a lateral drift 3.2 -> 0.2 D, lens 24 mm; the tank grows from about a sixth to a third of the width and slides slightly left.
- Render: mean 40 s wall per frame per process (2 processes x 2 threads running at the same time; min 34, max 50).

## light_metrics
```
take.mkv (2 fr)                        luma 0.482 p1 0.056 p99 0.686 lc 0.0374 sat 0.411 chroma 23.5 a +1.7 b +1.3 p98 1.00 blue 0.43 warm 0.50 neut 0.07 M 69  PASS  (guides off: p99,lc,chroma)
```
## qa_jitter
```
overall median jitter px 0.29
```
## Framing numbers (from the per-frame meta)
- highest head top y 0 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 0 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Wide (W) street shot: the Mark I rolls toward the camera up the cobbled street of Flers (pose_on_ground yaw 270, set_drive every frame), brick houses both sides, church tower, blue sky. No DOF, no backdrop, 70 % scale / 14 samples. Graded vibrance 2.4, wb a* -1 b* +5, gamma 0.9 (the bright washed sky needed it; contrast guide lc stays low, 0.037). First attempt had the tank out of sight; re-rendered.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
