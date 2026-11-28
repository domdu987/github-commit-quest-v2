# QA row 37 (g 1071-1094, first_g 1071, 24 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 37.5 s wall (mean over 24 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the crate swing (pan)
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.109 p99 0.868 lc 0.0325 sat 0.356 chroma 21.6 a +2.8 b +5.2 p98 0.84 blue 0.38 warm 0.57 neut 0.08 M 72  MISS  (guides off: p1,p99,lc,chroma,sat_p98)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 1.48
- 
