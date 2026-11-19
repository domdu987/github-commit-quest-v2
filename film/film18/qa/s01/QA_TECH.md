# QA_TECH s01 (take g0-77, 78 frames) - FAIL
Checked: 6 fps frames + first/last 3 (s01/qf/), re-measured framediff from take.mkv (90x160 grey): median 6.26, p90 9.55 (min 1.25, max 11.06).
1. whole take - camera: p90 9.55 < 12 (rule median>=4 AND p90>=12). Fix: re-render with larger punch-in snaps (the team's own QA.md admits the miss) so p90 >= 12.
2. g70-77 (f076/f077) - framing: Tian Dan drifts to the right edge; his torch-side arm and the fg torch are clipped at x=720 and his head sits against the edge. Fix: re-aim look_at so he stays centred/inside 60 px of the edges.
3. g0-77 - eye-line: Tian Dan looks at the lens with a frown, not at the ox he is dressing; reads as posing, not tugging. Fix: turn the face card toward the ox or add a glance card on the tug beats.
4. g0-77 - hook read: only 4-7 dressed oxen visible; "พันกว่าตัว" is carried by the audio only. Non-blocking; a longer row to the vanishing point would help.
Pass items: heads/chin <= y 840 (<880); caption band y880-950 mean max 72.6, bright(>200) 0.00 %; no mouths moving; no text; dragon-dressed oxen with short blades (continuity OK for s01); NIGHT; contact shadows weak but present; no frozen/black frames; g range 0-77 matches plan.
