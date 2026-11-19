# QA s15 (film 18, render team 4)
Range g 1136-1204, take.mkv frames 1130..1210 (81 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 26.6 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 5.72, p90 13.25, min 0.98, max 18.84, frames < 1: 1 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 732, "soldier0": 699, "crowd0": 710, "crowd1": 694, "crowd2": 678}

## Notes
- Lip-sync on every frame (quote 2b, 36.99-40.10 s); carving hand 4 levels, cup tilt 2 levels. Others held mouths.
- fg jars scaled to 70 % and placed in the bottom frame corners (ground_at projection), extra cups hidden (QA-art s15).
- Camera: slide 40 px/s, 10 %/s push, sway, 3 punch-ins homing on the general; warm rim light as s14.

See QA_AUTO.md and phone_sheet.jpg.
