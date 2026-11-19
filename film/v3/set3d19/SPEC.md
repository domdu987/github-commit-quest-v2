# set3d19 build spec: film 19 "ไอ้ช่างไม้" (John Harrison, 1730s-1773)

The look is approved by QA-art: `styleboard/board.jpg`, with the must-fix lists in `styleboard/QA_ART.md`. Grow the full set FROM the style board code (`styleboard/part_*.py`). Do not redesign it.

## Shape of the code (mirror film 16's set3d16, `API.md` there)
- `h19.py` is the single public API. Render workers do `import h19 as H`:
  - `A = H.build(preset, light=None)` resets the scene, builds the location of that preset, applies the light and returns:
    ```
    A = {'cams': {name: {loc, look_at, lens}},
         'cam': default_cam,
         'marks': {name: (x, y, z_ground)},
         'location': ...,
         'ship_root': obj or None}
    ```
  - `H.setup_render(scene, 'final'|'preview')`: 720x1280 or 360x640, Cycles CPU, low spp + OIDN, 2 threads.
  - `H.make_camera(A['cam'])`: 22 mm lens, 36 mm sensor, DOF OFF.
  - `H.placeholder_actor(role, mark, face_to)`, `H.project(pt)`, `H.head_pixels(cam)`, `H.render(path)`, `H.clear_keys()`.
  - Hooks key on `frame=` when given, as in film 16.
- Location modules: `h19_shop.py` (WORKSHOP), `h19_ship.py` (SHIP), `h19_hall.py` (HALL), each with a `build_<loc>(SET, preset, light)`. Shared materials and kit go in `h19_kit.py`, copied from `styleboard/machinery.py` and `part_common.py`.
- Units: 1 unit = 1 D = head width. **D = 1.85 x metres**, as film 16. Z up, floor or deck at the mark's z.
- **No DOF, no readable text anywhere**, magenta ≤ 10 %. Outdoors shade hue 225-265; indoors shade is warm by design (approved).
- **Each preset camera** is a start pose with foreground dressing 1-2 D from the lens at the frame SIDES, with the caption band y 880-950 kept calm. Characters stand at marks with heads at y 450-760 for a medium shot.
- **Render cost:** final ≤ 40 CPU-s per frame per preset on 2 threads. Report it in `cost_report.txt`.
- **Deliverables:**
  - `API.md` (the same sections as set3d16's: Use, World, Presets, Lights, Hooks, Stand points, Render cost, Colour, Hand props)
  - `t_anim.py`, a hook test that prints ALL OK
  - `make_contact.py` producing `contact.jpg`: one final 720x1280 tile per preset x light with placeholder actors at marks, a cyan line at y 880, and labels under the tiles
  - `hue_report.txt`, `cost_report.txt`
  - `.gitignore` for the work folders. Keep committed binaries small: textures ≤ 5 MB total, no renders except the contact sheets.

## WORKSHOP (h19_shop.py): Harrison's village workshop, Lincolnshire
QA-art must-fix: the H1 frame and gears in brass; no black gear slivers; no blue objects; a dense lower frame (tool chest, offcut basket, half-built clock case, small honey shavings); a better stump.

Presets:
- `shop_wide`: the sb1 framing, the room with the bench and window.
- `shop_bench`: medium on the bench and the hero clock, low-ish, plane and shavings in FG.
- `shop_clock`: a closer 3/4 on the clock, Harrison's mark behind the bench.
- `shop_door`: from the bench toward the door, for the mocker visiting.

Lights:
- DAY: approved, warm late sun through the window.
- NIGHT: candles and lamp only, blue-violet moon fill through the window, warm pools.

Hooks:
- `set_clock(n, frame)`: n=1 shows the H1 big brass (dumbbell bars), 2 the H2 (taller, similar), 3 the H3 (compact brass box with two big round balances), 4 the H4 (a silver watch about 13 cm across, on a red cloth on the bench, open face, NO numerals, just tick marks and hands), 0 none. Several may stand together: `set_clock([1,4])` shows the H1 and the H4 side by side for the "shrink" reveal image.
- `set_balance(t, frame)`: the H1 bars and balance rock, the gears turn.
- `set_candles(level, frame)`: flicker; a NIGHT candle stub height 0..1 burns down.

Marks: `harrison_bench` (behind the bench, facing camera), `harrison_lathe`, `harrison_window`, `door`, `visitor_a`, `visitor_b`, `william_bench`.

## SHIP (h19_ship.py): a 1760s 50-gun warship at sea (HMS Deptford type)
Grow it from `part_ship6.py` (the v6 exterior hero) and `part_ship.py` (deck, bow view).

QA-art must-fix:
- the bow wave a third of its height, a curling white roll with lacy foam, turquoise only in a thin band under the lip;
- lacy hull-side foam lines and a readable V-wake;
- the near sea deep teal with a gradient and calm reflections;
- a rounded, hazy headland;
- sails warm #e8dcc0;
- the bulwark cap rail;
- no sphere-chain foam, ghost blob or old faceted clouds anywhere.

The ship is ONE object tree under `ship_root`. All deck marks are children of it. `set_roll(t, frame)` gives a gentle roll and pitch (≤ 2°) and bob. Cards parented to `ship_root` move with the deck (film-10 lesson).

Presets:
- `ship_hero`: the v6 exterior view.
- `ship_aerial`: a high wide drifting view, the lone ship on the endless glittering sea.
- `ship_deck`: on the quarterdeck, wheel and binnacle in FG, the mast and sails above. Characters at the rail.
- `ship_rail`: at the waist rail, looking outboard and forward, the sea, the bow wave and foam visible (the v5 idea, fixed).
- `ship_rocks`: a stormy dusk, black rocks near the bow, fog, lantern lit.
- `ship_coast`: the anchored ship near a tropical palm coast and harbour (Jamaica, and Barbados with the same set dressed with a different fort/hill).

Lights:
- NOON: approved. The sun is high, so a mast's shadow falls short on the deck for the "sun overhead" beat. `set_sun_overhead(k)` raises the sun toward the zenith.
- DAY (coast).
- STORM_DUSK: grey-violet, rain optional, foam heavy.

Hooks: `set_sea(t, frame)` animates the swells, foam drift and wake by time; `set_roll`; `set_sun_overhead(k)`; `set_rain(on, frame)` for the rocks.

Marks:
- On the deck (children of `ship_root`): `captain_wheel`, `william_rail`, `sailor_a`, `sailor_b`, `sailor_c`, `astro_deck` (Barbados astronomer with a quadrant), `crew_bow`.
- On the shore: `shore_a`, `shore_b`.

## HALL (h19_hall.py): the astronomers' hall (Board of Longitude); also the ending room
QA-art must-fix:
- the carpet and seats greyer navy #2c3558, with crimson or green seat upholstery;
- a patterned carpet border, the floor at most 25 % of the frame;
- a soft grey painted Moon on a dark ground;
- the left side filled: a bookcase, a quadrant on a stand, warm practicals.

Presets:
- `hall_wide`: high crane, the room with the Board table and chairs.
- `hall_table`: the Board table on green baize with an orrery, charts, candles.
- `hall_low`: a low angle on the mocker's spot by the telescope.
- `hall_window`: the telescope at the arched window with the Moon picture.
- `hall_door`: the doorway the carpenter enters through.

Lights:
- DAY (approved).
- EVENING: candles, chandelier lit, dusk blue window. This is the King's timing sessions.

Hooks:
- `set_moneybag(state, frame)`: none / full / half.
- `set_box(state, frame)`: none / open / closed / sealed, a wooden box with three red wax seals.
- `set_candles(level, frame)`: flicker.
- `set_stubs(n, frame)`: 0-10 burnt candle stubs in a row on the table, the ten-weeks time-lapse.
- `set_kings_chair(on, frame)`: a gilt armchair with crimson velvet at the table.
- `set_regulator(on)`: a tall regulator clock against the wall that the King compares with.

Marks: `mocker_telescope`, `mocker_table`, `astro_a`, `astro_b`, `astro_c`, `astro_d`, `astro_e`, `harrison_door`, `harrison_table`, `king_chair`, `king_stand`.

## Hand props
Drawn by the cast cards (cast19), NOT the set: the H4 watch in a hand, the quadrant, a pocket watch, a quill, the King's pocket watch, a lantern.
