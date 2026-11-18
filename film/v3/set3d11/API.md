# v3/set3d11/dairy.py : film 11 set ("ไอ้หมอวัว", Jenner, cowpox, Berkeley 1796) as a real 3D Blender set (bpy 5.x, Cycles CPU)

Files (all in `film/v3/set3d11/`):
- `dairy.py`: the three locations, 11 presets, light states A / C, cameras, stand points, hooks, the CLI. Imports the helpers of the earlier sets (`tower`, `mine`, `wall`) like `set3d10/harbour.py`.
- `dairy_geo.py`: the geometry kit: prototype stamping, lofts, the detailed **cow**, hens, cats, dog, geese, strand hay and straw, **layered thatch** roofs (stepped courses with ragged fringes and a ridge roll), dry-stone walls, flowers / grass tufts / trees, windows and doors, and the animation hooks.
- `dairy_tex.py`: all the artwork, painted with numpy + PIL (strand thatch, strand hay, two brown-and-white cow coats, flagstones, cobbles, rag rug, patchwork quilt, lane, plus the board painters from `dairy_board_tex.py`). Cached in `tex_dairy/` keyed by `TEX_V`; bump `TEX_V` after editing a painter.
- `dairy_hue.py`: hue rows through `tools/hue_report.py` plus the **shade hue** and the **magenta share** per frame (client rule: shade hue 240-260, magenta <= 10 %). Prints the per-preset table.
- `make_contact.py` -> `contact.jpg` (11 tiles of 720x1280, label under each tile, cyan line at y 880) and `contact_small.jpg` (1/3).
- `t_anim.py`: the hook test (64 checks, prints ALL OK); `dairy_work/t_anim_log.txt` is its log.
- `dairy_work/`: `final/` (the 11 final tiles), `final_log.txt` (wall / CPU seconds, head pixels), `times_all.json`, `hue_rows.txt`, `hue.json`, `qa_tiles.py` + `qa_tiles_log.txt` (qa_auto-style sanity on the tiles), `contact_order.txt` (`python3 dairy.py stills` writes 360x640 6-sample previews to `stills/`).
- `board/`, `dairy_board.py`, `dairy_board_tex.py`, `board_hue.py`, `make_board.py`: the approved style board (kept untouched).

World: **1 unit = 1 D (one head), Z up.** Adults 3.1-3.4 D tall (`ROLES`: jenner 3.3, doctor 3.4, sarah / maid / mother 3.1, villager 3.2), the 8-year-old boy 2.3 D. Camera: 22 mm, sensor 36 mm fitted to the long side (vertical FOV 78.6 deg, horizontal 49 deg), **no depth of field**, **no text or signs anywhere**.

## Load a preset in a shot script

```python
import sys; sys.path.insert(0, 'film/v3/set3d11')
import dairy as D, bpy
A = D.build('barn_milking')                  # location + light + sky + dressing + hooks; light='A'|'C' overrides the preset's light
cam = D.make_camera(A['cam'])                # preset camera (A['cams'] holds every camera of the location); move it per shot as you like
sc = bpy.context.scene                       # final render settings are already set: 720x1280, Cycles CPU, 24 samples, OIDN, 4 threads
sc.frame_set(37)                             # hooks are drivers on `frame`: nothing is keyed, every frame is alive
D.stage_placeholders(A, 'barn_milking')      # placeholder_actor cards (+ a 3D cow marker at the Blossom point) on the stand points: stills / tests only
import tower as T; T.render('/tmp/x.png')    # wall / cpu seconds
```
For the real shots: put the cast11 cards at `A['stand'][preset][slot]['pos']` (x, y, contact z), scale by `height`, face the camera (yaw only), lean back a few degrees for high cameras. The z is the CONTACT z: the floor, or the stool top for seated figures (`seated: True`) and the mattress top for the boy in bed. The set has no card for Blossom: her 2D side-view puppet stands on the `blossom` point (centre of the 4.4 D body, head to -x).
CLI: `python3 dairy.py finals [preset[:LIGHT] ...]` (final 720x1280, writes `dairy_work/final/<preset>.png` + the log), `stills` (360x640 previews), `digest <preset>` (object / triangle counts). Set `ACTORS=0` to render without the cards. `DAIRY_P='{"shade":[..]}'` overrides light parameters for experiments.

## Locations, presets, light states, cameras

| preset | location | light | camera (loc -> look_at, 22 mm) | sun (azimuth, elevation) | what it shows |
|---|---|---|---|---|---|
| `barn_wide` | barn | A | (2.6, -1.0, 2.8) -> (0.6, 15.0, -0.9) | az 240, el 24 | eye-level wide from the barn front (golden morning): the open door and its sun pool left, the cow stalls right, the hay loft at the back, hens and tools along the whole lower third |
| `barn_milking` | barn | A | (-0.4, 6.6, 1.6) -> (-3.0, 15.0, 1.5) | az 215, el 24 | low medium on the milking nook inside the door: stool and pail at the cow flank, sun pool, the stalls and bg cows behind |
| `barn_high` | barn | C | (-2.0, 4.6, 6.0) -> (-5.4, 13.6, 0.6) | az 185, el 11 | high angle (amber C): the door crowd left against the clear-faced milkmaids in the sun pool, floor props everywhere |
| `barn_door` | barn | A | (2.2, 15.0, 1.3) -> (-12.0, 15.6, 2.6) | az 240, el 22 | low angle from inside out through the open door: sunny lane, wall, wagon, trees, hills, cumulus, sun shafts |
| `garden_hut` | village | A | (3.5, -6.6, 1.5) -> (-10.0, 0.8, 2.6) | az 300, el 34 | Jenner garden: the rustic thatched hut with the boy on his stool, the cottage and church tower behind, flower beds all round |
| `lane_wide` | village | A | (41.0, -12.3, 1.7) -> (-40.0, -9.2, 4.6) | az 300, el 40 | the village lane at eye level looking toward the church: stone cottages both sides, villagers, the doctor arrives |
| `lane_high` | village | A | (8.0, -34.0, 13.0) -> (-1.0, -11.0, 1.0) | az 300, el 36 | high angle over the lane and green: the crowd in the middle, cottages, church tower, hills |
| `garden_queue` | village | A | (2.0, -15.0, 3.2) -> (-3.0, -2.5, 2.4) | az 300, el 36 | side view across the picket fence: the long queue from the gate to the hut door, flower beds, orchard, church tower |
| `room_day` | cottage | A | (1.6, -2.6, 2.7) -> (-1.0, 5.0, 1.3) | az 163, el 26 | Phipps room: bed under the window (left), table, hearth, daylight shaft |
| `room_night` | cottage | C | (1.6, -2.6, 2.7) -> (-1.0, 5.0, 1.3) | az 166, el 9 | same room at late-amber dusk: candle on the table, the open door (right) for the doctor, deep blue-violet shade |
| `room_morning` | cottage | A | (1.6, -2.6, 2.7) -> (-1.0, 5.0, 1.3) | az 160, el 19 | same room in morning sun: the bed, the floor space for the jump out of bed |

Light states (`D.LIGHTS`): **A** = golden morning (key sun 1.95 / 1.50 / 0.88, honey light, blue-violet painted shade, warm no-shadow bounce sun at 7 %), **C** = late amber (key 1.65 / 0.92 / 0.36, low sun 11 deg, deeper violet shade). Exactly ONE hard key sun with cast shadows per frame, plus the board's no-shadow warm bounce sun; the only other lights are the practicals: the three hanging lanterns of the barn (point lights, swing with the lantern), and in `room_night` the **candle** (point light + flame) and a hearth glow. The sun direction is set per preset (`PRESETS[p]['sun']`, azimuth from +x CCW as the sky-texture convention, the sun sits at that azimuth). Far hills and far trees never cast shadows (a low sun must reach the barn floor). Cards are unlit emission and block the key (they cast shadows).
Shade hue / magenta are tuned per preset through `PRESETS[p]['P']` (shade, shade_tint, lift, air, key overrides): see the table at the end.

### World coordinates
- **barn** (all four barn presets share one build): the barn floor is z 0, x -10..10, y -1..34; the front gable (y -0.7) is shadow-only (invisible to the camera, so cameras may sit at y < 0) with a wide opening x -8.4..8.4 below z 5.7 that lets the sun onto the front floor. The **open door** is in the left wall: x -10, y 10..21, lintel z 5.8; outside it (x < -10) are the lane, a hay wagon, geese, hens, a stone trough, the farmyard dry-stone wall (x -36), orchard trees, hills and the sky dome. **Right wall stalls** (x 1.8..9.9; partitions at y 7.6 / 12.6 / 17.6 / 22.6 are low boards + two thin rails so the cows stay visible): three 3D brown-and-white cows (`cowS1..S3`, coats a / b) at (5.6, 10.1), (5.7, 15.1), (5.5, 20.1) eating at the mangers (x ~9), and a calf tethered at the back left (-5.8, 28.4). **Hay loft** y 22..34 (floor z 4.4..4.8) with strand hay heaps, a ladder at x -7. The **milking nook**: milking stool (-3.2, 13.1) (seat z 0.85), milk pail (-2.1, 14.0) under where Blossom's udder will be, a second pail, straw bedding and hay heaps. **No tie beams, collars or braces anywhere**: the roof has only purlins, a ridge beam, wall plates (all receding along y) and thin rafters; the loft has posts and a floor edge only.
- **village** (one build for the four village presets): the lane runs along **x** at y -15.2..-8.0 (cobble-dirt with ruts), the picket fence with the gate (x -2.6..-0.4) at **y -8.0**, **Jenner's garden** y -8..18 x -22..22 (flagged path from the gate north to the door at x -1.5; branch to the hut; flower beds both sides of the path, vegetable patch x 12.6..21.5 y -6.5..-2, bee skeps at (6..9, -3), washing line at y 9.5, water butt), the **honey-stone cottage** x -10..10 y 9..17 (layered thatch, two chimneys with animated smoke, eyebrow dormers) with the kitchen wing x 10..17, the **rustic round thatched hut** at (-12.0, -2.5) r 2.8 (door faces azimuth -20 deg, the boy's stool at (-8.0, -3.4)), the **orchard** at x -50..-22 (apple trees in blossom, falling petals, a grazing 3D cow at (-31, 9)), dry-stone walls east / west / north of the garden, **terrace cottages** along the lane (north side y -6.2..1.8: x 22..38, -44..-26, -66..-48, -90..-70, 42..64; south side y -30..-22: x 18..38, -34..-14, -58..-38, -84..-62, 42..62) with doorstep dressing, the **village green** south of the lane (pond at (-18, -32) with ducks / reeds, the old oak at (30, -32), a stone well at (-6, -22), a wain, barrels, sheep, wild flowers), the **church** with a tall tower at (-108, -2) at the end of the lane, a churchyard wall with yews, and a patchwork hill ring (radius 130..480, up to 85 D high) with sheep and hedged fields. Sky dome with cartoon cumulus, rotated per preset (`look_az`).
- **cottage** (Phipps family room, one build for the three presets): floor z 0, x -7.5..7.5, y -3.6..12 (front wall at y -3.6 is shadow-only, cameras sit inside), ceiling z 5.6 with beams along y only. **Bed** under the left-wall window: x -7.3..-3.2, y 2.4..8.8, mattress top z 1.7, head at y 8.8 (patchwork quilt, pillow). **Left window** y 4.0..9.0, z 2.3..5.2; **back window** x 0.8..4.2, z 2.6..5.3; **door** in the right wall x 7.5, y 3.0..6.6, z 0..4.6, leaf open into the room, doorstep and yard outside. **Hearth** at the back right (x 1..7, y 11..12; fire + iron pot), **dresser** with plates at the back (x -2.6..0.4), table + two benches + two chairs at (3.2, 5.2) with bowls, a loaf and the candlestick at (3.4, 5.5, 2.1..3.1), spinning wheel (6.2, 7.6), rag rugs, a cat and a dog by the hearth, coats on pegs by the door, hanging herbs and hams, floor dressing in front of the camera.

### Stand points (name -> (x, y, contact z)); all adults / boy placed as placeholder cards at these marks in `contact.jpg`
`A['stand'][preset]` is the dict below; `A['staging'][preset]` lists the slots that `stage_placeholders` fills. Cast roles: `jenner`, `boy` (James, 2.3 D; `pose: in bed` = lying in bed), `sarah` (milkmaid Sarah Nelmes), `maid` (2nd milkmaid), `doctor` (town doctor / mocker), `mother`, `villager`, `villager_p` (pockmarked), `cow` (Blossom, 2D side view, `length` 4.4 D, head to -x).

**barn_wide** (camera (2.6, -1.0, 2.8) -> (0.6, 15.0, -0.9))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `sarah` | sarah | 3.1 | (-3.4, 11.8, 0.00) | milkmaid Sarah Nelmes, standing in the sun pool by the stool |
| `maid` | maid | 3.1 | (0.4, 12.6, 0.00) | 2nd milkmaid |
| `jenner` | jenner | 3.3 | (-6.4, 10.0, 0.00) | Jenner at the door side |
| `blossom` | cow | - | (-1.6, 16.2, 0.00) | Blossom 2D puppet, side view, head to -x, 4.4 D long |
| `boy` | boy | 2.3 | (2.0, 9.0, 0.00) | James near the aisle |

**barn_milking** (camera (-0.4, 6.6, 1.6) -> (-3.0, 15.0, 1.5))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `sarah` | sarah | 3.1 | (-3.2, 13.1, 0.85) | milkmaid SEATED on the milking stool (z = stool top), at the udder side |
| `blossom` | cow | - | (-3.1, 15.4, 0.00) | Blossom 2D, side view, head to -x, flank to camera, udder at x -2.0 |
| `maid` | maid | 3.1 | (-6.8, 12.0, 0.00) | 2nd milkmaid standing left |
| `pail` | cow | - | (-2.1, 14.0, 0.00) | pail under the udder (3D pail already there) |

**barn_high** (camera (-2.0, 4.6, 6.0) -> (-5.4, 13.6, 0.6))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `sarah` | sarah | 3.1 | (-3.4, 12.2, 0.00) | clear-faced milkmaid |
| `maid` | maid | 3.1 | (-1.2, 13.4, 0.00) | clear-faced milkmaid 2 |
| `vill_a` | villager_p | 3.2 | (-8.8, 12.4, 0.00) | pockmarked villager in the door |
| `vill_b` | villager_p | 3.2 | (-9.6, 15.2, 0.00) | pockmarked villager in the door |
| `vill_c` | villager_p | 3.2 | (-8.6, 18.0, 0.00) | pockmarked villager in the door |
| `vill_d` | villager | 3.2 | (-11.4, 14.0, 0.00) | plain villager outside the door |
| `blossom` | cow | - | (-4.2, 17.4, 0.00) |  |

**barn_door** (camera (2.2, 15.0, 1.3) -> (-12.0, 15.6, 2.6))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `sarah` | sarah | 3.1 | (-5.2, 14.2, 0.00) | milkmaid in the foreground, back to the light |
| `jenner` | jenner | 3.3 | (-12.5, 17.0, 0.00) | Jenner on the lane in the sun |
| `vill_a` | villager | 3.2 | (-14.5, 13.6, 0.00) |  |
| `vill_b` | villager_p | 3.2 | (-16.0, 19.0, 0.00) |  |
| `blossom` | cow | - | (-2.0, 12.0, 0.00) |  |

**garden_hut** (camera (3.5, -6.6, 1.5) -> (-10.0, 0.8, 2.6))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `boy` | boy | 2.3 | (-8.0, -3.4, 0.80) | James SEATED on the stool at the hut door (z = stool top) |
| `jenner` | jenner | 3.3 | (-6.2, -0.8, 0.00) | Jenner with the lancet, beside the boy |
| `sarah` | sarah | 3.1 | (-3.0, 0.2, 0.00) | milkmaid at the bed edge |
| `doctor` | doctor | 3.4 | (-4.4, 2.6, 0.00) | town doctor in the garden, behind the others |

**lane_wide** (camera (41.0, -12.3, 1.7) -> (-40.0, -9.2, 4.6))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `doctor` | doctor | 3.4 | (27.0, -11.6, 0.00) | town doctor arriving, centre of the lane |
| `villager_a` | villager | 3.2 | (23.0, -9.4, 0.00) |  |
| `villager_b` | villager_p | 3.2 | (31.5, -13.0, 0.00) |  |
| `villager_c` | villager | 3.2 | (20.0, -12.8, 0.00) |  |
| `maid` | maid | 3.1 | (29.0, -9.2, 0.00) |  |
| `jenner` | jenner | 3.3 | (17.5, -10.6, 0.00) |  |
| `boy` | boy | 2.3 | (24.6, -13.6, 0.00) |  |

**lane_high** (camera (8.0, -34.0, 13.0) -> (-1.0, -11.0, 1.0))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `c0` | villager_p | 3.2 | (-6.0, -16.0, 0.00) | crowd slot 0 |
| `c1` | villager | 3.2 | (-3.2, -13.2, 0.00) | crowd slot 1 |
| `c2` | villager | 3.2 | (-0.4, -16.4, 0.00) | crowd slot 2 |
| `c3` | villager_p | 3.2 | (2.4, -13.0, 0.00) | crowd slot 3 |
| `c4` | villager | 3.2 | (5.2, -16.0, 0.00) | crowd slot 4 |
| `c5` | villager | 3.2 | (8.0, -13.4, 0.00) | crowd slot 5 |
| `c6` | villager_p | 3.2 | (-4.6, -9.6, 0.00) | crowd slot 6 |
| `c7` | villager | 3.2 | (0.4, -10.4, 0.00) | crowd slot 7 |
| `c8` | villager | 3.2 | (5.0, -9.6, 0.00) | crowd slot 8 |
| `doctor` | doctor | 3.4 | (0.8, -19.2, 0.00) | the mocking doctor at the front of the crowd |

**garden_queue** (camera (2.0, -15.0, 3.2) -> (-3.0, -2.5, 2.4))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `q0` | villager_p | 3.2 | (4.6, -3.2, 0.00) | queue slot 0 (0 = near the gate) |
| `q1` | villager | 3.2 | (2.7, -3.2, 0.00) | queue slot 1 (0 = near the gate) |
| `q2` | villager | 3.2 | (0.8, -3.2, 0.00) | queue slot 2 (0 = near the gate) |
| `q3` | villager_p | 3.2 | (-1.1, -3.2, 0.00) | queue slot 3 (0 = near the gate) |
| `q4` | villager | 3.2 | (-3.0, -3.2, 0.00) | queue slot 4 (0 = near the gate) |
| `q5` | villager | 3.2 | (-4.9, -3.2, 0.00) | queue slot 5 (0 = near the gate) |
| `q6` | villager_p | 3.2 | (-6.8, -3.2, 0.00) | queue slot 6 (0 = near the gate) |
| `jenner` | jenner | 3.3 | (-9.0, -1.5, 0.00) | Jenner at the hut door |
| `boy` | boy | 2.3 | (-8.0, -3.4, 0.00) | James first in the queue |
| `doctor` | doctor | 3.4 | (8.2, -3.6, 0.00) | the mocker, rolls up his sleeve at the tail |

**room_day** (camera (1.6, -2.6, 2.7) -> (-1.0, 5.0, 1.3))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `mother` | mother | 3.1 | (-0.8, 3.0, 0.00) | mother by the bed |
| `boy_bed` | boy | 2.3 | (-5.2, 7.2, 1.70) | James lying in bed: z = mattress top, pillow at the window end |
| `jenner` | jenner | 3.3 | (1.0, 4.8, 0.00) | Jenner at the bedside |

**room_night** (camera (1.6, -2.6, 2.7) -> (-1.0, 5.0, 1.3))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `mother` | mother | 3.1 | (-1.4, 3.0, 0.00) |  |
| `boy_bed` | boy | 2.3 | (-5.2, 7.2, 1.70) | feverish in bed |
| `doctor` | doctor | 3.4 | (6.4, 4.8, 0.00) | town doctor in the doorway, pointing (door opening y 3.0..6.6, x 7.5) |
| `jenner` | jenner | 3.3 | (1.2, 2.2, 0.00) | Jenner |

**room_morning** (camera (1.6, -2.6, 2.7) -> (-1.0, 5.0, 1.3))

| slot | role | height D | (x, y, contact z) | note |
|---|---|---|---|---|
| `boy` | boy | 2.3 | (-2.0, 3.2, 0.00) | James jumps out of bed (floor) |
| `mother` | mother | 3.1 | (1.6, 2.6, 0.00) | mother |
| `boy_bed` | boy | 2.3 | (-5.2, 7.2, 1.70) |  |

### Animation hooks (drivers on `frame`: no keys, any frame number works, nothing freezes)
`A['hooks']` lists `{kind, obj}`. Kinds: `cow_tail` / `cow_ear` (every cow: tail swish about the root, ears flick), `hen_peck` (every hen pecks on its own phase), `lantern` (the barn lanterns swing on their chains, their point light follows), `motes` (dust in the sun, 3-4 drifting clouds), `smoke` (chimney smoke: billows rise, grow and fade on a loop, drifting), `leaves` (blossom petals falling in the orchard), `cloth` (washing sheets sway), `curtain` (room curtains), `fire` (hearth flames flicker), `candle` + `candle_light` (room_night: flame wobble and light flicker). `t_anim.py` proves each moves between frames.

### Detail bar (what is in the set)
- **Cows**: loft-built body (14-point cross-sections, rump to chest), haunches, shoulders, hip and pin bones, neck with dewlap, head with brown patch, eyes, nostrils, muzzle, curved horns, ears, four jointed legs with knees / hocks / socks / hooves, udder with four teats, tail with switch; two painted coats (cream with brown patches, chestnut with cream patches). Placed with `cow(SET, cmb, M, pos, yaw, coat, head, phase, name, scale)`; the 2D Blossom puppet takes the `blossom` stand point.
- **Hay and straw**: heaps are textured lumps covered in hundreds of fine straw blades; bales with twine and ragged ends; floor straw as thin blades and flat rods; **thatch** is real geometry: 15 stepped courses per slope with a thick butt on each, hanging ragged fringes, a ridge roll with crossed spars; the hut has stacked straw rings.
- **Garden**: ~12 flower species (hollyhock, delphinium, foxglove, lupin, lavender, marigold, roses, poppy, viola, daisy, buttercup, cow parsley), cabbages, bean poles, bee skeps, stone-edged beds, picket fence and gate, climbing roses on the cottages, window boxes, dry-stone walls from individual stones, a church tower with buttresses and battlements, cumulus sky.
- **Lower third (y 880-1280)** is never bare: every preset has camera-relative dressing (`fg_props`: stools, pails, baskets, hens, hay, barrels, crates, a wheelbarrow, geese, a dog) plus straw / pebbles / tufts / flowers / litter scattered over the ground. Near-camera foliage is small and fine (grass blades <= 0.45 D, flowers <= 0.7 D).

### Render timings (4 cores, 24 samples, OIDN denoise, 720x1280; the per-frame budget is 25 s wall)
| preset | build s | render wall s | render CPU s | head px (slot size) | max chin y | shade hue | magenta % |
|---|---|---|---|---|---|---|---|
| `barn_wide` | 2.2 | 9.1 | 35.0 | sarah 61, maid 59, jenner 68 | 503 | 251.0 | 4.4 |
| `barn_milking` | 2.2 | 9.1 | 35.2 | sarah 112, maid 111 | 575 | 244.5 | 2.1 |
| `barn_high` | 2.2 | 12.7 | 49.3 | sarah 87, maid 84, vill_a 75, vill_b 62, vill_c 55, vill_d 64 | 612 | 248.7 | 8.1 |
| `barn_door` | 2.3 | 9.4 | 36.7 | sarah 104, jenner 52, vill_a 47 | 669 | 247.4 | 1.6 |
| `garden_hut` | 3.8 | 7.1 | 27.3 | boy 67, jenner 68, sarah 86, doctor 68 | 655 | 249.2 | 2.3 |
| `lane_wide` | 4.4 | 6.9 | 26.3 | doctor 56, villager_a 43, villager_b 82, villager_c 37, maid 64 | 649 | 259.3 | 2.8 |
| `lane_high` | 4.2 | 7.9 | 30.4 | c0 29, c1 28, c2 31, c3 30, c4 33, c5 32 | 735 | 254.7 | 2.6 |
| `garden_queue` | 4.2 | 7.2 | 27.6 | q0 78, q1 73, q2 68, q4 61, q6 55, jenner 47 | 696 | 248.6 | 1.7 |
| `room_day` | 0.8 | 7.1 | 27.4 | mother 132, boy_bed 72, jenner 113 | 583 | 242.2 | 1.5 |
| `room_night` | 0.6 | 7.8 | 30.2 | mother 128, boy_bed 72, doctor 150 | 580 | 249.8 | 3.3 |
| `room_morning` | 0.6 | 7.3 | 28.0 | boy 116, mother 163 | 668 | 243.2 | 1.5 |

Shade hue is the chroma-weighted mean hue of the shaded pixels (value 0.10..0.55, saturation > 0.2, blue >= red; target 240-260); magenta = share of chroma in the 290-345 deg band (target <= 10 %). Both are measured by `dairy_hue.py` on the finals (caption band excluded). `dairy_work/qa_tiles_log.txt`: no black / blank / magenta frames, Laplacian variance 200-820 (sharp), all chins above y 880.
`barn_high` has the highest magenta (8.1 %) because the amber low sun on warm timber sits against the violet shade; `lane_wide` is at the top of the hue band (259.3). Re-check with `python3 dairy_hue.py` after changing any light parameter (`PRESETS[p]['P']`: `shade`, `shade_tint`, `lift` move the hue; `lift` G is the strongest lever, `bounce` strength drives magenta on ceilings).

### How the shade is kept blue-violet (client rule)
The shade colour comes from `shade` / `shade_tint` with `shade_mix` 0.82-0.95 (the painted tint dominates, so brown timber and green grass shade to the same violet-blue), `lift` adds a little blue-green, and the warm bounce sun is only 5-7 % (a strong warm bounce on blue shade turns ceilings magenta). Rooms use brighter shade multipliers (`shade` x 1.6) so the interior does not go black.

## Known limits / open issues
- The barn roof (boards, purlins, thin rafters) still fills the top third of the wide barn frames: the structure is correct (no beams across the frame) but it is a large plank area; the lanterns, hanging onions / herbs and hay hanging over the loft edge break it up.
- Hay heaps on the loft are textured mounds with a fur of blades: they read as hay at phone size, but close up they look like soft clouds.
- Near-camera props look large by perspective (22 mm, vertical FOV 78 deg): the camera-relative dressing (`fg_props`) keeps them small and few; do not move a shot camera down into the floor dressing, or call `build()` with another preset camera and re-check the lower third.
- Hens, cats and the dog are low-poly stylised animals (smooth shaded); the cows are the detailed hero animals. Cats and the dog are static (hens, cows, lanterns animate).
- The `blossom` stand point is for the 2D puppet only; `stage_placeholders` adds a 3D cow marker (`blossom_marker_body`) for stills: delete it (and `D.T._clear_actors()` the cards) in real shots.
- The sun pool in `barn_high` (11 deg sun) is broken up by the dense floor props (long shadows): that is the late-amber look, but the pool is not one clean shape.
- `room_night` is amber / violet dusk through the windows plus a candle practical, not a pitch-dark night: it keeps the client's shade rules.
- Sheets on the washing line, curtains and the smoke are simple cards / billows (hard cartoon look, as in the style board).
- Cameras are fixed per preset (A['cams']); a moving camera needs its own checks of the foreground dressing.
