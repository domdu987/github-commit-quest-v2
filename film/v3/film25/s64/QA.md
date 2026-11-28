# s64 row 64

## Scope
- g 1880-1931 (first_g 1880, 52 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: FOLLOW the plane, then PUSH to the pilot: camera orbit around the pilot seat, 34 -> 3.4 D (eased from g 1893), lens 28 mm, azimuth 32 deg swing, height 2.4 -> 1.9 D; the plane drifts +x at 0.10 D/frame, the prop spins.
- Render: mean 48 s wall per frame per process (2 processes x 2 threads running at the same time; min 39, max 62).

## light_metrics
```
take.mkv (2 fr)                        luma 0.452 p1 0.082 p99 0.839 lc 0.0232 sat 0.488 chroma 35.7 a +3.1 b -2.7 p98 1.00 blue 0.32 warm 0.27 neut 0.02 M 79  MISS  (guides off: p1,p99,lc,warm_frac)
```
## qa_jitter
```
overall median jitter px 1.09
```
## Framing numbers (from the per-frame meta)
- highest head top y 453 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1216 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- One build (sky_close_cockpit): the RFC biplane (scale 2.2, 60 D up) over the green Somme field, pilot25 lean_look in the cockpit seat (cockpit-crop canvas), lean 24 -> 40, head roll, blink g 1913. W -> C in one move; DOF f/2.8. Cloud puff sprites hidden (they read as lilac blobs): the sky is the set's own cumulus-on-blue world shader. Deviation: single build from the close-cockpit preset instead of the wider sky_plane preset; pale sky graded with vibrance 2.0 + HSV saturation x1.2, gamma 0.92.
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
