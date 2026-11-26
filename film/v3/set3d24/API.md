# v3/set3d24/joseon.py : film 24 set ("ไอ้เรือเต่า", Admiral Yi Sun-sin's turtle ship, Joseon Korea 1592)  (bpy 5.x, Cycles CPU, PATH TRACED)

Look (client change "R9 look", qtest/r9_scene.py): Cycles path tracing with GI (diffuse 2, glossy 2), Principled materials with real roughness / bump (plank wood, lacquer,
iron spikes metallic .85, matting sails, rope, stone, tiles), ONE soft warm sun (RGB 1.0 / 0.66 / 0.40, 15-17 deg, 1.5 deg disc, from the camera's left and a little behind it,
re-aimed per preset by `sun_for_camera`), a gradient sky as the world (peach horizon -> blue zenith) as the fill, a THIN volumetric haze (Principled Volume, density 0.0007 yard /
0.0009 sea, anisotropy 0.5, box +-1500) so far ships, islands and mountains fade. DOF only on the macro presets (the camera has `fstop`), everything else is sharp.
**Shade hue of the exteriors is 170-222 deg** (measured, `joseon_hue.py`), not the film-10 blue-violet 240-260: the shade is lit by the blue-to-peach sky and the deep teal-blue water; accepted for exteriors, explained in QA.md.
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
- Japanese fleet (hook `set_fleet_chase`), 26 ships sailing +x, period built: 8 atakebune (castle ships: brown plank hull, tall boxy WOODEN fighting wall of dark-brown planks with a few black / red lacquer panels
  and small loopholes, upper deck with railing, two-storey dark-wood castle (yagura) with small plaster panels at most, a tiled skirt roof + curved tiled hip roof, gold ridge ends, cloth nobori banners with a plain circle or
  diamond mon on poles at the deck corners; every 2nd one carries a square cloth sail with seams) `jflag` (flagship: stage with taiko drum + weapon rack, black-circle banners), `j_near`, `j_board` (with a boarding ladder
  hooked over its rail), `j4..j8`; 18 sekibune `s01..s18` (slender brown plank hulls, shield boards of planks and lacquer, small wooden cabin with a tiled roof, mon nobori, square cloth sail on every 2nd).
  No continuous red stripe, no white box cabin. Every ship differs in length (+-2.5), scale (0.9-1.12), heading, tower height, roof tone, banner count / mon, sail.
- Korean fleet: the TURTLE SHIP `turtle` (sea version, masts, no sail) and 7 PANOKSEON `k1..k7`, clearly different from the Japanese: red-brown plank hull and casemate, green bulwark, green + red dancheong trim beams along the
  casemate top, an open hip-roofed deck pavilion (red pillars, dancheong beams, railing, grey tiled roof), 2 matting sails, red / black flags, 9 oars per side.
- 5 rocky green islands (`isl_a..e`) with instanced pines and boulders, the beach island `beach` at (-150, 150) (sand, 40 pines, surf foam lines driven by the swell), the PLANK half-beached at the surf line (lies on the sand in very shallow water, surf foam washing round it), far mountain ring.
- Water: deep teal-blue with darker troughs, crest tint, whitecaps, Fresnel sky mirror and sun glitter; swell amplitudes 0.34 / 0.20 / 0.11 D.
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
| `set_oar_splash(t, frame=None)` | sea (macro_oar): spray at the dipping blade of the turtle ship's hero oar (starboard oar 5, no stroke driver): 70 small droplets on ballistic arcs that shrink, plus two foam rings that grow and fade. t 0 = nothing; 0..1 = the splash; for a 15-frame splash key `t = (frame - f0) / 15` every frame. Keys linear (visibility constant). CLI token `os<t>`. |
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
| `macro_spikes` | yard | insert | 60 mm f/2.8 on the port roof aft of the cross walkway (no walkway in frame), yard in bokeh (rows appear with `set_spikes`) |
| `macro_dragon` | yard | insert | 55 mm f/2.8 on the dragon mouth, bay in bokeh (`set_dragon_smoke`) |
| `fleet_wide` | sea | 3 | (-55, -118, 16) -> (-62, 0, 8), 26 |
| `flag_deck`, `flag_deck_b`, `flag_deck_crew` | sea | 5, 6, 7 | on the flagship `jflag` upper deck (stage: tower, banners, drum, weapon rack), three angles |
| `hansan_high` | sea | 9 | (60, -330, 150) -> (50, 0, 0), 22 |
| `flag_bow` | sea | 10 | ahead of the flagship bow, commander at the bow rail, the fleet behind |
| `chase` | sea | 11 | on `j_near`'s bow deck: 3 soldier spots |
| `board` | sea | 12 | camera over the turtle roof looking at the rail of `j_board`: 3 soldier cards stand at the rail in the upper half (heads y 340-360, chin <= 423 px, nearest head 144 px), the hooked boarding ladder hangs between them, the spiked roof fills the lower half; sharp (no DOF). The caller pushes in from `cams['board']` to `cams['board_end']` (down onto the spikes). State `special:board`. |
| `reveal_top` | sea | 13 | (-22, -250, 185) -> (-22, 2, -5), 22 : the U, cannon smoke, damage 0.35 |
| `aftermath` | sea | 14 | low behind the turtle ship at the U front, smoke, Japanese ships listing (dm 1) |
| `shore` | sea | 15 | beach island: the plank lies half-beached at the surf line, sand above it. The staging has NO card on the plank (the lying commander is added by the cast); `commander_plank` is the anchor on the plank top, `commander_sand` / `commander_crawl_a` on the sand |
| `macro_oar` | sea | insert | 40 mm f/2.8 at 1.3 D above the water from outside the blade: the oar enters the water, droplets and foam rings (`set_oar_splash`, preset t 0.4); state `special:solo,os0.4`; rendered at 14 samples |

CLI state tokens: `sp<k>` spikes, `pt<k>` ports, `ds<level>` dragon smoke, `s<sec>` chase, `k<turn>`, `cs<level>` cannon smoke, `dm<k>` damage, `special:board|solo`.
`python3 joseon.py final|stills [preset[:state[:cam]] ...]` ; `./run_finals.sh` then `python3 make_contact.py`.

## Anchors (`A['marks']` world feet; `A['parented']` = ship + ship-local point for cards that must ride a ship: parent them to `J.ship_root(ship)`)
- yard: `yi_quay` (9.5, 1.2), `yi_bow` (9.2, 14), `yi_front` (8.6, -2.3), `worker_quay_a/b/c`, `worker_land_a`; roof-edge workers `worker_roof_p1..p4` (port = east side) and `worker_roof_s1..s4` (starboard):
  parent `turtle`, local (x, +-0.99 x half-width, roof surface) with x = -8, -3, 2.5, 7.5: they stand ON the roof surface at the edge (checked by ray cast in t_anim).
- sea (the `shore` plank anchor is `commander_plank` = plank top, lying pose): `commander_deck`, `soldier_deck_a..d` (parent `jflag`); `commander_bow` (`jflag`); `soldier_chase_a..c` (`j_near`); `soldier_board_a..c` (`j_board`, the rail beside the turtle ship); `commander_plank` (on the plank),
  `commander_sand`, `commander_crawl_a` (beach); `turtle_deck`. Cards: roles `yi`, `worker`, `commander`, `soldier`, `soldier_b` (film-10 puppets as placeholders).

## Measured (joseon_work/final_log*.txt, hue_rows.txt)
- Render cost, 720x1280 final = 540x960 at 24 adaptive samples + OIDN + post, 2 threads on the shared 4-core box: **36-57 s wall, 70-123 s CPU per frame**
  (yard 76-87 CPU s, sea wide 70-104, board 91, macros 77-123; macro_oar 110-123 and macro_dragon 111 are the heaviest). On 4 free cores that is about CPU / 4 = **18-31 s per frame** (all <= 35 s).
  Post adds ~1 s. Scene build 10-20 s per preset.
- Colour shares (whole frame, COLOUR_SPEC bands are relaxed for these exteriors): yard frames red 24 %, orange 29 %, blue 31 %, cyan 8 %, sat 0.35, val 0.5-0.6;
  sea frames blue 66 %, cyan 7 %, red + orange 24.5 %, sat 0.40, val 0.5-0.6 (water and sky dominate; red / orange only from the ships). Purple 0.1-1 %, magenta 0.8 %.
- **Shade hue** (`joseon_hue.py`): 174-225 deg, i.e. NOT in 240-260. The shade is lit by a blue-to-peach sky and by the blue-green water, and AgX keeps the teal;
  the blue-violet shade of film 10 came from painted emission shade, which the path-traced look does not have. Raising it would need a more violet sky fill (zenith #3a6ccc -> #5a58c8) and a violet water tint.
- `t_anim.py`: ALL OK (34 yard + 49 sea checks, two processes).

## Known limits
- Shade hue and colour shares are outside the film-10 / COLOUR_SPEC bands (see above); exteriors, daytime sea.
- The Korean fleeing direction is +x (see Hooks); the spec's "-x" contradicts a chase.
- Cost: macro_oar (DOF, glossy water close up, 70 droplets) is the heaviest frame: rendered at 14 samples; on the loaded box it measured 120-125 CPU s, which is ~25-30 s on 4 free cores. All other frames 66-102 CPU s (17-26 s on 4 cores) with the other worker's load at 4-5.
- Spikes pop in stage by stage (no growth animation); 3 stages of 3 lines, outer lines point upward so the roof edge stays free for kneeling workers.
- Ships are low-poly cartoon forms (dragon head, castle ships) lit physically; the dragon head is faceted. Atakebune have a rounded hull plan; no crew on any ship (cards only).
- Roof workers are upright cards standing on the roof edge (no kneeling pose in the placeholder puppets). Anchors are nominal (calm water): cards parented to `ship_root()` follow the heave.
- The haze is a box volume of +-1500: cameras must stay inside it. Far mountains / islands beyond 1100 D fade to the sky.
- The swell moves with the frame number (30 fps); foam is flat strips on drivers, not a fluid. Boarding ladder, rigging blocks and lanyards are not modelled.
- `reveal_top` and `hansan_high` are very high: ships are 30-60 px long, the U and the smoke read as shapes, not as detail. Use `aftermath` / `chase` for close ship detail.
- The 27 + 1 contact tiles use film-10 puppets as placeholders; stage_placeholders faces them to the camera; chin check: every staged chin is above y 880 (head_pixels); in `board` the nearest soldier's head is large (about 345 px) because the rail is close.

## flag_deck_crew: the open deck and the crew spots
The flagship `jflag` has an open upper deck in front of the cabin: x -4.0 .. 10.6 (14.6 D) by about 8 D wide at z 5.44 (ship-local; the tower stands aft of x -4.0; the drum and the weapon rack sit at the bow corners, y -3.0 / +3.2).
Planted soldier cards, nearest to the `flag_deck_crew` camera first (camera at ship-local (9.9, 0, 7.5), 22 mm, looking aft). All stand on deck z 5.44 (feet) and are parented to `J.ship_root('jflag')`; heights (cards 2.9 D `soldier` / 3.1 D `soldier_b`) keep true perspective:

| order | anchor | ship-local (x, y, z) | distance to camera | head px | chin y px | feet y px |
|---|---|---|---|---|---|---|
| 1 | `soldier_deck_c` (soldier) | (4.42, 3.2, 5.44) | 7.3 | 132 | 696 | 941 |
| 2 | `soldier_deck_d` (soldier_b) | (4.02, -3.3, 5.44) | 7.8 | 123 | 666 | 919 |
| 3 | `soldier_deck_a` (soldier) | (2.62, 2.2, 5.44) | 8.6 | 99 | 674 | 859 |
| 4 | `soldier_deck_b` (soldier_b) | (2.22, -2.0, 5.44) | 9.0 | 94 | 652 | 846 |
(the `commander_deck` stand is (5.9, 0, 5.44), 5.9 D ahead of the tower front.) Farther cards have smaller heads and higher feet, as in true perspective; every chin is above y 880.

## Round 3 notes (API unchanged)
- Water tiling fixed: the ocean mesh carries 5 incommensurate long swells (41 / 27 / 17.3 / 11.7 / 9.9 D, total amplitude 0.7 D) and no short chop (it aliased against the 2.4 D cells as a grid of blobs from high cameras); fine chop is bump only, fading with view distance;
  trough darkness and whitecaps are modulated by large-scale noise and fade out beyond 80-260 D. Ships, foam, plank and rings use the same 5 waves (compact driver expressions < 255 chars; `swell_expr_at` for fixed points, `drive_at` for root-local points).
- Oar splash: ~46 droplet STREAKS (elongated, oriented along their arcs) + two soft partly transparent irregular foam patches that grow and fade (no ring); the oar foam patches at the other blades use the same soft texture.
- Smoke (cannon grey-white, dragon grey-yellow, damage dark grey): each puff / column is a cluster of overlapping lumps with a soft facing-ratio alpha edge (partly transparent, no shadow), so they merge into billows. Same hooks, same per-frame call rule.
- Cost under the other worker's load (4-5): smoke-heavy frames reveal_top 106-124 CPU s, fleet_wide_dm1 106, macro_dragon 114 (16 samples), macro_oar 126-128 (12 samples): about 27-32 s on 4 free cores.

## Look A (the original look of films 1-13), a runtime switch next to the R9 look B
Same set, cameras, hooks, cards and animation; ONLY the render setup changes. B (R9) stays the default and is pixel-identical (regression: roof_low mean abs diff 0.0).
- Select: `J.set_look('A')` right after `build()`, or env `JOSEON_LOOK=A` (build() reads it and applies it itself: teams' shot.py need no edit). `J.LOOK` is `'A'` or `'B'` (common.py branches on it).
  `set_look('B')` after A raises (build() again gives B). Constants: `J.KEY_A = (2.30, 1.65, 0.74)`, `J.SHADE_A = (0.20, 0.27, 0.54)`, `J.A_SAMPLES = 8`, `J.A_ELEV = 27` (sun elevation).
- Light: ONE sun, colour / strength so that a white diffuse surface facing it reads (2.30, 1.65, 0.74) linear (energy pi x 2.30), 0.45 deg softness, from the camera's left (`sun_for_camera`, elevation 27; `aim_sun` works as before).
- Shade: every `J_` set material is rebuilt as Diffuse(base) + Emission(base x SHADE_A x shade_mul) (textures and bump kept; plain diffuse flags / foam get the same emission; alpha stays a transparent mix; muzzle flash and droplets keep their glow;
  iron / gold / the sea get a sharp sun glint). The world lights nothing: the sky is visible to the camera only (Background strength x Is Camera Ray), so shadows are base x SHADE = blue-violet. Direct light only (diffuse bounces 0, glossy 1).
- No haze volume (the object is hidden), no DOF on any camera (macro_spikes / macro_dragon / macro_oar are sharp; `make_camera` ignores `fstop` in A), no motion blur, no bloom (glow only on real sources: the muzzle flash).
- Water: same geometry, swell, foam and wakes; opaque diffuse + shade emission + crisp warm cel band on the swell faces turned to the sun + a sharp GGX glint (film-10 sea style). Smoke: the same soft cluster puffs, no volume.
- Render: full 720x1280 (no 75 % upscale), 8 adaptive samples + OIDN, `Standard` view; `render_still` and `Take.render` skip `J.post()` in A (the v1.1 grade runs in conform: `grade_frame`). CLI: `JOSEON_LOOK=A python3 joseon.py final ...` writes `joseon_work/final_A/`; `./run_finals_A.sh`.
- Sheet: `python3 make_contact_A.py` grades the raw A finals with `grade_frame` (g = 300) into `joseon_work/final_A_graded/` and builds `contact_A.jpg` / `contact_A_small.jpg` (same 30 tiles and labels as contact.jpg).
- common.py (`v3/film24`): with `JOSEON_LOOK=A`, `C.LOOK_A`, `C.RES_PCT = 1.0`, `C.SAMPLES = J.A_SAMPLES` (`preset_samples` returns it for every preset), `Take` turns DOF off, and `Take.render` skips `J.post`. Frames keep the same names (`f_%04d.png` / `g_%04d.png`); put them in separate folders.
- Cost (2 threads, light load): **33-52 CPU s per frame, mean 39** (wall 17-26 s) = about 8-13 s on 4 free cores (mean ~10 s). Heaviest: macro_oar 51 (droplets, foam, glossy water), reveal_top 46. About 17 CPU s of it is fixed (scene sync, OIDN at 720x1280); each sample costs ~2.3 CPU s.
- Hue (graded, `joseon_hue.py`, `joseon_work/hue_rows_A.txt`): the frame-wide shade-hue metric reads 170-199 because it is dominated by the teal sea; shadows on wood, stone and sails are blue-violet (base x SHADE). Colour shares: yard red 9 %, orange 30 %, blue 43 %; sea orange 14 %, cyan 38 %, blue 42 %, saturation 0.49-0.58 (exteriors, daytime sea).
- Limits: A cannot be switched back to B inside a scene; the sea reads teal (not the violet sea of film 10); A samples are low, so the sun softness and OIDN carry the noise; `t_anim.py` now runs yard + sea in both looks (ALL OK, 188 checks).
