# v3/set3d2/vault.py : the gunpowder vault under San Nazaro (bpy 5.3, Cycles CPU)

Files: `vault.py` (the set), `small_work/smallkit.py` (shared with `room.py`: light model node groups, materials, ink hull, raster, render settings, placeholder actors), textures drawn as SVG inside `vault.py` and rasterised by headless Chromium (`v3/set3d/raster.js`) into `tex_small/v_*.png` (cached by SVG hash).
Stills: `small_work/stills/vault_<PRESET>_<cam>.png` (360x640, 8 samples, placeholder actors), final frames `small_work/final_vault_*.png` (720x1280, 12 samples). Contact sheet `small_contact.jpg`.

World: 1 unit = 1 D, Z up, floor z = 0. Back wall (stair end) = plane y = 0, vault runs toward -y to the front wall y = -12 (barred door). x = 0 = vault axis, +x = right for a viewer facing the back wall. Walls x = +-3, springing z = 2.0, segmental barrel vault crown z = 4.4 (radius 3.075, centre z 1.325).

## Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d2"); import vault as V
A = V.build("LANTERN" | "BURN", clear=True)   # collections SET + LIGHTS, black world, Cycles settings, grade; returns anchors
V.set_crack_glow(u, frame=None)     # orange emission along the crack from the stair (u=0) to the barrels (u=1); frame=N keys it (linear)
V.flash(strength, frame=None)       # key energy x (1+strength) and an orange ambient flash term (0.6*strength); frame=N keys both. flash(0, N+3) to return
V.burn_pulse(f0, f1, period=7, depth=0.35, seed=3)   # deterministic flicker keys between f0 and f1 (calls flash)
V.crack_point(u)                    # world point at arc-length fraction u of the crack
cam = V.make_camera(A["cams"]["dolly_barrels"])      # = office3d.make_camera (22 mm, {loc, look_at, lens[, up]})
V.setup_render(scene, "final" | "preview")          # final 720x1280 12 samples, preview 360x640 8 samples; always 2 threads, fixed seed
V.placeholder_actor(cast, pose, mark, face_to=None, name=None, scale=1.0, z=None)   # stills/tests only (v2 puppet on an emission card); scale 0.8 = the boy
V.stage(A, cam_name)                # the stills' placeholder staging (soldier at soldier_mark, boy at aisle_mark)
```
Actor cards: emission to camera rays only (`office3d.mat_card`), then `V.no_bounce(card)`. Every set object is already hidden from bounce rays.
CLI: `python3 vault.py stills [preview|final] [LANTERN,BURN]`, `timing [preset] [cam]`, `digest [preset]`.

## Presets
| preset | key | ambient (emission) | notes |
|---|---|---|---|
| `LANTERN` | Point light in the hanging lantern (0.15, -7.2, 2.75), radius 0.025 (hard), K (1.9, 2.5, 0.05), falloff 1/(1+(d/2.6)^2) | blue-violet (0.15, 0.28, 1.14) on the artwork pulled 85 % to grey; falls off 94 % over 4.5 D from the lantern and 85 % from z 2.6 to 5.5 (dark crown and shaft) | the only light; long barrel shadows thrown up the walls; glass panes emit 4.0 (bloom) |
| `BURN` | orange Point light under the crack (-1.0, -6.7, 3.0), radius 0.08, K (3.0, 1.15, 0.22), falloff 2.6 | dark plum (0.10, 0.06, 0.24) + painted orange pools at the lantern and the fire; flash colour (0.85, 0.32, 0.06) | crack glow starts at u = 1; use `flash` / `burn_pulse` for the pulse |
The key colour of LANTERN is yellow-green in linear terms on purpose: the blue ambient is added under the key too, and only a yellow key keeps lit brick orange (hue 20-30) instead of pink.

## Anchors (`A[...]`)
| key | value |
|---|---|
| `vault` | x_left -3, x_right 3, y_front -12, y_back 0, springing 2.0, crown 4.4, arc radius / centre |
| `hole` | stair opening x 0.8..3 (edge x from the mesh), y -4.5..0, shaft top z 8 |
| `stair` | x 1.55..3, 15 steps rise 0.30 tread 0.45 from y -6.75 (floor) to y 0 (z 4.5); `top` (2.27, -0.2, 4.5), `foot` (2.27, -7.05, 0) |
| `lantern`, `burn_light`, `key_pos` | light positions |
| `crack_path` | 61 points on the vault surface (0.012 D proud) from `crack_start` (0.857, -4.55, 4.266, the stair opening) over the crown to `crack_end` (-2.889, -7.42, 2.344, on the left wall just above the middle barrel pyramid) |
| `barrels` | 27 lying barrels (c, axis 'x', side -1 left / +1 right, row 0..2) in five pyramids on wooden chocks; heads with the stencil face the aisle; 2 standing barrels near the door |
| `stencil_insert`, `stencil_normal` | (-1.9, -7.89, 1.27), (1, 0, 0): the head filmed by `barrel_insert` |
| `soldier_mark` | (-1.05, -9.1, 0) in front of the left barrels |
| `aisle_mark` | (0.55, -10.2, 0) second actor in the aisle |
| `cams` | below |

## Cameras (all 22 mm)
| name | loc | look_at | shows |
|---|---|---|---|
| `dolly_barrels` | (-0.45, -3.2, 0.95) | (-2.2, -7.4, 1.35) | low, along the left barrel rows; `move` = end pose loc (-0.45, -6.4, 0.95) look_at (-2.2, -10.6, 1.35) (3.2 D dolly) |
| `stair_high` | (1.3, -2.3, 4.3) | (-0.5, -10.8, 0.2) | from the head of the stair in the opening down the whole vault to the door; shaft walls frame the top |
| `barrel_insert` | (-0.95, -7.57, 1.39) | stencil head | 1 D from a head: the crossed cannons fill the width |
| `crack_follow` | (0.95, -3.5, 2.05) | (-2.5, -7.6, 2.55) | from under the opening along the crack to the left barrel stack |
Keep cameras out of the barrel stacks (|x| > 1.85, z < 2.4) and the stair mass (x > 1.55).

## Measured
- hue_report (4 cameras, 360x640, with actors): LANTERN red 40.6 orange 34.3 blue 16.3 violet 1.5 magenta 5.3, sat 0.42 val 0.45 dark 0.09: all in band. BURN red 89.8 orange 0.9 blue 0.1 (special light: fire, no cool light by design).
- shade/lit on the floor in `dolly_barrels` (key on vs off, same pixels): 0.168 linear luminance (p10-p90 0.15-0.34), lit hue 20 -> shade hue 232.
- final 720x1280, 12 samples, 2 threads: 15.4-15.7 CPU s (7.8-7.9 s wall) LANTERN dolly_barrels; 14.3-14.7 CPU s BURN.
- deterministic: same digest (`b651691a...` LANTERN) and bit-identical pixels from two processes.
