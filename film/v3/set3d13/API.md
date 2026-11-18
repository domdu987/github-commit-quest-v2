# v3/set3d13/chicago.py : film 13 set ("ไอ้แม่แรง", raising the Tremont House, Chicago 1861) - FULL SET, QA fix round 1 (bpy 5.3, Cycles CPU)

Files: `chicago.py` (set, hooks, presets, cameras, stand points, crowd helpers, CLI), `chicago_tex.py` (numpy/PIL artwork, cached in `tex_chicago/`; bump `TEX_V` after editing a painter),
`chicago_hue.py` (shade hue + hue families), `t_anim.py` (hook test: `ALL OK (n checks)`), `make_contact.py`, `contact.jpg` / `contact_small.jpg` (17 tiles, one 720x1280 final each, cyan line at y 880,
placeholders at the stand points), `hue_rows.txt` (shade hue AND magenta share per tile), `board/` (the approved style board), `work/` (drafts, `run_finals.sh`, `final_log.txt`, `contact_order.txt`, `final/` = only the 17 tiles).
Imports the old helpers (tower / mine / bakery / desert / wall, harbour_tex.sky_rich) like set3d10. World: 1 unit = 1 D (head), Z up. No DOF, no text.
Light model as film 10: one hard warm sun with real shadows, painted blue-violet shade (hue 240-260), `_untoon` Lambert, point lamps, compositor mist + sun beams, grade with bloom.

```python
import sys; sys.path.insert(0, '.../v3/set3d13'); import chicago as C
A = C.build('front_stair')                 # build(preset, clear=True, light=None, state=None) -> anchors; state string overrides the preset's, e.g. 'lift1,fill0.15'
cam = C.make_camera(A['cam'])              # no DOF, far clip 6000, cards turn to it
C.stage_placeholders(A, A['cam_name'], tuple(cam.location))     # actors at the named stand points + the preset's crowd (PRESET_CROWD, camera-aware)
C.setup_render(bpy.context.scene, 'final' | 'preview'); C.T.render(path)      # or C.render_preset(preset, path, 'final', light=None, state=None)
C.head_pixels(preset)                      # [(role, mark, chin_y, feet_y)] at 720x1280 (rule: chin y < 880)
```
CLI: `python3 chicago.py stills|final [spec ...]`, spec = `preset[:LIGHT[:state]]` (-> work/stills | work/final). `work/run_finals.sh` renders the 17 contact tiles (2 in parallel), then `python3 make_contact.py`.

## Hooks (all take `frame=` for linear keys; `clear_keys()` before re-keying)
| hook | does |
|---|---|
| `set_lift(h, frame)` | street: h 0..1 -> 0..`LIFT_MAX` **3.6 D** (1.2 character heights, ~2 m): hotel, awnings, portico, gap lamps, jack screws/heads and levers rise; **the stair stays at the old street level** (`stair` top z 2.5), so the door threshold (`stand('door')` z = 2.6 + lift) is lift above it; crib layers appear as the building clears them. under: h -> beams (`floor_beams`), slab, screws/heads, levers rise `CELL_LIFT` = 1 D. |
| `set_jack_turn(angle_deg, frame)` | rotates every lever about its screw axis (street 78 jacks, cellar 207 `jf_bar*`). |
| `set_jack_count(n, frame)` | **dense field (under_rows)**: shows the first n of 4992 low-poly jacks (208 chunks of 24, filled from the front); 100 -> 1000 -> 5000 for the count shot (constant keys). |
| `set_bars_visible(v)` | hide the 3D levers when the cast13 `worker_turn_bar_*` sprites (which draw their own bar and jack collar) are used. |
| `set_fill(k, frame)` | street fill: mud, puddles, scum, piles, carts, barrels, planks rise k * `FILL_MAX` (2.5 D); stair, sidewalks, buildings stay. |
| `set_mound(k, frame)` | the side fill mound `mound_side` at (11, -11.5) beside the stair grows 0..1 (3.2 D high); hidden at 0 (front_stair DAY plan 8). |
| `set_wheel_sink(k, frame)` | the stuck cart `cartA_*` at (-24, -35) sinks 0..0.9 D into the mud (the horse `cartA_horse` stays up). Adds with `set_fill`. |
| `set_tea_ripple(k, frame)` | tea surface: 0 = perfectly flat mirror (no normal perturbation), 1 = ripples (4D noise bump; phase follows the frame). |
| `set_rain(level, frame)` | RAIN light only: compositor rain streaks. `build(light='RAIN')` turns it on (level 1). |
| `set_cutaway(on)` | cellar slab + joists (`floor_slab`) invisible to camera AND shadows; the cross beams stay (under_rows). |
| `set_flames(k)`, `clear_keys()`, `apply_state('lift0.5,jack30,fill0.15,mound0.5,sink0.8,count1000,tea0,cut1,rain1')` | |
| `crowd(n, regions, seed, kinds, ground, min_dist, scale, points)` | n cast cards copied from prototypes (shared mesh + material, named `bgcard_*`, turned to the camera every frame). `crowd_view(n, regions, cam, ...)` = same but only points fully inside the camera frame with chin y < 870. `crowd_aisles(n, seed, kinds, rows, cam)` fills cellar aisles. Placeholder roles: worker, foreman, rich, maid, clerk, kid, towns_m, towns_f, towns_o (`T.PH`; swap for v3/cast13 in `T.PH` / `_proto()`). |
| `stand(name)` | stand point at the current lift. `_jack_hands(cam_loc, jx, jy)` = feet for a `worker_turn_bar_*` card so its drawn jack collar (1.22 D right of the feet, waist height) lines up with the 3D jack. |

## Presets (`C.PRESETS`, `C.CAMS`; loc -> look_at, mm) and stand points (`C.STAGING`)
| preset | light, state | camera | staged at |
|---|---|---|---|
| street_wide | DAY lift 0.6 (also RAIN, MORNING via spec) | (-30,-58,2.8) -> (-4,0,15.5), 22: plank leading line, stuck cart + horse, raised left shop | rich@front_a, worker@front_b, foreman@walk_a, clerk@sidewalk_r + 10 cards |
| street_end | MORNING lift 1 fill 0.15 (day 5, plan 28) | (14,-48,2) -> (-4,0,9), 22: the raised base, jacks, cribs and the old stair fill the middle; carts moved out of the way | worker@trench_b, foreman@front_b, clerk@pile_b + 8 cards |
| hotel_front | DAY lift 0.6 (hook; plan 23 plays h 0.5 -> 0.8) | (-4,-24,0.5) -> (0,0,10), 17: worm's-eye, crib pier + spare jack in the left foreground (`prop_cribs`, `prop_jacks`) | rich@top_window (leaning out, moves with lift), worker@hf_c, foreman@hf_a, clerk@hf_b |
| front_stair | DAY lift 1 mound 0.5 (plan 8) / MORNING lift 1 fill 0.15 (ending) | (-13,-13,2) -> (0,-2,4), 22: low three-quarter side view, portico floor edge 3.6 D above the old landing, dark gap with cribs and lit lamps, cream threshold, real door | rich@door, clerk@stair_foot, worker@mud_fall (0.6,-12.5: mud, outside the stair footprint) |
| mud_low | DAY lift 0.5 sink 0.5 (also RAIN) | (-4,-45,1) -> (-19,-35,2.4), 22: stuck cart + horse, puddle mirror | rich@sit_mud (-12.5,-38.5), foreman@pay_a (-9.5,-37.5), worker@cart_a + 5 cards |
| rain_street | RAIN | (-22,-52,3.4) -> (0,0,13), 22 | worker@front_a, clerk@sidewalk_r, foreman@walk_a + 8 cards |
| crowd_street | DAY lift 0.1 | (-6,-34,2.6) -> (0,-8,7.5), 24 | rich@front_c + 26 + 8 cards in frame (`PRESET_CROWD`); jack carriers: marks carry_a / carry_b |
| under_wide | CELLAR lift 0.2 | (3,-3,1.9) -> (3,40,2.2), 20: symmetric aisle x 3, 5 receding oil lamps over the aisle, dust shafts | worker@worker_a..d, foreman@foreman + 14 aisle workers |
| under_rows | CELLAR lift 0.2 cut 1 count 5000 (dense) | (6.5,-12,26) -> (6.5,16,0.5), 28: pitched down 42 deg, no horizon, 4992 jacks each pushing a beam, cut-away brick walls, mud all round | foreman@foreman_far + up to 220 workers (in frame, chin < 870) |
| jack_close | CELLAR lift 0.2 jack 30 | (11.4,12.6,2) -> (7.5,14.1,1.9), 30: one jack (col 5, row 3 at (7.5, 14.1)), dark-iron lever socketed in the head, warm lamp at camera-right | worker@jack_hands = `_jack_hands(cam, 7.5, 14.1)` + 5 |
| suite_window | SUITE | (-2,1.6,32.6) -> (2.2,-14,22.9), 20: the window looks DOWN: street (carts, 46 townsfolk) in the middle third, period shops across, skyline | - |
| suite_room | SUITE | (5.2,13,32.4) -> (-1,0,31.2), 22: red velvet armchair, tea table, chandelier, finer rug, window | rich@window_l |
| tea_close | SUITE tea 0 | (-0.2,5.6,32.9) -> (-3.6,1.9,31.8), 40: cream cup + saucer with gold rims in the sunbeam, tea mirror, window bars behind | - |
| suite_two | SUITE | (-1,5.5,32.7) -> (2.5,-2,30.5), 22: rich man, lady and gentleman at the window | rich@window_r, maid@guest_lady, clerk@guest_gent |
Stand points (x, y, z): **street** `door` (0,-0.9,2.6+lift), `door_b` (-3.5,-0.9), `top_window` (0,-0.5,30.75+lift), `stair_top` (0,-3,2.5), `stair_mid` (0,-6.5,1.3), `stair_foot` (0,-9.6,0), `mud_fall` (0.6,-12.5,0),
`front_a/b/c` (-9,-13) (9,-13.5) (-1.5,-17), `hf_a/b/c`, `walk_a/b/c`, `cart_a/b/c`, `sit_mud` (-12.5,-38.5), `pay_a` (-9.5,-37.5), `trench_a/b` (+-12,-2.4: the gap entrance), `carry_a/b` (-20,-14) (-14,-8.5),
`jack_pile` (-9,-13.5), `shovel_a/b`, `pile_a/b`, `sidewalk_r/l`. **under** `worker_a..d`, `foreman`, `foreman_far`, `pullman_walk_a/b` (3,9) (3,30), `jack_target` (7.5,14.1), `jack_hands`, `aisle_<k>_<j>` (k 0..7, j even 0..22: x = UX[k] + 1.5, y = UY[j] - 1.35).
**suite** `window` (0.8,1,30), `window_l` (-3.2,1), `window_r` (3.4,1), `guest_lady` (-0.8,1), `guest_gent` (1.5,1), `tea_side`, `chair_side`, `room_c`.

## Lights (`LIGHTS`): DAY | RAIN | MORNING (street), CELLAR (under), SUITE (suite)
| light | key | shade | notes |
|---|---|---|---|
| DAY | warm (1.95,1.42,0.82), az 325 el 33 | (0.10,0.105,0.31) | blue day sky `sky_CH_DAY` |
| MORNING | soft gold (1.75,1.28,0.84), az 338 el 17 | (0.105,0.11,0.32) | day 5; sky `sky_CH_MORN` with the magenta pulled out (peach / pale lilac) |
| RAIN | cool grey (0.72,0.72,0.80), el 52, soft | (0.12,0.125,0.335) | blue-grey overcast `sky_CH_RAIN` (no violet), wet mud, lit lamps, rain streaks |
| CELLAR | warm, az 300 el 30 via vents | (0.10,0.10,0.31) | 5-7 oil lamps (point lights + pools + halos), additive dust shafts |
| SUITE | warm, az 305 el 36 through the window | (0.19,0.186,0.48) | sky `sky_CH_SUITE` = the DAY blue sky with a cooled horizon (no golden-hour flip) |

## Coordinates
**street**: street along x, building fronts on y = 0 facing -y. Mud y -70..-8 (smooth height field, ruts, crown, 30 puddle basins with scum rims). Hotel x -20..20, y 0..30, base z 0 (+ lift), plinth top GF 2.6, 7 bays,
storeys 6.2 5.5 5.5 5.2 5.0 4.6, cornice top 40.5; real **doorway** in the centre bay (x -1.8..1.8, door leaves, fanlight, cream surround, proud cream threshold slab) and a cream base course. Gap: 78 dark-iron screw jacks
(13 columns x -18..18, rows y 1.3 6 11 16 21.5 27), 17 crib piers, 9 gap lamps. Stair x -5.4..5.4, y -9..-4 (10 steps, top 2.6, static) + landing to y -1.4. Telegraph poles at x -112 -74 -38 34 72 110 (y -13): none in front of the hotel.
Shops L1..L4 (x -52..-110, L1 raised) and R1..R4 (x 20..102); a belt of ~420 low gabled houses 140..400 D out; church + spire at (105, 210). Props: 3 carts + horses (smoother, jointed), 5 fill piles, shovels, wheelbarrows, brown burlap sacks, plank walks.
**under**: x -9..19 (right wall x = 19 with 6 vents at y 10..60), y -4..68 (front open), floor z 0 earth; cross-beam underside z 2.6 + lift; 207 jacks (9 columns x -7.5 + 3k, 23 rows y 6 + 2.7k), levers 2.8 long at z 1.9 (hand height) turning inside the 3 D aisles.
Dense mode (under_rows): 48 x 104 jacks at 0.56 spacing, thin beams every 1.12, brass caps on top.
**suite**: room x -11..11, y 0..18, floor z 30, ceiling 36.2; floor-length open window x -5..5 (threshold z 30.08); street below built without the hotel; opposite row y -84..-66 at 12.5-21 D (3-4 storeys); table (-3.4, 2.4), cups 1.1 scale.

## Measured (720x1280, 12 samples, 2 threads, OIDN; work/final_log.txt)
Wall 11-21 s, CPU 22-40 s per tile (two processes in parallel; jack_close slowest). Drafts 360x640 6 samples: 2-3 s wall.
