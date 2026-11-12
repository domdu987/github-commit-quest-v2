# v3/set3d2/tower.py : set 1, the bell tower of San Nazaro (Brescia 1769), bpy 5.3, Cycles CPU

Files: `tower.py` (the set), `tower_tex.py` (all artwork drawn as SVG in Python, rasterised by `v3/set3d/raster.js` into `tex_tower/`, cached by content hash), `tower_measure.py` (shade / lit ratio per surface, key on / key off), `tower_hue.py` (the rows of `v3/tools/hue_report.py`; that tool's own `__main__` crashes on reference file names that do not exist, so this calls its `row()`), `tower_sheet.py` (contact sheets), `tower_contact.jpg`, `tower_REVIEW.md`. Work files, stills and tests: `tower_work/` (`stills/<PRESET>_<cam>.png`, `storm/`, `measure/`, `t_storm.py`, `t_digest.py`).

World: 1 unit = 1 D (head diameter), Z up, the square at z = 0. The tower is centred on x = y = 0 (4.5 D square), its front faces the square toward -y. Church to the right (+x), houses to the left (-x) and along the left side of the square, the square in front (-y). Camera 22 mm on 36 mm, sensor fit AUTO, 720x1280 (782 px focal; 1 D at depth z covers 782 / z px).

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d2"); import tower as T
A = T.build("DAY")                # DAY | DUSK | NIGHT_STORM | NIGHT_CALM ; clear=True removes every object first
T.set_rod(state, frame=None)      # 0 no rod, 1 iron rod nailed to the finial, >=2 rod + thin wire down the west face into the ground
T.set_bell(angle_deg, frame=None) # swing of bell + headstock + clapper + bell rope about the axle (x); + = mouth toward +y. Bezier keys
T.flash(strength, frame=None)     # lightning: flash light (2nd sun along the key) = strength x flash_e, sky and plate x (1 + 1.6 strength); CONSTANT keys
T.set_bolt(visible, frame=None, target="tower"|"sky")   # jagged emissive bolt; "tower" ends at rod_tip if set_rod >= 1 at call time, else at finial_top
cam = T.make_camera(A["cams"]["square_low"], name="cam")  # creates/reuses a 22 mm camera and makes it scene.camera ({loc, look_at, lens[, up, roll]})
T.setup_render(scene, "final" | "hq" | "preview")   # final 720x1280 12 samples; hq 16 samples; preview 360x640 6 samples; always 2 threads
T.setup_grade(scene)              # spec/grade_compositor.py: bloom > 1.0 (size 0.05), CDL offset, saturation; no vignette (build() calls it)
T.no_bounce(obj)                  # call on every actor card (as office3d)
T.placeholder_actor(role, mark, face_to=None, tilt=0)   # role boy | priest | extra_a | extra_b | extra_c (stills/tests only)
T.stage_placeholders(A, "chamber" | "square" | "none", cam_loc)
T.render(path) -> (wall s, cpu s)
```

`build()` makes the collections `SET` (about 70 objects) and `LIGHTS` (`key_sun`, `flash_sun`), a black world, render settings and the grade; no camera, no actors. Deterministic: two processes give the same digest of object names, transforms, vertices, UVs, materials and anchors, and identical pixels (checked, `tower_work/t_digest.py`). Our materials are named `TWR_<preset>_*` and `ink` and are rebuilt on each call.

Keying: every setter writes the value now and, with `frame=N`, inserts a key at N. Visibility (rod, wire, bolts) and flash use CONSTANT keys, the bell Bezier. Example (in `tower_work/t_storm.py`): `set_rod(2, frame=1); set_bell(0, frame=1); set_bell(35, frame=10); flash(0, frame=1); set_bolt(False, frame=1); flash(1, frame=10); set_bolt(True, frame=10, target="tower")`. Call `set_rod` before `set_bolt(target="tower")` for the same frame, since the bolt end is chosen at call time.

## 2. Anchors (world D)

| key | value | meaning |
|---|---|---|
| `chamber_floor` | z 15.0, rect x,y -1.85..1.85, `hero_mark` (0.55, 0.6, 15), `priest_mark` (-0.75, -0.7, 15), `extra_marks` [(1.2, -0.45, 15), (-1.15, 0.85, 15)] | the bell-chamber stage; priest near the south (camera) arch, hero far, under the bell |
| `square_marks` | hero (-0.9, -11, 0), priest (1.3, -10.2, 0), extra1 (-3.4, -9.4, 0), extra2 (3.6, -12.2, 0), extra3 (-5.2, -13, 0) | actors in the square in front of the tower |
| `rod_base`, `rod_tip` | (0.10, 0, 27.95), (0.10, 0, 29.45) | the iron rod (1.5 D) strapped to the finial spike |
| `finial_top` | (0, 0, 28.45) | top of the copper spike (lightning target without the rod) |
| `wire_points`, `wire_ground` | 19 points, ends at (-2.7, -1.75, 0.02) | wire from rod_base down the spire (west facet), across the terrace, over the parapet and cornice, down the west face at x = -2.45, y = -1.75 (0.2 D off the wall, iron brackets every 2.4 D), into a ground plate in the alley |
| `bell` | pivot (0, 0, 20.6), axis x, diameter 2.2, rim_z 18.35, crown_z 20.39, rope (0.93, 1.0) with the striped sally at z 16.55..17.15, second rope `rope_b` (-1.3, 1.12) through the trapdoor | |
| `tower` | half_width 2.25, shaft 0..15, cornice 21.4..21.9, terrace 21.9, arches half width 1.3 sill 15.75 spring 19.0 top 20.3, spire 21.9..27.6, clock (0, -2.262, 12.3), lantern | |
| `church` | facade x 2.45..11.85 at y -2.6, eave 9.6, apex 13.6 | |
| `bolt_ends`, `key_dir`, `key_note`, `cams`, `cam_notes`, `render` | | |

## 3. Cameras (`A["cams"]`, 22 mm)

| name | loc -> look_at | height, pitch | shows |
|---|---|---|---|
| `square_low` | (0.6, -15.6, 1.2) -> (0.1, -2, 8) | 1.2 D, +27 deg | actors at square_marks (hero head about 170 px, heads at 0.55 to 0.6 H), the tower to the spire and rod above them, church facade right, houses left |
| `chamber_eye` | (0.35, -4.1, 17.4) -> (-0.05, 1.9, 17.75) | 2.4 D above the stage, +3 deg | from just outside the south arch (the opening fills the frame): priest_mark near, hero_mark far (two-shot in depth), the bell overhead, the town plate through the north arch |
| `chamber_high_down` | (-4.3, -0.6, 24.1) -> (-1.2, -10.2, 0) | 24 D, -67 deg | from beside the parapet down the west face (wire) to the square marks (tiny figures) |
| `spire_insert` | (-2.45, -2.25, 27.8) -> (0.05, 0, 28.55) | +13 deg | finial, rod and rod tip against the sky and the plate |
| `town_wide` | (-13, -34, 9) -> (0.5, 0, 13.6) | +7 deg | establishing: square, actors, houses, church, the tower full height, mid town, painted plate, sky |
| `tower_side_mid` | (-7.8, -6.9, 9.6) -> (-2.3, -0.9, 12.6) | +20 deg | the west face at mid height with the wire, the bell chamber above |

Keep cameras out of the tower (|x|, |y| < 2.6 below z 22.8 except inside the chamber), the church (x 2.4..12, y > -3.8), the houses (x < -4.9, y -1..6; x < -14, y -16..-5; x 12.2..17.2, y > -1.6).

## 4. Presets and light model

`displayed = art x gain x KEY x vis x toon(cos) + ((1 - m) art x SHADE x shade_mul + m x lum(art) x TINT x shade_mul + LIFT) x (1 + N.form)`.
`toon(cos) = (k0 + (1 - k0) cos) / max(cos, 0.12)`: a face square to the key gets the full key, a grazing face k0 of it (sides of the tower read as volumes). The shade term is a painted blue-violet: m = `shade_mix` of it is the art's luminance times `shade_tint`, so terracotta in sky light shades to hue 238 to 252 instead of magenta. Ambient is emission (noise-free); one hard sun; no fill, no bounce (every set object `no_bounce`). Lit materials can carry a glow mask (lit windows of the mid town at night).

| preset | key (linear), direction of travel | sun angle | sky / plate | notes |
|---|---|---|---|---|
| `DAY` | (1.31, 1.08, 0.28), (0.45, 0.75, -1.0): 49 deg high from the south-south-west, behind square cameras at screen-left | 0.5 | `sky_day`, `pano_day` | shade/lit 0.15 to 0.18 on every wall (section 5) |
| `DUSK` | (1.55, 1.02, 0.26), (0.60, 0.75, -0.36): 19 deg, golden | 0.6 | `sky_dusk` (sun and painted rays at azimuth 190), `pano_dusk` | windows and lanterns faintly lit |
| `NIGHT_STORM` | moon (0.14, 0.24, 0.62), (0.55, 0.5, -0.8), art desaturated 65 percent in the key | 0.7 | `sky_storm` (storm masses, moon glow behind clouds), `pano_night` | warm windows (emission 1.6), church rose window glows, lanterns; `flash()`, `set_bolt()` |
| `NIGHT_CALM` | moon (0.20, 0.31, 0.74) | 0.6 | `sky_night` (moon disc at azimuth 215, 38 deg, stars) | as the storm without storm clouds |

Set content: brick campanile (Lombard corner strips, three stone string courses with hanging-arch bands, plinth, slit windows, painted clock), open bell chamber (four round arches with voussoir rings, plank floor, beamed ceiling, bell frame on posts, bronze bell with inscription band and clapper on a headstock with straps and axle, rope lever, rope with striped sally, second rope through an open trapdoor with ladder, lantern, bucket, coiled rope, crate, broom, pigeons on the sills), cornice with dentils, terrace with a balustrade (48 balusters, corner piers with balls), octagonal drum with little arched windows, fish-scale tiled octagonal spire, copper ball and spike finial; church facade (pilasters, portal with studded doors and lunette fresco, steps, niches with saints, rose window, raking cornices, cross) with brick nave and tiled roof; five houses (plaster in terracotta, ochre, pink, cream, red; shutters, flower boxes with geraniums, arched doors, a baker's shop) with tiled roofs; cobbled square with fountain, market stall with striped awning and produce, hand cart, barrels, flower pots, bench, wall lanterns; about 60 simplified mid-town houses with window tiles, two more campaniles, a dome, cypresses; the painted plate ring (r 72, z -2..53, repeats twice) of hills, villas, cypresses, towers, domes and dense roofs (day / dusk / night versions, night with lit windows); sky dome (r 110) per preset.

## 5. Measured

| quantity | value | target |
|---|---|---|
| shade / lit, same surface, linear luminance, DAY square_low, final (`tower_measure.py DAY square_low final`) | tower shaft 0.160, corner strips 0.161, chamber walls 0.161, church facade 0.172, house_a 0.156, cobbles 0.148, courses 0.179 | 0.15 to 0.31 |
| hue lit -> shade | brick 18 -> 246, church 34 -> 238, cobbles 26 -> 240, house 12 -> 252 | shade 240 to 260 |
| final 720x1280, 12 samples, 2 threads, placeholder actors | chamber_eye 17.2 to 17.8 CPU s (8.7 s wall), square_low 13.4 to 14.1 (DAY and NIGHT_STORM), town_wide 11.3 to 11.6 | under 25 CPU s |
| determinism | identical digest and pixels in two processes | |

Hue rows: `tower_REVIEW.md` section 2.

## 6. Command line

```
python3 tower.py stills DAY DUSK NIGHT_STORM NIGHT_CALM   # tower_work/stills/<PRESET>_<cam>.png, 360x640, 6 samples, placeholder actors, rod state 2
python3 tower.py timing <cam> <preset>                     # three final frames, wall and CPU seconds
python3 tower_measure.py DAY square_low final               # shade / lit per surface
python3 tower_hue.py tower_work/stills/*.png                # hue_report rows
python3 tower_work/t_storm.py                               # flash, bolts, bell swing, rod states, NIGHT_CALM
python3 tower_work/t_digest.py DAY out.png                  # determinism digest
python3 tower_tex.py                                        # (re)rasterise changed textures
```
