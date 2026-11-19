# v3/set3d16/telegraph.py : film 16 set ("ไอ้บ้าลวด", Samuel Morse's telegraph line, 1825-1845)

Real 3D Blender set (bpy 5.x, Cycles CPU), grown from the client-approved style board (`styleboard/sb.py`, board.jpg): warm low sun + blue-violet sky ambient outdoors, no post recolour (only the board's sat 1.08 compositor grade), warm cream / gilt / crimson chamber, painterly two-tone noise materials, dense props. **No depth of field anywhere. No text anywhere** (portraits are painted, the register tape has dots and dashes only).

Files: `telegraph.py` (API, lights, presets, hooks, render), `telegraph_kit.py` (builder, materials, wet group, props), `tg_line.py`, `tg_studio.py`, `tg_chamber.py` (locations), `telegraph_tex.py` (painted textures, cache `tex_telegraph/`), `tg_hue.py`, `make_contact.py` (+ `contact.jpg`, `contact_small.jpg`, `hue_report.txt`, `cost_report.txt`, `telegraph_work/final/*.png`), `t_anim.py` (hook test, prints ALL OK, 76 checks).

## Use (one process builds one location; as film8 Take / harbour.py)
```python
import telegraph as TG
A = TG.build(None, 'line_close', light='AFTER_RAIN')   # location comes from the preset; light optional; resets the scene
TG.setup_render(scene, 'final')                         # 720x1280, 'preview' 360x640; Cycles CPU, 6-7 spp + OIDN, no diffuse bounce, 2 threads
cam = TG.make_camera(A['cam'])                          # 22 mm, sensor 36, DOF OFF, clip 0.05..2000   (TG.apply_dof is a no-op)
act = TG.placeholder_actor('morse', A['marks']['morse_ladder'], face_to=cam.location)   # roles morse mocker cornell worker messenger clerk congress; HEIGHT dict
TG.clear_keys()      # removes every key the hooks made (objects, lights, nodes, groups, world, scene); keeps drivers (none used)
TG.STATE             # live dict: STATE['sun'], ['poles'], ['train'], ['marks'], ['light'] ...
```
Hooks key when `frame=n` is given (LINEAR; visibility keys are CONSTANT); without `frame` they set the value now. **Key every hook on every rendered frame** (once a hook is keyed an un-keyed call is overridden). `TG.render(path)` -> (wall s, cpu s). `TG.head_pixels(cam_name)`, `TG.stage_placeholders(A, cam_name, cam_loc)`. CLI: `python3 telegraph.py final|stills [preset[:LIGHT]]`.

## World
1 unit = 1 D = head, adult 3.0-3.4 D (`TG.HEIGHT`). Authoring in sb metres, **D = 1.85 x metres** (`SC`). Z up, ground z = 0.
**LINE** (the whole film-16 outdoors): the road, the rail and the pole line run along **world +x** (the sb1 camera looks along +x; camera-right = -y). Road centre y ~ -2.3 (x 0..260 D), poles 6.3 D right of... on the camera-right side (y ~ -9), railway track at y ~ +13, pole row x = 7.4 + 16.65 k (16 poles, k 0..15, 5 m = 9.25 D high, bottle neck 1.06 D). Furrow beside the road (x 3.7 .. 115 D, y ~ -6.4), spool/wagon/key crate at the furrow end (x ~ 100-121), station platform on the rail side x 63..115 (z 1.85), farm and barn far +x, trees ring, hills ring R 460-700 D. The cut-away **pit** (trench_cut) lies at (96, -22.2 .. ) in the field away from every other preset (mark `pit_ground`), ground has a real hole there.
**STUDIO**: room x -7.4..7.4, y -4.8..13 (+y into the room), height 8.9; tall window on the back wall (x -1.5), door in the right wall (x 7.4, y 5.7), outside: long road + rooftops far below, fields, hills.
**CHAMBER**: from sb2: back wall with 7 windows at y 63, tiers of desks around (0, 13), front table (0, 7.8), telegraph on it, crimson carpet, chandelier; new: speaker's panelled **door-screen** (doorway) behind the dais at y ~ 25 (Morse peeks there), the mocker's stool beside the register, hats/inkwells/quills on the desks.

## Presets (A['cams'][name] = {loc, look_at, lens}; default light)
LINE: `line_close`(AFTER_RAIN) `line_wide`(DAY) `line_rail`(DAY) `line_trench`(DAY) `line_trench_high`(DUSK/DAY) `line_trench_end`(DUSK) `trench_cut`(DUSK) `line_road`(DUSK) `line_wagon`(AFTER_RAIN). STUDIO: `studio_wide studio_easel studio_door studio_window` (DAY). CHAMBER: `chamber_wide_high chamber_low chamber_table` (DAY, NIGHT).
Preset cameras are start poses (22 mm); every preset carries 1-2 D foreground dressing (tall grass, crates, spool, coil, bottles, shovel / paint jars, canvases / an inkwell desk). Cameras are cheap to move; the set is dense in all directions (hills, trees, clouds ring).

## Lights (`build(..., light=)`, `TG.apply_light(name, frame=None)`, `TG.set_light_mix(a, b, k, frame=None)` keys sun, sky ramp, ambient, hills, clouds, exposure, lamps, wet)
LINE: **DAY** (sb1: warm key 24 deg, ambient #4454FF), **DUSK** (key 12 deg, orange, long shadows), **RAIN** (overcast, soft sun, grey-violet sky, wet 1, puddles on), **AFTER_RAIN** (sb3: key from the other side, wet 0.9, puddles). STUDIO: **DAY** (warm window key + blue-violet window fill). CHAMBER: **DAY** (sun shafts, chandelier + sconce candles) and **NIGHT** (only candles + desk candles, blue-violet moon key and window fill, shafts off). `set_light_mix('DAY','DUSK',k,frame)` is the shot 14 DAY->DUSK blend (all numbers interpolate). Sun, ambient and sky are the only light sources outdoors: shade is blue-violet from the ambient. **Wetness is separate and keyable**: `set_wet(k, frame)` (poles, wood, road, ground, grass darken and gloss; puddles appear above 0.35).

## Hooks (LINE)
- `set_poles(state, count=None, frame=None)`: `'none'|'bare'|'bottle'`, count 0..16 from the camera end. bottle = peg + inverted green bottle neck + wire over the neck; bare = wire on the wood. Birds sit on the wire.
- `set_ladder(on, pole=0|3, frame)`: ladder against pole 0 (hero, line_close) / pole 3.
- `set_trench(k, plough=None, frame)`: furrow length 0..1 (shader clip, smooth). The plough (beam, share, handles, whiffletree + traces) stands at the front (plough=None), a float puts it elsewhere, False hides it; hidden at k 0 and 1. `TG.plough_marks(k)` -> marks mule_a, mule_b, cornell, worker_a, worker_b, morse_trench that follow it.
- `set_pipe(k, frame)`: grey lead pipe laid in the furrow 0..1 (clip) + pipe reel on a cart at its front while 0<k<1.
- `set_train(x, frame=None, speed=None)`: x = world x of the loco's front buffer (D); `'home'` = sb1 spot; None hides. The train runs toward **-x** (toward the sb1 camera): wheels roll with the distance, connecting rods turn, 10 smoke puffs billow and trail (speed from the previous call).
- `set_rain(on, frame)`: bool or 0..1 (layers); three depth layers of real streak geometry (5200 faces) that follow the camera and fall every frame (key per frame). Pair with light RAIN (wet, puddles).
- `set_leak(where, intensity, frame)`: `'pipe'` (16 blue spark beads leaking from the torn cloth of the opened pit pipe into the soil, trench_cut) | `'pole'` (14 beads crawling down the wet wood of poles 0 and 1). Phase follows the frame: key per frame.
- `set_pulse(s, frame)`: glowing bead + 6-bead trail along the whole wire, s 0..1 (path follows the current pole state: over every bottle neck, or the bare wire); s < 0 hides it.
- `set_buggy(x, frame)`: open 1840s buggy on the road at world x (D), wheels turn; None hides. `TG.buggy_marks(y_m)`.
- wagon with the crate of 15 empty green beer bottles (+ spool + key crate), ladder, key + register crate at the furrow end, coil, station platform: static props (marks below).
## Hooks (STUDIO) `tg_studio.set_door(k, frame)` (0..1), `set_palette(on, frame)` (palette + brush on the floor, mark palette_floor).
## Hooks (CHAMBER) in `tg_chamber` (import as CH): `set_tape(len 0..1, clicking=None, frame)` paper strip (dots / dashes only) out of the register, over the table edge, looping round the mocker's stool; `set_click(on 0..1, frame)` armature lever; `set_moneybag(on, frame, lift=0.0)` (lift = D above the table, key a bounce); `set_mailsacks(on, frame)` (10 sacks round mark mocker_post); `set_flames(level, frame)` candle flicker (call per frame); `set_shafts(on, frame)`.

## Stand points (A['marks'][name] = (x, y, ground z in D); z > 0 = a raised floor: ladder, wagon bed, platform, desk tier, dais)
LINE: morse_ladder (6.4 up the ladder, shot 1/23), morse_ladder_foot, morse_ladder3, morse_wire, morse_pole, morse_key + worker_key_a/b/c (furrow end crate), morse_wagon_key (wagon bed z 1.85), morse_wagon_bed, worker_wagon, morse_bottle (beside the wagon crate), platform_a..d (z 1.85), plough, mule_a, mule_b, cornell, worker_a, worker_b, morse_trench (for furrow k = 0.5; `plough_marks(k)` for others), mocker_buggy (seat, z 1.76) + mule_buggy (`buggy_marks`), pit_ground.
STUDIO: morse_easel, morse_stool (seat height 1.04 D: `tg_studio.SEAT`), morse_window, morse_door, messenger_door, palette_floor.
CHAMBER: morse_table, clerk_table, mocker_table, mocker_stool (seat 1.04 D), mocker_desk (= mocker_post, front-row desk, z 0), cong_a..e (desks, tiers 0-2), morse_door (door-screen), table_front, dais (z 0.74).

## Render cost (final 720x1280, CPU s of the render call, two workers in parallel, 2 threads each; build ~6 s studio/chamber, ~20 s line, once per process)
LINE 11.6-13.5 (line_close) / 17-21 (wide, rail, trench, road, wagon, cut) / 24.6 (trench_end + rain); STUDIO 17.8-19.3 (6 spp); CHAMBER 20.7-27.6 (6 spp; chamber_low DAY 27.6 is the maximum). Per-tile numbers in cost_report.txt. Settings: no light tree, max bounces 2, no diffuse bounce (chamber/studio fills are shadow-less area lights), denoise OIDN FAST. `use_persistent_data` can cut ~5 s on moving-camera takes. Samples per preset: `TG.FINAL_SAMPLES`.

## Colour (hue_report.txt, method of styleboard/hue_check.py: cast-shadow pixels from a sun-only render)
Outdoor tiles: shade hue 202-275 (target 240-260, DAY wide 254), magenta share 1.0-8.7 % (limit 10 %). Indoor tiles: n/a (warm shade by design, magenta < 1 %).
