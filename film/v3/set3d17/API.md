# v3/set3d17: the film 17 set ("Bertillon", Paris police 1882-83) (bpy 5.x, Cycles CPU)

Four locations, 14 camera presets, 3 light presets, life hooks, stand points for 1-4 cast cards. Built from code only (numpy + PIL textures, batched
meshes). **No depth of field anywhere. No readable text anywhere** (notices, ledgers, the Bertillon card and the sign board are greeked or blank).

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
| `measure_wide` | measure / DAY_INT | (-1.9, -3.9, 1.5) -> (0.8, 2.4, 1.35) | 22 | gas standard + stool with ledgers (-2.55, -2.9) | bench1, bench2, chair, clerk, prisoner_toise | eye-level wide: bench queue left, chair + tripod centre, toise right |
| `measure_chair` | measure / DAY_INT | (2.0, 0.2, 1.5) -> (0.7, 2.4, 1.2) | 22 | the tripod camera + clerk's table corner | chair, clerk | medium on the chair, head rest and calipers table |
| `measure_high` | measure / DAY_INT | (2.9, -3.8, 3.55) -> (-0.4, 1.9, 0.5) | 22 | gas bracket at the corner | bench0-3, queue0, chair | high angle over the room, the queue on the bench |
| `measure_door` | measure / DAY_INT | (-1.7, 0.9, 1.5) -> (3.2, -2.4, 1.3) | 22 | ledger table corner | door_in, door_mid, queue1 | from inside toward the door: entrances |
| `measure_low` | measure / DAY_INT | (-0.45, -0.3, 0.5) -> (0.9, 2.4, 1.5) | 22 | ledgers + crate on the floor | chair, clerk | low-angle hero of the clerk at the chair |
| `records_aisle` | records / DAY_INT | (0.75, -3.2, 3.9) -> (-0.2, 6.5, 2.0) | 22 | gas bracket + crates | aisle0-2 | high, off-centre down the cabinet canyon |
| `records_low` | records / DAY_INT | (0.1, -0.8, 0.55) -> (-0.9, 6.0, 3.2) | 22 | crate stack + stool | low_a | low angle up the cabinet wall |
| `records_desk` | records / DAY_INT | (0.9, 0.6, 1.5) -> (-0.8, 2.6, 1.0) | 22 | a drawer pulled out (`pn`) + crate | desk_clerk, desk_stand | medium at the desk: fanned cards (`fan` 1), green lamp |
| `records_ladder` | records / DAY_INT | (-0.2, 4.8, 1.4) -> (1.1, 7.6, 2.4) | 22 | crates + ledgers | ladder_foot, ladder_up | the rolling ladder on the right run |
| `drawer_big` | reveal / DAY_INT | (0.6, 2.6, 2.2) -> (0.1, 0.5, 1.15) | 22 | stool + ledgers (0.65, 2.15) | clerk, inspector | the big drawer pulled out, many cards |
| `drawer_box` | reveal / DAY_INT | (0.15, 1.4, 2.2) -> (0.0, 0.45, 1.1) | 22 | stool + ledgers | clerk | a smaller box inside the drawer (lid open), fewer cards |
| `card_hero` | reveal / DAY_INT | (0.3, 1.5, 1.75) -> (0.0, 0.7, 1.3) | 22 | stool + ledgers, the lamp table at the left | - | one Bertillon card lifted in lamplight, calipers beside |
| `street_wide` | street / DUSK_EXT | (-1.6, -6.0, 1.9) -> (1.2, 12.0, 2.6) | 22 | street lamp + barrels (-2.9, -4.4) | street_a-c, wagon_door | wide down the street: wagon, station, lamps, puddles |
| `street_wagon` | street / DUSK_EXT | (0.2, 2.5, 1.5) -> (3.2, 8.0, 1.6) | 22 | barrels | wagon_step, wagon_door, steps_top | medium on the wagon and the station steps |

Preset start state (`state`): `drawer_big` big 1, lid 0, lift 0; `drawer_box` big 1, `box` lid 1; `card_hero` big 1, `box` lid 1, lift 1; `records_desk` fan 1. Every preset also starts the life hooks at frame 1.
Light variants rendered on the contact sheet: `measure_wide`, `measure_chair`, `records_aisle`, `records_desk`, `card_hero` in `EVENING_INT`, and `street_wide` in `DAY_INT` (the street at day-sun, for comparison). `K.build(preset=..., light='EVENING_INT')` works for any preset.

## 6. Stand points (`A['marks']`, feet; z = floor level of that mark; tuple = x, y, z, facing deg, card type)

| location | marks |
|---|---|
| measure | `chair` (0.7, 2.3, 0.5, 180, seated inspector); `clerk` (1.45, 1.95); `clerk_toise` (1.7, 3.55); `prisoner_toise` (1.7, 3.1); `bench0..3` (-2.35, y 0.15 / 0.85 / 1.55 / 2.25, facing +x); `queue0` (-1.5, -1.0); `queue1` (-0.2, -0.6); `door_in` (2.45, -2.45); `door_out` (3.0, -2.4); `door_mid` (1.3, -1.5); `table` (2.0, 0.55); `armspan` (-1.55, 3.45); `tripod` (0.2, 0.35) |
| records | `desk_clerk` (-0.2, 3.35); `desk_stand` (0.4, 2.6); `aisle0` (0.2, 0.9); `aisle1` (-0.3, 4.6); `aisle2` (0.5, 5.4); `ladder_foot` (0.35, 7.3); `ladder_up` (1.0, 7.6, z 1.8); `aisle_far` (0.0, 9.5); `wall_look` (0.3, 3.0); `low_a` (0.45, 2.4) |
| reveal | `clerk` (-0.95, 1.55); `inspector` (1.15, 1.35); `pair_l` (-0.2, 2.0); `pair_r` (0.9, 2.1) |
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
- `EVENING_INT` differs from `DAY_INT` only in key colour, lamp strength and the window sky (barely visible); it is a preset hook rather than a separate look yet.

- Placeholder cast only; the cast cards are drawn elsewhere. The seated inspector (`chair`) uses a card height of 0.95; a real seated sprite needs its own pose.
- Textures have no mip-mapping: the setts and plank seams stay readable up to about 12 m, beyond that they shimmer slightly in motion (kept low-contrast on purpose).
- The records and measure rooms are lit by area fills plus the sun, so shadows from the fill are soft; the sun shadows are hard (0.8 degrees).
- Light shafts are flat additive prisms (a cartoon read), not volumetric.
- `street` is an exterior: its hue numbers may leave the interior band (the sky is large and saturated by design, and the lit stone is pale).
