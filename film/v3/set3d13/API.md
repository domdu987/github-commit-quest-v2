# v3/set3d13/chicago.py : film 13 set ("ไอ้แม่แรง", Tremont House, Chicago 1861) - STYLE-BOARD build (bpy 5.3, Cycles CPU)

Files: `chicago.py` (set, hooks, presets, cameras, CLI), `chicago_tex.py` (numpy/PIL artwork, cached in `tex_chicago/`, bump `TEX_V` after editing a painter),
`chicago_hue.py` (shade hue + hue families), `board/` (3 stills 720x1280, `board.jpg`, `board_small.jpg`), `work/` (drafts, `run_board.py`, `final_log.txt`).
Imports the old helpers (tower / mine / bakery / desert / wall, harbour_tex.sky_rich) exactly like set3d10; all geometry and textures here are new.
World: 1 unit = 1 D (head), Z up. No depth of field, no text anywhere. Same light model as film 10: one sun with real shadows, painted blue-violet shade, `_untoon` Lambert, point lamps.

```python
import sys; sys.path.insert(0, '.../v3/set3d13'); import chicago as C
A = C.build('street_wide')          # build(preset, clear=True, light=None) -> anchors; applies the preset's state string
cam = C.make_camera(A['cam'])       # no DOF, far clip 6000
C.stage_placeholders(A, A['cam_name'], tuple(cam.location))   # placeholder_actor cards (roles worker / foreman / rich / maid / clerk)
C.setup_render(bpy.context.scene, 'final' | 'preview'); C.T.render(path)   # or C.render_preset(preset, path, 'final')
```
CLI: `python3 chicago.py stills|final [preset ...]` (-> work/stills | work/final). Board: `python3 work/run_board.py <preset> board/<preset>.png`.

## Locations / presets (`C.PRESETS`, `C.CAMS`)
| preset | loc / light | state | camera (loc -> look_at, mm) | status |
|---|---|---|---|---|
| street_wide | street / DAY | lift0.5 | (-16,-58,2.4) -> (2,0,15), 22 | on the board |
| hotel_front | street / DAY | lift0.5 | (-8,-30,2.4) -> (0,0,15), 22 | camera NOT tuned |
| front_stair | street / DAY | lift1 | (2,-16,3) -> (0,0,6), 24 | NOT tuned (ending fall) |
| mud_low | street / DAY | lift0.3 | (-12,-40,1.1) -> (4,-6,7), 22 | NOT tuned |
| under_wide | under / CELLAR | - | (5,-2,2.5) -> (9,30,2.9), 22 | on the board |
| jack_close | under / CELLAR | - | (4,8,2) -> (8,20,2.4), 24 | NOT tuned |
| suite_window | suite / SUITE | - | (4.6,10.2,32.2) -> (-0.4,0,30.9), 22 | on the board |
| tea_close | suite / SUITE | - | (-1.5,9.5,30.9) -> (-2.2,5,30.3), 26 | NOT tuned |
State string (CLI/`apply_state`): `lift<k>`, `fill<k>`. RAIN light (overcast swamp street) is NOT built.

## Hooks (street only; all take `frame=` for linear keys)
- `set_lift(h, frame=None)` : h 0..1 -> 0..`LIFT_MAX` (6.0 D; deliberately larger than the film's ~2 m so the gap reads). Moves the whole hotel (`hotel`, `hotel_awn`, `hotel_portico`,
  `under_beams`, `under_lamps`, jack heads) by z; the jack screws (`jf_screw`) and the 10 stair carriages (`stair_body_i`) stretch in z; the 10 stone treads (`stair_tread_i`) rise
  with it (rise = (GF + lift) / 10); timber crib layers (`crib_layer<i>`, every 0.5 D, 13 objects) are shown only once the building clears them (hide_render keys).
- `set_fill(k, frame=None)` : k 0..1 raises mud, puddles, piles, carts, barrels, planks (`fill_objs`) by k * `FILL_MAX` (3.0 D). Buildings and sidewalks stay.
- `set_flames(k)` (desert): gas / oil lamp glass + point lights. `clear_keys()` drops all keys.
Not done yet: workers, the whistle, smoke, rain, set_lift for the cellar (cellar jacks are fixed at beam height 5.0), crowd cards.

## Coordinates (street)
Street runs along x. Building fronts on y = 0, facing -y (camera side). Mud street y -46..-8, ground z 0 (height field with ruts, crown and 15 puddle basins `PUDDLES`; flat water discs
cut by the terrain; mud shader blends wet-dark by height and has a GGX lobe; glossy bounce 1 mirrors hotel and sky in the puddles). Sidewalks (planks): right x 20..110 at z 0.5,
left x -110..-28 at z 1.3 (the already-raised neighbour L1 sits on timber blocks), y -8.5..-3.
- Hotel: x -20..20, y 0..30, 7 bays of 5.71, plinth top GF = 2.6, storeys 6.2 5.5 5.5 5.2 5.0 4.6 (floor levels `ZS`), cornice top ~ z 40.5, pediment ~ 43 (+ lift). Window reveals are real
  geometry (`_openings`). Centre bay (index 3, x -2.9..2.9) = door + portico (columns x +-1.8 / +-4.3, y -3.3, landing y -4..0) + stair (x -5.4..5.4, y -9..-4).
- Jacks: 13 columns x -18..18 (step 3), rows y 1.6 6.2 11 16 21.5 27 (skipped near crib piers x -19.2 -9.6 0 9.6 19.2). 78 jacks (`jf_*`).
- Neighbours: left alley x -28..-20, shops L1..L4 x -52..-28..-110 (painted facades `fac_a..f`, cornices, awnings), right R1..R4 x 20..102. Carts (barrels / crates + horses) `_cart`, fill piles
  `_mound` (smooth), barrels, crate stacks, plank walks, 7 telegraph poles at y -13 with wires, 8 gas lamps, hitching posts, church + spire at (105, 210).
- Marks used for placeholders: see `C.STAGING` (street_wide: rich (-6.5,-14), worker (9,-13), foreman (-9,-41), clerk (22,-9.2,z0.5)).
## Cellar (`under`)
Crawlspace x -9..19, y -4..56, floor z 0 (right side x=19 open to the sunlit street), cross beams every 3.4 D from y 6 (underside z 5.0), joists along y, floor boards z 7.4.
Jack field 8 columns (x -6 + 3.2 k) x 13 rows (y 6 + 3.4 k), 6 oil lamps (`lamps` list; real point lights, 4 with shadows, halo, warm pool decal), crates, barrels, leaning bars.
Marks: worker_a..d, foreman (see `anchors()['marks']`).
## Suite (`suite`)
Room x -11..11, y 0..18, floor z 30 (`ZF`), ceiling 36.2. Window in the y = 0 wall: x -3.6..3.6, sill z 30.35, head 35.4. The street (terrain, puddles, carts, the opposite shop row
y -52..-36) is built outside. Furniture: red + teal velvet armchairs, round tea table (x 0.8, y 4.6) with cups, saucers, pot, cakes; chandelier (x -0.8, y 4.6); 6 gilt-framed paintings
(no text); rug, parquet, wallpaper (damask), dado, drapes.

## Light presets
| light | key | shade | notes |
|---|---|---|---|
| DAY | warm (1.95,1.42,0.82), sun az 325 el 33 (right-front, behind camera) | (0.10,0.105,0.31) | air #f2c88c, bounce sun, lamps 0.6 |
| CELLAR | warm, az 342 el 27 (through the open right side) | (0.092,0.108,0.30) | lamps 1.0 (oil lamp point lights are the real fill) |
| SUITE | warm, az 305 el 36 (through the window) | (0.20,0.19,0.55) | brighter shade for the interior, chandelier light |

## Measured (720x1280, 12 samples, 2 threads, OIDN; work/final_log.txt)
Wall 10.4-12.4 s, CPU 21.1-24.9 s per frame (draft 360x640 6 samples about 2 s wall). Shade hue (chicago_hue.py): street_wide 256.7, under_wide 251.9, suite_window 250.3 (target 240-260).
