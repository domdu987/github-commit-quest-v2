# QA s09 (film 18, render team 3)
Frames g 674..736 in shot, take.mkv g 674..736 (63 frames, handle in 0, out 0); transition in: cut 0.
Render: 11.8 s wall / 23.1 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 674..736)
median **14.84**, p90 **20.79**, min 5.50, max 22.98  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). PASS
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 628, max 752 (rule < 880). PASS
- caption band y 880-950: mean max 60.900001525878906, bright (luma > 200) share max 0.0 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths: lip-sync (cast18.talk_mouth, hold 2) only g 676..736 (quote 1a starts 22.45 s = g 676); g 674-675 flat. Soldiers: constant laugh drawings, no mouth change.
- set items: cloud base bars shortened (patched sky texture); caption band clear (was 1.82 % bright in the set report; camera tilted down).
- checked by eye: contact.jpg (12 frames) + phone_sheet.jpg.
