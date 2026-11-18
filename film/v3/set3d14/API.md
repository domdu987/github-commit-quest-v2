# v3/set3d14/farm.py : film 14 set ("ไอ้บ้าผึ้ง", beehive fence, Kenyan smallholding) (bpy 5.x, Cycles CPU)

Files: `farm.py` (set, hooks, presets, cameras, stand points, placeholders, CLI), `farm_geo.py` (materials, numpy mesh builder `MB`, every prop), `make_contact.py`, `farm_hue.py`,
`contact.jpg` / `contact_small.jpg` (16 tiles, 720x1280 each, label under the tile, cyan line at y 880), `farm_work/` (`final/` the 16 PNGs, `final_log.txt`, `hue_rows.txt`, `contact_order.txt`, `stills/`), `tex/` (ground mask, placeholder card art), `styleboard/` (the approved board).
Grown from `styleboard/sb.py`: same palette, same hard warm key + blue-violet ambient, painterly noise materials, red laterite, blue Mt Kenya. **No depth of field. No text in any picture.** Build takes about 4 s.

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
| `set_wire_push(t, point=None)` | t 0..1 spans 5 s (`F.SEQ_T`). t < 0 = at rest. The push point is the front row x 1.0 (arc length 15.0, mid-span between units 2 and 3). The wire bows in 1.3 m over 0.55 s, then rings down (1.1 Hz, damped 1.3 s); the wave **travels outward in both directions round the ring at 15 m/s** (amplitude falls with exp(-d/45)). Every hive swings about the wire (up to 0.72 rad) and twists, with the same phase delay; posts pin the wire (35 % motion). Rest pose is exact at t < 0. |
| `set_bees(t, burst=1.0, target=None, local=None)` | t < 0: asleep (5 bees per hive end, silent). t 0..1 (same clock as the push): each hive end releases a cloud when the wave reaches it (about 150 bees per end, 4800 at most): they rise, orbit and spread. `burst` 0..1 = share shown. `target=(x,y,z)`: the swarms stream toward it (use `F.MATRIARCH_EYE`). `local=((x,y,z), radius, n)`: extra cloud round a point (the elephant's head). Bees are 7.5 cm gold/black spindles with wing triangles, rebuilt per call; no shadows. Call again every frame (call `set_wire_push` first; it re-poses the bees' hives). |
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

## Presets (`F.PRESETS`, cameras `F.CAMS`, 22 mm unless noted)
| preset | default light, state | camera loc -> look | what it shows |
|---|---|---|---|
| `village_wide` | DAY fs3 | (-6,-17,6.5) -> (10,7,0.2), 20 mm | high wide: field + fence ring, huts, mountain (stage 1 for the hook) |
| `fence_line` | DAY fs3 | (-16.5,1.7,1.6) -> (3,5.3,0.95) | eye level along the hive fence (fs0..fs3) |
| `hive_close` | DUSK fs3, bees asleep | (-9.7,2.4,1.2) -> (-5.2,5,1.45), 24 mm | one hive on the wire, wire receding |
| `yard_two_shot` | DAY fs3 | (-2.4,-3.7,1.5) -> (-1.9,3,0.75) | hero + uncle in the yard (DUSK + `cr1` = crowd) |
| `field_night_wide` | NIGHT fs3 | (-4,-13.5,9) -> (-0.5,10,0.8) | herd outside the ring |
| `fence_low_night` | NIGHT fs3 | (4.8,-3.2,1.1) -> (-1,5,1.7) | matriarch arriving, moon |
| `push_side` | NIGHT, wp0.35 + bees | (-9,-0.9,2.2) -> (1.5,5,0.8) | the push and the travelling wave |
| `trunk_close` | NIGHT, wp0.5, bees + `bloc` | (-0.4,-1,2.3) -> (2,4.2,1.2), 28 mm | head, bees at eyes and trunk |
| `uncle_field_morning` | MORNING uf1 | (-26,-2.2,2.6) -> (-33,12,0.3) | the trampled field |
| `uncle_hang` | MORNING uf1 uh1 | (-20,-1,1.4) -> (-22.6,4,1.5) | uncle on his stool, hanging his hive |

## Stand points and heights (`F.STAND`, `F.HEIGHT`, metres; card bottom = feet, cards face the camera in yaw)
hero 1.75, uncle 1.72, woman 1.62, kid 1.15, oldman 1.6, man 1.75, matriarch 3.3 (card 4.95 wide, side view facing +x, eye about x+1.5, z 1.9), elephant 3.0, calf 1.5.
`hero_yard (-3.4,1)`, `hero_fence (-8.8,3.4)`, `hero_hive (-6.5,3.6)`, `hero_proud (-1.2,2.4)`, `uncle_yard (-0.4,0.5)`, `uncle_night (3.6,1.2)`, `villager_woman (-7,0.2)`, `villager_kid (-5.6,-0.6)`, `villager_oldman (-4.2,0)`, `villager_woman2 (-1.6,-0.3)`, `villager_man (1.8,-0.5)`,
`matriarch_push (0.4,4.3)` (chest at the wire, x 1.0), `matriarch_arrive (-0.2,0.3)`, `ele_2 (-6.2,2)`, `ele_3 (6.4,1.4)`, `ele_4 (-11,0.6)`, `calf (-3.2,-0.8)`, `herd_a..d`, `herd_calf`, `uncle_stool (-22.4,2.4)`, `uncle_field (-27,1.2)`, `uncle_fence_hive (-23,5)`.
Placeholder cards are flat plum-outlined PIL puppets (`tex/card_<role>.png`), emission-only with shadows; `P['card_k']` dims them per light (NIGHT 0.72). Heads/chins stay above y 880 (printed by the CLI as `heads`).

## CLI
`python3 farm.py final|stills [spec ...]`, spec = `preset[:LIGHT[:state[:camera]]]` (no spec = every preset at its default). Output `farm_work/final/` or `farm_work/stills/`, file `<camera>_<LIGHT>[_<state>].png`. ACTORS=0 skips the placeholders. `python3 farm.py digest [preset]`.
Contact sheet: edit `farm_work/contact_order.txt` (spec|label), render the specs, `python3 make_contact.py`. Hue: `python3 farm_hue.py farm_work/final` (writes the rows in `farm_work/hue_rows.txt`).

## Render cost (720x1280 final, 24 samples, OIDN, 4 threads, nothing else running)
Wall 29-43 s per frame (mean 34 s), 111-173 CPU s; build 3-4 s extra per process. Slowest: `hive_close` 42.9 s (dense foreground grass), `uncle_field_morning` 41.7 s. Previews (360x640, 14 samples): 5-8 s. Samples are the lever: 16 samples is about 22 s.

## Hue (tools/hue_report.py, farm_hue.py; `farm_work/hue_rows.txt`)
Magenta share: max 7.7 % (village_wide DUSK), all other frames 0-5 %: **every tile is under the 10 % limit**. By light: DAY 0.1 %, MORNING 0.2 %, NIGHT 0.7 %, DUSK 5.2 %.
Shade hue (blue>=red shaded pixels): NIGHT tiles 239.5-244 (the four push/low/wide tiles OK, `trunk_close` 239.5), DUSK 247.9-260.3, MORNING 239.5-255. **DAY exteriors do not measure**: the shaded fraction is about 0 % (shade on red laterite is dark red-brown, not b>=r, so the metric sees only a handful of sky-edge pixels: 222-272). The ambient itself is violet-blue (zenith hue about 235-245).
Whole-set band: red+orange 54-78 %, blue 4-6 % in DAY (out of band: this is a warm red-earth exterior), NIGHT blue 60 %, saturation 0.52-0.66, dark 5-22 %.

## Known weak points
- DAY/MORNING shade is warm, not blue-violet (see above); DAY blue is only 4 % (the sky is peach, the board's look).
- The uncle's trampled field still reads as a lumpy dry mat from low views more than as flattened stalks; footprints are best seen from higher cameras.
- `push_side`: the wave is visible but small (the fence is 12-30 m away); a closer or higher camera along the row shows it better. The wire is the thinnest read in `village_wide`.
- Fence tiles `fence_line` show 30 % sky; `fence_low_night` / `trunk_close` have a flat violet sky (stars are tiny).
- Placeholder elephants are flat lilac cards; real cards will need a shadow look test against the grass.
- Foreground grass is dense by design; it can hide actor feet at low cameras (stand points are in clear patches).
