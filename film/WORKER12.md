# Render-team worker brief, film 12 (ไอ้ร่มเดินได้ — Jonas Hanway's umbrella, London 1750s)

Follow film/WORKER.md exactly: section 1 setup (the PROJ symlink; bpy 5.x needs `pip install bpy` for the default python3),
section 4 delivery, section 5 rules. The film-12 differences are below and override WORKER.md.

## Inputs
- **Brief and shots:** PROJ/film12/BRIEF.md and PROJ/film12/shot_plan.md (23 shots, the ONLY plan; follow it shot by shot).
- **Look (client rules):** wide or medium framings that show the dense rainy street, a calm camera that is always moving (never static
  > 6 frames, a new framing every 1.5-2.5 s), warm amber windows vs blue-violet rain shade. SHARP, NO depth of field, NO text anywhere.
- **Narration:** PROJ/film12/audio/narration.wav (59.0 s), placed at +0.10 s. **Captions:** PROJ/film12/script/captions.json.
- **Frames:** 30 fps, 720x1280, N = 1785. Shot boundaries t0/t1 from the plan fall on g = round(t*30); in-shot events tied to
  narration fall on g = round((t+0.10)*30).
- **Sentence starts (s):** hook 0, pivot 5.75, boss 10.51, nickname 19.07, count 21.69, false 28.61, reveal 34.98, aha 44.66,
  ending 52.64, end 58.99.

## Set (client-approved 2026-11-18): PROJ/v3/set3d12/street.py
READ PROJ/v3/set3d12/API.md completely first (presets, lights RAIN / DUSK_RAIN, the 27+ stand points, hooks, gotchas, weak points),
then QA_TECH.md and QA_ART.md in the same folder. Look at contact.jpg: tiles 01-25 are the approved framings; match them.
- Presets: street_wide, street_wide_low, street_wide_rev, street_high, coach_low, coach_close, hero_track, box_seat, box_trio, market,
  puddle_low, rank_rush, rank_wide, rank_idle. Cameras have pose A and B; `S.key_camera` keys the move.
- Hooks (pass frame=N to key, key EVERY animated hook on every frame it changes): set_crowd_umbrellas, set_rush, set_rank_busy,
  set_pink_umbrella, pink_to_hand, rain, throw('cabbage'|'egg', ...), mud_splash, run_coach, roll_rank, crowd_figures,
  cast_card / stage_cards / stage_rush_cards (real cast12 cards with amber rim and tint).
- The tile-render script PROJ/v3/set3d12/street_work/render_tiles.py shows how each approved tile was staged: copy its staging.
- Samples: final 20 (24 on puddle_low and other puddle-heavy shots), OIDN denoise as in the set. Cost about 16-34 s wall per frame
  at 2 threads. Never edit the set module; change things at runtime from your shot.py.

## Cast: PROJ/v3/cast12 (read API.md)
Keys hanway, coachman (head coachman, the mocker), coachman_b, coachman_c, crowd_man_a-d, crowd_woman_a/b, passenger_a/b; 111 poses
in STORY12; props: black umbrella, pink lace umbrella (use the 3D one from the set at the ending, not the sprite), whip, cabbage12, egg,
purse; fx mud / soaked / egg_splat. Seated coachmen stand on the 3D coach plank; NEVER use coach_box=1 on a 3D coach.
Replace the set's blocky placeholder people with cast12 cards wherever a person is readable (foreground and mid-ground).

## Mouths and acting
- Mouths move ONLY on the head coachman's quotes: boss quote 12.66-19.00 s ("ผู้ชายกางร่มเหรอ! ... ของเมียข้าเอง!") and false quote
  33.00-34.95 s ("เห็นมั้ย ไม่มีใครบ้าตามเอ็งหรอก!"); use the lip-sync poses (coachman_point_mock / boast / shout and the _box_ twins)
  with talk_mouth. Everywhere else mouths stay still (laughs may show an open laughing mouth only in the laugh poses).
- Comedy only: cabbage, egg and mud hit the umbrella or splash him; nobody is hurt. Hanway stays calm and smug.
- Ending: the head coachman sulks on his EMPTY coach under the pink lace umbrella (set_pink_umbrella + pink_to_hand); slow push;
  the film hard-cuts on the last word at 58.99 s.

## Teams and takes (take sNN = number of its first shot; one take = one process = consecutive shots with in-take cuts)
| team | takes | shots | t range (s) |
|---|---|---|---|
| 1 | s01, s04 | 1-3, 4-5 | 0.00-10.51 |
| 2 | s06, s09 | 6-8, 9 | 10.51-21.69 |
| 3 | s10, s13 | 10-12, 13-14 | 21.69-34.98 |
| 4 | s15 | 15-18 (REVEAL) | 34.98-44.66 |
| 5 | s19 | 19-21 | 44.66-52.64 |
| 6 | s22 | 22-23 (ENDING) | 52.64-59.50 |
Transitions: all cuts, except s13 enters with a dissolve of 12 frames ("ten years later"): team 3 renders the handles for it and team 2/3
give 8 handle frames on that side. Everyone else: 6 handle frames each side.

## Worked example and helpers
There is no film-12 s01 yet. Use PROJ/v3/film8/s01/shot.py + QA.md and PROJ/v3/film8/common.py as the pattern (gotchas: moves must
move, key every hook every frame, one location per process). Make your OWN helper module inside your take folder (e.g.
film/v3/film12/sNN/c12.py) copied from film8/common.py and switched to cast12 + street.py. No shared film/v3/film12/common.py.
Draft first at 360x640 / 6 samples, look at a contact sheet next to the approved tiles, fix, then final.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
- Before delivering: `python3 film/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>`; fix every FAIL; add
  QA_AUTO.md and phone_sheet.jpg to the take folder.
- Then check yourself at 6 fps plus every cut ±3 frames: heads above y 880, contact shadows / no floating feet, props held in hands,
  eye-lines, continuity with neighbouring takes (Hanway's coat, umbrella, rain, light RAIN vs DUSK_RAIN as the plan says), mouths only
  in the quote windows, no grain/speckle, no glowing orbs on the road. Write QA.md.
- The director's QA-tech re-checks every take; QA-art (opus) must pass the key takes (s01 hook, s15 reveal, s10 mud/false payoff, s22).

## Delivery
- Folders PROJ/v3/film12/sNN with shot.py, helper, meta.json (g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve",
  "frames":n}), cues.json, contact.jpg, QA.md, QA_AUTO.md, phone_sheet.jpg, take.mkv
  (`ffmpeg -framerate 30 -start_number <first g> -i frames/g_%04d.png -c:v libx264rgb -crf 6 -preset slow take.mkv`).
  If take.mkv > 45 MB: `split -b 40M take.mkv take.mkv.part` and commit the parts instead. frames/ stay out of git.
- Push each take to your own branch as soon as it is final. Do not open pull requests. Work autonomously and do not wait for
  confirmation: the client already approved the set, the cast and the render. Final message: takes, frame ranges, s/frame, deviations.
