# v3/set3d4/pagoda.py (v2) : film 4 set, an old-Japan temple town with the five-storey pagoda and the master builder's rigid tower (bpy 5.3, Cycles CPU)

Files: `pagoda.py` (the set), `pagoda_tex.py` (all artwork drawn as SVG in Python, rasterised by `v3/set3d/raster.js` into `tex_pagoda/`, cached by content hash), `pagoda_measure.py` (shade / lit per surface, key on / key off), `pagoda_contact.jpg`, `pagoda_REVIEW.md`. Work files: `pagoda_work/` (`stills/<PRESET>_<cam>.png` 360x640, `tests/` sway / pillar / crack / collapse / quake stills, `final/<PRESET>_<cam>.png` 720x1280 12 samples, `anim/` keyed-control test from `t_anim.py`, `measure/`, `hue_rows.txt`, `final_log.txt`, `actors/` placeholder sprites).

Built on the film-2/3 template `v3/set3d2/tower.py`, imported, not copied: `mat_lit` / `mat_emit` / `mat_card` / ink hull, `MB` mesh builder, `setup_render`, `setup_grade`, `make_camera`, `render`, `no_bounce`, the keying helpers (`_key`, `_show`, `_fcurves`) and `placeholder_actor` (sprite cache redirected to `pagoda_work/actors`). `pagoda_tex.py` imports `tower_tex`'s SVG helpers and job registry. `pagoda.STATE` is `tower.STATE`. Same module shape as `harbor.py`.

World: 1 unit = 1 D, Z up, ground z = 0. Pagoda at (0, 0), front (doors, path, gate) toward -y. Master's tower at (14, 0). Walled gravel courtyard x -16..28, y -32..18 (wall 2.95 D: stone base, white plaster, tiled coping), red gate at (0, -32), temple hall at x -15..-7, y 0..9. The street runs south from the gate (y -34..-104, x -4.5..4.5) between two rows of machiya (pent roof 2.9..3.55, ridge 7..7.4) with hanging red lanterns; a row of houses faces the gate square at y -40; a ring of town houses beyond; pines; painted mountain ring R 150 (z -1.5..50) and sky dome R 170.

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d4"); import pagoda as G
A = G.build("DAY")                     # DAY | SUNSET | NIGHT | DAWN ; clear=True removes every object first
                                       # v2: build(preset, clear=True, open_base=True, dress=True) (see section 1b)
G.set_sway(amp, phase=pi/2, frame=None, pillar=True)
        # storey i (0 bottom .. 4 top) moves x = amp*(i+1)/5*(-1)^i*sin(phase) and tilts with it (snake dance: adjacent storeys
        # opposite, amplitude growing upward; the top storey + finial move amp D). Keys location/rotation (Bezier) with frame.
        # Call every frame with that frame's phase, e.g. phase = 2*pi*f*1.2/30 for 1.2 Hz. pillar=True keys the hanging pillar the
        # other way (its foot moves -0.3 x top offset). G.sway_offsets(amp, phase) -> (offsets, tilts) for planning.
G.set_cutaway(on, frame=None)          # hide the front (-y) walls, doors, floors, railing, roof quarter, soffit of all five storeys
G.set_pillar_swing(angle_deg, frame=None)   # shinbashira pendulum about its chain anchor (0,0,16) on the y axis; + moves the foot +x;
                                       # 1 deg = 0.25 D at the foot. It hangs from the top storey, so it also follows the sway
G.set_crack(level, frame=None)         # tower joint crack decal: 0 none, 1 hairline, 2 finger-wide, 3 split open (visibility keys)
G.set_plaster(level, frame=None)       # plaster patches over it: 0, 1 (small, over the hairline), 2 (both; crack 3 runs through them)
G.set_collapse(u, frame=None, settle=None, dust=True)
        # rigid tower snaps at its joint (z 11.3) and the top half falls south into the courtyard: u 0..0.15 joint opens + lean 5 deg,
        # puffs at the break; ..0.62 topples to 75 deg over the south edge; ..0.8 drops onto the ground; 0.68..0.95 rubble pile grows,
        # 26 timbers / plaster slabs fly break -> pile (0.18..1); dust column to z ~25 by u 1 (ref a t0096). settle 0..1: low dust bank
        # over the ruins; dust=False hides the burst / column (morning after). With frame: everything keyed (Bezier / constant vis);
        # call per frame. G.collapse_pose(u) -> (angle deg, hinge drop D); G.pile_height(x, y).
G.set_quake(strength, frame=None)      # loose props shake: 12 hanging lanterns (10 street, 2 gate) + 20 pagoda wind bells swing (10..14 deg at 1.0), 24 loose
                                       # roof tiles on the near street houses hop/twist. Deterministic in the frame; call per frame
                                       # (strength 0 = rest). Camera shake is the shot's job.
G.apply_cam_state(cam, preset)         # the set-state used for the contract stills of a camera (cutaway, crack 2 + patch 1, DAWN ruins)
cam = G.make_camera(A["cams"]["two_buildings"])
G.setup_render(scene, "final" | "hq" | "preview")   # tower.setup_render: final 720x1280 12 samples, preview 360x640 6; 2 threads
G.placeholder_actor(role, mark, face_to=None, tilt=0)   # roles apprentice (2.4 D), master (3.1), towns_a/b/c (+ tower roles)
G.stage_placeholders(A, "pagoda"|"yard"|"street"|"pile"|"wide"|"none", cam_loc);  G.STAGING[cam]
G.render(path) -> (wall s, cpu s);  G.digest() -> sha1 of the scene (determinism)
```

Keying note: visibility controls (`set_cutaway`, `set_crack`, `set_plaster`) key constant steps; key the starting state as well (e.g. `set_plaster(0, frame=1)` before `set_plaster(1, frame=80)`), otherwise the single key holds over the whole shot.

`build()` makes collections `SET` and `LIGHTS` (`key_sun`), a black world, render settings, the grade; no camera, no actors; it leaves sway 0, cutaway off, crack 0, plaster 0, collapse 0, quake 0. Materials `PGD_<preset>_*` and `ink`, rebuilt each call; all actions are cleared on build. Pivots (empties): `storey_0..4`, `pillar_pivot` (child of storey_4), `bell_i_j` (children of the storeys), `tower_top_pivot`, `rubble_root`, `debris_NN`, `lantern_NN`, `tile_N`.

## 1b. v2 additions (pagoda_REVIEW2.md)

```python
A = G.build("DAY", open_base=True, dress=True)   # defaults; build("DAY") gives the v2 set. open_base=False keeps the v1 doors / lattice
                                       # on the ground storey's front; dress=False leaves out ornament + dressing (the pillar foot is always dressed)
G.setup_dof(scene, focus, fstop, cam=None, blur_max=None)
        # depth of field from the Cycles Z pass (compositor, inserted before the bloom; ~0.4 CPU s at 720x1280, headless-safe).
        # focus: an object (followed per frame: pass the actor's card, e.g. Tk.kenta.card), an (x, y, z) point, or a distance (D).
        # fstop: smaller = more blur. CoC px (720x1280) = 12 f^2 / (fstop (s - f)) / sensor x 1280 x |1 - s/Z|, capped at blur_max
        # (DOF_BLUR_MAX 28 px, scaled with the resolution %). Useful: 0.5..1 at 10..20 D, 2..3.5 at 3..5 D, 3..6 for 1..3 D inserts,
        # 7+ for a hint. fstop None/0 switches it off (the node graph stays, factor 0). cam: default scene.camera at render time.
        # The focus distance is recomputed on every frame change and render (handlers frame_change_post / render_pre: update_dof).
G.apply_dof(cam_name)                  # the default of a set camera (G.DOF): cutaway_insert 3.0 on the pillar's dragon head, crack_insert 2.5,
                                       # street_eye 2.0 at (0, -44), pagoda_low 4.0 (a hint), rubble_dawn 6.0 on the master; OFF for two_buildings,
                                       # town_wide, cutaway_full. CLI stills / final call it after make_camera.
G.update_dof(scene)                    # recompute now (normally automatic)
```

s01 settings used for compare2.jpg (`pagoda_work/v2/s01_v2.py`): shot 1 focus kenta's card fstop 3.5; shot 2 (0.2, -0.62, FOOT_Z+0.5) 6.0;
shot 3 (-3.6, -3.4, 6) 7.0; shot 4 kenta's card 3.0; shot 5 off.

What build() now adds (all parented to the storey pivots where they sit on the pagoda, so they sway; front (-y) parts join the cutaway list):

| part | objects | notes |
|---|---|---|
| open base (was s01 `open_ground_front`) | edits `storey_0_front`, `storey_0_body` | front door / lattice panels and their linings gone, the two middle back posts gone. shot.py's `open_ground_front()` is now a no-op |
| warm interior (was s01 `warm_interior`) | slots of `pillar`, `storey_0..4_body`, `soseki`, `oil_lamps` | shade art x (0.6, 0.46, 0.33), no blue tint, + painted lamp glow; ground-storey bracket band warm. shot.py's `warm_interior()` is now a no-op |
| pillar foot (key insert) | `pillar_foot`, `pillar_beads`, `pillar_dragon`, `pillar_dragon_head` (children of `pillar_pivot`), `soseki_shade` | polished bronze shoe with beaded gold rims, cloud-scroll sleeve (FOOT_Z+0.41..0.95), gold bands, a gold dragon coiling 1.3 turns down to its head at azimuth -72 deg (faces the insert cameras) at FOOT_Z+0.4..2.35, max radius ~0.85 D; the 0.25 D gap stays open; dark contact shade on the stone (fixed: it does not follow a pillar swing) |
| ornament, all storeys | `orn_i`, `orn_i_front`, `brackets_i` | gold fittings on every post, 3D bracket blocks with gold caps (no ink hull: cost), beam ends with gold tips |
| festival lanterns | pivots `lantern_e<storey>_<side>_<k>` + `_mesh` (38), `lantern_v2_0/1` (big pair at the ground-storey front, (+-1.95, -3.95, 4.38)) | lit paper (emission 1.25 by day, 2.6 at night); all swing in `set_quake` |
| bunting / banners | `bunting_1..4(_front)`, `ban_banners` (front eave corners of storey 0), `ban_storey1` (four corners of storey 1) | alpha-cut, no shadow |
| ground storey | `drapes`, `pelmets` (front bays), `interior_v2` (dragon murals on the side bays of the three inner walls, red dado, runner + square carpet, gilded canopy at z 3.35 with an opening of 1.05 D round the pillar), `yoraku_chains`, `canopy_pelmet`, `round_windows` (glowing round lattice windows in the middle bays), `flames_v2`, `fire_bowls` (kagaribi at FIRE_BOWLS (-2.55, -4.6), (2.6, -4.7) on the platform) | two gold candelabra at (+-1.55, -1.05) |
| yard / street / gate (was s01 `build_dressing`, extended) | `yard_dressing`, `cloth_v2`, `gate_ban` | same props and positions as shot.py, plus a third plank stack, a log-sawhorse, a tool rack (-10.8, -4.6), rope coils, log piles, a second east plank stack, a sawhorse (11.6, -8), potted pines (+-4.6, -6); one red runner `runner` (RUNNER_HW 0.975, centred, 65 % of the stair) from the street (y -70) through the gate and courtyard, draped over every riser / tread of the steps with a lip at each nosing (`runner_profile()` gives the y-z polyline), across the platform and on inside the storey to the carpet ring; 22 approach / street banners (nobori2) on poles, 24 hangings on the south yard wall, the gate curtain (maku, z 2.85..3.78) and two ban on the gate. The v1 `banners` object is removed. The street cart moved to (2.9, -61.5) (it filled street_eye) |

**shot.py**: its `build_dressing()` must be dropped (it would place every prop twice); `open_ground_front()` and `warm_interior()` are harmless no-ops now.

New keep-out zones: fire bowls (r 0.5) at FIRE_BOWLS; potted pines (+-4.6, -6); banners on poles at x +-1.9 (y -21.5, -24.5, -27.5, -30.5) and x +-3.3 in the street; tool rack x -12..-9.6, y -5..-4.2.

Painted light (no light objects, noise free): `_extra(material, glow=(points, rgb, k, radius), spec=(points, rgb, k, power), glossy=(rgb, k, roughness))`
adds a warm lamp glow (art x rgb x k x wrap(N.L) x r^2/(r^2+d^2)) and a Blinn highlight of the flames as emission, and a GGX lobe for the
one key (exterior gold only). Points: `GLOW_IN` (the inner flames, one per side), `GLOW_FRONT` (fire bowls + front lanterns per side).
Materials: `STATE['MV']` (exterior), `STATE['MW']` (interior, warm shade). Strength per preset `GLOW_K`, flames `FLAME_K` (4..4.5, bloom).

## 2. Anchors (world D)

| key | value | meaning |
|---|---|---|
| `apprentice_mark` | (-1.6, -11.5, 0) | on the approach path in front of the pagoda |
| `master_mark` | (9.6, -10.8, 0) | in front of his tower |
| `yard_marks` | (-5,-16), (3.6,-18.5), (11,-17), (-2.2,-22.5), (7,-24) | townspeople in the courtyard |
| `street_marks` | (-1.4,-40), (1.9,-44.5), (-0.6,-49), (2.4,-38), (-2.4,-46.5) | in the street, in depth from street_eye |
| `pile_mark` | (12.9, -9.4, 2.355) | the master standing on the fallen tower (DAWN) |
| `platform_marks` | (-1.4,-4.4,0.9), (1.6,-4.6,0.9) | on the pagoda platform at the doors |
| `pagoda` | storeys [half_width, base_z, wall_top, eave_out]: (3.0, 0.9, 3.9, 5.25), (2.7, 5.1, 7.1, 4.8), (2.4, 8.3, 10.2, 4.4), (2.1, 11.4, 13.2, 4.0), (1.8, 14.4, 16.1, 3.7); apex 17.9, sorin_top 23.2; pillar r 0.42, foot_z 1.5, top_z 15.45, chain_anchor (0,0,16), soseki_top 1.25, gap 0.25 | |
| `tower` | center (14,0), half 2.6, plinth 0.8, storey 4.2 x 4, wall_top 17.6, apex 20.8, snap_z 11.3, joint (13.4,-2.6,11.3), hinge (14,-2.6,11.3), falls -y, pile center (14,-8.6) radii (4.4, 6.2) height 2.6 | |
| `yard`, `gate`, `street`, `lanterns` (hook points), `pines`, `key_dir`, `sun_elevation_deg`, `cams`, `cam_notes`, `render` | | |

## 3. Cameras (`A["cams"]`, 22 mm)

| name | loc -> look_at | shows |
|---|---|---|
| `pagoda_low` | (-0.9, -16, 1) -> (0, 0, 12) | low on the path, up the five eaves to the bronze finial; apprentice + townsman at the doors |
| `two_buildings` | (6.9, -31, 3.4) -> (7.4, 0, 9.6) | wide: pagoda left, tower right, full height side by side (sway comparison, collapse: the top falls toward this camera, the pile lands in front of the tower) |
| `street_eye` | (1.3, -58, 2.5) -> (0.6, -20, 6.4) | eye level in the street: machiya rows, lanterns, banners, actors in depth, gate and pagoda beyond |
| `cutaway_insert` | (0.9, -3.4, 1.36) -> (0, 0, 1.62) | inside the ground storey (cutaway on): the pillar foot floating 0.25 D over the granite foundation stone, two oil lamps |
| `crack_insert` | (13.6, -5.4, 11.4) -> (13.4, -2.6, 11.3) | close on the tower joint: crack and plaster decals, the iron joint plate |
| `town_wide` | (-22, -58, 24) -> (6, -2, 6) | establishing: street, walled courtyard, pagoda + tower, hall, town ring, painted mountains |
| `rubble_dawn` | (15.6, -13.4, 3.6) -> (0, 0, 9) | from the south tip of the rubble pile toward the pagoda; master on the pile |
| `cutaway_full` | (0.6, -24, 9.6) -> (0, 0, 10.6) | extra: the whole pagoda in cutaway |

Keep cameras out of: the pagoda (|x|,|y| < 5.3 above the platform unless inside for the cutaway), the tower (|x-14|,|y| < 3.6), the pile (u >= 0.7), houses (|x| > 4.5 for y < -34; y -48..-40 for |x| > 6), courtyard walls, pines and toro (x ±3, y -12 / -20), banners (x ±1.9, y -21.5 / -27.5).

## 4. Presets and light model (tower.py: one hard key + painted blue-violet shade as emission, no bounce)

| preset | key (linear) | sun | sky / plate | extras |
|---|---|---|---|---|
| `DAY` | (1.31, 1.08, 0.30) | 45 deg from the south-west (travel (0.45, 0.75)), angle 0.5 | `sky_day` clear blue with clouds, `pano_day` blue snowy mountains, green hills, far town, castle keep | |
| `SUNSET` | (1.62, 0.98, 0.32) | 11 deg from the west, angle 0.6 | `sky_sunset` red-orange with a ray-burst sun at az 200, `pano_sunset` | lanterns lit (1.0), windows 0.5, warm haze veil 0.10 |
| `NIGHT` | (0.20, 0.31, 0.74) moon, key_desat 0.6 | 40 deg from the south-west | `sky_night` stars, big moon with glow at az 100 el 36 (north: behind the pagoda in two_buildings / street_eye) | lanterns 2.6 (bloom), lit lattice windows 1.0, warm light pools on the ground, stone lantern windows |
| `DAWN` | (1.30, 1.00, 0.74) pink-gold | 14 deg from the east-south-east, angle 3 (soft) | `sky_dawn` blue to gold, sun at az 337 | gold haze veil 0.2 (3 camera-only additive rings); contract stills show the tower fallen with settled dust |

Shade per preset: DAY (0.10, 0.18, 0.56), SUNSET (0.17, 0.13, 0.42), NIGHT (0.07, 0.10, 0.34), DAWN (0.15, 0.15, 0.46), all with a violet shade tint. Two oil lamps inside the ground storey are always lit (emission + pool decal) so the cutaway is never pitch dark. v2: plus two candelabra, two fire bowls, two big front lanterns and 38 eave lanterns, all emitting in every preset (flames 4..4.5 bloom), and the painted lamp glow / highlights on the interior, the pillar and the ground storey's front.

## 5. Measured

| quantity | value | target |
|---|---|---|
| shade / lit, same surface (`pagoda_measure.py DAY <cam> preview`) | two_buildings: tower walls 0.183, ground 0.168, banners 0.167; pagoda_low: pagoda storey fronts 0.171..0.173, platform 0.187; street_eye: ground 0.164, roofs 0.218 | 0.15..0.31 |
| hue lit -> shade | plaster / timber 36 -> 236..238, red lacquer 12 -> 250, banners 354 -> 264..266, ground 26..38 -> 236..242 | shade 240..260, never magenta |
| final 720x1280, 12 samples, 2 threads (CPU s) | v2: 12.5..23.6 for all 32 camera x preset (insert cameras 20..23.6, includes DOF + bloom); s01 shots on the v2 set with cast4 actors 13.8..25.1 (`pagoda_work/v2/final_log2.txt`, `pagoda_work/v2/s01/log.json`). v1: 11.6..25.1 | under ~25 |
| determinism | v2 digest dd713287... identical in two processes (v1 e446bc77...) | |

## 6. Command line

```
python3 pagoda.py stills DAY SUNSET NIGHT DAWN     # pagoda_work/stills, 360x640, placeholder actors, apply_cam_state per camera
python3 pagoda.py tests [DAY]                     # pagoda_work/tests: sway 0/0.5/1/1.5 (+ opposite phase), pillar +-3 deg, crack x plaster, collapse u, quake
python3 pagoda.py final <PRESET> [cam ...]        # pagoda_work/final 720x1280 12 samples, prints wall / cpu s
python3 pagoda.py digest <PRESET> [out.png]       # determinism digest
python3 pagoda_measure.py <PRESET> <cam> [final|preview]
python3 ../set3d3/harbor_hue.py pagoda_work/stills/*.png
python3 pagoda_work/t_anim.py $PWD                # keyed sway / quake per frame, crack / plaster keys, collapse 0 -> 1, cutaway key
```
