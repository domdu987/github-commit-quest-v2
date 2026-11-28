# s21 row 21 GAG: the general dangles the toy tank

## Scope
- g 602-625 (first_g 602, 24 frames, 30 fps, 720x1280), hard cut in, Look A (client pick 28 Nov): 2D cast25 cards with an inflated normal-map shading pass, near plate backdrop with a crisp cast shadow where the shot is C / M, mild DOF on close shots only.
- Pipeline (film/v3/film25/s21): `d25.py` (rig, beauty 24 adaptive samples thr 0.02 OIDN 75 % + white-card shading pass 10 samples at 50 %), `post_d.py` (background grade, sprite colour x shading, face cap, ink occlusion), `finish.py`.
- Camera move: PUNCH 20 % over g 602-609 (camera 5.0 -> 4.17 D at 40 mm; head width 279 -> 340 px), then a slow +4 % push and a 0.25 D slide with a 6 deg arc (measured from the head size on screen: scale +22 %, pan under 3 % of the width per second).
- Render: mean 99 s wall per frame per process (2 processes x 2 threads running at the same time; min 76, max 130).

## light_metrics
```
take.mkv (1 fr)                        luma 0.499 p1 0.090 p99 0.972 lc 0.0478 sat 0.416 chroma 28.7 a +2.9 b +5.4 p98 0.90 blue 0.29 warm 0.55 neut 0.26 M 85  PASS  (guides off: p1,p99)
```
## qa_jitter
```
overall median jitter px 0.73
```
## Framing numbers (from the per-frame meta)
- highest head top y 229 px (rule: heads above y 880 means head bottoms; head tops far above), lowest feet y 1462 px (feet are below the frame edge when > 1280 or above y 860 when in frame).
## Notes
- Toy tank 1.6x (prop scale 1.6) and held higher; head 0.39-0.47 of the frame width; waist-up crop with the boots just in the frame (soles below the frame edge).\n- Lip-sync inside his quote (talk_mouth). Poses change every phrase: toy swing t every frame, gaze, yaw, head roll, squash accent on g 602-607, sneer on g 615, blink g 613.\n- Near backdrop: a grey-olive riveted plate wall 2 D behind him, sky above; his cast shadow lands on it. Sun disc 0.5 deg, sun 8, sky 0.5.\n- Deviation: post_d.py raised vibrance to 1.55 and the white-balance gain clamp to 0.55-1.9 so that sat is 0.40+ and b* <= 6 on the warm sun (s21 was rendered with the first warm sun colour; later takes use sun colour 1.0/0.9/0.74).
## Files
shot.py, d25.py / c25.py / post_d.py / finish.py (in ../s21), meta.json, contact.jpg, QA_AUTO.md, phone_sheet.jpg, take.mkv (frames, raw and work stay out of git).
