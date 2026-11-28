# QA row 33 (g 960-981, first_g 960, 22 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 40.8 s wall (mean over 22 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 10 % on the sponson
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.088 p99 0.974 lc 0.0404 sat 0.451 chroma 26.2 a +2.7 b +5.4 p98 0.78 blue 0.29 warm 0.63 neut 0.06 M 86  PASS  (guides off: p1,p99,chroma,sat_p98)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.47
- 
