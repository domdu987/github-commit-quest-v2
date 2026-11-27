# s07 QA, look C (relight only, same shot.py, JOSEON_LOOK=C)
- Render: 24 samples at 540x960 + J.post (C grade) -> 720x1280, g 638-739 (102 frames, 6 in-handle, 6 out-handle), ~55 s/frame wall. Rendered in 34-frame chunks (shot.py final takes the range as argv[2]).
- qa_auto: PASS (QA_AUTO_C.md). qa_jitter: overall median 0.55 px (the camera move plus the hip bounce), no shake windows listed.
- Reviewed contact_C.jpg (every 6th frame): three different ashigaru laughing and pointing on flag_deck_crew, feet planted, backlit by the low sun with a warm lantern pool; the deck is darker than in B, which is the intended sunset look.
- meta_C.json: g0 644, g1 734, first_g 638 (unchanged, no shift).
