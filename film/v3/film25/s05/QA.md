# QA row 5 (g 84-124, first_g 84, 41 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 46.8 s wall (mean over 41 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 12 % + slight ARC
- **light_metrics:** `take.mkv (1 fr)                        luma 0.502 p1 0.088 p99 0.974 lc 0.0395 sat 0.490 chroma 29.1 a +4.9 b +5.1 p98 0.97 blue 0.38 warm 0.53 neut 0.09 M 98  PASS  (guides off: p1,p99)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.34
- 
