# s01 QA: film 10, shots 1-2 (hook), harbour DAY
Delivered: take.mkv g 0..139 (140 frames, 720x1280, 12 samples, libx264rgb crf 6), first_g 0, g0 0, g1 134, out-handle g 134..139. transition_in: open.
- g 0..68 shot 1 hull_plank: Norman (cast10 painter10, plank=0 because the set has its own plank) sweeps the big brush; set_stripes keyed 0.30 -> 0.48 every frame (front enters frame ~g 20, reaches the brush at the end). Slow push 24 -> 26 mm.
- g 69..139 shot 2 harbour_wide, crane out (rise + pull back), stage 0.48 -> 0.50; 7 visible placeholder cards swapped for cast10 sailors, the rest hidden.
- Cut at g 69 detected by qa_auto (PASS, no frozen/pops/blur/magenta). Heads: painter y ~560 (0.44 H) in shot 1, all heads < 880.
- Mouths: none move (no quote). No DOF. Own review at 6 fps via contact.jpg: no problems found.
- Differs from plan: set_stripes starts at 0.30 (visually identical to 0 in the plank view; the front first appears at ~0.36).
