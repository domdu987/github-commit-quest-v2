# QA s14 (film 18, render team 4)
Range g 1071-1135, take.mkv frames 1065..1141 (77 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 13.5 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 7.63, p90 11.86, min 1.23, max 14.61, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 694, "soldier0": 742, "soldier1": 730, "crowd0": 725, "crowd1": 722, "crowd2": 721, "crowd3": 722, "crowd4": 724, "crowd5": 719}

## Notes
- Rework after TAKE gate (QA-art FIX-FIRST): eye-level medium, general ~60 % of frame height; push 11 %/s + slide 55 px/s + sway; TWO HELD punch-ins (+14 % at g 1093, +12 % at the quote g 1112), no pulses.
- Lip-sync only from g 1113 (36.99 s): an overlay open mouth drawn BELOW the moustache (4 shapes, bigger than the moustache); before that a held open laugh. Warm tint + orange rim on the general; 3 Hz belly bounce.
- Navy faceted jars removed (party cups hidden, fg prop hidden); one brown-glazed jar with a warm light in the lower right corner; moon scaled to 60 %.
- p90 frame diff 11.9 (just under 12) because the pulses were removed as required.

See QA_AUTO.md and phone_sheet.jpg.
