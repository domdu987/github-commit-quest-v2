# QA row 62 (g 1813-1842, first_g 1813, 30 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 28.9 s wall (mean over 30 frames, 2 threads, 2 processes running)
- **Camera move:** lateral slide from the water tank to the Mark I
- **light_metrics:** `take.mkv (1 fr)                        luma 0.498 p1 0.089 p99 0.932 lc 0.0494 sat 0.357 chroma 21.2 a +1.4 b +2.2 p98 0.99 blue 0.37 warm 0.58 neut 0.15 M 67  MISS  (guides off: p1,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.35
- 
