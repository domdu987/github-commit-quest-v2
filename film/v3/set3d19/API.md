# v3/set3d19/h19.py : film 19 set ("ไอ้ช่างไม้", John Harrison, 1730s-1773)

Real 3D Blender set (bpy 5.x, Cycles CPU), grown from the client-approved style board (`styleboard/`, board.jpg, QA_ART.md): warm honey / crimson interiors, painterly two-tone noise materials, brass that reads as brass, one hard sun with real cast shadows, blue-violet ambient outdoors, only the board's sat 1.08 grade as post. **No depth of field anywhere. No text anywhere** (maps, charts, dials and clocks have lines, dots and tick marks only).

Files: `h19.py` (public API, dispatch), `h19_kit.py` (materials, builder, lights, keying, render, hue; shared with the ship), `h19_shop.py` (WORKSHOP), `h19_hall.py` (HALL), `h19_tex.py` (painted textures, cache `tex_h19/`, < 1.3 MB), `h19_ship*.py` (SHIP, written by builder B: `h19_ship.py` + hull / deck / sea / land / fx modules), `make_contact.py` (+ `contact.jpg`, `contact_small.jpg`, `hue_report.txt`, `cost_report.txt`, `h19_work/final/*.png` are not committed), `t_anim.py` (hook test, prints ALL OK), `draft.py` (one preview tile: `python3 draft.py shop_wide:DAY`).

## Use (one process builds one location)
```python
import h19 as H
A = H.build('shop_wide', light=None)        # resets the scene, builds the location of that preset, applies the light, returns the anchors
H.setup_render(scene, 'final')               # 720x1280 ('preview' 360x640), Cycles CPU, 10-16 spp + OIDN, no diffuse bounce, 2 threads (build() already did it)
cam = H.make_camera(A['cam'])                # 22 mm, sensor 36, DOF OFF, clip 0.05..2000
act = H.placeholder_actor('harrison', A['marks']['harrison_bench'], face_to=cam.location)   # roles: harrison william mocker astro king captain sailor visitor clerk boy (H.HEIGHT)
H.stage_placeholders()                       # the preset's own staging (A['staging'][cam_name]); H.head_pixels() -> [(role, mark, head y, head px, chin y, feet y, head x)]
H.project(world_pt)                          # pixel of a world point in the scene camera (720x1280, y from the top)
H.render(path) -> (wall s, cpu s);  H.clear_keys()   # drop every key the hooks made
```
`A = {'cams': {name: {loc, look_at, lens}}, 'cam': default cam, 'cam_name', 'cam_notes', 'marks': {name: (x, y, z_ground)}, 'staging': {cam: [(role, mark)]}, 'location', 'preset', 'light', 'ship_root': obj or None, 'floor_z', 'render', 'heights', 'lights'}`.
Hooks key when `frame=n` is given (LINEAR for numbers, CONSTANT for visibility); without `frame` they set the value now. **Key every hook on every rendered frame** (visibility keys hold their first value before the first key). `python3 t_anim.py` tests all of them.

## World
1 unit = 1 D = head width, **D = 1.85 x metres**, adults 3.0-3.4 D (`H.HEIGHT`). Z up, floor / deck at the mark's z. Each location is authored in metres under one scaled root empty (`K.ROOT`, scale 1.85), lights / cameras / marks are converted with `K.W`.
**WORKSHOP** (metres): room x -2.3..2.3, y -2.9 (front wall with the door, x -0.75..0.15) .. 3.4 (back wall with the 6x5 small-pane window x -1.55..-0.3), height 2.9; bench x 0.3..2.2, y 1.5..2.3, top 0.9 m; treadle lathe under the window shelf; longcase clock back-left; wall gears + saws behind the bench; cart-wheel candle chandelier, herbs, saws, stored planks overhead; braided rag rug, tool chest with open drawers, offcut basket, half-built clock case, stump + axe, sawhorse, shavings (about 240 thin honey ribbons).
**HALL**: room x -3.6..3.6, y -3.4 (double doors, lit corridor) .. 5.6 (arched window to Greenwich: haze hill, trees, observatory dome), height 6.0; patterned Georgian carpet (greyer navy #2c3558 field, crimson + gold border, medallions, corner motifs), Board table x -0.75..0.75, y 0.6..4.2 on green baize with orrery, charts, candelabra, six chairs (crimson / green upholstery), chandelier + gilt coffered ceiling, brass telescope on a tripod pointing at the window, painted Moon picture (oval gilt frame) left of the window, wall map + seascape right, bookcases (4), quadrant on a stand, orrery on a round table, globes, floor candelabra, wall sconces.
**SHIP**: see `h19_ship.py` (builder B): one object tree under `ship_root`.

## Presets (A['cams'][name]; start poses, 22 mm; every preset carries foreground dressing at the SIDES, the caption band y 880-950 stays calm)
WORKSHOP: `shop_wide` (sb1 framing, DAY) `shop_bench` (medium on the bench + hero clock, plane / shavings in FG) `shop_clock` (closer 3/4, default hook `set_clock([1, 4])`) `shop_door` (from the room toward the front door: mocker visiting).
HALL: `hall_wide` (crane from the front) `hall_table` (the Board table, King chair at the head) `hall_low` (low angle on the mocker's spot by the telescope) `hall_window` (telescope at the arched window with the Moon picture) `hall_door` (toward the double doors, the carpenter enters).
SHIP: `ship_hero ship_aerial ship_deck ship_rail ship_rocks ship_coast` (default lights NOON, NOON, NOON, NOON, STORM_DUSK, DAY).
Per-preset staging (placeholders): shop_wide harrison_lathe + william_bench; shop_bench / shop_clock harrison_bench; shop_door mocker + astro at visitor_a / visitor_b; hall_wide mocker_table + astro_a..e + harrison_table; hall_table harrison_table, astro_b, astro_d, king_stand; hall_low / hall_window mocker_telescope; hall_door harrison_door.

## Lights (`H.build(preset, light=)`, `H.apply_light(name)`)
WORKSHOP: **DAY** (warm late sun az -46 el 19 through the window, a soft shaft volume, blue-violet fills, warm practicals: candle, lamp, lantern, hanging lamp, wheel chandelier) and **NIGHT** (candles and lamps only, blue-violet moon key through the window, cool fill, warm pools; the pane shows stars + a moon; door daylight goes dark).
HALL: **DAY** (sun az -22 el 38 through the arched window, shaft, candles subtle) and **EVENING** (candles, chandelier lit, dusk-blue window, the King's timing sessions).
SHIP: **NOON** (sun high, `set_sun_overhead(k)` raises it to the zenith), **DAY** (coast), **STORM_DUSK** (grey-violet, rain optional, foam heavy).

## Hooks
WORKSHOP: `set_clock(n, frame)` n = 0 none | 1 H1 big brass (frame, exposed gears, two crossed dumbbell bars with four balls) | 2 H2 (taller, similar) | 3 H3 (compact brass box with two big round balances) | 4 H4 (silver watch about 13 cm across on a red cloth, open face, tick marks + two hands, NO numerals); a list shows several: `set_clock([1, 4])` = H1 + H4 side by side (the "shrink" reveal). `set_balance(t, frame)` t in seconds: crossed bars of H1 / H2 rock +-24 deg (1.3 s period), H3 balances counter-rotate +-70 deg, every gear turns at its own rate. `set_candles(level, frame)` flame flicker (call per frame), level 0..1 burns the bench candle stub down (0 hides the flame and its light). `set_door(deg)` is a stub (the door stands ajar).
HALL: `set_moneybag(state, frame)` 'none' | 'full' | 'half' (slumped, coins spilled). `set_box(state, frame)` 'none' | 'open' (lid up, red velvet) | 'closed' | 'sealed' (three red wax seals + ribbons). `set_candles(level, frame)` flicker. `set_stubs(n, frame)` 0-10 burnt stubs in brass dishes along the near edge of the table (ten-weeks time-lapse). `set_kings_chair(on, frame)` gilt armchair with crimson velvet at the table head (default on in hall_table / hall_wide). `set_regulator(on, frame)` tall regulator clock (open dial, tick marks, brass pendulum) against the right wall.
SHIP (h19_ship): `set_sea(t, frame)`, `set_roll(t, frame)` (gentle roll / pitch <= 2 deg and bob on `ship_root`), `set_sun_overhead(k, frame)`, `set_rain(on, frame)`. `H.set_*` dispatch lazily (`import h19_ship` inside); a hook of another location raises AssertionError.

## Stand points (A['marks'][name] = (x, y, ground z in D))
WORKSHOP: `harrison_bench` (behind the bench, facing the camera), `harrison_lathe`, `harrison_window`, `door` (in the doorway), `visitor_a`, `visitor_b`, `william_bench`.
HALL: `mocker_telescope`, `mocker_table`, `astro_a..astro_e`, `harrison_door`, `harrison_table`, `king_chair`, `king_stand`.
SHIP (children of `ship_root`): `captain_wheel`, `william_rail`, `sailor_a..c`, `astro_deck`, `crew_bow`; shore: `shore_a`, `shore_b`.

## Render cost
See `cost_report.txt` (CPU s of the final render call, 720x1280, two workers, 2 threads each; limit 40). Settings: no light tree, max bounces 2, no diffuse bounce (all fills are shadow-casting area lights), glossy 1, 10 spp for the workshop / hall, OIDN fast; build about 4 s per process.

## Colour (hue_report.txt, method of styleboard/hue_check.py: cast-shadow pixels from a sun-only render)
Indoor tiles (workshop, hall): the shade is warm by design (approved indoor exception, like film 16's chamber); magenta share is reported per tile and stays under 10 %. Outdoor tiles (ship): shade hue target 225-265.

## Hand props (how render workers do them)
The set only provides WORLD props. Everything a character holds is drawn by cast19 in the cards: the H4 watch in a hand, the quadrant, a pocket watch, a quill, the King's pocket watch, a lantern. World props on the set: the four clocks (set_clock), the money bag, the sealed box, the candle stubs, the King's chair, the regulator, the quadrant on its stand, the telescope, orrery, globes, charts and quill + ink on the table, the bench plane / mallet / chisels / saw.

## Fix round (WORKSHOP + HALL, after the SET gate)
- **Caption band**: `STATE['caption_shade']` (set by build_shop / build_hall, NOT by the ship) makes `make_camera` attach `caption_shade`, a camera-only card that blends the frame toward warm dark brown from row ~740-770 (0 %) to row ~890-900 (50-68 %) and the bottom edge (62-80 %). It affects no light. Band y 880-950 now averages 0.01-0.06 linear luminance (see below); ship tiles are unchanged (opt-in).
- **WORKSHOP**: dusty ochre-grey plaster + walnut bench (#6b4a2e) + violet fill (orange share of saturated pixels 92-96 % -> 64-77 %); DAY sun 36 W warm-grey; NIGHT = moon key + candle pools only (fill 0.08). H4 watch: hero scale 2.3 (about 30 cm), tilted 43 deg to the lens on a ledger, slot in front of the bench, about 200 px wide in shop_clock; `set_clock([1,4])` puts H1 at x 0.5, H4 at x 1.12. `harrison_bench` mark is now x 1.8 m. H3: brass #cb9f48, two upright polished rings. Warm iron (no blue bars); brass rims never black. Rag rug = muted stripes; gear moved to the bench; offcut planks lie flat on a contact strip; plane + shavings on the sawhorse plank (shop_bench bottom-left). Chest + lantern moved right (x 2.0 m). Front-wall window, coat pegs with coat / apron / hat, upright saws. **Outside the door is real geometry** (`build_exterior`): path, rail fence with an open gate, hedge, bushes, trees in three depth layers, far hill, gradient sky, a cart; self-lit, switched by `apply_light` (night colours + moon).
- **HALL**: muted carpet (gold #a8894a, crimson #7a2a2a, one small soft oval medallion); King's chair is a gilt armchair with crimson velvet seat, back panel and arm pads, facing the camera; panelled door leaves (one slab, 3 raised panels per face, gilt moulding, brass knob, 3.1 m under the 3.2 m lintel); real corridor (2.6 x 2.2 m, runner, two sconce pairs, portrait, console, own warm lights `corr`); Georgian fanlight (radial bars, no X); small yellowed curled charts; EVENING exposure -0.45, fill 0.04, candles 1.05, chandelier 0.75 (mean linear luminance about 55 % of DAY, warmer).
- **Cameras / marks** (heads 450-760 for every WORKSHOP and HALL preset, see `heads.txt`): hall_wide (0,-3.2,3.6)->(0,3.5,1.15); hall_table look z 1.4 (tilted up); hall_low (-1.9,-1.2,0.7)->(-1.7,2.0,1.35); hall_window (-0.6,-1.6,1.1)->(-1.3,5.6,2.2); shop_clock (1.15,0.45,1.3)->(1.25,1.9,1.1). Marks (m): mocker_table (-1.75,1.35), astro_a (-1.9,2.2), astro_b (-1.9,3.2), astro_c (1.9,1.8), astro_d (1.9,2.9), astro_e (1.7,3.9), harrison_table (0.35,0.9).
