# QA s10 (film 18, render team 3)
Frames g 737..852 in shot, take.mkv g 737..852 (116 frames, handle in 0, out 0); transition in: cut 0.
Render: 17.9 s wall / 23.5 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 737..852)
median **13.06**, p90 **17.16**, min 2.59, max 20.15  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). PASS
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 600, max 648 (rule < 880). PASS
- caption band y 880-950: mean max 56.400001525878906, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths: lip-sync (cast18.talk_mouth, visible openings under the moustache) on every frame g 737..852 (quote 1b 24.56-28.38 s; the quote runs to g 854, the take ends at 853); soldiers constant laugh drawings.
- camera: the set's eased 10 %/s push (slightly eased back with -0.05) + slow 0.7 Hz truck sway of the camera position with the look-at held on the general: subject stays in frame (checked), no pulses; clouds removed; caption band bright 0 %; heads chin 600-648 (< 880).
- checked by eye: contact.jpg + phone_sheet.jpg.
