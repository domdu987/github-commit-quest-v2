# v3/set3d3/harbor.py : film 3 set, the Boston waterfront in January 1919 with the molasses tank (bpy 5.3, Cycles CPU)

Files: `harbor.py` (the set), `harbor_tex.py` (all artwork drawn as SVG in Python, rasterised by `v3/set3d/raster.js` into `tex_harbor/`, cached by content hash), `harbor_measure.py` (shade / lit per surface, key on / key off), `harbor_hue.py` (hue_report rows), `harbor_contact.jpg`, `harbor_REVIEW.md`. Work files: `harbor_work/` (`stills/<PRESET>_<cam>.png` 360x640, `flood/flood_<cam>_u020|050|100.png`, `final/<PRESET>_<cam>.png` 720x1280, `anim/` keyed-control test, `measure/`, `hue_rows.txt`, `t_anim.py`, `t_timing_all.py`, `actors/` placeholder sprites).

Built on the film-2 template `v3/set3d2/tower.py`, which is imported, not copied: `mat_lit` / `mat_emit` / `mat_card` / ink hull, `MB` mesh builder, `setup_render`, `setup_grade`, `make_camera`, `render`, `no_bounce`, the keying helpers and `placeholder_actor` (its sprite cache is redirected into `harbor_work/actors`). `harbor_tex.py` imports `tower_tex`'s SVG helpers, job registry and sky painter (two new skies, `winter` and `warm`). `harbor.STATE` is `tower.STATE`.

World: 1 unit = 1 D, Z up, street z = 0. Tank centre (14.5, 22), radius 13, wall 24 D (8 courses of 3 D, 12 plates round), roof apex 26.3. Commercial Street runs from the tank yard toward the camera along -y (cobbles x -5..5, brick sidewalks to +-7.5 at z 0.15, house fronts at x = +-7.5): red-brick rows with pitched slate roofs on the west (-x), ochre / red warehouses with flat roofs on the east (+x). The elevated railway (dark green riveted steel) runs along the street over its west half (columns x -6.2 and -0.6 every 12 D, girders 7.6..9.0, ties and four rails on top) and passes 2 D beside the tank. Horse stable x 12..21, y -4.5..4.5 in the yard. Harbour water (z -1.2) north of y 42 and east of x 34, granite quays, a pier, a moored freighter (x 5..78, y 48..59). Camera 22 mm, 720x1280.

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d3"); import harbor as H
A = H.build("WINTER")              # WINTER | WARM | NOON ; clear=True removes every object first
H.set_paint(state, frame=None)     # 0 grey steel with molasses streaks under the seams; 1 painted brown (no streaks); in between the
                                   # brown climbs the wall from the foot (paint line z = state x 27.6 - 0.5). Linear keys with frame
H.set_seep(amount, frame=None)     # glossy dark seep strips hanging from the seams (50 strips, 0.4..2.3 D): 0 hidden .. 1 full length
                                   # (shape key, linear); the drip drop above the bucket shows from 0.3
H.set_bucket(pos=None, fill=None, visible=None, frame=None, rot=None)
                                   # tin bucket 0.72 D tall, rim r 0.40; pos = base centre (default bucket_mark); rot (deg, e.g. kicked
                                   # over (90, 0, 40)); fill 0..1 molasses level, 1 = overflowing (dribbles + puddle). loc/rot Bezier,
                                   # fill linear, visibility constant keys
H.set_flood(u, frame=None)         # the molasses flood (below). Without frame: shows u now. With frame: one shape key per distinct u,
                                   # keyed so the mesh blends linearly between consecutive keyed states (any call order)
H.flood_height(u)                  # the height field itself (numpy), for planning
H.rivet_points(seams=(1, 2), span_deg=60, step=0.5)   # 242 world points on the rivet rows of the lower seams + the bucket seam
H.set_tank_ink(on)                 # tank ink hull on/off (costs ~5 CPU s per frame when the wall fills the frame)
cam = H.make_camera(A["cams"]["street_low"])          # tower.make_camera
H.setup_render(scene, "final" | "hq" | "preview")     # tower.setup_render: final 720x1280 12 samples, preview 360x640 6; 2 threads
H.placeholder_actor(role, mark, face_to=None, tilt=0) # roles hero (boy), foreman, worker, worker_b, kid (+ tower roles)
H.stage_placeholders(A, "base" | "street" | "none", cam_loc);   H.STAGING[cam] gives the one used for the stills
H.render(path) -> (wall s, cpu s);  H.digest() -> sha1 of the scene (determinism)
```

`build()` makes collections `SET` (about 30 objects) and `LIGHTS` (`key_sun`), a black world, render settings and the grade; no camera, no actors; it leaves paint 0, seep 0.6, bucket fill 0.3, flood 0. Materials are `HBR_<preset>_*` and `ink`, rebuilt on each call. Deterministic: two processes give the same digest and identical pixels (checked).

The flood: flow coordinate s = distance from the burst at the foot of the bucket seam (`A["tank"]["burst"]`); front at s = 2.5 + 49.5 u^0.8; steep rounded front, crest 8.1 D at u 0.2, 7.7 D at 0.5 (well above the 4 D ground floors), 4.6 D at 1; a layer 0.9 + 2.6 u behind; a tall mound against the wall while u is small; a dark jagged rupture on the wall from u > 0 (grows to full size by u 0.08). Confined to the street between the house fronts and to the yard (not inside the stable or the tank); flat-shaded heightfield 0.4 D grid, dark glossy amber, no emission. u 0.2: burst and mound round the tank foot; u 0.5: a house-high wave halfway down the street (about y -20); u 1: the street full, the crest 6 D in front of `street_low`.

## 2. Anchors (world D)

| key | value | meaning |
|---|---|---|
| `bucket_mark` | (9.216, 9.61, 0) | bucket base centre, 0.47 D off the wall under the bucket seam (azimuth -113.1 deg) |
| `hero_mark` | (7.839, 9.186, 0) | the boy beside the bucket (1.4 D out, 1.1 D to the left looking at the wall) |
| `boss_mark` | (9.83, 4.423, 0) | foreman 5 D out, nearer `base_eye` (depth two-shot) |
| `worker_marks` | (13.836, 6.614, 0), (2.621, 10.985, 0), (24.5, 44.5, 0.15) | by the ladder, by the barrels, on the pier |
| `kid_marks` | (-2.2, -20, 0), (2.8, -27, 0), (-3.6, -33, 0) | kids on Commercial Street |
| `street_marks` | (0,-8), (1.5,-16), (-1,-24), (0.5,-36), (-2,-46) | along the street centre |
| `square_marks` | center (3.5, 1), by_stable (10.5, 0), street_end (0, -4), trestle_foot (-3.2, 2) | the open yard where the street ends |
| `tank` | center, radius 13, wall_top 24, roof_apex 26.3, courses 0..24 step 3, bucket_seam_azimuth_deg -113.1, ladder_azimuth_deg -94.2, plate_width 6.807, pipe (7 points, pier to roof), burst (9.4, 10.04, 0) | |
| `trestle` | column_x (-6.2, -0.6), deck_top 9.0, girder_bottom 7.6, bents_y every 12 from -146 | |
| `street`, `stable`, `harbour`, `key_dir`, `sun_elevation_deg`, `cams`, `cam_notes`, `render` | | |

## 3. Cameras (`A["cams"]`, 22 mm)

| name | loc -> look_at | shows |
|---|---|---|
| `tank_low` | (10.39, 6.12, 1.2) -> (9.04, 10.2, 10.5) | from the foot of the tank, 3.4 D out, up the riveted wall past the ladder to the rim against the sky |
| `base_eye` | (6.15, 0.03, 2.6) -> (8.92, 9.6, 2.2) | eye level at the tank base: hero by the bucket far, foreman near right, barrels left, ladder right |
| `street_low` | (1.6, -50, 1.2) -> (10, 20, 10) | down Commercial Street, 1.2 D high: trestle overhead-left, warehouses right, the tank at the end |
| `street_wide` | (2, -60, 22) -> (9, 12, 6) | establishing over the street: trestle, both rows, the tank towering at the end, harbour and freighter right of it |
| `seam_insert` | (9.5, 7.33, 2.4) -> (9.28, 10.09, 2.1) | close on the bucket seam (first horizontal seam meeting the lowest vertical seam), seep strips, bucket at the bottom |
| `bucket_insert` | (7.08, 8.51, 1.05) -> (9.24, 9.67, 0.75) | low and close on the bucket under the drip |
| `high_down` | (9.79, 10.96, 27.6) -> (0.5, -26, 0) | from the tank roof railing down onto the yard and the street (the flood's best overview) |

Keep cameras out of the tank (r < 13.5 round (14.5, 22) below z 26.5), the house rows (|x| > 7.5 for y < 40 west / y < -6 east), the stable, the trestle columns (x -6.2 / -0.6 every 12 D in y from -146).

## 4. Presets and light model (tower.py model: one hard sun + painted blue-violet shade as emission, no bounce)

| preset | key (linear) | sun | sky / plate | notes |
|---|---|---|---|---|
| `WINTER` | (1.28, 1.12, 0.52) | 20 deg, from the south-south-west (travel (0.20, 0.98)), angle 0.4 | `sky_winter` deep clear blue, `pano_winter` | crisp, long shadows: the west rows shade most of the street; all snow patches |
| `WARM` | (1.36, 1.08, 0.38) | 37 deg, (0.14, 0.99), angle 0.7 (softer) | `sky_warm` paler with a warm hazy horizon, `pano_warm` (more haze) | snow 45 percent (fewer, smaller patches) |
| `NOON` | (1.48, 1.18, 0.42) | 40 deg, from the south, angle 0.35 (hardest) | warm sky and plate | for the disaster; snow 40 percent |

Shade colour per preset: shade (0.08..0.10, 0.14..0.15, 0.44..0.50), shade_tint violet; molasses and seep strips get a small Glossy BSDF (sun highlight only).

## 5. Measured

| quantity | value | target |
|---|---|---|
| shade / lit, same surface (`harbor_measure.py`) | WINTER street_low: houses 0.195, tank 0.162; NOON street_low: cobbles 0.142, houses 0.234, tank 0.154, trestle 0.183; WARM base_eye: yard 0.163, tank 0.170, tank foot 0.162, barrels 0.168 | 0.15 to 0.31 |
| hue lit -> shade | houses 4..10 -> 242..252, tank 16..24 -> 234..242, cobbles 22 -> 242, yard 20 -> 248 | shade 240..260 |
| final 720x1280, 12 samples, 2 threads (CPU s) | WINTER: tank_low 15.0, base_eye 20.5, street_low 15.8, street_wide 14.5, seam_insert 24.6 (19 without tank ink), bucket_insert 22.0, high_down 17.1; NOON with flood u 1: 15.5, 17.2, 15.1, 14.5, 22.3, 20.8, 17.9 | under 25 |
| determinism | same digest, max pixel difference 0 in two processes | |

## 6. Command line

```
python3 harbor.py stills WINTER WARM NOON       # harbor_work/stills, 360x640, placeholder actors (WARM/NOON painted brown)
python3 harbor.py flood [NOON]                  # harbor_work/flood: u 0.2 / 0.5 / 1.0 from street_low, street_wide, high_down
python3 harbor.py timing <cam> <preset>         # three final frames
python3 harbor.py digest <preset> [out.png]     # determinism digest
python3 harbor_measure.py <preset> <cam> [final|preview]
python3 harbor_hue.py harbor_work/stills/*.png harbor_work/flood/*.png
python3 harbor_work/t_anim.py $PWD              # keyed paint, seep, bucket (fill, kick), flood
```
