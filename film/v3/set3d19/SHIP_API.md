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
Presets: `ship_hero` (v6 exterior), `ship_aerial` (high, wide, wake + glitter), `ship_deck` (quarterdeck, wheel + binnacle FG, mizzen + sails above), `ship_rail` (camera at the starboard waist rail,
looking forward-outboard: sea, foam lines, bow wave, headland), `ship_rocks` (forecastle, black rocks + surf, fog, lantern lit; use light STORM_DUSK), `ship_coast` (anchored, Jamaica or Barbados dressing),
extra `ship_shore` (camera on the beach, shore_a / shore_b 5 m in front, ship across the bay).
Lights: `NOON` (hero default), `DAY` (tropical, coast), `STORM_DUSK` (grey-violet, dim low sun, lanterns lit, fog cards, foam x1.5, swell x1.7). Coast dressing: light `DAY_JAMAICA` / `DAY_BARBADOS`
(or `DAY` + `K.STATE['coast']='barbados'` before build). Any preset renders in any light.

## Marks (world D, ground z of the deck)
On the deck (children of ship_root): captain_wheel (behind the wheel, faces +y), william_rail (starboard waist rail), sailor_a, sailor_b, sailor_c, astro_deck (waist, port side), crew_bow (forecastle).
On the shore (world, only in ship_coast / ship_shore): shore_a, shore_b.

## Hooks (frame= keys LINEAR as K._keysock/_keyxf; without frame sets now; key every hook on every frame)
- `set_sea(t, frame=None)`: t seconds; geometry-nodes swells + chop and the foam-drift noise key on `sea_t`; the bow sheet rides the swell.
- `set_roll(t, frame=None)`: ship_root pitch/roll <= 1.9 deg + bob from the swell at the ship; call with the SAME t as set_sea.
- `set_sun_overhead(k, frame=None)`: sun elevation from the light's value (46 deg NOON) to 88 deg; mast shadow shrinks to its foot.
- `set_rain(on, frame=None)`: streak geometry parented to the scene camera (call after K.make_camera); per frame keys the fall.

## Cost / colour: see ship_cost.txt, ship_hue.txt. Test: `python3 ship_contact.py [draft] [--only preset[:LIGHT]] [--nohue]` -> ship_contact.jpg.
