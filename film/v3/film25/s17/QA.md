# QA row 17 (g 459-484, first_g 459, 26 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 60.7 s wall (mean over 26 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the brush
- **light_metrics:** `take.mkv (1 fr)                        luma 0.497 p1 0.110 p99 0.965 lc 0.0433 sat 0.317 chroma 20.5 a +2.9 b +5.4 p98 1.00 blue 0.24 warm 0.55 neut 0.25 M 73  MISS  (guides off: p1,p99,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.57
- 
