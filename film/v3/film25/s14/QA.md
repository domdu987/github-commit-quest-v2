# QA row 14 (g 353-395, first_g 353, 43 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 84.4 s wall (mean over 43 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the model tank (3/4 top-down), then PULL / swoop to the engineer's face
- **light_metrics:** `take.mkv (1 fr)                        luma 0.501 p1 0.152 p99 0.807 lc 0.0241 sat 0.459 chroma 33.6 a +1.7 b +4.2 p98 0.64 blue 0.32 warm 0.48 neut 0.01 M 81  PASS  (guides off: p1,p99,lc,sat_p98)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 1.68
- 
