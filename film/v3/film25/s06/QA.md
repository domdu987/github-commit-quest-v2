# QA row 6 (g 125-153, first_g 125, 29 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 42.8 s wall (mean over 29 frames, 2 threads, 2 processes running)
- **Camera move:** PULL 10 % (4.0 -> 4.4 D) + slight drift
- **light_metrics:** `take.mkv (1 fr)                        luma 0.499 p1 0.106 p99 0.974 lc 0.0415 sat 0.470 chroma 28.1 a +1.8 b +0.7 p98 0.82 blue 0.42 warm 0.46 neut 0.08 M 96  PASS  (guides off: p1,p99,sat_p98)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.39
- 
