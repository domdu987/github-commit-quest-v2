# QA s08 (film 18, render team 3)
Frames g 597..673 in shot, take.mkv g 588..673 (86 frames, handle in 9, out 0); transition in: dissolve 13.
Render: 13.6 s wall / 26.3 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 597..673)
median **4.08**, p90 **4.38**, min 2.98, max 5.59  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 609, max 612 (rule < 880). PASS
- caption band y 880-950: mean max 56.599998474121094, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- director round 4 (all done): red slab = the palisade gate lintel (b82c20 faces at z >= 7.9): removed (its cut ends go with it); remaining b82c20 trim toned (linear #8a2a20 x0.35 for the dusk gain); the grey-navy lump (fire-ring stones 'firestone') and the bare stump ('logs') hidden; reframed (camera (1.8,-53.2,4.7) -> general, 24 mm): general about 30 % of the frame height, full body above the rail, never behind it; sky about 30 %.
- mouths: none move (quote 1 is at g 676); closed 'dash' while he looks at Jimo, constant open laugh from g 636 with 0.06 D / 3 Hz bounce; soldiers catch the laugh g 642-648.
- camera: the set's eased 8 %/s push + a one-way orbit-style drift of the camera position (look-at held on the general; no reversal, no pulse). Subject stays centred (head chin 609-612).
- frame diff passes the calibrated gate (median >= 4).
- earlier set items kept: clouds removed, near brazier dimmed (no caption-band flare); caption band bright 0 %.
- checked by eye: contact.jpg + phone_sheet.jpg.
