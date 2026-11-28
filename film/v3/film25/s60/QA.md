# QA row 60+61 (g 1778-1812, first_g 1778, 35 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 43.3 s wall (mean over 35 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 10 %, PUNCH 15 % on the lid open (g 1801)
- **light_metrics:** `take.mkv (1 fr)                        luma 0.499 p1 0.042 p99 0.919 lc 0.0302 sat 0.282 chroma 15.5 a +5.4 b +9.5 p98 0.59 blue 0.08 warm 0.87 neut 0.12 M 44  MISS  (guides off: lc,chroma,sat_p98,M)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.38
- 
