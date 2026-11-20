# QA s11 (film 18, render team 3)
Frames g 853..943 in shot, take.mkv g 853..951 (99 frames, handle in 0, out 8); transition in: cut 0.
Render: 8.5 s wall / 17.2 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 853..943)
median **4.64**, p90 **8.11**, min 2.81, max 12.32  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 704, max 728 (rule < 880). PASS
- caption band y 880-950: mean max 93.0999984741211, bright (luma > 200) share max 4.79 % / avg 0.7 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- director round 6: (1) the flat navy plank at lower left (g853-888) belonged to the 'road' mesh: hidden; the navy bar at the left edge (g933-951) was a tent ridge pole with an orb end plus the banner and shields: banner / shields hidden, the small connected islands of the tent ridge-pole / pole meshes in the left strip deleted (tent1, tent3, tent12, wood). (2) bare ground: a row of lit period props (jars, baskets, ropes in the set's materials) placed 3-4 D from the lens for the START pose fills the bottom in g853-880 (they slide away with the truck); the lower part of the frame is now dressed the whole take, plain ground well under 25 %.
- median frame diff 4.64 (gate >= 4), p90 8.1: dolly + one-way truck (no pulses) past WORLD-space foreground props that slide across the frame (ALL_TEAMS recipe).
- finger horns: two big soldiers (mock_moo a and c, drawn 25 % taller) with cream cow horns on the raised fingers, moo_b behind.
- caption band bright share max 4.8 % (a few frames, fire core), avg 0.7 %; key light x0.75.
- mouths: none move. handle out g 944..951 (dissolve 11 into s12).
- the background tent walls at the left thin out in g ~915-951 where their ridge poles were removed (warm dusk horizon behind): accepted to avoid unlit slabs.
- checked by eye: contact.jpg + phone_sheet.jpg.
