# v3/set3d12/street.py : film 12 set ("ไอ้ร่มเดินได้", a Georgian London street in the rain, 1750s) (bpy 5.x, Cycles CPU)

Read only this file. Everything lives in `film/v3/set3d12/`:
- `street.py`: the whole set, every hook, presets, cameras, stand points, CLI. `street_parts.py`: horse, hackney coach, wheel, crowd figure, umbrella geometry. `street_tex.py`: all artwork (numpy / PIL, cached in `tex_street/`, bump `TEX_V` after editing a painter).
- `street_hue.py`: shade hue + magenta share per frame. `street_work/`: `t_anim.py` (hook test, prints ALL OK), `render_tiles.py` + `make_contact.py` (the contact sheet), `final/` (the 25 finals), `old/` (round-1 leftovers), `final_log.txt`, `hue_rows.txt`.
- `contact.jpg` (5 columns of 720x1280 tiles, label under each, cyan line at y 880) and `contact_small.jpg` (1/3). `styleboard/` = the client-approved board. Backups: `bak_r0/` (board build), `bak_r1/` (before the SET-gate fix round).

Style (client-approved, do not change): warm amber lit windows vs blue-violet rain shade, one hard warm key from the left-behind, dense terraces, wet setts with layered puddles, crisp cartoon clouds, sharp image, NO depth of field, NO text or letters anywhere (signs are pictures).

## 1. Quick start
```python
import sys; sys.path.insert(0, '/abs/path/film/v3/set3d12')
import street as S, bpy
A = S.shot('box_seat', 'RAIN', placeholders=False)      # build + camera + rain + halos + lights.  placeholders=True stages the REAL cast12 cards (cards='cast', default) at the stand points
S.key_camera('box_seat', 1, 60)                          # camera move A -> B between frames 1 and 60
S.set_pink_umbrella(0, frame=100); S.set_pink_umbrella(1, frame=106)
sc = bpy.context.scene
for f in range(1, 61):
    sc.frame_set(f)                                      # REQUIRED for keyed hooks, rain and rolling wheels (drivers read the frame)
    S.render('/abs/out/f%04d.png' % f)                   # 720x1280 PNG, compositor grade included
```
- `S.shot(preset, light='RAIN', u=0.0, placeholders=True, figures=False, quality='final', cards='cast')` -> anchors dict `A` (keys below). `u` 0..1 places the camera between pose A and pose B. One `shot()` per take (it rebuilds the whole scene, 2-8 s); then animate with the hooks. Changing preset or light = a new `shot()`.
- CLI: `python3 street.py final [preset ...] [RAIN|DUSK_RAIN]` (720x1280 -> `street_work/final/<preset>_<LIGHT>_final.png`), `python3 street.py stills ...` (360x640, 6 samples, ~3 s). `THREADS=2 SAMPLES=24` environment variables are honoured (default 2 threads, 20 samples, OIDN denoise, glossy filter 1.0, indirect clamp 1.6).
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
| `street_wide` | (1.0, -14.0, 3.4) -> (0.3, 40.0, 6.4) | (0.6, -4.0, 3.3) -> (0.3, 40.0, 6.7) (lens 22) |
| `street_wide_low` | (0.8, -12.0, 1.4) -> (0.3, 40.0, 5.6) | (0.5, -4.0, 1.3) -> (0.3, 40.0, 6.0) (lens 22) |
| `street_wide_rev` | (-0.6, 72.0, 3.4) -> (0.2, 10.0, 6.2) | (-0.2, 62.0, 3.3) -> (0.2, 10.0, 6.4) (lens 22) |
| `street_high` | (-3.0, -20.0, 32.0) -> (0.5, 34.0, 1.0) | (-2.0, -9.0, 17.0) -> (0.5, 32.0, 2.0) (lens 22) |
| `coach_low` | (-3.6, 4.2, 1.35) -> (3.6, 19.0, 3.3) | (-1.0, 7.5, 1.5) -> (3.55, 19.5, 3.9) (lens 22) |
| `coach_close` | (-2.6, 12.0, 1.5) -> (3.55, 19.4, 4.9) | (0.3, 13.2, 2.5) -> (3.55, 18.8, 6.3) (lens 25) |
| `hero_track` | (-3.8, 0.4, 2.2) -> (-0.6, 8.0, 3.3) | (-3.6, 10.2, 2.2) -> (-0.6, 17.8, 3.3) (lens 22) |
| `box_seat` | (-1.2, 10.5, 3.2) -> (3.4, 18.8, 6.6) | (0.9, 14.2, 4.4) -> (3.45, 18.7, 6.7) (lens 26) |
| `box_trio` | (-2.2, 5.5, 2.2) -> (3.55, 36.0, 5.6) | (-1.0, 9.5, 2.6) -> (3.55, 44.0, 5.4) (lens 24) |
| `market` | (0.4, 0.4, 2.0) -> (-6.0, 11.0, 4.2) | (-0.8, 3.0, 2.1) -> (-6.4, 11.5, 4.3) (lens 22) |
| `puddle_low` | (-5.3, 3.6, 0.75) -> (-1.8, 12.6, 2.0) | (-5.3, 4.6, 0.7) -> (-2.2, 12.6, 2.2) (lens 22) |
| `rank_rush` | (-3.2, 8.0, 2.8) -> (1.8, 25.0, 4.0) | (-2.6, 14.0, 3.0) -> (3.0, 37.0, 4.0) (lens 22) |
| `rank_wide` | (-3.4, -4.0, 4.6) -> (3.4, 42.0, 3.4) | (-2.4, 4.0, 3.8) -> (3.4, 48.0, 3.4) (lens 22) |
| `rank_idle` | (-3.2, 6.0, 1.8) -> (3.6, 34.0, 3.4) | (-2.2, 9.0, 2.0) -> (3.6, 40.0, 3.4) (lens 22) |

| preset | what it shows | plan shots |
|---|---|---|
| `street_wide_low` | the same street from 1.3 high, big puddle in the foreground | 9 |
| `street_wide_rev` | REVERSE: camera at y 72 looks toward -y down the street (closed south terrace, rank rears on the left) | 20 |
| `coach_close` | 25 mm: the head coachman on his box plus Hanway passing below, closer | 7, 15 |
| `box_trio` | boxes a, b, c in frame (three coachmen) | 2, 14 |
| `rank_wide` | wide and high on the whole rank, for `roll_rank` | 17 |
| `rank_idle` | the rank from the road for the empty / bored state (`set_rank_busy(0)`) | 22 |
| `street_wide` | eye level (3.4) down the whole street, rank far right, push in to B | 1, 9, 19, 20 (reverse: build a reverse pose yourself with `make_camera`) |
| `street_high` | crane from 32 (A) down to 17 (B): roofs, chimneys, the whole street | 4, 13, 21 |
| `coach_low` | low (1.35) at the rank, the box seats up in frame, the head coach centre | 2, 7, 15, 22 |
| `hero_track` | medium along the left of the crown following the hero (his walk `hanway_b` -> `hanway_c`), rank behind right | 3, 11, 18 |
| `box_seat` | 26 mm: A wide, B (u 1) close enough that the coachman's face is ~250 px; pink umbrella over him | 6, 8, 23 |
| `market` | eye level at the barrow / stall corner on the left pavement, road with puddles in front | 5, 10 |
| `puddle_low` | 0.75 above the road: big puddle, gutter and grating in the foreground, the coach crossing and the splash target `hanway_mud` | 12 |
| `rank_rush` | the rank from the road, the crowd fights for the doors of coaches 0 and 1 | 16 |

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
| `hanway_mud` | (-4.3, 11.0, 0.0) | (0.5, -1.0) | -63 | puddle_low: beside the big puddle, the splash target (faces the camera) |
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
| `queue_a` | (0.1, 21.0, 0.0) | (0.9, 0.0) | 0 | by the head coach street-side door (coach_0), faces the coach (x <= 0.3 keeps 1.2 from the wheels) |
| `queue_b` | (-0.2, 23.4, 0.0) | (0.9, 0.0) | 0 | the rank queue, 2nd |
| `queue_c` | (0.1, 25.8, 0.0) | (0.9, 0.0) | 0 | the rank queue, 3rd |
| `queue_d` | (0.0, 14.8, 0.0) | (0.9, 0.3) | 18 | the rank queue, in front of the head horse |
| `hanway_low2` | (0.9, 17.2, 0.0) | (0.0, -1.0) | -90 | coach_close: Hanway passing below the head coach |
| `hanway_rev` | (-0.8, 27.0, 0.0) | (0.0, 1.0) | 90 | street_wide_rev: Hanway, the street opened umbrellas around him (faces the camera at y 70) |
| `rev_a` | (-4.0, 40.0, 0.0) | (0.0, 1.0) | 90 | street_wide_rev: gentleman on the left of the road |
| `rev_b` | (1.0, 33.0, 0.0) | (0.0, 1.0) | 90 | street_wide_rev: gentleman mid road |
| `rev_pave_L` | (-7.5, 44.0, 0.28) | (0.0, 1.0) | 90 | street_wide_rev: left pavement |
| `rev_pave_R` | (7.6, 30.0, 0.28) | (0.0, 1.0) | 90 | street_wide_rev: right pavement |
| `mud_wheel` | (-1.7, 12.2, 0.0) | (0.0, -1.0) | -90 | mud_splash: the wheel contact point (a position, not an actor) |

Placeholder staging (`stage_placeholders`, automatic in `shot(placeholders=True)`; `S.staged(preset, u)` lists them): 

| preset | staged at pose A | staged at pose B |
|---|---|---|
| `street_wide` | `hanway_a`, `man_road_1`, `box_a`, `pave_R1` | `hanway_a`, `man_road_1`, `box_a` |
| `street_wide_low` | `hanway_a`, `man_road_1`, `box_a`, `pave_R1` | `hanway_a`, `man_road_1`, `box_a` |
| `street_wide_rev` | `hanway_rev`, `rev_a`, `rev_b`, `rev_pave_L`, `rev_pave_R` | `hanway_rev`, `rev_a`, `rev_b`, `rev_pave_L`, `rev_pave_R` |
| `street_high` | `hanway_crowd`, `box_a` | `hanway_crowd`, `box_a` |
| `coach_low` | `box_a`, `box_b`, `hanway_low` | `box_a`, `box_b` |
| `coach_close` | `box_a`, `hanway_low2` | `box_a` |
| `hero_track` | `hanway_b`, `box_a`, `box_b` | `hanway_c` |
| `box_seat` | `box_a` | `box_a` |
| `box_trio` | `box_a`, `box_b`, `box_c` | `box_a`, `box_b`, `box_c` |
| `market` | `hanway_market`, `lady_market`, `gent_wet`, `seller` | `hanway_market`, `lady_market`, `gent_wet`, `seller` |
| `puddle_low` | `hanway_mud` | `hanway_mud` |
| `rank_rush` | `box_a`, `box_b` | `box_b` |
| `rank_wide` |  |  |
| `rank_idle` | `box_a`, `box_b`, `box_c` | `box_a`, `box_b`, `box_c` |

**Cards.** `shot(..., cards='cast')` stages REAL cast12 cards (`cast_role_card`): `hero` = `hanway_walk_umbrella` with an amber rim (`rim='#f2b25c'`) and in DUSK_RAIN a shade tint; `man` / `man_b` / `woman` = walk cycles; `coachman` = `coachman_gloat`, `coachman_b` = `coachman_b_glare`, `coachman_c` = `coachman_c_nod`, `coachman_sulk` = `coachman_sulk_standing` with the sprite umbrella removed (use the 3D pink umbrella); coachmen are mirrored to face the road and **stand on the plank (z 4.22), never with `coach_box`**. `cards='ph'` gives the old blocky placeholders. Extra cards: `S.stage_cards([(name, role, (x, y, z), pose_overrides)])`; any cast pose: `S.cast_card(name, cast, pose_dict, (x, y, z), face_to=cam_location, tilt=0, tint=None, rim=None, mirror=False, over=None)` (the card is 1 unit = 1 head, feet at the mark). Crowd cards at the rush anchors: `S.stage_rush_cards(k, n)` (running cycle while on the way, push pose at the door). Card rasters are cached in `street_work/actors/`. Heads of every staged card are at px y 400-770, all above 880 (see tile table).

## 6. Coaches (rig)
`A['coaches']` = list of dicts `name, i, box_seat (world), door_street (world, the side facing the roadway, x 1.9 for the rank), door_kerb, horse_head, lamps, root`. Each coach is an empty `coach_i` with children `_body`, `_glass` (amber windows), `_pass` (passenger silhouettes), `_lamps`, `_w_rl/_w_rr/_w_fl/_w_fr` (spoked wheels), `_horse`, `_reins`. Move the empty (location / rotation_euler z) to drive a coach: the wheels roll and the horse bobs by drivers from the empty's y travel. `coach_run` is the same rig for the charging coach. The head coachman is `box_a` on `coach_0`; the pink umbrella belongs there (`A['pink_hand']` = (3.75, 18.45, 6.0) the hand / pole foot).
`S.run_coach(f0, f1, y0=40, y1=-14, x=0.2)` keys `coach_run` along y (linear). It faces -y. Left wheels at x-1.9.

## 7. States / hooks (each takes `frame=None`: with a frame it KEYS the value at that frame; without it sets the value now and clears keys of that hook)
All are driven by custom properties of the empty `CTRL` through drivers, so a single pair of keys (0 at f0, 1 at f1) animates the whole staggered effect.
- `S.set_crowd_umbrellas(k, frame=None)` k 0..1. about 70 umbrellas (A['umbrella_slots']) (A['umbrella_slots'][i]: `feet, look, hand, open_at, radius, colour`), pavements near the hero first (open_at ~0.03-0.4), the roadway last (0.42-0.95). Each umbrella pops (scale 0 -> 1, 0.05 of k wide). At k=1 street_high shows a sea of umbrellas. Cast: put a card at `feet` facing `look`, the umbrella pole foot is `hand`. Placeholder people for the slots: `S.crowd_figures('umb')` (use `shot(..., figures='umb')`); hide them with `S.crowd_figures(False)` once cards stand there.
- `S.set_rush(k, frame=None)` k 0..1: 24 rush anchors (A['rush'][j]: `name, coach, start, end, look, delay`) run from the left kerb to the street-side doors of the 4 coaches, staggered by `delay` (a hop bob while running). Placeholder figures `S.crowd_figures('rush')`. Cast: interpolate your own cards from `start` to `end` with the same delay, or key `CTRL['rush']`.
- `S.set_rank_busy(k, frame=None)` k 0..1: coach i is FULL when k > i/4 (passenger silhouettes in the windows, lit windows, amber lanterns + halos + point lights, alert horse with raised head) else EMPTY (silhouettes gone, windows dim, lanterns out, the horse hangs its head: `coach_i_horse_idle`). 0 = all empty, 0.5 = coaches 0 and 1 full, 1 = all full (default).
- `S.set_pink_umbrella(on, frame=None)` on True/False or 0..1 (scale pops from 0 to 1 over the value): pink frilled lace umbrella (alpha lace cut-outs, rosette frill) over the head coachman's box, pole foot `A['pink_hand']`, canopy top 2.7 above, radius 2.45.
- `S.rain(intensity=1.0, frame=None)` 0..1: 4 tiers of streaks (about 700 at 1.0) and of puddle ripple rings. Rain falls with the frame (drivers), 2 px wide streaks, camera-local.
- `S.throw(prop, p0, p1, t0, t1, normal=(0,0,1), arc=2.2, bounce=None, splat=True)` prop `'cabbage'` or `'egg'`; frames t0..t1: a spinning parabola from world p0 to p1 (arc = extra height at the middle); at t1 a splat decal (egg yolk / cabbage leaves) appears at p1 on the surface with that normal and stays; the prop disappears (a cabbage with `bounce=(dx, dy)` bounces away over 10 frames first). Example (cabbage hits the umbrella top of `hanway_market`, umbrella apex ~ z 4.1): `S.throw('cabbage', (-5.0, 11.4, 4.6), (-2.55, 10.45, 4.35), 120, 132, bounce=(1.6, -1.8))`.
- `S.mud_splash(t, frame=None)` t 0..1: big comic mud-water wave (12 lit glossy brown fins with bulb tips, translucent spray sheets, 16 droplets on parabolas; a clear lane in the middle so the card stays readable) from the wheel contact `A['mud']['wheel_contact']` = (-1.7, 12.2, 0) toward `hanway_mud` (-4.3, 11.0); rises to a peak at t 0.35 and collapses by 1. Recipe: `S.run_coach(f0, f0+40, y0=26, y1=0)` (origin y 14.5 puts the left front wheel at y 12.2 at frame f0 + 40*(26-14.5)/26), key `mud_splash(0, frame=fc-1)`, `(1, frame=fc+24)` from that moment.
- `S.roll_rank(f0, f1, dy=-14, coaches=(0,1,2,3))` shot 17: keys the four rank coaches pulling away along y (wheels roll, horses bob). Frame it with `rank_wide`.
- `S.crowd_figures(on)` True / 'all' / 'umb' / 'rush' / False: the 3D placeholder people (coat cone + head + tricorn, 3.2 high).
- `S.apply_state(dict(umb=, busy=, pink=, rush=, rain=, mud=))` sets several at once (static).
All hooks work on an animated scene: after keying call `scene.frame_set(f)` before every render.

## 8. Render cost (720x1280, 14 samples, OIDN denoise, 2 threads, direct light + 1 glossy bounce)
- Per frame (tiles at 24 samples): **27 s wall (min 16, max 34) and about 54 CPU-s** (2 threads; with 4 threads about half the wall time). Default 20 samples is about 20 % cheaper. Puddle and coach shots are the slowest, box shots the fastest. Cast cards add 0.3-0.5 s each the first time (raster cache).
- One-time per process: texture load + `shot()` build about 3-8 s. A 60-frame take at 2 threads: about 16-18 min.
- Rain, drivers and halos are evaluated by Blender; nothing is baked. Keep `SAMPLES` >= 20 (lower shows speckle in the puddles).

## 9. Contact tiles (finals with real cast cards; wall / cpu s; head pixel y of every staged card) and colour
| 01_hook_wide | street_wide RAIN (hook) | 27 / 54 | hanway_a 689, man_road_1 692, box_a 587, pave_R1 692 |
| 02_wide_low | street_wide_low RAIN (shot 9) | 27 / 54 | hanway_a 606, man_road_1 657, box_a 551, pave_R1 625 |
| 03_wide_rev | street_wide_rev umb 0.6 (shot 20) | 29 / 58 | hanway_rev 677, rev_a 684, rev_b 680, rev_pave_L 681, rev_pave_R 676 |
| 04_high_hunched | street_high RAIN bare heads (shot 4) | 23 / 46 | hanway_crowd 760, box_a 674 |
| 05_coach_low | coach_low busy 1 (shot 2) | 34 / 67 | box_a 446, box_b 574, hanway_low 546 |
| 06_coach_close | coach_close two-shot (shots 7, 15) | 23 / 47 | box_a 421, hanway_low2 695 |
| 07_hero_track | hero_track RAIN (shots 3, 11) | 30 / 60 | hanway_b 639, box_a 540, box_b 621 |
| 08_queue | hero_track + rank queue (shot 18) | 30 / 60 | hanway_b 639, box_a 540, box_b 621 |
| 09_box_face | box_seat B (shots 6, 8) | 16 / 33 | box_a 536 |
| 10_box_trio | box_trio three coachmen (shots 2, 14) | 29 / 59 | box_a 423, box_b 579, box_c 646 |
| 11_market | market RAIN (shot 5) | 29 / 58 | hanway_market 680, lady_market 699, gent_wet 713, seller 700 |
| 12_puddle_low | puddle_low RAIN (shot 12) | 28 / 56 | hanway_mud 476 |
| 13_reveal | rank_rush REVEAL rush 1 busy 1 (shot 16) | 26 / 52 | box_a 401, box_b 557 |
| 14_rush_dusk | rank_rush DUSK_RAIN rush 1 | 28 / 56 | box_a 401, box_b 557 |
| 15_rank_rolling | rank_wide coaches rolling (shot 17) | 30 / 59 |  |
| 16_rank_idle | rank_idle busy 0 bored (shot 22) | 30 / 60 | box_a 372, box_b 530, box_c 596 |
| 17_box_dusk | box_seat DUSK_RAIN (shot 14) | 19 / 38 | box_a 551 |
| 18_wide_dusk | street_wide DUSK_RAIN | 26 / 53 | hanway_a 689, man_road_1 692, box_a 587, pave_R1 692 |
| 19_high_dusk_bare | street_high DUSK bare heads + ONE umbrella (shot 13) | 28 / 56 | hanway_crowd 759, box_a 625 |
| 20_umb_05 | umbrellas 0.5 (street_high B) | 27 / 54 | hanway_crowd 759, box_a 625 |
| 21_umb_10 | umbrellas 1.0 (street_high B) | 27 / 55 | hanway_crowd 759, box_a 625 |
| 22_ending_pink | box_seat pink umbrella, sulking (shot 23) | 19 / 37 | box_a 554 |
| 23_mud | puddle_low mud splash t 0.4 (shot 12) | 32 / 65 | hanway_mud 476 |
| 24_throw | market cabbage mid-arc (frame 18 of 10-22) | 26 / 52 | hanway_market 680, lady_market 704, gent_wet 731, seller 717 |
| 25_coach_dusk | coach_low DUSK_RAIN busy 1 | 29 / 59 | box_a 421, box_b 611 |

Shade hue (target 240-260) and magenta share (target <= 10 %) per tile (`street_hue.py`, which uses `tools/hue_report.py`):
```
  01_hook_wide               shade hue  244.8  shaded 0.37  magenta   4.8 %  ok
  02_wide_low                shade hue  242.4  shaded 0.43  magenta   3.9 %  ok
  03_wide_rev                shade hue  243.6  shaded 0.51  magenta   4.2 %  ok
  04_high_hunched            shade hue  247.6  shaded 0.29  magenta   6.9 %  ok
  05_coach_low               shade hue  252.3  shaded 0.40  magenta   5.0 %  ok
  06_coach_close             shade hue  253.2  shaded 0.27  magenta   6.5 %  ok
  07_hero_track              shade hue  247.6  shaded 0.35  magenta   4.4 %  ok
  08_queue                   shade hue  247.5  shaded 0.34  magenta   4.6 %  ok
  09_box_face                shade hue  257.7  shaded 0.16  magenta   3.5 %  ok
  10_box_trio                shade hue  253.6  shaded 0.37  magenta   6.5 %  ok
  11_market                  shade hue  246.8  shaded 0.51  magenta   3.0 %  ok
  12_puddle_low              shade hue  245.6  shaded 0.42  magenta   5.2 %  ok
  13_reveal                  shade hue  242.7  shaded 0.41  magenta   5.0 %  ok
  14_rush_dusk               shade hue  241.9  shaded 0.45  magenta   4.7 %  ok
  15_rank_rolling            shade hue  255.3  shaded 0.43  magenta   6.3 %  ok
  16_rank_idle               shade hue  255.7  shaded 0.44  magenta   7.1 %  ok
  17_box_dusk                shade hue  257.5  shaded 0.21  magenta   5.0 %  ok
  18_wide_dusk               shade hue  243.9  shaded 0.45  magenta   3.5 %  ok
  19_high_dusk_bare          shade hue  244.3  shaded 0.49  magenta   4.9 %  ok
  20_umb_05                  shade hue  245.4  shaded 0.41  magenta   7.1 %  ok
  21_umb_10                  shade hue  245.0  shaded 0.41  magenta   7.1 %  ok
  22_ending_pink             shade hue  258.7  shaded 0.13  magenta   4.8 %  ok
  23_mud                     shade hue  242.9  shaded 0.50  magenta   3.2 %  ok
  24_throw                   shade hue  243.8  shaded 0.46  magenta   4.8 %  ok
  25_coach_dusk              shade hue  253.4  shaded 0.40  magenta   5.3 %  ok
```
A Hue Correct node in the grade (`_hue_guard`) pulls the magenta band toward blue-violet; pink / red stays.

## 10. Gotchas
- `shot()` first, hooks after. `S.render(path)` writes one PNG; call `scene.frame_set(f)` first for anything keyed (rain, wheels, umbrellas, throws).
- `placeholders=True` stages real cast cards for stills; for production `placeholders=False` and stage / animate your own cards at `A['stand']`. Do not place cards inside the 3D placeholder figures (`figures=False` by default).
- Umbrella holders: hide `crowd_figures` when you stand cards at the slots. The umbrella itself stays 3D.
- A card on a box seat floats on the plank: z 4.22 is the plank top. Coachmen faces the camera side of the coach (look (-0.5, -0.85)).
- The camera may not enter the crowd figures or coaches (keep >= 2.5 from stand points, the slot list avoids the preset cameras and stand points by 2.4 / 1.6).
- Real point lights (7 lamps, 6 shop windows, coach lanterns) are chosen near the preset camera's middle pose when `shot()` runs: for a long dolly along the street build the shot at the middle `u`.
- Eave drips and rain are camera-only geometry; do not hide `cam`. No DOF: never enable it. The sky is a dome (8192 px) painted for az 90 = down the street; reverse shots look at the dusk/overcast dome with the warm rift behind: fine, but the far-end terrace is then the near end (y -56 row ends open).
- Colour rule: shade hue 240-260 and magenta <= 10 %: if you add a coloured prop, keep reds orange-leaning or use warm unshaded materials.
- No text anywhere: signs are pictures; if you add anything, no letters.

## 11. Weak points (honest list, SET gate round 2)
- The horse is still low-poly and flat-toon shaded (22 segments, faceted at close range); legs do not walk (a bob with travel only). The coach cabin and its lit windows are partly hidden by the box from low angles.
- The 3D placeholder crowd (`crowd_figures`) is blocky: bare-headed people for the umbrella slots and rush crowd are only for scale. Real cards: `stage_rush_cards`.
- Mud splash: stylised lit-brown fins + spray, tested at t 0.4 only in stills; it is not a fluid. Check t 0.2-0.6 in the take.
- Hue guard: shaded reds (hammercloth, wheels) lean orange/violet; pink / coral stays. Dusk horses read purple-brown.
- Residual fine grain in dark puddle reflections below 20 samples; lantern reflections in puddles can still read as a glowing orb when the puddle outline is not visible (tile 24, bottom right).
- Setts are regular; 16 facade types repeat along the street; cloud bottoms are flat. Rain is camera-parented (no parallax).
- The egg-on-umbrella impact on hero_track (shot 11) and the cabbage hit on the card's own umbrella are not placed for you: `throw()` needs the target point from the card pose anchors (`umb_top_r`).
- Real point lights are picked at `shot()` for the camera's middle pose.
- Stale files of the first round were moved to `street_work/old/`.
