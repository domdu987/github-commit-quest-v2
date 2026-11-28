# QA row 6 (g 125-153, first_g 125, 29 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 48.3 s wall (mean over 29 frames, 2 threads, 2 processes running)
- **Camera move:** PULL 10 % (4.0 -> 4.4 D) + slight drift
- **light_metrics:** `take.mkv (1 fr)                        luma 0.499 p1 0.102 p99 0.974 lc 0.0412 sat 0.257 chroma 16.1 a +2.5 b +9.0 p98 0.67 blue 0.11 warm 0.72 neut 0.24 M 47  MISS  (guides off: p1,p99,chroma,sat_p98,M)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.39
- 
