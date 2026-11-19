# s18 QA (re-take 3 after QA-art round 2): film 16, shot 18, LINE line_road / DUSK
- take.mkv g 1110..1234 (125 f; shot g 1119..1225), 720x1280, 7 spp, 2 threads, 12.0 s wall / 23.1 s cpu per frame, 40.1 MB (one file). Hard cuts.
- Staging: camera now OUTSIDE the buggy on the field side (+y), low (z 1.8-2.5): a textured wheel + the plank-grain side panel in the foreground, the mocker seated above them (the set's red seat slab is hidden: its visibility is re-keyed every frame), and BEHIND him the road, the furrow edge, the pole fence and MORSE'S GROUP (Morse clutching his coil, workers a and b leaning on shovels; cast cards staged at the furrow, mirrored to face the buggy) on the side he points to. The buggy heads +x = screen-left (the mule is on the left, facing left, in the opening wide). He rolls gently past the group (0.45 D/s).
- The mocker turns his head toward the group on "ใต้ดินแล้ว" (yaw 0.45 -> 0.78 over g 1201..1209). Still laughing + tears from the blink at g 1154; belly bounce, buggy / mocker / mule bob 0.05 D at 3 Hz.
- LIP-SYNC only g 1157..1227 (38.46-40.80 s): raw/*.json "flat" <= 1156, "sync" from 1157.
- Opening wide is short (reframes by g 1138) and centres him (head 117 px at g 1119, 164 px by g 1138, 164 px when the lips start, 280 px at the end); head centre y 516-604, bottoms <= 688.
- Camera: wide quint reframe, lateral slide 28 px/s + arc 9 deg/s, snap x1.8 with a pan back onto his face on g 1204..1216.
- Frame-diff in shot: median 5.45, p90 13.14 (target 4 / 12: met). qa_auto PASS.
- Known: the field-side light is backlit, so the tree masses behind are dark; the mule is on screen only in the first ~0.6 s.
