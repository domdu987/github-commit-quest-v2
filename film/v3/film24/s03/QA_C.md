# s03 QA, look C (relight only, same shot.py, JOSEON_LOOK=C)
- Render: 24 samples at 540x960 + J.post (C grade) -> 720x1280, g 145-293 (149 frames, 6 in-handle, 7 out-handle), ~52 s/frame wall with two processes running.
- qa_auto: PASS (QA_AUTO_C.md). qa_jitter: overall median 0.12 px, no shake windows.
- Reviewed contact_C.jpg (every 6th frame): fleet sails +x with a slow lateral slide, low warm sun behind the fleet, lavender water with amber glitter, no floating hulls, no smoke or characters in the shot.
- meta_C.json: g0 151, g1 288, first_g 145 (unchanged, no shift). Frames rendered in 10-frame chunks (pose cost grows with range length).
