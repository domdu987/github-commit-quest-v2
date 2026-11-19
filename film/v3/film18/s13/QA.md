# QA s13 (film 18, render team 4)
Range g 1003-1070, take.mkv frames 994..1076 (83 frames), transition in: dissolve.
Render: 720x1280, 12 samples, OIDN, 2 threads, 15.3 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 7.75, p90 13.32, min 1.57, max 19.72, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 505, "crowd0": 527, "crowd1": 522, "crowd2": 534, "crowd3": 592, "crowd4": 595, "crowd5": 635, "crowd6": 627, "crowd7": 654, "crowd8": 600, "crowd9": 499, "crowd10": 483, "crowd11": 528, "crowd12": 541, "crowd13": 560, "sentry": 651}

## Notes
- Transition in: dissolve 13 frames (night falls); handles 9 in / 6 out.
- Cut dark box at the top-right removed (pennant pole at (-15.5,-84) skipped at build); camera tilted down (sky ~30 %).
- Sentry drops a real 3D spear at g 1030 and joins the cheering; 14 crowd cards cheer/dance (bounce 0.10 D at 3 Hz, mirror turns); warm point lights and rim light; general laughs (held mouth).
- Camera: pull-out 6 %/s, slide 40 px/s, sway 0.6 deg, 3 punch-ins. Mouths do not move.

See QA_AUTO.md and phone_sheet.jpg.
