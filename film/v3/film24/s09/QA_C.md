# QA_C s09 (shots 9a macro_oar + 9 hansan_high), relight only, look C
- Old shot.py unchanged, JOSEON_LOOK=C, frames numbered by OLD g 913-1007 (hard cut at 954); meta_C.json carries +208 (g0 1127, g1 1210, first_g 1121). 24 samples (macro_oar preset 12), 540x960 + post -> 720x1280. Shots 9 and 19 rendered in separate processes (a second sea build in one process crashes in kit).
- qa_auto: only "suspected blur" on 25 frames (g 913-923, 934-...): the macro_oar shot 9a has intended shallow DOF (f/2.8) and haze, not a real focus problem. No frozen runs, no pops.
- qa_jitter: median 0.1 px, no shake. No cast (no people); no mouths.
- Reviewed contact_C.jpg.
