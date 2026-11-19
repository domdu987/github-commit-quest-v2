# s18 QA (re-take 2 after the director's note): film 16, shot 18, LINE line_road / DUSK
- take.mkv g 1110..1234 (125 f; shot g 1119..1225), 720x1280, 7 spp, 2 threads, 10.4 s wall / 20.1 s cpu per frame, 33.7 MB. Hard cuts.
- LIP-SYNC only g 1157..1227 (38.46-40.80 s; raw/*.json "flat" <= 1156, "sync" from 1157). Smug flat mouth to the blink at g 1154, then laughing + tears; belly bounce +/-0.09 D at 3 Hz + squash; pointing at the furrow.
- Camera: OPENS WIDE (whole rig: mocker, buggy, mule with its head and ears bobbing in frame, ~1.1 s), a quint reframe onto the mocker by g 1160 (head 68 px -> 182 px when the lips start, y centre 540-575), then a lateral slide 50 px/s + arc 12 deg/s round him (head 180-185 px, y 555-620), and a pan + push x1.4 sideways onto his face on "ใต้ดินแล้ว" (g 1204..1216; head 254 px, y centre 494 at g 1225). Head centre y 478-576 in the medium part, bottoms <= 662 (< 880). No grass in frame after the reframe (camera z 2.5+).
- Jolt: the buggy and the mocker bob 0.05 D at 3 Hz, the mule 0.04 D, wheels turning, trot 3 D/s so the road and furrow stream past; plank-grain texture on the buggy.
- Frame-diff in shot: median 6.65, p90 18.68 (target 4 / 12: met). qa_auto PASS.
- Known: the first ~1.1 s is a wide (mocker head 68-70 px) so the mule's head reads; it is still silent then (lips start at g 1157, head >= 170 px).
