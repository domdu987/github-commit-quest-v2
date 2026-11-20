# QA s10 (film 18, render team 3)
Frames g 737..852 in shot, take.mkv g 737..852 (116 frames, handle in 0, out 0); transition in: cut 0.
Render: 16.0 s wall / 24.7 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 737..852)
median **6.56**, p90 **8.88**, min 4.03, max 9.53  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 615, max 654 (rule < 880). PASS
- caption band y 880-950: mean max 56.400001525878906, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- director round 4: the pendulum is gone: one monotonic orbit-style drift of the camera position (no reversal) while the look-at stays on the general, on top of the set's eased 10 %/s push and -25 px/s slide; no pulses. Subject always in frame (head chin 615-654).
- mouth: closed 'dash' line outside speech; lip-sync (cast18.talk_mouth, new drawing every 2 frames) with openings enlarged so they read under the moustache, g 737..852 (quote 1b).
- clouds removed; caption band bright 0 %; bottom is dark lane ground with tents / lamp stands / spear racks behind (bare ground about 28 %).
- checked by eye: contact.jpg + phone_sheet.jpg.
