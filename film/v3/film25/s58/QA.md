# QA row 58 (g 1724-1745, first_g 1724, 22 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 42.6 s wall (mean over 22 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 10 % onto the board
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.059 p99 0.974 lc 0.0303 sat 0.456 chroma 28.6 a +8.4 b +6.0 p98 0.93 blue 0.32 warm 0.62 neut 0.07 M 99  MISS  (guides off: p99,lc)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.56
- 
