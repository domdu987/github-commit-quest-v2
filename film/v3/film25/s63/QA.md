# QA row 63 (g 1843-1879, first_g 1843, 37 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 38.3 s wall (mean over 37 frames, 2 threads, 2 processes running)
- **Camera move:** PULL 10 % + ARC
- **light_metrics:** `take.mkv (1 fr)                        luma 0.499 p1 0.098 p99 0.974 lc 0.0433 sat 0.423 chroma 26.5 a +2.5 b +5.0 p98 1.00 blue 0.25 warm 0.59 neut 0.10 M 99  PASS  (guides off: p1,p99,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.12
- 
