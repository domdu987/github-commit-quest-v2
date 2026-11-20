# QA s13 (film 18, render team 4)
Range g 1003-1070, take.mkv frames 994..1076 (83 frames), transition in: dissolve.
Render: 720x1280, 12 samples, OIDN, 2 threads, 15.0 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 8.07, p90 10.74, min 2.27, max 12.41, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 494, "crowd0": 517, "crowd1": 511, "crowd2": 525, "crowd3": 589, "crowd4": 592, "crowd5": 640, "crowd6": 633, "crowd7": 661, "crowd8": 597, "crowd9": 489, "crowd10": 472, "crowd11": 519, "crowd12": 533, "crowd13": 554, "sentry": 659}

## Notes
- Transition in: dissolve 13 frames (night falls); handles 9 in / 6 out.
- Cut dark box at the top-right removed (pennant pole at (-15.5,-84) skipped at build); camera tilted down (sky ~30 %).
- Sentry drops a real 3D spear at g 1030 and joins the cheering; 14 crowd cards cheer/dance (bounce 0.10 D at 3 Hz, mirror turns); warm point lights and rim light; general laughs (held mouth).
- Camera: pull-out 6 %/s, slide 40 px/s, sway 0.6 deg, 3 punch-ins. Mouths do not move.
- Re-render after TAKE gate rules: zoom pulses removed (two held punch-ins), stronger sway; p90 frame diff just under 12 as a result.

See QA_AUTO.md and phone_sheet.jpg.
