# Film 22 full set brief (builders: Sonnet, two in parallel) -> film/v3/set3d22/
Read first: film/film22/WORLD.md, film/film22/shot_plan.md (THE cameras you must provide), film/v3/set3d22/board/QA_ART.md (both rounds; its carry-forward rules are mandatory), board/NOTES.md, film/QA_TEAM.md §G, §H and §I, and the existing board code `beck.py` / `beck_tex.py`. Cast: film/v3/cast22/API.md.
PROJ = /home/user/github-commit-quest-v2/film. bpy 5.3 installed. 4 cores: ONE render at a time between the two builders. Before rendering, check `pgrep -f "blender|bpy" -a`, and if the other builder is rendering, wait for it.

## Split (do not edit the other builder's files)
- `beck.py` stays the shared core: materials, ink, lights, sky, camera helpers, the CLI, the board stills. Only **builder A** may edit it. Builder B imports it and puts any new helper in its own module.
- **Builder A:** `beck_london.py` (london DUSK + NIGHT) and `beck_hq.py` (Beck's lodgings NIGHT; HQ corridor + publicity dept EVENING + NIGHT with the map towers). Shots s01, s02, s04, s05, s06, s07, s08, and s15 (london NIGHT → publicity window → official).
- **Builder B:** `beck_under.py` (grate shaft, noodle tunnels cutaway, platform, ticket hall, carriage) and `beck_map.py` (mapworld + the world of other cities' diagrams). Shots s03, s09, s10, s11, s12, s13, s14.
- Shared registry: each module registers its shots in its own dict `SHOTS = {'sNN': {...}}`. `beck.py` builds a merged `ALL_SHOTS` by importing the 4 modules lazily. Builder A adds this hook first, within the first 10 minutes; builder B only fills its own dict.

## What each location needs
Use the locations, props, signs and light described in WORLD.md, and the actions and camera moves in shot_plan.md. Rules:
- **Light.** Motivated key and rim light everywhere; deep dark blue + warm amber + the Tube-line colours.
- **Colour targets.** Saturation ≥ 0.50, vivid ≥ 45 %, luma 85-110, shade hue 240-260 per contact tile (use `stats.py`).
- **Density.** Interior wides show 20+ distinct objects, exteriors 12-18+. No bare floor over about 20 % of the frame: rugs with props, newspapers, luggage, benches, light pools.
- **Ink and text.** Man-made props carry the inverted-hull ink. Signs are short English text, never mirrored, and readable at 360x640. No text or heads in the caption band (y 880-950) in the key framings.
- **Connected travel joins.** These must line up across the two modules, so agree the coordinates in API.md:
  - the lodgings window and the publicity window ↔ london;
  - the grate in london ↔ the shaft top in under. Builder B's shaft starts at the same xy as builder A's grate, and the london ground is z 0. Builder A exports `GRATE_XY` and the window positions in `beck_london.py`.
  - the old map on the platform ↔ the old map in the lodgings (the same texture);
  - the pocket map in the carriage ↔ the mapworld paper.

## Per shot: a named camera with its planned move
`key_camera('sNN', f0)` keys the eased move from shot_plan.md, from the shot's first film frame (g = round(t*30)), with 6 handle frames each side.
- **BIGZOOMs** (s02+s03, s15) start EXTREME WIDE, with the character under 5 % of the frame height, and end MEDIUM (35-60 %). They pass through set detail.
- **Marks** are named stand points for every character in every shot (`MARKS['sNN']['beck'] = (x, y, z, yaw)`), on the floor, at the right scale (person about 3 D).
- **Setters** are keyable state functions, for example:
  - `set_line_progress(k)`: the diagram lines drawing on Beck's board, 0..1, plus a separate red/blue/green/yellow order and a 45° bend event.
  - `set_station_squeeze(k)`
  - `set_drawer(open)`
  - `set_stamp_mark(on)`
  - `set_trial_stack(n)`
  - `set_rack(full 0..1)`
  - `set_reprint_crates(n)`
  - `set_map_towers(h)`
  - `set_train(pos)`: the train in platform and tunnel
  - `set_carriage_rock(t)`
  - `set_map_glow(which)`: red line / interchange / station
  - `set_city_diagrams(k)`
  - `set_crowd(n, seed)` per location
- **Placeholder cards.** Render with placeholder or cast22 cards at the marks. The render teams put in the real cast22 cards.

## Deliverables
1. The modules, plus an updated `API.md`. It covers coordinates, marks, every camera and its move, every setter, the join coordinates, and how to build each location (`beck.build(location, light, shot)`). One location per process.
2. `contact/` with one final 720x1280 still per shot. Each still is at the shot's START frame and at its END frame, with an extra mid frame for BIGZOOMs. Use 12-16 samples with denoise and no DOF, placeholder or cast22 cards at the marks, and a cyan line at y 880.
3. `contact_sheet.jpg`, labelled `sNN start/mid/end` with stats per tile, plus `contact_phone.jpg` at 360x640.
4. `hue_rows.txt` / stats per tile.
5. A short `BUILD_NOTES.md` per builder: what was built, render seconds per frame per location (teams need this), and known issues.

Look at your stills at full size and at phone size, and fix empty areas, unreadable signs, floating things and washed-out colour before you report. Do not commit; the director commits. Stay inside v3/set3d22.
