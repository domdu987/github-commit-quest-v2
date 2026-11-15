# Render-team worker brief, film 9 (ไอ้ช่างขนม — sticky-rice mortar, Ming city wall)

Follow film/WORKER.md (setup section 1, delivery section 4, rules section 5) exactly, with these film-9 differences:
- Brief PROJ/film9/BRIEF.md and USER TASTE in PROJ/film8/BRIEF.md (wide/medium framings showing the dense set, calm but always-moving
  camera, warm lit 3D world, sharp, NO depth of field, no text signs). Shot plan PROJ/film9/shot_plan.md.
- Narration PROJ/film9/audio/narration.wav (58.4 s) at +0.10 s; captions PROJ/film9/script/captions.json; N = 1767; g = round(t*30).
- Set PROJ/v3/set3d9/wall.py (+ wall_API.md incl. gaps: presets site_wide, cauldron, two_sections, two_sections_out, wall_top,
  cannon_line, mortar_macro, mortar_macro_rice; lights DAY DAWN DUSK RAIN BATTLE; hooks set_wall_height, set_cauldron_steam, set_rain,
  set_mortar_wet, set_cracks, set_impact, set_collapse, set_smoke, set_flames, set_army, set_macro, clear_keys — animated hooks every frame).
- SET UPDATED (client-approved after 3 QA rounds): extra presets pour_close (shot 2), gate_dusk (shot 4), two_shot_low with stand
  points two_shot_general / two_shot_lin (shot 6), wall_top_battle (30 courses, shot 19), aftermath_dawn (shot 17, warm dawn, dents),
  macro_front is the default camera of mortar_macro / mortar_macro_rice (shots 15-16). Read set3d9/QA_TECH.md + QA_ART.md (take notes:
  site_wide Lin chin near 880 -> lower camera ~1 D; shots 7/12 need a closer camera so figures read; two_shot_low look-at +0.5 D x;
  keep the ball visible at macro 0.9).
- Your take will pass a QA-tech check (film/QA_TEAM.md) before conform; run your own qa.py first.
- Cast PROJ/v3/cast9 (+ API.md; general_fall needs CANVAS9_FALL["general"]; helmet_off, wet, dust keys).
- WORKED EXAMPLE (previous film, same conventions): PROJ/v3/film8/s01/shot.py + QA.md and PROJ/v3/film8/common.py (read its gotchas,
  esp. "moves must move", key every hook every frame, one location per process). Make YOUR OWN helper module inside your take folder
  (e.g. film/v3/film9/sNN/c9.py) by copying film8/common.py and switching it to cast9 + wall.py. Do not create film/v3/film9/common.py.
- Mouths move only on the general's quotes (boss ~11.3-14.3 s, false ~32.0-34.6 s). The general's fall at the end is comic (no injury).
- Take folders PROJ/v3/film9/sNN; meta.json with g0, g1, first_g, n_frames, transition_in {"type":"cut"|"dissolve","frames":n}; render 6
  handle frames each side. take.mkv over 45 MB: split -b 40M take.mkv take.mkv.part . Push each take as soon as it is final.
