# v3/set3d17: the film 17 set ("Bertillon", Paris police 1882-83) (bpy 5.x, Cycles CPU)

## v2 render recipe (render teams, film 17 remake; `prefecture17.py`; take sheet: `film/film17/v2/takes.md`; reference: §v2 at the end)

```python
import sys; sys.path.insert(0, "film/v3/set3d17"); import prefecture17 as P, bpy
take = 'T3'
assert P.check_take(take)['hits'] == [] and P.check_face(take)['ok']          # 1. both checks PASS before anything renders (§v2.10, §v2.11)
A = P.world_build(take)                               # 2. only what the take sees, lit by its presets + TAKE_OVER; camera 'cam'
P.key_take(take)                                      # 3. camera path, story hooks, light schedules, cutaway, life: keyed on every frame (frame = g + 1)
P.setup_render2((720, 1280), samples=16, threads=2)   # 4. 16 samples + OIDN, adaptive 0.03 (A/B approved). grade2 as is: never raise saturation
g0, g1 = P.TAKES[take]['render']
for g in range(g0, g1 + 1):                           # 5. frame by frame (resume: skip frames/gNNNN.png > 50 kB)
    bpy.context.scene.frame_set(g + 1)
    acts = P.stage_cast2(take, g, assign_for(g))      #    REAL cast17 cards on every frame: floor_z feet, face keys, +-35 deg clamp, back views, lip-sync via opts talk
    bpy.context.scene.render.filepath = 'frames/g%04d.png' % g; bpy.ops.render.render(write_still=True); P.grade2(bpy.context.scene.render.filepath)
```
- **Cast:** real cast17 cards only, through `stage_cast2(take, g, assign)` on every frame. Never use `bertillon.stage_cast` or placeholder cards
  in a delivered frame. `opts={'talk': True}` drives the mouth with `cast17.speak` and is used **only** inside the quote windows
  (g493-651 and g1128-1196). Every other mouth stays closed, except the planned held shapes: the laugh g467-493 and the P2 jaw-drop.
- **Motion blur:** shutter **0.5** only on T1 g152-278 and T7 g1800-1867 (optional on T4 g1035-1038 and T5 g1141-1150). Everything else is
  sharp, so qa_auto's blur check is not tripped.
- **Before the full render, every team:**
  - run `check_take(take)` and `check_face(take)`;
  - render **one full-res 720x1280 still with the real cards** at the take's key frame:

    | take | key frame |
    |---|---|
    | T1 | g105 |
    | T2 | g560 |
    | T3 | g800 |
    | T4 | g930 |
    | T5 | g1150 |
    | T6 | g1515 |
    | T7 | g1730 |
    | T8 | g2018 |

  - commit the still and both check outputs, and wait for the director's OK.
- **After the first 30 frames:**
  - Check qa_stats2 luma against the take's target:

    | target | takes |
    |---|---|
    | 95-112 | T1; T6 (P1 excluded) |
    | 95-110 | T2, T3, T4, T8 |
    | 90-108 | T5 |
    | 88-105 | T7 |

    Fix by light only (`TAKE_OVER` / preset), never by haze or lowering saturation.
  - Watch the 30 frames as a clip for OIDN shimmer on flat walls (T5 night, T1 roofs). If it shimmers, use 24 samples for that take only.
- **Façade-sign rule (T1):** PRÉFECTURE DE POLICE must be whole and readable (cap height ≥ 28 px at 720x1280) for **≥ 20 consecutive
  frames** between g200 and g300. The g218 crane top does not show it whole today: re-aim that look-at up and toward the band, or hold the band
  whole through the swoop g227-287. BIGZOOM 1 must still PASS.
- **Light schedules already in `take_state` (QA v2b):**
  - T1: the window key goes 300 W → 220 W over g96-110.
  - T2: the door lanterns and fanlight run at -20 % for g330-360.
  - T6: if the take mean is above 112, tone the card paper to cream (#F2E6C8).
  - T7: if the first 30 frames are below 88, add +5 % to the `TAKE_OVER` shade.
- **Keep:**
  - the clock face and its screen position matching across the T3 → T4 cut;
  - the T5 escort lanes at x 15.9 / 16.6 / 17.3;
  - the T2 corridor gendarme's head not cut by the left edge for more than 10 frames;
  - the OTS heads not cut by the top edge;
  - P2 / P3 faces at no more than 35 % of the frame height.
- **Cost:**
  - World alone at 16 samples: 36-73 s/frame (§v2.10).
  - Real cast sprites add about 30-40 s/frame for 4-6 cards; the 4 real-cast stills took 50-87 s each in total.
  - Whole film about 45 CPU-hours (2 threads), about 8 h with 8 teams.

## Files

| file | what |
|---|---|
| `bertillon.py` | the module: materials, light presets, batching, every prop, the 4 locations, hooks, presets, camera, render, placeholders, CLI |
| `bertillon_tex.py` | the drawn textures (plank seams `#432219`, wainscot panels, ashlar, setts, zinc, runner, frieze, the Bertillon card, framed portraits). Cached in `tex/` (git-ignored, about 3 MB, rebuilt on demand) |
| `bertillon_hue.py` | colour numbers per frame: hue_report families + shade hue + black point + vivid blue + dim-pixel hue shares |
| `make_contact.py` | renders every tile, builds `contact.jpg` / `contact_small.jpg`, writes `hue.md` |
| `contact.jpg`, `contact_small.jpg`, `hue.md` | the review sheet (20 tiles, 720x1280, label strip under each, cyan line at y 880), 1/3 size, and the numbers |
| `bertillon_board.py`, `styleboard.py`, `hue_check.py`, `styleboard/` | the old style-board kit, kept for the record (`QA_ART.md` is the review this build answers) |

## 1. Conventions

- **1 unit = 1 m = 0.59 D.** One **D = one character height = 1.7 units** (`bertillon.D`). Card heights in units: `HEIGHT = clerk 1.78, prisoner 1.68, inspector 1.66, gendarme 1.82, prefect 1.74, seated 0.95` (the inspector in the measuring chair: a seated sprite stands with its feet at the seat). The stage package works in head diameters (a hero is 3 head-D tall): pass `scale = HEIGHT[who] / card_height_in_head_D` to `Actor.place`.
- Z up, floor z = 0. Camera: 22 mm, sensor 36 (AUTO fit), 720x1280, so 782.2 px focal; a 1.7 unit person at distance d is 1330 / d px tall. Every preset places a **foreground prop 1-2 units from the lens** (`fg`), and the cameras have room to drift (rooms are 6.4 x 8.4, the aisle 18 long, the street 70 long).
- Placeholder cast: `stage_placeholders(A)` puts a near-white head `#fef7f6` with a plum ring on a flat coloured body at each stand point, turned to the camera. The head is 0.3 of the card height. `head_ring_luma` measures the background ring around each head.

## 2. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d17"); import bertillon as K
A = K.build('measure', 'measure_wide', light='DAY_INT')   # build(location=None, preset=None, light=None, ink=True, fg=True) -> anchors dict
A = K.build(preset='card_hero')                           # the preset decides location, light, camera, foreground prop and start state
cam = bpy.context.scene.camera                            # build() makes the camera when a preset is given
K.stage_placeholders(A, only=K.PRESETS['measure_wide']['stage'])   # stand-in cards
K.render('/tmp/f.png', 'final' | 'draft', samples=None)   # 720x1280 80 samples | 360x640 24 samples, OIDN denoise, 4 threads, then grade()
K.head_ring_luma(A, '/tmp/f.png', only=[...])             # {mark: {luma, cx, cy, R, chin}} (screen px)
```
`A` holds: `marks` (stand points), `cam` (loc, look, lens), `location`, `light`, `preset`, and location extras (`door`, `smoke_src`, `pendulum`, `dust_box`, `cab`, `big_front`, `hero_ref`, `fan`, `wagon`, `station`).

Other public functions:

| function | what |
|---|---|
| `build(location, preset, light, ink, fg)` | builds the scene (new Blender scene each call). `ink=False` drops the outlines. |
| `new_scene(light, over)` | empty scene + the light preset (`over` overrides single numbers). |
| `Batch` (`box, cyl, sphere, mesh, quad, prism_roof, xf, wpt, finalize`) | the batcher: one Blender object per material key; `finalize(prefix, loc, parent, ink_t)` adds the ink hull. |
| `get_mat(key)` | material by key (palette below). |
| `sun()`, `point()`, `area()`, `spot()`, `camera()`, `sky_dome()` | lights and camera. Point lights register for `set_flicker`. |
| `setup_render(scene, mode, samples)`, `render(path, mode, samples, do_grade)`, `grade(path)` | render + grade (bloom halo only around real emitters: min channel >= 252; saturation 1.05; nothing else). |
| `stage_placeholders`, `head_ring_luma`, `project(cam, p)` | placeholders and screen measurements (world to px at 720x1280). |
| `cli_render(preset, light, out, mode, samples)` | build + placeholders + render + `<out>.json` (times, head ring luma, chin px, triangles). |
| `drawer_assembly`, `card_box`, `cards_fan_objects`, `card_plane` | the animated assemblies (see hooks). |
| `t_hooks.py` | hook test: keys every life hook, the reveal hooks, the fan and the drawers and checks the values move (prints `ok 15 bad []`) |
| props (all take the `Batch` first) | `table, stool, bench, measuring_chair, toise, arm_span_scale, foot_board, sliding_calipers, spreading_calipers, camera_tripod, ledger_stack, open_ledger, inkpot, kepi, coat_rack, stove, wall_clock, pendulum_case, ledger_shelf, crate, bucket, umbrella_stand, wastebin, door, barred_window, gas_bracket, gasolier, gas_stand, gas_pipe, street_lamp, banker_lamp, cabinet_wall, rolling_ladder, police_wagon, station, shop, mansard, paris_roofs, puddles, light_shaft, room_shell, wall_box` |

CLI: `python3 bertillon.py render <preset> [light|-] out.png [final|draft] [samples]`, `python3 bertillon.py list`.

## 3. Light model (answers QA_ART fix 1)

Per surface: `Diffuse(art) lit by the real lights  +  Emission( (1-m) * art * SHADE * shade_mul + m * lum(art) * TINT * mean(shade_mul) * (afl + (1-afl) lum) + LIFT ) * (1 + N.form)`.
Fully matte (Lambert, roughness 1, no specular, no metal, no coat). The ambient is injected as emission, so shade is painted blue-violet and never brown.

| light | key | shade / tint / lift | sky | extras |
|---|---|---|---|---|
| `DAY_INT` | sun (2.30, 1.65, 0.74), hard shadows, through the barred window (measure), the skylights (records) or the window (reveal), plus a warm window area light | SHADE (0.10, 0.11, 0.36), TINT (0.075, 0.085, 0.25), LIFT (0.003, 0.008, 0.026), mix 0.85 | `#4a78cd` top to `#92b7e7` horizon, stretched over 260 m of height so only the lower, pale part shows | gas lamps (point light + glass globe), lamp_k 0.75 |
| `EVENING_INT` | sun (2.0, 1.3, 0.55) low and orange, gas lamps stronger (lamp_k 1.7) | as DAY_INT | `#40448f` / `#d98a78` / `#f6b97c` | glass globes glow harder |
| `DUSK_EXT` | low orange sun (2.0, 1.05, 0.5) raking down the street from behind the camera | as DAY_INT | `#5e5aa8` / `#e8837f` / `#ffd592` | street lamps (900 W), station lanterns, lit windows (glow), puddle reflections (the only glossy material) |

Per-surface `shade_mul`: woods (0.8, 1.0, 1.12), floors (0.8, 1.0, 1.15), warm walls (0.7, 0.95, 1.15), navy cloth (0.9, 0.95, 1.2). Big painted surfaces (walls, floors, ceilings, wainscot) have an ambient floor `afl`.
Emitters (`glow_gas` 14, `glow_frost` 3, `glow_win` 5, `glow_green` 3, `glow_door` 4, `glow_dust` 5) are **camera-only**: they do not light the scene (the point and area lights do), so the room does not turn orange-red. Only they bloom.

**Ink**: every man-made prop material carries an inverted-hull outline (solidify shell, flipped normals, transparent to every ray but the camera's, only the silhouette shows). Thickness `0.00384 x subject distance` (`sd` of the preset, 4-18 mm); foreground props use 0.7 x. Walls, floors, ceilings, sky, glass, glow, cabinet drawer fronts (dense, oblique) and paper (cream) carry no ink.

**Textures** are drawn (PIL), at 512 px per tile with every feature >= 3 texels, and projected in object space (box projection): plank seams `#432219` 5 texels wide, per-board flat tone (grey-level std 7-8), a few wobbly grain strokes, raised wainscot panels, ashlar courses, rounded setts (0.44 m, joints 4+ texels), zinc seams, a navy runner with a red border and gold lozenges, a frieze strip, and the card art. **No mip-mapping in Cycles, so nothing is finer than a screen pixel at the nearest camera** (checked: seams are 1.2-3 px at 4 m).

## 4. Locations

### A. `measure`: the measuring room of the Dépôt (x -3.2..3.2, y -4.2..4.2, h 4.2)
Terracotta-ochre walls over a dark crimson-brown panelled wainscot (1.3), a gold lozenge frieze, a navy-painted ceiling with oak beams, planked floor, a navy rug.
Left wall (x -3.2): barred window (y 0..2.4, z 1.95..3.4) with mansard roofs and chimneys outside (shadow-less), the prisoners' bench under it, the big display calipers on a plaque (y 3.35). Back wall (y 4.2): arm-span scale (x -1.55), ledger shelves, the wall clock (x 0.2, z 3.05, no numerals) with its pendulum case, the **toise** (x 1.7), notices and portraits (blank/greeked), stove in the back-right corner with its pipe. Right wall (x 3.2): the door to the corridor (y -3.0..-1.85, ajar, lit corridor glow), the clerk's table (y 0.55) with ledgers, ink pots, a green lamp and calipers, the coat rack with 3 kepis, notices. Middle: the **measuring chair** with head rest on a dais (0.7, 2.4, facing -y), the camera on its tripod aimed at the chair (0.95, 0.55, black cloth on the back), the small calipers table (1.9, 1.55), the foot board (2.2, 3.3). Two gasoliers with gas pipes, 3 wall brackets, crates, bucket, umbrella stand, bin, stools. About 29 distinct object types, 121 objects, 19 k triangles (plus hooks).

### B. `records`: the records office (aisle x -1.35..1.35, y -4..14, ceiling 6.8)
Both sides: 17 m runs of card cabinets (56 columns x 21 rows of 0.30 x 0.20 drawers: raised fronts, brass label frames with **blank** cream cards, brass pulls) with plinth, cornice, a pilaster every 1.5 m and rails. **14 drawers pulled out** (`p0..p7` right run, `q0..q5` left run) at different depths, a rolling library ladder on an iron rail (right run, y 7.6), gas brackets on the cabinet faces and pipes along the cornice, the clerk's desk (-0.8, 2.6) with the green banker's lamp, ledgers, ink, calipers and a **fan of 9 cards** (`set_cards_fan`), a second desk (0.9, 8.6), card boxes stacked on the floor, the navy runner with a red border, three frosted glowing skylights (y 1.2-3.0, 5.0-6.8, 8.8-10.6) with mullions and light shafts, and a barred end window (y 14) with rooftops. 257 objects, 70 k triangles.

### C. `reveal`: inside the records office (cabinet wall at y 0, camera side y > 0)
The narrowing chain, all lit: the **big drawer `big`** (front 0.9 x 0.4, depth 0.95, travel 0.78) in the cabinet wall (front centre (0.15, 0, 1.2)), with 34 cards at the back, two **card boxes** `box` (hinged lid, 10 cards) and `box2`, and calipers lying in the drawer; **the hero card** (0.30 x 0.20, two portrait frames front + profile, an ear sketch, a hand, ruled measurement rows with squiggle digits; no text) standing in `box`. Beside: the lamp table with a green banker's lamp, calipers, ink; calipers hanging on a baize plaque at the drawer's right; stool + ledgers; gas brackets. 120 objects.

### D. `street`: Paris street at dusk (x -4..4 carriageway, y -14..60)
Setts, pavements and kerbs, 2 x 5 Haussmann blocks with ashlar, balconies, mansard roofs, dormers, chimneys, ground-floor shopfronts with striped awnings and **blank** sign bands (no lettering), lit windows (40-55 %), the **police station** at x 6, y 4..18 (arched door with warm glow, steps, two lanterns, a **blank sign board**, balcony), the **police wagon** (Black Maria: dark navy box, red cornice, barred slits, rear door and step, driver's box with lantern, shafts) at (3.0, 8.5) facing +y, 12 gas street lamps, barrels, a blank advertising column, 7 puddles with real reflections, a closing block at the end of the street, a dusk sky dome. 84 objects, 26 k triangles.

## 5. Presets (`K.PRESETS`)

Camera, look-at, stand points and the foreground prop (1-2 units from the lens). `sd` = subject distance for the ink width.

| preset | loc / light | camera -> look | lens | foreground prop | stand points staged | what |
|---|---|---|---|---|---|---|
| `measure_wide` | measure / DAY_INT | (-1.9, -3.9, 1.5) -> (0.8, 2.4, 1.35) | 22 | gas standard, stool + ledgers, a small rug, crate stack, coal scuttle, stool + kepi (all y -3.5..-1.5) | bench0, queue0, chair, clerk, door_mid | eye-level wide: bench queue left, chair + tripod centre, toise right |
| `measure_chair` | measure / DAY_INT | (2.0, 0.2, 1.5) -> (0.7, 2.4, 1.2) | 22 | the tripod camera + clerk's table corner | chair, clerk | medium on the chair, head rest and calipers table |
| `measure_high` | measure / DAY_INT | (2.9, -3.8, 3.55) -> (-0.4, 1.9, 1.1) | 22 | an UNLIT gas bracket (brass, no glow) at the corner; the second gasolier hangs 0.85 m higher (`lamps_up`) | bench0, bench2, queue0, chair, tripod | high angle over the room, the queue on the bench |
| `measure_door` | measure / DAY_INT | (-1.7, 0.9, 1.5) -> (3.2, -2.9, 1.3) | 22 | ledger table corner | door_out, door_r, door_x | from inside toward the door: entrances |
| `measure_low` | measure / DAY_INT | (0.3, 0.55, 0.5) -> (0.9, 2.4, 1.5) | 22 | ledgers + crate on the floor, 1-1.5 m ahead | chair, clerk | low-angle hero of the clerk at the chair |
| `records_aisle` | records / DAY_INT | (0.75, -3.2, 3.9) -> (-0.2, 6.5, 2.0) | 22 | gas bracket + crates | aisle1, aisle2, ladder_foot, aisle_far | high, off-centre down the cabinet canyon |
| `records_low` | records / DAY_INT | (0.1, -0.8, 0.55) -> (-0.9, 6.0, 3.2) | 22 | crate stack + stool | low_a | low angle up the cabinet wall |
| `records_desk` | records / DAY_INT | (0.9, 0.6, 1.5) -> (-0.8, 2.6, 1.4) | 22 | a drawer pulled out (`pn`) + crate | desk_clerk, desk_stand | medium at the desk: fanned cards (`fan` 1), green lamp |
| `records_ladder` | records / DAY_INT | (-0.2, 4.8, 1.4) -> (1.1, 7.6, 3.2) | 22 | crates + ledgers | ladder_up | the rolling ladder on the right run |
| `drawer_big` | reveal / DAY_INT | (0.6, 2.6, 2.2) -> (0.1, 0.5, 1.15) | 22 | stool + ledgers (0.65, 2.15) | drawer_r, drawer_l | the big drawer pulled out, many cards |
| `drawer_box` | reveal / DAY_INT | (0.09, 0.99, 1.68) -> (-0.03, 0.58, 1.2) | 22 | the drawer front | - | the light-ochre card box (lid open) lifted flush with the drawer rim on a ledger block, own warm spot `box_lamp`; sun 0.5x, window 200 W |
| `card_hero` | reveal / DAY_INT | (0.3, 1.5, 1.75) -> (0.0, 0.7, 1.3) | 22 | stool + ledgers, the lamp table at the left | - | one Bertillon card lifted in lamplight, calipers beside |
| `street_wide` | street / DUSK_EXT | (-1.6, -6.0, 1.9) -> (1.2, 12.0, 2.6) | 22 | street lamp + barrels (-2.9, -4.4) | street_a-c, wagon_door | wide down the street: wagon, station, lamps, puddles |
| `street_wagon` | street / DUSK_EXT | (0.2, 2.5, 1.5) -> (3.2, 8.0, 1.6) | 22 | barrels | wagon_step, wagon_door, steps_top | medium on the wagon and the station steps |

Preset start state (`state`): `drawer_big` big 1, lid 0, lift 0; `drawer_box` big 1, `box` lid 1; `card_hero` big 1, `box` lid 1, lift 1; `records_desk` fan 1. Every preset also starts the life hooks at frame 1.
Light variants rendered on the contact sheet: `measure_wide`, `measure_chair`, `records_aisle`, `records_desk`, `card_hero` in `EVENING_INT`, and `street_wide` in `DAY_INT` (the street at day-sun, for comparison). `K.build(preset=..., light='EVENING_INT')` works for any preset.

## 5b. Fix round 1 (see FIX1.md)

- **Real cast on the stand points.** `K.stage_cast(A, assign)` puts the real cast17 cards (stage `Actor` cards: unlit emission sprites, billboarded, shadow proxy; sprites through Chromium) on stand points. `assign = {mark: (story_pose, opts)}`; opts: `mirror`, `seated` ('chair' | 'bench': same head size as standing, the hidden feet float so the head centre sits at the seat's head height; `seat17` is dropped because the set has its own seats), `rim` (warm rim, default on bertillon / prefect / inspector17), `H`, `dx/dy/dz`, `expr`. `K.PRESETS[p]['cast']` (= `K.CAST_ON[p]`) is what the contact sheet uses; append `ph` to the CLI (`python3 bertillon.py render <preset> <light> out.png final 64 ph`) for the placeholder discs. Cards lean toward a low or high camera (stage `tilt`): a big near head lands up to 130 px further out than its placeholder (measure_low clerk, so he has `dx -0.3`).
- **Light hooks** (light preset or preset `over`): `sun_k` (sun scale), `frost` (skylight colour, strength), `beam_k` (shaft strength). `EVENING_INT` = sun_k 0.25, navy skylights `#2f3270`, sky `#12143a / #26295a / #3a3878`, gain 0.5, window 40 W, lamp_k 1.4 (frame mean luma about 20 % below DAY_INT).
- **Preset keys**: `lamps_up` (measure_high), `cast`, `over`. `gas_bracket(..., lit=False)`; `card_box(..., mat, lining)`; material `box_ochre`.
- **Tools**: `stand_report.py <preset> [light]` (screen position, OFF / LOW / BAND flags, overlaps, lamps in frame), `stand_report.hood_mask(preset)` (true tripod-hood coverage by a magenta repaint).
- The tripod has not moved; its black cloth drape is shorter (0.72 m instead of 0.95, hem radius 0.38 instead of 0.54) so the hem stays out of the low shots.
- Hero card art: `bertillon_tex.card` (texture `card_bertillon_dupont_v3.png`) and `cast17.card_svg` show Dupont bare-headed (ginger hair, stubble, ruddy cheeks, red neckerchief; front + true profile with an ear) and an empty glass bottle in a framed name panel, no text; `card_match.jpg` shows prop and 3D card side by side. cast17 `inspector17` moustache `tache_scale` 1.3.

## 6. Stand points (`A['marks']`, feet; z = floor level of that mark; tuple = x, y, z, facing deg, card type)

| location | marks |
|---|---|
| measure | `chair` (0.7, 2.3, 0.5, 180, seated inspector); `clerk` (1.45, 1.95); `clerk_toise` (1.7, 3.55); `prisoner_toise` (1.7, 3.1); `bench0..3` (-2.35, y 0.15 / 0.85 / 1.55 / 2.25, facing +x); `queue0` (-1.5, -1.0); `queue1` (-0.2, -0.6); `door_in` (2.45, -2.45); `door_out` (3.0, -2.4); `door_mid` (1.3, -1.5); `door_r` (-0.2, -1.6); `door_x` (-0.4, -3.3); `table` (2.0, 0.55); `armspan` (-1.55, 3.45); `tripod` (0.2, 0.35) |
| records | `desk_clerk` (-0.9, 3.4); `desk_stand` (0.3, 3.8); `aisle0` (0.2, 0.9); `aisle1` (-0.9, 5.4); `aisle2` (0.5, 5.4); `ladder_foot` (0.35, 7.3); `ladder_up` (1.0, 7.6, z 1.8); `aisle_far` (0.0, 9.5); `wall_look` (0.3, 3.0); `low_a` (0.45, 2.4) |
| reveal | `clerk` (-0.95, 1.55); `inspector` (1.15, 1.35); `pair_l` (-0.2, 2.0); `pair_r` (0.9, 2.1); `drawer_r` (-0.9, 0.9); `drawer_l` (0.9, 0.9) |
| street | `wagon_door` (3.0, 6.3); `wagon_step` (2.2, 6.0); `steps_top` (5.5, 7.0, z 0.7); `steps_low` (4.9, 8.0, z 0.3); `street_a` (-1.0, 3.0); `street_b` (0.4, 4.0); `street_c` (-2.2, 5.0); `wagon_side` (1.4, 9.5) |

## 7. Hooks (every setter takes `frame=None`: set now; `frame=N`: keyframe it)

**The keys rule**: a hook that moves must be keyed on every frame (`frame=f` for each f); un-keyed calls lose to keys, so call `clear_keys()` first when re-keying. `key_life(f0, f1)` keys all the life hooks on every frame.

| hook | what it does |
|---|---|
| `set_flicker(level=1, frame=None, seed=0)` | every gas lamp (12 in measure, 9 records, 16 street) breathes up to ~12 % x level, the glass globes too. Per-frame. |
| `set_smoke(level=1, frame=None, speed=1)` | stove smoke (measure; source `A['smoke_src']`) or chimney smoke (street, 5 chimneys): 8 soft puffs per source rising, drifting, growing and shrinking away. `level 0` hides it. Per-frame. |
| `set_dust(k=1, frame=None)` | 42 dust motes drifting in the light shaft (measure window shaft, records skylights, reveal window). `k` scales them, 0 hides. Per-frame. |
| `set_pendulum(t=None, frame=None, amp=24, period=2)` | the wall-clock pendulum (measure): +-24 degrees, 2 s period; `t` in seconds, default from the frame. |
| `set_drawer(name, open=1, frame=None)` | pull a card drawer out 0..1. Names: `big` (reveal, travel 0.78), `p0..p7`, `q0..q5` (records, travel 0.42), `pn` (the near drawer of `records_desk`). |
| `set_box_lid(name='box', open=1, frame=None)` | the hinged lid of a card box (`box`, `box2`), 110 degrees at 1. |
| `set_card_lift(t=1, frame=None)` | the hero card rises out of `box`: 0 top just over the rim, 1 lifted 0.34 and forward 0.14, tilted 22 degrees to the lamp. Move the drawer first (`set_drawer('big', 1)`). |
| `set_cards_fan(t=1, frame=None, name='fan')` | the desk cards: 0 a squared stack, 1 a 75-degree fan. |
| `key_life(f0, f1, flicker=1, smoke=1, dust=1, pendulum=True)` | keys flicker, smoke, dust and pendulum on every frame f0..f1. |
| `clear_keys()` | drops every hook key (objects, lights, glow sockets); poses stay. |
| `apply_state(A, state)` | what presets use for their start state. |

## 8. Cost (720x1280, final)

Measured (`hue.md`, `contact_work/final/*.json`): **75-133 s per frame** (street 75-98, reveal 93-106, measure 100-119, records 115-148), build 0.3-1.1 s, 12-70 k triangles. Settings: Cycles CPU 4 threads, 64 samples + OIDN denoise, adaptive sampling 0.02, 0 diffuse bounces (the ambient is emission), 2 glossy bounces (puddles only), transparent bounces 16 (the ink hull), no DOF.

## 9. Known issues

- **Colour bands are only partly met** (see the Summary at the end of `hue.md`): one tile passes every band; the others miss one or two (magenta 10-19 % in records / reveal / street, shade hue 230-238 or 255-261 instead of 240-260, p1 above 0.12 in a few). The numbers are measured on the finals, not claimed.
- Several staged heads read against dark backdrops (records canyon, the toise corner, the wagon: ring luma 55-98).
- `EVENING_INT` now reads as night. Do not stand anyone at (head off-frame or below y 880): `aisle0`, `ladder_foot` at records_ladder, `desk_*` / `wall_look` / `low_a` at records_aisle, `door_in` with `door_mid` (overlap), bench0..3 together (overlap).
- The police wagon still has shafts and no horse (P3 not done).

- Placeholder cast only; the cast cards are drawn elsewhere. The seated inspector (`chair`) uses a card height of 0.95; a real seated sprite needs its own pose.
- Textures have no mip-mapping: the setts and plank seams stay readable up to about 12 m, beyond that they shimmer slightly in motion (kept low-contrast on purpose).
- The records and measure rooms are lit by area fills plus the sun, so shadows from the fill are soft; the sun shadows are hard (0.8 degrees).
- Light shafts are flat additive prisms (a cartoon read), not volumetric.
- `street` is an exterior: its hue numbers may leave the interior band (the sky is large and saturated by design, and the lit stone is pale).

## v2. `prefecture17.py`: one connected world (PLAN_V2 §3) + takes T1-T8

Imports `bertillon.py` (the v1 kit, behaviour unchanged: v1 `build()` / presets / hooks still work; the only edit there names the ambient nodes of
`_lit_mat` and stores the palette params on the material, so `set_light_mix` can drive them; renders are identical).
`t_hooks.py` still prints `ok 14 bad ['lift mid']`, as before this change (that check predates the v1 hero-card height fix).

### v2.1 World frame (metres, Z up; street floor z 0, interior floor `FZ` = 1.2)

| part | where | built by |
|---|---|---|
| street at dusk | carriageway x -4..4 along +y (y -24..64), pavements to x +-6, left row of Haussmann blocks, café terrace (y 17-25), Morris column, kiosk, fiacre + horse, Black Maria + horse (root, `set_wagon`), 17 gas lamps, puddles, flower cart, barrels | `build_street2` |
| rooftop plate | ~300 low-poly blocks out to r 220 (ochre skin, lit amber windows 60 % as emission, cobalt zinc), chimneys, the Seine (y 95-118) with quay lamps + amber reflections, a bridge, **Notre-Dame** silhouette at (40, 140) (towers, rose, nave, flèche). No Eiffel Tower. No ink, shadow-less | `paris_roofscape` |
| Préfecture façade | outer face x = `FACADE_X` 5.45 (deviation, see v2.9), y -1.6..37.6, 3 storeys + mansard, ochre ashlar, cobalt shutters, balconies, lit windows with silhouettes, pigeons, flags (WAVE modifier), sentry box, desk gendarme, **PRÉFECTURE DE POLICE** band (11.2 x 1.15 m, z 6.15) + 2 lanterns, main door y 4.6-6.8 (`set_door('main')`), outside steps to the sill at z 0.6, the measuring room's French window y 12-14.4, **z 1.35-4.6** with balconnet and geraniums | `build_facade` |
| corridor | x 5.7-12.7, y 4.0-7.4, ceiling 5.7: 5 steps up from the door, red/ochre tiles, cobalt walls, photo walls (texture + 360 relief cards) with **PHOTOGRAPHIES — SÛRETÉ**, gas brackets (5), rolling ladder, bench, lectern; doors **SERVICE D'IDENTIFICATION** (`ident`, x 9.8-10.8, into the measuring room), **CABINET DU PRÉFET** (`prefet`), **ARCHIVES** (`archives`, end wall) | `build_corridor` |
| measuring room | v1 room + `MO` = (9.2, 12.0, 1.2): x 6.0-12.4, y 7.8-16.2. Repainted (ochre walls, cobalt dado / ceiling, honey beams, oak, cobalt rug with red border); open French casement (`set_window`), the SERVICE D'IDENTIFICATION door + sign, the ARCHIVES double door (`archive`) with **ARCHIVES →**, the **11 MESURES** chart (11 pictograms) beside the clock, the calendar **MARS 1882 / 3 MOIS** (`set_calendar`) | `build_measure2` |
| ARCHIVES hall | x 13-21, y 2-34, walls to 8.6, segmental cobalt vault to 10.2 with honey ribs and 5 skylights (y 5, 11, 17, 23, 29: shafts + dust); two storeys of cabinets: **PETIT** y 2-12.7 (0.30x0.20 drawers), **MOYEN** 12.7-23.3 (0.45x0.25), **GRAND** 23.3-34 (0.90x0.40); gallery at 4.2 m (red rail), spiral stair (19.6, 32.6), 3 rolling ladders, 3 gasoliers, hanging banners PETIT (y 9.5) / MOYEN (18) / GRAND (27.4), big **ARCHIVES** on the north wall + over both doors, 3 clerk desks with banker lamps, 4 card trolleys, overflow piles, Bertillon's desk (16.5, 27.7: banker lamp, candle, card fan `fan`), tally board **RÉCIDIVISTES 1884** (`set_tally`), reveal: drawer `big` at (13.55, 26.25, 2.4) opening +x, `box`, `box2`, hero card (`card_bertillon_martin_v2.png`: **MARTIN** + the bottle sketch), labels GRAND + number ranges on the hero row, `box_lamp` spot | `build_archive` |

Marks (stand points) are in `A['marks']` (world; the measure ones from `marks_local` + MO). Cast anchors per take are in `TAKES[take]['cast']`.

### v2.2 `world_build(take, light=None, parts=None, cutaway=None)` and the visibility sets

Each location is its own collection `loc_<name>` built with its own light preset (materials are made per location). Suns and area fills are
light-linked to their collection (receiver), and the interior suns also use it as the shadow blocker set, so the street buildings never block the
measuring-room window sun and the façade roof never blocks the skylights.

| take | parts built | light per location | ceiling cut away |
|---|---|---|---|
| T1 | roofs, street, facade, measure | ext BLUE_HOUR_EXT, measure SUNSET_INT | - |
| T2 | street, facade, corridor, measure | + corridor GASLIGHT_INT | - |
| T3, T8 | measure | SUNSET_INT | measure (bird's-eye) |
| T4 | measure, archive | SUNSET_INT, ARCHIVE_DAY | - |
| T5 | archive | ARCHIVE_NIGHT -> DAY (`set_light_mix`, g 1196-1211) | - |
| T6 | archive | ARCHIVE_DAY | - |
| T7 | archive | ARCHIVE_DAY | archive vault (top-down) |
`world_build('ALL')` builds everything (6 s, 170 k faces). Per take 0.2-0.9 s, 16-96 k faces.

### v2.3 Light presets (in `bertillon.LIGHTS`, usable by v1 `build(light=...)` too)

| preset | key | ambient (shade) / fill | rim (`RIM[p]`) |
|---|---|---|---|
| `BLUE_HOUR_EXT` | low amber sun x0.35, gas lamps x1.6, windows 70 % lit | cobalt SHADE, blue sky fill area 900 W; dome: zenith #1A3FB8, thin amber horizon | cool #9cc2ff |
| `GASLIGHT_INT` | gas brackets every 2.5 m (lamp_k 2.2), no sun | cobalt, blue transom glow, cool area fill 60 W | warm #ffb85a |
| `SUNSET_INT` | low amber sun through the French window (hard shaft + dust), window key 240 W | blue sky fill area (+30 %) | warm #ffb85a (cool #8fb4ff as `rim2`) |
| `ARCHIVE_DAY` | pale blue-white sun through 5 skylights (x0.62), banker lamps, gasoliers | cobalt, warm strip fills 300 W along both galleries, cool skylight areas | warm #ffb85a |
| `ARCHIVE_NIGHT` | moon-blue skylights, ONE banker lamp + candle on Bertillon's desk (other desk lamps off), gasoliers x0.4 | lifted cobalt (luma >= 85), strip fills 110 W | cool #9cc2ff |
`AMB_K` = 0.78 scales the painted ambient of the five presets (SET-gate calibration). `set_light_mix(a, b, t, frame, loc)` blends sun, every
material's ambient, skylight glow, beams, fills and gas lamps (through `set_flicker2`'s multiplier).

### v2.4 Signs and textures

`sign(B, text, w, h, c, n, fg, bg, font, sub, emit, ...)`: PIL texture (2x supersampled, >= 520 texels/m) on a plane whose front faces the
horizontal direction `n` (+ a painted board in `B`). Fonts: `fonts/LiberationSerif-Bold.ttf` (bundled, SIL OFL, drawn condensed 0.84; film/fonts
has no serif or condensed face), `'sans'` = film/fonts/WorkSans-Black, `'thai'` = film/fonts/Kanit_900Black. Signs emit a little (0.3-0.55) so they
read in shade. `tex_sign`, `tex_chart11`, `tex_page`, `tex_tally(n)` (sequence `tex/tally/tally_0000..0241.png`), `tex_hero_v2`, `tex_photowall`,
`tex_runner`, `tex_flag`, `tex_facade_far` cache to `tex/v2_*.png` (git-ignored, rebuilt on demand). Cap heights at the nearest planned frame:
PRÉFECTURE DE POLICE 0.6 m, ARCHIVES (north) 0.7 m, banners 0.7 m, door signs 0.18-0.25 m, drawer labels 0.06 m (read at the P1 push).

### v2.5 Hooks (`frame=None` sets, `frame=N` keys; key every frame, as in v1)

`set_door(name, open)` (`main`, `ident`, `archive`, `archives`, `prefet`), `set_window(open)`, `set_calendar(page)`, `set_tally(n)`,
`set_banner_sway(t)`, `set_wagon(t)`, `set_light_mix(a, b, t)`, `set_flicker2`, `set_smoke2` (30 chimneys + stove + 2 horse breaths),
`set_dust2` (window shaft + 5 skylight shafts), `key_life2(f0, f1)`, `life_at(g)` (stills). v1 hooks `set_drawer('big')`, `set_box_lid('box')`,
`set_card_lift`, `set_cards_fan`, `set_pendulum` work on the world. `take_state(take, g, frame)` applies every planned story hook of a take.

### v2.6 Camera paths (PLAN §4 / §5)

`cam_path(keys)`: cubic Hermite in time through keys `{g, loc, look, lens=22, hold, tension}` (Catmull-Rom tangents; first / last / `hold`
keys have zero velocity, so takes and BIGZOOMs ease in and out), look-at with world up (roll 0; straight down uses +y as up). Returns one dict per
frame: `g, loc, look, rot` (quaternion), `lens`. `path_T1() .. path_T8()` = `path_take(take)` over the take's render range with handles
(T1 0-342, T2 330-657, T3 645-856, T4 844-1051, T5 1039-1383, T6 1371-1701, T7 1689-1874, T8 1862-2052). `key_cam(cam, frames)` keys
Blender frame g + 1. Lens 22 mm everywhere (the BIGZOOM starts too). Paths: T1 roofs (45 m) -> over the smoke and the wagon -> through the
French window -> bench (track) -> back out and up to 30 m -> swoop to the wagon -> arc on the steps; T2 street -> main door -> corridor track
-> SERVICE D'IDENTIFICATION door -> low drift -> OTS -> low push (kepi rack fg); T3 bird's-eye (cutaway) -> crane to eye height -> low under
the calipers table -> into the clock; T4 out of the clock -> station track -> low at the desk -> through ARCHIVES into the hall; T5 gallery crane
-> OTS push down the aisle -> escort track -> arc to the three-shot -> push; T6 BIGZOOM 2 (8.4 m up at the south end, past the PETIT banner and the
gasolier, between the galleries) -> P1 on the card -> OTS -> three-shot -> P2; T7 low hero -> crane up to a top-down at 24 m (vault cut away);
T8 bird's-eye (cutaway) -> crane down past the gasolier -> OTS behind the crowd -> P3.

### v2.7 Size check: `cam_report(take, names=None, step=6)` / `anchor_frac(fr, feet, H)`

Per frame: every cast anchor's height in % of the frame height (feet to head top projected, 720x1280, lens from the path) + in/out of frame +
camera speed. BIGZOOM verdict (start < 5 %, end 35-60 %, both in frame), measured:

| BIGZOOM | g | start | end | verdict |
|---|---|---|---|---|
| 1 (T1, Bertillon in the French window) | 0 -> 105 | 1.2 %H | 36.4 %H | PASS |
| 2 (T6, Bertillon at the GRAND bank) | 1377 -> 1515 | 4.4 %H | 48.0 %H | PASS |
`python3 prefecture17.py report T1 T6` prints it (`STEP=` env sets the sampling). Placeholder cards: `cast_cards(take, g)`.

### v2.8 SET gate and render cost (measured)

`v2_gate/`: 24 stills (3 per take, 360x640, 16 samples + OIDN, placeholder cards), `contact_v2.jpg`, `stats.md`, and one 720x1280 frame per
location (`full720_*.jpg`). qa_stats2.py on an mp4 of the stills: **sat 0.642, vivid 82.0 %, luma 104.6** (targets >= 0.50, >= 45 %, 85-110);
no take below sat 0.59. Per take luma: T6 121 (the skylight band in the BIGZOOM 2 start, the P1 card push) and T7 84 are just outside 85-110; watch them at the TAKE gate (all others 104-110). Stills: 7-20 s each at 360x640 / 16 samples / 2 threads.

Full frame 720x1280, Cycles CPU **2 threads, 32 samples** + OIDN, adaptive 0.03 (`setup_render2`), placeholder cast:

| location (take, g) | s / frame @ 32 | s / frame @ 16 |
|---|---|---|
| rooftop plate, BIGZOOM 1 start (T1 g0) | 76 | |
| street + façade (T1 g287) | 115 | |
| corridor (T2 g400) | 123 | 62 |
| measuring room (T3 g750) | 84 | |
| archive, day (T6 g1515) | 56 | |
| archive, night (T5 g1060) | 135 | 69 |
Mean ~98 s at 32 samples -> 2144 frames ~ 58 CPU-hours (PLAN §5's "100 s/frame" case: use 11-16 teams). 16 samples halves it (OIDN holds
the flat-shaded look; check the night archive for noise first). Build per take <= 1 s; textures cache in tex/ on first run (~10 s).

### v2.9 Deviations from PLAN_V2 §3

- Façade outer face at x 5.45 (not 6.0): the v1 measuring-room wall occupies x 5.7-6.0, the façade skin sits in front of it.
- The French window is z 1.35-4.6 (to the floor) instead of 3.15-4.6, so a figure inside is visible from the BIGZOOM 1 start (the v1 sill was
  1.95 m above the room floor). The prisoners' bench stands in front of it.
- Corridor is 7 m long (x 5.7-12.7) instead of 10: the archive west wall is at x 13 per the same plan.
- PETIT banner at y 9.5 (not 1/3 of the hall) so it clears the BIGZOOM 2 line; banners hang just under the vault.
- Notre-Dame at (40, 140) beyond the Seine (y 95-118) so it falls in the T1 crane-up frame.
- 11 MESURES chart is 1.2 x 1.5 m (fits under the frieze).
- `stage_cast` v2 (yaw clamp, walk_path, contact decals) is not in this build: cast anchors + placeholder cards + `RIM` colours only.
- Bundled serif font (film/fonts has only Kanit Black and Work Sans Black).

### v2.10 SET gate fixes B1-B6 and re-gate (v2b, answers `v2_gate/QA_ART_SET_V2.md`)

**Anchors and paths (B1, B2).** `check_take(take, limit=0.75, vmax=6.0)` runs every frame: anchors in frame above 75 %H outside
`PLANNED_CLOSE` (OTS shoulders, P1-P3), anchors within 1.0 m of the lens, camera speed above 6 m/s. Result in `v2_gate/anchors_v2b.md`:
**0 unplanned hits above 75 %H in all 8 takes** (largest 73 %), no lens pass-throughs (one gendarme at 0.98 m from the T2 corridor track, a
wall-side figure), and the only frames above 6 m/s are the planned cranes (T1 1c/1d g152-278 at <= 14.8 m/s, T7 7b g1800-1867 at 15.5 m/s)
plus two 6.1 m/s moments (T4 g1035-1038, T5 g1141-1150). Changes:
- T6: inspector at (15.2, 24.35) (T5 ends there too; T7 puts him at (15.5, 27.4), behind Dupont); gendarmes at (13.95, 28.2) and (16.9, 29.6);
  P1 aims at the lifted card's measured centre (14.29, 26.14, 2.88) from 0.44 m along its normal: the card is ~74 % of the frame width; P2 on the
  inspector's new head.
- T3: no hold at g792; the low key is at g812 (20 frames, <= 5.7 m/s); the prankster walks off the rise; Bertillon steps to ML(1.0, 1.3) for 3c.
- T1: the crane-out clears the seated heads (key at z FZ + 2.9), crane end at (-2.5, -3, 15) above the carriageway (was inside a block);
  BIGZOOM 1 start (-34, -6, 34) aimed with the horizon in the top fifth.
- T5: the night crane starts on the NW gallery rail (14.75, 32.3, 7.0) and lands behind Bertillon's desk, so the OTS push down the aisle turns
  only 20 deg (no whip); the push ends on the east side (19.2, 16.8); the escort lanes are x 15.9 / 16.6 / 17.3, at least 1.9 m from the track.
- T7: the end is a high bird's-eye from the south (17, 5, 23) -> (17, 21, 1.2), so every banner reads upright (a straight top-down shows the
  south banner upside down whatever its orientation).

**T1 hook frame (B3).** Ground plane of setts under the whole plate (no void), lamp dots at every block corner, `tex_zinc2` seamed zinc on all
roofs, dormers on all four slopes of the blocks within 90 m and on the back slopes of the street rows (`roof_back`), the sky dome with its thin
amber horizon and Notre-Dame (moved to (120, 135)) in frame, all v1 window glows amber (`glow_win` 1.7, never white), a red/amber awning over
the French window and a warm lamp inside it (`win_glow`; T1 window key 300 W), so the French window is the brightest pool. `report T1 T6`:
BIGZOOM 1 1.6 -> 36.4 %H PASS, BIGZOOM 2 4.4 -> 48.0 %H PASS.

**Foreground (B4).** Measuring room: ledgers, kepi on the floor, spittoon, open calipers case, dropped cards, a rug and a crate by the doors.
Corridor: runner and photo-box piles. Archive entry: a card trolley and an overflow pile. Street: a refuge island with a lamp post (the 1d
foreground), smaller puddles, more crowd anchors.

**Light (B5).** Archive shafts visible: `beam_k` 2.4 (day) / 2.6 (night) with pale-blue / moon-blue beam colour, 34 larger motes per shaft,
the shafts land at x 17.9-20.3 (east of every cast anchor). Night vault: two cool `vault_fill` areas (1100 W at night) light the vault and ribs.
Fanlight `glow_fan` 1.4 (no white transom), right-side street lamps 420 W, door lanterns 45 W. Per-take overrides `TAKE_OVER`: T1 measure
(window), T6 archive (shade x0.8, fills 220 W, beams 0.5: on the hall axis the five additive shafts stack into haze), T7 archive (shade x1.16).
`Loc` accepts `shade_mul`. Ceilings in `TAKE_CUTAWAY` hide only while the camera is above them (`cutaway_at(frame)`).

**Signs.** Corridor side: `IDENTIFICATION` (2.9 x 0.6 m, cap 0.37 m), whole in frame T2 g445-458 (it then leaves through the top as the camera
pushes under it into the door). Room side: `SERVICE D'IDENTIFICATION` 3.9 x 0.5 m (cap 0.31 m), whole in T3 g736-760.

**stage_cast v2 (B6).**
- `floor_z(x, y)`: walkable height (street 0, pavement 0.14, the 3 façade steps, the 0.6 sill, the 5 corridor steps, interiors 1.2). Feet and
  contact shadows of the placeholder cards and of `stage_cast2` stand on it.
- `yaw_clamp(face_deg, pos, cam_loc, max_dev=35)`: the card turns toward the camera by at most 35 deg from the story facing; the rest of the turn
  goes into the puppet `yaw` key (`pose_yaw`, +-0.6); `back` = camera more than 110 deg off the facing; `yaw_fixed` is the value for
  `stage.actors.Actor.yaw_fixed` (card yaw 0 = facing -y).
- `walk_path(keys, stride=0.72)`: per frame pos on `floor_z`, heading, speed, gait `phase` from the distance walked (feed `cast17.cycle(cast,
  phase, 'walk')`: the planted foot does not skate), `planted` foot, `idle`.
- `BACK_VIEW` (OTS shoulders: T2 Bertillon g555-625, T5 Bertillon g1100-1150, T6 Dupont g1546-1616, T8 gendarme g1958-2052) and
  `is_back(take, anchor, g)`. cast17 has no back art (cast17/API.md), so `stage_cast2` mirrors the pose and puts a dark back-of-head disc and coat
  silhouette in front of the card (`_back_cover`); the placeholder cards show a dark head.
- `stage_cast2(take, g, assign)`: bertillon.stage_cast + all of the above for frame g (call it on every frame of a frame-by-frame render).
  `cast_face(take, anchor, g)`: explicit `face`, else the walking direction, else toward the take's first camera.

**Re-gate material (`v2_gate/`):** `contact_v2b.jpg` (18 stills: the 14 requested + T1 g0218, T2 g0450, T3 g0750), `*b.jpg`, `stats_v2b.md`,
`anchors_v2b.md` (frame-size table, sign check, BIGZOOM verdicts), `full720_roofs_bigzoom_v2b.jpg`, `full720_archive_night_v2b.jpg`,
`AB_archive_night_16_vs_32.jpg`. qa_stats2 on the re-gate stills: **sat 0.629, vivid 75.7 %, luma 109.1** (saturation not pushed: 0.64 -> 0.63).
Per take on these frames: T1 120 (interiors through the bright window), T6 121 (the P1 frame is the near-white MARTIN card filling the frame; the
BIGZOOM start fell from 137 to 121), T7 88, the others 103-108.

| full frame 720x1280, 2 threads | 32 samples | 16 samples |
|---|---|---|
| rooftop plate, BIGZOOM 1 start (T1 g0) | 67 s | 36 s |
| archive night (T5 g1060) | 145 s | 73 s |
16 vs 32 samples on the night archive: identical numbers (sat 0.606 / 0.608, luma 97.3 / 97.4) and no visible noise difference at 1:1 (OIDN
holds the flat-shaded look). **Recommendation: 16 samples + OIDN** for all takes.

Known after v2b: T1 g218 (crane top) still does not show the whole PRÉFECTURE DE POLICE band (QA non-blocking note); at T3 g796 a gasolier
crosses the room-side sign for a few frames; placeholder cards seen at the clamp limit read thin (expected: the real puppets carry the rest of the
turn in `pose_yaw`).

### v2.11 B7: card facings (`face_keys`, `check_face`) and `stage_cast2` on the real cards

- **Face keys.** `face_keys(take)` gives every anchor of every take per-segment story facings `[(g, deg azimuth)]`, linear between keys.
  - They are generated from the planned camera path. Each key is the weighted circular mean of the direction to the camera over its segment:
    weight 1 where the card is in frame above 15 %H, 0.05 elsewhere.
  - Keys come every 20 frames, and every 8 frames for the hero inside `STRICT` windows.
  - `FACE_OVERRIDE` holds hand keys. In T1, Bertillon (-25°) and the bench prisoners (-15°) face into the room, constant. The camera flies in
    through the window behind them, which is a back view on g60-96 and g158-186.
  - Export: `write_face_keys()` writes `v2_gate/face_keys.json`.
  - `cast_face()` uses the keys, which also drive `yaw_clamp`. Walkers keep the key facing; give the puppet cycle its direction from
    `walk_path()['heading']`.
- **Back views.** `BACK_VIEW` adds T2 thief g330-386 (2a), T1 window passes, and T2 Bertillon g530-657 (the OTS, extended with the measured
  prisoner as OTS foreground g600-657).
- **`check_face(take)`.** It FAILS when:
  - a card in frame above 15 %H, not on `BACK_VIEW`, is more than 60° off the camera, or
  - the speaker / hero is more than 35° off the camera in a `STRICT` window: lip-sync g493-651 and g1128-1196, BIGZOOM ends g97-148 and
    g1500-1530, P1, 6c g1545-1616, P2, P3.

  It also reports the card yaw rate. All 8 takes PASS (`v2_gate/check_face_v2c.md`); the largest error anywhere is 39°, and 6° in a strict
  window. CLI: `python3 prefecture17.py faces`.
- **`stage_cast2(take, g, assign)`.** It is its own implementation, posing at the scene's current frame.

  Per card it does this:
  - the story pose, with `opts` expr, `talk` (cast17.speak, quote windows only), mirror, and seated `chair | bench`;
  - the clamped facing: `Actor.yaw_fixed`, with the rest of the turn in the puppet `yaw`;
  - feet on `floor_z`;
  - the v2 rim colour of the location preset;
  - on `BACK_VIEW` frames, a mirrored pose plus a dark back-of-head disc and coat panel built from the card's own head anchor
    (`actors.local_to_world`).

  Then it renders the sprites for that frame and syncs the cards. The camera and hooks are set by `shot()` / `key_take()`.
- **Real-cast stills** (720x1280, 16 samples, `python3 prefecture17.py real <take> <g> out.png`, assignments in `REAL_STILLS`):

  | still | what it shows | time |
  |---|---|---|
  | `v2_gate/real_T1_g0105.jpg` | BIGZOOM 1 end: Bertillon front-on, calipers at the prisoner's ear, prisoners front-on | 87 s |
  | `v2_gate/real_T2_g0560.jpg` | inspector lip-sync, front-on, talking mouth, clear of every prop | 83 s |
  | `v2_gate/real_T6_g1600.jpg` | 6c: Bertillon with the card, inspector arms crossed, Dupont in back view as the OTS foreground | 71 s |
  | `v2_gate/real_T6_g1690.jpg` | P2: inspector jaw-drop front-on | 67 s |

  Mouths are closed outside the quote windows (the jaw-drop is the planned held shape). No back-of-head cover sits on a speaker.
- **T2 2d/2e re-framed for the real cards.**
  - The inspector stands at ML(-0.2, 1.4) from g545, clear of the tripod.
  - The OTS camera sits behind Bertillon's right, over the clerk's table (ML(2.3, 0.9) → ML(2.25, 1.0)). That keeps the measured prisoner
    and Bertillon's calipers off the speaker.
  - 2e is a slow 22 → 28 mm push-in on the same axis, ending with the inspector at 55 %H. The corner has no low path.
- **Known:**
  - The cast17 sitting poses on `seated='bench'` read as standing figures in front of the bench (grounded, feet on the floor).
  - Card yaw rates above 2°/frame occur only on close orbit passes. The largest is 12°/frame on T8 crowd2 during the crane-down; QA-art
    checks it on the 0.5 s tiles.

