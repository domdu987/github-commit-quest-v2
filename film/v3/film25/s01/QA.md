# QA row 1+2 (g 0-43, first_g 0, 44 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 49.5 s wall (mean over 44 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH in through the doors (wide to close), eased
- **light_metrics:** `take.mkv (1 fr)                        luma 0.497 p1 0.138 p99 0.828 lc 0.0376 sat 0.379 chroma 22.5 a -0.7 b -1.7 p98 0.95 blue 0.49 warm 0.34 neut 0.13 M 74  MISS  (guides off: p1,p99,lc,chroma,blue_frac,warm_frac)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 1.7
- 
