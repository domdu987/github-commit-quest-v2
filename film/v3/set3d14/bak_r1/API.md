# v3/set3d14/farm.py : film 14 set ("ไอ้บ้าผึ้ง", beehive fence, Kenyan smallholding) (bpy 5.x, Cycles CPU)

Files: `farm.py` (set, hooks, presets, cameras, stand points, placeholders, CLI), `farm_geo.py` (materials, numpy mesh builder `MB`, every prop), `make_contact.py`, `farm_hue.py`,
`contact.jpg` / `contact_small.jpg` (16 tiles, 720x1280 each, label under the tile, cyan line at y 880), `farm_work/` (`final/` the 16 PNGs, `final_log.txt`, `hue_rows.txt`, `contact_order.txt`, `stills/`), `tex/` (ground mask, placeholder card art), `styleboard/` (the approved board).
Grown from `styleboard/sb.py`: same palette, same hard warm key + blue-violet ambient, painterly noise materials, red laterite, blue Mt Kenya. **No depth of field. No text in any picture.** Build takes about 4 s.

## Round 2 changes (QA-tech FAIL / QA-art FIX-FIRST). Backup of round 1: `bak_r0/`.
- Push point moved to the front row x 6.0 (arc 20.0); wave speed 11 m/s, bow 1.6 m, hive swing up to 0.9 rad; wire radius is per preset (`wire_r`: default 4.6 cm, push_side 7.5, trunk_close 6, fence_ring 12).
- Bees: 45 per hive end (4 x 16 hives = 1440 max), sized by distance to the camera (7 cm near, 17 cm at 17 m) so they read as bees; 14 resting bees per end when asleep; wings smaller. **Call `set_bees` after the camera exists/moves** (the CLI does).
- New presets `hook_close`, `fence_ring`, `yard_crowd`, `uncle_nose_close`; old ones re-framed with actors 3.7-5 m away, grass culled near cameras (tufts only beyond 4.6 m from the camera, shorter blades, no flowers within 6 m), yard clutter moved behind/left of the cameras, no goat at NIGHT, no fire pit in front of the matriarch (yard fire now at x -10.4), tin-sheet slab removed, uncle's fire unlit in the morning.
- Uncle field: 78 % of stalks torn out/eaten (97 % along the three herd tracks), the rest flat in green-brown (`maizefall`), deep round footprints (dark pit + raised rim, 0.4 m), mud patches (soft colour), dung heaps, half of the thorn piles thrown aside.
- Night: sky gradient (light horizon, deep zenith), stars brighter, the moon is put 22 deg left of the camera azimuth at 24 deg elevation so it is in frame (key follows it).
- Shade: a shadow-tint grade in `render()` (dark pixels desaturated then pushed to hue about 245, `shade_tint` 0.9 DAY/MORNING, 0.5 DUSK) plus a violet-blue zenith; the measured shade hue is now 233-272 on DAY/MORNING (see Hue).

## World
METRES (not D). +x right, +y away from the camera rig, z up, floor z 0. Camera 22 mm / 36 mm sensor (fit AUTO on the 1280 side, focal length 782 px), 720x1280.
- **Hero field** x -13..10, y 5.9..25 (about 1000 maize plants, rows run along y). **The fence ring** is a rectangle x -14..11, y 5..25.5 (outside = away from the field), wire at z 2.0 (sags to 1.9), cream-coloured, 7.6 cm thick (cartoon-thick so it reads at 50 m).
  16 hive units: front row 5 (x -11.5, -6.5, -1.5, 3.5, 8.5), right side 3, back 5, left 3. Each unit = 2 posts 2 m apart, corrugated-tin pitched roof with real ribs and a warm planked underside, a top-bar hive hanging 0.68 m under the wire from a hanging bar the wire runs through. Extra posts keep every free span under 3.7 m.
  Wire length 91 m = ONE continuous closed polyline through every bar.
- **Hero yard** (front, y -3..4): jerrycans, stools, bench, baskets of cobs, hoes, spare hives, tin sheets, wire spools, ladder on the fence, wheelbarrow, sacks, pots, fire pit (1.3, 0.5), lantern pole (4.9, 2.6), chickens, goats (not at NIGHT), kale rows, sunflowers, pumpkins, papayas.
- **Village** x 14..46, y 0..32: 4 round huts, 2 tin-roof houses, 2 granaries, coop, boma with goats, cooking fire, benches, washing lines, water tank, bicycle, wheelbarrow, firewood, banana, acacias, red paths.
- **Uncle's farm** x -47..-21, y 5..26 (thorn-branch fence, tin cans on strings, house + hut + granary behind, yard with fire pit). **Savanna** to y 120: acacias, scrub, termite mounds, rocks, giraffes (DAY/MORNING), cartoon clouds, birds, hills, Mt Kenya-like mountain.

## Functions
```python
import sys; sys.path.insert(0, ".../v3/set3d14"); import farm as F
A = F.build('push_side', 'NIGHT')      # build(preset=None, light=None, clear=True, dress=True) -> anchors dict (cams, stand, heights, units, wire ...)
cam = F.make_camera(A['cams']['push_side'])      # dict(loc, look_at, lens); clip 0.05..3000, DOF off
F.setup_render(scene, 'final' | 'preview')       # 720x1280 / 360x640, 24 / 14 samples, 4 threads, OIDN, Standard view
F.apply_state('fs3,wp0.35,bees0.35')             # CLI state tokens (below)
F.stage_placeholders(preset, cam_loc, state)     # placeholder cards at the preset's stand points, facing cam_loc (yaw only)
F.place_actor(role, F.STAND['hero_yard'], face_to=cam_loc, name='actor_hero')   # one card; roles = F.HEIGHT keys
F.head_pixels(preset, state); F.render(path) -> (wall s, cpu s)   # render applies the light-state grade
```
Hooks are **immediate**: call them before every frame you render (no `frame=` keys). Calling order is free; each hook rebuilds what it needs.

| hook | what it does |
|---|---|
| `set_fence_stage(k)` | 0 posts only (all 16 post pairs, no roofs, no wire), 1 one hive (unit 1, front row x -6.5) on its own short wire, 2 ten hives (units 1,0,2..9: the whole front, the right side, 2 of the back), 3 all 16 hives + the continuous wire ring. |
| `set_wire_push(t, point=None)` | t 0..1 spans 5 s (`F.SEQ_T`). t < 0 = at rest. The push point is the front row x 6.0 (arc length 20.0, mid-span between units 3 and 4). The wire bows in 1.6 m over 0.55 s, then rings down (1.1 Hz, damped 1.5 s); the wave **travels outward in both directions round the ring at 11 m/s** (amplitude falls with exp(-d/45)). Every hive swings about the wire (up to 0.9 rad) and twists, with the same phase delay; posts pin the wire (35 % motion). Rest pose is exact at t < 0. |
| `set_bees(t, burst=1.0, target=None, local=None)` | t < 0: asleep (5 bees per hive end, silent). t 0..1 (same clock as the push): each hive end releases a cloud when the wave reaches it (45 bees per end, 1440 at most): they rise, orbit and spread. `burst` 0..1 = share shown. `target=(x,y,z)`: the swarms stream toward it (use `F.MATRIARCH_EYE`). `local=((x,y,z), radius, n)`: extra cloud round a point (the elephant's head). Bees are 7.5 cm gold/black spindles with wing triangles, rebuilt per call; no shadows. Call again every frame (call `set_wire_push` first; it re-poses the bees' hives). |
| `set_uncle_field(k)` | 0 intact. 1 trampled: stalks fall (each at its own threshold, so 0..1 can be keyed as the herd passes), 70 % torn out or eaten, dry colour, thorn fence broken, tin-can strings down, mud patches, 54 big footprints, dung heaps, chewed cobs. |
| `set_uncle_hive(k)` | the uncle's own hive on his fence (x -23, y 5): 0 none, 0..1 lifted from hand height to its hook, 1 hung. |
| `set_crowd_props(k)` | villagers' lit torches (with point lights) and banged pots at the villager stand points. 0/1. |

CLI state tokens (`state` of a spec): `fs<k> wp<t> bees<t>[/<burst>] btgt bloc uf<k> uh<k> cr<k>`. `btgt` = stream to the matriarch's eyes, `bloc` = local cloud at her head.

## Light states (`build(..., light=)`, any preset with any light)
| light | key (sun/moon) | sky / ambient | in frame |
|---|---|---|---|
| DAY | warm gold 4.6, el 27, az -60 (behind-left) | peach horizon, violet-blue zenith (ambient 1.45) | cartoon clouds, birds, giraffes, cooking fire dim |
| MORNING | pale gold 4.2, el 17, az +64 (behind-right) | pale peach to lilac | fires lit |
| DUSK | deep orange 3.4, el 8, az -115 | magenta-orange horizon, indigo zenith | window glows, fire, lantern, torches |
| NIGHT | cool moon 3.2, el 27, az -32, moon disc, stars | indigo, bright ambient (2.0) | warm fire pits, lantern, windows, torches; animals asleep |
A soft shadow-less warm ground-bounce area light lights roof undersides and walls (the style board's blotchy dark undersides are gone: the underside material also carries its own warm bounce).

## Presets (`F.PRESETS`, cameras `F.CAMS`, 22 mm unless noted; 14 presets)
| preset | default light, state | camera loc -> look | what it shows |
|---|---|---|---|
| `hook_close` | DAY fs1 | (-5.2,-2.7,1.5) -> (-3.9,4,1.15), 20 mm | hero on the ladder hanging the hive on unit 1, laughing villagers 3-5 m in front |
| `village_wide` | DAY fs3 | (3,-10.5,5.2) -> (14,12,1), 20 mm | wide: field + ring, huts, mountain |
| `fence_line` | DAY fs1 | (-9.9,0.9,1.45) -> (-5.7,5,1.25) | aimed at unit 1: the one hive centred (fs0 posts, fs1 one hive) |
| `fence_ring` | DAY fs3 | (-1.5,-14.5,18) -> (-1.5,15,0), 20 mm | high over the yard: whole ring, 10 hives (fs2) vs 16 + wire (fs3) countable; wire 12 cm here |
| `hive_close` | DUSK fs3, bees asleep | (-9.7,2.4,1.2) -> (-5.2,5,1.45), 24 mm | one hive on the wire, wire receding |
| `yard_two_shot` | DAY fs3 | (-2.1,-2.5,1.4) -> (-2.1,1.5,0.7) | hero + uncle, heads 125 px, unit 2 behind them, clear ground at their feet |
| `yard_crowd` | DUSK fs3, cr1 | (-2.2,-4.4,1.45) -> (-2.2,2,0.85) | uncle + 5 villagers with torches and pots |
| `field_night_wide` | NIGHT fs3 | (-4,-13.5,9) -> (-0.5,10,0.8) | herd turned 55-70 deg toward the fence (yaw offsets), moon key |
| `fence_low_night` | NIGHT fs3 | (3.4,-4.4,1.15) -> (-1.3,2.4,1.3) | matriarch arriving, moon in frame, no fire behind her |
| `push_side` | NIGHT, wp0.35 + bees, wire 7.5 cm | (12.5,-2.2,3.4) -> (-2.2,7.5,0.2), 26 mm | 3/4 along the front wire from the right: matriarch at the near end (push point x 6.0), 6+ hives receding left |
| `trunk_close` | NIGHT, wp0.5, bees + `bloc` + `btgt` | (5.2,0.2,1.5) -> (6.9,4.3,1.4), 28 mm | whole head + trunk, swarm at eye and trunk |
| `uncle_field_morning` | MORNING uf1 | (-27,-3.5,4.8) -> (-33.5,14,0) | raised view: flat green-brown stalks, deep round footprints, broken thorn fence, cobs, no fire |
| `uncle_hang` | MORNING uf1 uh1 | (-20.4,-1.2,1.5) -> (-22.4,2.4,1.5) | uncle standing ON his stool (stand z 0.46 = stool seat) hanging his hive |
| `uncle_nose_close` | MORNING uf1 uh1 | (-23.4,1.1,2.0) -> (-22.2,2.7,2.15) | uncle on the stool, head about 275 px, hive roof above-left (the nose beat) |

## Stand points and heights (`F.STAND`, `F.HEIGHT`, metres; card bottom = feet at the stand z)
`HEIGHT`: hero 1.75, uncle 1.72, woman 1.62, kid 1.15, oldman 1.6, man 1.75, matriarch 3.3, elephant_b 2.84, elephant_c 3.07, elephant_d 2.54, calf 1.2 (the real cast14 sizes; 1 D = 0.583 m).
People placeholders now have the cast's proportions (head = 1/3 of the height). Elephant placeholder cards are the size of the REAL cast14 canvas (matriarch 26.4 x 5.4 m, others scaled by height/3.3; body in the middle, facing +x), so occlusion and shadow extents match. `head_pixels` uses chin = 0.67 H (people) / 0.62 H (elephants).
`hero_yard (-3,1.2)`, `uncle_yard (-1.2,1.2)`, `hero_hive (-6.6,3.2)`, `hero_ladder (-6,4,z 1.25)` (on the ladder under unit 1), `hero_fence`, `hero_proud`, `uncle_night (-2.4,2.6)`, `crowd_a..e` (yard crowd), `villager_woman/kid/oldman/woman2/man` (hook crowd, y 1-2.4),
`matriarch_push (5.4,4.3)` (chest at the wire, push point x 6.0), `matriarch_arrive (-0.6,2.3)`, `ele_2/3/4`, `calf`, `herd_a..d`, `herd_calf` (staging entries may carry a 3rd value = yaw offset in degrees), `uncle_stool (-22.4,2.4,z 0.46)` (the stool prop sits under it), `uncle_field`, `uncle_fence_hive`.
Cards: `place_actor(role, mark, face_to, name, yaw_off)`; NIGHT card brightness 0.72. The ground within 1.9 m of every staged stand point and 4.8 m of the preset camera is cleared of grass and flowers (the scatter is built for the ACTIVE preset only).

## CLI
`python3 farm.py final|stills [spec ...]`, spec = `preset[:LIGHT[:state[:camera]]]` (no spec = every preset at its default). Output `farm_work/final/` or `farm_work/stills/`, file `<camera>_<LIGHT>[_<state>].png`. ACTORS=0 skips the placeholders. `python3 farm.py digest [preset]`.
Contact sheet: edit `farm_work/contact_order.txt` (spec|label), render the specs, `python3 make_contact.py`. Hue: `python3 farm_hue.py farm_work/final` (writes the rows in `farm_work/hue_rows.txt`).

## Render cost (720x1280 final, 24 samples, OIDN, 4 threads, nothing else running)
Wall 25-41 s per frame (mean 33 s), 95-153 CPU s; build 3 s extra per process. Slowest: `hive_close` 40.7 s, `uncle_field_morning` 40.2 s, `field_night_wide` 39.6 s. Previews (360x640, 14 samples): 5-8 s.

## Hue (tools/hue_report.py, farm_hue.py; `farm_work/hue_rows.txt`, 18 tiles)
Magenta: max 6.1 % (village_wide DUSK), everything else 0.3-5.2 %; **all tiles under 10 %**.
Shade hue (blue>=red shaded pixels, shaded fraction 1-18 %): in band 240-260: fence_low_night 241.1, field_night_wide 241.7, hive_close 258.9, hook_close 250.9, push_side x2 244.0, uncle_field_morning 258.5, uncle_hang 248.4, uncle_nose_close 252.6, village_wide DUSK 250.1, yard_two_shot 253.1.
Out of band: fence_line fs0/fs1 267.0/264.4, fence_ring fs2/fs3 269.4/271.9, village_wide DAY 233.1, trunk_close 238.9, yard_crowd 232.5 (the blue placeholder dresses count as shade pixels). DAY frames still only have about 1-2 % measurable shade (shade on red laterite is desaturated violet-grey after the tint, not strongly blue).
Light groups: DAY red 43 / orange 41 / blue 6 %, MORNING 29 / 47 / 9, DUSK 53 / 33 / 7, NIGHT blue 58 %, saturation 0.39-0.58.

## Known weak points
- Shade hue is out of band on the DAY fence tiles (264-272) and village_wide DAY (233); the metric counts few pixels there.
- hook_close: villagers are 80-95 px head height, the hero on the ladder only 65 px (he is 6.5 m away); fence_line hero head 114 px.
- Low presets are now clear red earth in the bottom 35 %: clean for the cast, but bare compared with round 1. Foreground detail can be added at the frame edges.
- Placeholder cards are flat; the trampled field's footprints read as round pits/donuts; push_side bees and the wire bow read, but the wire is a thick cartoon line (7.5 cm).
- No 6-frame shimmer test was run this round (thicker wire, fewer wider blades, no flower dots within 6 m were used to reduce it).
