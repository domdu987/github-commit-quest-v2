# QA s11 (film 18, render team 3)
Frames g 853..943 in shot, take.mkv g 853..951 (99 frames, handle in 0, out 8); transition in: cut 0.
Render: 8.9 s wall / 18.0 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 853..943)
median **4.13**, p90 **8.24**, min 1.88, max 11.72  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 704, max 728 (rule < 880). PASS
- caption band y 880-950: mean max 93.4000015258789, bright (luma > 200) share max 4.8 % / avg 0.7 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- director round 5: median 4.13 (gate >= 4), p90 8.2. Camera per the ALL_TEAMS recipe: a dolly (set camera + plan push 7.5 %/s, held +10 % snap on 'ไอ้เสมียนวัว' g~904) and a one-way sideways truck of the camera position (look-at held on the fire; no reversal, no pulse) with WORLD-space foreground props (jar, rope, basket 2.8 D from the lens, plus a row of jars / baskets / ropes 4-6 D away) that slide across the frame.
- two big soldiers (mock_moo a and c; moo_b behind) with the raised fingers painted as cream cow horns, cards drawn 25 % taller: the finger-horns read on the phone sheet. Soldiers sit on fixed marks, no sway: nobody changes size except through the planned dolly.
- bare ground: the lower part is filled by the fire ring, soldiers and the prop row; plain ground at the very bottom is about 25 % (up to ~33 % in the first ~25 frames while the truck starts from the left; filled from g ~880).
- the dark post at the left edge: the small connected islands of the tent-pole mesh that project into the left strip were deleted; a small dark flag remnant still shows at the top-left in the out-handle g 944..951 (dissolved away).
- caption band (y 880-950): key light x0.75 and the camera tilt eased back: bright share max 4.8 % (a few frames when the fire core crosses the band), avg 0.7 %. (qa_numbers.json head chins are measured on the set's default soldier marks; the take's soldier heads are at about 45-60 % of the frame height.)
- mouths: none move (constant laugh / shout drawings).
- checked by eye: contact.jpg + phone_sheet.jpg.
