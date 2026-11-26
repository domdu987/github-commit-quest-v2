# v3/set3d24/joseon.py : film 24 set ("ไอ้เรือเต่า", Admiral Yi Sun-sin's turtle ship, Joseon Korea 1592)  (bpy 5.x, Cycles CPU, PATH TRACED)

Look (client change "R9 look", qtest/r9_scene.py): Cycles path tracing with GI (diffuse 2, glossy 2), Principled materials with real roughness / bump (plank wood, lacquer,
iron spikes metallic .85, matting sails, rope, stone, tiles), ONE soft warm sun (RGB 1.0 / 0.66 / 0.40, 15-17 deg, 1.5 deg disc, from the camera's left and a little behind it,
re-aimed per preset by `sun_for_camera`), a gradient sky as the world (peach horizon -> blue zenith) as the fill, a THIN volumetric haze (Principled Volume, density 0.0007 yard /
0.0009 sea, anisotropy 0.5, box +-1500) so far ships, islands and mountains fade. DOF only on the macro presets (the camera has `fstop`), everything else is sharp.
Characters stay 2D puppet cards (emission to camera rays only, cast shadows; film-10 `placeholder_actor`). No text anywhere (flags are plain shapes).
Render: 24 samples adaptive (threshold 0.05), OIDN, 75 % = 540x960, then `post()` upscales to 720x1280 (Lanczos) + the R9 grade (bloom on hot spots only, sat x1.15, mild S, vignette <= 5 %, ceiling 0.985).

Files
- `joseon.py` (single module, ~1570 lines) set, hooks, presets, cameras, anchors, `post()`, CLI. Imports film-10/9/2 machinery (`tower.MB` mesh builder, `placeholder_actor`, `harbour_tex.foam`, key helpers); everything visible is new.
- `joseon_tex.py` artwork (hex roof plates, grey roof tiles, ashlar stone, rush matting, dancheong, plain flags, foam lace), cached in `tex_joseon/` (bump `TEX_V`).
- `t_anim.py` hook test, two processes (yard, sea), prints ALL OK. `joseon_hue.py` hue rows + shade hue. `make_contact.py`, `run_finals.sh`, `contact_order.txt`.
- `contact.jpg` / `contact_small.jpg`: 28 finals (18 presets + 10 states), label under each tile, cyan line at y 880. `joseon_work/final/` the PNGs, `final_log.txt` the timing.

World: 1 unit = 1 D (head); people ~3.2 D (cards 2.9-3.3); Z up. Ships are built in ship-local axes: x bow (+) / stern (-), y starboard, z up, waterline z 0.
`S` (= `J.S`) is the scene state dict.

## Locations
### yard : Joseon naval yard, Yeosu, daytime (calm harbour water z 0, land z 2.2, wharf z 2.25)
- Slipway: stone-walled trench x -7..7, y -17.5..-3.5 cut into the land, ramp slab sloping 7 deg down into the water (water edge at y ~ -0.3), guide piles in the water.
- The TURTLE SHIP lies on cradles on the slip: ship +x = world +y (bow in the water at y +18, dragon head to y +19), ship +y = world -x. Root (0, -1.5, 2.56) yaw 90, bow-down pitch 7 deg
  (carried by the `ride` empty). Cradle blocks, sliding rails and slanted shores are world-fixed timbers. `J.yw((x, y, z))` maps ship-local -> world.
- East wharf (L-shaped timber quay on piles) x 7.4..17, y -16..21: timber stacks, plank piles, rope coils, baskets, barrels, 3 chongtong cannons on low carts, flag poles, bollards. West landing stage x -17..-7.
- Land: 5 workshop sheds with grey tiled hip roofs (concave slopes, up-turned corners, plaster walls, lattice windows, red beams), a dancheong pavilion (red pillars, red/blue/green beams, tiled roof, steps) at (24, -42),
  a shear-legs crane with tackle at (12.5, -19), a stone fortress wall ring with merlons + gate pavilion + watch tower on the hill at (-70, -135), 300 pines (instanced kit), green-brown hills.
- Bay: 5 panokseon moored (pk1 / pk2 along the wharf with mooring lines, pk3-5 in the bay; oars stowed along the hull), 3 rocky green islands with pines, far mountains.
### sea : Hansan waters, daytime (bright, a little hazy; water z 0 with the film-10 animated swell, physically shaded deep blue-green, Fresnel, whitecaps, sun glitter)
- Japanese fleet (hook `set_fleet_chase`), 26 ships sailing +x: 8 atakebune (castle ships: black lacquer hull + red band, loophole wall, upper deck with railing, 2-storey tower with white plaster, tile roof and
  gold ridge ends, white nobori banners on poles; some with a square cloth sail) `jflag` (flagship: stage with taiko drum + weapon rack), `j_near`, `j_board`, `j4..j8`; 18 sekibune `s01..s18` (slender, shield boards, sail on every 3rd).
  Every ship differs in length (+-2.5), scale (0.9-1.12), heading, tower height, band / roof colour, banner count, sail.
- Korean fleet: the TURTLE SHIP `turtle` (sea version, masts, no sail) and 7 PANOKSEON `k1..k7` (two-deck: gun-port casemate with flat top deck + railing, tiled deck house, 2 masts with matting sails, red / black flags, 9 oars per side).
- 5 rocky green islands (`isl_a..e`) with instanced pines and boulders, the beach island `beach` at (-150, 150) (sand, 40 pines, surf foam lines driven by the swell), the floating PLANK, far mountain ring.
- Ships heave on the SAME swell as the ocean mesh: drivers read the ship root x, y (so they sit in the water at every frame); foam / oar rings are swell-driven flat strips; oars stroke by driver.

## Functions
```python
import sys; sys.path.insert(0, ".../v3/set3d24"); import joseon as J
A = J.build('yard', 'roof_low')              # build(location=None, preset=None): the preset decides the location; returns anchors()
cam = J.make_camera(A['cam'])                # dict {loc, look_at, lens[, fstop, focus]}; DOF only when fstop is given; nothing is parented to the camera
J.stage_placeholders(A, A['cam_name'], A['cam']['loc']); J.head_pixels(cam_name)     # placeholder cards at the anchors (film-10 puppets), chin px check
w, c = J.render_still(path, 'final')         # 540x960 render + post() -> 720x1280. J.post(src, dst) is the grade alone.
J.clear_keys()                               # drops hook keys, keeps the drivers
J.ship_root(name)                            # the `ride` empty of a ship: PARENT deck / roof cards to it ('turtle', 'jflag', 'j_near', 'j_board', 'k1'...). J.ship_motion_root(name) = the moving root
```
Keys rule: once a hook was keyed with `frame=`, keys win over un-keyed calls: key every state or call `clear_keys()` first. Smoke hooks must be called EVERY frame.

## Hooks (both locations unless noted)
| hook | what |
|---|---|
| `set_spikes(rows_k, frame=None)` | turtle roof iron spikes (dark steel cones, 3 stages of 3 lines per side, ridge -> eave, ~420 spikes): stage j shown when rows_k >= j. 0 none, 3 full roof. Keys constant (pop-in on the hammer beat). |
| `set_ports(k, frame=None)` | 12 gun ports (6 per side): 0 lids shut (red lids with a gold boss), 1 lids hinged open 72 deg and iron cannon muzzles poking out (muzzles show from 0.5). Keys linear. |
| `set_dragon_smoke(level, frame=None, speed=1)` | grey-yellow cartoon smoke billows from the dragon's mouth (10 puffs, hard round silhouettes). 0 none .. 1 .. 1.5. Call every frame. |
| `set_cannon_smoke(level, frame=None)` | sea: smoke puffs + 3-frame muzzle flashes at every Korean gun port (turtle 12 + 7 x 10 = 82 guns); the fraction `level` of the guns fires, each on its own 1.2-1.7 s cycle. Every frame. |
| `set_fleet_chase(s, frame=None)` | sea: the Japanese fleet sails +x by CHASE_V (3 D/s) x s; the Korean ships keep their offset, so the picture holds. Keys linear. |
| `set_korean_turn(k, frame=None)` | sea: 0 = Korean ships (turtle + 7 panokseon) fleeing AHEAD of the pursuers, 1 = turned into the U (crane wing: arc R 78 round the front, arms 150 long back along both flanks, turtle ship front centre, all facing in). Linear. |
| `set_damage(k, frame=None)` | sea: ships are hit one after another (72 % of the Japanese fleet, thresholds 0.03..0.65): list 3-8.5 deg, mast + sail replaced by a stump with a splintered top lying on the deck, grey smoke column. No fire, no people, no bodies. |
| `set_special(name, frame=None)` | sea: `'board'` puts the turtle ship and `j_board` alongside (10.3 D apart) at BOARD_AT; `'solo'` puts the turtle ship alone at SOLO_AT (macro_oar). `''` back to the formation. |
| `build_...` | `build_turtle`, `build_panokseon`, `build_atakebune`, `build_sekibune` (`sea=False` = moored / on the slip, oars stowed). The turtle ship is one function used by both locations. |

Heading convention: the spec said the fleeing Koreans head -x while the Japanese chase +x; that cannot be a chase, so the fleeing Koreans head +x (away from the pursuers) and turn back to face them (U).
`CHASE_V` / `BOARD_AT` / `SOLO_AT` / `U_C, U_R, U_ARM` are module constants.

## Presets (`J.PRESETS`, `J.LOC_PRESETS`); lens on a 36 mm sensor (film-10 convention)
| preset | loc | shot | camera (loc -> look_at, lens) |
|---|---|---|---|
| `roof_low` | yard | 1 | (15.8, 9, 3.6) -> (-0.5, -3.5, 5.9), 22 : low 3/4 from the wharf, roof-edge workers, Yi in front |
| `bow` | yard | 2 | (6.6, 27, 4) -> (4.8, 15, 4.3), 26 : dragon head over the water, Yi on the wharf beside the bow |
| `yard_wide` | yard | 4 | (16, 24.5, 7.6) -> (-3, -10, 5), 21 : ship, sheds, pavilion, fortress hill behind |
| `roof_top` | yard | 8 | (-9.5, -29, 15) -> (0.8, -4, 5.2), 24 : high 3/4 over the roof, workers kneeling on the roof edge |
| `macro_spikes` | yard | insert | 60 mm f/2.8, port roof edge, yard in bokeh (rows appear with `set_spikes`) |
| `macro_dragon` | yard | insert | 55 mm f/2.8 on the dragon mouth, bay in bokeh (`set_dragon_smoke`) |
| `fleet_wide` | sea | 3 | (-55, -118, 16) -> (-62, 0, 8), 26 |
| `flag_deck`, `flag_deck_b`, `flag_deck_crew` | sea | 5, 6, 7 | on the flagship `jflag` upper deck (stage: tower, banners, drum, weapon rack), three angles |
| `hansan_high` | sea | 9 | (60, -330, 150) -> (50, 0, 0), 22 |
| `flag_bow` | sea | 10 | ahead of the flagship bow, commander at the bow rail, the fleet behind |
| `chase` | sea | 11 | on `j_near`'s bow deck: 3 soldier spots |
| `board` | sea | 12 | from the deck of `j_board` over its railing onto the spiked roof of the turtle ship alongside (state `special:board`) |
| `reveal_top` | sea | 13 | (-22, -250, 185) -> (-22, 2, -5), 22 : the U, cannon smoke, damage 0.35 |
| `aftermath` | sea | 14 | low behind the turtle ship at the U front, smoke, Japanese ships listing (dm 1) |
| `shore` | sea | 15 | beach island: plank on the swell near the surf, sand above it |
| `macro_oar` | sea | insert | 55 mm f/2.8 low at the water on an oar blade dipping with foam ring + spray (state `special:solo`) |

CLI state tokens: `sp<k>` spikes, `pt<k>` ports, `ds<level>` dragon smoke, `s<sec>` chase, `k<turn>`, `cs<level>` cannon smoke, `dm<k>` damage, `special:board|solo`.
`python3 joseon.py final|stills [preset[:state[:cam]] ...]` ; `./run_finals.sh` then `python3 make_contact.py`.

## Anchors (`A['marks']` world feet; `A['parented']` = ship + ship-local point for cards that must ride a ship: parent them to `J.ship_root(ship)`)
- yard: `yi_quay` (9.5, 1.2), `yi_bow` (9.2, 14), `yi_front` (8.6, -2.3), `worker_quay_a/b/c`, `worker_land_a`; roof-edge workers `worker_roof_p1..p4` (port = east side) and `worker_roof_s1..s4` (starboard):
  parent `turtle`, local (x, +-0.99 x half-width, roof surface) with x = -8, -3, 2.5, 7.5: they stand ON the roof surface at the edge (checked by ray cast in t_anim).
- sea: `commander_deck`, `soldier_deck_a..d` (parent `jflag`); `commander_bow` (`jflag`); `soldier_chase_a..c` (`j_near`); `soldier_board_a..c` (`j_board`, the rail beside the turtle ship); `commander_plank` (on the plank),
  `commander_sand`, `commander_crawl_a` (beach); `turtle_deck`. Cards: roles `yi`, `worker`, `commander`, `soldier`, `soldier_b` (film-10 puppets as placeholders).

## Measured (joseon_work/final_log*.txt, hue_rows.txt)
- Render cost, 720x1280 final = 540x960 at 24 adaptive samples + OIDN + post, 2 threads on the shared 4-core box: **36-57 s wall, 70-123 s CPU per frame**
  (yard 76-87 CPU s, sea wide 70-104, board 91, macros 77-123; macro_oar 110-123 and macro_dragon 111 are the heaviest). On 4 free cores that is about CPU / 4 = **18-31 s per frame** (all <= 35 s).
  Post adds ~1 s. Scene build 10-20 s per preset.
- Colour shares (whole frame, COLOUR_SPEC bands are relaxed for these exteriors): yard frames red 21 %, orange 29 %, blue 29 %, cyan 13 %, sat 0.34, val 0.58, dark 6 %;
  sea frames blue 61 %, cyan 19 %, red + orange 17 %, sat 0.39, val 0.61 (water and sky dominate; red / orange only from the ships). Purple 0.1-1 %, magenta 0.8 %.
- **Shade hue** (`joseon_hue.py`): 170-222 deg, i.e. NOT in 240-260. The shade is lit by a blue-to-peach sky and by the blue-green water, and AgX keeps the teal;
  the blue-violet shade of film 10 came from painted emission shade, which the path-traced look does not have. Raising it would need a more violet sky fill (zenith #3a6ccc -> #5a58c8) and a violet water tint.
- `t_anim.py`: ALL OK (34 yard + 43 sea checks, two processes).

## Known limits
- Shade hue and colour shares are outside the film-10 / COLOUR_SPEC bands (see above); exteriors, daytime sea.
- The Korean fleeing direction is +x (see Hooks); the spec's "-x" contradicts a chase.
- Spikes pop in stage by stage (no growth animation); 3 stages of 3 lines, outer lines point upward so the roof edge stays free for kneeling workers.
- Ships are low-poly cartoon forms (dragon head, castle ships) lit physically; the dragon head is faceted. Atakebune have a rounded hull plan; no crew on any ship (cards only).
- Roof workers are upright cards standing on the roof edge (no kneeling pose in the placeholder puppets). Anchors are nominal (calm water): cards parented to `ship_root()` follow the heave.
- The haze is a box volume of +-1500: cameras must stay inside it. Far mountains / islands beyond 1100 D fade to the sky.
- The swell moves with the frame number (30 fps); foam is flat strips on drivers, not a fluid. Boarding ladder, rigging blocks and lanyards are not modelled.
- `reveal_top` and `hansan_high` are very high: ships are 30-60 px long, the U and the smoke read as shapes, not as detail. Use `aftermath` / `chase` for close ship detail.
- The 27 + 1 contact tiles use film-10 puppets as placeholders; stage_placeholders faces them to the camera; chin check: every staged chin is above y 880 (head_pixels); in `board` the nearest soldier's head is large (about 345 px) because the rail is close.
