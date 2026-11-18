# s13 QA (render team 3)
- g 770..848 (79 frames, 776..842 + 6 handles each side), room_night / C, 12 samples, ~10 s/frame wall (2 threads).
- QA_AUTO: PASS (see QA_AUTO.md, phone_sheet.jpg). Max chin y 718 (< 880). No mouths (nobody speaks). Sore: blister overlay on James's upper_arm_l (11+ look).
- Checked contact sheet: candle prop in the mother's hand + set candle light, James in bed under quilt overlay, push-in moves every frame.
- Deviation: bed shot uses a custom camera (the preset room_night camera does not see the bed); the sore is an overlay in the sprite rather than a separate card.
- Gate fix 2026-11-18: camera raised to z 3.75 -> 3.55 looking down on the bed (James head ~100-130 px), sky/hills hidden behind the window (deep-blue plates), candle light x2.8, sore card hidden (QA-art). QA_AUTO PASS.
- Gate round 2: the upright patchwork square (my quilt overlay) removed (he lies on top of the quilt), curtains hidden, a deep-blue night pane outside the left window. QA_AUTO PASS.
