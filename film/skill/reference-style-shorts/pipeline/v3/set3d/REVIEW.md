# REVIEW of v3/set3d (office3d.py): independent look, measurement, contract check and repair

Reviewer pass on the set built by another agent. Everything below was rendered and measured by me with my own scripts (`review/`), on my own renders and on the reference stills. "Before" is the builder's state (backup in `v3/tmp/review/office3d_builder_backup.py`), "after" is `office3d.py` and `textures.py` as they are now.

Result in one paragraph: the builder's set was already of the reference's family (inked, saturated, dense, one hard sun, real perspective) and far from the pale room of version 1. Its flaws were in the three things being judged: the far shadow edges were too soft, the shadows on the wall surfaces were shallow, the sunlit wallpaper clipped to a flat neon red, the ceiling carried no readable converging lines, boxes and room corners had no tonal form in shade, the foreground was as bright as the background, and neither the high nor the low camera was steep enough to feel high or low. Those are repaired. The contract (anchors, track, determinism, cost) held and still holds, with one claim of the builder corrected (shadows on the track, section 3).

Pictures: `review_compare.jpg` (ten cameras with two placeholder actors next to the closest reference frame), `review_anchors.jpg` (every anchor drawn on every camera), `review_track.jpg` (track states).

## 1. Looking (step 1)

Every camera rendered at 720x1280 final quality with two v2 puppets on emission + alpha cards (`stage_placeholders`), put next to a/t16.0, a/t13.5, a/t32.0, b/t24.5, b/t10.0, a/t58.5, b/t07.0, a/t34.0, a/t27.5, b/t52.0.

| Question | Before | After |
|---|---|---|
| One clear light direction? | Yes. Window-bar shadows fan across the floor, actor shadows fall to screen-left onto the map wall. | Same direction, crisper and deeper. |
| Actor shadows crisp, long enough to read, clear of the track and the N.Y. label? | Crisp on the wall (2 to 3 px). The near actor's whole silhouette lands on the right half of the map, the wall actor's 0.29 D to his left. Bodies and heads are clear of the track; reaching arms are not (the builder's "ok = True in all four" holds only with the arms down, section 3). On the floor an actor leaves only two thin leg lines, because the sun is 10 degrees above the horizon. | Unchanged in geometry (the sun direction is kept, it is what lights the whole map wall). The shadows are darker on map, wallpaper and wainscot. |
| Floor and ceiling lines converge strongly? | Floor planks and rug: yes. Ceiling: no, plum boards with seams 20 levels darker, and three flat dark beams; a Canny pass found nothing in the top quarter of the frame. | Ceiling boards lighter with dark seams and a highlight line, beams inked and textured (arris, checks, iron straps): the boards run visibly to the same vanishing point as the floor. |
| Objects near the lens? | `desk_fg` (lamp, ink bottle), pendant shade in the two-shots. The ink bottle had a 9 px outline and the desk top was an empty slab. | `desk_fg`: typed sheet, pencil, smaller bottle, thinner ink. New `low_rake` (an actor 2.8 D from the lens) and `high_steep` (pendant shade in the top corner). |
| Does a low angle feel low, a high angle high? | `low_medium` matches a/t16.0 in numbers (1.2 D, +14 degrees) but looks at a wall square-on. `high_two_shot` (-15 degrees) still showed a quarter frame of ceiling; `wide_high` a third. | `low_rake`: 0.9 D, +20 degrees, raking along the wall. `high_two_shot` 3.7 D, -22 degrees, no ceiling. `high_steep` 4.75 D, -43 degrees, horizon above the frame, as a/t58.5. `wide_high` -25 degrees. |
| Inked, saturated, dense, or sliding back to version 1? | Same family as the reference. Version 1 measures saturation 0.29, mid luma 0.64, Canny 0.017, 56 percent featureless blocks; the builder's set 0.50, 0.24, 0.07, 11 percent. | 0.49, 0.26, 0.083, 2 percent on the eye-level two-shot. |

## 2. Measurements (step 2)

Tools: `review/rmeasure.py` (pair ratio, edge profile, halo, used identically on reference frames and on renders), `review/review_render.py passes` (the same frame with the key on, off, and on without shadows, plus a surface-id map), `review/review_analyze.py`, `review/tone_table.py` (which calls `ref/crops/env/tools/metrics.py` and `spec/measure_color.py`).
For our renders the cast-shadow ratio is exact per pixel: (frame with the key off) / (frame with the key on) on pixels the key reaches, by surface. For the reference it is a pair of patches on the same material.

### 2.1 Light

| Quantity | Reference, measured by me | Before | After |
|---|---|---|---|
| Same surface in cast shadow / lit, linear luminance, floor | a/t32.0 floor 0.084; a/t13.5 sleeper 0.083, ballast 0.21; a/t34.0 floor 0.25; a/t58.5 ballast 0.20 (brief: 0.11 to 0.33) | 0.16 to 0.17 | 0.15 to 0.16 |
| ... map | | 0.33 to 0.36 | 0.28 to 0.31 |
| ... wallpaper | | 0.29 to 0.30 | 0.30 |
| ... wainscot | | 0.32 | 0.29 to 0.31 |
| The same as display luma: floor / map / wallpaper / wainscot | 0.29 to 0.52 | 0.43 / 0.61 / 0.59 / 0.59 | 0.42 / 0.57 / 0.58 / 0.57 |
| V ratio, floor | 0.32 to 0.60 | 0.38 | 0.37 |
| Hue lit -> cast shadow (S of the shadow) | 27 -> 252 (0.26) a/t32.0; 354 -> 251 (0.45) a/t13.5; 24 -> 246 (0.22) a/t34.0 | floor 14 -> 304 (0.36), map 9 -> 236 (0.40), wallpaper 347 -> 328 (0.68), wainscot 2 -> 329 (0.51) | floor 14 -> 302 (0.37), map 14 -> 238 (0.38), wallpaper 356 -> 326 (0.57), wainscot 2 -> 328 (0.48) |
| Colours, lit -> cast shadow | a/t32.0 `#b28e71` -> `#2d2a39`; a/t13.5 `#9a7d80` -> `#27223e` | floor `#d16e51` -> `#543652`, map `#a07d77` -> `#3e4167`, wallpaper `#cd002e` -> `#682147` | floor `#cf6d4e` -> `#513350`, map `#a27d72` -> `#3c3d60`, wallpaper `#e74751` -> `#77335a` |
| Sunlit wallpaper | | `#cd002e`: green channel 0. The grade's saturation works on linear values, where this paper was already 0.91 saturated, so 1.12 x clipped it to pure red and the pattern vanished in the sun | `#e74751`, pattern kept |
| Cast-shadow edge width, 10 to 90 percent, p10 / median / p90 / max, all edges of the frame | 1.7 to 2.1 px (a/t32.0, occluder 0.5 D from the floor), 7.7 px (a/t34.0 roof bars), 8.2 to 12.6 px (a/t13.5, a/t32.0 far edge); brief 4 to 21 px | eye_two_shot 2.0 / 8.0 / 13.2 / 23.8; low_medium 3.0 / 16.3 / 23.5 / 32.0; high_two_shot 3.3 / 8.3 / 11.8 / 21.3 | 2.0 / 5.0 / 8.5 / 11.8; 2.0 / 9.6 / 15.5 / 21.8; 2.5 / 5.3 / 7.3 / 11.8 |
| The same with the reference tool on the graded frame | | | 1.2 / 4.5 / 10.3 / 16.5; 1.6 / 8.4 / 14.5 / 18.8; 1.5 / 5.4 / 10.1 / 14.5 |
| Bloom halo on a bulb: radius where the glow falls to 10 percent, minus the core radius | a/t27.5 9, 11, 12, 16 px; a/t27.0 14, 16 px; a/t28.0 11 to 25 px (bulb radius 17 to 36 px); brief 12 to 24 px | 23, 24, 26 px (bulb radius 37 to 45 px) | 16, 20, 24 px. The compositor quantises the size: 0.044 and below gives 9 to 12 px, 0.047 and above 16 to 24 px; the spec's 0.05 is kept |
| Do the white heads glow? Bloom on minus bloom off | reference: no halo around heads | at most 1 to 2 levels in a 24 px ring around a head, 4 to 5 levels on it | at most 1 to 3 levels in the ring (mean 0.02 to 0.14), 4 to 5 on it. No |
| Head fill on screen | `#fcf8f6` typical, V 0.98 to 1.00, S 0.02 to 0.04 | `#fff5f3`, V 1.00, S 0.047, the same in sun and shade | unchanged (the card is authored `#fef7f6`; the grade's warm slope and saturation move it 2 to 3 levels) |
| Head ink on screen | `#3a2832` (`#3d2835` measured) | `#3f2838` hero, `#322839` under the hat brim | unchanged |
| Luminance of the set in a ring around each head (0 to 255) | 95 to 170 | far actor 101 to 114, near actor 63 to 72 | far 97 to 114, near 69 to 81 |

### 2.2 Tone, ten cameras with two placeholder actors

| Quantity | Reference interiors (a/t27.5, a/t32.0, a/t34.0, b/t07.0, b/t24.5, b/t10.0) | Target | Before (8 cameras) | After (10 cameras) |
|---|---|---|---|---|
| Mean saturation | 0.74, 0.41, 0.40, 0.47, 0.58, 0.38 | 0.40 to 0.50 | 0.44 to 0.52 | 0.43 to 0.51 (`low_medium` 0.505, the rest at most 0.50) |
| Luma p1 / p5 | 0.07 to 0.17 / 0.09 to 0.21 | 0.08 to 0.12 / 0.09 to 0.18 | 0.12 to 0.17 / 0.17 | 0.12 to 0.15 / 0.15 to 0.17 |
| Luma p50 | 0.15, 0.42, 0.37, 0.29, 0.21, 0.26 | 0.22 to 0.45 | 0.20 to 0.31 (two-shots 0.24) | 0.22 to 0.30 (two-shots 0.26) |
| Luma p95 | 0.45 to 0.95 | 0.75 to 0.92 | 0.55 to 0.80 | 0.55 to 0.80 |
| Darkest tenth | `#330d1f`, `#3f2428`, `#532a2d`, `#3a1616`, `#2e0f11`, `#1e1526` | plum, hue 250 to 345, S at least 0.35 | `#3d2142`, hue 265 to 330, S 0.43 to 0.63 | `#372143`, hue 255 to 329, S 0.42 to 0.59 |
| Canny 60/140 edge density | 0.020, 0.077, 0.083, 0.114, 0.079, 0.101 | at least 0.085 | 0.053 to 0.073 (two-shots 0.070) | 0.081 to 0.085 on seven cameras; `low_medium` 0.075, `top_down` 0.070, `insert_rake` 0.056 |
| Featureless 40 px blocks | 0.41, 0.02, 0.02, 0.06, 0.12, 0.14 | at most 0.25 | 0.05 to 0.20 | 0.02 to 0.08 |
| Mean luma of the top eighth / brightest middle band / bottom eighth | 40 to 121 / 95 to 191 / 27 to 117 | 40 to 90 / 105 to 150 / 30 to 70 | 50 to 99 / 100 to 133 / 55 to 97 | 55 to 98 / 101 to 137 / 52 to 96 |
| Colourfulness; share S > 0.5; share V > 0.95 | 44 to 103; 0.23 to 0.90; 0.00 to 0.11 | 55 to 100; at least 0.25; 0.02 to 0.09 | 60 to 87; 0.37 to 0.55; 0.013 to 0.074 | 62 to 88; 0.38 to 0.52; 0.017 to 0.075 |

### 2.3 Depth and camera angle

Vanishing point of the floor and ceiling boards (they run along world +y), from the camera matrix and measured on the render (Canny, Hough lines, RANSAC over line pairs):

| Camera | Height, pitch | Horizon | Vanishing point from the matrix | Measured on the render | Pitch class |
|---|---|---|---|---|---|
| `low_rake` | 0.90 D, +20.4 deg | y 930 (0.73 H) | (1283, 930), off frame right | (1259, 916) from ceiling lines | low |
| `low_medium` | 1.20 D, +14.4 deg | y 841 (0.66 H) | (232, 841) | (238, 819) from ceiling lines | low (a/t16.0: 1.16 D, about +15 deg) |
| `insert_rake` | 2.05 D, +7.7 deg | y 746 | (-1856, 746) | | close insert |
| `window_side` | 2.10 D, -1.2 deg | y 623 | (-1665, 623) | | eye level, side |
| `desk_fg` | 2.25 D, -1.0 deg | y 626 (0.49 H) | (211, 626) | (209, 626) | eye level |
| `eye_two_shot` | 2.55 D, -2.5 deg | y 606 (0.47 H) | (381, 606) | (380, 604) | eye level |
| `high_two_shot` | 3.70 D, -22.0 deg | y 324 (0.25 H) | (432, 324) | (431, 322) | high |
| `wide_high` | 4.40 D, -25.3 deg | y 271 (0.21 H) | (56, 271) | (57, 271) | high |
| `high_steep` | 4.75 D, -43.2 deg | y -94, above the frame | (592, -94) | (590, -94) | steep high (a/t58.5) |
| `top_down` | 4.80 D, -84.1 deg | none | | | top-down |

Parallax between two renders with the camera moved 0.5 D to its right (predicted from depth = 782 x 0.5 / z, and measured by template matching around each anchor):

| Camera | Far | Near | Nearest | Features one 2D zoom + pan + roll can explain (3 px) |
|---|---|---|---|---|
| `eye_two_shot` | map 63 px predicted, 67 measured (z 6.2) | near head 93 / 93 (z 4.2) | pendant lamp 110 / 104 (z 3.6) | 46 percent of 2397 matches |
| `low_rake` | far head 103 / 103 (z 3.8) | near head 141 / 141 (z 2.8) | | 15 percent |
| `high_steep` | wall marks 59 to 62 / 61 (z 6.4 to 6.6) | near head 126 / 126 (z 3.1) | | 18 percent |
| `low_medium` (before the repair, camera unchanged) | map 105 / 117 | head 119 / 119 | | 29 percent |

Two-shot staged in depth: near head 186 px, far head 134 px in `eye_two_shot`, ratio 1.39 (reference 1.36 to 1.46).

## 3. Contract and cost (step 3)

| Check | Result |
|---|---|
| Anchors `map_track`, `map_storm`, `map_ny`, `ny_label_rect`, `map_rect`, `hero_mark`, `boss_mark`, `near_mark` | Projected and drawn on all ten cameras (`review_anchors.jpg`): the 85 track points lie on the rendered red line, the rectangle on the paper edge, the label rectangle around the printed "N.Y.", each mark between the feet of the card standing on it. Correct |
| `key_dir` | The shadow of each head centre predicted with `key_dir` onto the map plane falls inside the rendered shadow: key visibility 0.00 at all six predicted centres (three cameras, two actors), offsets (-20, +10) px for the wall actor and (-254, +75) px for the near actor in `eye_two_shot`. Correct |
| `set_track(line, 0)` at 0, 0.25, 0.5, 0.75, 1 | Grows from the storm symbol off Florida toward New York; the end of the red line is within 1 px (at 360x640) of `track_point(line)`; the arrow head appears only at 1. Correct |
| `set_track(1, erase)` at 0.25, 0.5, 0.75, 1 | Removes from the New York end (arrow head first), leaves the pink smudge and the arrow ghost; the remaining red ends at `track_point(1 - erase)` (checked at erase 0.4: 4 px at 360x640). Correct |
| Keyframed track | Keys at frames 1, 21, 41 rendered at 1, 6, ... 41: bit-identical to the directly set states (maximum pixel difference 0). Correct |
| Deterministic build | Two processes: identical digest of object names, transforms, vertex and UV hashes, materials, texture files and anchors; identical pixels (maximum difference 0). The PNG files differ only in their time-stamp metadata. `build(clear=False)` gives the same frame as a fresh build and keeps the actors. Correct |
| Shadows on the track (builder: "ok = True in all four") | True only with the arms down: hero at `hero_mark`, boss at `boss_mark`, either at `near_mark`, standing, all ok. With the builder's own placeholder poses it is false: `hero_draw` shadows the track at u 0.62 to 0.73 and 10 percent of the N.Y. label, `boss_rub` shadows u 0.90 to 1.0 and 24 percent of the label. This follows from the light: every shadow on the map lies 0.29 D left of its caster. API.md now says so and how to stage around it |
| Cost of a final 720x1280 frame, two placeholder cards, 16 samples, 4 threads | Before: 15.2 to 15.8 CPU s; 3.9 s wall on the two fastest frames, 5.2 to 5.8 s on the others (another job at about one core). After: 16.0 to 16.5 CPU s; 3.8 to 4.2 s wall on the frames rendered while no other job ran (seven frames in two runs), 6.1 to 7.9 s wall while another agent's render used about two of the four cores (it ran during most of my timing runs, so I never had a whole run alone). Under the 6 s target with the machine to itself; nothing had to be cut. The repair costs about 0.5 CPU s (one more inked object, a few shader nodes) |

## 4. What I changed in `office3d.py` and `textures.py` (step 4)

API is backward compatible: no function or anchor key was removed or renamed; `mat_lit` gained an optional `form` argument; `A["cams"]` gained two entries and `A["render"]` three keys.

| # | Change | Why (measured) |
|---|---|---|
| 1 | Sun angle 0.7 -> 0.45 degrees | Bar shadows are thrown from 5 to 8 D away: edges were up to 32 px in `low_medium` (reference 2 to 13 px). Now median 5 to 10 px, maximum 22 px |
| 2 | Deeper cast shadows on the wall surfaces: map shade 0.7 -> 0.56 and gain 0.28 -> 0.30, wood shade 1.0 -> 0.85 and gain 0.6 -> 0.7, wallpaper gain 0.7 -> 0.95 | Map 0.34 -> 0.29, wainscot 0.32 -> 0.30 of lit; the wallpaper stays at 0.30 although its ambient was raised (next row) |
| 3 | Wallpaper base `#9c3139` -> `#9c4a50` (close to the spec's `#9c5257`), stripes a little stronger, ambient multiplier 1.35 -> 2.0, frieze pattern bolder | The sun patch no longer clips to pure red; the wall behind the near actor reads 69 to 81 instead of 63 to 72; mean saturation comes down |
| 4 | Ceiling: boards `#7d4350` with seams at 0.2 x and a highlight line; beams are their own inked object with a drawn side face (light arris, checks, two iron straps) and a crown strip | The top quarter of the frame had no detectable edge and no convergence cue. Edge density of the two-shots 0.070 -> 0.083 |
| 5 | Orientation term in the ambient (`form`): top faces 26 percent lighter, undersides 26 percent darker, faces toward the window 14 percent lighter, away 14 percent darker | In pure flat ambient a cabinet top, front and side had one colour, and adjacent walls met without a tonal step |
| 6 | Depth falloff of the ambient (`falloff_y` 0.34): full at the map wall, two thirds at the camera-side wall | The foreground desk and chair were as bright as the wall; now they are the darkest layer (spec 3.1: light pooled on the middle band, painted into the set, not a vignette) |
| 7 | Darker plank seams and butt joints; wainscot grain | Seams did not survive in shade |
| 8 | Cameras: `high_two_shot` 3.6 D / -15 deg -> 3.7 D / -22 deg; `wide_high` -19 -> -25 deg; new `low_rake` and `high_steep` | Section 1, last but one row |
| 9 | `desk_fg` foreground: typed sheet and pencil at the camera end of the desk, smaller ink bottle, hull for a 1.3 D viewing distance | A 9 px outline and an empty slab next to the lens |
| 10 | Not changed: sun direction, marks, anchors, track, materials of cards, render settings, grade (bloom size tried at 0.04 and put back) | |

## 5. What remains different from the reference

1. An actor's body shadow lies on the wall, not on the floor. The sun is 10 degrees above the horizon so that the whole map wall is in sunlight; on the floor a standing actor leaves two thin leg lines. In a/t32.0, a/t13.5 and a/t58.5 the sun is at 35 to 50 degrees and the whole figure lies on the ground. Raising the sun would put the map and both wall marks in shade (at 33 degrees the sun reaches only 0.43 D up the wall at the hero mark).
2. Shadows on the map, wallpaper and wainscot are 0.28 to 0.31 of lit in linear luminance; the reference pairs measure 0.08 to 0.25. The floor (0.15) is inside. Going further would darken the wall behind the heads, which is already under the 95 to 170 band for the near actor (69 to 81).
3. Edge density is 0.081 to 0.085 on seven cameras and below on three; the goal of 0.085 is reached on two (`high_steep` 0.0854, `low_rake` 0.0852; `high_two_shot` 0.0845, `eye_two_shot` 0.0834). The reference interiors measure 0.077 to 0.114 with the same code.
4. An arm reaching across the map shadows a short stretch of the track or the label (section 3). Physically right, but it does cross the story prop.
5. The darks are lifted plum (luma p5 0.15 to 0.17); clip B interiors go down to 0.09 to 0.12, the sunlit clip A interiors measure 0.17 to 0.21.
6. Heads display `#fff5f3` (V 1.00, S 0.047) instead of `#fef7f6`, because cards pass through the grade.
7. No light shafts or dust glow from the window (clip B has painted shafts); the view through the window is a flat sky card.
8. Ink outlines are inverted hulls of fixed world thickness: about 3 px at the distance each prop was designed for, thicker when a prop comes close to the lens.
9. `top_down` shows flat cards as flat; `INTERIOR_LAMP` is smoke-tested only (it builds and renders).

## 6. Re-running

```
cd v3/set3d/review
python3 review_render.py staged <dir> 2          # ten final stills with placeholder actors + cams.json
python3 review_render.py passes <dir> eye_two_shot two_shot ; python3 review_analyze.py light <dir> eye_two_shot ; python3 review_analyze.py heads <dir> eye_two_shot
python3 review_render.py bloom <dir> eye_two_shot two_shot ; python3 review_analyze.py bloom <dir> eye_two_shot
python3 review_render.py parallax <dir> eye_two_shot two_shot ; python3 review_analyze.py parallax <dir> eye_two_shot
python3 review_analyze.py vp <dir>               # needs the staged stills and cams.json
python3 review_render.py track <dir> ; python3 review_render.py digest <dir> ; python3 review_render.py timing <dir> 6 4
python3 tone_table.py <dir>/staged_*.png ; python3 make_compare.py <dir> ../review_compare.jpg
```
The measurement outputs of this pass are in `v3/tmp/review/` (`m0` and `r0` before the repair, `m5` and `m6` after).
