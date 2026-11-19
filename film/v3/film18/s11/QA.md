# QA s11 (film 18, render team 3)
Frames g 853..943 in shot, take.mkv g 853..951 (99 frames, handle in 0, out 8); transition in: cut 0.
Render: 13.3 s wall / 22.9 s cpu per frame (two processes at once, 2 threads each, 12 samples, 720x1280)

## Frame diff (90x160 grey, mean abs diff x255, consecutive frames, in-shot g 853..943)
median **12.82**, p90 **17.47**, min 7.30, max 20.93  (gate: median >= 4, p90 >= 12; film 2: 5.3 / 19.1). PASS
Camera = the set's planned move (jimo_shots.pose_at) plus c18.make_mod: extra push, lateral slide, handheld sway and look-at wobble (params in shot.py PARAMS); characters bounce 0.06 D at 3 Hz, lean toggles, small sway.

## Numbers
- chin (head bottom) y over all frames incl. handles: min 599, max 819 (rule < 880). PASS
- caption band y 880-950: mean max 107.80000305175781, bright (luma > 200) share max 0.23 % / avg 0.01 %.
- qa_auto: see QA_AUTO.md (phone_sheet.jpg).
- mouths: no lip-sync anywhere in this take; constant laugh / moo mouths only (quote 2 is at 36.99 s).
- set items: cloud base bars shortened; foreground: the set's jar (left) + a coiled rope (bottom-right) + 11 ground props (hay, basket, pot, rope, silk, stone) in the lower third; soldiers use 6 different poses (mock_moo a/b/c, laugh_point b/c, cheer_cup a) with staggered bounce phases and lean toggling; camera tilted up 0.3 D to shrink bare ground.
- handle out g 944..951 (dissolve 11 into s12 = half 5.5 + 2). Caption band bright share max 0.23 % (one frame, fire edge).
- checked by eye: contact.jpg + phone_sheet.jpg; a soldier passes close to the lens in the last 20 frames (big laughing face, heads still above y 880).
