# QA row 28 (g 838-881, first_g 838, 44 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 37.6 s wall (mean over 44 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 10 %
- **light_metrics:** `take.mkv (1 fr)                        luma 0.501 p1 0.050 p99 0.974 lc 0.0379 sat 0.404 chroma 22.8 a +2.9 b +3.4 p98 0.97 blue 0.32 warm 0.64 neut 0.07 M 83  PASS  (guides off: p99,lc,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.31
- 
