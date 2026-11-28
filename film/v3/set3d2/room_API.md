# v3/set3d2/room.py : Nico's attic bedroom (bpy 5.3, Cycles CPU)

Files: `room.py`, shared helpers `small_work/smallkit.py`, textures (SVG in `room.py`, Chromium raster) in `tex_small/r_*.png`. Stills `small_work/stills/room_<PRESET>_<cam>.png`, finals `small_work/final_room_*.png`, contact sheet `small_contact.jpg`.

World: 1 unit = 1 D, Z up, floor z = 0. Back gable wall (window) = plane y = 0 (0.3 thick, outer face y = 0.3), room toward -y to the front gable y = -6. x = 0 = ridge line; knee walls x = +-2.8 at height 1.6, ridge z 5.2 (roof z = 1.6 + (2.8 - |x|) x 1.286). The bed is on the right (+x).

## Functions
```python
import room as R
A = R.build("DAWN" | "NIGHT", clear=True)  # SET + LIGHTS, world, Cycles, grade -> anchors
png = R.book_page_texture()               # the open book's two pages, 1560x1092 PNG (left: lightning -> pointed rod on a roof -> wire down the wall -> stake in the ground; right: handwriting, the point enlarged, a tower without rod split by the bolt). No bpy needed.
cam = R.make_camera(A["cams"]["push_rod"]); R.setup_render(scene, "final" | "preview")
R.placeholder_actor(...), R.stage(A, cam_name), R.no_bounce(card)    # as in vault.py
```
CLI: `python3 room.py stills [preview|final] [DAWN,NIGHT]`, `timing [preset] [cam]`, `digest`, `book`.

## Presets
| preset | key | ambient | notes |
|---|---|---|---|
| `DAWN` | Sun through the window, elevation 30.2 deg, direction (0.300, -0.811, -0.502) (window -> between the book and the rod), angle 0.45 deg, K (2.2, 1.85, 0.75) | blue (0.36, 0.44, 0.90); warm surfaces (plaster, wood, beams) keep a dusky warm shade (shade x (2.4, 1.5, 0.5)), the floor goes blue-violet; dark roof peak and corners; painted warm bounce pool around the light patch | the light patch lands on the floor beyond the bed foot, the lower rod, the bed foot and half the book; window bars throw a cross |
| `NIGHT` | moon, same direction, K (0.62, 0.82, 1.6), artwork pulled 80 % to grey for the key (pale patches) | deep blue (0.15, 0.21, 0.72) | candle flame emits 5.0 (bloom) + an unshadowed painted candle pool (1.3, 0.95, 0.12), r 0.75; night sky with moon and town in the window |

## Anchors
| key | value |
|---|---|
| `room`, `window` | dimensions; window x -0.85..0.45, z 2.55..4.0 in y = 0, centre (-0.2, 0.15, 3.275), cross bars |
| `key_dir`, `sun_elevation_deg`, `light_target` | (0.300, -0.811, -0.502), 30.2, (1.07, -3.28, 1.15) |
| `bed`, `bed_top` | x 1.35..2.62, y -3.5 (foot)..-0.9 (head), mattress top 0.78 |
| `rod_lean` | base (1.10, -3.95, 0), top = tip (2.10, -4.02, 2.40) against a rafter, length 2.60, radius 0.026, pointed last 0.14 D |
| `stool`, `book`, `candle`, `candle_flame` | stool top (0.55, -2.6, 1.0); book centre (0.51, -2.62, 1.05), 0.62 x 0.43, normal +z, top edge +y; candle (0.80, -2.42, 1.0) |
| `crucifix` | (1.25, -0.05, 2.45) on the back gable |
| `hero_mark` | (0.95, -1.55, 0) beside the bed head |
| `bed_sit_mark`, `bed_sit_seat_z` | feet (1.08, -2.15, 0), seat 0.78 |

## Cameras (22 mm)
| name | loc | look_at | shows |
|---|---|---|---|
| `push_rod` | (-1.45, -5.75, 2.1) | (1.5, -3.6, 1.15) | eye level, toward the rod and the bed foot in the light; `move` end loc (-0.55, -4.95, 2.0) look_at (1.55, -3.65, 1.15) |
| `book_insert` | 0.85 D above the book | book centre, up (0, 1, 0) | top-down on the open pages (page diagram readable at 720 px) |
| `room_wide` | (-0.6, -4.95, 4.15) | (0.7, -1.3, 1.25) | high corner under the ridge: window, crucifix, bed, stool, rod |
Rafters at y -0.55, -1.75, -2.95, -4.15, -5.35 hang 0.26 below the roof: keep cameras between them near the roof.

## Measured
- hue_report: DAWN red 36.8 orange 31.7 blue 27.8 violet 0.5 magenta 3.2, sat 0.44 val 0.45 dark 0.08: all in band. NIGHT blue 89.2, violet 1.2, magenta 3.6 (night: blue-dominant expected; reference night frames 74.8 blue).
- shade/lit on the floor light patch (push_rod): 0.29 linear luminance (p10-p90 0.27-0.36), lit hue 10 -> shade hue 243.
- final 720x1280 12 samples 2 threads: 14.1-14.8 CPU s (DAWN push_rod), 14.6-15.1 CPU s (NIGHT room_wide).
- deterministic: digest `9a6c4498...` and bit-identical pixels from two processes.
