# QA row 31+32 (g 918-959, first_g 918, 42 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 40.9 s wall (mean over 42 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the track drop, then a gentle slide along the loop
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.079 p99 0.974 lc 0.0590 sat 0.450 chroma 29.3 a +3.5 b +2.3 p98 0.90 blue 0.28 warm 0.52 neut 0.10 M 103  PASS  (guides off: p99)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.28
- 
