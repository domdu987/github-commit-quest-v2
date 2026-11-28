# QA row 6 (g 125-153, first_g 125, 29 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 95.6 s wall (mean over 29 frames, 2 threads, 2 processes running)
- **Camera move:** PULL 10 % (4.0 -> 4.4 D) + slight drift
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.103 p99 0.974 lc 0.0483 sat 0.447 chroma 25.4 a +1.9 b +4.6 p98 0.74 blue 0.34 warm 0.53 neut 0.12 M 98  PASS  (guides off: p1,p99,chroma,sat_p98)`
- **qa_auto:** PASS (QA_AUTO.md, phone_sheet.jpg)
- **qa_jitter:** overall median jitter px 0.63
- 
