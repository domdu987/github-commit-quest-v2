# QA s10 (film 13, shots 10 + 11), self-check
- Frames g 585..731 (147; g0 591, g1 726; 6 in/out handles), 720x1280, 12 samples, ~12.5 s wall / 24.5 s CPU per frame.
- qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg); planned cut 650 detected; no frozen/black/pop frames; magenta 0 %.
- Checked at ~6 fps + cut 647..653: rich head chin y <= ~600 (limit 880); cards stand on the carpet with contact shadow; cup+saucer stay in his left hand through the laugh; no text.
- Mouth: laugh pose (own held mouth) in shot 10; talk_mouth only for g >= 649 (Q1 21.68 s - 0.15 s); 'flat' before. Shot 11 mouth runs to the end of the take (inside Q1).
- Cameras always move (push ~2.5 D in shot 10, push+orbit in shot 11); no DOF.
- Deviations from the plan: shot 10 uses a camera looking from the window into the room (chandelier, armchair, paintings) with the rich man standing, instead of suite_window/armchair seated; shot 11 is an interior medium of him pointing down toward the street (pullman is not visible from inside; he appears in shot 12). The laugh is a one-frame pose swap with a squash pop at g 612.
- Known: sprite pose swap at 612 (smug -> laugh) is abrupt by design (burst).
- take.mkv is split in take.mkv.part* (cat them to rejoin).
