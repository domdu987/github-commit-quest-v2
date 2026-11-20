# v3/set3d21: the film 21 set ("Stirling", the Forth valley, 11 Sept 1297) (bpy 5.x, Cycles CPU)

A lit 3D world seen through flat 2D puppet cards: one sunny morning in the Forth valley. Real geometry, one warm low sun from the south-east, blue-violet shade, flat
low-poly matte props, a teal layered river. **No depth of field, no haze or blur (distance is colour only), no readable text.** 15 camera presets, hooks that every render team can key
per frame, stand points for the cast. Built from code only (numpy + PIL textures, batched meshes). Runs from this folder alone (needs `bpy` 5.x, `numpy`, `Pillow`).

## Files

| file | what |
|---|---|
| `stirling.py` | the module: materials, light, terrain/river analytics, props, the camp, the bridge, hooks, presets, camera, render, placeholders, CLI |
| `stirling_tex.py` | drawn textures (sky with flat clouds, wood grain, brush-stroke meadow). Cached in `tex/` (git-ignored, rebuilt on demand) |
| `stirling_hue.py` | colour numbers per frame (hue families, sat, val, dark, shade hue, black point) + `sharp_bands()` |
| `make_contact.py` | renders every preset (final or draft) into `contact.jpg` / `contact_small.jpg` + `hue.md` |
| `make_board.py` | the old three-still style board (hill_over, camp_bank, valley_loop) |
| `t_hooks.py` | hook test: `python3 t_hooks.py` -> `ok 21 bad []` |
| `contact.jpg`, `contact_small.jpg`, `hue.md` | the review sheet (15 tiles, 720x1280, label strip, cyan line at y 880) and the numbers |
| `styleboard/` | the style board, `QA_ART.md` (the review this build answers), `NOTES.md` |
| `cache/` | terrain tables (`terrain{A,M,B}_v<TERRAIN_V>.npz`, git-ignored, first run about 15 s, then loaded) |

## 1. Conventions

- **1 unit = 1 m. One D = one character height = 1.7 units** (`K.D`). Card heights in units: `HEIGHT = scot 1.70, wallace 1.92, moray 1.80, cressingham 1.78, surrey 1.66, knight 1.78, foot 1.68, archer 1.66, squire 1.55`. A card of height H at distance d is `H * 782 / d` px tall at 22 mm (focal 782.2 px; `H * 782 * lens / 22 / d` for other lenses).
- Z up, water level z = 0. x east, y north. Camera 36 mm sensor, AUTO fit, 720x1280. **Lens: 22 mm everywhere except `hill_over` (32 mm) and `camp_bank` (30 mm)**: QA-art needed the 280 px bridge and the knights readable there; every other preset is 22 mm as the camera rules say.
- Every preset has a foreground prop 1-2 m from the lens (`fg`), stand points (`marks`) for the cast, and room to drift (the push/slide in the shot plan fits the scene: nothing is placed inside the move path).
- Placeholder cast: `stage_placeholders(A)` puts a near-white head `#fef7f6` with a plum ring on a flat coloured body at every stand point, turned to the camera. Head = 0.3 of the card height. `build_for_cli` stages them for presets that have marks.
- Head screen positions: the `<out>.json` that `cli_render` writes has `heads: {mark: {cx, cy, chin, dist}}` (px at 720x1280). The stand points are placed so heads are at cy 450-800; check the table in section 6 (a few are at 760-800: the card chin may reach 830) and call `head_report()` after your first frame. Hiding foreground props: objects are named `fg_generic_<material>` (posts and spears in `fg_generic_wood` / `fg_generic_steel`, gorse and reeds in `fg_generic_g_*`, rocks and heather in `fg_generic_r_*`).

## 2. Geography (one coherent valley)

| thing | where |
|---|---|
| the main river | runs west to east through y = 0 (36-46 m wide, gentle bends); `river_query(X, Y)` gives sd (negative in the water), arc length, flow |
| the wooden bridge | along x = 0, y -34..38, deck z = 1.75 (`DECK_Z`), 2.6 m wide (two horses), rails, trestle piers with foam collars and V wakes; the causeway runs north of it (y 17..62, x +-5, 0.45 m up) |
| the loop (the trap) | a pear-shaped meander north of the bridge: leaves the main river at x -33 and rejoins at x +33, reaches y 210, x -86..84, channel 25-35 m wide; the meadow inside is flat (the bottle), the bridge + causeway are its neck |
| Abbey Craig | the hill at (200, 190), 72 m high: grey crag (stepped, south-west face), heather, bracken, gorse, red-trunk Scots pines; the Scots' ledges: the shelf (131, 131, z 15.6), `PAD2` (137, 137, z 19), `PAD` (158, 148, z 44.5, the lens of hill_over) |
| the English camp | on the south bank (y < -20), x -130..130: 14 + 5 pavilions with pennants, tent clusters, horse lines, carts, racks, fires, Cressingham's money table at (-13, -26.9) |
| Stirling castle rock | far south-west at (-330, -480), 70 % size, small castle on top (`build_castle`) |
| farmland | irregular fields (8 tints, furrows, hedgerows), 10 farmsteads with smoke, lanes; the Ochil hills north, calm 3-band tint |

## 3. Functions

```python
import sys; sys.path.insert(0, ".../film/v3/set3d21"); import stirling as K
A = K.build_for_cli('camp_table')     # build(preset) + foreground + troops + placeholders; returns the anchors dict A
A = K.build(preset='camp_table')      # the bare scene + camera (no placeholders, no fg: call K.PRESETS[p]['fg'](A, K.PRESETS[p]) yourself)
K.render('/tmp/f.png', 'final')       # 720x1280, 64 samples, OIDN, 4 threads, then grade()  |  'draft' = 360x640, 20 samples
K.head_report(A)                      # {mark: {cx, cy, chin, dist}} (call after render/setup_render)
K.project(cam, (x, y, z))             # world -> (px x, px y, depth) at 720x1280; call K.setup_render(scene, 'final') first, then bpy.context.view_layer.update()
```
CLI: `python3 stirling.py render <preset> [-] <out.png> [final|draft] [samples]` (the `-` is an optional no-op placeholder for a light name; there is one light; mode other than `final`/`draft` is an error), `python3 stirling.py list`. Example: `python3 stirling.py render bridge_deck - /tmp/f.png draft`. `A` holds `marks`, `cam`, `camp` (`table`, `fires`, `pav`), `scale_beam`, `chest_lid`, `troops`.
Other public functions: `new_scene(light, over)`, `Batch` (`box, cyl, sphere, rock, mesh, quad, tri, prism_roof, xf, wpt, finalize`), `get_mat(key)`, `ground(x, y)` (terrain z), `sd_at(x, y)` (distance to the water line: negative in the river), `river()`, `hill_h`, `rel_xy`, `mark_at`, `mark_px`, props `pavilion, bell_tent, ridge_tent, banner, campfire, cart, weapon_rack, barrel, sacks, horse, knight_pair_column, spear, gorse, reed_cluster, pine, oak, boulder, crag_group, farmstead, scots_slope_line, spear_wall`.

## 4. Hooks (all keyable per frame: call the hook with the frame's value, then render; they only set scene values)

| hook | what | notes |
|---|---|---|
| `K.set_flutter(t, amp=1.0)` | every banner flutters (Wave modifier phase keyed by `t` seconds; amp scales the ripple) | live banners = `K.STATE['anim']['flags']`; poles bob a few cm; 3-4 objects per banner |
| `K.set_smoke(t, speed=0.12)` | every smoke column (camp fires, farms): puffs rise, grow and fade out in a loop (cycle = 1/speed s) | columns in `K.STATE['anim']['smoke']`; flat grey emission, no shadow |
| `K.set_flow(t, speed=1.0)` | the water: current streaks, foam streaks and the sun glitter twinkle | the glitter uses a 4D voronoi; one call per frame |
| `K.splash(x, y, age, size=1.0, z=0.0, name='a', seed=0)` | a spray crown on the water `age` s after the impact: white emission-lit foam (never shaded), 15 separate tapered spikes flaring out 30-45 deg and ending in beads, 8 inner spikes, a thick central column with a bead cap, mist discs, an expanding foam ring and 80 ballistic droplets (r 0.06-0.14 m). `age < 0` or `> 1.6` removes it. Size 1 = a man jumping (crown 1.5 m at age 0.3); river_low uses size 1.8 at ages 0.15/0.3/0.45; `splash_strip.py` renders ages 0.1/0.25/0.4/0.6/0.9 | calling again with the same `name` replaces it (never stacks); use one name per jumper; size 1 = a man jumping |
| `K.set_scale_tip(A, deg)` | Cressingham's coin scale: tips the balance beam (deg, + = right pan down) | the beam is its own object with its pivot |
| `K.set_chest_lid(A, deg_open)` | the coin chest lid: 72 = open, 0 = slammed shut | hinge object |
| `K.place_troops(A, where, n, kind=None, seed=0, cb=None, horses=True)` | English troops by COUNT: `'bridge'` (n mounted knights two by two on the deck, 3D riders), `'causeway'` (n foot soldiers, 3 abreast north of the bridge), `'meadow'` (n foot soldiers in ranks in the loop meadow), `'south'` (n queued on the south road) | returns `[(x, y, z, kind, scale)]`. With `cb=f` the list goes to `f(items)` so a team can place its real cast sprites at those points; without `cb` the default placeholder cards are staged (bridge: the 3D riders; `horses=False` hides them). Re-calling the same `where` replaces the set |

`python3 t_hooks.py` builds `camp_table` and checks every hook moves vertices, node values, rotations or object counts (`ok 21 bad []`). Preset start state: `bridge_*`, `valley_wide`, `bridge_end_north` start with troops (`troops` key); `river_low` starts with three splashes at ages 0.35 / 0.55 / 0.8.

## 5. Light model

Per surface: `Diffuse(art) lit by the sun + Emission(shade)`: the ambient is injected as emission, so shade is blue-violet (shade hue 240-260) and never brown. One hard warm key (`MORNING`: colour (2.35, 1.82, 0.98), 24 deg high from the south-east; `sun_k` scales it per preset: 1.6-2.1), long shadows, matte (no glossy). Distance is colour only: far terrain mixes at most 20-25 % toward `#a39cec`. The water is layered (turquoise shallows `#5cc8b4` to deep teal `#0f5e74`, foam, current streaks, glitter). `over=dict(...)` in a preset overrides single numbers (`sun_k, key, shade, tint, lift, world, haze_max, foam_k, glit_s, glit_t, glit_stretch, wake_k, reed_k, sun_dir`). Banners and smoke cast no shadow.

## 6. Presets (`K.PRESETS`)

Camera, look-at, foreground prop, stand points with their head centre in screen px (720x1280), and the move the preset has room for. `z = ground + d` means the camera is `d` above the terrain at that point.

| preset | loc | camera -> look | lens | foreground prop | stand points (head cx, cy) | room to drift | cost |
|---|---|---|---|---|---|---|---|
| `hill_over` | hill | (160.0, 150.0, z = ground + 2.70) -> (0.0, 2.0, -20.0) | 32 | two spear shafts (1.6-1.8 m), two gorse bushes, a boulder at the bottom edge, one pine at the left edge | `s1` (92, 758), `s2` (598, 653), `s3` (641, 588), `s4` (121, 567), `s5` (56, 664) |  | 84 s render, 4 s build |
| `hill_eye` | hill | (128.0, 128.0, z = ground + 1.75) -> (144.0, 144.0, 20.5) | 22 | spear 2.6 m, gorse 2.4 m | `s1` (150, 665), `s2` (265, 659), `w` (370, 637), `s3` (500, 657), `s4` (590, 665) | slide 40 px/s; snap push x1.4 on s2 | 135 s render, 3 s build |
| `hill_low` | hill | (118.0, 112.0, z = ground + 1.40) -> (140.0, 134.0, 19.0) | 22 | gorse 1.6 m, gorse 1.9 m, rock 2.2 m, spear 1.8 m | `s1` (102, 763), `s2` (242, 682), `horn` (388, 747), `w` (509, 636), `s3` (614, 685) | pull-out 7 %/s, tilted up 14 deg | 84 s render, 3 s build |
| `bridge_deck` | bridge | (-2.7, -2.4, z 3.0) -> (0.6, 1.6, 2.9) | 22 | post 1.1 m | `k1` (190, 563), `k2` (520, 570) | push 8 %/s | 101 s render, 2 s build |
| `bridge_high` | bridge | (-5.0, -62.0, z 24.0) -> (0.0, 6.0, 1.0) | 22 | - | - | push along the bridge 8 %/s; snap pull-out x0.7 | 88 s render, 2 s build |
| `bridge_end_north` | bridge | (-2.0, 50.0, z 4.6) -> (0.0, 22.0, 1.8) | 22 | gorse 2.0 m, reeds 2.0 m | `e1` (174, 774), `e2` (419, 730), `e3` (595, 751), `e4` (301, 701) | push 8 %/s | 67 s render, 2 s build |
| `bridge_end_south` | bridge | (-2.0, -37.5, z 2.6) -> (0.0, -31.0, 2.6) | 22 | spear 2.4 m | `k1` (215, 538), `k2` (505, 549) | snap push x1.4 (16 f) | 71 s render, 2 s build |
| `valley_wide` | valley | (445.0, 244.0, z 361.0) -> (64.0, 44.0, 0.0) | 22 | - | - | crane down + push 6 %/s | 106 s render, 35 s build |
| `valley_loop` | valley | (-72.0, -133.0, z 229.0) -> (12.0, 36.0, 0.0) | 21 | - | - |  | 108 s render, 33 s build |
| `valley_river` | valley | (38.0, -24.0, z = ground + 2.10) -> (105.0, 28.0, 4.0) | 22 | reeds 2.2 m, reeds 2.0 m, rock 2.4 m | `e1` (130, 762), `e2` (601, 783) | push 7 %/s + slide | 91 s render, 35 s build |
| `camp_wide` | camp | (-78.0, -96.0, z 13.0) -> (12.0, -52.0, 2.0) | 22 | rope 1.8 m, pole 2.2 m | `k1` (203, 733), `k2` (518, 709) | slide 50 px/s + push | 82 s render, 3 s build |
| `camp_table` | camp | (-13.0, -30.0, z = ground + 1.30) -> (-13.0, -26.5, 1.7) | 22 | barrel 2.4 m | `cress` (365, 540) | push 8 %/s; hooks: set_scale_tip(A, deg), set_chest_lid(A, deg) | 174 s render, 3 s build |
| `camp_bank` | camp | (-95.0, -15.0, z = ground + 2.00) -> (-2.3, 22.5, -16.5) | 26 | banner pole with its banner at the right edge, a barrel, reeds and tent pegs | `cress` (191, 585), `surrey` (640, 556), `e0` (56, 572), `e1` (335, 522), `e2` (441, 502), `e3` (541, 516), `e4` (612, 503) |  | 87 s render, 3 s build |
| `riverbank` | riverbank | (-27.0, 54.0, z = ground + 1.80) -> (-28.0, 22.0, -3.5) | 22 | reeds 1.7 m, gorse 2.2 m | `e1` (81, 574), `e2` (215, 559), `e3` (129, 540), `e4` (42, 520) | slide 40 px/s + push; the channel is on the right: splash() points in PRESETS["riverbank"]["splashes"] | 78 s render, 3 s build |
| `river_low` | riverbank | (-26.0, 46.0, z = ground + 0.90) -> (-44.0, 44.0, 0.9) | 22 | reeds 1.4 m, reeds 1.6 m, rock 1.8 m | - | quick push; splash() crowns at pr["splashes"] | 73 s render, 3 s build |

Notes per preset:
- `hill_over`: the Scots stand on `PAD` (a levelled ledge 44 m up) with their backs to us; the far bridge (x 235-510, y 520-570, about 280 px, knights two by two) is the hook; castle rock upper left; run path coloured on the slope for shot 22 (the lens rides down it).
- `hill_eye`, `hill_low`: on the shelf (`PAD2`) in front of the Scots line; `hill_low` looks up 14 deg with sky above the pines.
- `bridge_deck`: outside the rail at deck height; the rail post is the foreground; two knight stand points on the deck. `bridge_end_south`: the south gate (camp pavilions cleared). `bridge_end_north`: from the meadow side down the causeway to the bridge mouth; `troops` (bridge 10, causeway 12) are settable; for the spear wall (shot 23) call `K.spear_wall(14, 2, rs)` or place the Scots cards across x -9..9 at y 27-29 (the neck is 31 m wide: the slot is kept clear).
- `bridge_high`: 24 m up over the south bank, looking along the bridge; troops on the bridge by count.
- `valley_wide`: the whole valley from the north-east, 361 m up; loop, bridge, camp, hill, castle rock far left. `valley_loop`: 229 m up, pitch 50 deg, the bottle; the Scots line (90 tan figures with spear tips on the hill) and the spear wall slot at the north end of the bridge; troops by count (`crowd_loop` default = 120 placeholder figures; call `place_troops(A, 'meadow', n)` for your own count after removing `crowd_*` objects).
- `valley_river`: eye level 2 m above the south bank looking north-east across the river at the hill with the Scots line.
- `camp_wide`: 13 m up over the camp, a parade of 4 caparisoned knights (3D) past tents and banners. `camp_table`: Cressingham stands behind the table (`cress`), chest lid and scale hooks work; remove `cress` for the empty ending table (do not stage him: pass `only=` to `stage_placeholders`, or delete `ph_cress*`).
- `camp_bank`: south bank at the water, bridge x ~210-520 y ~430-470 (about 310 px long, 37 px tall, 4+ knight pairs), hill with the Scots line at the left, pavilions at the right, Cressingham x 178, Surrey x 640, nothing in x 260-560 at head height.
- `riverbank`, `river_low`: the loop's west channel; `riverbank` has water on the right (the jump), the bridge in the background; `river_low` is 0.55 m above the water, with reeds and room for splashes: `K.splash(-34.0, 41.0, age)` etc. (the three points in `PRESETS['river_low']['splashes']`).

## 7. Cost

Terrain tables load in 0.2 s (first run builds them in about 15 s); scene build 3-40 s (valley presets 35 s because of the farms and hedges, the others 3-5 s). One final frame (720x1280, 64 samples, OIDN) takes 85-130 s on 4 cores (valley_loop about 105 s + 35 s build); a draft (360x640, 20 samples) 8-15 s. Render time is dominated by the 600k-1M triangles of grass/heather; to render a frame sequence in one process, build once and call the hooks + `K.render()` per frame (the build is the only slow part). Hooks take 1-50 ms.

## 8. Gotchas

- `K.project()` needs `K.setup_render(scene, ...)` (aspect) and `bpy.context.view_layer.update()` first; `head_report()` is only right after a render.
- Banners are live: do not merge them; `set_flutter` must be called after `build` (it uses the Wave modifier of the banner cloth objects).
- `place_troops` and `splash` delete their previous objects by name prefix (`troops_<where>`, `splash_<name>_`); do not rename them.
- The pad ledges (`PAD`, `PAD2`) change the terrain near the Scots: do not move the hill presets' cameras without re-checking the view over the ledge (the bridge hides behind the ledge edge if the camera is too far back).
- Placeholder heads are flat cards turned to the camera at render start; if the camera moves a lot during a drift, call `stage_placeholders(A)` again or use your cast sprites (billboards).
- No glossy anywhere; the water glitter is emission only. Do not add a world volume or fog: QA-art rejects haze.
- 4 cores: use `threads_mode FIXED, threads 4` (the render function does).

## 9. Final grade: the VIVID stage (client rule QA_TEAM §G / §I 3)

`grade()` ends with a per-preset VIVID stage `(gamma, sat)` from the dict `K.VIVID` (`STATE['vivid']` overrides it, which is how `cam_path` eases it): frame saturation >= 0.47-0.50 and mean luma 85-110 as `film/qa_stats.py` measures them (mean of (max-min)/max and mean grey at 90x160); the vivid share (pixels with (max-min)/max > 0.5) is >= 45 %. Current valley entries: `valley_wide` (1.11, 1.83), `valley_loop` (1.07, 1.71), `valley_river` (2.28, 1.18) (measured on 24-sample finals at 0.54 / 54 %, 0.54 / 56 %, 0.55 / 51 %). River_low is capped at gamma 1.9 (its tile stays bright). Do not remove or bypass VIVID; if you change a preset's light, re-measure and retune its entry.

## 10. Connected world and camera travel (many long takes, few cuts)

```python
A = K.build_world(['valley_wide', 'camp_wide', 'hill_low'], fg=False)      # ONE scene; presets = only the 2-3 a segment needs
A['cams']['camp_wide']  # (loc, look, lens)      A['marks']['hill_low']  # {mark: (x, y, z, 0, who)} stand points of that preset
for g in range(0, 96):
    r = K.cam_path(None, [(0, 'valley_wide'), (36, 'camp_wide'), (66, (30, 10, 36), (120, 110, 10), 22.0), (96, 'hill_low')], g)    # moves the scene camera, eases STATE['vivid']
    K.set_flow(g / 30.0); K.set_smoke(g / 30.0); K.set_flutter(g / 30.0); K.render(path, 'final')
```
- `build_world(presets, light='MORNING', fg=True, hide=(), over=None, placeholders=False)`: the whole valley (terrain, river, loop, bridge, camp, Abbey Craig with crag, castle rock, farms) plus the near-camera dressing of every listed preset: vegetation (grass, heather, reeds), the preset's foreground props, camp dressing and money-table extras, the Scots line (+ spear wall at the neck), troops (max count per `where` over the presets), signs, light shafts, lantern, splashes (named `<preset><i>`), bridge knights. `fg=False` builds no foreground props at all (use it for pass-through presets); `fg=[names]` keeps them only for those presets; `hide=[names]` skips them for those. Placeholder cards are not staged unless `placeholders=True`; the stand points are in `A['marks'][preset]`. Light: one world light (`WORLD_OVR`: sun_k 1.8, foam, glitter, haze 0.2); `over=` overrides single numbers. Build 33 s for 1-3 presets (the valley farms dominate), +3-5 s per extra ground preset; a draft frame about 10 s, a final frame 85-130 s. The tent/pavilion `clear` zones of the listed presets are merged, so the camera poses are free of tents.
- `cam_path(cam, keys, g, clearance=1.2)`: `keys` = `[(frame, loc, look, lens), ...]` or `(frame, 'preset_or_pose_name')`, mixed. Position is a Catmull-Rom curve through the keys (no stops in between); look target and lens follow the same curve; ease-in on the first segment, ease-out on the last. `STATE['vivid']` is eased (log gamma, sat) between the VIVID entries of the named presets (nearest preset for a free key). The lens is kept `clearance` m above the terrain and the water (soft). `cam=None` = the scene camera. Returns `dict(loc, look, lens, vivid)`. Route the path ABOVE tents and pavilions (add a free waypoint, as `t_path.py` does): only the terrain is checked.
- `K.POSES` (named join poses, usable as cam_path keys): `P_A` (290, 205, 170) -> (120, 110, 10) 22 mm (high over Abbey Craig looking down at the camp and the bridge), `P_CAMP` = the `camp_wide` camera, `P_BANK` = the `camp_bank` camera, `P_NECK` (-2.0, 50.0, 4.6) -> (0.0, 22.0, 1.8) 22 mm (the bridge mouth from the meadow), `P_TOP` (-10, -40, 120) -> (0, 80, 0) 22 mm (high over the bridge, the loop beyond). `styleboard/poses.jpg` shows one draft of each (`python3 poses_sheet.py`).
- `python3 t_path.py` flies valley_wide -> camp_wide -> a waypoint -> hill_low in 12 drafts -> `styleboard/path_strip.jpg` and prints the step per frame and the vivid values.

## 11. Signs (the only text in the set), light shafts, lantern

- Signs: painted wooden boards, cream capitals with a dark outline and a gold border on dark planks (DejaVu Sans Bold, supersampled), on UV quads with the same lit material model. Preset key `signs=[...]`: `'stirling'` = "STIRLING BRIDGE" on two posts just west of the bridge's south end (bridge_end_south, bridge_high, camp_bank); `'treasury'` = "KING'S TREASURY" painted on the front of Cressingham's coin chest (camp_table; 2 lines, letters about 35 px at 3 m); `'english'` = "ENGLISH CAMP" on a board at the camp entrance (camp_wide, `sign_at` (-56, -84), letters about 0.9 m). `K.make_sign(name, center, yaw, w, h, lines, posts=0)` makes another; `K.face_yaw(frm, to)` turns a sign toward a camera. Textures are cached in `tex/sign_*`.
- Light shafts: soft additive strips along the sun direction (transparent/emission mix with a gradient and noise, no world volume, no shadow). Preset key `shafts='pines'` (hill_over, hill_eye, hill_low: through the Scots pines on Abbey Craig) or `'smoke'` (camp_wide, camp_table, camp_bank: through the campfire smoke). Strength: `over=dict(shaft_k=0.6)`. They are separate objects named `shaft_*`; hide them with `o.hide_render = True`.
- Lantern: `lantern=True` (camp_table) hangs a lantern from the money-table canopy: an emissive glow (`glow_flame`, blooms in `grade()`) plus a warm point light (140 W) on the table. Objects `lantern`, `lantern_glow`, light `lantern`.

## 12. Signature colour and the rim light

- Blue saltire banners (deep blue `t_saltire`, white diagonal cross; banner shape `'saltire'`) fly on poles along the Scots line on Abbey Craig (4 along `scots_slope_line`) and at both ends of the spear wall at the bridge's north end. They are live banners (`set_flutter`). The English stay crimson and gold.
- Rim light for the cast cards. An emission card cannot take light from the scene, so the rim is the puppet pose key: `rim="#rrggbb"` (v2/puppet/API.md, `rim` row): a thin light halo behind arms, hands, legs and feet where they leave the body silhouette (never across the torso or head). Default for film 21: `K.RIM_GOLD = '#ffc766'` (warm gold, the sun side is the south-east, so a gold halo reads as sun rim). Put every cast pose through `K.with_rim(pose)` (or set `rim='#ffc766'` yourself) before drawing; use the cool shade tint from the scene (`tint` key) on the opposite side for the warm/cool split.

## 13. Fix after the H2a TAKE gate (2026-11-20 16:00)
- `VIVID[p]` may now carry a third value, an EXPOSURE multiplier applied before the gamma: `(gamma, sat, expo)`. `cam_path` eases all three.
- **P_TOP moved** to `(-10, -115, 115) -> (0, 70, 0)`, 22 mm (old pose kept as `P_TOP_OLD`). It now looks NORTH from above the south bank, so the south-bank half of the army (camp) is in frame above the caption band. A crane up from P_NECK, which looks south, must turn its heading smoothly over the whole move and never pass straight overhead (no 180° spin).
- `VIVID['P_TOP'] = (1.4, 1.1, 0.75)`: a calm ochre meadow and a deep-blue river, about sat 0.63 / luma 105 at the top view. Use it as the grade at P_TOP.
- **Story colours of the cork image** (H2a/H2b): the English trapped in the loop are solid CRIMSON (no blue or white caps, packed tighter, softer shadows). The Scots spear wall is 4-5 ranks deep, in BLUE (tint the Scots cards blue for the top view), with 4-6 large saltire banners (at least 25-30 px at P_TOP). The bridge deck ENDS at the wall and does not run past it into the loop.

## 14. Palette fix for the far-wide views (A1 TAKE gate)

- **Farmland tints** (`vor_fields`): 5 muted greens, 2 straw-golds, 1 muted brown (no red, orange or lime tiles). The base meadow colours (`G1..G4`) were moved from gold-orange toward straw-green.
- **Abbey Craig**: crag rock is slate grey-green (`rock` `#566864`, terrain rock `#62746e` / `#3f504c`, `rock_warm` `#5e6a5c`), the heather/skirt colours are olive and green-brown with 30 % bracken instead of 85 %, so from the far wide it reads as a dark crag with green patches and pines, not a pale lump. The same terrain colours apply to every preset (hill_*, camp_*, ...): their ground is a little greener-grey on the hill, a little more straw in the meadows.
- **River glow**: valley presets and `WORLD_OVR` use `shallow='#2e9a92'`, `sheen_k` 0.45-0.5 and `foam_k` 1.0-1.5 (was 3.0): the bank glow is about half, the deep teal is unchanged. New water override keys: `shallow` (shallow-water colour), `sheen_k` (grazing sheen strength).
- **Light shafts**: `build_world(..., shafts='auto')` builds NO shafts when a `valley_*` preset is listed (they read as flat slabs from above); pass `shafts=True` to force them. The valley presets themselves have none. Shafts in the hill/camp presets run along the sun direction (south-east, high, falling toward the north-west/Scots shelf).
- **VIVID** (3-value, gamma, sat, exposure): `valley_wide` (1.11, 2.38, 1.31), `valley_loop` (0.98, 2.39, 1.23), `valley_river` (2.28, 1.3, 1.0), new `P_A` (1.3, 1.5, 0.96) used by `cam_path` for the P_A pose, `P_TOP` unchanged (1.4, 1.1, 0.75). Measured on 360x640 drafts (qa_stats metric): valley_wide sat 0.59 / vivid 56 % / luma 101, P_A 0.58 / 64 % / 102, P_TOP 0.59 / 73 % / 105, valley_loop 0.58 / 55 % / 102, valley_river 0.60 / 57 % / 98. `python3 palette_fix.py` re-renders the three views -> `styleboard/palette_fix.jpg` with the numbers.
- **Scots line for the far wide**: `K.scots_wide_line(n=26, banners=3, scale=1.7, toward=(445, 244), hh0=30)` puts a two-rank row of oversized blue/ochre figures along the 30 m contour of Abbey Craig on the side that faces `toward` (default the far-wide camera, north-east), on open slope, with 3 oversized blue saltire banners (14 m poles, 7 x 4.6 m cloth). Flag: preset key `scots_wide=True` (now ON in `valley_wide`) or `build_world(..., scots_wide=True)` (auto-on when a listed preset has the flag). Objects `scots_wide*`; hide with `hide_render`. In P_A it shows at the lower edge of the frame; in valley_wide it is small (about 4 px figures, the banner poles about 15 px).
- Known: warm ochre/orange still shows in the loop meadow and around the camp in valley_wide / P_A (the low warm sun on the straw meadow); the hill's lower skirt has a thin orange rim.

## 15. Director retune after the palette fix (2026-11-20 19:00)
- The palette-fix VIVID of valley_wide and valley_loop (sat multipliers of about 2.4) made those views violet and orange. They are now calm, in the same family as P_TOP (1.4, 1.1, 0.75): valley_wide (1.3, 1.2, 0.85) and valley_loop (1.35, 1.15, 0.8).
- The valley_wide camera looks toward the sun, so its frame is mostly shade. Do NOT use it as a hero wide.
- **New `P_HOOK`** = (-60, -260, 230) -> (60, 60, 0), 22 mm, VIVID (1.4, 1.1, 0.75). It is the front-lit extreme wide from the south: the loop, the bridge, the camp and the dark crag in one frame. BIGZOOM 1 (A1) STARTS here.
- **P_A moved** to (40, 10, 95) -> (150, 140, 20), 22 mm, VIVID (1.3, 1.2, 0.85): low over the river SW of Abbey Craig, looking NE at the crag and its pines. The old pose is kept as `P_A_OLD`.
- **A2** flies from P_A up the crag and arcs around over the Scots, ending behind them looking SW down at the bridge (the hill_over family of poses).
- Use `scots_wide=True` with `toward` at the P_HOOK/P_A camera, so the Scots line faces the south viewer.

## 16. Banners and smoke near the lens (fix after the H2b / C gates)
- The grey curved "blades" were the SMOKE plumes (flat grey emission tubes), not the banner cloths: the Wave-modified cloth keeps its material, its tint attribute and both sides (checked close up: crimson with the gold chevron, blue saltire). The plume material is now soft: warm-grey emission, transparent at the silhouette (facing falloff) and fading to the top, so a plume near the lens is a soft puff.
- `K.hide_near_banners(points, radius=15.0, smoke=True, banners=True)`: hides (hide_render) every live banner (all parts of it) and, with smoke=True, every smoke plume within `radius` m of any point of the camera path (`(x, y, z)` 3D distance, or `(x, y)`); returns (banners hidden, plumes hidden). `K.show_all_banners()` undoes it. Typical: `pts = [K.cam_path(None, keys, g)['loc'] for g in range(f0, f1 + 1, 3)]; K.hide_near_banners(pts, 15)` before rendering the segment. `python3 t_banners.py` flies camp_wide -> camp_bank through the camp in drafts (`styleboard/banner_strip.jpg`).
- Colour story: English banners crimson/gold (and cream, green), Scots banners blue saltire only (`t_saltire`); the generic banner list in the camp has no blue-and-white saltire.
- **Blue means Scots only.** The English camp has no blue left: pavilion stripes are crimson/cream or gold/cream, the knight surcoats and caparisons (`KNIGHT_MATS`, the horse lines, the camp_wide parade) are crimson, gold or cream, the table canopy is crimson/gold, the weapon-rack shields are crimson/gold, and the `knight_b` placeholder card is gold. Blue stays on the Scots saltire banners (`t_saltire`) and the Scots tunics.

## 17. Scots far-wide line in saltire blue (director, 2026-11-20 22:10)
`K.scots_wide_line` figures are now saltire blue with a few white, with no ochre, thatch or brown: QA-art A1 found the ochre read as gold "confetti" close to the English gold. Pass `banners=5` (or more) for the hook. A1 and A2 must use the SAME call (same `n`, `banners`, `toward`) so P_A matches across the D6.
