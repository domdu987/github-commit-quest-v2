# QA row 16 (g 429-458, first_g 429, 30 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 56.1 s wall (mean over 30 frames, 2 threads, 2 processes running)
- **Camera move:** PULL 10 %
- **light_metrics:** `take.mkv (1 fr)                        luma 0.499 p1 0.098 p99 0.974 lc 0.0428 sat 0.468 chroma 28.8 a +2.4 b +5.0 p98 1.00 blue 0.32 warm 0.61 neut 0.05 M 90  PASS  (guides off: p1,p99)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 1.03
- 
