# v3/set3d7/louvre.py : film 7 sets ("ไอ้มักกะโรนี", the Mona Lisa theft, Paris, August 1911) (bpy 5.3, Cycles CPU)

Files:
- `louvre.py`: the three locations (louvre, paris, room) and their hooks.
- `louvre_tex.py`: all artwork, drawn as SVG in Python and rasterised by `v3/set3d/raster.js` into `tex_louvre/`, cached by content hash. Includes `mona_svg()`, the flat cartoon Mona Lisa (public-domain painting, simplified). It is reused small, in sepia, on the newspapers and posters.
- `louvre_hue.py`: hue rows through `v3/tools/hue_report.py`.
- `contact.jpg`: every preset at 720x1280, 12 samples, with placeholder actors, plus a row of 6 reference frames. The cyan line is y 880.
  - `contact_small.jpg` is the same sheet at half size.

Work files are in `louvre_work/`:
- `final/<preset>.png`: the finals.
- `stills/`: 360x640 previews.
- `final_log.txt`: CPU time and head pixels per frame.
- `hue_rows.txt`
- `t_anim.py`: a test of the keyed hooks.
  - It also renders `hooks/` and `hooks.jpg`, one still per hook state.
- `t_cost.py`: a cost profile.
- `run_stills.sh`, `run_finals.sh`
- `magmap.py`: a magenta pixel map.
- `sheet.py`: the contact sheet builder (`CAP_Y`, default 880).
- `actors/`: the placeholder sprites.

The module is built on `v3/set3d6/bakery.py`, which in turn is built on `mine.py` → `pagoda.py` / `tower.py`. Helpers are imported, not copied:
- from `tower`: `mat_lit`, `mat_emit`, `MB`, the ink hull, `setup_grade`, `make_camera`, `render`, `no_bounce`, the keying helpers, `placeholder_actor`.
- from `pagoda`: `_kd`, `_pivot`, `_parent`, `_haze_mat`, `digest`.
- from `mine`: `obox`, `beam`, `rod`, `lumpy`, `catenary`, `chain_rod`, `_obj`, `_untoon`, `_glossy`, `_denoise`, `setup_render`.
- from `bakery`: `Frame`, `_mat_add` (camera-only glow cards), `_halo`, `_candle`, `_light`.

`louvre.STATE` is `tower.STATE`.

**No depth of field anywhere** (user rule: sharp). The set never sets up DOF. `apply_dof()` is a no-op. `setup_dof` is re-exported only so that shot scripts can call `L.setup_dof(scene, None, None, cam=cam)` as in film 6.

World: 1 unit = 1 D (head diameter), Z up, floor z = 0. `build` clears the scene and builds **only the area of the preset**. One area per build keeps the lamp count and the cost down.

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d7"); import louvre as L
A = L.build('louvre', 'gallery_wide')   # build(location, preset=None, clear=True, dress=True, light=None) -> anchors (section 3)
cam = L.make_camera(A['cam'])           # the preset camera; every camera of the area is in A['cams'], A['cam_name'] names it
L.setup_render(scene, 'final' | 'preview')   # 720x1280 12 samples / 360x640 6, 2 threads, direct light, OIDN, light tree off
L.apply_preset_state(preset)            # re-apply the preset's set state (build already did)
L.clear_keys()                          # drop all hook keys so un-keyed set_* calls hold at render time again
L.placeholder_actor(role, mark, face_to=None)  # stand-ins only (section 4)
L.stage_placeholders(A, cam_name, cam_loc); L.head_pixels(cam_name)   # contract-still staging + caption check
L.render(path) -> (wall s, cpu s);  L.digest() -> sha1
```

`light=` overrides the preset's light with any key of `L.LIGHTS`. For example, `build('louvre', 'wall_eye', light='CORRIDOR_MORNING')` gives a cooler, dimmer gallery.

**Keys rule.** Once a hook has been keyed with `frame=`, Blender's keys win over later un-keyed calls. Either key every state, or call `L.clear_keys()` first.

### Animatable hooks (all keyable with `frame=N`; key the start state too)

| hook | where | what |
|---|---|---|
| `set_mona(present, frame=None)` | louvre gallery | The Mona Lisa (canvas, gilt frame, her glass box) on the wall (`True`) or gone (`False`). **The four iron hooks always stay.** When she is gone, the unfaded damask patch with its dust line shows where she hung. Visibility keyed constant. `build`: present in `gallery_wide` / `wall_eye`, gone in `empty_wall_queue`. |
| `set_mona_lift(d, frame=None)` | louvre gallery | Lifts the framed painting off its hooks by `d` D. It moves along (0, -0.9, +0.6) per D, out and up. 0 = hanging, 0.3 = clear of the hooks, 0.8 = in his hands. Keys Bezier. |
| `set_queue(on, frame=None)` | louvre gallery | The reopening-day queue lanes (rope stanchions x ±2.6, y 14.6..20.4). The main rope before her (y 20.4) is always there. Keyed constant. |
| `set_frame_on_stairs(visible, frame=None)` | staircase | The empty gilt frame and her glass box left on the steps (step 5 / step 7). |
| `set_door(angle_deg, frame=None)` | exit_door | The locked service door swings inward-left on its hinge (-1.1, 9.88): 0 = shut, 95 = wide open. The bright courtyard plate and a shadowed daylight lamp (0 → 900 W by 60°) flood in. Keys Bezier for rotation, linear for light. |
| `set_papers(n, frame=None)` | paris | Newspapers and posters with her face, 0..24. They fill in order: kiosk front (8), kiosk sides (4), the Morris column (6), shop walls / shutters (6). Keyed constant. `build`: 24. |
| `set_trunk(pull=0, open_deg=0, panel=True, frame=None)` | room attic | The wooden trunk under the bed:<br>- `pull` 0 (under) .. 1 (out by 1.9 D toward +x)<br>- `open_deg` 0..100: the lid hinge on the -x edge. It clears the bed rail only once `pull` > 0.7.<br>- `panel`: the Mona panel on its red cloth inside.<br>Keys Bezier / constant. |
| `set_panel(visible, frame=None)` | dealer_shop | The panel (on red cloth) lying on the dealer's desk. |
| `set_flames(k=1, frame=None)` | all | Every gas jet, lantern, street lamp and candle: lamp energies and glow materials. 0 = out, 1 = normal, 1.5 = bright. Deterministic flicker from the frame number. **Call it every frame** (keys linear). |

`louvre_work/t_anim.py` checks all the hooks (ALL OK). It covers the eased lift, present/gone with the hooks staying, papers 0 → 12 → 24, the door 0 → 90, the trunk pull, the stair frame, and the flame ramp. It also renders the hook states to `hooks.jpg`:
- present / lifted 0.5 / gone
- papers 0 / 8
- door 85
- trunk out and open
- shop without the panel

Digests are identical in two processes:

| preset | digest |
|---|---|
| louvre gallery_wide | `88a77a52…` |
| exit_door | `5306f3b8…` |
| paris kiosk | `bf98ebad…` |
| room dealer_shop | `0ef02a51…` |

## 2. Presets (`L.PRESETS`, `L.LOC_PRESETS`)

| location | preset | area built | light (`L.LIGHTS`) | state at build |
|---|---|---|---|---|
| louvre | `gallery_wide` | Salon Carré | GALLERY_DAY | Mona present |
| louvre | `wall_eye` | Salon Carré | GALLERY_DAY | Mona present |
| louvre | `empty_wall_queue` | Salon Carré | GALLERY_DAY | Mona gone, queue on |
| louvre | `closet` | storage closet | CLOSET_NIGHT | lantern |
| louvre | `staircase` | service stair | STAIR_MORNING | frame + glass on the steps |
| louvre | `exit_door` | service corridor end | CORRIDOR_MORNING | door 0 (shut) |
| paris | `street_wide` | the rue + quai | STREET_GOLDEN | papers 24 |
| paris | `kiosk` | the rue + quai | STREET_GOLDEN | papers 24 |
| paris | `notre_dame_view` | the rue + quai | STREET_DUSK (lamps up, lit windows) | papers 24 |
| room | `room_wide` | attic room | ATTIC_DUSK | trunk under the bed, shut |
| room | `under_bed_insert` | attic room | ATTIC_DUSK | trunk pulled 0.45 |
| room | `dealer_shop` | Florence dealer's shop (dressing variant of `room`) | SHOP_DAY | panel on the desk |

### What each area holds

**Salon Carré** (x -13..13, y 0..22)
- Herringbone parquet, marble dado, red silk damask, gilt frieze with N medallions, a coffered cove, a laylight with the skylight opening (x -8..8, y 4.5..17.5) and iron glazing bars that pattern the sun.
- Floor-to-ceiling salon hang on all four walls: 155 gilt-framed pictures from 3 painted atlases. The upper rows lean forward.
- A 12 x 8 D Venetian feast canvas on the left wall.
- The Mona Lisa on the back wall at (0, 21.92, 3.55): canvas 1.0 x 1.45 D, frame 0.2, glass, brass plaque, the four hooks.
- The round velvet divan with a bronze urn, two benches, the brass stanchions and red rope, the guard chair, the copyist's easel, a picture ladder.
- Four bronze gas torchères with frosted globes.
- The service door (front wall, x 8..10).

**Closet** (5.2 x 3.6 x 6 D)
- Shelves of tins, jars and rags; brooms and mops; zinc buckets; crates.
- White smocks on pegs.
- A storm lantern on a crate (the only light); a line of light under the door.

**Service stair**
- 14 stone steps (rise 0.36, run 0.6) to a landing at z 5.04, between ashlar walls.
- An iron and wood handrail, two gas brackets.
- A tall landing window with a morning shaft.

**Exit door corridor**
- An oak door with iron straps and a lock box; the knob is missing (the hole shows).
- A glazed fanlight with daylight and a shaft.
- Gas brackets, lead water pipes (the plumber's), a coat rail with white smocks, framed notices, a bench, a fire bucket.

**Paris**
- The road (cobbles) x -4..4 and pavements to x ±7, running +y to the quai at y 62.
- Haussmann blocks both sides: painted facades with 3D balconies, cornice and zinc mansard.
- The Café du Louvre awning and tables.
- Cast-iron gas lamps along both kerbs and on the quai.
- The green newspaper kiosk "JOURNAUX" at (-5.6, 10) and a Morris column at (5.4, 16).
- A fiacre and horse, trees.
- The river, and Notre-Dame's west front: a painted cut-out plate, 72 x 60 D, at (5, 108).
- Painted Paris rooftops (Eiffel Tower, Sacré-Cœur, domes) on the R 120 ring.

**Attic** (x -4..4, y 0..6, 7 high; the mansard slope over the back wall)
- Faded wallpaper; a dormer window onto the rooftops.
- An iron bed with a quilt, the trunk under it.
- A washstand with basin and jug.
- A table with a candle, bread and a tin; a chair.
- The smock and cap on pegs, a shelf of books.
- His boots, a chamber pot, and a stub of candle on the floor by the bed.

**Dealer's shop** (x -6..6, y 0..9, 7.5 high)
- Green damask walls hung salon-fashion.
- Empty gilt frames leaning on the wall.
- Two glass cabinets of maiolica and bronzes, a marble bust on a column.
- The desk with a green-shaded oil lamp and the panel.
- A six-candle brass chandelier.
- The shop window onto Florence: the Duomo, Giotto's tower and the Palazzo Vecchio, painted.

## 3. Cameras, stand points, staging, card scales, caption check

Card scale: the puppet card height in D equals the role height in `L.HEIGHT`. There is no extra scale: cast scale 1.0 at these heights.

| role | height (D) |
|---|---|
| vincenzo (small) | 2.75 |
| director (tall) | 3.6 |
| guard / police | 3.2 |
| worker / plumber / man / painter | 3.0 |
| dealer | 3.1 |
| woman | 2.9 |
| newsboy | 2.4 |

**Caption rule: every staged head stays above y 880 of 1280.** The table checks the **chin** (head bottom) at 720x1280; the head centre is higher still.

`head_pixels(cam)` returns `(role, mark, head_centre_y, head_px, chin_y, feet_y)`.

| preset cam | loc → look_at, lens | shows | staged cards (feet) | head centre / chin px (head px) |
|---|---|---|---|---|
| `gallery_wide` | (9.9, 1.3, 3.6) → (-3.6, 21, 4.7), 22 | From the service-door corner: three hung walls, the feast canvas, divan, skylight and bars, the patterned sun on the back wall. She is small behind the rope | guard (4.6, 8.4), woman (-3.4, 14.6), man (-1.2, 17), director (2.8, 13.6) | 756/801 (89), 727/748, 721/742, 704/732 |
| `wall_eye` | (0.6, 14.6, 2.8) → (-0.2, 22, 3.5), 24 | Eye level at the rope: the Mona Lisa canvas 115 px wide in her gilt frame and glass, the hang tight round her, torchère glow | vincenzo (1.7, 21.1) | 796/865 (138) |
| `empty_wall_queue` | (3.2, 10, 6.8) → (-0.3, 22, 2.2), 22 | High over the queue: the empty wall (hooks, patch, plaque), the rope lanes | women (-1.1, 19.4), (-0.2, 17.7), (-1.0, 16.2); men (0.9, 18.9), (1.3, 16.6); guard (4, 19.8) | 682..804 / 714..846 |
| `service_door` (extra) | (-2, 12, 3.6) → (8.6, 0, 2.6), 22 | Reverse onto the service door and the guard chair | guard (6.6, 2.2) | — |
| `closet` | (2.0, 0.45, 3.3) → (-1.3, 3.1, 1.7), 20 | Inside by the lantern: shelves, brooms, smocks | vincenzo (-0.9, 1.6) | 624/724 (213) |
| `staircase` | (0.9, -2.6, 2.6) → (-0.4, 8, 5.4), 22 | From the foot up the flight: gas brackets, the window shaft, the frame and glass on the steps | vincenzo on step 8 (0.2, 4.2, z 2.88) | 563/615 (102) |
| `exit_door` | (1.5, 3.4, 2.5) → (-0.3, 10, 3.1), 22 | Before the locked door: fanlight, lock, smocks, pipes; `set_door` opens it on the courtyard | vincenzo (0.9, 8.0) | 752/839 (173) |
| `street_wide` | (-2.4, -9, 4.2) → (1, 20, 5.4), 22 | Down the rue: Haussmann rows, café awning, kiosk, column, fiacre, lamps, Notre-Dame at the end | woman (-5.2, 8, z 0.25), man (5, 6.5, 0.25), newsboy (-3.4, 3), man (-1, 14) | 726..826 / 747..860 |
| `kiosk` | (-1.5, 6.3, 2.6) → (-4.8, 10.6, 2.4), 22 | The sunlit kiosk front: 8 front pages with her face, the lamp, the column beyond | man (-3.3, 13.8), newsboy (-2.3, 12.2) | 622/678, 717/791 |
| `notre_dame_view` | (1.5, 40, 3) → (3, 108, 16), 22 | Dusk at the quai: Notre-Dame's two towers standing, lamps lit | woman (0.4, 54), man (3, 56) | 825/854, 815/841 |
| `room_wide` | (3.7, 0.2, 3.0) → (-0.4, 4.5, 1.5), 18 | The attic at dusk: bed and trunk, dormer window, table candle, floor candle | vincenzo (-0.2, 2.3) | 594/666 (148) |
| `under_bed_insert` | (1.5, 0.7, 0.95) → (-2, 2.9, 0.45), 22 | Floor level: the trunk under the bed, quilt edge, boots, the floor candle | none (a hand can enter from frame right) | — |
| `dealer_shop` | (4.8, 0.4, 4.4) → (-2.2, 6.2, 2.3), 20 | The Florence shop: hung walls, cabinets, bust, chandelier, the desk with the panel and lamp, the window light | dealer (-1.6, 5.0), vincenzo (0.9, 3.6) | 639/681, 766/827 |

### Stand points (`A['marks']`, feet; z is the floor or the pavement height)

**Gallery**
- `mona_viewer` (0, 19.6)
- `thief_at_wall` (0.9, 21.0): in front of her, inside the rope
- `director` (3, 13)
- `guard_chair` (6.6, 1.2)
- `copyist_easel` (-6.2, 13.5)
- `rope_line` y 20.4, x ±2.6
- `queue_lanes` x ±2.6, y 14.6..20.4
- `divan` at (0, 10), r 1.9
- `A['mona']['hooks']`: the four hook points

**Closet**
- `vincenzo_hide` (-0.9, 1.6)
- `lantern` (0.75, 2.6, 1.28)

**Stair**
- `vincenzo_step8` (0.4, 5.1, 2.88)
- `vincenzo_landing` (0, 10, 5.04)
- A card on step k stands at z = (k+1) × 0.36 for y in k × 0.6 .. (k+1) × 0.6.

**Exit door**
- `vincenzo_door` (0.9, 8)
- `plumber_enter` (0.4, 11.5): beyond the door, in the courtyard light
- `A['door']`: hinge, width, height

**Paris**
- `kiosk_reader` (-2.9, 9.4, 0) and `kiosk_side` (-4.0, 12.4, 0.25)
- `newsboy` (-3.4, 13.5)
- `cafe` (5, 7, 0.25)
- `passers`, three spots
- `quai` (0, 58.5, 0.25)
- Pavements are z 0.25; the road is z 0.

**Attic**
- `vincenzo_bed` (-0.9, 2.6)
- `vincenzo_table` (1.0, 3.2)
- `trunk`: rest (-2.85, 2.6)
- `window` (1.7, 6.0, sill 1.9)

**Shop**
- `dealer_desk` (-1.6, 5.0)
- `vincenzo_shop` (0.9, 3.6)
- `police_door` (4.2, 1.0)

Keep-out zones are in `A['keep_out']`.

## 4. Light presets

Same light model as the templates:
- one hard sun with real shadows;
- painted shade emission;
- no bounce, `emission_sampling` NONE;
- every material `_untoon`ed (plain Lambert), so the sun and the point lamps both work;
- the grade compositor with bloom.

Warm in-scene emitters everywhere: gas globes, lanterns, candles, street lamps. Each has a camera-only halo card and a floor light pool where it matters. Camera-only sun-shaft cards come from the skylight and windows.

**Interiors.** In lamp-lit interiors, red + blue shade turns magenta. To stop that:
- the shade is pushed toward hue ~225, the complement of the lamps;
- saturated reds (velvet, rope, damask, quilt) carry their own low `shade_mix`;
- the lamps are yellow-orange: GAS (1, 0.8, 0.5).

| light | sun | shade | lamps |
|---|---|---|---|
| GALLERY_DAY | (1.55, 1.30, 0.92), 57°, through the skylight bars | (0.085, 0.095, 0.21), mix 0.78 | skylight fill 2600 W + front fill 700 W (no shadow), 4 torchères 140 W (2 shadowed); 2 shaft sheets |
| CLOSET_NIGHT | none | dark blue | storm lantern 150 W, shadowed |
| STAIR_MORNING | through the landing window, 38° | neutral grey-blue | 2 gas brackets 170 W |
| CORRIDOR_MORNING | through the fanlight, 30° | neutral grey-blue | 2 gas brackets 170 W; the daylight lamp opens with the door |
| STREET_GOLDEN | (1.75, 1.12, 0.55), 35°, travelling along the street (-0.3, 0.95) so the kiosk side is lit | (0.13, 0.13, 0.27) | lamps near the kiosk 60 W; warm haze |
| STREET_DUSK | 8°, low from the north-west | — | lamps 140 W, lit windows (facade variant `_n`), dusk sky and rooftop ring |
| ATTIC_DUSK | low sun through the dormer, 14° | — | table candle 60 W + floor candle 30 W (shadowed), window fill 90 W |
| SHOP_DAY | through the shop window, 30° | — | desk lamp 90 W (shadowed), chandelier 160 W |

## 5. Measured

**Render cost.** Final 720x1280, 12 samples, 2 threads, denoise + bloom, CPU s per frame (`louvre_work/final_log.txt`):

| preset | CPU s |
|---|---|
| gallery_wide | 24.4 |
| wall_eye | 25.4 |
| empty_wall_queue | 25.4 |
| closet | 21.0 |
| staircase | 20.0 |
| exit_door | 21.7 |
| street_wide | 20.8 |
| kiosk | 22.3 |
| notre_dame_view | 18.7 |
| room_wide | 22.0 |
| under_bed_insert | 24.0 |
| dealer_shop | 24.3 |

The gallery profile (`t_cost.py`):
- each shaft sheet costs about 0.9 s;
- the ink hulls about 2.6 s;
- the denoiser about 3 s.

**Hue** (`louvre_work/hue_rows.txt`), all 12 finals together:

| hue family / measure | value | target band |
|---|---|---|
| red | 30.2 | 30-41 |
| orange | 45.8 | 22-38 |
| blue | 14.5 | 14-30 |
| violet | 2.4 | 0-5 |
| magenta | 3.1 | 0-10 |
| sat | 0.33 | 0.38-0.48 |
| val | 0.50 | 0.45-0.63 |
| dark | 0.12 | 0.08-0.15 |

Every frame has magenta under 10 (the highest is `notre_dame_view` at 8.0). Violet is at most 9.0 per frame (`room_wide`); the daylit gallery frames are about 0.1.

**Determinism**: the digest is identical in two processes (section 1).

## 6. Command line

```
python3 louvre.py stills <louvre|paris|room> [preset ...]   # louvre_work/stills 360x640, placeholders, prints head pixels (EXTRA=1: also the area's other cams)
python3 louvre.py final  <louvre|paris|room> [preset ...]   # louvre_work/final 720x1280 12 samples, wall / cpu s, head pixels
python3 louvre.py digest <loc> <preset>
louvre_work/run_stills.sh ; louvre_work/run_finals.sh       # everything, 2-3 processes
python3 louvre_hue.py louvre_work/final ; python3 louvre_work/t_anim.py ; python3 louvre_work/t_cost.py louvre gallery_wide
cd louvre_work; W=360 H=640 COLS=6 CAP=1 python3 sheet.py ../contact.jpg <pngs...>   (CAP=1 draws the y 880 line, CAP_Y to change)
```

## 7. Known gaps (honest)

- **Warmth and saturation.**
  - The set runs warmer than ref A: orange 46 vs 36, saturation 0.33 vs 0.39.
  - The lamp-lit service rooms are low-saturation: exit door 0.19, attic 0.21.
  - `closet` is a night frame: dark 0.31, blue 45.
  - The street frames are blue-heavy, about 45 % (ref day exteriors 21 %), because half the street is in shade.
- **The Mona Lisa is a simplified flat cartoon.** It shows the three-quarter pose, the dark hair and veil, the smile, the folded hands, the ochre sleeves, the mountains and the road. The bridge is mostly hidden by her shoulder.
  - On the newspapers and posters she is small. They read as "her face" at the kiosk distance, but the mastheads are only legible in close-ups.
- **The salon pictures** are 3 atlases × 16 procedural cells (landscapes, portraits, madonnas, seascapes, still lifes, battles, ruins, feasts), so repeats can be found in the wide shot. The canvases are painted flat with no ink.
- **Placeholders only.** All actors are stand-in cards facing the camera. The queue crowd should face the wall in the real shots. The kiosk vendor has no stand point because the kiosk interior is a solid box.
- **The paris street is one area for three presets.** `notre_dame_view` is the same street at dusk looking at the quai. Notre-Dame is a painted plate, not 3D, and is placed closer than in reality (artistic).
- **The trunk lid** collides with the bed rail if it is opened while `pull` < 0.7. The panel inside is visible only from above (`room_wide`-style height) when the lid is open.
- **Cost** is at the 25 s limit in the gallery. If a shot needs headroom: hide `sun_shafts` (about -1.8 s), or drop the `frames` ink hull (`STATE['objects']['frames'].modifiers['ink_hull'].show_render = False`, about -1.5 s).
- **The service door in the gallery is static** (painted double door). Only the `exit_door` area has the working door.
