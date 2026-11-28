# QA row 38 (g 1095-1134, first_g 1095, 40 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 21.0 s wall (mean over 40 frames, 2 threads, 2 processes running)
- **Camera move:** slow ARC 6 deg round the crate
- **light_metrics:** `take.mkv (1 fr)                        luma 0.504 p1 0.071 p99 0.840 lc 0.0263 sat 0.449 chroma 26.3 a +1.0 b +3.1 p98 0.99 blue 0.32 warm 0.65 neut 0.05 M 100  PASS  (guides off: p99,lc,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.31
- 
