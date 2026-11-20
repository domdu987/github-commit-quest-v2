# Film 23 style board brief (builder: Sonnet; QA-art (Opus) approves, client sees it FYI only)
Film: "ไอ้กองทัพลูกโป่ง": the WWII US "Ghost Army" (23rd Headquarters Special Troops), France 1944 and the Rhine 1945.
Script: film/film23/script/script_th.txt. Facts: film/film23/FACTS.md. Client rules: film/QA_TEAM.md §G, §H, §I (blocking).
Targets: film/ref_shorts/*_sheet.jpg (look at R2, R4, R5, R7 sheets FIRST) and film 2 (film/release/sky_poker_v3.mp4).

## Goal
3 stills (720x1280, Cycles CPU, 12 samples, NO depth of field, sharp) that show the LOOK of the NEW set before it is built in full:
palette, detail level, the dawn and the night light presets. Build them in the module that will grow into the full set:
`film/v3/set3d23/ghost.py` (+ `ghost_tex.py` for painted/procedural textures, + `ghost_props.py` for the rubber tank etc.).
Output: `film/v3/set3d23/board/board_1.png..board_3.png`, `film/v3/set3d23/board/style_board.jpg` (3 tiles side by side, labelled
under each, cyan line at y 880 on each tile), `board/numbers.json`, `board/NOTES.md`. Rebuild command: `python3 ghost.py board`.

## Reuse helpers, never an old set
New set every film: do NOT render any older location. You MAY import helpers the way v3/set3d10/harbour.py does
(tower.make_camera/render/mat_lit/mat_emit/setup_grade, mine.obox/rod/lumpy, bakery._halo, ...). Read v3/set3d10/API.md and the top of
v3/set3d10/harbour.py first; film 18's set (git show origin/film18/main:film/v3/set3d18/jimo.py, board.py, jimo_hue.py) is the most
recent worked example of a board module, copy its structure (board.py, hue script) freely.
Skill references: film/skill/reference-style-shorts/references/bible/sets.md (8-9), colour-light.md, camera.md.
bpy 5.3 is installed (`python3 -c "import bpy"`). 4 cores: render with threads 4, ONE render at a time.

## THE HERO PROP: inflatable rubber M4 Sherman tank (build it well, it is in every scene)
Olive drab (#5b6b2e-ish, saturated, not grey), slightly puffy rounded edges (bevel/subdivided, soft pillow seams along every edge),
visible inflation seams and a small valve, a white US star on the side, a long barrel that can SAG (parameter `sag` 0..1 for a
half-inflated state) and a `inflate` parameter 0..1 that shrinks/crumples the whole hull (0 = flat rubber sheet on the grass).
Rubber sheen (low roughness spec, soft highlight) so it reads as rubber up close but as a real tank from far away.
Also: inflatable 2.5-ton truck and a towed gun (simpler), camouflage nets on poles, wooden crates with stencil text, a sound truck
(half-track or truck with a big round loudspeaker horn on the back), a radio tent.

## The three stills
1. **dawn_fields_high** (BIGZOOM start frame, high bird's-eye from ~60-80 D up, 30-45 deg down): Normandy bocage at blue dawn:
   bright saturated green fields in a patchwork separated by dark hedgerows, a winding dirt lane, a column of 8-12 olive rubber tanks
   along the lane under camouflage nets, a stone farmhouse with RED tile roof and a barn, poplar trees, an orchard, cows in a field,
   a village with a church steeple far off, a river glinting, low mist only in the far valley (no haze over the frame).
   Sky: clear blue dawn with a warm gold sunrise rim on the horizon. Tiny soldiers (placeholder cards are fine) findable, <5 % height.
2. **inflate_lane_morning** (medium-wide, LOW hero angle ~1.2 D up, from the lane): 4 soldiers (placeholder cards, olive uniforms,
   helmets) around a HALF-inflated rubber tank (barrel sagging), a hand pump/compressor with a hose, open crates stencilled
   "23rd HQ SPECIAL TROOPS" and "DECOY M4  HANDLE WITH CARE", a canvas sign on a post "23rd HQ SPECIAL TROOPS", a French bicycle
   leaning on a stone wall in the FOREGROUND (1-2 D from lens, for parallax), hedgerow, red-roof farmhouse behind, morning sun low
   from camera-left giving a warm RIM on the tank and soldiers, blue sky. Text must be sharp and readable on a phone.
3. **night_sound_truck** (wide, slightly high, night): deep blue moonlit field, rubber tank silhouettes in rows under nets, a sound
   truck with a big loudspeaker horn, a radio tent glowing with WARM LANTERN light (emitters with halo), a jeep with dim lamps,
   oil lanterns hanging on poles, a soldier at a radio set inside the tent (placeholder card). Moon low, stars. Warm vs cool in one frame.

## Look rules (client, hard)
- SIGNATURE COLOURS: olive + khaki (army) against BRIGHT French-countryside green and a BLUE dawn; warm lantern light at night.
- Sharp, no DOF, no blur, no haze over the frame. Wide, dense, beautiful lit 3D world (interior/exterior 12-26 distinct objects in view).
- Motivated key light (low sun / moon / lanterns) and a rim light on characters and the tanks; warm and cool in the same frame.
- Colour targets (QA_TEAM §G, §I): mean saturation >= 0.50 (max-min)/max, mean luma 85-110 (night still may sit at 70-95, say so),
  shade hue 240-260 on lit sets, magenta <= 10 %. Measure with film/qa_stats2.py style numbers + v3/tools/hue_report.py; numbers in NOTES.md.
- Props have thickness and the 3 px inverted-hull ink (as earlier sets); never ink sky, water, fog, grass.
- Nothing floats: everything sits on the ground with contact shadows.
- Caption band y 880-950 kept free of important detail and text.

## Done = 3 PNGs + style_board.jpg + numbers.json + NOTES.md (numbers, render times, what each still tests) + `python3 ghost.py board`.
Do not commit; the director commits. Report paths and numbers, and honestly what still looks weak.
