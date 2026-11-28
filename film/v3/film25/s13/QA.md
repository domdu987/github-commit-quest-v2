# QA row 13 (g 316-352, first_g 316, 37 frames incl. handles)
- **Look A pipeline** (rig25.py): beauty 16 adaptive samples thr 0.03 OIDN at 75 %, shading pass (white cards + inflated normal map, 6 samples at 50 %), composite (set sharpen/clarity, gentle bg grade, sprite colour x shading, face centre exact #fef7f6, ink AO). Near backdrop plate + crisp 0.5 deg sun; mild DOF.
- **s/frame:** 29.6 s wall (mean over 37 frames, 2 threads, 2 processes running)
- **Camera move:** PUSH 12 %, WHIP out over the last 5 frames
- **light_metrics:** `take.mkv (1 fr)                        luma 0.500 p1 0.097 p99 0.974 lc 0.0442 sat 0.305 chroma 21.4 a +1.4 b +10.6 p98 0.96 blue 0.03 warm 0.46 neut 0.04 M 58  MISS  (guides off: p1,p99,chroma,M)`
- **qa_auto:** see QA_AUTO.md (FAILS: # QA_AUTO FAIL  (take.mkv, 37 frames, 30.00 fps, g 316-352)

## FAIL
- suspected blur on 2 frames, e.g. g [351, 352]
## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.
)
- **qa_jitter:** overall median jitter px 0.72
- 
