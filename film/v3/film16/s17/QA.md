# s17 QA: film 16, shot 17 (empty money bag), LINE line_trench_end / DUSK
- take.mkv g 1066..1127 (62 f; shot = g 1075..1118 = 35.82-37.30 s; 9 handle frames each side), 720x1280, 7 spp, 2 threads, 11.5 s wall / 22.3 s cpu per frame. Hard cuts both sides.
- Staging: the preset's key crate would hide the bodies, so the three stand to its right (marks overridden at runtime): Morse hero in front (head 220 -> 330 px), worker_a left (145-171 px), worker_b right (108-150 px, mirrored). Head centres y 537-629, whole heads above y 880 (bottoms <= 721).
- Poses: morse_empty_bag (bag shaken from g 1072, lining out), worker lean_shovel x2; blinks and sway; expression mouths only (no lip-sync).
- Camera (own 22 mm, c16.CamPath): push 13 %/s + slide 40 px/s + arc 20 deg/s (parallax), plus a soft snap x1.35 g 1085..1098 (shot is 1.5 s: the plan has none; added for the frame-diff target) that keeps the bag + worker_b in frame.
- Frame-diff in shot: median 3.91, p90 9.59 (target 4 / 12): marginally below.
- qa_auto PASS. Checked at 6 fps: bag in hand all shot, shovels held, contact shadows on the grass; sprites are 256 px/D so the snap-time Morse (330 px head) is slightly soft.
