# QA row 14 (g 353-395, first_g 353, 43 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 39.4 s wall (mean over 43 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the model tank (3/4 top-down), then PULL / swoop to the engineer's face
- **light_metrics:** `take.mkv (1 fr)                        luma 0.502 p1 0.127 p99 0.893 lc 0.0172 sat 0.216 chroma 11.6 a +1.0 b +7.1 p98 0.49 blue 0.01 warm 0.72 neut 0.28 M 35  MISS  (guides off: p1,p99,lc,chroma,sat_p98,M)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 3.08
- 
