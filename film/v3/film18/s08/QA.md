# QA s08 (film 18, render team 3)
Frames g 597..673 in shot, take.mkv g 588..673 (86 frames, handle in 9, out 0); transition in: dissolve 13.
Render: 11.7 s wall / 23.6 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 597..673)
median **6.31**, p90 **8.76**, min 1.81, max 10.24  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). FAIL
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 596, max 645 (rule < 880). PASS
- caption band y 880-950: mean max 66.69999694824219, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths: none move (quote 1 starts g 676): closed 'dash' mouth while he looks at Jimo, constant open laughing mouth from g 636 (belly bounce 0.06 D at 3 Hz, lean toggling); the two soldiers catch the laugh at g 642-648.
- set items applied: red slab (palisade / roof / rampart material b82c20) toned to #8a2a20 (linear), the cut beam top-left removed (wood faces in that corner deleted at start/mid/end poses), cloud sprites removed, the near brazier dimmed + its halo faces removed (it blew out the caption band at the shot start: bright share 31 % -> 0 %), fg spear rack kept. NOTE: the palisade post caps are dark navy flat-painted; they are part of the set's palisade mesh and could not be re-textured from the take.
- camera: the set's eased push + a 0.8 Hz lateral truck sway of the camera position with the look-at held on the general; he stays in frame (head x 349..372 of 720 in checks); no pulses; handle in g 588..596 (dissolve 13 = 6.5 + 2).
- **Frame-diff p90 is BELOW the 12 gate** (median passes). Bigger sway or push hid him behind the palisade rail / crashed the camera into the palisade in tests; no pulse was added (ALL_TEAMS rule 1). Needs the director's call.
- checked by eye: contact.jpg + phone_sheet.jpg.
