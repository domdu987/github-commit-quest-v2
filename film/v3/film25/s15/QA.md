# QA row 15 (g 396-428, first_g 396, 33 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 58.8 s wall (mean over 33 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 12 % + ARC
- **light_metrics:** `take.mkv (1 fr)                        luma 0.502 p1 0.094 p99 0.974 lc 0.0306 sat 0.451 chroma 22.8 a -0.9 b -1.9 p98 0.98 blue 0.64 warm 0.33 neut 0.08 M 84  PASS  (guides off: p1,p99,lc,chroma,blue_frac,warm_frac)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.87
- 
