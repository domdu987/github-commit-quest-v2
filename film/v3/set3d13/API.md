# v3/set3d13/chicago.py : film 13 set ("ไอ้แม่แรง", raising the Tremont House, Chicago 1861) - FULL SET (bpy 5.3, Cycles CPU)

Files: `chicago.py` (set, hooks, presets, cameras, stand points, crowd helper, CLI), `chicago_tex.py` (numpy/PIL artwork, cached in `tex_chicago/`, bump `TEX_V` after editing a painter),
`chicago_hue.py` (shade hue + hue families), `t_anim.py` (hook test, prints `ALL OK (75 checks)`), `make_contact.py`, `contact.jpg` / `contact_small.jpg` (15 tiles, one 720x1280 final each, cyan
line at y 880, placeholders at the stand points), `hue_rows.txt` (hue families + shade hue per tile), `board/` (the approved style board), `work/` (drafts, `run_finals.sh`, `final_log*.txt`, `contact_order.txt`).
Imports the old helpers (tower / mine / bakery / desert / wall, harbour_tex.sky_rich) like set3d10; geometry and textures are new. World: 1 unit = 1 D (head), Z up. No DOF, no text.
Light model as film 10: one hard warm sun with real shadows, painted blue-violet shade (hue 240-260), `_untoon` Lambert, point lamps, compositor mist (`air`) + sun beams, grade with bloom.

```python
import sys; sys.path.insert(0, '.../v3/set3d13'); import chicago as C
A = C.build('front_stair')                 # build(preset, clear=True, light=None, state=None) -> anchors; state string overrides the preset's (e.g. 'lift1,fill0.5')
cam = C.make_camera(A['cam'])              # no DOF, far clip 6000, cards turn to it
C.stage_placeholders(A, A['cam_name'], tuple(cam.location))     # actors at the named stand points + the preset's crowd (PRESET_CROWD)
C.setup_render(bpy.context.scene, 'final' | 'preview'); C.T.render(path)      # or C.render_preset(preset, path, 'final', light=None, state=None)
C.head_pixels(preset)                      # [(role, mark, chin_y, feet_y)] at 720x1280 (rule: chin y < 880)
```
CLI: `python3 chicago.py stills|final [spec ...]` with spec = `preset[:LIGHT[:state]]` (-> work/stills | work/final). `work/run_finals.sh` renders the 15 contact tiles (2 in parallel), then `python3 make_contact.py`.

## Hooks (all take `frame=` for linear keys; call `clear_keys()` before re-keying)
| hook | does |
|---|---|
| `set_lift(h, frame)` | street: h 0..1 -> 0..`LIFT_MAX` = **3.6 D** (1.2 character heights, ~2 m). Moves `hotel`, `hotel_awn`, `hotel_portico`, `under_lamps`, the jack screws/heads (`jf_head`) and every lever (`jf_bar<i>`); **the front stair (`stair`) stays at the old street level**, so the door threshold (z = GF + lift = 2.6 + lift) is `lift` above the stair top (z 2.5); timber crib layers (`crib_layer<i>`, 0.5 D each) appear once the building clears them. under: h -> beams (`floor_beams`), screws/heads and levers rise `CELL_LIFT` = 1 D. |
| `set_jack_turn(angle_deg, frame)` | rotates every jack lever about its screw axis (street 78 jacks `jf_bar*`, cellar 230). A half turn = 180. |
| `set_fill(k, frame)` | street fill: mud, puddles, scum, piles, carts, barrels, planks rise k * `FILL_MAX` (2.5 D); buildings, stair, sidewalks stay. |
| `set_tea_ripple(k, frame)` | tea surface: 0 = perfectly flat mirror (no normal perturbation), 1 = ripples (4D noise bump, phase follows the frame). |
| `set_rain(level, frame)` | RAIN light only: compositor rain streaks (2 layers, fall with the frame). `build(light='RAIN')` turns it on. |
| `set_cutaway(on)` | cellar ceiling (beams, joists, slab) invisible to the camera AND to shadows (`under_rows`). |
| `set_flames(k)` | gas / oil lamp glass + point lights (desert). `clear_keys()`, `apply_state('lift0.5,jack30,fill0.4,tea0,cut1,rain1')`. |
| `crowd(n, regions, seed, kinds, ground, min_dist, scale, points)` | n cast cards copied from prototypes (shared mesh + material, **named `bgcard_*`**, turned to the camera every frame by `_cards_face`). `regions` = [(x0,x1,y0,y1)] rejection sampling, or `points=[(x,y)]`; `ground` = z or f(x,y). Uses `placeholder_actor` now; swap `T.PH` entries (roles worker, foreman, rich, maid, clerk, kid, towns_m, towns_f, towns_o) or `_proto()` when v3/cast13 exists. `crowd_aisles(n, seed, kinds, rows)` fills cellar aisles. |
| `stand(name)` | stand point at the current lift (marks flagged 'moves with the lift', e.g. `door`). `A['marks']` has the static ones. |

## Presets (`C.PRESETS`, `C.CAMS`; camera loc -> look_at, mm) and stand points (`C.STAGING`)
| preset | light, state | camera | staged at (role @ mark) |
|---|---|---|---|
| street_wide | DAY, lift 0.7 (MORNING / lift 1 / fill via spec) | (-30,-58,2.8) -> (-4,0,15.5), 22: plank walk leading line, stuck cart + horse, hotel on jacks, left raised shop, right shops | rich@front_a, worker@front_b, foreman@walk_a, clerk@sidewalk_r + 10 street cards |
| hotel_front | DAY, lift 0.7 | (-7,-38,1.6) -> (0,0,13), 18: low, hotel towering | rich@hf_c, worker@hf_b, foreman@hf_a |
| front_stair | DAY, lift 1 | (7,-25,3.4) -> (0,-3,6.2), 24: portico + stair, door 3.6 D above the stair top | rich@door (z = GF + lift), clerk@stair_foot, worker@mud_fall (ending: rich man steps out at `door`, drops to `mud_fall` / mud z 0) |
| mud_low | DAY, lift 0.5 | (-14,-38,0.9) -> (0,-12,3.2), 20: mirror puddles, cart | worker@cart_c, foreman@walk_b |
| rain_street | RAIN, lift 0 | (-22,-52,3.4) -> (0,0,13), 22: overcast swamp street, rain streaks, lit lamps | worker@front_a, clerk@sidewalk_r, foreman@walk_a + 6 cards |
| crowd_street | DAY, lift 0.8 | (-6,-34,2.6) -> (0,-8,7.5), 24: townsfolk laughing at the hotel | rich@front_c + 24 + 8 cards (`PRESET_CROWD`) |
| under_wide | CELLAR, lift 0.2 | (3,-3,2.3) -> (8,30,2.3), 22: rows of jacks to the vanishing point | worker@worker_a..d, foreman@foreman + 16 aisle workers |
| under_rows | CELLAR, lift 0.2, cut 1 | (4,-6,17) -> (5,30,1.5), 24: high angle over 230 jacks | foreman@foreman_far + 70 aisle workers |
| jack_close | CELLAR, lift 0.2, jack 30 | (2,5,2) -> (7,14,2.2), 26: one jack, lever, worker | worker@jack_hands (8.6,12.4) + 6 |
| suite_window | SUITE | (-2,1.6,32.6) -> (2.2,-14,18.5), 20: window looks DOWN on the street (carts, 46 townsfolk) | - |
| suite_room | SUITE | (5.2,13,32.4) -> (-1,0,31.2), 22: red velvet armchair, tea table, chandelier, rug, window | rich@window_l |
| tea_close | SUITE, tea 0 | (3.6,9.6,33.7) -> (0.4,4.9,31.8), 30: cup + saucer, still tea | - |
| suite_two | SUITE | (-5,4.2,32.6) -> (0,-8,28.4), 22: rich man at the window, street beyond | rich@window_l |
Stand points (x, y, z): **street** `door` (0,-0.9,GF+lift), `door_b` (-3.5,-0.9,GF+lift), `stair_top` (0,-3,2.5), `stair_mid` (0,-6.5,1.3), `stair_foot` (0,-9.6,0), `mud_fall` (2,-6.4,0),
`front_a/b/c` (-9,-13) (9,-13.5) (-1.5,-17), `hf_a/b/c` (-9,-10) (9,-10) (-3.8,-11.5), `walk_a/b/c` (-14,-41) (-8,-35) (8,-20), `cart_a/b/c` (-21,-29.5) (-27.5,-31.5) (-14.5,-31),
`pile_a/b` (-30,-20.5) (5,-40), `sidewalk_r` (24,-5.6,0.5), `sidewalk_l` (-36,-5.6,1.3). **under** `worker_a..d`, `foreman`, `foreman_far`, `jack_hands`, `aisle_<k>_<j>` (aisle between jack columns, x = column + 1.3).
**suite** `window` (0.8,1,30), `window_l` (-1.8,0.9), `window_r` (3.4,1.8), `tea_side`, `chair_side`, `room_c`. Every staged chin is below y 880 (t_anim checks it).

## Lights (`LIGHTS`): DAY | RAIN | MORNING (street), CELLAR (under), SUITE (suite)
| light | key (colour, az / el) | shade | notes |
|---|---|---|---|
| DAY | warm (1.95,1.42,0.82), az 325 el 33 (behind camera, right) | (0.10,0.105,0.31) | air #f2c88c, bounce sun, lamps 0.6 |
| MORNING | soft gold (1.75,1.28,0.84), az 338 el 17, sun_angle 2.2 | (0.105,0.11,0.32) | day 5: rosy-gold sky `sky_CH_MORN`, long shadows, lamps 0.35 |
| RAIN | cool (0.62,0.66,0.82), el 52, sun_angle 9 (soft) | (0.12,0.125,0.335) | grey sky, wetter mud (glossy 0.44), lamps + windows glow, rain streaks, heavy mist |
| CELLAR | warm, az 300 el 30 through 6 vents in the right wall (additive dust shafts `shafts`) | (0.10,0.10,0.31) | 7 oil lamps (point lights, pools) |
| SUITE | warm, az 305 el 36 through the window | (0.215,0.185,0.55) | bright shade for the interior; chandelier light |

## Coordinates
**street**: street along x, building fronts on y = 0 facing -y (camera side). Mud street y -70..-8 (smooth height field with wheel ruts at y -26 -29.4 -35 -38.2, crown, 30 elliptical puddle basins incl. long thin
rut puddles; water discs cut by the terrain + a scum disc 0.09 above for soft foam edges; mud shader blends wet-dark by height, soft GGX, glossy bounce mirrors hotel/sky). Sidewalks: right x 20..110 z 0.5,
left x -110..-28 z 1.3 (shop L1 already raised on timber blocks). Hotel x -20..20, y 0..30, base z 0 (+ lift), plinth top GF = 2.6, 7 bays of 5.71, storeys 6.2 5.5 5.5 5.2 5.0 4.6, cornice top 40.5, pediment ~ 43.
Gap: 78 dark-iron screw jacks (13 columns x -18..18, rows y 1.3 6 11 16 21.5 27), 17 timber crib piers (x -19 -9.5 0 9.5 19 at y 1.3 11 21.5, plus (+-5,-2.6) under the portico), 6 warm gap lamps + 3 hanging lamps.
Stair x -5.4..5.4, y -9..-4 (10 steps, top 2.6) + landing to y -1.4, static. Alley x -28..-20; shops L1..L4 x -52..-110, R1..R4 x 20..102. Props: 3 horse carts, 5 fill piles, ~35 barrels, crate stacks, sacks, wheelbarrows, plank walks (3), 7 telegraph poles at y -13, 8 gas lamps, church + spire at (105, 210), pano ring skyline R 420.
**under**: x -9..19 (right x = 19 wall with 6 vents at y 10..60), y -4..68 (front open), floor earth z 0; cross beams every 2.7 D from y 6 (underside z 3.5 + lift), joists, planks; jack grid 10 columns (x -6 + 2.6 k) x 23 rows (y 6 + 2.7 k) = 230 jacks on a timber block + base plank, levers at z 2.7.
**suite**: room x -11..11, y 0..18, floor z 30 (`ZF`), ceiling 36.2; floor-length window x -5..5 (threshold z 30.08, head 35.6) with a see-through iron rail; no balcony ledge so the street stays visible. The street below is the street builder (no hotel): opposite shop row y -84..-66, 3 carts, 46 townsfolk cards.

## Measured (720x1280, 12 samples, 2 threads, OIDN; work/final_log*.txt)
Wall 12-26 s, CPU 21-40 s per frame (two processes in parallel; jack_close the slowest at ~40 s CPU). Drafts 360x640 6 samples: about 2-3 s wall. Shade hue per tile in `hue_rows.txt`.
