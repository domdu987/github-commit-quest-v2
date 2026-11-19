# REVIEW of the office set (`v2/sets/office.py`)

Independent review and repair, 2026-11-11. The reviewer did not build the set. Everything below was re-rendered and re-measured with `v2/sets/review.py`; nothing is taken from the builder's report.

- Reference frames used: `ref/b/t07.0`, `b/t18.5`, `b/t23.0`, `a/t27.5` (style) and `b/t03.0`, `b/t05.5`, `b/t21.0` (staging).
- Comparison sheet: `review_compare.jpg` (top row: the four style references with our two-shot and wide between them; bottom row: the staging references with our medium and two-shot carrying two white discs, and the insert).
- "Builder" = the set as delivered (copy kept in `v2/tmp/rev/office_orig.py`, renders `v2/tmp/rev/v0_*.png`). "Repaired" = `office.py` now (renders `v2/tmp/rev/final_*.png` and the `office_*.png` in this folder).

## Verdict

The builder's set was sound in structure (staging, perspective, anchors, state, speed) and passed the five acceptance numbers, but next to the reference it read as a flat vector illustration in one orange-brown family with a pale map in the middle. After the repair it reads as the same film as the clip B throne room: rose patterned wall, old-gold and teal map, walnut wainscot, one navy rug, cream only as accents, painted light inside every shape. All acceptance ranges still pass, the contract checks pass, and the remaining differences are minor (listed at the end).

## Step 1. Likeness: what I saw

| # | Check | Builder | Repaired |
|---|---|---|---|
| 1 | Colour blocking | Wall `#ad6039`, wainscot, plank floor and map land all orange-tan: one hue family from ceiling to floor, mid colour of the frame `#6d524d` to `#98775f` (hue 9 to 26). The reference separates bands by hue (crimson, grey stone, navy, gold); its mid colour is `#743e3f`, `#5d4b57`. Green was a second block on the right (cabinets, plus shades and sign: 3.8 percent of the wide, 2.8 percent of the two-shot; clip B interiors 0.1 to 0.8 percent). `spec/LOOK_SPEC.md` 3.2 had already resolved this (rose wall, steel-violet cabinets) because orange paper swallows warm costumes. | Rose wall `#9c3139` with a tan-gold sprig, frieze `#7a3037`, walnut wainscot, mauve-brown planks, steel-violet cabinets, navy rug. Mid colour now `#6b474f` (hue 347) in the two-shot. Green 1.7 percent of the wide and 1.9 percent of the two-shot (lamp shades and sign only). |
| 2 | Fills | Flat. Zoomed crops show the reference shades every surface with soft gradients (drapery folds, stone, cushion, carpet); the builder had gradients only on the cabinets, the fg desk and the wall pool. This was the largest single difference at full resolution. | Every inked shape carries a soft top-light / plum-shade overlay; panels, drawers, sign, dials, coat, baskets and lamp shades have stronger or round-form shading; the map sheet has a light pool, old-paper corners and the frame's shade; floor and rug have soft light and dark patches. Gradients only, no filters. |
| 3 | The map (largest light area, directly behind both heads) | Land `#c9ab78`, sea `#82abb8`: pale, low in saturation, and flat (texture 5.3 on the sea against 9 to 22 on reference surfaces). Ring behind the hero's head 162 of 255, at the top of the 95 to 170 range. | Land old gold `#c49b58`, sea teal `#6b9aad` with engraved water lining and slate isobars. Ring behind heads 148 and 125. Sea texture 7.8. The title strip, date slip and station dots stay cream. |
| 4 | White heads and the red line | Read, but against a pale chart. The red track was 4.8 px in the two-shot, thinner than the puppet's 8 px ink. | Two white discs with plum outlines pasted at the marks read instantly in the wide, two-shot, medium and push-in (`review_compare.jpg`, `v2/tmp/rev/final_*_discs.png`); so do the real puppets from `v2/puppet/puppet.py` (`final_*_cast.png`). Track 5.7 px in the two-shot, red on teal. |
| 5 | Line weight and colour | Ink `#2a1712`, 3.0 px silhouettes, 1.5 px details at 150 px per D: inside the measured 2 to 6 px, warm near-black. Thin-dark-line share (black-hat over 28) 0.102 to 0.120 against 0.088 to 0.105 in the three clip B interiors: matched. Uniform weight on every object. | Unchanged, plus 1.2 to 1.3 x on the largest props (map frame, sign, clock, cabinets, coat). Thin-dark-line share 0.095 to 0.108. |
| 6 | Density of drawn pattern | Wallpaper motif at 0.32 x 0.38 D pitch (reference fleur-de-lis 0.32 x 0.38 D): right pitch, but the motif was two tints of the same orange and nearly invisible. About 30 objects in the wide, more than 8 behind the actors. | Same pitch, tan-gold sprig on rose with a dark edge. Surface texture (luminance std after a 3 px Gaussian): wall 16.9, rug 14.4, floor 12.8, wainscot 13.6 (reference backdrop 22.2, carpet 9.3 to 11.9, stone floor 17.3). |
| 7 | Where the light sits | Luminance rows (8 rows, top to bottom) two-shot `71 110 132 140 115 88 102 65`: right shape, second row a little bright. | Two-shot `68 93 119 130 102 89 97 68` against the reference b/t07.0 `66 90 103 125 102 87 86 70`. The warm pool is now a saturated screen colour, so the lit rose stays rose instead of going salmon. |
| 8 | Lamp glow | Halo measured on the isolated light layer: 10 percent point 11 px beyond the bulb on the side pendants in the wide (1 px under the range), 15 px in the two-shot, 20 px in the medium. | 14 to 18 px (wide), 18 to 24 px (two-shot), 24 px (medium). Target 12 to 24. |
| 9 | Hard-edged dark block left of the fg chair | The chair's shade was one rectangle 0.3 D wider than the chair; it darkened the rug in a straight-edged block (visible in the wide). | Clipped to the chair parts. |

## Step 2. Numbers

Tools: `ref/crops/env/tools/metrics.py` (`stats`: saturation, Canny 60/140, colour bins; caption band y 850 to 960 masked), featureless 40 px blocks (high-pass sigma 3, std under 3), mean luminance of 8 rows (top = row 1, middle = mean of rows 4 and 5, bottom = row 8; this reproduces the spec's 66 / 114 / 70, 66 / 131 / 43, 63 / 131 / 52 for the three clip B interiors), ring behind each head (0.55 to 0.95 D from the head centre, heads at the real puppet heights: hero y = -2.47, boss y = -2.87), and `spec/measure_color.py` (`stats`, `palette`).

### 2.1 Acceptance table

Acceptance: saturation 0.40 to 0.50; edge density at least 0.085 in the two-shot (at least 0.05 anywhere); featureless blocks at most 0.25; luminance top / middle / bottom about 65 / 105 to 130 / 40 to 70 in the wide and the two-shot; wall behind heads 95 to 170.

| Frame | Saturation | Canny edge | Featureless | Luminance top / middle / bottom | Behind heads (hero, boss) |
|---|---|---|---|---|---|
| builder, wide | 0.481 | 0.121 | 0.061 | 62 / 112 / 43 | 162, 138 |
| builder, two-shot | 0.458 | 0.112 | 0.034 | 71 / 128 / 65 | 162, 138 |
| builder, medium | 0.431 | 0.109 | 0.029 | 104 / 146 / 98 | 162, 158 |
| builder, insert | 0.431 | 0.113 | 0.015 | 122 / 150 / 92 | - |
| **repaired, wide** | 0.485 | 0.122 | 0.057 | 58 / 105 / 44 | 148, 125 |
| **repaired, two-shot** | 0.459 | 0.110 | 0.031 | 68 / 116 / 68 | 148, 125 |
| **repaired, medium** | 0.436 | 0.104 | 0.021 | 89 / 131 / 95 | 148, 145 |
| **repaired, insert** | 0.437 | 0.104 | 0.017 | 98 / 133 / 87 | - |
| repaired, two-shot + white discs | 0.444 | 0.107 | 0.040 | 68 / 127 / 68 | - |
| repaired, two-shot + real puppets | 0.451 | 0.111 | 0.027 | 68 / 119 / 68 | - |
| repaired, medium + real puppets | 0.425 | 0.105 | 0.025 | 89 / 135 / 95 | - |
| repaired, wide + real puppets | 0.480 | 0.122 | 0.057 | 58 / 107 / 44 | - |
| reference b/t07.0 | 0.472 | 0.114 | 0.092 | 66 / 114 / 70 | - |
| reference b/t18.5 | 0.319 | 0.110 | 0.098 | 66 / 131 / 43 | - |
| reference b/t23.0 | 0.373 | 0.089 | 0.213 | 63 / 132 / 52 | - |
| reference a/t27.5 | 0.738 | 0.020 | 0.536 | 89 / 64 / 27 | - |
| reference b/t03.0 | 0.274 | 0.024 | 0.487 | 67 / 141 / 55 | - |
| reference b/t05.5 | 0.531 | 0.064 | 0.218 | 76 / 127 / 42 | - |
| reference b/t21.0 | 0.440 | 0.017 | 0.661 | 164 / 60 / 46 | - |

Reading: every repaired framing passes every range. The medium and the insert never show the ceiling or the camera end of the floor, so their top and bottom rows are brighter (89 / 95 and 98 / 87); the spec states those two targets for wide interior frames only. The close reference frames (b/t03.0, b/t21.0, a/t27.5) are listed for completeness: they are blurred or flat close-ups and are not edge-density targets.

### 2.2 Colour statistics (`measure_color.py`)

Targets for interiors (`spec/LOOK_SPEC.md` 4.1): S p90 at least 0.62; V mean 0.44 to 0.60; luma p5 0.09 to 0.18, p50 0.22 to 0.45, p95 0.75 to 0.92; contrast 0.60 to 0.75; colourfulness 55 to 100; share S > 0.5 at least 0.25; share S < 0.15 at most 0.12; share V > 0.95 0.02 to 0.09 (with heads); darkest tenth hue 250 to 345 and S at least 0.35; mid band hue 330 to 25; largest cluster dark and saturated.

| Frame | S p90 | V mean | Luma p5 / p50 / p95 | Contrast | Colourfulness | S > 0.5 | S < 0.15 | V > 0.95 | Darkest 10 percent | 40 to 60 percent band | Largest cluster |
|---|---|---|---|---|---|---|---|---|---|---|---|
| builder, wide | 0.667 | 0.438 | 0.109 / 0.258 / 0.706 | 0.597 | 52.9 | 0.493 | 0.049 | 0.021 | `#27181b` H351 S0.38 | `#5b3d38` H8 | `#593328` 27% |
| builder, two-shot | 0.642 | 0.519 | 0.129 / 0.333 / 0.864 | 0.735 | 60.3 | 0.474 | 0.054 | 0.038 | `#331d19` H9 S0.51 | `#6d524d` H9 | `#4c3027` 24% |
| builder, medium | 0.584 | 0.578 | 0.134 / 0.457 / 0.895 | 0.761 | 63.8 | 0.461 | 0.068 | 0.046 | `#37221e` H11 S0.45 | `#8e6e55` H26 | `#c09d70` 20% |
| builder, insert | 0.607 | 0.593 | 0.162 / 0.490 / 0.869 | 0.707 | 64.6 | 0.462 | 0.058 | 0.036 | `#352622` H13 S0.37 | `#98775f` H25 | `#946a4f` 21% |
| **repaired, wide** | 0.671 | 0.435 | 0.118 / 0.245 / 0.673 | 0.555 | 54.9 | 0.504 | 0.046 | 0.015 | `#291923` H321 S0.38 | `#5b373b` H353 | `#46272b` 29% |
| **repaired, two-shot** | 0.642 | 0.504 | 0.142 / 0.306 / 0.781 | 0.638 | 62.7 | 0.453 | 0.056 | 0.026 | `#331f24` H344 S0.40 | `#6b474f` H347 | `#492d30` 20% |
| **repaired, medium** | 0.604 | 0.553 | 0.167 / 0.391 / 0.811 | 0.645 | 66.3 | 0.443 | 0.067 | 0.028 | `#362424` H358 S0.34 | `#7f5c58` H6 | `#5f3430` 23% |
| **repaired, insert** | 0.608 | 0.563 | 0.175 / 0.408 / 0.772 | 0.597 | 67.2 | 0.432 | 0.059 | 0.022 | `#372627` H358 S0.31 | `#88605d` H4 | `#643735` 22% |
| repaired, two-shot + real puppets | 0.651 | 0.502 | 0.148 / 0.296 / 0.888 | 0.740 | 62.4 | 0.448 | 0.079 | 0.045 | `#351f23` H349 S0.42 | `#654550` H340 | `#75433e` 24% |
| repaired, medium + real puppets | 0.617 | 0.551 | 0.174 / 0.361 / 0.936 | 0.762 | 66.4 | 0.442 | 0.105 | 0.061 | `#352328` H345 S0.33 | `#755655` H2 | `#71403c` 24% |
| reference b/t07.0 | 0.725 | 0.491 | 0.123 / 0.287 / 0.790 | 0.668 | 63.2 | 0.553 | 0.214 | 0.034 | `#3a1716` H1 S0.62 | `#743e3f` H359 | `#383a55` 19% |
| reference b/t18.5 | 0.630 | 0.437 | 0.124 / 0.313 / 0.754 | 0.630 | 38.4 | 0.231 | 0.238 | 0.016 | `#221a32` H260 S0.48 | `#5d4b57` H322 | `#5e5262` 25% |
| reference b/t23.0 | 0.646 | 0.454 | 0.124 / 0.304 / 0.885 | 0.760 | 45.1 | 0.225 | 0.075 | 0.061 | `#311a1f` H347 S0.47 | `#614943` H11 | `#604f4d` 21% |
| reference a/t27.5 | 1.000 | 0.450 | 0.089 / 0.145 / 0.447 | 0.358 | 102.7 | 0.897 | 0.033 | 0.024 | `#320d21` H328 S0.73 | `#6a102e` H340 | `#161a42` 31% |
| reference b/t03.0 | 0.585 | 0.467 | 0.145 / 0.363 / 0.783 | 0.638 | 39.2 | 0.154 | 0.281 | 0.042 | `#272235` H258 S0.36 | `#6a5861` H330 | `#706672` 28% |
| reference b/t05.5 | 0.746 | 0.470 | 0.109 / 0.237 / 0.972 | 0.862 | 65.5 | 0.675 | 0.111 | 0.083 | `#281624` H316 S0.45 | `#65332e` H5 | `#2d2545` 21% |
| reference b/t21.0 | 0.740 | 0.529 | 0.104 / 0.263 / 0.870 | 0.765 | 62.3 | 0.455 | 0.245 | 0.056 | `#27162b` H289 S0.49 | `#823336` H358 | `#34213f` 23% |

Reading: the darkest tenth moved from red-brown (hue 351 to 13) to plum-red (hue 321 to 358), toward the reference (hue 260 to 347, and 1 in b/t07.0); the mid band moved from hue 8 to 26 to hue 347 to 6. Not met without characters: luma p95 and contrast in the empty wide (0.673 and 0.555) and contrast in the insert (0.597); with the white heads in frame the two-shot and medium reach p95 0.888 and 0.936 and contrast 0.740 and 0.762. S p90 is 0.604 to 0.608 in the medium and insert (target 0.62; reference 0.63 to 0.75). Darkest-tenth saturation is 0.31 to 0.34 in the medium and insert (target 0.35), where no ceiling is in frame.

### 2.3 Lines, colours, light rows

| Frame | Thin dark lines (black-hat over 28) | Colour bins | Warm / cool / green share | Luminance of the 8 rows, top to bottom |
|---|---|---|---|---|
| builder, wide | 0.106 | 101 | 0.73 / 0.18 / 0.038 | 62 77 129 135 88 101 56 43 |
| builder, two-shot | 0.108 | 96 | 0.69 / 0.22 / 0.028 | 71 110 132 140 115 88 102 65 |
| builder, medium | 0.120 | 93 | 0.65 / 0.27 / 0.018 | 104 108 160 152 141 86 92 98 |
| builder, insert | 0.102 | 89 | 0.65 / 0.28 / 0.010 | 122 103 168 152 147 92 89 92 |
| **repaired, wide** | 0.099 | 102 | 0.71 / 0.20 / 0.017 | 58 69 116 126 85 99 61 44 |
| **repaired, two-shot** | 0.102 | 118 | 0.68 / 0.24 / 0.019 | 68 93 119 130 102 89 97 68 |
| **repaired, medium** | 0.108 | 116 | 0.64 / 0.26 / 0.029 | 89 97 145 141 121 85 93 95 |
| **repaired, insert** | 0.095 | 116 | 0.64 / 0.27 / 0.023 | 98 98 154 141 125 91 90 87 |
| reference b/t07.0 | 0.104 | 120 | 0.59 / 0.17 / 0.001 | 66 90 103 125 102 87 86 70 |
| reference b/t18.5 | 0.105 | 100 | 0.30 / 0.36 / 0.001 | 66 83 109 140 121 113 66 43 |
| reference b/t23.0 | 0.088 | 98 | 0.70 / 0.16 / 0.008 | 63 83 109 147 116 123 80 52 |
| reference a/t27.5 | 0.011 | 68 | 0.57 / 0.32 / 0.010 | 89 83 69 80 47 47 28 27 |
| reference b/t03.0 | 0.017 | 91 | 0.35 / 0.28 / 0.000 | 67 86 110 141 142 119 94 55 |
| reference b/t05.5 | 0.058 | 97 | 0.65 / 0.21 / 0.001 | 76 86 102 168 86 83 56 42 |
| reference b/t21.0 | 0.013 | 87 | 0.51 / 0.20 / 0.000 | 164 177 143 56 65 75 83 46 |

### 2.4 Lamp halo (isolated light layer on black; radius where the glow falls to 10 percent, minus the bulb radius)

| Frame | Lamp | Bulb radius | 50 percent | 10 percent | Beyond the core |
|---|---|---|---|---|---|
| wide | side pendants | 22.0 px | 24 px | 36 px | 14 px |
| wide | centre pendant | 29.7 px | 32 px | 48 px | 18 px |
| two-shot | side pendants | 30.0 px | 32 px | 48 px | 18 px |
| two-shot | centre pendant | 40.5 px | 43 px | 65 px | 24 px |
| medium | left pendant | 40.0 px | 43 px | 64 px | 24 px |

Target 12 to 24 px (clip A lamps: 12, 12 and 24 px). The halo is drawn in world units, so it grows with the zoom: about 30 px at the push-in (250 px per D), where the lamps are almost out of frame.

### 2.5 Surface texture (luminance std after removing a 3 px Gaussian / luma std after a sigma-12 high-pass)

| Surface | Reference | Builder | Repaired |
|---|---|---|---|
| Wall | backdrop b/t07.0: 22.2 / 0.111 | 19.8 / 0.119 | 16.9 / 0.095 |
| Rug | carpet b/t07.0: 9.3 / 0.061; b/t18.5: 11.9 / 0.080 | 16.1 / 0.084 | 14.4 / 0.075 |
| Floor beside the rug | stone b/t07.0: 17.3 / 0.104 | 14.2 / 0.072 | 12.8 / 0.065 |
| Wainscot | - | - | 13.6 / 0.067 |
| Map sea (largest flat field) | - | 5.3 / 0.024 | 7.8 / 0.036 |

Target for wall and floor patches: 0.03 to 0.10 on the second measure. The wall dropped a little because the lit rose has less luminance contrast against its sprig than orange had; it stays inside the range.

## Step 3. Contract

Debug renders: `review_anchors.png` (whole world at 78 px per D, every anchor drawn; fg anchors drawn in the fg layer's transform) and `v2/tmp/rev/anchors_map.png` (map at 215 px per D).

| Check | Result |
|---|---|
| `map_rect`, `map_paper_rect` | On the outer frame and on the sheet. Correct. |
| `map_track`, `map_storm`, `map_ny` | 85 points, length 1.076 D, runs monotonically north from the storm symbol off Florida (0.2349, -1.6183) to the New York station dot (0.0623, -2.6197). Correct. |
| `pencil_tip`, `line_end` | Equal to `track_point(line)` and `track_point(line * (1 - erase))`; the markers sit on the end of the drawn red line. Correct. |
| `hero_mark`, `boss_mark`, `floor_y` | Marks at x = -0.55 and 1.30 on the contact line y = 0, which lies 0.40 D in front of the wall base. With the real puppets the hero's hand reaches `map_ny`; the boss (taller: head centre y = -2.87) has his hat just under the date slip. Correct; the API text assumed both heads at y = -2.5 and is now annotated. |
| `ledge_y`, `ledge_x`, `eraser_on_ledge`, `red_pencil_on_ledge` | On the ledge top, on the pink eraser, on the red pencil. Correct. |
| `lamps`, `lamp_radius`, `banker_lamp`, `desk_top` | On the three bulbs; on the glow slit and the top surface of the fg desk when drawn with the fg parallax. Correct. |
| `window_rect`, `sign_rect`, `calendar_rect`, `clock` | Match the drawn props. Correct. |
| Cameras | `cam_wide` frame x -3.27..3.27, y -7.52..4.12, eye line at 43 percent; `cam_two_shot` 46 percent; `cam_medium_hero` 45 percent; `cam_push_in` 48 percent. All four frames lie inside the painted world (-4.6, -8.2, 4.6, 4.8). Correct. |
| State `line` at 0, 0.25, 0.5, 0.75, 1 | Grows from the storm symbol to New York (`review_states.jpg`, rows 1 and 3); red pixel count rises monotonically in 21 steps; the arrow head grows over 0.97 to 1.0. Correct. |
| State `erase` at 0, 0.25, 0.5, 0.75, 1 | Starts at the New York end, leaves a smudge, ends with the whole line gone and the printed symbol left. **Defect found and fixed:** the arrow head disappeared in a single step as soon as `erase` exceeded 0 (21 percent of the red pixels in one frame). It is now rubbed out over erase 0 to 0.06. **Second defect fixed:** the rubbing strokes were re-spaced along the erased part on every call, so they slid while the eraser moved; they are now fixed on the paper and fade in. Largest change between neighbouring states (line step 0.0025, erase step 0.005): 2.2 percent (build), 2.4 percent (insert). |
| `build_insert_map` | Same world coordinates, same state behaviour (rows 3 and 4 of `review_states.jpg`), thinner lines, extra map detail; map at y 309..823 px, clear of the caption band. Layers now also carry `depends` like `build()`. Correct. It is a close view of the map wall (sign above, wainscot and rug below), not a full-frame flat insert, because the map is landscape. |
| State `t` | 0.05 percent of pixels change per frame (fan, clock, dust); largest single-frame change 0.08 percent; no pops. Correct. |
| Determinism | Two calls give identical SVG (all random generators are seeded). Layer dependencies are as declared: `bg` on line, erase, t; `light` on t; `mid`, `fg` on nothing. |
| ids | 31 ids in `build()`, 30 in `build_insert_map()`, all prefixed by the uid, no dangling `url(#...)`, no duplicates; two builds in one document give 61 unique ids. |
| Fonts | System DejaVu Serif Bold (present: `/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf`); the documents contain no `@font-face`, no `href` to a file and no URL other than the SVG namespace. Lettering renders in the rasters. |
| Speed | `build()` 8 to 14 ms; one 720x1280 frame rasterises in 300 to 420 ms (was 240 to 340 ms before the shading overlays; limit 1 s); no filters. |

## Step 4. Repairs made in `office.py` (API unchanged)

1. Palette re-blocked to the resolved palette of `spec/LOOK_SPEC.md`: rose wall with a visible sprig, steel-violet cabinets, mauve-brown planks, plum ceiling and fall-off, more saturated navy and border red.
2. Painted shading added everywhere (automatic overlay on inked shapes, plus targeted overlays and floor patches). New optional `shade=` argument on the primitives and a `tone()` helper; no API function changed its signature incompatibly.
3. Map re-toned to old gold and teal, given a light pool, aged corners, frame shade, water lining and slate isobars; red track widened from 0.032 to 0.038 D.
4. Warm wall pool changed from pale yellow to a saturated orange screen (keeps the wall rose, keeps saturation at 0.44 to 0.49).
5. Arrow head and rubbing strokes made continuous under `erase`; crumbs appear one at a time.
6. Lamp halo radius 1.85 to 2.0 bulb radii with re-spaced stops (14 to 24 px beyond the core).
7. Chair shade clipped to the chair.
8. Heavier contour on the five largest props; `depends` added to the insert layers.
9. `API.md` updated (marked **(review)**), `office_*.png`, `compare.jpg`, `metrics.json` regenerated with `python3 office.py frames`.

Anchors, marks, cameras, world box, layer names, parallax values and state keys are unchanged.

## Remaining differences against the reference, by visual impact

1. Shading is still simpler than the reference: each shape has one soft gradient, where clip B paints several tones per surface (drapery folds, tufted cushions, specular touches on gold).
2. Lines are vector-clean. The reference contours vary in weight along a stroke and gold trim often replaces ink; here weight varies only between objects.
3. The composition is many small props where the reference builds a frame from a few large shapes (throne, curtains, columns). It is right for an office, but it reads busier than b/t07.0.
4. The map is a large mid-light area behind both heads (ring 148 and 125). It is inside the range and the heads read at once, but the reference usually puts heads against darker, more saturated cloth.
5. Without characters the wide's luma p95 (0.673) and contrast (0.555) are below the interior targets; with the real puppets in the wide they are 0.731 and 0.61 (p95 still 0.02 short), and both are met in the two-shot and medium. S p90 in the medium and insert is 0.604 to 0.608 against a target of 0.62. Green is 1.7 to 2.9 percent of the frame (lamp shades and sign) against 0.1 to 0.8 percent in the clip B interiors.
6. The boss puppet's hat touches the lower edge of the date slip and overlaps the coat stand a little at `boss_mark` 1.30. The mark was left where the builder put it to keep the API stable; staging can shift him by 0.05 to 0.1 D or tilt the head.
7. `bg` parallax is 1.0 (no wall-against-actor parallax); depth comes only from the fg layer at 1.12. Kept, because it holds the hand on `map_ny`.
8. Fonts are DejaVu Serif Bold; a period fat-face would be closer to reference signage (none is installed, the network is closed).
9. No background blur for close-ups is built in (the reference blurs the set behind heads of 300 px and more); the compositor has to blur `bg` and `mid`.
10. The hero's torso hides the Florida peninsula in the two-shot and medium; the storm symbol, the track, N.Y. and BOSTON stay visible.

## Files

- `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/office.py` (repaired), `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/API.md` (updated)
- `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/REVIEW.md` (this file), `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/review.py` (harness)
- `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/review_compare.jpg`, `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/review_anchors.png`, `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/review_states.jpg`
- `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/sets/office_wide.png`, `office_two_shot.png`, `office_medium.png`, `office_insert.png`, `office_states.png`, `office_staged_two_shot.png`, `office_staged_medium.png`, `compare.jpg`, `metrics.json` (regenerated)
- Scratch: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/tmp/rev/` (builder copy `office_orig.py`, renders `v0_*` and `final_*`, metric JSON, patch scripts)
