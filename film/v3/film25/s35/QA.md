# QA row 35 (g 1016-1042, first_g 1016, 27 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 52.8 s wall (mean over 27 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the hammer, slide right
- **light_metrics:** `take.mkv (1 fr)                        luma 0.444 p1 0.030 p99 0.974 lc 0.0439 sat 0.382 chroma 20.0 a +6.6 b +10.6 p98 0.97 blue 0.08 warm 0.84 neut 0.05 M 61  MISS  (guides off: p99,chroma,M)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.34
- 
