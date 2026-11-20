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
- Head screen positions: the `<out>.json` that `cli_render` writes has `heads: {mark: {cx, cy, chin, dist}}` (px at 720x1280). All heads are above y 880.

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
CLI: `python3 stirling.py render <preset> <out.png> [final|draft] [samples]`, `python3 stirling.py list`. `A` holds `marks`, `cam`, `camp` (`table`, `fires`, `pav`), `scale_beam`, `chest_lid`, `troops`.
Other public functions: `new_scene(light, over)`, `Batch` (`box, cyl, sphere, rock, mesh, quad, tri, prism_roof, xf, wpt, finalize`), `get_mat(key)`, `ground(x, y)` (terrain z), `sd_at(x, y)` (distance to the water line: negative in the river), `river()`, `hill_h`, `rel_xy`, `mark_at`, `mark_px`, props `pavilion, bell_tent, ridge_tent, banner, campfire, cart, weapon_rack, barrel, sacks, horse, knight_pair_column, spear, gorse, reed_cluster, pine, oak, boulder, crag_group, farmstead, scots_slope_line, spear_wall`.

## 4. Hooks (all keyable per frame: call the hook with the frame's value, then render; they only set scene values)

| hook | what | notes |
|---|---|---|
| `K.set_flutter(t, amp=1.0)` | every banner flutters (Wave modifier phase keyed by `t` seconds; amp scales the ripple) | live banners = `K.STATE['anim']['flags']`; poles bob a few cm; 3-4 objects per banner |
| `K.set_smoke(t, speed=0.12)` | every smoke column (camp fires, farms): puffs rise, grow and fade out in a loop (cycle = 1/speed s) | columns in `K.STATE['anim']['smoke']`; flat grey emission, no shadow |
| `K.set_flow(t, speed=1.0)` | the water: current streaks, foam streaks and the sun glitter twinkle | the glitter uses a 4D voronoi; one call per frame |
| `K.splash(x, y, age, size=1.0, z=0.0, name='a', seed=0)` | a spray crown on the water `age` s after the impact: scalloped crown sheet that rises and opens, central column, expanding foam ring, 40 ballistic droplets. `age < 0` or `> 1.6` removes it | calling again with the same `name` replaces it (never stacks); use one name per jumper; size 1 = a man jumping |
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
| `hill_eye` | hill | (128.0, 128.0, z = ground + 1.75) -> (144.0, 144.0, 20.5) | 22 | spear 1.5 m, spear 1.7 m, gorse 2.4 m, heather 1.8 m | `s1` (81, 664), `s2` (225, 659), `w` (360, 637), `s3` (505, 657), `s4` (639, 665) | slide 40 px/s; snap push x1.4 on s2 | 135 s render, 3 s build |
| `hill_low` | hill | (118.0, 112.0, z = ground + 1.40) -> (140.0, 134.0, 22.0) | 22 | gorse 1.6 m, gorse 1.9 m, rock 2.2 m, spear 1.4 m | `s1` (99, 821), `s2` (242, 738), `horn` (389, 804), `w` (509, 692), `s3` (647, 851) | pull-out 7 %/s, tilted up 14 deg | 84 s render, 3 s build |
| `bridge_deck` | bridge | (-2.7, -2.4, z 3.0) -> (0.6, 1.6, 2.9) | 22 | post 1.1 m | `k1` (190, 563), `k2` (520, 570) | push 8 %/s | 101 s render, 2 s build |
| `bridge_high` | bridge | (-5.0, -62.0, z 24.0) -> (0.0, 6.0, 1.0) | 22 | post 1.6 m | - | push along the bridge 8 %/s; snap pull-out x0.7 | 88 s render, 2 s build |
| `bridge_end_north` | bridge | (-3.2, 50.0, z 2.9) -> (0.0, 22.0, 2.2) | 22 | spear 1.5 m, gorse 2.0 m, reeds 2.2 m | `e1` (170, 646), `e2` (420, 643), `e3` (600, 647), `e4` (300, 640) | push 8 %/s | 67 s render, 2 s build |
| `bridge_end_south` | bridge | (-2.3, -40.0, z 3.0) -> (0.0, -31.0, 2.7) | 22 | spear 1.4 m, spear 1.7 m | `k1` (205, 575), `k2` (505, 579) | snap push x1.4 (16 f) | 71 s render, 2 s build |
| `valley_wide` | valley | (445.0, 244.0, z 361.0) -> (64.0, 44.0, 0.0) | 22 | - | - | crane down + push 6 %/s | 106 s render, 35 s build |
| `valley_loop` | valley | (-72.0, -133.0, z 229.0) -> (12.0, 36.0, 0.0) | 21 | - | - |  | 108 s render, 33 s build |
| `valley_river` | valley | (38.0, -24.0, z = ground + 2.10) -> (105.0, 28.0, 4.0) | 22 | reeds 2.2 m, reeds 2.0 m, rock 2.4 m | `e1` (69, 910), `e2` (641, 761) | push 7 %/s + slide | 91 s render, 35 s build |
| `camp_wide` | camp | (-78.0, -96.0, z 13.0) -> (12.0, -52.0, 2.0) | 22 | rope 1.8 m, pole 2.2 m | `k1` (146, 1109), `k2` (549, 995) | slide 50 px/s + push | 82 s render, 3 s build |
| `camp_table` | camp | (-12.0, -32.6, z = ground + 1.50) -> (-13.2, -25.0, 1.3) | 22 | barrel 1.6 m, rope 1.7 m | `cress` (360, 552) | push 8 %/s, coin chest in the middle ground | 139 s render, 3 s build |
| `camp_bank` | camp | (-140.0, -17.3, z = ground + 2.00) -> (-43.0, 6.9, -16.6) | 30 | banner pole with its banner at the right edge, a barrel, reeds and tent pegs | `cress` (177, 589), `surrey` (640, 546), `e0` (37, 568), `e1` (110, 529), `e2` (214, 487), `e3` (601, 505), `e4` (667, 494), `e5` (709, 479) |  | 87 s render, 4 s build |
| `riverbank` | riverbank | (-17.0, 60.0, z = ground + 1.80) -> (0.0, 30.0, 1.6) | 22 | reeds 1.6 m, reeds 2.0 m, gorse 2.4 m | `e1` (91, 679), `e2` (250, 669), `e3` (400, 661), `e4` (175, 642) | slide 40 px/s + push; water on the right for the jumps (splash()) | 73 s render, 3 s build |
| `river_low` | riverbank | (-26.0, 46.0, z = ground + 0.55) -> (-44.0, 44.0, 0.9) | 22 | reeds 1.4 m, reeds 1.6 m, rock 1.8 m | - | quick push; splash() crowns at pr["splashes"] | 78 s render, 2 s build |

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
