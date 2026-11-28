# QA row 34 (g 982-1015, first_g 982, 34 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 34.4 s wall (mean over 34 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the barrel in, PUNCH 15 % on the clunk (g 1005)
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.086 p99 0.974 lc 0.0429 sat 0.349 chroma 21.6 a +3.6 b +6.2 p98 0.70 blue 0.19 warm 0.67 neut 0.12 M 72  MISS  (guides off: p1,p99,chroma,sat_p98)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.13
- 
