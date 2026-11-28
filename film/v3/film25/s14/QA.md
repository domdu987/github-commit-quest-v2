# QA row 14 (g 353-395, first_g 353, 43 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 45.6 s wall (mean over 43 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the model tank (3/4 top-down), then PULL / swoop to the engineer's face
- **light_metrics:** `take.mkv (1 fr)                        luma 0.501 p1 0.153 p99 0.806 lc 0.0184 sat 0.519 chroma 32.1 a -1.2 b +8.9 p98 1.00 blue 0.19 warm 0.65 neut 0.01 M 142  MISS  (guides off: p1,p99,lc)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** 0s shake   2.1px
overall median jitter px 2.81
- 
