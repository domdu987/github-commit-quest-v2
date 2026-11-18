# Render-team worker brief, film 11 (ไอ้หมอวัว: Jenner, cowpox, 1796)

Follow film/WORKER.md exactly: section 1 setup (PROJ symlink to the repo's film/), section 4 delivery, section 5 rules. Film 11 differences:

## Inputs
- Story + look: PROJ/film11/BRIEF.md. Shots: PROJ/film11/shot_plan.md (28 shots; you own only the takes your launch message names).
- Narration PROJ/film11/audio/narration.wav (62.38 s) at +0.10 s. Captions PROJ/film11/script/captions.json. N = 1875, g = round(t*30).
- Take = one shot; take folder PROJ/v3/film11/sNN (NN = shot number, 2 digits).

## Set (client-approved 2026-11-18): PROJ/v3/set3d11/dairy.py
Read PROJ/v3/set3d11/API.md first (incl. "Round 2 changes"), then QA_TECH.md and QA_ART.md. Presets: barn_wide, barn_milking, barn_high,
barn_door, garden_hut, lane_wide, lane_high, garden_queue, room_day, room_night, room_morning. Light A everywhere except C on barn_high and
room_night (candle). Use the named stand points (contact z) from API.md; replace every placeholder card and the 3D Blossom marker with real
cast11 cards. Hooks are driven by frame: key/set them on every frame. Do NOT edit dairy.py; per-shot changes go in your shot.py at runtime.
Colour limits per frame: shade hue 240-260, magenta <= 10 % (barn_wide/barn_high are near the limit: do not add pink/violet).
Never re-enable the shaft planes (SHAFTS stays False).

## Cast: PROJ/v3/cast11 (read API.md)
jenner, james (+ james_horns gag, horns/cow_ears keys), sarah, milkmaid2, towndoc, mother, villager_a..e (a/b/c pockmarked), blossom (cow11).
Poses in STORY11; canvases CANVAS11, CANVAS11_LIE (james in bed), CANVAS11_YOKE. Milking: plant sarah_milk on Blossom's milker_feet anchor,
pail on pail_spot. jenner_scratch_arm: adjust arm_r hand until lancet_r meets james upper_arm_l. james_in_bed needs the set's bed + quilt
over him. Mouths: mouth=cast11.talk_mouth(g) ONLY for the towndoc inside 14.84-18.10 s and 28.21-29.85 s; still everywhere else.

## Worked example and helpers
Worked example: PROJ/v3/film8/s01/shot.py + QA.md and PROJ/v3/film8/common.py (moves must move, key every hook every frame, one location
per process). Make your OWN helper in your take folder (e.g. PROJ/v3/film11/sNN/c11.py) by copying film8/common.py and switching it to
cast11 + set3d11/dairy.py. No shared film/v3/film11/common.py.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
Run `python3 film/qa_auto.py take.mkv --first_g <first_g> --cuts <your cut g's>`, fix every FAIL, add QA_AUTO.md + phone_sheet.jpg.
Then check every frame yourself at 6 fps plus cuts ±3: heads above y 880, contact shadows, props in hands, eye-lines, continuity, mouths only
in the quote windows, the sore card on the arm consistent (none before shot 2; red dot shots 2-10; blister 11+).
The director's QA-tech re-checks every take; QA-art reviews key takes (1-2 hook, 13-15 false payoff, 21-23 reveal, 26-28 ending).

## Delivery
meta.json: g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n} (dissolve 8 where the plan says D). Render 6 handle
frames each side. take.mkv over 45 MB -> `split -b 40M take.mkv take.mkv.part`. Commit only your take folders, push to your own branch as
soon as each take is final. No pull requests. Work autonomously: the client has approved the set, the cast and the render.
