# QA sC (film 21, plan v3): segment C, g 418-541 (CUT in, no handles), shots "the only crossing"
World K.build_world(['bridge_high','bridge_end_south']), 32 samples, 720x1280, one travelling camera (K.cam_path): high on the east side looking down along the bridge (column of 14 marching 3D knights, 1.6 m/s), flying south and DESCENDING past the south end and the "STIRLING BRIDGE" gantry, then riding beside/behind two cast knights (knight_a_mtd red near, knight_b_mtd blue far, walk cycle, riders pinned, rim gold) whose horses fill the 2.6 m deck side by side; rails brush their lower legs. Camera stays above rail height (z >= 3.4 over the deck) and east of the deck so the side-view horse cards never flip.
g 524 ("ม้าสองตัวก็เต็มแล้ว"): the near knight sucks his belly in (squash 0.84, sweat drop) with a quick x1.3 push (14 f); the far knight gets a sweat drop 3 frames later. Mouths closed, nobody speaks.
Numbers: saturation 0.701, vivid 81.2 %, luma 120.2 (OVER the 85-110 limit: sunlit sand and sky fill the descent; the per-preset VIVID grade was used unchanged), in-shot motion median 14.40 p90 26.74. qa_auto PASS (soft frames g442-444, 448-450 are the fast descent, motion streak).
Colour note: the sand reads lemon yellow in the last third (same issue the director flagged on H2a); I will re-render this segment with the palette fix when it lands on film21/main if asked.
Heads: centre y 520-700, whole heads above y 880, nobody cut by the frame edge, contact shadows on, riders on their horses.
Known: the 3D column ahead of the cast pair is rigid (marches, hoof bob only); the sign is visible from g ~470 and passed in the last second.

## REDO after the TAKE gate (sets e07ceb1 / cast 528bf9d)
1. Belly-suck beat: camera lifted (end z 4.2, look z 4.45-4.55, tilt up) so both riders' torsos clear the rail and sit mid-frame (40-60 % of frame height); at g524 the near knight deflates explicitly (squash 0.74 wide, 1.05 tall, leaning back -9 deg, held, with a sweat drop), the far knight sweats 3 frames later.
2. Colours: current cast (knights crimson/gold, caparisons crimson); my 3D column uses only crimson/gold/cream liveries (no t_blue); camp pavilions come out cream/red/yellow with the new set (no blue).
3. End framing: rail + sand below the knights reduced (lower end position, tilt up).
4. Horizon blades: the set now renders the smoke as soft puffs (no workaround needed).
Numbers (redo): saturation 0.684, luma 120.4 (colour is normalised at the conform per the director), in-shot motion median 15.08 p90 27.79, qa_auto PASS.
