# s12 QA: film 24, shot 12 (sea board): soldiers at the rail look at the spikes, then step back

Delivered: `take.mkv.partaa/ab` (cat them to get take.mkv; libx264rgb crf 6, 30 fps, first_g 1251, 168 frames g 1251..1418, 54.5 MB split 40M),
`meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` + `phone_sheet.jpg` (qa_auto PASS), `shot.py`, `deliver.py`. g 1257..1412 = shot 12 (41.91-47.10 s),
6 in-handle + 6 out-handle frames rendered in 3D. Hard cuts at both ends.

| rule | how / measured |
|---|---|
| nothing floats, contact shadow | 3 cards Child-Of the j_board ride, decal laid on the deck, sun shadow; soles on the planks (strip work/step.jpg) |
| no shake, one eased move | preset board camera moved 30 % toward board_end (look point 14 %), eased (0.35 sine + 0.65 linear), following the fleet; qa_jitter median 0.11 px |
| never static > 6 frames | qa_auto: none |
| nothing parented to camera | camera unparented; the set's own ladder and rail are world objects |
| walk, no sliding | ashi_c24 steps back from g 1389 ("มีแต่เหล็กแหลม") over 24 frames with the reversed walk cycle (0.8 D, step_back expression); the other two are planted (max screen step 1.65 / 2.02 px/frame = camera only; c max 4.6 px in the walk) |
| no duplicate characters | ashi_c24 (peer/step back), ashi_b24 + ashi_d24 (ladder pair): three different members, sizes and poses |
| near bigger than far | head w b 125-133 > c 107-117 (farther along the rail); d is nearest to the camera edge, 144-153 |
| heads above y 880 | head bottoms max 456 px |
| sharp | DOF off |
| mouths | no quote: fixed expression mouths |
| tone | sweat drops only, no injury |

Set state keyed each frame: special 'board', set_spikes 3, set_ports 0, fleet chase s=(g-1251)/30, korean_turn 0, damage 0, cannon smoke 0.
Deviations from the plan: ONE soldier (ashi_c24) steps back (plan: 1-2); the ladder pair stays planted (the walk cycle has no ladder variant);
the push stops at 30 % of the preset's board_end move (the full move pans the camera off the soldiers onto bare roof); the preset's 3 soldier
spots were rearranged (c / b / d on the rail) so nobody is cut by the 9:16 frame. Render 35.2 s wall / 68.0 s cpu per frame.
