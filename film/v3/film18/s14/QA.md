# QA s14 (film 18, render team 4)
Range g 1071-1135, take.mkv frames 1065..1141 (77 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 22.7 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 7.71, p90 11.98, min 1.25, max 14.8, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"general": 694, "soldier0": 742, "soldier1": 730, "crowd0": 725, "crowd1": 722, "crowd2": 721, "crowd3": 722, "crowd4": 724, "crowd5": 719}

## Notes
- Rework after TAKE gate (QA-art FIX-FIRST): eye-level medium, general ~60 % of frame height; push 11 %/s + slide 55 px/s + sway; TWO HELD punch-ins (+14 % at g 1093, +12 % at the quote g 1112), no pulses.
- Lip-sync only from g 1113 (36.99 s): an overlay open mouth drawn BELOW the moustache (4 shapes, bigger than the moustache); before that a held open laugh. Warm tint + orange rim on the general; 3 Hz belly bounce.
- Navy faceted jars removed (party cups hidden, fg prop hidden); one brown-glazed jar with a warm light in the lower right corner; moon scaled to 60 %.
- p90 frame diff 11.9 (just under 12) because the pulses were removed as required.
- Round 4: the fg jars now use a toon-glazed material (dark outline ramp, warm centre) instead of flat tan.

See QA_AUTO.md and phone_sheet.jpg.


## V2 (client fixes: no camera shake / nothing floats)
- Camera: NO sway / shake / pulses. One smooth eased dolly + an ORBIT truck (camera moves sideways, look-at stays on the general, so he never leaves the frame) with ONE/TWO held punch-ins eased over 10 frames. Bounce 0.02 D at 1.8 Hz (was 0.06 D at 3 Hz); the carving hand-saw is 2 Hz. Set tents are built 0.4 D into the ground (sunk, counted as planted).
- take.mkv crf 21, first_g 1065, 77 frames; transition in: {'type': 'cut', 'frames': 0}.
- frame diff (90x160 grey, in-shot): median 4.26 / p90 6.51 (rule: median >= 4).
- ground_check (film/v3/tools/ground_check.py through film18/gc_run.py, every 6th frame): - checked objects: 26   rows: 312   FAIL rows: 0   **result: PASS**  (full table in GROUND.md; cards are checked by bounding box, so only a floating card base can fail; shadows are the cards' contact quads).
- qa_jitter output:
```
overall median jitter px 0.32
```
