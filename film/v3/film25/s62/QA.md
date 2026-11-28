# QA row 62 (g 1813-1842, first_g 1813, 30 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 26.0 s wall (mean over 30 frames, 2 threads, 2 processes running)
- **Camera move:** lateral slide from the water tank to the Mark I
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.090 p99 0.899 lc 0.0278 sat 0.335 chroma 18.7 a +3.7 b +4.0 p98 0.85 blue 0.32 warm 0.65 neut 0.05 M 57  MISS  (guides off: p1,p99,lc,chroma,M)`
- **qa_auto:** see QA_AUTO.md (exit 0)
- **qa_jitter:** overall median jitter px 0.35
- 
