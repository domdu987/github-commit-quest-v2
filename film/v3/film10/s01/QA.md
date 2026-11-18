# s01 QA: film 10, shots 1-2 (hook), harbour DAY
Delivered: take.mkv g 0..139 (140 frames, 720x1280, 12 samples, libx264rgb crf 6), first_g 0, g0 0, g1 134, out-handle g 134..139. transition_in: open.
- g 0..68 shot 1 hull_plank: Norman (cast10 painter10, plank=0 because the set has its own plank) sweeps the big brush; set_stripes keyed 0.43 -> 0.48 every frame; the painter sidesteps along the plank so the stripe front stays at the brush tip (front x = -32 + 64*stage); shadow casters of scaffold/extras switched off in shot 1 so the navy/white band does not read as shadow; camera shifted left to keep the ladder away from the brush. Slow push 24 -> 26 mm.
- g 69..139 shot 2 harbour_wide, crane out (rise + pull back), stage 0.80 -> 0.90 (bold zigzag + staircase along the hull); 7 visible placeholder cards swapped for cast10 sailors, the rest hidden.
- Cut at g 69 detected by qa_auto (PASS, no frozen/pops/blur/magenta). Heads: painter y ~560 (0.44 H) in shot 1, all heads < 880.
- Mouths: none move (no quote). No DOF. Own review at 6 fps via contact.jpg: no problems found.
- QA-art rework (round 2): stripe visible from frame 1 attached to the brush; stage capped at 0.48 in shot 1 (front cannot outrun the plank, which spans x -6..-0.2; 0.75 would be x +16); shot 2 camera moved right to drop the cyan water wedge at the left edge.
