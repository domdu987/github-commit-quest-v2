# v3/set3d6/bakery.py : film 6 set ("the 13th loaf"), a medieval English market town in the 1260s: Henry's bakery and the market square (bpy 5.3, Cycles CPU)

Files:
- `bakery.py`: both locations.
- `bakery_tex.py`: all artwork, drawn as SVG in Python and rasterised by `v3/set3d/raster.js` into `tex_bakery/`, cached by content hash.
- `bakery_hue.py`: hue rows through `v3/tools/hue_report.py`.
- `contact.jpg`: every camera x light preset at 720x1280, 12 samples, with placeholder actors, plus 5 reference frames in the last row.

Work files are in `bakery_work/`:
- `final/<loc>_<PRESET>_<cam>.png`: the finals.
- `stills/`: 360x640 previews.
- `final_log.txt`: CPU time and head pixels per frame.
- `hue_rows.txt`
- `t_anim.py`: a test of the keyed hooks.
- `t_cost*.py`: cost profiles.
- `actors/`: placeholder sprites.

The module is built on `v3/set3d5/mine.py`, which in turn is built on `pagoda.py` v2 and `tower.py`. Helpers are imported, not copied:
- from `tower`: `mat_lit`, `mat_emit`, `MB`, the ink hull, `setup_grade`, `make_camera`, `render`, `no_bounce`, the keying helpers, `placeholder_actor`.
- from `pagoda`: `_kd`, `_pivot`, `_parent`, `_haze_mat`, `digest`.
- from `mine`: `obox`, `beam`, `rod`, `lumpy`, `catenary`, `chain_rod`, `_light`, `_obj`, `_untoon`, `_glossy`, `_denoise`, `setup_render`.

`bakery.STATE` is `tower.STATE`. The module shape is the same as `mine.py`: `build` returns an anchors dict, the `set_*` hooks are keyed with `frame`, and there is a CLI for stills, finals and digest.

**No depth of field anywhere** (client rule: images must be sharp). The set never sets up DOF. `apply_dof()` is a no-op. `setup_dof` is re-exported only so that shot scripts can keep calling `B.setup_dof(scene, None, None, cam=cam)` as in film 5.

World: 1 unit = 1 D (head diameter), Z up, floor / ground z = 0. One location is built at a time (`build` clears the scene).

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d6"); import bakery as B
A = B.build('bakery', 'MORNING')        # bakery: 'MORNING' | 'AFTERNOON'   build(location, preset=None, clear=True, dress=True) -> anchors (section 2)
A = B.build('market', 'AFTERNOON')      # market: 'AFTERNOON' | 'MORNING'
B.setup_render(scene, 'final' | 'preview')   # = mine.setup_render: 720x1280 12 samples / 360x640 6, 2 threads, direct light only,
                                             #   OpenImageDenoise (albedo+normal, FAST prefilter), light tree off. Call it after build if you change quality.
cam = B.make_camera(A['cams']['counter'])    # tower.make_camera (uses the 'lens' of the preset)
B.placeholder_actor(role, mark, face_to=None)  # roles kit 2.4 D, henry 3.1, inspector 3.4, guard 3.2, woman 2.9, man 3.0 (stand-ins only)
B.stage_placeholders(A, cam_name, cam_loc)     # the contract-still staging (B.STAGING[cam_name])
B.head_pixels(cam_name) -> [(role, mark, head_centre_y_px, head_px, feet_y_px)]   # caption check at 720x1280 for the staged roles
B.apply_cam_state(cam_name, preset)          # contract-still state (section 4)
B.render(path) -> (wall s, cpu s);  B.digest() -> sha1 (determinism)
```

### Animatable hooks (all keyable with `frame=N`; key the start state too)

| hook | signature | what |
|---|---|---|
| steam | `set_steam(level, frame=None)` | White steam wisps rising off the hot loaves: 9 table sources (cooling boards), the basket on the inside counter, and two spots on the outside shutter board. `level` runs 0 (hidden) .. 1 (full) .. 1.5 (thick). The wisps scroll upward with the frame number: the scroll offset is keyed **linear**, so sparse keys still rise smoothly. Strength is keyed linear. Bakery only (no-op in the market). `build` leaves 0.8. |
| oven fire | `set_oven(k=1.0, frame=None)` (alias `set_fire`) | 0 = out, 1 = roaring, 1.5 = flaring. Deterministic flicker from the frame number: the light energies of `L_oven_fire` and `L_oven_fill` (in the market, the two braziers), the fire and ember emission (the bakery-front fires too), and the mouth halo. **Call it every frame**; keys are linear. |
| small balance | `set_scale(angle_deg, frame=None)` | The hand balance on the bakery counter. **+ = the loaf pan (left, -x) goes down**; - = the weights pan goes down. Useful range ±8. The pans hang level from the beam ends. Keys are Bezier. |
| loaf on the small balance | `set_scale_loaf(visible, frame=None)` or `set_loaves(n, frame, which='small')` | Shows or hides the loaf on the left pan. Visibility is keyed constant. |
| big balance | `set_big_scale(angle_deg, frame=None)` | The public balance in the market. **+ = the bread pan (x 3) goes down = the bread passes**; - = the weights pan (x 9) goes down = the bread is short. Story: hold -7 ("does not move"), then ease to +6 over about 1.5 s once the 13th loaf is on. Keys are Bezier. |
| loaf pile | `set_loaves(count, frame=None)` | Loaves on the big bread pan, 0..13. The first `count` loaves are shown: 7 round the rim, 4 inside, the 12th on top. **13 adds the paler 13th loaf on the very top.** The loaves are children of the pan pivot, so they move with the tilt. Visibility is keyed constant. |

`build()` leaves: steam 0.8 (bakery), oven 1, small balance 0 with its loaf shown, big balance 0, 12 loaves. All actions are cleared on build.

Checked by `bakery_work/t_anim.py`:
- steam, small balance and oven keyed over 60 frames; the values between keys are correct.
- big balance -7 → +6 and loaves 12 → 13 at frame 40: correct.

Digests are identical in two processes:
- bakery MORNING: `b131fbb1...`
- market AFTERNOON: `379dd71b...`

## 2. Anchors (world D)

### Bakery (`build('bakery', ...)`)

**Room**
- x -7..7, y 0..11. The front wall is y -0.5..0 and the street is at -y. The ceiling is at z 7, with beams at y 1.6 / 4.0 / 6.4 / 8.8.

**Openings in the front wall**
- Counter opening: x -1.5..3.5, z 1.25..4.1.
- Half door: x -4.6..-2.8, z 0..4.3. The lower leaf is shut up to z 2.0.
- Leaded window: x 4.7..6.3, z 2.5..4.3.

**Counter**
- `counter`: inside counter x -1.7..3.7, y 0..1.3, top z 1.25.
- The let-down shutter board outside is at y -1.55..-0.5, at the same height, heaped with loaves and baskets.
- Above the opening, inside: a shelf of crocks and baskets (z 4.6) and ladles.
- Above the opening, outside: the painted fascia "HENRY · BAKER" (z 4.4..5.3) and the hanging bread sign (x 2.25).

**Oven**
- `oven`: dome centre (-2.5, 9.0), R 2.7, plinth top z 1.4.
- The front face is at y ≈ 6.5, with the arched mouth (fire and ember bed) centred at (-2.5, 6.52, 2.1). A sooty brick hood rises to the ceiling.

**Table**
- `table`: x 3.75..5.45, y 3.0..9.6, top z 1.3.
- `table.loaves` lists the cooling-loaf positions.

**Small balance**
- `small_scale`: foot (2.4, 0.75, 1.25), pivot z 2.2, arm 0.5. The pans hang 0.62 below the beam ends: loaf pan at -x, weights at +x.

**`marks`** (floor z 0)

| key | position | where |
|---|---|---|
| `henry_counter` | (2.0, 2.0) | behind the counter |
| `kit_counter` | (-0.2, 1.85) | |
| `kit_table` | (3.0, 5.4) | |
| `henry_oven` | (-1.4, 4.6) | |
| `kit_sacks` | (-4.6, 3.6) | |
| `customer_street` | (0.4, -2.6) | the hooded man at the shutter board |
| `passers_street` | (-2.5, -6), (3.5, -7.5), (6, -5) | |

**Lights and keep-out**
- `lights`: oven `L_oven_fire` / `L_oven_fill`, `L_candle_*`; also `L_candle_wheel`.
- `keep_out` is listed in the anchors dict (the oven, table, racks, sacks, trough, counter and candle wheel).

### Market (`build('market', ...)`)

**Square and houses**
- The square is x -22..22, y -16..24.
- Rows of jettied houses face in on all four sides. There is a 2.5 D gap in the south row at x -0.7..-3.2.

**Henry's bakery front**
- `henry_front`: in the west row (front at x -22, facing +x), door outside at (-21.0, 3.5) (`A['henry_front']['door']`).
- It has a glowing shop opening with loaves on the shutter board, an open door with oven glow and fire, and the bread sign.
- The pilloried neighbour's bakery front is in the east row (pretzel sign).

**Pillory**
- `pillory`: platform 4 x 4 at (-4, 9.5), top z 1.0, steps down to (-4, 6.2).
- Board at z 2.73..3.35. Neck hole (-4, 9.62, 3.05), r 0.21. Hand holes at x -4.95 / -3.05.
- `stand` (-4, 9.95, 1.0): put baker2's pilloried card here, head through the neck hole.

**Big balance**
- `big_scale`: base (6, 6), pivot (6, 6, 6.6), arm 3.0.
- Pan tops at rest: bread (3, 6, 1.85), weights (9, 6, 1.85), pan radius 1.05. The pan tops move by ∓3 sin(angle) with the tilt.
- The bread pan is low enough for the 2.4 D boy to reach.

**`marks`** (ground z 0)

| key | position |
|---|---|
| `inspector` | (4.0, 3.9) |
| `henry` | (1.3, 3.6) |
| `kit_scale` | (2.6, 4.4) |
| `guard1`, `guard2` | (-5.8, 6.0), (-2.2, 6.2) |
| `baker2_in_pillory` | = pillory stand |
| `crowd` | 9 spots |
| `run_lane` | 5 points from (-19.5, 4.6) to (1.5, 5.0) |
| `lane_crowd` | 7 spots flanking the lane |

**Keep-out**: the houses, stalls, platform, balance base and pans, the well (-12, -3), hay (-17.5, 9), the cart (14, 17).

## 3. Camera presets (`A['cams']`), staging, and the caption-safe zone

The rule from earlier films still applies: keep heads above y ≈ 900 px of 1280, leaving the band below for captions. Every staged head below sits above that line.

Cards: puppet card height in D = the role height. There is no extra scale; all film-6 cast scale is 1.0 at these heights.

### Bakery cameras

| cam | loc → look_at, lens | shows | staged cards (feet on z 0) | head centre y px / head px |
|---|---|---|---|---|
| `bakery_wide` | (5.9, 0.7, 3.5) → (-2.2, 9.6, 2.1), 22 mm | Inside, from the front-right corner toward the roaring oven mouth: candle wheel, beams with herbs, onions and wheat, racks, the table with steaming loaves, sun patches on the floor | kit (-0.6, 5.4), henry (2.3, 3.4) | 707 / 96, 707 / 171 |
| `counter` | (0.55, -3.9, 2.5) → (1.2, 4.0, 3.1), 22 mm | From the street over the shutter board of loaves into the shop. Fascia sign top, bundles hanging in the opening, the oven glow and brick behind the actors, the hand balance at right | kit (-0.2, 1.85), henry (2.0, 2.0) | 783 / 141, 686 / 131 |
| `table_insert` | (3.1, 2.1, 2.55) → (4.55, 4.0, 1.55), 26 mm | ECU of the cooling loaves and steam on the floury table, racks behind | none | |
| `small_scale_insert` | (1.55, 2.15, 2.0) → (2.4, 0.75, 1.75), 26 mm | ECU of the brass hand balance (loaf pan / weights), with the sunny half-timbered street through the opening | none (a hand can enter from frame left) | |
| `window_out` | (0.6, 6.8, 2.7) → (1.0, -6.0, 3.2), 22 mm | From deep in the shop out through the counter opening to the street. Crocks shelf and ladles above, hanging bundles | kit (0.2, 2.6); passers man (-2.5, -6), woman (3.5, -7.5) | 821 / 190, 683 / 62, 687 / 55 |

### Market cameras

| cam | loc → look_at, lens | shows | staged cards | head centre y px / head px |
|---|---|---|---|---|
| `market_wide` | (11, -14.5, 15.5) → (-3, 9, 1), 22 mm | High establishing shot: the whole square, pillory, balance, stalls, bunting, houses, backdrop town and castle | inspector (4, 3.9), henry (1.3, 3.6), kit (-3, 4.6), guard (-5.8, 6), crowd | ≈ 610..790 / 25..30 |
| `square_eye` | (1.2, -4.5, 2.6) → (0.6, 12, 4.0), 22 mm | Eye level looking north: balance right, pillory left, bunting overhead | inspector, henry, kit (2.6, 2.4), guard, woman (-1.5, 2), man (-3.5, 3) | 678..788 / 73..120 |
| `pillory_low` | (-1.2, 4.9, 0.9) → (-4.0, 9.5, 3.4), 22 mm | Low, up at the pillory board and its three holes, against the north row and the sky | guard (-7.4, 11.8), man (-1.0, 8.2) (cropped at frame right) | 831 / 88, 563 / 217 |
| `big_scale_insert` | (2.3, 1.3, 2.5) → (3.0, 6.0, 3.7), 24 mm | The bread pan with the loaf pile low centre, chains up to the beam end and pivot, the royal banner | none (the boy / inspector can stand at about (2.0, 4.6)) | |
| `run_lane` | (3.4, 4.3, 1.3) → (-21, 4.6, 2.8), 22 mm | Low at the balance, looking west down the lane to Henry's glowing bakery front; the boy runs at camera along `run_lane` | kit (-6.5, 4.6), crowd at (-11, 2.9), (-10, 6.4), (-6, 2.8), (-5.5, 6.5), henry (-1, 3) | 459..641 / 54..173 |

Keep cameras out of the keep-out zones in section 2. The market cameras are all inside the square.

## 4. Light presets

The light model is the same family as the templates: one hard sun with real shadows, painted shade emission, no bounce, emission_sampling NONE, and the grade compositor with bloom.

**Bakery** (`MORNING` / `AFTERNOON`):
- Every material is `_untoon`ed (plain Lambert), so the sun through the three openings and the point lights both work.
- The sun:
  - MORNING (1.36, 1.10, 0.72), 30°, from the street (front-left).
  - AFTERNOON (1.52, 0.95, 0.42), 22°, from the front-right.
- Real point lights:
  - the oven fire (1100 W, shadowed) and a fill (280 W);
  - the candle wheel (150 W);
  - 5 candles (45 W: the table ends, the counter, two sconces).
- Painted shade (0.07, 0.075, 0.21), deep blue, mix 0.6.
- Warm emitters: the oven mouth fire cards and ember bed, a mouth halo, a floor light pool, candle flames with halos, and the bakery-front fire.
- Sun shafts: two crossed camera-only additive sheets per opening, `shaft_k` 0.3, with dust motes.
- The street outside has a painted backdrop, sky and haze. The opposite house row casts no shadow, so the bakery front stays sunlit.

**Market**:
- `AFTERNOON`: warm sun (1.70, 1.06, 0.46) from the west-south-west at 26°, shade (0.085, 0.10, 0.32), saturation 1.25.
- `MORNING`: soft sun (1.36, 1.14, 0.80) from the east-south-east at 16°, lilac haze 0.10.
- Emitters: two braziers (point lights, flicker via `set_oven`), the two glowing bakery fronts, and the pillory lanterns.

**Contract-still state** (`apply_cam_state`):
- Bakery: steam 0.8 (1.0 on `table_insert`), small balance +6 on `small_scale_insert`.
- Market: big balance -7 with 12 loaves, except `big_scale_insert`, which shows +6 with 13.

## 5. Measured

| quantity | value |
|---|---|
| final 720x1280, 12 samples, 2 threads, denoise + bloom (CPU s, `bakery_work/final_log.txt`) | market 19.0..22.0 (= mine.py's 19.8..24.2). Bakery 28.3..38.1: steam cards about +6, shafts +3, ink hull +4. `table_insert` and `bakery_wide` are the heaviest |
| hue (`bakery_work/hue_rows.txt`) | bakery MORNING red 33 orange 57 blue 0.5 magenta 5, val 0.59, dark 0.04 (ref A interiors red 46 orange 36 blue 8, val 0.47, dark 0.11). Market AFTERNOON red 37 orange 14 blue 34 violet 7, sat 0.43, val 0.66. MORNING blue 52, sat 0.33 |
| determinism | digest identical in two processes |

## 6. Command line

```
python3 bakery.py stills <bakery|market> [PRESET] [cam ...]   # bakery_work/stills 360x640 6 samples, placeholder actors, prints head pixels
python3 bakery.py final  <bakery|market> [PRESET] [cam ...]   # bakery_work/final 720x1280 12 samples, wall / cpu s, head pixels
python3 bakery.py digest <bakery|market> [PRESET]
python3 bakery_hue.py bakery_work/final
python3 bakery_work/t_anim.py $PWD                            # keyed hooks + determinism
W=360 H=640 COLS=5 python3 bakery_work/sheet.py contact.jpg <pngs...>   (CAP=1 draws the y 900 caption line)
```

## 7. Known gaps (honest)

- **Bakery value and warmth.** The bakery is warmer and lighter than the ref A interiors: orange 57 vs 36, value 0.59 vs 0.47, too few deep darks (4 % vs 11 %), almost no blue (the ref has 8 %). The sunlit floor patches and the cream plaster lift it. If a shot looks washed, lower the key, or darken the shade or plaster.
- **Steam.** The steam reads as thin wavy ribbons, not billowing clouds. It is single cards, turned 45°, so a camera looking exactly along a card sees it edge-on.
- **Bakery render cost.** The bakery is 28..38 CPU s against mine.py's 20..24. If needed: `set_steam(0)` in shots without steam, hide `sun_shafts`, or drop the ink hulls on `racks` and `dressing`.
- **Market tonality.** The market is brighter and flatter than the ref day exteriors: dark 0.02 vs 0.11, low orange (14 %). The MORNING variant is blue-heavy and low-saturation (the mist look).
- **Backdrop resolution.** The backdrop and sky textures are about 8 px/D at R 120. They are sharp at 720x1280, but they are cartoon-flat with no ink.
- **Market detail.** The market houses come from 4 facade variants, so the repetition is visible in `market_wide`. There are no 3D window shutters or flower boxes. The crowd is only placeholders.
- **No pillory hook.** The pillory board does not open: there is no `set_pillory` hook. baker2 is a card standing at `pillory.stand`.
- **Henry's front in the market is a 3D facade only.** It is not the same building as the bakery interior (the interior's own front is on its own street). Continuity of the facade (fascia, sign) is only approximate.
