# s10 QA: film 24, shot 10 (sea flag_bow): the commander shouts from the flagship bow

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 996, 123 frames g 996..1118, 31.8 MB), `meta.json`, `cues.json`, `contact.jpg`
(16 frames, cyan = y 880), `QA_AUTO.md` + `phone_sheet.jpg` (qa_auto PASS), `shot.py`, `deliver.py`. g 1002..1112 = shot 10 (33.40-37.09 s),
g 996..1001 in-handle, g 1113..1118 out-handle (same 3D, push and chase go on). Hard cuts at both ends.

| rule | how / measured |
|---|---|
| nothing floats, contact shadow | jp_cmd24 card Child-Of the jflag ride at `commander_bow` (deck), contact decal laid on the deck, sun shadow; feet on the planks (checked full-size crops of the sheet) |
| no shake, one eased move | preset flag_bow camera pushed 9 % along its view line (0.35 sine + 0.65 linear) and travelling with the fleet; qa_jitter median 0.12 px, no shake |
| never static > 6 frames | qa_auto: no frozen runs (camera, swell and fleet move every frame) |
| nothing parented to camera | camera unparented |
| feet planted | one point keyed every frame, screen path moves only with camera/swell (max 1.87 px/frame) |
| no duplicate characters | one figure (jp_cmd24_shout_forward, gunbai) |
| heads above y 880 | head bottom max 778 px, centre y 704-734; head width 82-92 px (no face fills the frame) |
| characters sharp, DOF | DOF off |
| mouths | talk_mouth only g 1047..1111 (34.81-37.0 s quote "เห็นไหม เต่ากลัวแล้ว! ตามไปให้หมด!"); flat before/after |
| hard cuts | transition_in/out cut; qa_auto sees no pop |
| tone | no injury, no fire |

Set state keyed every frame: set_spikes 3, set_ports 0, set_korean_turn 0, set_fleet_chase (g-996)/30, damage 0, cannon smoke 0.
Continuity: shot 9 (hansan_high, Korean ships flee) -> this deck close-up -> shot 11 (chase on j_near's bow).
Deviation: the flagship deck is only the preset's; no extra crew in frame (plan: "the fleet behind" = ships far behind the commander).
Render: 29.7 s wall / 54.1 s cpu per frame (2 procs x 2 threads, 24 samples).
