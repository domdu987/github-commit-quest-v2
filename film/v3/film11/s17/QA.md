# s17 QA (render team 3)
- g 1050..1121 (72 frames, 1056..1115 + 6 handles each side), garden_hut / A (closer), cut in, 12 samples, ~10 s/frame wall.
- QA_AUTO: PASS. Heads above y 880 (see meta max_chin_y). No mouths (doctor scoffs, mouth still).
- Lancet tip pinned to James's upper-arm anchor (reach error 0.000 D); Jenner/James mirrored vs the story pose (camera is on the other side), so the blister uses upper_arm_r. Doctor stands behind at the garden path (-8.7, 0.3) instead of the gate (the gate is behind the camera in this view).
- Re-rendered 2026-11-18 per the director note: the chimney smoke hooks (blob stacks) are hidden (hide_render) in c11.Take; QA_AUTO PASS again.
