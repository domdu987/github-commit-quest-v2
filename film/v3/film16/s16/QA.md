# s16 QA: film 16, shot 16 (trench cut-away), LINE trench_cut / DUSK
- take.mkv: g 998..1083 (86 f; shot = g 1007..1074 = 33.57-35.82 s; 9 handle frames each side), 720x1280, 7 spp, 2 threads, 12.4 s wall / 24.3 s cpu per frame.
- Hard cut in and out (transition_in cut 0). No characters, no mouths, no text, no DOF.
- Camera (c16.CamPath): whip-tilt dive from above the pit into the elevation view (g 999..1028), push 9 %/s + slide 90 px/s carrying the split from left of centre across the frame, snap x1.9 on "ไฟรั่วหายลงดิน" (g 1050..1063). Split sits at ~43-48 % of the frame height while the pit floor is cut by the push (QA_ART note handled). Leak keyed per frame.
- Frame-diff in-shot (90x160 grey): median 3.98, p90 10.48 (target 4 / 12): flat soil texture; slightly below target.
- qa_auto: FAIL "suspected blur" on g 998..1011 only = the fast tilt of the whip dive (handles + first 5 shot frames); intentional motion, the soft painted ground. Nothing else; cut-change note is expected (neighbours are other takes).
- Checked at 6 fps (contact.jpg): split, copper wire, rags and cyan drips read, no heads/captions concerns, no stray props.
