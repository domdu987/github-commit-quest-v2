# v3/set3d_kitchen: the kitchen (shots 15 and 26), bpy 5.3, Cycles CPU

A table corner by a four-pane window in a Long Island cottage, September 1938 (shot plan, build-order step 10, sets_needed "kitchen").
It is built the way the office is built: `kitchen3d.py` imports `v3/set3d/office3d.py` and uses its light model and helpers
(`mat_lit` two-tone key plus emission ambient, `mat_emit`, `mat_card`, `add_hull` ink hulls, `MB` mesh builder, `no_bounce`,
`setup_render`, `setup_grade`, `make_camera`). Nothing in `set3d/` is edited. Only what the one planned camera sees exists.

## Files

| file | what |
|---|---|
| `kitchen3d.py` | the set: `build(light)`, `set_state(...)`, `anchors()`, `wb_point(u, y)`, CLI `python3 kitchen3d.py <light> [preview\|final] [samples]` (stills of the three cameras into `work/`) |
| `kitchen_tex.py` | the kitchen's own artwork as SVG -> PNG through `set3d/raster.js` (Chromium), sha1 cache `tex/manifest.json`: `oilcloth`, `kwall`, `curtain`, `toast`; sequences `steam` (24-frame loop), `drizzle` (24-frame loop), `wave` (92 frames, one per film frame g 1873-1964, lightning in `LIGHTNING`), `crack` (6 frames from g 1923) |
| `kitchen_geom.py` | bpy-free numbers (weather-box points, cameras, cup rest) for the take scripts and post |
| `kshot.py` | the shared take machinery: arm card, render loop, plate/matte layers, streak post (post.py's own functions), contact sheet |
| `kqa.py` | QA numbers, meta.json, cues.json, contact.jpg of a take |

Paper artwork comes from `v3/paper/tex/registry.json` (read only): `newspaper` (the folded front page), `newspaper_bleed` f_00-f_11 (drop and ink bleed on ฝนตก), `calendar_pad_21`.
Office textures reused read only: `wainscot.png`, `planks.png`.

## World

1 unit = 1 D, Z up. Window wall = plane y = 0 (room toward -y). Table top z = 1.30 (x -1.6..0.98, y -1.95..-0.02, red-check oilcloth with a 0.24 D drop).
Window glass opening x -0.40..0.90, z 1.98..3.06, one mullion and one transom (four panes 0.65 x 0.54), sill board at z 1.90-1.98, reveal 0.2 D,
exterior card at y 0.9 (x -1.9..2.3, z 0.9..4.1, 300 px per D), curtains (blue gingham) at both sides on a brass rod, calendar pad 21 left of the window.

The newspaper: the front page at 0.9 scale (1.35 x 1.755 D), folded in half, its lower half (with the weather box) facing the lens: a 0.075 D bottom
margin lies flat on the table (the saucer stands on its corner), then the page leans back 62 degrees onto a bread box; the folded-back upper half
hangs behind. `wb_point(u, y)` gives the world point of page coordinate (u, y) in the registry's page units (1.5 x 1.95, y down), e.g. the weather-box
centre `wb_point(1.0, 1.42)` = (0.225, -0.944, 1.638). Text extents measured on the texture: header y 1.051-1.135, ฝนตก 1.288-1.47, ลมกระโชก 1.536-1.65.

Cup and saucer (cream enamel, navy rim; coffee disc; spoon; steam card) are rigged: `saucer_rig` stands on the table at `CUP_REST` (0.38, -1.40),
the `cup_rig` (cup, coffee, steam) is its child. Toast plate at (-0.50, -1.50). Chair at the right end of the table (out of the table framing; `chair` 0..1 shoves it back).

## Cameras (`A['cams']`, 22 mm)

| name | loc | look_at | use |
|---|---|---|---|
| `table` | (0.225, -2.42, 1.80) | (0.225, -0.30, 1.07) | THE TABLE FRAMING (end of 15, 26 after the snap): weather box centred, its Thai between y 300 and 570, ฝนตก 76 px tall, the window with four panes above the paper, cup at right |
| `steep` | (0.225, -1.62, 2.30) | weather-box centre | start of 15: about 44 degrees down, tight on the weather box (ฝนตก about 150 px) |
| `window_tight` | (0.25, -1.05, 2.48) | (0.25, 0, 2.50) | start of 26: the four panes fill the frame |

## Lights (`build(light)`)

| preset | key (one sun) | ambient (SHADE) | window card | notes |
|---|---|---|---|---|
| `kitchen_grey` | (0.56, 0.53, 0.54), from front-left above (`key_dir` (0.42, 0.62, -0.66)), angle 2.0 deg: soft overcast shadows | (0.25, 0.27, 0.52) blue-violet | drizzle loop at 1.0 | dull drizzle morning; the grey window is the brightest thing |
| `kitchen_storm` | (0.28, 0.20, 0.125): a weak warm lamp-like key, same direction, angle 4.0 deg | (0.05, 0.072, 0.20) deep blue; ambient falls by 1.2 x y / 9 toward the lens | wave sequence at 0.85, x 1.6 in lightning | lightning: a second sun through the window (`flash_sun`, `flash_dir` (-0.15, -0.75, -0.62)) pulsed by `set_state(lightning=...)`, hidden when 0 |

## `set_state(...)`

`cup=(x, y, z, rot)` of the cup rig on the saucer, `saucer=(x, y, z, rot)` on the table (None = at rest), `ripple=(phase, amplitude)` rings on the coffee
(Wave texture, rings travel outward as the phase falls), `steam=k` (an integer frame of the 24-frame loop; a float raises TypeError; None hides), `window=('drizzle'|'wave', k)`, `flutter=(t, amp)` (page vertices
re-posed: a wave across the leaning page plus the free top-left corner lifting), `bleed=k` (swap the page to `newspaper_bleed` f_k), `lightning` 0..1,
`crack=k` (pane crack card, None hides), `chair` 0..1, `drop=(x, y, z)` (falling drop, None hides).

## Cost

720x1280, 8 samples, 2 threads: 5.8 s per frame on an idle machine, 6.3 to 6.6 s with other renders running (12 samples: 8.5 s, measured identical to 8 samples:
mean difference 0.25 of 255).
