# QA s22 (film 18, render team 4)
Range g 1683-1741, take.mkv frames 1677..1747 (71 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 15.1 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 6.85, p90 10.34, min 2.05, max 20.39, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"hero": 721, "soldier": 694}

## Notes
- Hero ox: front-3/4 startled dragon card, flame drawings flicker every 2 frames, whole head + both blades inside the frame (right blade margin > 100 px), tail flame visible; 10 background gallop oxen.
- Frozen soldier (coloured card, sweat + O mouth) kept apart on the left, carried with the camera (position scaled with the snap zoom) so he never leaves the frame.
- Camera: push 9 %/s, slide 22 px/s, sway, 3 punch-ins homing on the ox (last on "วาววับ", 57.64 s). Mouths do not move.
- Re-render after TAKE gate rules: zoom pulses removed, only held punch-ins (s21: +12 % then the x1.4 held snap on the word; s22: two held +12 %). Frame-diff from push, slide, sway and herd motion.

See QA_AUTO.md and phone_sheet.jpg.
