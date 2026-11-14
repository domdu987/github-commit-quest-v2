# v3/set3d9/wall.py : film 9 set ("ไอ้ช่างขนม", sticky-rice mortar of a Ming city wall, ~1370s) (bpy 5.3, Cycles CPU)

Files:
- `wall.py`: the location `wall_site` (construction site, the wall in two sections, gate tower, field + river, enemy cannon line) and the macro area (inside the mortar joint), with every hook.
- `wall_tex.py`: all artwork, painted with numpy + PIL (bricks plain / rice / old + mortar masks, stone, ground, field, pastes, rice soup, roof tiles, canvas, banners, lantern skin, crack maps + reveal-order maps, dents, drips, rain screens, macro clay / matrix, 5 skies, 5 painted rings). Cached in `tex_wall/` by a hash of the params + `TEX_V` (bump `TEX_V` after editing painter code). Glow images `pool`, `shaft`, `glint`, `wisp` are read from `v3/set3d8/tex_desert/`.
- `contact.jpg`: every preset x relevant light / state at 720x1280, 12 samples, placeholder actors, plus a row of 6 reference frames (A t0040 t0062 t0072 t0096 t0104, B t0033). The cyan line is y 880. `contact_small.jpg` is 1/3 size. Order: `wall_work/contact_order.txt`.

Work files in `wall_work/`: `final/` (the 27 finals), `final_log.txt` (wall / CPU s, head pixels), `hue_rows.txt`, `t_anim.py` (hook test, prints ALL OK), `t_cost.py`, `run_finals.sh`, `REF_*.jpg`.

Built on `v3/set3d8/desert.py` → louvre → bakery → mine → pagoda / tower. Imported, not copied:
- `tower`: `MB`, `mat_lit`, `mat_emit`, `setup_grade`, `make_camera`, `render`, `no_bounce`, `_key`, `_show`, `_fcurves`, `placeholder_actor` (+ `PH` roles).
- `mine`: `obox`, `beam`, `rod`, `lumpy`, `chain_rod`, `_obj`, `_untoon`, `_glossy`, `_append_shader`, `_denoise`, `_mat_fire`, `setup_render`.
- `pagoda`: `_kd`, `_haze_mat`, `digest`. `bakery`: `Frame`, `_halo`, `_light`, `_mat_add`, `_basket`.
- `desert`: `set_flames` (fire flicker), `clear_keys`, `_keyval`, `_value`, `_retarget`, `_mat_alpha_k`, `_mat_sky`, `_mat_water` (river + puddles mirror the sky), `_sky` (sky dome + painted ring), `_flame_light`, `_brazier`, `_bucket`, `_jar`.

`wall.STATE` is `tower.STATE`. **No depth of field anywhere** (`apply_dof()` is a no-op).

World: 1 unit = 1 D (head), Z up, ground z 0. The wall runs along x. **Outer face y = 0 (faces -y: field, river, enemy)**, **inner face y = 5 (faces +y: the construction site)**, thickness 5. Stone plinth z 0..1; courses of 0.5 D above it (`top_z = 1 + 0.5 x courses`, max 30 courses = 16 D).
- **Lin's section (rice mortar) x -22..0**: warmer bricks, thick creamy ivory mortar beads with smears, blue banners on top.
- **The general's section (plain mortar) x 0..22**: cooler blue-grey bricks, thin dark-grey recessed joints, red banners on top.
- Old finished wall x -74..-22 (16 D, crenels), stub x 22..24, **gate tower x 24..38** (17 D base, arched tunnel at x 31, red two-storey pavilion with glowing lattice windows, double swept-eave roof, lanterns).
Seen from the site (inside, looking -y) the general's section is on screen LEFT and the gate further left; from the field (looking +y) it is on the right.

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d9"); import wall as W
A = W.build('wall_site', 'two_sections', light='DAY')   # build(location, preset=None, clear=True, dress=True, light=None) -> anchors
cam = W.make_camera(A['cam'])                           # all cameras of the area in A['cams']; A['cam_name']
W.setup_render(scene, 'final' | 'preview')              # 720x1280 12 samples / 360x640 6, 2 threads, direct light, OIDN, transparent bounces 24
W.apply_preset_state(preset); W.clear_keys()
W.stage_placeholders(A, cam_name, cam_loc); W.head_pixels(cam_name)
W.render(path) -> (wall s, cpu s); W.digest(); W.top_z('general')
```
`light=` any of **DAY | DUSK | DAWN | RAIN | BATTLE** for every preset (DAWN added for shot plan 9/17).

**Keys rule** (as the templates): once a hook was keyed with `frame=`, keys win over un-keyed calls. Key every state, or `clear_keys()` first. Hooks that animate with time (steam, smoke, rain, flames, impacts, collapse, macro) must be called **every frame** of a shot.

### Hooks

| hook | what |
|---|---|
| `set_wall_height(section, courses, frame=None)` | `'lin'` / `'general'` / `'both'`, 0..30 courses of 0.5 D. Hides the courses above, moves the top dressing (rubble bed, half-laid course in wet mortar, tub, trowel, brick stacks, a bamboo shear-leg hoist with basket, the banners) to the new top, clips the crack overlay there. Visibility keys constant. Month 1: lin 18 / general 21; month 2: 20 / 26; battle: 26 / 30. |
| `set_cauldron_steam(level, frame=None, speed=1)` | white steam billows rising, swelling and drifting from the rice soup; 0 none .. 1 .. 1.5. |
| `set_rain(level, frame=None, speed=1)` | rain streaks as a **compositor overlay** (two scrolling screen layers added after the grade; render cost 0). 0 .. 1 steady .. 1.5. Wet sheen on brick / stone / tiles / ground, darker wet brick and sky-mirror puddles come with the **RAIN light**. RAIN builds with rain 1 and mortar wet 0.8. |
| `set_mortar_wet(k, frame=None)` | Lin's rice mortar soft and wet (false payoff): 0 dry cream .. 1 glossy joints + milky runs hanging from every bed joint. Keys linear. |
| `set_cracks(section, level, frame=None)` | crack overlay on both faces, growing outward from the impacts. general: 0.33 = shot 1 star round impact 0; 0.66 = shot 2 long stair-stepping cracks along the courses across the whole row; 1 = shot 3 the whole slab broken. lin: hairlines round the dents only. Keys linear. |
| `set_impact(section, slot, t, frame=None)` | one cannon shot at impact slot 0..2 (`A['wall']['impacts']`): t 0..0.06 muzzle flash + light + smoke puff at its cannon; 0.06..0.35 the ball flies in an arc; 0.35 hit: flash + light burst, dust burst (fades by 1), the decal appears and stays (general: deep dark crater; lin: shallow dent, face whole), the ball stays embedded. Slot → cannon: lin 0,1,2 → cannons 0,1,2; general → 3,4,5. Pair with `set_cracks` for the general. |
| `set_collapse(t, frame=None)` | the general's section above course 3 (z 2.5) breaks into 2-course chunks (2.2 D long, outer / inner half) that tumble to both sides with spin (0.05..0.8), the rubble mound rises out of the dust (0.35..0.85), a big dust cloud billows from the base and hangs (0.08..1). Cracks, decals, top dressing hide at 0.05. Uses the general's current height. |
| `set_smoke(level, frame=None, speed=1)` | battlefield smoke: 10 columns of soft billow balls (cannon line, camp fires, burning spots) rising, swelling and drifting; 0 .. 1 .. 1.5. |
| `set_flames(k=1, frame=None)` (= `set_lanterns`) | all fires, lanterns, stove glow, windows, tent glows: 0 out .. 1 .. 1.5 with deterministic flicker (desert.set_flames). |
| `set_army(on, frame=None)` | the enemy: 6 bronze cannons on wheeled carriages (y -22, x -16.5..18.5, facing the wall), fire pots by each gun, wicker gabions, black banners, the camp (tents y -46, 3 camp fires), stakes. On in BATTLE. |
| `set_macro(t, frame=None)` | macro presets only (see 2). |
| `clear_keys()` | drops every hook key (objects, lamps, materials, the rain overlay). |

`wall_work/t_anim.py`: ALL OK (impact flight + decal, cracks, smoke, rain scroll, collapse chunks / rubble / top course, steam, keyed height 10 → 20, wet easing, rice dent + flex, plain crack spread).

## 2. Presets (`W.PRESETS`, `W.LOC_PRESETS['wall_site']`)

| preset | area | default light | state at build | relevant lights (in contact.jpg) |
|---|---|---|---|---|
| `site_wide` | site | DAY | lin 18 / gen 21, steam | DAY, DUSK, DAWN, RAIN, BATTLE |
| `cauldron` | site | DAY | same | DAY, DAWN, DUSK, RAIN |
| `two_sections` | site | DAY | same | DAY (h18/21, h20/26), RAIN (wet 1), BATTLE (h26/30, cracks) |
| `two_sections_out` | site | BATTLE | lin 26 / gen 30, army, smoke | BATTLE: impact + crack 0.33, crack 0.66 + dents, crack 1 + collapse 0.35, collapse 1 |
| `wall_top` | site | DAY | lin 20 / gen 26 | DAY, RAIN |
| `cannon_line` | site | BATTLE | lin 26 / gen 30, army, smoke | BATTLE (plus a ball in flight) |
| `mortar_macro` | macro | BATTLE | plain joint, t 0 | BATTLE t 0 / 0.45 / 0.9 |
| `mortar_macro_rice` | macro | BATTLE | rice joint, t 0 | BATTLE t 0 / 0.36 / 0.9 |

**The macro area (`mortar_macro*`)** – the lit 3D reveal: 1 D here ≈ 2 mm. Two huge bevelled porous fired-clay bricks above and below a recessed bed joint (z -1.2..1.2, face y 0.22), a head joint rising at x -3, more courses above / below to fill the frame. ~440 calcite rhomb crystals (cool white-cyan inner glow + glints) are set into the matrix face. Warm raking fire key from the front-left + two flickering fire lamps, cool blue rim / fill (complementary), dark void behind the camera.
- **plain** (grey grainy matrix): `set_macro(t)`: t 0..0.3 the ball flies in from the front-left; 0.3 hit (flash light); the face dents slightly, a **black brittle crack** with a pale chipped lip races from the impact along the whole joint both ways and branches up / down into the bricks (0.3..0.75, reveal-order in UV), shards spall toward the camera, a short dust puff; the ball drops away (0.4..0.9).
- **rice** (creamy matrix): a **fine glowing gold web** (~1430 starch strands, sagging + bowed out of the face, small loops wrapped round single crystals) between the crystals. On the hit the face, crystals and web dent in (shape keys), the web **stretches outward and flares 2.4x, flexes back in a damped spring and holds**, glowing a little brighter after; the ball bounces back out and drops away (0.36..0.95).
Cameras `macro_plain` / `macro_rice` (same: oblique along the joint, the impact point mid-frame), `macro_front` (square-on). Any light works; BATTLE is the one tuned.

## 3. Cameras, stand points, card scales, caption check

Card scale: card height in D = `W.HEIGHT` (cast scale 1.0): **lin 3.0, general 3.3, worker 2.9, gunner 2.9**. Placeholders: `beach_man` (lin), `boss` (general), `senior_a` (worker), `senior_b` (gunner) until the film-9 cast exists.

**Caption rule: every staged head stays above y 880 of 1280** (`head_pixels`: head centre / chin px at 720x1280). All chins < 880.

| cam | loc → look_at, lens | shows | staged (feet) | head / chin px |
|---|---|---|---|---|
| `site_wide` | (-21, 36, 17) → (4, 3, 6.6), 20 | high crane from inside: tents and lantern path, the cauldron, both sections with scaffolds, ladders, hoists and banners, gate tower left, over the wall the river plain, mountains, pagodas | lin `lin_stir` (-15.15, 13.3, z 1.5), worker (-2.6, 10.8), general (6.4, 14.8) | 856/869, 778/788, 751/761 |
| `cauldron` | (-6.2, 23, 7.6) → (-11.4, 11, 3.4), 22 | the giant wok of milky rice soup (paddle, bubbles), glowing stove gap + fire mouth with logs, steam; Lin on his platform right, the general left, Lin's section + scaffold behind | lin `lin_stir`, general (-7.4, 10.6) | 617/646, 698/726 |
| `two_sections` | (0.4, 25, 7.6) → (0, 5, 6.7), 20 | front view of both sections from the site: general's taller grey section left, Lin's creamy section right, meeting at x 0; ladders, hoists, banners, brick stacks, troughs | lin (-2.8, 10.0), general (4.6, 10.4), worker (10.6, 9.4) | 846/869, 840/864, 845/868 |
| `two_sections_out` | (2, -19, 3) → (2, 0, 9), 20 | the outer faces from the field (between cannons and wall): impacts, dents, cracks, collapse | none (cast can stand at `outer_foot`) | – |
| `wall_top` | (17.5, 2.7, 18) → (3, 2.2, 13.6), 20 | on top of the general's section (gen 26: top z 14): the general mid-frame, banners and hoist behind him, field left, site + cauldron right | general (8, 2.4, `top_z('general')`) | 519/556 |
| `cannon_line` | (-23, -28.5, 3.4) → (5, -13, 5.4), 20 | behind the enemy cannon row: bronze guns and fire pots in a diagonal into depth, gunners, black banners, smoke columns, both sections and the gate | gunners (-1.2, -23.6), (5.8, -23.6) | 718/735, 710/723 |
| `macro_plain` / `macro_rice` | (-4.6, -4.4, 0.9) → (2.6, 0.2, -0.15), 22 | the joint receding to the right, impact at (1.5, 0.22, 0) | – | – |
| `macro_front` | (1, -9.5, 0.4) → (1.2, 0.2, 0), 22 | square-on to the joint | – | – |

Camera height note for `wall_top`: the camera is set for the general at 26 courses; at other heights add `0.5 x (courses - 26)` to loc z and look_at z.

### Stand points (`A['marks']`, feet; z is the floor)
`lin_stir` (-15.15, 13.3, 1.5) on the platform beside the wok (paddle in reach); `general_cauldron` (-6.4, 15.0); `lin_trough` (-5.2, 11.2) / `general_trough` (8.2, 11.4) (pouring rice soup, the buckets of soup at (-3, 8.8)); `lin_wallfoot` (-4.5, 8.4) / `general_wallfoot` (5.0, 8.6) (trowelling at the inner face); `workers` (-2.6, 10.8) (5.8, 14.6) (7.4, 14.0); `ramp` (3.5, 8, 0) → (11.3, 8, 6) plank ramp up the general's scaffold; `gate` (31, 8.5); `outer_foot` (±11, -3); `gunners` x 6 at (cannon x + 1.3, -23.6); `cannons`. On top: `A['wall']['top_z'][section]` (stand at y 1.5..3.5). **Comic slide**: `A['slide_out']` / `A['slide_in']` = path from the general's top (8, 2.4, top) down the rubble mound to the ground on the field / site side (pair with `set_collapse` ≥ 0.6). Cauldron: `A['cauldron']` centre (-11, 13.5), rim z 3.0, soup z 2.65, radius 2.85. Keep-out zones in `A['keep_out']`.

## 4. Light presets

Light model of the templates: one sun with real shadows, painted shade emission (shade_mix tint keeps brown ground from going magenta), no bounce, untooned Lambert, warm point lamps for practicals (cauldron fire 300 W shadowed + rim fire, 3 braziers, 6 red paper lanterns on poles, 2 scaffold torches, gate tunnel + pavilion lamps; BATTLE adds 3 camp fires + 3 cannon fire pots), camera-only halos, grade with bloom.

| light | key | shade | practicals | sky / ring |
|---|---|---|---|---|
| DAY | warm sun (1.80, 1.52, 1.08), az 135 el 42: rakes across the inner face | (0.10, 0.12, 0.30) | x 0.45 | blue sky, cumulus, blue ranges, pagodas, villages |
| DUSK | golden (1.75, 0.98, 0.52), az 160 el 9 | blue (0.05, 0.095, 0.25), mix 0.8 | x 1.0 | gold-orange horizon to blue, warm windows |
| DAWN | pink-gold (1.62, 1.08, 0.80), az 20 el 7 | (0.07, 0.12, 0.28) | x 0.8 | peach horizon, pale blue |
| RAIN | soft cool overcast (0.82, 0.88, 1.0), el 62, sun angle 28° | (0.15, 0.17, 0.27) | x 1.0 (lanterns pop) | grey clouds; wet sheen, puddles, rain overlay |
| BATTLE | low red-orange (1.60, 1.0, 0.56), az 262 el 12 (behind the cannons: lights the outer face) | deep blue (0.04, 0.08, 0.22), mix 0.82 | x 1.3 | smoky orange-red horizon under dark blue, smoke clouds |

Macro area overrides: raking warm key (1.55, 0.98, 0.52) from the front-left, shade (0.05, 0.08, 0.26), fire lamps 650 / 300 W, cool rim 2600 W + fill 800 W.

## 5. Measured

**Render cost** (720x1280, 12 samples, 2 threads, OIDN + grade; `wall_work/final_log.txt`, two processes in parallel): **12.2..25.1 CPU s/frame**. Highest: `cauldron` RAIN 25.1, cauldron DAY..DUSK 21-22, `two_sections` RAIN 20-22, site_wide 16-19, macro 12-15. (3D rain cards cost ~4.5 CPU s per layer: the rain is a compositor overlay for that reason.)

**Hue** (`wall_work/hue_rows.txt`, tools/hue_report.py): orange-vs-blue complementary everywhere. ALL frames: red 17.7, orange 28.0, blue 46.3, violet 1.9, magenta 3.9 (ref A whole clip: 24.5 / 34.1 / 28.6 / 4.5 / 5.0). Magenta ≤ 13.5 per frame (highest: macro plain 13.5, cauldron DAWN 12.4, site_wide DUSK 11.7). DAY frames are blue-heavy (sky); RAIN low saturation (0.14-0.18, overcast by design); macro plain 75 % red (warm-lit grey brick + blue rim, black crack). Dark fraction 0.01-0.11 (lower than ref 0.08).

**Determinism**: `digest` identical in two processes (two_sections `38de7c9b…`; mortar_macro_rice `611fcded…`).

## 6. Command line

```
python3 wall.py stills [spec ...]       # wall_work/stills 360x640 with placeholders and head pixels
python3 wall.py final  [spec ...]       # wall_work/final 720x1280 12 samples, CPU s
   spec = preset[:LIGHT[:state[:cam]]], state = comma list: h<lin>/<gen>, wet<k>, crack<g>, crackl<l>, imp<g|l><slot>@<t>, col<t>, smoke<k>, rain<k>, steam<k>, macro<t>, army0/1
   e.g. python3 wall.py final two_sections_out:BATTLE:crack0.66,impl0@1.0 mortar_macro_rice::macro0.36
python3 wall.py digest <preset>
wall_work/run_finals.sh ; python3 ../set3d8/desert_hue.py wall_work/final ; (cd wall_work; python3 t_anim.py)
```

## 7. Known gaps (honest)

- **Placeholders only** (old cast cards). Hand props of the brief (paddle in hand, trowel, brick, bucket of rice soup, linstock) belong to the cast; the set has a paddle resting in the wok, buckets of soup, trowels on the tops, fire pots by the guns. The general's slide / flying helmet is the cast's job (paths `slide_out` / `slide_in`).
- Wall faces are textured course boxes, not individual bricks: from very close (< 4 D) the bricks are flat. Cracks / dents are decals on the faces (both sides), not geometry. The collapse chunks are 2.2 x 2.5 x 1 D blocks (read as broken masonry slabs, a little "crate"-like up close); the rubble mound and dust are generic, the stump keeps 3 courses.
- The general's section is visibly taller only by courses (3 / 6 courses = 1.5 / 3 D); `two_sections` and `site_wide` show it clearly, `wall_top` mostly shows the top surface (Lin's lower section is behind the camera's view axis there; use `two_sections` or `site_wide` for the height comparison).
- Rain is a 2D screen overlay (no occlusion by near objects); at preview size (360x640) the streak layer is cropped, not scaled. Puddles mirror only the sky.
- Steam / smoke / dust are soft camera-only billow balls (no lighting from the fires beyond their tint). Smoke columns and the steam recycle per ball; keep `speed` ≤ 2.
- The macro is stylised (crystals 0.035-0.17 D boxes, web as emissive tubes); its plain crack is a ribbon overlay with a slight face dent, the joint does not physically split apart. Shards and ball are simple shapes.
- Hue: DAY frames are blue-heavy (big sky), RAIN frames are low-saturation; red is under the band in most site frames (grey brick); the dark fraction is low (airy look, as film 8).
- `cauldron` RAIN is the most expensive frame (25.1 CPU s, at the limit); everything else ≤ 22.3.
- Enemy soldiers are not modelled (stakes + banners + camp only); gunners are cast.
