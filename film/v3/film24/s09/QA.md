# s09 QA: film 24, shots 9a + 9 (sea macro_oar, hansan_high)

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 913, 95 frames g 913..1007, 22.2 MB), `meta.json` (g0 919, g1 1002 = exclusive), `cues.json`,
`contact.jpg`, `QA_AUTO.md` + `phone_sheet.jpg` (qa_auto PASS with --cuts 954), `shot.py`, `deliver.py`.
g 913..918 in-handle (9a), g 919..953 = shot 9a (30.64-31.80 s), HARD CUT g 954, g 954..1001 = shot 9 (31.80-33.40 s), g 1002..1007 out-handle (shot 9 continues).
Two builds (internal ids 9 and 19): macro_oar (special solo) and hansan_high.

| rule | how / measured |
|---|---|
| nothing floats | no people; the turtle ship hull sits in the water (set's swell driver) |
| no shake, one eased move | 9a: one lateral slide 1.1 D (0.35 sine + 0.65 linear); 9: 8 % push along the view line; qa_jitter median 0.14 px, no shaky second |
| never static > 6 frames | qa_auto: none (swell, splash, oars move every frame) |
| nothing parented to camera | focus empty is world-fixed at the preset look_at (9a); camera unparented |
| DOF | only 9a (preset f/2.8, 12 samples); shot 9 sharp |
| characters / mouths / heads | none in these shots |
| hard cuts | cut at g 954 inside the take (qa_auto sees it, no ghost); in/out cuts |
| tone | spray and foam only |

Set state keyed every frame: 9a special 'solo', set_oar_splash t = ((g-922) mod 24)/15 (splash for 15 frames, then 0; first dip g 922, next g 946),
fleet chase 0, korean_turn 0; 9: special '', korean_turn 0 (Korean ships flee ahead, +x as in the set API), set_fleet_chase (g-954)/30.
Notes / deviations: the set makes the Korean fleet flee +x (the plan says -x); in the high wide the ships are small (30-60 px) as the set API warns;
the splash foam patches stay on the water between dips (set behaviour). Render: 9a 34.0 s wall / 64.5 cpu, 9 24.7 s / 46.4 cpu per frame.
