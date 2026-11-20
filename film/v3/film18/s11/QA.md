# QA s11 (film 18, render team 3)
Frames g 853..943 in shot, take.mkv g 853..951 (99 frames, handle in 0, out 8); transition in: cut 0.
Render: 12.6 s wall / 24.0 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 853..943)
median **5.99**, p90 **7.89**, min 1.95, max 10.16  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 567, max 701 (rule < 880). PASS
- caption band y 880-950: mean max 92.5999984741211, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths: none move (quote 2 is elsewhere); constant laugh / moo drawings.
- director round 1+2 fixes: ghost ground props removed (only the set's jar + a coiled rope in the corners); clouds removed; sky stays dusk the whole shot (camera held level, dz -1.0); caption band bright 0 %; two big mock-moo soldiers (mock_moo a and c, drawn 12 % taller) in front of the fire plus a third moo soldier, laugh_point and cheer_cup variants behind; soldiers look at the camera/fire group.
- camera: set camera s11 (wide pull-out + the planned push-in on 30.64 s) + a gentle 0.9 Hz vertical bob; no lateral slide because the right side of the lane is blocked by a brazier / palisade (a lateral truck hit them in tests). **Frame-diff p90 is BELOW the 12 gate** (median ok): the wide shot has little parallax without a truck; the push-in snap and actor bounce carry the numbers. Needs the director's call (no pulse added, per ALL_TEAMS rule 1).
- checked by eye: contact.jpg + phone_sheet.jpg.
