# QA s09 (film 18, render team 3)
Frames g 674..736 in shot, take.mkv g 674..736 (63 frames, handle in 0, out 0); transition in: cut 0.
Render: 11.4 s wall / 22.3 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 674..736)
median **8.87**, p90 **13.04**, min 4.38, max 15.13  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). PASS
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 725, max 749 (rule < 880). PASS
- caption band y 880-950: mean max 61.400001525878906, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths: closed 'dash' at g 674-675, cast18.talk_mouth lip-sync (mapped to visible openings under the moustache) g 676..736 only; soldiers constant laugh drawings.
- director round 2: subject kept in frame (general's head x 337..381 of 720 over the whole take, checked per frame; no look-at wobble, no lateral slide drift); camera = the set's eased push + a slow 0.7 Hz truck sway of the camera position while the look-at stays on the general (parallax, no zoom pulsing); clouds removed; caption band bright 0 %.
- checked by eye: contact.jpg + phone_sheet.jpg.
