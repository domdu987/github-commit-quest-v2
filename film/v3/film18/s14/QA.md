# QA s14 (film 18, render team 4)
Range g 1071-1135, take.mkv frames 1065..1141 (77 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 26.2 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 7.56, p90 21.06, min 1.02, max 28.98, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 832, "soldier0": 839, "soldier1": 817, "crowd0": 804, "crowd1": 798, "crowd2": 799, "crowd3": 798, "crowd4": 799, "crowd5": 794}

## Notes
- Lip-sync only from g 1113 (36.99 s, quote 2a); all other mouths held. Crowd cheers use a held mouth (talk drawing removed).
- Camera: slide 40 px/s, 9 %/s push, hand-held sway 0.55 deg at 2.8 Hz and 3 punch-ins (1.2-1.26x) homing on the general; chins stay < 840.
- Warm rim light (orange copy shifted left) on the general and crowd; party fires add warm point lights. transparent_max_bounces 64.
- Deviation: fg party jars/cups left as the set builds them (QA-art asked the 70 % corner jars for s15 only).

See QA_AUTO.md and phone_sheet.jpg.
