# s05 QA: film 24, shots 5-6 (sea, flagship jflag)
Delivered: take.mkv.partaa/ab (libx264rgb crf 6, 58 MB split; `cat take.mkv.part* > take.mkv`), first_g 425, 225 frames g 425..649 (6 in-handle, shot 5 g 431..512, shot 6 g 513..643, 6 out-handle), meta.json, cues.json, contact.jpg, QA_AUTO.md (PASS), phone_sheet.jpg. Hard cut inside the take at g 513.

| rule | result |
|---|---|
| floating / shadows | all cards Child-Of `jflag` ride, feet on deck z 5.44 with contact decal + shadow proxy; checked on strips |
| camera | shot 5 push-in 10 % (flag_deck), shot 6 slide left 2.6 D (flag_deck_b), 0.35 sine + 0.65 linear; qa_jitter median 0.26 px, no shake; no frozen run |
| duplicates / size | jp_cmd24 + ashi_a24 (laugh_point) + ashi_b24 (laugh_point, mirrored); commander head 168-255 px, soldiers 108-134 px |
| heads above y 880 | max head bottom 831 (commander), soldiers <= 750 |
| faces | commander head <= ~255 px wide, never fills the frame |
| mouths | only jp_cmd24. Shot 5: held laugh mouth; from g 486 (16.1 s) talk_mouth alternating with the laugh shape every 3 frames (director note). Shot 6: talk_mouth g 513..645, flat after 645 (out-handle) |
| pose change | point_mock -> finger_up_promise at g 547 (18.11 s, "ถ้าเต่าตัวนั้น") |
| tone | comic, no injury |

Render: R9, 24 samples, 540x960 + post; 49.4 s wall / 94.9 s CPU per frame (two processes, 2 threads each).
Deviations: the quote starts inside shot 5 (g 486), handled as above. Pose swap in shot 6 is a hard pose change (puppet style). Commander feet sit low in frame (y ~1100) because the deck camera is close.

## Revision (director QA): shot 6 re-rendered g 513-649
- Camera now aims at the commander: head centre x 0.45-0.49 W (g 513/547/581/615/649), kabuto, arm and drum fully in frame, nothing clipped by the left edge. Shot 5 unchanged (accepted).
- qa_auto PASS, jitter median 0.27 px, heads bottom max 830 (<880), 45.4 s wall / 87.3 s CPU per frame.
