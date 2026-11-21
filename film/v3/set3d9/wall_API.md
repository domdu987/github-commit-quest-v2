# v3/set3d9/wall.py : film 9 set ("ไอ้ช่างขนม", sticky-rice mortar of a Ming city wall, ~1370s) (bpy 5.3, Cycles CPU)

Files:
- `wall.py`: the location `wall_site` (construction site, the wall in two sections, gate tower, field + river, enemy cannon line) and the macro area (inside the mortar joint), with every hook.
- `wall_tex.py`: all artwork, painted with numpy + PIL (bricks plain / rice / old + mortar masks, stone, ground, field, pastes, rice soup, roof tiles, canvas, banners, lantern skin, crack maps + reveal-order maps, dents, drips, rain screens, macro clay / matrix, 5 skies, 5 painted rings). Cached in `tex_wall/` by a hash of the params + `TEX_V` (bump `TEX_V` after editing painter code). Glow images `pool`, `shaft`, `glint`, `wisp` are read from `v3/set3d8/tex_desert/`.
- `contact.jpg`: every preset x relevant light / state at 720x1280, 12 samples, placeholder actors (33 frames, round 2 adds `wall_top_battle`, `pour_close`, `gate_dusk`, `two_shot_low`, `aftermath_dawn` and the old oblique `macro_rice` camera), plus 6 reference frames (A t0040 t0062 t0072 t0096 t0104, B t0033). The cyan line is y 880. `contact_small.jpg` is 1/3 size. Order: `wall_work/contact_order.txt`; rebuilt by `wall_work/make_contact.py` after `wall_work/run_finals.sh`.

Work files in `wall_work/`: `final/` (the 33 finals), `make_contact.py`, `final_log.txt` (wall / CPU s, head pixels), `hue_rows.txt`, `t_anim.py` (hook test, prints ALL OK), `t_cost.py`, `run_finals.sh`, `REF_*.jpg`.

Built on `v3/set3d8/desert.py` → louvre → bakery → mine → pagoda / tower. Imported, not copied:
- `tower`: `MB`, `mat_lit`, `mat_emit`, `setup_grade`, `make_camera`, `render`, `no_bounce`, `_key`, `_show`, `_fcurves`, `placeholder_actor` (+ `PH` roles).
- `mine`: `obox`, `beam`, `rod`, `lumpy`, `chain_rod`, `_obj`, `_untoon`, `_glossy`, `_append_shader`, `_denoise`, `_mat_fire`, `setup_render`.
- `pagoda`: `_kd`, `_haze_mat`, `digest`. `bakery`: `Frame`, `_halo`, `_light`, `_mat_add`, `_basket`.
- `desert`: `set_flames` (fire flicker), `clear_keys`, `_keyval`, `_value`, `_retarget`, `_mat_alpha_k`, `_mat_sky`, `_mat_water` (river + puddles mirror the sky), `_sky` (sky dome + painted ring), `_flame_light`, `_brazier`, `_bucket`, `_jar`.

`wall.STATE` is `tower.STATE`. **No depth of field anywhere** (`apply_dof()` is a no-op).

World: 1 unit = 1 D (head), Z up, ground z 0. The wall runs along x. **Outer face y = 0 (faces -y: field, river, enemy)**, **inner face y = 5 (faces +y: the construction site)**, thickness 5. Stone plinth z 0..1; courses of 0.5 D above it (`top_z = 1 + 0.5 x courses`, max 30 courses = 16 D).
- **Walls are individual instanced bricks** (geometry-nodes instancing, `_inst_obj` / `WAL_inst_*` groups): each course object (`STATE['courses']`) is the mortar core box + one point per face brick; 12 bevelled brick meshes per kind with chipped corners / edge nicks (pale broken-clay chip faces) and hand-made jitter (`_brick_bmesh`, `_brick_variants`). Bricks stand 0.065-0.09 D proud of the core (recessed joints that cast shadow), each its own atlas cell, value and warm / grey / dark tint (Object Info random), small tilt and set-back. Damp band to a ragged tide line, run-down streaks, moss and lichen at the foot (`stain` texture, 4.5 D high, also on the plinth) plus moss cushions on the plinth ledge and at the foot (`wall_moss`). Brick piles on the site are instanced the same way (no foot stains).
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
| `set_impact(section, slot, t, frame=None)` | one cannon shot at impact slot 0..2 (`A['wall']['impacts']`): t 0..0.06 muzzle flash + light + smoke puff at its cannon; 0.06..0.35 the ball (r 0.75 D) flies in an arc **with a 9-puff smoke trail behind it** (readable at phone size); 0.35 hit: flash + light burst, dust burst (fades by 1), the decal appears and stays (general: deep dark crater; lin: shallow dent, face whole), the ball stays embedded. Slot → cannon: lin 0,1,2 → cannons 0,1,2; general → 3,4,5. Pair with `set_cracks` for the general. |
| `set_collapse(t, frame=None)` | the general's section above course 3 (z 2.5) breaks into broken-brick debris (per 2-course band 10 x 2 pieces: single bricks and broken halves of different sizes, bonded pairs, ragged 2-3 course blocks held by grey mortar beds, all instanced bevelled / chipped / snapped bricks, with mortar crumbs) that tumble to both sides with spin (0.05..0.8), ~90 mortar crumbs and brick bits fly out; pieces land, bounce once and settle; the rubble mound (lumpy mortar core + 520 loose whole / broken bricks of five sizes + 140 crumbs) pushes up out of the ground under the dust (0.35..0.85), a big three-tone dust cloud (sun-caught pale tops) billows from the base and hangs (0.08..1). Cracks, decals, top dressing hide at 0.05. Uses the general's current height. |
| `set_smoke(level, frame=None, speed=1)` | battlefield smoke: 9 columns of **hard-edged cartoon billows** (cannon line, camp fires, burning spots) rising, swelling and drifting; 0 .. 1 .. 1.5. (Round 2 removed the column over the gun at x -2.5 that read as a ghost face in `cannon_line`.) |
| `set_flames(k=1, frame=None)` (= `set_lanterns`) | all fires, lanterns, stove glow, windows, tent glows: 0 out .. 1 .. 1.5 with deterministic flicker (desert.set_flames). |
| `set_army(on, frame=None)` | the enemy: 6 bronze cannons on wheeled carriages (y -22, x -16.5..18.5, facing the wall), fire pots by each gun, black banners (cast no shadow), the camp (tents y -46, 3 camp fires), stakes; **the field in front of the wall** (gabions, sharpened stake rows, scorched patches, a broken cart, 3 fire pots + a burning-field lamp that warm-lights the collapse debris); **the host on the far horizon** (`army_horizon`: 34 black / red banners + a dust bank on an arc ~100 D beyond the gate, visible from `gate_dusk` over the wall while the near army stays hidden behind it). On in BATTLE; `gate_dusk` turns it on at DUSK. |
| `set_macro(t, frame=None)` | macro presets only (see 2). |
| `clear_keys()` | drops every hook key (objects, lamps, materials, the rain overlay). |

`wall_work/t_anim.py`: ALL OK, 17 checks (impact flight + **smoke trail** + decal, cracks, smoke, rain scroll, collapse chunks / rubble / top course, steam, keyed height 10 → 20, wet easing, rice dent + flex, **rice held state at t 0.9 (dent ring glows)**, plain crack spread, **set_army + set_smoke at DUSK (gate_dusk)**).

## 2. Presets (`W.PRESETS`, `W.LOC_PRESETS['wall_site']`)

| preset | area | default light | state at build | relevant lights (in contact.jpg) |
|---|---|---|---|---|
| `site_wide` | site | DAY | lin 18 / gen 21, steam | DAY, DUSK, DAWN, RAIN, BATTLE |
| `cauldron` | site | DAY | same | DAY, DAWN, DUSK, RAIN |
| `two_sections` | site | DAY | same | DAY (h18/21, h20/26), RAIN (wet 1), BATTLE (h26/30, cracks) |
| `two_sections_out` | site | BATTLE | lin 26 / gen 30, army, smoke | BATTLE: impact + crack 0.33, crack 0.66 + dents, crack 1 + collapse 0.35, collapse 1 |
| `wall_top` | site | DAY | lin 20 / gen 26 | DAY, RAIN |
| `wall_top_battle` | site | BATTLE | lin 26 / gen 30, army, smoke | BATTLE (shot 19 start: the general on the 30-course top; camera = wall_top + 2 D in z) |
| `pour_close` | site | DAY | lin 18 / gen 21, steam | DAY (shot 2: Lin at his rice-mortar trough by the cauldron) |
| `gate_dusk` | site | DUSK | lin 18 / gen 21, steam, **army on, smoke 0.6** | DUSK (shot 4: the gate tower; the host's banners and dust on the horizon) |
| `two_shot_low` | site | DAY | lin 18 / gen 21, steam | DAY (shot 6: low medium two-shot, general left, Lin right) |
| `aftermath_dawn` | site | DAWN | lin 26 / gen 30, preset `state` = `impl0@1.0,impl1@1.0,impl2@1.0,crackl1.0` | DAWN (shot 17: Lin's outer face dented but whole) |
| `cannon_line` | site | BATTLE | lin 26 / gen 30, army, smoke | BATTLE (plus a ball in flight) |
| `mortar_macro` | macro | BATTLE | plain joint, t 0, camera `macro_front` | BATTLE t 0 / 0.45 / 0.9 |
| `mortar_macro_rice` | macro | BATTLE | rice joint, t 0, camera `macro_front` | BATTLE t 0 / 0.36 / 0.9 (+ t 0.9 on the old oblique `macro_rice` camera) |

A preset may carry `state` (a CLI state string, see 6) applied after the preset defaults.

**The macro area (`mortar_macro*`)** – the lit 3D reveal, rebuilt in round 2 to read on a phone like ref A t0104 (one focal point dead centre, a few graphic lines, gold against blue-grey): 1 D here ≈ 2 mm. Big bevelled fired-clay bricks above and below a recessed bed joint (z -1.2..1.2, face y 0.22), a head joint at x -3. **The bricks sit in cool, low-detail shade**: pore bump halved (0.25), and light linking keeps the warm key + fire lamps on the joint only (matrix face, crystals, web / cracks, ball, shards); the bricks get only the cool rim / fill and the painted blue shade. ~130 **large faceted calcite gems** (convex hulls of jittered rhombs, 0.1-0.27 D) with a **cyan inner glow**, most in the window round the impact. Embers, hard-edged smoke billows, a dark void behind the camera.
- **plain** (grey grainy matrix): `set_macro(t)`: t 0..0.3 the ball flies in from the front-left; 0.3 hit (flash light); the face dents slightly; **5 thick black cracks** (two along the joint both ways, up-right and down-left into the bricks, a short spur) with a pale chipped lip and a **hot orange running front** at the tip race from the impact (0.3..0.75, reveal order in UV), drawn in front of the crystals; 48 **brick-red and grey grit shards** spall toward the camera, a small hard-edged dust puff; the ball drops away (0.4..0.9).
- **rice** (creamy matrix): an **ordered net of 54 thick gold strands** (12 spokes radiating from the impact, 3 elliptical rings, glowing knots, three long strands with diamond cross-ties along the joint both ways), in front of the crystals. On the hit the face, crystals and web dent in (shape keys), a bright ring pulses out over the net (0.33..0.62), the web stretches, flexes back in a damped spring and holds; **held state from t 0.36 on: a glowing gold dent ring round the impact and the web ~1.7x brighter** (clearly different from t 0 at 0.9); the ball bounces back out and drops away (0.36..0.95).
Cameras: **`macro_front` (default of both presets)**: near square-on, impact point dead centre, the joint a horizontal band through the middle third. The old oblique `macro_plain` / `macro_rice` cameras are kept (pass the cam name, e.g. `mortar_macro_rice::macro0.9:macro_rice`). Any light works; BATTLE is the one tuned.

## 3. Cameras, stand points, card scales, caption check

Card scale: card height in D = `W.HEIGHT` (cast scale 1.0): **lin 3.0, general 3.3, worker 2.9, gunner 2.9**. Placeholders: `beach_man` (lin), `boss` (general), `senior_a` (worker), `senior_b` (gunner) until the film-9 cast exists.

**Caption rule: every staged head stays above y 880 of 1280** (`head_pixels`: head centre / chin px at 720x1280). All chins < 880.

| cam | loc → look_at, lens | shows | staged (feet) | head / chin px |
|---|---|---|---|---|
| `site_wide` | (-16, 31, 17.5) → (3, 5, 1.2) | high crane from inside, tilted down (the site fills ~80 % of the frame, sky ~20 %): the cauldron, brick piles, cart, timber, baskets in front, both sections with scaffolds, ladders, hoists and banners, gate tower left, over the wall the river plain, mountains | lin `lin_stir` (-15.15, 13.3, z 1.5), worker (-2.6, 10.8), general (6.4, 14.8) | 838/852, 703/714, 669/680 |
| `cauldron` | (-6.2, 23, 7.6) → (-11.4, 11, 3.4), 22 | the giant wok of milky rice soup (paddle, bubbles), glowing stove gap + fire mouth with logs, steam; Lin on his platform right, the general left, Lin's section + scaffold behind | lin `lin_stir`, general (-7.4, 10.6) | 617/646, 698/726 |
| `two_sections` | (0.4, 28, 15.5) → (0, 5, 4.6) | front view of both sections from the site (round 2: the lower 40 % dressed with a hand cart, mortar buckets, plank stack, baskets, a tool rack, loose bricks, a second brazier, two more workers): general's taller grey section left, Lin's creamy section right, meeting at x 0; ladders, hoists, banners, brick stacks, troughs | lin (-2.8, 10.0), general (4.6, 10.4), workers (10.6, 9.4), (-6.8, 11.5), (2.4, 11.4) | 771/784, 773/786, 766/779, 803/816, ~802/815 |
| `two_sections_out` | (3, -13.5, 2.1) → (3, 0, 8.4), 20 | pushed in: the outer faces fill the frame (wall ~y 360-1000); stakes, a gabion and a fire pot in the foreground; glowing orange horizon behind the wall; impacts, dents, cracks (thicker: readable at phone size), warm-lit collapse | none (cast can stand at `outer_foot`) | – |
| `wall_top` | (18.5, 2.6, 17.0) → (1, 3.2, 14.6), 20 | lower, looking along the general's top (gen 26): brick-paved walkway (staggered pavers, three tints), crenellated brick parapet on the outer edge, mortar tubs, the hoist, banners; a worker behind the general | general (8, 2.4, `top_z`), worker (4.2, 3.9, `top_z`) | 556/590, 573/598 |
| `wall_top_battle` | (18.5, 2.6, 19.0) → (1, 3.2, 16.6), 20 | the same at 30 courses (+2 D in z), BATTLE sky | general (8, 2.4, `top_z`) | 556/590 |
| `pour_close` | (-0.4, 12.9, 3.6) → (-5.4, 10.6, 1.6), 24 | close on Lin's rice-mortar trough by the cauldron (shot 2) | lin `lin_trough` (-5.2, 11.2) | 524/603 |
| `gate_dusk` | (14, 26, 21) → (31, 2, 9.5), 20 | high from the site toward the gate tower and over the wall to the horizon (near army hidden behind the wall) | – | – |
| `two_shot_low` | (-4.6, 22.2, 1.8) → (-6, 14, 1.3), 24 | low medium two-shot by the cauldron, wall + scaffold behind (shot 6) | general `two_shot_general` (-4.4, 16.6), lin `two_shot_lin` (-7.6, 16.4) | 431/510, 492/561 |
| `aftermath_dawn` | (-11.5, -15.5, 2.4) → (-11.5, 0, 7.6), 20 | Lin's outer face from the field at DAWN: three dents with embedded balls, hairlines, the section whole (shot 17) | – | – |
| `cannon_line` | (-25, -31, 3.6) → (0, -13.5, 5.6), 20 | behind the enemy cannon row: the hero cannon now fully in frame, guns and fire pots in a diagonal into depth, gunners, banners, smoke columns, both sections and the gate | gunners (-1.2, -23.6), (5.8, -23.6) | 723/738, 716/728 |
| `macro_plain` / `macro_rice` | (-4.6, -4.4, 0.9) → (2.6, 0.2, -0.15), 22 | the joint receding to the right, impact at (1.5, 0.22, 0) | – | – |
| `macro_front` | (1.4, -8.6, 0.25) → (1.5, 0.22, 0), 24 | near square-on, impact dead centre, joint a horizontal band through the middle third (default of both macro presets) | – | – |

Camera height note for `wall_top`: the camera is set for the general at 26 courses; at other heights add `0.5 x (courses - 26)` to loc z and look_at z.

### Stand points (`A['marks']`, feet; z is the floor)
`lin_stir` (-15.15, 13.3, 1.5) on the platform beside the wok (paddle in reach); `general_cauldron` (-6.4, 15.0); `lin_trough` (-5.2, 11.2) / `general_trough` (8.2, 11.4) (pouring rice soup, the buckets of soup at (-3, 8.8)); `lin_wallfoot` (-4.5, 8.4) / `general_wallfoot` (5.0, 8.6) (trowelling at the inner face); `workers` (-2.6, 10.8) (5.8, 14.6) (7.4, 14.0); `ramp` (3.5, 8, 0) → (11.3, 8, 6) plank ramp up the general's scaffold; `gate` (31, 8.5); `outer_foot` (±11, -3); `gunners` x 6 at (cannon x + 1.3, -23.6); `cannons`. On top: `A['wall']['top_z'][section]` (stand at y 1.5..3.5). **Comic slide**: `A['slide_out']` / `A['slide_in']` = path from the general's top (8, 2.4, top) down the rubble mound to the ground on the field / site side (pair with `set_collapse` ≥ 0.6). Cauldron: `A['cauldron']` centre (-11, 13.5), rim z 3.0, soup z 2.65, radius 2.85. Keep-out zones in `A['keep_out']`.

## 4. Light presets

Light model of the templates: one sun with real shadows, painted shade emission (shade_mix tint keeps brown ground from going magenta), no bounce, untooned Lambert, warm point lamps for practicals (cauldron fire 300 W shadowed + rim fire, 3 braziers, 6 red paper lanterns on poles, 2 scaffold torches, gate tunnel + pavilion lamps; BATTLE adds 3 camp fires + 3 cannon fire pots), camera-only halos, grade with bloom.

| light | key | shade | practicals | sky / ring |
|---|---|---|---|---|
| DAY | golden late-morning sun (1.95, 1.42, 0.80), az 135 el 32 + warm bounce sun from below (1.0, 0.62, 0.34) x 0.28; warm aerial dust haze from the mist pass (`air` #f2c88c k 0.42 from 18 D) + compositor sun beams (`beams` 0.06, round 2) | blue (0.08, 0.11, 0.30): the complementary blue is only in the shade | x 0.6 | sky hazed pale gold toward the horizon, ranges, villages |
| DUSK | golden (1.75, 0.98, 0.52), az 160 el 9 | blue (0.05, 0.095, 0.25), mix 0.8 | x 1.0 | gold-orange horizon to blue, warm windows |
| DAWN | pink-gold (1.62, 1.08, 0.80), az 20 el 7 | (0.07, 0.12, 0.28) | x 0.8 | peach horizon, pale blue |
| RAIN | soft cool overcast (0.82, 0.88, 1.0), el 62, sun angle 28° | (0.15, 0.17, 0.27) | x 1.0 (lanterns pop) | grey clouds; wet sheen, puddles, rain overlay |
| BATTLE | low red-orange (1.60, 1.0, 0.56), az 262 el 12 (behind the cannons: lights the outer face) | deep blue (0.04, 0.08, 0.22), mix 0.82 | x 1.3 | smoky orange-red horizon under dark blue, smoke clouds |

Macro area overrides: raking warm key (1.55, 0.98, 0.52) from the front-left, shade (0.05, 0.08, 0.26), fire lamps 650 / 300 W, cool rim 2600 W + fill 800 W.

## 5. Measured

**Render cost** (720x1280, 12 samples, 2 threads, OIDN + grade; `wall_work/final_log.txt`, two processes in parallel), **round 2, on the current container**: 19.0..33.3 CPU s/frame. Note: this container is ~1.45x slower than round 1's: the unchanged round-1 code (`bak_r1`) measures two_sections DAY 27.2 / cauldron DAY 29.4 / wall_top DAY 25.1 / mortar_macro_rice 20.5 CPU s here (round 1 logged 18.3 / 21.6 / 17.9 / ~18). Round 2 is at or below round 1 on the same machine (two_sections 23.9, cauldron 28.9-29.3, wall_top 19.5, macro 19.0-22.0); savings: the transparent haze ring is dropped wherever the free compositor mist 'air' pass exists (now all five lights; ~2.5 CPU s). Per frame: site_wide 23.5-27.2 (RAIN 27.2, BATTLE 25.7), cauldron 29.2-29.6 (RAIN 33.3), two_sections 23.2-27.7, wall_top 19.5-21.2, cannon_line 20.6-21.0, two_sections_out 24.0-28.0, pour_close 26.8, gate_dusk 21.9, two_shot_low 26.9, aftermath_dawn 22.2, macro 19.0-22.0. Fixed overhead ~6.5 CPU s (sync + OIDN + compositor), ~1.9 CPU s per sample. (3D rain cards cost ~4.5 CPU s per layer and 3D sun-beam cards ~6: rain and beams are compositor layers for that reason; `_beams` cards stay off unless P['beam_cards'].)

**Hue** (round 1 numbers, not re-measured in round 2; `wall_work/hue_rows.txt`, tools/hue_report.py): ALL frames red 32.8, orange 33.6, blue 23.0, violet 2.8, magenta 4.8 (ref A whole clip: 24.5 / 34.1 / 28.6 / 4.5 / 5.0). DAY frames are now warm (site_wide DAY orange 68.7 / blue 0.8, two_sections DAY 72.5 / 1.9, wall_top DAY 48.7 / 8.7): the blue sits only in the shadows; if DAY should read cooler, lower `air` k (0.42) in LIGHTS['DAY']. Magenta ≤ 12.7 per frame (cauldron DAWN). Dark fraction 0.01-0.04.

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

## 6b. Round 2 look changes (QA_ART / QA_TECH)

- **Billows (steam, smoke, dust, trail)**: `_mat_dust` is a stylised cartoon billow: hard silhouette (alpha steps up within a thin facing band), flat two-tone cel shading split on the normal (lit top / blue-shifted shade), a thin darker ink rim, no noise holes; every billow mesh gets 2 subdivision levels + smooth shading (`_billow_round`) so the hard edge is a smooth curve. Same names, same `op` value, same hooks.
- **Skies** (`wall_tex.sky`, TEX_V w9.19): DAY = warm blue (no white top third), crisp cartoon clouds (`disc_clouds`: rows of discs with flat bottoms, gold-lit tops, lavender bottoms, brighter toward the sun, as ref A t0062). BATTLE = dark smoke banks with thin fire-lit undersides, plus an orange-red glow band low behind the wall on the field side (az 90). The painted sky dome is masked out of the mist 'air' pass (object index 7 + ID mask), so the air no longer bleaches it.
- **BATTLE**: a warm shadowless `city_glow` sun lights the inner (site-side) faces, so `two_sections` BATTLE is no longer near-black; crack overlays are drawn thicker (wk 3.4 general / 2.6 lin).
- **Blown highlights** (QA_TECH 8): DAY sun disc / glow lowered, DAY compositor beams 0.10 → 0.06 with threshold 0.55 → 0.7, steam no longer a soft wash. Full-size site_wide / two_sections / wall_top DAY: 0.00 % clipped pixels in the top third (0.03-0.2 % in the whole frame: fire cores).
- **RAIN / BATTLE** now also have a mist 'air' pass (`#9aa6b8` 0.3 / `#a85a40` 0.22).

## 7. Known gaps (honest)

- **Render budget**: on the current (slower) container cauldron (29-33), site_wide RAIN/BATTLE, two_sections RAIN/BATTLE, two_sections_out impact frames, pour_close and two_shot_low exceed 25 CPU s; the same frames from round-1 code are as expensive or more here (see 5). If the 25 s budget is absolute on this hardware, the remaining lever is samples or fewer lamps (fixed overhead ~6.5 s + ~1.9 s/sample).
- `two_sections_out`: the upper half above the wall is still mostly plain navy (the orange horizon glow sits behind the wall and shows mainly through the collapse gap).
- `gate_dusk`: the host on the horizon is small (banners ~10-15 px tall at 720 wide); the battlefield smoke columns sit behind the gate tower from this camera.
- `aftermath_dawn` shows the dents in blue DAWN shade (the sun is behind the wall); no "today" weathered variant was made.
- Steam columns read as stacked smooth puffs (cartoon), not a continuous plume.

- **Placeholders only** (old cast cards). Hand props of the brief (paddle in hand, trowel, brick, bucket of rice soup, linstock) belong to the cast; the set has a paddle resting in the wok, buckets of soup, trowels on the tops, fire pots by the guns. The general's slide / flying helmet is the cast's job (paths `slide_out` / `slide_in`).
- Only the two working sections are per-brick geometry; the old wall, stub and gate tower are still textured boxes. Cracks / dents are decals floating ~0.03 D in front of the brick faces, not geometry. The collapse stump keeps 3 courses. Collapse dust is limited to 16 + 6 billows by the render budget (each billow ~0.4 CPU s).
- Macro: the thin back joints (head joint, joints above / below) are flat quads without crystals; the brittle crack is still ribbons on the face (no physical split).
- The general's section is visibly taller only by courses (3 / 6 courses = 1.5 / 3 D); `two_sections` and `site_wide` show it clearly, `wall_top` mostly shows the top surface (Lin's lower section is behind the camera's view axis there; use `two_sections` or `site_wide` for the height comparison).
- Rain is a 2D screen overlay (no occlusion by near objects); at preview size (360x640) the streak layer is cropped, not scaled. Puddles mirror only the sky.
- Steam / smoke / dust are soft camera-only billow balls (no lighting from the fires beyond their tint). Smoke columns and the steam recycle per ball; keep `speed` ≤ 2.
- The macro is stylised (crystals 0.035-0.17 D boxes, web as emissive tubes); its plain crack is a ribbon overlay with a slight face dent, the joint does not physically split apart. Shards and ball are simple shapes.
- Hue: DAY frames are now orange-dominant (see 5); RAIN frames are low-saturation; the dark fraction is low (airy look, as film 8). Sun beams (compositor glare at quarter resolution) streak from the brightest areas (fires) away from the sun's screen position, set by a render / frame handler from the scene camera.
- `cauldron` RAIN is the most expensive frame (24.2 CPU s); everything else ≤ 21.6.
- Enemy soldiers are not modelled (stakes + banners + camp only); gunners are cast.
