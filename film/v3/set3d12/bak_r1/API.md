# v3/set3d12/street.py : film 12 set ("ไอ้ร่มเดินได้", a Georgian London street in the rain, 1750s) (bpy 5.x, Cycles CPU)

Read only this file. Everything lives in `film/v3/set3d12/`:
- `street.py`: the whole set, every hook, presets, cameras, stand points, CLI. `street_parts.py`: horse, hackney coach, wheel, crowd figure, umbrella geometry. `street_tex.py`: all artwork (numpy / PIL, cached in `tex_street/`, bump `TEX_V` after editing a painter).
- `street_hue.py`: shade hue + magenta share per frame. `street_work/`: `t_anim.py` (hook test, prints ALL OK), `render_tiles.py` + `make_contact.py` (the contact sheet), `final/` (the 20 finals), `final_log.txt`, `hue_rows.txt`.
- `contact.jpg` (5 columns of 720x1280 tiles, label under each, cyan line at y 880) and `contact_small.jpg` (1/3). `styleboard/` = the client-approved board. Backup of the board build: `bak_r0/`.

Style (client-approved, do not change): warm amber lit windows vs blue-violet rain shade, one hard warm key from the left-behind, dense terraces, wet setts with layered puddles, crisp cartoon clouds, sharp image, NO depth of field, NO text or letters anywhere (signs are pictures).

## 1. Quick start
```python
import sys; sys.path.insert(0, '/abs/path/film/v3/set3d12')
import street as S, bpy
A = S.shot('box_seat', 'RAIN', placeholders=False)      # build + camera + rain + halos + lights.  placeholders=True stages grey-ish cards at the stand points
S.key_camera('box_seat', 1, 60)                          # camera move A -> B between frames 1 and 60
S.set_pink_umbrella(0, frame=100); S.set_pink_umbrella(1, frame=106)
sc = bpy.context.scene
for f in range(1, 61):
    sc.frame_set(f)                                      # REQUIRED for keyed hooks, rain and rolling wheels (drivers read the frame)
    S.render('/abs/out/f%04d.png' % f)                   # 720x1280 PNG, compositor grade included
```
- `S.shot(preset, light='RAIN', u=0.0, placeholders=True, figures=False, quality='final')` -> anchors dict `A` (keys below). `u` 0..1 places the camera between pose A and pose B. One `shot()` per take (it rebuilds the whole scene, 2-8 s); then animate with the hooks. Changing preset or light = a new `shot()`.
- CLI: `python3 street.py final [preset ...] [RAIN|DUSK_RAIN]` (720x1280 -> `street_work/final/<preset>_<LIGHT>_final.png`), `python3 street.py stills ...` (360x640, 6 samples, ~3 s). `THREADS=2 SAMPLES=14` environment variables are honoured (default 2 threads, 14 samples, OIDN denoise).
- Units: 1 unit = 1 head. Adults 3.0-3.2 units. z up, street along +y, the camera looks mostly toward +y (the far end of the street). 30 fps; hooks take frame numbers `g = round(t*30)`.

## 2. World
- Roadway x -5.9..5.9 (z 0), gutters (running water) along both kerbs, kerbs, pavements x +-6.3..9.8 (z 0.28), house fronts x = +-9.8 (22 lots of 8 units each side, y -56..120), cornices z 19.35, roofs and chimneys above, a closed terrace at the far end (y 120), a cross lane on the left at y 40..48.
- Right row (x > 0) is in the warm key, the left row in blue shade. Lamp posts every 16 units on alternate sides (lit lanterns + halos + real point lights near the shot).
- Facades: 16 painted brick types (10 houses with fanlight / transom / arched doors, porticos, hoods, iron balconies, area railings; 6 shops with bow windows full of goods: boots, teapots, pretzels, greens, tricorn hats, chemist jars) with pictorial hanging signs (boot, teapot, pretzel, hat, jar: no letters) and striped awnings.
- **Market corner** on the left pavement (x -9.5..-7, y 3..19): stall with awning, trestle table with produce, two barrows, baskets, sacks.
- **Coach rank** on the right kerb: 4 hackney coaches `coach_0..coach_3` at x 3.55, y 22 / 38.5 / 55 / 71.5, facing -y (toward the camera of street_wide), each with a horse in the shafts, plus the running coach `coach_run` parked at y 140 (see `run_coach`). Water troughs between them.
- Puddles: ~60 layered decals (soft dark wet halo, shallow film with a pale shore line, deeper core, ripple rings). The big one for the mud splash is at (-1.7, 12.4) r 3.3. Gully gratings at the kerbs.

## 3. Presets, cameras (22 mm, 720x1280, no DOF)
Camera name `cam` (the scene camera). `S.CAMS[preset]` has `loc, look_at, loc_b, look_b, lens`; `S.camera_pose(preset, u)` interpolates (smoothstep); `S.key_camera(preset, f0, f1)` keys A at f0 and B at f1. Rain and halos follow `cam` (parented / constrained). **Use `S.make_camera(setup)` (same object `cam`) for your own moves; do not create another camera object** or the rain stays behind.

| preset | pose A (loc -> look_at) | pose B (loc -> look_at) | shot plan use |
|---|---|---|---|
| `street_wide` | (1.0, -14.0, 3.4) -> (0.3, 40.0, 3.2) | (0.6, -4.0, 3.3) -> (0.3, 40.0, 3.5) |
| `street_high` | (-3.0, -20.0, 32.0) -> (0.5, 34.0, 1.0) | (-2.0, -9.0, 17.0) -> (0.5, 32.0, 2.0) |
| `coach_low` | (-3.6, 4.2, 1.35) -> (3.6, 19.0, 3.3) | (-1.0, 7.5, 1.5) -> (3.55, 19.5, 3.9) |
| `hero_track` | (-3.8, 0.4, 2.2) -> (-0.6, 8.0, 3.3) | (-3.6, 10.2, 2.2) -> (-0.6, 17.8, 3.3) |
| `box_seat` | (-1.6, 10.0, 1.5) -> (3.2, 18.6, 5.9) | (0.2, 12.4, 2.3) -> (3.4, 18.6, 6.3) |
| `market` | (0.4, 0.4, 2.0) -> (-6.0, 11.0, 2.9) | (-0.8, 3.0, 2.1) -> (-6.4, 11.5, 3.0) |
| `puddle_low` | (-5.3, 3.6, 0.75) -> (-1.8, 12.6, 2.0) | (-5.3, 4.6, 0.7) -> (-2.2, 12.6, 2.2) |
| `rank_rush` | (-3.4, 4.0, 3.0) -> (3.4, 28.0, 3.4) | (-3.4, 10.0, 3.6) -> (3.4, 36.0, 3.4) |

| preset | what it shows | plan shots |
|---|---|---|
| `street_wide` | eye level (3.4) down the whole street, rank far right, push in to B | 1, 9, 19, 20 (reverse: build a reverse pose yourself with `make_camera`) |
| `street_high` | crane from 32 (A) down to 17 (B): roofs, chimneys, the whole street | 4, 13, 21 |
| `coach_low` | low (1.35) at the rank, the box seats up in frame, the head coach centre | 2, 7, 15, 22 |
| `hero_track` | medium along the left of the crown following the hero (his walk `hanway_b` -> `hanway_c`), rank behind right | 3, 11, 18 |
| `box_seat` | low angle up at the head coachman on his box (`box_a`), horse chest lower right | 6, 8, 14, 23 |
| `market` | eye level at the barrow / stall corner on the left pavement, road with puddles in front | 5, 10 |
| `puddle_low` | 0.75 above the road: big puddle, gutter and grating in the foreground, the coach crossing and the splash target `hanway_mud` | 12 |
| `rank_rush` | the rank from the road, crowd runs to the doors | 16, 17 |

`S.project_px(cam, (x, y, z)) -> (px_x, px_y, depth)` gives the 720x1280 pixel of a world point (use it for the head check: every head must be above y 880; all staged heads below are, at both poses where listed).

## 4. Lights
`light='RAIN'` (grey-day rain, all windows lit, lamps lit, pale lavender sky with peach rift) and `light='DUSK_RAIN'` (deeper blue shade, lower warmer key, indigo sky with orange horizon, lamps and windows brighter, halos bigger). Same geometry. Shade hue 240-260 holds for both.

## 5. Stand points (feet, world, z = the floor under the feet)
`A['stand'][name] = dict(pos=(x, y, z), look=(lx, ly), note=...)`. `look` = the ground direction the actor faces. A card facing `look` has yaw about z = `atan2(lx, -ly)` (this is what `tower.placeholder_actor(face_to=...)` does for a target); heading_deg below = `atan2(ly, lx)` (0 = +x, 90 = +y, -90 = toward the street_wide camera). Cards normally just face the camera. Coachmen stand ON the box seat (z 4.22; the plank of the seat; seated acting: put the card lower by what you need).

| name | feet (x, y, z) | look | heading deg | use |
|---|---|---|---|---|
| `hanway_a` | (-0.9, 3.0, 0.0) | (0.0, -1.0) | -90 | street_wide: walks toward the camera down the left of the crown |
| `hanway_b` | (-1.2, 8.0, 0.0) | (0.2, -1.0) | -79 | hero_track start: medium, rank behind right |
| `hanway_c` | (-1.2, 17.8, 0.0) | (0.2, -1.0) | -79 | hero_track end (walk a -> b -> c along +y, face the camera) |
| `hanway_low` | (-2.4, 12.5, 0.0) | (0.5, -1.0) | -63 | coach_low: passes below the first coach |
| `hanway_market` | (-2.6, 10.5, 0.0) | (0.5, -1.0) | -63 | market: passes the barrow corner |
| `hanway_mud` | (-3.8, 14.2, 0.0) | (0.5, -1.0) | -63 | puddle_low: beside the big puddle, the splash target (faces the camera) |
| `hanway_crowd` | (-1.0, 16.0, 0.0) | (0.0, -1.0) | -90 | street_high: the one umbrella among many |
| `box_a` | (3.55, 18.6, 4.22) | (-0.5, -0.85) | -120 | HEAD coachman (coach_0 box) |
| `box_b` | (3.55, 35.1, 4.22) | (-0.6, -0.8) | -127 | coachman_b (coach_1 box) |
| `box_c` | (3.55, 51.6, 4.22) | (-0.6, -0.8) | -127 | coachman_c (coach_2 box) |
| `box_d` | (3.55, 68.1, 4.22) | (-0.6, -0.8) | -127 | coachman_d (coach_3 box) |
| `man_road_1` | (-4.2, 16.0, 0.0) | (0.5, -1.0) | -63 | passer-by on the left of the road |
| `man_road_2` | (0.2, 22.0, 0.0) | (0.0, -1.0) | -90 | passer-by mid road |
| `lady_market` | (-4.4, 8.0, 0.0) | (0.5, -1.0) | -63 | market: the dry lady under a parasol-umbrella |
| `gent_wet` | (-5.4, 11.8, 0.0) | (0.7, -0.7) | -45 | market: the soaked gentleman (wrings his wig) |
| `seller` | (-7.9, 12.6, 0.28) | (0.8, -0.6) | -37 | market: stall holder behind the barrow |
| `jeer_a` | (-7.0, 7.0, 0.28) | (0.8, -0.5) | -32 | market jeerer on the pavement |
| `jeer_b` | (-4.5, 11.6, 0.0) | (0.8, -0.6) | -37 | market jeerer in the road (the thrower) |
| `pave_L1` | (-7.4, 4.0, 0.28) | (0.6, -1.0) | -59 | left pavement, street_wide foreground |
| `pave_R1` | (7.7, 6.0, 0.28) | (-0.4, -1.0) | -112 | right pavement, street_wide foreground |
| `pave_R2` | (7.6, 20.5, 0.28) | (-0.5, -1.0) | -117 | right pavement |
| `pave_L2` | (-7.4, 21.0, 0.28) | (0.5, -1.0) | -63 | left pavement |
| `queue_a` | (1.0, 22.0, 0.0) | (0.9, 0.0) | 0 | by the head coach street-side door (coach_0), faces the coach |
| `mud_wheel` | (-1.7, 12.2, 0.0) | (0.0, -1.0) | -90 | mud_splash: the wheel contact point (a position, not an actor) |

Placeholder staging (`stage_placeholders`, automatic in `shot(placeholders=True)`; `S.staged(preset, u)` lists them): 

| preset | staged at pose A | staged at pose B |
|---|---|---|
| `street_wide` | `hanway_a`, `man_road_1`, `box_a`, `pave_R1` | `hanway_a`, `man_road_1`, `box_a` |
| `street_high` | `hanway_crowd`, `box_a` | `hanway_crowd`, `box_a` |
| `coach_low` | `box_a`, `box_b`, `hanway_low` | `box_a`, `box_b` |
| `hero_track` | `hanway_b`, `box_a`, `box_b` | `hanway_c` |
| `box_seat` | `box_a` | `box_a` |
| `market` | `hanway_market`, `lady_market`, `gent_wet`, `seller` | `hanway_market`, `lady_market`, `gent_wet`, `seller` |
| `puddle_low` | `hanway_mud` | `hanway_mud` |
| `rank_rush` | `box_a`, `box_b` | `box_b` |

Roles: hero (priest puppet, 3.1), man (2.9), woman (2.9), coachman (3.0). Heads of every staged card are at px y 400-770, all above 880 (see tile table).

## 6. Coaches (rig)
`A['coaches']` = list of dicts `name, i, box_seat (world), door_street (world, the side facing the roadway, x 1.9 for the rank), door_kerb, horse_head, lamps, root`. Each coach is an empty `coach_i` with children `_body`, `_glass` (amber windows), `_pass` (passenger silhouettes), `_lamps`, `_w_rl/_w_rr/_w_fl/_w_fr` (spoked wheels), `_horse`, `_reins`. Move the empty (location / rotation_euler z) to drive a coach: the wheels roll and the horse bobs by drivers from the empty's y travel. `coach_run` is the same rig for the charging coach. The head coachman is `box_a` on `coach_0`; the pink umbrella belongs there (`A['pink_hand']` = (3.75, 18.45, 6.0) the hand / pole foot).
`S.run_coach(f0, f1, y0=40, y1=-14, x=0.2)` keys `coach_run` along y (linear). It faces -y. Left wheels at x-1.9.

## 7. States / hooks (each takes `frame=None`: with a frame it KEYS the value at that frame; without it sets the value now and clears keys of that hook)
All are driven by custom properties of the empty `CTRL` through drivers, so a single pair of keys (0 at f0, 1 at f1) animates the whole staggered effect.
- `S.set_crowd_umbrellas(k, frame=None)` k 0..1. 75 umbrellas (A['umbrella_slots'][i]: `feet, look, hand, open_at, radius, colour`), pavements near the hero first (open_at ~0.03-0.4), the roadway last (0.42-0.95). Each umbrella pops (scale 0 -> 1, 0.05 of k wide). At k=1 street_high shows a sea of umbrellas. Cast: put a card at `feet` facing `look`, the umbrella pole foot is `hand`. Placeholder people for the slots: `S.crowd_figures('umb')` (use `shot(..., figures='umb')`); hide them with `S.crowd_figures(False)` once cards stand there.
- `S.set_rush(k, frame=None)` k 0..1: 24 rush anchors (A['rush'][j]: `name, coach, start, end, look, delay`) run from the left kerb to the street-side doors of the 4 coaches, staggered by `delay` (a hop bob while running). Placeholder figures `S.crowd_figures('rush')`. Cast: interpolate your own cards from `start` to `end` with the same delay, or key `CTRL['rush']`.
- `S.set_rank_busy(k, frame=None)` k 0..1: coach i is FULL when k > i/4 (passenger silhouettes in the windows, lit windows, lanterns + halos + point lights) else EMPTY (silhouettes gone, windows dim, lanterns out). 0 = all empty, 0.5 = coaches 0 and 1 full, 1 = all full (default).
- `S.set_pink_umbrella(on, frame=None)` on True/False or 0..1 (scale pops from 0 to 1 over the value): pink frilled lace umbrella (alpha lace cut-outs, rosette frill) over the head coachman's box, pole foot `A['pink_hand']`, canopy top 2.7 above, radius 2.45.
- `S.rain(intensity=1.0, frame=None)` 0..1: 4 tiers of streaks (about 700 at 1.0) and of puddle ripple rings. Rain falls with the frame (drivers), 2 px wide streaks, camera-local.
- `S.throw(prop, p0, p1, t0, t1, normal=(0,0,1), arc=2.2, bounce=None, splat=True)` prop `'cabbage'` or `'egg'`; frames t0..t1: a spinning parabola from world p0 to p1 (arc = extra height at the middle); at t1 a splat decal (egg yolk / cabbage leaves) appears at p1 on the surface with that normal and stays; the prop disappears (a cabbage with `bounce=(dx, dy)` bounces away over 10 frames first). Example (cabbage hits the umbrella top of `hanway_market`, umbrella apex ~ z 4.1): `S.throw('cabbage', (-5.0, 11.4, 4.6), (-2.55, 10.45, 4.35), 120, 132, bounce=(1.6, -1.8))`.
- `S.mud_splash(t, frame=None)` t 0..1: big comic mud-water wave (13 fins, bulb tips, 16 droplets on parabolas) from the wheel contact `A['mud']['wheel_contact']` = (-1.7, 12.2, 0) toward `hanway_mud`; rises to a peak at t 0.35 and collapses by 1. Recipe: `S.run_coach(f0, f0+40, y0=26, y1=0)` (origin y 14.5 puts the left front wheel at y 12.2 at frame f0 + 40*(26-14.5)/26), key `mud_splash(0, frame=fc-1)`, `(1, frame=fc+24)` from that moment.
- `S.crowd_figures(on)` True / 'all' / 'umb' / 'rush' / False: the 3D placeholder people (coat cone + head + tricorn, 3.2 high).
- `S.apply_state(dict(umb=, busy=, pink=, rush=, rain=, mud=))` sets several at once (static).
All hooks work on an animated scene: after keying call `scene.frame_set(f)` before every render.

## 8. Render cost (720x1280, 14 samples, OIDN denoise, 2 threads, direct light + 1 glossy bounce)
- Per frame: **17 s wall (min 11, max 22) and about 35 CPU-s** (2 threads; with 4 threads about half the wall time). Coach shots with big puddles are the slowest, box_seat the fastest.
- One-time per process: texture load + `shot()` build about 3-8 s. A 60-frame take at 2 threads: about 16-18 min.
- Rain, drivers and halos are evaluated by Blender; nothing is baked. Keep `SAMPLES` >= 12 (lower shows speckle in the puddles).

## 9. Contact tiles (finals with placeholder cards; wall / cpu s; head pixel y of every staged card) and colour
| 01_street_wide | street_wide RAIN | 17 / 35 | hanway_a 651, man_road_1 650, box_a 545, pave_R1 646 |
| 02_street_high | street_high RAIN umb 0 | 15 / 30 | hanway_crowd 763, box_a 676 |
| 03_coach_low | coach_low RAIN busy 1 | 22 / 44 | box_a 455, box_b 588, hanway_low 563 |
| 04_hero_track | hero_track RAIN | 19 / 39 | hanway_b 656, box_a 547, box_b 634 |
| 05_box_seat | box_seat RAIN | 14 / 28 | box_a 563 |
| 06_market | market RAIN | 19 / 38 | hanway_market 613, lady_market 619, gent_wet 642, seller 629 |
| 07_puddle_low | puddle_low RAIN | 18 / 35 | hanway_mud 567 |
| 08_rank_rush | rank_rush RAIN rush 0 | 19 / 39 | box_a 446, box_b 551 |
| 09_wide_dusk | street_wide DUSK_RAIN | 18 / 36 | hanway_a 651, man_road_1 650, box_a 545, pave_R1 646 |
| 10_high_dusk | street_high DUSK_RAIN | 15 / 30 | hanway_crowd 763, box_a 676 |
| 11_box_dusk | box_seat DUSK_RAIN | 11 / 23 | box_a 566 |
| 12_umb_05 | umbrellas 0.5 (street_high B) | 17 / 33 | hanway_crowd 764, box_a 630 |
| 13_umb_10 | umbrellas 1.0 (street_high B) | 16 / 31 | hanway_crowd 764, box_a 630 |
| 14_busy_0 | coach_low rank empty (busy 0) | 20 / 40 | box_a 455, box_b 588, hanway_low 563 |
| 15_pink | box_seat pink umbrella on | 11 / 21 | box_a 570 |
| 16_rush_1 | rank_rush rush 1, busy 0.5 | 20 / 40 | box_a 446, box_b 551 |
| 17_rush_wide | rank_rush B, rush 1, busy 1 | 20 / 39 | box_b 528 |
| 18_mud | puddle_low mud splash t 0.4 | 16 / 32 | hanway_mud 567 |
| 19_throw | market cabbage mid-arc (f 18 of 10-22) | 19 / 38 | hanway_market 602, lady_market 608, gent_wet 646, seller 632 |
| 20_dusk_rush | rank_rush DUSK_RAIN rush 0.7 | 19 / 38 | box_b 528 |

Shade hue (target 240-260) and magenta share (target <= 10 %) per tile (`street_hue.py`, which uses `tools/hue_report.py`):
```
  01_street_wide             shade hue  248.1  shaded 0.33  magenta   4.6 %  ok
  02_street_high             shade hue  248.6  shaded 0.27  magenta   7.2 %  ok
  03_coach_low               shade hue  248.2  shaded 0.45  magenta   6.1 %  ok
  04_hero_track              shade hue  247.8  shaded 0.37  magenta   5.2 %  ok
  05_box_seat                shade hue  253.4  shaded 0.27  magenta   7.3 %  ok
  06_market                  shade hue  246.4  shaded 0.59  magenta   2.2 %  ok
  07_puddle_low              shade hue  247.6  shaded 0.43  magenta   7.1 %  ok
  08_rank_rush               shade hue  249.0  shaded 0.44  magenta   7.7 %  ok
  09_wide_dusk               shade hue  248.0  shaded 0.47  magenta   3.7 %  ok
  10_high_dusk               shade hue  244.7  shaded 0.43  magenta   3.9 %  ok
  11_box_dusk                shade hue  253.6  shaded 0.40  magenta   3.8 %  ok
  12_umb_05                  shade hue  245.3  shaded 0.44  magenta   7.1 %  ok
  13_umb_10                  shade hue  246.7  shaded 0.47  magenta   8.4 %  ok
  14_busy_0                  shade hue  248.2  shaded 0.45  magenta   6.2 %  ok
  15_pink                    shade hue  256.9  shaded 0.29  magenta   7.0 %  ok
  16_rush_1                  shade hue  248.6  shaded 0.43  magenta   6.7 %  ok
  17_rush_wide               shade hue  247.1  shaded 0.49  magenta   7.5 %  ok
  18_mud                     shade hue  245.9  shaded 0.48  magenta   2.9 %  ok
  19_throw                   shade hue  244.1  shaded 0.61  magenta   2.1 %  ok
  20_dusk_rush               shade hue  245.7  shaded 0.54  magenta   3.3 %  ok
```
A Hue Correct node in the grade (`_hue_guard`) pulls the magenta band toward blue-violet; pink / red stays.

## 10. Gotchas
- `shot()` first, hooks after. `S.render(path)` writes one PNG; call `scene.frame_set(f)` first for anything keyed (rain, wheels, umbrellas, throws).
- Placeholder cards (`placeholders=True`) are for scale only: `placeholders=False` for the cast render team and stage your own cards at `A['stand']`. Cards must not be placed inside the 3D placeholder figures (`figures=False` by default).
- Umbrella holders: hide `crowd_figures` when you stand cards at the slots. The umbrella itself stays 3D.
- A card on a box seat floats on the plank: z 4.22 is the plank top. Coachmen faces the camera side of the coach (look (-0.5, -0.85)).
- The camera may not enter the crowd figures or coaches (keep >= 2.5 from stand points, the slot list avoids the preset cameras and stand points by 2.4 / 1.6).
- Real point lights (7 lamps, 6 shop windows, coach lanterns) are chosen near the preset camera's middle pose when `shot()` runs: for a long dolly along the street build the shot at the middle `u`.
- Eave drips and rain are camera-only geometry; do not hide `cam`. No DOF: never enable it. The sky is a dome (8192 px) painted for az 90 = down the street; reverse shots look at the dusk/overcast dome with the warm rift behind: fine, but the far-end terrace is then the near end (y -56 row ends open).
- Colour rule: shade hue 240-260 and magenta <= 10 %: if you add a coloured prop, keep reds orange-leaning or use warm unshaded materials.
- No text anywhere: signs are pictures; if you add anything, no letters.
