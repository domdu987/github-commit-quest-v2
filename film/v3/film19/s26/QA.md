# s26 QA: film 19, shot 26 (HALL EVENING), after the QA-art / QA-tech fix round
- take.mkv: g 2077..2159 (83 frames), shot g 2086..2159; transition in: cut.
- The money bag falls and bounces onto the tabletop at g 2107 (1.35x, squash on landing); Harrison stands behind the table edge, looks down at the bag, then up at the lens and grins, with the H4 in his left hand; the King nods (2x nods); orbit camera ends with Harrison, bag and King in frame, moving at the cut (g 2159, film end, N = 2160). Known: bag 1.35x not 1.8x (1.8x covered Harrison's face), bag stays brown (no coin hooks in the set), tie not turned to camera; median 3.95 (target 4), p90 5.9; the King's head may touch the right edge in the last frames.
- Rules: no DOF, no text, no caption_shade; set hooks keyed every frame; samples 8; heads in shot (px): {"har": {"w": [184, 232], "y": [516, 544], "x": [152, 332], "bottom_max": 644}, "king": {"w": [97, 134], "y": [484, 494], "x": [442, 668], "bottom_max": 552}}
- qa_auto: see QA_AUTO.md + phone_sheet.jpg. Contact sheet checked at full size.
- s/frame wall 17.13 (2 procs x 2 threads, some frames rendered while a second job ran), cpu 33.51.
- Frame-diff in shot (90x160 grey): median 3.95, p90 5.91 (target 4 / 12).
