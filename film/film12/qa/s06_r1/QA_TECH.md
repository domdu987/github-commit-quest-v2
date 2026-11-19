# QA_TECH s06 (film12 shots 6-8) - VERDICT: FAIL
Checked: all 54 f6 frames (n=0..265, g309-574) full size, 14 cut frames (g375-381, g462-468), extra ffmpeg crops n64-84 (g373-393) and n254-268 (g563-577), meta, QA_AUTO (PASS).
Note: meta transition_in = cut, frames 6 (reported only).

## Issues
1. Head crossing y 880 (FAIL): Hanway's face/chin goes below y 880 in shot 7 from about f_022 (g~420) to f_031 (g~459) and in cut frames g462-464 (g465_1..3; face spans y~800-935). Fix: raise camera/move Hanway path so head stays < 880 (or drop Hanway out earlier).
2. Coachman posture/contact (FAIL per client rule): the head coachman STANDS on the coach-box plank/roof (boots visible on the box top, f_001-f_054, all three shots). Should sit on the box (legs below, seat visible).
3. Whip (plan miss): whip is held (hand on shaft, OK) but the tip points up/back (arc over left shoulder) in shots 6-8; plan shot 7 wants it pointing at Hanway passing below. Never points at him.
4. Eye-line: in shot 7 (f_016-031) and shot 8 (f_033-054) his half-lidded eyes look straight into camera, not down at Hanway. Shot 7 gives no sense of him addressing Hanway.
5. Plan coverage: shot 8 "other coachmen roar" - only one tiny coachman at far left edge (f_033-046, g464-540 region) with open mouth, clipped by frame edge, then gone. Shot 7 is a wide, not the planned "two-shot". Non-blocking.
6. Hanway clipped at bottom: in g462-464 legs/feet are cut by the lower frame edge (y~1270).
7. Lip-sync: PASS. Laugh g315-377 (open laughing mouth, eyes shut, belly/hands on belly) fine; mouth closed/neutral at g378-381 (n69-72 tiny opening, <0.15 s early); moves from g383 (n74, first open at g383-385) and stays animated through ~g571; at g563-569 wide open, g570-573 small, g574-577 thin dark slit only (within tolerance). No mouth movement outside window.
8. Pops/cuts: cut at g378 (laugh close-up -> wide with Hanway) and g465 (Hanway wide -> coachman wide) are clean, single-frame, on plan. No black/frozen/magenta frames seen. Sharp, no blur, no grain/orbs, no text. Rain is light and consistent; costume (olive caped greatcoat, red scarf, low round hat) consistent; coach ochre side + red box consistent; lanterns lit.
9. Non-blocking: Hanway's walk in shot 7 has no visible foot contact shadow on wet setts; coachman body in shot 8 is rigid (only mouth moves).

Verdict: FAIL (issues 1, 2; 3-4 should be fixed in the same re-render).
