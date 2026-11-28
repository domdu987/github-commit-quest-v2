# QA row 62 (g 1813-1842, first_g 1813, 30 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 26.0 s wall (mean over 30 frames, 2 threads, 2 processes running)
- **Camera move:** lateral slide from the water tank to the Mark I
- **light_metrics:** `take.mkv (1 fr)                        luma 0.499 p1 0.090 p99 0.910 lc 0.0277 sat 0.482 chroma 26.9 a +2.0 b +4.5 p98 0.91 blue 0.28 warm 0.65 neut 0.02 M 93  PASS  (guides off: p1,lc,chroma)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.36
- 
