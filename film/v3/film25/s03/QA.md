# QA row 3+4 (g 44-83, first_g 44, 40 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 50.6 s wall (mean over 40 frames, 2 threads, 2 processes running)
- **Camera move:** tilt down with the hull, then pan / push onto the dial
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.073 p99 0.973 lc 0.0456 sat 0.476 chroma 28.6 a +4.8 b +6.9 p98 1.00 blue 0.25 warm 0.64 neut 0.04 M 94  MISS  (guides off: p99)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** 0s shake   7.3px
overall median jitter px 4.32
- 
