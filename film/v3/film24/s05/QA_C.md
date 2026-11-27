# s05 QA, look C (shots 5 + 6, relight only, same shot.py, JOSEON_LOOK=C)
- Render: 24 samples at 540x960 + J.post (C grade) -> 720x1280, g 425-649 (225 frames, 6 in-handle, 6 out-handle), ~52 s/frame wall.
- Shot 5 (425-512) and shot 6 (513-649) were rendered in two processes (a second build in one process crashes in look C); hard cut at g 513.
- qa_auto: PASS with --cuts 513 (QA_AUTO_C.md). qa_jitter: overall median 0.24 px, no shake windows.
- Reviewed contact_C.jpg (every 6th frame): sun-side rim on jp_cmd24 and the rigging shadow pattern on the deck, ashigaru behind him in shot 5, backlit flag deck with sea glow in shot 6, feet planted with contact shadows, heads clear of the caption band. Mouth: closed before 16.1 s, lip-sync only in shot 6 as in the B take.
- meta_C.json: g0 431, g1 644, first_g 425 (unchanged, no shift).
