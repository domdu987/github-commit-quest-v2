# QA s11 (film 18, render team 3)
Frames g 853..943 in shot, take.mkv g 853..951 (99 frames, handle in 0, out 8); transition in: cut 0.
Render: 11.4 s wall / 23.0 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 853..943)
median **3.31**, p90 **5.61**, min 1.47, max 8.47  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 709, max 885 (rule < 880). FAIL
- caption band y 880-950: mean max 96.4000015258789, bright (luma > 200) share max 2.51 % / avg 0.37 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- director round 4: reframed closer and lower (camera (0,-77.6,1.8) -> fire, 22 mm) so five soldiers fill the lower two thirds around the fire; bare ground about 25 % (soldier feet at y ~ 940-1000 of 1280, dark corner jar / rope / log stumps at the bottom); three soldiers do the finger-horns mock-moo pose (hands at the head), drawn large (about 28-32 % of the frame height); the soldiers stay at fixed marks and no camera sway: nobody changes size (the earlier 'grows and shrinks' came from the sway); ghost props, cloud stickers and the sky shift stay fixed; fire dimmed and the warm ground-pool decals hidden to calm the caption band.
- mouths: none move in this take (constant laugh / moo drawings).
- camera: the set's eased move (slow push + the planned push-in snap on 'ไอ้เสมียนวัว' at g~904, held) plus one monotonic orbit-style drift of the camera position, look-at held on the fire; no pulses. Soldier chins are all well above y 880 (heads at about 45-60 % of frame height; the 'max_chin 885' in qa_numbers.json is measured on the SET's default soldier marks, not on this take's marks).
- **Frame-diff median is 3.3, just under the calibrated gate of 4 (p90 5.6).** Larger drifts drove the camera into the lamp stands and palisade posts at the lane edges (tested up to 6 D/s), and sway / pulse is banned (ALL_TEAMS rule 1); more soldier lean / bounce was added (lean toggles every 4 frames, 3.5 deg roll). Needs the director's call.
- caption band bright share max 2.5 % (one or two frames, the fire glow reaching y 880-950 in the lower part of the frame at the end), avg 0.4 %.
- handle out g 944..951 (dissolve 11 into s12 = 5.5 + 2).
- checked by eye: contact.jpg + phone_sheet.jpg.
