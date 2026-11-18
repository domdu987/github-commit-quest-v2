# QA s10 (film 13, shots 10 + 11), rework after QA-tech FAIL
- Frames g 585..731 (147; g0 591, g1 726; 6 in/out handles), 720x1280, 12 samples, ~12-18 s wall per frame. take.mkv 43 MB (single file).
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg), 0 % magenta, no frozen/black frames. All heads above y 880 (rich chin < 700).
- Fixes vs the failed take: 
  1. Shot 10 staged in the suite with the red armchair and the window: he sits with cup + saucer, looks out of the window (head/eyes turned to screen-left), hears (surprised, g 604-611), turns to us and laughs with a CLOSED mouth (grin, squeezed eyes, tears, belly shake) from g 612. talk_mouth only for g >= 649 (Q1 21.68 s - 0.15 s); flat/closed everywhere before.
  2. Cup continuity: cup + saucer stay in his left hand into shot 11 (the table cups were removed at runtime).
  3. Shot 11: he stands at the window, head turned and eyes down, pointing DOWN and out with the right arm toward the street, camera looks down 25 deg over his shoulder; Pullman is far below (see deviation).
  4. Chandelier: kept out of frame except a small arm at the right edge in shot 10 (camera moved to the right of the chair); not present in shot 11.
- Runtime set edits (from shot.py): the 3D armchair and the tea table cups are collapsed to a point under the floor (bmesh delete hangs on that mesh).
- Deviation: from inside the room the street cannot be seen (the room floor hides every line of sight steeper than ~29 deg), so Pullman stands at (4.5,-54) at scale 2.4 so that he reads as a tiny figure far below (head ~25 px), right of the rich man's belly. Cut convention (cuts at round(t*30), G1) unchanged as the director decided.
- take.mkv single file (43 MB < 45).
