# SHIP section for API.md (builder B: h19_ship.py + h19_ship_{hull,deck,sea,fx,land}.py)

## Use
```python
import h19_ship as SH
A = SH.build_ship(SET, 'ship_rail', 'NOON')   # SET unused (may be None). Returns dict(cams, cam, marks, ship_root, location='ship')
```
`build_ship` does NOT reset the scene or clear `K.MATS` (h19.build does). It creates `K.new_root('ship_world')` (scale 1.85, metres authoring) and sets `K.ROOT` to it,
sets `K.STATE['samples']=12`, `K.STATE['dbounce']=0`, `K.STATE['grade_sat']`, `K.STATE['coast']` is read (`'jamaica'|'barbados'`). Camera far clip must be >= 2000 (K.make_camera does it).
Preset cameras are in world D; A['cams'] holds only the preset camera (the sea grid is fitted to it).

## World
Ship at the origin heading +y (bow y=+21 m waterline), starboard +x, z up, waterline z=0; D = 1.85 x metres. `ship_root` (unscaled empty at the origin) carries the roll: every deck mark is an
empty `mark_<name>` child of it, so cards parented to `ship_root` (keep world transform: `ob.parent=root; ob.matrix_parent_inverse=root.matrix_world.inverted()`) ride the deck.
Deck levels: waist z 5.25 m, quarterdeck 7.75 m (y < -12.6), forecastle 6.45 m (y > 13.6). Hull 42 m waterline, 3 masts.

## Presets / lights
Presets: `ship_hero` (v6 exterior; curling bow roll, V-wake, a floating spar and a swell-crest foam line near the lens), `ship_aerial` (high, wide, wake; one narrow glitter path, no random whitecaps),
`ship_deck` (quarterdeck, camera at the stern looking forward: wheel + binnacle at the left frame side, thin mizzen on the right, sails above, y 450-1000 clear for captain / William / astronomer; sun el 60 from astern so the
mast and sail shadows fall on the deck; `set_sun_overhead(1.0)` shrinks the mast shadow to its foot), `ship_rail` (camera over the starboard waist rail, 14 deg outboard, pitched down 12 deg: deck strip, cap rail, hull foam bands, bow wave flank, one glitter path),
`ship_rocks` (forecastle, rounded black basalt + surf foam, slate storm-cloud deck, two fog layers, a 2200 K lantern 0.9 m = 1.6 D from the lens, captain at the left; use light STORM_DUSK),
`ship_coast` (a BEACH: camera on the dry sand, longboat hauled up on the left, driftwood, palm fronds in from the top right, anchored ship across the bay, hills behind; three standing marks shore_a / shore_b / shore_c 4-7 m in front).
`ship_shore` is kept in `PRESETS` of h19_ship.py only (not in h19.PRESETS); it is the old beach camera, superseded by ship_coast.
Lights: `NOON` (hero default), `DAY` (tropical, coast), `STORM_DUSK` (slate blue-grey, dim low sun, lanterns lit, fog cards, foam x1.5, swell x1.7). Coast dressing: light `DAY_JAMAICA` / `DAY_BARBADOS`
(or `DAY` + `K.STATE['coast']='barbados'` before build). Any preset renders in any light. The deck / rail / rocks presets use the "warm" theme (HU.THEME): mast #3a2e26, cap rail #5a4632, canvas #e8dcc0,
wood-and-brass wheel, warm iron, dark-oak gun carriages (no magenta). The ship is exactly level at t = 0 (set_roll is relative to t = 0), so the marks and cameras below are exact in the first frame.

## Marks (world D, ground z of the deck)
On the deck (children of ship_root): captain_wheel (beside the wheel, quarterdeck), william_deck, astro_quarter (quarterdeck, in frame of ship_deck), william_rail (starboard waist rail, in frame of ship_rail), sailor_rail,
sailor_a, sailor_b, sailor_c, astro_deck (waist, port side), crew_bow, captain_bow (forecastle, in frame of ship_rocks).
On the shore (world, only in ship_coast): shore_a (William), shore_b (sailor), shore_c (astronomer).
Staging (placeholders, `h19.stage_placeholders()` after `H.make_camera`; `A['staging'][preset]`): deck = captain_wheel / william_deck / astro_quarter, rail = william_rail / sailor_rail,
rocks = captain_bow / crew_bow, coast = shore_a / shore_b / shore_c. Head y at 720x1280 per preset is listed in `ship_heads.txt`.

## Hooks (frame= keys LINEAR as K._keysock/_keyxf; without frame sets now; key every hook on every frame)
- `set_sea(t, frame=None)`: t seconds; geometry-nodes swells + chop and the foam-drift noise key on `sea_t`; the bow sheet rides the swell.
- `set_roll(t, frame=None)`: ship_root pitch/roll <= 1.9 deg + bob from the swell at the ship; call with the SAME t as set_sea.
- `set_sun_overhead(k, frame=None)`: sun elevation from the light's value (46 deg NOON) to 88 deg; mast shadow shrinks to its foot.
- `set_rain(on, frame=None)`: streak geometry parented to the scene camera (call after K.make_camera); per frame keys the fall.

## Cost / colour / single source
`ship_contact.py` and `make_contact.py` share ONE pipeline: `ship_contact.render_tile()` = `h19.build` -> `make_camera` -> hooks -> `stage_placeholders` -> `render` -> `measure_hue` (make_contact.do_tile calls it for every S* tile with the S-tile hooks).
Outputs: `ship_contact.jpg`, `ship_cost.txt` (CPU s of the render call, 2 threads; limit 40, ship_deck 38), `ship_hue.txt`, `ship_heads.txt`. Test: `python3 ship_contact.py [draft] [--only preset[:LIGHT]] [--nohue] [--sheet]`.
Hue method: `K.measure_hue` (sun-only render, white override, real cast shadows). The sun object is named `ssun_key` (the kit hides names starting with `sun_` in the mask pass, which is why every tile used to report "None").
Tiles with lanterns are measured with the lamps and the glowing lantern meshes off (6 spp re-render), so the number is the sun / sky shade hue; the lantern pools are warm by design.
Sky objects (storm deck, fog cards) are invisible to diffuse rays, so the blue world ambient still lights the shade.
