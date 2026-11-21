# COLOUR: the colour pass on the 3D office (INTERIOR_DAY)

Client note: "very good, but the colours are not like the reference yet". Measured cause: the picture was magenta and pink-purple (rose wallpaper, plum ceiling, a violet ambient that turned every shade magenta), with too little blue, too little orange-brown and almost no deep darks.

The fix is at the source: `v3/set3d/office3d.py` (preset `INTERIOR_DAY`, the material builder and the grade hook) and `v3/set3d/textures.py` (artwork colours). The originals are in `v3/set3d/backup_before_colour/` (both files, the old `tex/` and the old `still_*.png`). Shots, timing, camera and acting were not changed. The whole opening was rendered again with `make.sh` (150 frames, 12 samples, post, Thai captions, narration), and the sound was mixed again with `audio/mixer.py`. The old outputs are in `v3/out/before_colour/` (including `raw/`), and the old delivery file is `deliver/opening_v3_3d_thai_sound_before_colour.mp4`.

Picture: `colour_before_after.jpg` has three rows (insert g 25, low angle g 55, two-shot g 120). Each row shows the reference frame (a/t32.0, a/t27.5, b/t07.0), the frame before the fix and the frame after.

## 1. hue_report.py, before and after

`python3 v3/tools/hue_report.py <set>`: share of chroma per hue family in percent, caption band excluded.

| Set | red | orange | blue | violet | magenta | sat | val | dark | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| Target band | 30-41 | 22-38 | 14-30 | 0-5 | 0-10 (aim 5-9) | 0.38-0.48 | 0.45-0.63 | 0.08-0.15 | |
| Reference A interiors | 40.1 | 27.6 | 21.9 | 1.1 | 8.6 | 0.47 | 0.55 | 0.09 | in |
| Reference B interiors | 36.3 | 37.7 | 13.9 | 4.5 | 5.1 | 0.38 | 0.45 | 0.15 | blue 13.9 |
| **Opening, 150 final frames (`out/frames`)**: before | 38.8 | 21.9 | 8.8 | 3.1 | **24.8** | 0.46 | 0.52 | 0.04 | OUT: orange, blue, magenta, dark |
| **Opening, 150 final frames**: after | 39.9 | 31.2 | 17.9 | 0.8 | 3.5 | 0.44 | 0.49 | 0.13 | **all in band** |
| Ten cameras, two placeholder actors (`review/quick.py`, 360x640): before | 35.3 | 13.9 | 14.1 | 5.1 | 28.0 | 0.47 | 0.49 | 0.04 | OUT: orange, violet, magenta, dark |
| Ten cameras, two placeholder actors: after | 35.0 | 25.6 | 28.3 | 1.1 | 4.2 | 0.46 | 0.47 | 0.145 | **all in band** |
| Set stills `set3d/still_*.png` (final, no actors): before | 37.4 | 17.1 | 11.1 | 4.8 | 28.0 | 0.48 | 0.49 | 0.03 | OUT: orange, blue, magenta, dark |
| Set stills `set3d/still_*.png`: after | 38.3 | 28.0 | 24.5 | 0.7 | 3.5 | 0.47 | 0.47 | 0.13 | **all in band** |

Single cameras after the fix (ten-camera set). The band applies to the sets above; single frames scatter around it, as the single reference frames do:

| Camera | red | orange | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|
| desk_fg | 38.6 | 11.7 | 37.0 | 0.9 | 6.0 | 0.48 | 0.45 | 0.15 |
| eye_two_shot | 38.9 | 26.7 | 21.7 | 1.1 | 5.6 | 0.45 | 0.47 | 0.17 |
| high_steep | 32.7 | 33.8 | 25.7 | 0.8 | 1.9 | 0.48 | 0.51 | 0.10 |
| high_two_shot | 34.9 | 30.7 | 22.7 | 1.1 | 4.3 | 0.47 | 0.49 | 0.13 |
| insert_rake | 32.2 | 37.4 | 18.3 | 0.5 | 2.1 | 0.41 | 0.45 | 0.12 |
| low_medium | 47.9 | 23.9 | 19.4 | 1.2 | 4.2 | 0.46 | 0.49 | 0.15 |
| low_rake | 45.2 | 14.3 | 25.3 | 1.1 | 3.9 | 0.47 | 0.47 | 0.17 |
| top_down | 14.1 | 42.1 | 35.7 | 1.5 | 3.0 | 0.46 | 0.51 | 0.10 |
| wide_high | 29.7 | 13.5 | 40.2 | 2.1 | 7.5 | 0.46 | 0.39 | 0.23 |
| window_side | 36.2 | 18.0 | 38.3 | 1.0 | 4.0 | 0.47 | 0.49 | 0.14 |

These numbers sit at or near the edge of the band:

- Magenta is 3.5 in the film and 4.2 on the ten cameras. That is inside the band (0-10) but under the 5-9 aim.
- Red in the film is 39.9, close to its upper limit of 41.
- Dark share on the ten cameras is 0.145, close to its upper limit of 0.15.
- Blue on the ten cameras is 28.3, close to its upper limit of 30.

## 2. What was changed (old -> new)

### Light, `PRESETS['INTERIOR_DAY']`

| Setting | Before | After | Why |
|---|---|---|---|
| `shade` (flat ambient) | (0.28, 0.255, 0.48) violet | (0.20, 0.27, 0.54) blue | Shade on warm surfaces turns blue-violet, not magenta |
| `lift` (flat dark lift) | (0.024, 0.016, 0.040) plum | (0.0, 0.010, 0.026) navy | The plum lift made every dark and every red shade magenta |
| `key` (sun), `key_dir`, `sun_angle` | (2.30, 1.65, 0.74), unchanged | unchanged | The warm orange sun was already right |
| `wall_shade` | 2.0 | per channel (2.8, 2.05, 0.7) | Red wall in shade stays deep crimson (hue 351), as the reference walls do |
| `wood_shade` (wainscot, rails, stiles) | 0.85 | (0.62, 0.95, 1.1) | Wainscot shade hue 328 -> 257 |
| `floor_shade` | 0.78 | (1.06, 1.32, 1.38) | Floor shade hue 302 -> 240-257, and the floor shade/lit ratio stays at 0.15 or more |
| `ceil_shade` | 2.6 | (3.8, 3.0, 1.8) | Ceiling boards brown and orange-brown, not plum |
| beam materials (shade multiplier) | 2.0 | (3.4, 2.6, 1.4) | Brown beams |
| `gains.wallpaper` | 0.95 | 0.85 | The crimson sun patch no longer clips (`#e43625` instead of `#fe3820`) |
| `falloff_y` | 0.34 | 0.30 | Foreground slightly less crushed, so the dark share stays at 0.15 or less |
| `grade_offset` (new; the spec grade's offset was (0.0075, 0.0035, 0.0095)) | plum black point | (0.002, 0.0045, 0.010) navy-plum | Darks are navy-plum, never black |
| `grade_saturation` (new; the spec grade's value was 1.12) | 1.12 | 1.06 | Mean saturation 0.50 -> 0.46 |

Code: `mat_lit` now also accepts a 3-tuple `shade_mul`, which tints the ambient of one surface. A scalar still behaves as before. `setup_grade` passes `grade_offset` and `grade_saturation` to `spec/grade_compositor.py` when the preset has them. `spec/` itself is unchanged.

### Albedos (`textures.py` artwork and `office3d.py` flat colours)

| Surface | Before | After |
|---|---|---|
| Wallpaper base `WALL3` | `#9c4a50` rose | `#aa3e2c` crimson-terracotta |
| Frieze `FRIEZE` | `#7a3037` | `#6a2a1e` |
| Ceiling boards | `#7d4350` plum | `#8c5030` orange-brown |
| Beam side, beam body | `#4a2238` | `#4a2616` |
| Beam chamfer strip | `#5a2c40` | `#5c3220` |
| Beam straps, bolts | `#2a2034`, `#7a6f8c` | `#22222e`, `#6f7488` |
| Floor planks `FLOOR`, seams `SEAM` | `#99695c`, `#3f2224` | `#a6764e` tan, `#2e1d22` |
| Wainscot `WOOD`, `PANEL` | `#5f2a1a`, `#7a3a21` | `#5e3018`, `#7c4620` orange-brown |
| Rug navy `NAVY` | `#233a68` | `#283a74` |
| Filing cabinets `STEEL`, `STEEL_HI` | `#51578f`, `#5f66a3` steel-violet | `#34508c`, `#42609e` blue |
| Radiators | `#6f6372`, `#4a4254` | `#5d6478`, `#3c4458` |
| Teletype body (`dark`), iron | `#2d2239`, `#3b3442` | `#20263c`, `#2f3444` |
| Telephone | `#241a2e` | `#1c1e2c` |
| Window reveal | `#b8847a` | `#b88a68` |
| Eraser block on the ledge | `#4d3f44` | `#3a3e4c` |

The v2 names (`FRIEZE`, `FLOOR`, `SEAM`, `STEEL`, `STEEL_HI`, `NAVY`, `WOOD`, `PANEL`) are re-bound in memory by `textures.COLOUR`. `v2/sets/office.py` is not modified. These were not changed: map, track, sign, clock, lamps (green), sky card, actor cards.

### How the pass went

16 passes. Each pass rendered the ten staged cameras at 360x640, ran `hue_report.py` and put the stills next to a/t27.5, a/t32.0, b/t07.0, b/t18.5 and b/t24.5. Several passes also rendered 18 opening frames small. Wrong turns along the way:

- A more crimson wall (`#a42c34`) went magenta in shade, so it was undone.
- A higher lift added blue and lifted the darks too much, so it was undone.
- A plain blue ambient left the woods and the ceiling violet. Per-surface shade tints fixed that.

## 3. Light numbers after the fix (`review/review_render.py passes` + `review_analyze.py light|heads|bloom`, final quality, 720x1280)

| Quantity | Before (REVIEW.md) | After | Target |
|---|---|---|---|
| Shade / lit, linear, floor | 0.15-0.16 | 0.155 eye_two_shot, 0.156 low_medium | 0.15-0.31 |
| ... map | 0.28-0.31 | 0.247 / 0.257 | in |
| ... wallpaper | 0.30 | 0.279 / 0.281 | in |
| ... wainscot | 0.29-0.31 | 0.207 / 0.210 | in |
| Shade hue on warm surfaces | floor 302, wallpaper 326, wainscot 328 | floor 245 / 257, wainscot 257 / 261, map 209-211 (blue), wallpaper 351-352 (deep crimson, as in the reference) | 240-260 |
| Floor lit -> cast | `#cf6d4e` -> `#513350` | `#d48653` -> `#464552` (reference a/t32.0: `#b28e71` -> `#2d2a39`) | |
| Cast-shadow edge width, eye_two_shot / low_medium (p10 / median / p90 / max, px) | 2.0 / 5.0 / 8.5 / 11.8 ; 2.0 / 9.6 / 15.5 / 21.8 | 2.0 / 5.0 / 8.5 / 11.5 ; 2.0 / 9.5 / 15.3 / 22.0 | unchanged |
| Bloom | halo only on emitters | bulb 10 percent halo 22 px; ring around the heads mean 0.03 / 0.13 levels, at most 1-3 levels | unchanged |
| Head fill / ink on screen | `#fff5f3`, `#3f2838` | `#fff6f4` (V 1.00, S 0.043), ink `#3b2b39` hero, `#2d2a39` under the brim | near `#fef7f6` / `#3a2832` |
| Wall luminance in a ring around the heads | far 97-114, near 69-81 | far 112.6, near 69.9 | 95-170 (near actor was already under the band before) |
| Canny edge density, eye_two_shot | 0.083 | 0.086 | at least 0.085 |
| Darkest tenth, eye_two_shot | `#372143` plum | `#122442` navy (hue 219) | plum-navy, not black |
| Luma p5 / p50 / p95, eye_two_shot | 0.15 / 0.26 / 0.80 | 0.131 / 0.276 / 0.770 | |
| Render cost | 18.9 CPU s per final film frame (median, 12 samples) | 17.9 CPU s (about 4.5 s on 4 threads); set stills 4.4-5.2 s wall at 16 samples, 4 threads | about 4.5-5 s |

The map stays readable in the insert. The red track and the N.Y. label are clear, because the map texture and its gains were not touched (see `colour_before_after.jpg`, top row). The white heads are still the brightest large shapes.

## 4. What remains outside or different

1. Magenta is 3.5 to 4.2: inside the band, under the 5-9 aim. The reference's magenta comes from purple costumes and curtains, which this set does not have.
2. The wall ring around the near actor is 70 (band 95-170). Before the fix it was 69-81, so it was already low. A saturated crimson wall has low luma even in the sun.
3. Red shadow surfaces stay red, not blue. The crimson wall in shade has hue 351, and the red rug border in shade has hue about 305. The reference's red walls and curtains in shade are also deep crimson.
4. The darkest tenth is navy (hue 219). The reference interiors' darkest tenth runs from plum to dark red.
5. The ink line around the heads is part of the actor cards and was not changed.
