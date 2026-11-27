# QA_C s09 (shots 9a macro_oar + 9 hansan_high), relight only, look C
- Old shot.py unchanged, JOSEON_LOOK=C, frames numbered by OLD g 913-1007 (hard cut at 954); meta_C.json carries +208 (g0 1127, g1 1210, first_g 1121). 24 samples (macro_oar preset 12), 540x960 + post -> 720x1280. Shots 9 and 19 rendered in separate processes (a second sea build in one process crashes in kit).
- qa_auto: only "suspected blur" on 25 frames (g 913-923, 934-...): the macro_oar shot 9a has intended shallow DOF (f/2.8) and haze, not a real focus problem. No frozen runs, no pops.
- qa_jitter: median 0.1 px, no shake. No cast (no people); no mouths.
- Reviewed contact_C.jpg.

## Update: 9a relight (director note: first draft was dark navy)
- Shot 9a (g 913-953, macro_oar) re-rendered with shot_9aC.py: exposure +0.8, a warm amber area rim behind the oar (sun side) and an amber bounce from the camera side. Same camera and splash timing as shot.py. Frames come from relit9a/raw/s9; shot 9 (g 954-1007) is unchanged.
- qa_auto now PASS (the earlier "blur" flag went away with the lift). The water is still blue-lavender (deep-water palette) but clearly lighter; the hull and oar blades read warm.
