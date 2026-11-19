# QA_TECH s09 (take g674-736, 63 frames) - FAIL (re-check of the re-shot)
Checked: 6 fps frames + first/last 3, framediff re-measured (62 pairs): median 12.82, p90 18.43 (min 7.74, max 19.76) - passes. Caption band y880-950 mean max 82.9, bright 0.05 %. Mouth crops at g674,675,676,678,680,682,684,686 viewed at full size.
## Earlier issues (previous QA_TECH s09)
- E1 lip-sync legibility / mouth open at g674: FIXED. Mouth is closed at g674-675; from g676 a brown oval opens below the moustache and alternates open/closed.
- E2 cloud stickers: FIXED (clear gradient sky).
- E3 armour skirt, legs and feet in the band: NOT FIXED (feet to y ~1100 at g714); legs in the band are allowed, non-blocking, see 3.
- E4 wobble: improved (max diff 19.8 vs 24); the lateral drift is now the problem, see 1.
- E5 eye-line to the lens: acceptable, unchanged.
## Issues
1. g704-736 - framing, BLOCKING: the camera slide carries the general off the left edge. He is clipped by x=0 from g704 (g709, g714 the skirt and arm are cut), his head is half out at ~g724, and he is gone from g~727 to g736 (only a red sleeve at x=0 at g729-736). The end of "งั้นเหรอ!" (23.93-24.56 s) is spoken with the general off screen and the shot ends on a laughing soldier. Fix: reverse the slide direction or retarget look_at on him so he stays 60+ px inside the frame to g736.
2. g709-736 - lip-sync: with the general out of frame the quote 1a lip-sync cannot be seen for the last ~10 frames (follows from 1).
3. g674-724 - framing (non-blocking): armour skirt and red legs sit across the caption band y 880-950, feet at y ~1000-1100. Legs allowed; head chin max ~y 800 OK.
4. g709-736 - mouths (note): the soldier at the right has a wide open yelling mouth (teeth) from g709. It is a constant laugh drawing, not animated, so not lip-sync; keep, but make sure it reads as laughing, not as speaking.
## Pass items
heads/chin < 880 (general chin max ~y 800); mouths of the general closed at g674-675 and moving only from g676 (22.45 s) on; no other mouth animates; no text; no flames except the camp fire; DUSK matches the plan; arms wide beat visible; contact shadows faint but present; no frozen/black/magenta frames; g range 674-736 matches the plan.
