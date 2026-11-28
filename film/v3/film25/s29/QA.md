# QA row 29+30 (g 882-917, first_g 882, 36 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 40.3 s wall (mean over 36 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the plate in, then PUSH 8 % on the rivets
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.052 p99 0.974 lc 0.0481 sat 0.516 chroma 31.2 a +2.7 b +5.5 p98 0.97 blue 0.37 warm 0.50 neut 0.05 M 98  MISS  (guides off: p99)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.56
- 
