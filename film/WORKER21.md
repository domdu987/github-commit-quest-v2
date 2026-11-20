# Render-team worker brief, film 21 (ไอ้ชาวนาบนเนิน — Battle of Stirling Bridge, 11 Sept 1297)

Follow film/WORKER.md exactly: section 1 setup, section 4 delivery, section 5 rules. The film-21 differences are below.
PROJ = your clone's film/ folder (clone_depth 1 of branch film21/main). Push to YOUR outcome branch only (render21/teamK).
Install: `pip install -q bpy numpy pillow opencv-python-headless pythainlp`.

## Inputs
- **Brief and shots:** PROJ/film21/BRIEF.md and PROJ/film21/shot_plan.md (31 shots, 11 takes). Your take, its shots, g range and internal cuts are in PROJ/film21/RENDER_TEAMS.md and your task message.
- **Facts / content:** comic and BLOODLESS. No wounds, nobody lying still, nobody dying. Spears block and point. English soldiers back off, bump, wobble, splash into water and come up spluttering. Cressingham appears ONLY on the south bank. In the ending only his EMPTY money table is shown.
- **Look:** wide or medium framings that show the dense lit set. The camera is always moving. Sharp, NO depth of field, no haze, no readable text.
- **Narration:** PROJ/film21/audio/narration.wav (61.25 s), placed at +0.10 s. **Captions:** PROJ/film21/script/captions.json (narration time).
- **Frames:** N = 1848, g = round(film_t*30), film_t = narration_t + 0.10. Hard cut at the end on the last "ตูม".
- **Sentence starts** (narration time): hook 0 / pivot 5.19 / bridge 13.82 / mocker 18.02 / nickname 26.32 / count 29.39 / false 34.71 / crisis 37.94 / reveal 41.19 / aha 50.53 / ending 54.55 / end 61.25.

## CAMERA RHYTHM (client rule, production-lessons §10 + bible camera.md): your take FAILS QA without it
- Every shot has a clear eased move: a drift push or pull of 6-10 %/s plus a lateral slide of 20-60 px/s, or a snap (13-25 frames, x1.3-x3).
- Never more than 6 frames under 0.25 px/frame. No near-static hold over 1 s.
- Framing changes every 1.3-1.4 s on average: add a snap or a reframe inside any shot longer than 2.2 s.
- A foreground prop 1-2 m from the lens in most shots; every preset has one, keep it in frame while you drift.
- Laughing characters bounce about 0.06 D at about 3 Hz (`cast21.laugh(pose, g)`). Nobody is frozen: idle sway, blinks, horse head bob and tail swish.
- Measure your take: `python3 PROJ/film21/rhythm.py take.mkv --first_g <first_g> --cuts <your internal cuts>`. Median in-shot frame-diff must be >= 4 and p90 >= 12 (film 2 = 5.1 / 18.7). Report both in QA.md.
- Heads: centre y 450-760, whole head above y 880.

## Set
PROJ/v3/set3d21/stirling.py. READ FIRST: PROJ/v3/set3d21/API.md (all sections) and **QA_ART_SET.md, "Notes for render teams" per preset (mandatory)**.
- Units: 1 unit = 1 m; character height D = 1.7 units (`K.D`). Card heights are in `K.HEIGHT` (API §1).
- Presets: hill_over, hill_eye, hill_low / bridge_deck, bridge_high, bridge_end_north, bridge_end_south / valley_wide, valley_loop, valley_river / camp_wide, camp_table, camp_bank / riverbank, river_low.
- Build once per process and location, then per frame call the hooks and `K.render()`. The build is the slow part.
- Hooks (key every frame): `set_flutter(t)`, `set_smoke(t)`, `set_flow(t)` (water: ALWAYS call it), `splash(x, y, age, size, name)`, `set_scale_tip(A, deg)`, `set_chest_lid(A, deg)`, `place_troops(A, where, n, cb=...)`. Use the troop counts in shot_plan.md (shot 15 about 10 on the causeway; shot 17 hundreds on the meadow; shots 20 and 24 about half the army).
- Lenses: 22 mm, except hill_over 32 and camp_bank 30 (set by the preset; keep them).
- **Render cost:** the default final (64 samples) costs about 100 s a frame. Use `samples=24` with OIDN for production unless QA_ART_SET.md says otherwise. Check your first final frame at full size for noise or blotches, and raise samples only if it is visibly noisy. Draft at 360x640 first.

## Cast
PROJ/v3/cast21 (`import cast21` BEFORE `sprites`/`stage.sprites`). Read API.md.
- Members: cressingham, surrey, knight_a/_open, knight_b/_great, footman_a/b (variants `variant21`), wallace, moray, scot_a/b/c, scot_horn, horse, *_mtd riders, helmet_float, swim crop cards.
- Poses: `cast21.STORY21` (see API.md).
- Mouths are closed unless you call `speak(...)` inside the quote windows below.
- Riders are pinned to the horse card (`*_mtd`), so move the whole card.
- Jump poses keep the soles on the ground: lift the card 0.5-0.8 D for airborne frames.
- For the water, use the swim crop cards with `K.splash()` crowns at the entry point.

## Mouths and acting
- Cressingham's mouth moves ONLY in his quotes (narration time, ±0.15 s): **21.29-26.26** and **36.32-37.89**. He laughs (laugh pose and bounce, no lip-sync) at 20.29-21.29. The camp laughs at 34.71-36.32 (fixed laugh drawing and bounce).
- Nobody else speaks. The Scots never open their mouths; the horn blower puffs his cheeks on the horn at 39.7-41.1.
- One gesture per shot on its caption word. Shocked faces swap behind a blink and get a sweat drop.

## Worked example and helpers
- Worked example: PROJ/v3/film8/s01/shot.py, QA.md and PROJ/v3/film8/common.py. Read their gotchas: moves must move, key every hook every frame, one location per process.
- Make your OWN helper module inside your take folder (for example PROJ/v3/film21/sNN/c21.py) by copying film8/common.py and switching it to cast21 and set3d21/stirling.py.
- Do not create a shared film/v3/film21/common.py.

## QA_TEAM.md §G (client complaint 2026-11-20): BLOCKING at the TAKE gate
- Colour: `python3 PROJ/qa_stats.py take.mkv` must show saturation >= 0.47 and brightness 85-110. The set's grade has a per-preset VIVID stage that gets you there (API.md §9); keep `K.STATE['preset']` set and never skip the grade.
- Nothing floats: every character's feet on the ground with a contact shadow (`contact=True` on the Actor), riders on their horses, nothing hanging in the sky, no pole or prop passing through a face.
- Camera distance: at least half your shots wide or medium-wide (they show the place). No face taller than 35 % of the frame height. Nobody cut in half by a frame edge.

## QA (stricter, film/QA_TEAM.md "Stricter QA")
- Before delivering, run `python3 PROJ/qa_auto.py take.mkv --first_g <first_g> --cuts <your planned cut g's>` and fix every FAIL. Add QA_AUTO.md and phone_sheet.jpg to the take folder.
- Then check your frames yourself at 6 fps, plus every cut ±3 frames:
  - heads above y 880
  - contact shadows
  - props held
  - eye-lines
  - continuity with the neighbouring takes
  - mouths only in the quote windows
  - riders move with their horses
  - nothing bloody
- The director's QA-tech re-checks every take. QA-art reviews the key takes s01, s07, s09 and s11.

## Delivery
- Take folder: PROJ/v3/film21/sNN. meta.json holds g0, g1, first_g, n_frames and transition_in {"type":"cut"|"dissolve","frames":n}. Also deliver cues.json (sound cue suggestions with g), contact.jpg and QA.md.
- Render 6 handle frames on each side. If take.mkv is over 45 MB, run `split -b 40M take.mkv take.mkv.part`.
- Commit and push the take to your outcome branch as soon as it is final. Also push work in progress every ~30 min (the container can restart; `git add` your sNN folder, not frames). Do not open pull requests.
- Work autonomously. Do not ask for confirmation: the set has passed QA-art (the client delegated approval to QA-art) and rendering is approved.
- If a fix request arrives from the director, fix that take, re-run QA and push again.
