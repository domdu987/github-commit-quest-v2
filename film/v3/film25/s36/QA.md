# QA row 36 (g 1043-1070, first_g 1043, 28 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 55.3 s wall (mean over 28 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the brush stroke
- **light_metrics:** `take.mkv (1 fr)                        luma 0.501 p1 0.027 p99 0.967 lc 0.0374 sat 0.283 chroma 15.2 a +3.3 b +11.4 p98 0.50 blue 0.02 warm 0.93 neut 0.08 M 37  MISS  (guides off: p99,lc,chroma,sat_p98,M)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.48
- 
