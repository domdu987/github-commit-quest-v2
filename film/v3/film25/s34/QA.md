# QA row 34 (g 982-1015, first_g 982, 34 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 37.9 s wall (mean over 34 frames, 2 threads, 2 processes running)
- **Camera move:** FOLLOW the barrel in, PUNCH 15 % on the clunk (g 1005)
- **light_metrics:** `take.mkv (1 fr)                        luma 0.494 p1 0.086 p99 0.974 lc 0.0429 sat 0.394 chroma 24.5 a +5.1 b +5.2 p98 1.00 blue 0.18 warm 0.64 neut 0.08 M 90  MISS  (guides off: p1,p99,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.1
- 
