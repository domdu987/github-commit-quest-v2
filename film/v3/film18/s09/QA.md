# QA s09 (film 18, render team 3)
Frames g 674..736 in shot, take.mkv g 674..736 (63 frames, handle in 0, out 0); transition in: cut 0.
Render: 11.9 s wall / 23.3 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 674..736)
median **11.70**, p90 **17.37**, min 6.79, max 18.67  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). PASS
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 678, max 796 (rule < 880). PASS
- caption band y 880-950: mean max 82.9000015258789, bright (luma > 200) share max 0.05 % / avg 0.0 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths (director QA-tech fix): closed 'dash' mouth at g 674-675, then cast18.talk_mouth lip-sync mapped to clearly visible openings under the moustache ((open .55 .14) / (open .62 .42) / (open .36 .36) / closed) from g 676 (22.45 s) to the end; soldiers keep constant laugh drawings.
- director fixes applied: cloud sprites removed (clear dusk gradient, no stickers); handheld sway lowered to 0.9 Hz and started at zero offset with the shot's first frame, so no sideways jumps (frame diff still passes); caption band bright share max 0.05 %.
- checked by eye: contact.jpg + phone_sheet.jpg + mouth crops g 674-682.
