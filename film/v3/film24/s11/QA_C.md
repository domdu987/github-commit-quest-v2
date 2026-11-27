# s11 QA, look C (relight only, same shot.py, JOSEON_LOOK=C)
- Render: old g 1107-1262 (156 frames, 6 in-handle, 6 out-handle), 24 samples at 540x960 + J.post (C grade) -> 720x1280, about 67 s/frame wall with two lanes of 26-frame chunks.
- qa_auto: PASS (QA_AUTO_C.md). qa_jitter: overall median 0.13 px, no shake windows.
- Reviewed contact_C.jpg (every 6th frame): three ashigaru on j_near's bow with sword_raise, planted, backlit by the low sun with the Hinomaru banner lit from behind; the hull is dark against the sun, which is the intended backlight look, and a warm lantern pool appears late in the take.
- meta_C.json: shifted +208 as the plan says: g0 1321, g1 1465, first_g 1315 (old_g holds the render numbers 1113 / 1257 / 1107).
