# v3/set3d/office3d.py : the 1938 Weather Bureau office as a real 3D set (bpy 5.3, Cycles CPU)

Files: `office3d.py` (the set), `textures.py` (per-surface artwork, drawn with the v2 code in `v2/sets/office.py`, rasterised by Chromium into `tex/`, cached by content hash), `raster.js`, `measure_light.py` (the builder's ratio and edge tool), `sheet.py` (contact sheets), `still_<cam>.png` (one still per camera, no actors).
Review pass (independent, after the build): `REVIEW.md` (measurements against the reference, what was repaired and why, what remains), `review_compare.jpg` (every camera with placeholder actors next to its closest reference frame), `review_anchors.jpg` (every anchor drawn on every camera), `review_track.jpg` (track states), `review/` (the reviewer's scripts).

World: 1 unit = 1 D, Z up, floor z = 0, map wall = plane y = 0, room toward -y, x = 0 = centre of the wall map, +x to the right for a viewer facing the map. Camera 22 mm on 36 mm, sensor fit AUTO, 720x1280 (782 px focal).

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d"); import office3d as S

A = S.build(preset="INTERIOR_DAY", clear=True)   # -> anchors dict (section 2)
S.set_track(line, erase, frame=None)             # the red track, section 3
cam = S.make_camera(A["cams"]["low_medium"], name="cam")   # creates/reuses a 22 mm camera object and makes it scene.camera
S.setup_render(scene, "final" | "fast" | "preview")   # final: 720x1280, 16 samples, 4 threads; fast: 12 samples; preview: 360x640, 8 samples, 2 threads
S.setup_grade(scene, bloom=True)                 # compositor: bloom above 1.0, plum black point, saturation 1.12 (spec/grade_compositor.py, no vignette)
S.no_bounce(obj)                                 # call on every actor card (see section 5)
S.track_point(u)                                 # world point on the map at fraction u of the track (0 storm symbol, 1 New York); set_track(u, 0) ends the red line there (checked: within 1 px)
S.line_up(target, cam_loc, plane_y)              # where the sight line camera -> target crosses the plane y = plane_y (hand registration)
S.sun_blocker(point) / S.sun_visible(point)      # which object shadows a world point from the key (alpha of cards respected)
S.track_shadow_report()                          # {'track_shadowed': [(u, blocker)], 'label_shadowed': fraction, 'ok': bool} for the actors now in the scene
S.placeholder_actor(cast, story_key, mark, face_to=None, pose=None)   # stand-in card from a v2 puppet (stills, timing, tests only)
S.stage_placeholders(A, "hero" | "wall" | "two_shot", cam_loc)        # hero / hero + boss at the wall / hero at the wall + boss at near_mark
```

`build()` works in the current `bpy.context.scene`. It creates the collections `SET` (46 objects: the room, 26 distinct props) and `LIGHTS` (one Sun, `key_sun`), a black world, Cycles settings (`setup_render(scene, "final")`), the grade compositor, and the track at line 0. It adds no actors, no camera and no camera animation. `clear=True` deletes every object of the scene first; `clear=False` only rebuilds `SET` and `LIGHTS` (actors and cameras stay; checked: the frame is bit-identical to a fresh build). Materials named `INTERIOR_*` and `ink` are ours and are rebuilt on each call. The build is deterministic: two processes give the same object, vertex, UV, texture and anchor digest and bit-identical pixels (only the PNG time-stamp metadata differs). Presets: `INTERIOR_DAY` (the hard sun through the window; calibrated and reviewed) and `INTERIOR_LAMP` (same room without the sun, dusk sky, brighter bulbs; smoke-tested only).

## 2. Anchors (world units)

| key | value | meaning |
|---|---|---|
| `map_center`, `map_normal`, `map_size` | (0, -0.05, 2.5), (0, -1, 0), (3.0, 2.16) | paper sheet; its surface is the plane y = -0.05 (it stands 0.05 proud of the wall) |
| `map_rect`, `map_frame_rect` | dicts x0, z0, x1, z1, y | paper -1.5..1.5 x 1.42..3.58; frame -1.6..1.6 x 1.32..3.68, frame front at y = -0.11 |
| `map_track` | 85 points | the red track from the storm symbol off Florida to New York, on the map surface (y = -0.0515): since build step 0 ONE ruled straight segment, 85 evenly spaced collinear points |
| `map_storm`, `map_ny` | (0.2349, -0.0515, 1.6183), (0.0623, -0.0515, 2.6197) | ends of the track (unchanged by the straightening: the printed storm symbol and N.Y. dot sit here) |
| `track_heading_deg`, `track_width`, `track_length` | 9.779, 0.024, 1.01617 | the line leans 9.78 degrees west (toward -x) of straight up on the wall; drawn width 0.024 D; length 1.016 D |
| `calendar_rect` | x -2.14..-1.54, z 3.71..4.53, y -0.048 | the printed calendar leaf (card `calendar_face`, faces -y) on its block x -2.12..-1.56, z 3.72..4.50; for the leaf swap and flutter (shots 4, 17, 18, 25) |
| `label_rect` | x -0.45..0.70, z 3.10..3.44, y -0.054, `pin` (0.125, -0.062, 3.40) | where the nickname label 'ทางด่วนพายุ' (1.15 x 0.34 D) is pinned on the map, above the arrow head; reserved, not built yet (build step 4) |
| `teletype_sheet` | x 2.90..3.44, z 1.88..2.36, y -0.70, normal (0, -1, 0), `feed_top` (3.17, -0.685, 2.36) | front face of the paper sheet standing in the teletype (object `teletype`) |
| `ny_label_rect` | x 0.147..0.40, z 2.50..2.60 | the printed N.Y. label |
| `hero_mark` | (-0.55, -0.42, 0) | feet of the hero: left of the track, card plane 0.37 D in front of the map (`wall_gap`); in-plane shoulder (-0.31, 2.0) to `map_ny` = 0.72 D |
| `boss_mark` | (1.30, -0.42, 0) | feet of the chief: right of the track (head 0.8..1.8) |
| `near_mark` | (2.6, -1.95, 0) | foreground actor of a two-shot, 1.53 D nearer the camera; his wall shadow lands on the right part of the map (x 0.6..1.6), clear of the track |
| `key_dir` | (-0.600, 0.780, -0.180) | unit travel direction of the key: from the window wall (+x) toward -x, toward the map wall (+y), 10.4 degrees downward |
| `key_screen_side`, `key_note` | "right" | for a camera facing the map the sun is at screen-right, behind the camera; shadows fall to screen-LEFT and away. A card 0.37 D from the map throws its shadow 0.29 D to the left and 0.09 D lower |
| `room` | dict | x_left -3.8, x_right 3.8, y_map_wall 0, y_back -9, ceiling 5.3, wainscot_top 1.27, picture_rail 4.72, rug x -1.2..1.2 from y -9 to -0.62, window: right wall x = 3.8, y -7.72..-1.74, z 0.36..5.08, glazing bars at y -6.71, -5.51, -4.31, -3.12, transom z 2.45 |
| `ledge`, `eraser_on_ledge`, `red_pencil_on_ledge` | | chalk ledge under the map (top z 1.315, y -0.19..0) and two pick-up props |
| `desk_top`, `banker_lamp`, `lamps` | | foreground desk top (x -3.49..-1.41, y -5.04..-3.71, z 1.45), lamp glow, four pendant bulbs |
| `cams` | dict of `{loc, look_at, lens}` (+ `up` for `top_down`) | section 4 |
| `render` | | samples, resolution, sun angle, shade / key / lift, form, falloff_y, bloom_size of the preset |

All of these were checked by drawing them on a render of every camera (`review_anchors.jpg`): the track points lie on the red line, `map_rect` on the paper edge, `ny_label_rect` around the printed "N.Y.", the marks between the feet of cards standing on them, and the shadow of a head predicted with `key_dir` falls on the rendered shadow (key visibility 0.00 at the six predicted centres).

## 3. The red track

Real geometry: four flattened curve tubes 1.5 mm proud of the map (`track_red`, `track_smudge`, `track_arrow`, `track_arrow_ghost`), driven by one control object `track_ctl` with custom properties `line` and `erase`.

**Straightened (build step 0 of the shot plan).** The script says the line is ruler-straight ("ตรงเป๊ะ"), so the track is one ruled segment from the storm symbol off Florida (`map_storm`) to the N.Y. dot (`map_ny`); the curved v2 point list (`v2/sets/office.py` `TRACK`) is no longer used by the 3D set. The single point list is `office3d.TRACK` (map plane, 85 collinear points; the ends are v2's ends, so the printed map texture is unchanged). `track_point(u)` is linear in u along that segment, `map_track` is its 85 points on the map surface, and the geometry is a two-point spline. Firm pencil-and-ruler line: width 0.024 D (`TRACK_R` 0.012; it was 0.038 D, which the hook QA found read as a marker stroke at about 30 px in the insert); about 11 px from 1.55 D square-on, 3 px in `high_two_shot`. Eraser smudge 0.080 D wide (`SMUDGE_R`), arrow-head barbs 0.115 D at 152 degrees from the heading (`ARROW_L`, `ARROW_DEG`), which keeps the right barb clear of the printed N.Y. label (x from 0.147). Checked on a square-on debug view (`v3/out/straight/`, `check_straight.py`, `straightness.json`): the red centre of 420 rows deviates from a straight line by at most 0.28 px (rms 0.09 px) and from the projected `track_point(0)`-`track_point(1)` line by at most 0.62 px. The old file is `backup_before_straight/office3d.py`.
`set_track(line, erase)`: line 0..1 grows the red line from the storm symbol to New York (the arrow head grows over line 0.97..1); erase 0..1 removes it from the New York end (arrow head first, gone at erase 0.06) and leaves a faint pink smudge and a pink ghost of the arrow head. `frame=N` keyframes both controls at frame N with linear interpolation, so `set_track(0,0,frame=1); set_track(1,0,frame=20)` animates the whole stroke; the curves follow through drivers with simple expressions (no Python needed at render time; checked: keyed frames are bit-identical to the directly set states, `review_track.jpg`). The track casts no shadow and receives the key and the cast shadows like the map. In the sun it displays pure red (about (237, 3, 0)), the most saturated mark on the wall.

## 4. Cameras (`A["cams"]`, all 22 mm)

| name | loc | look_at | height, pitch | what it shows |
|---|---|---|---|---|
| `insert_rake` | (-1.05, -0.62, 2.05) | (0.55, -0.05, 2.28) | 2.05 D, +8 deg | 0.7 D from the map at a raking angle: the sheet recedes in perspective, track in the middle |
| `low_medium` | (-0.95, -3.45, 1.2) | (-0.45, -0.3, 2.02) | 1.2 D, +14 deg | low angle at the hero mark, head about 240 px, horizon at 0.66 H |
| `low_rake` (new) | (2.35, -2.5, 0.9) | (-0.25, -0.15, 2.2) | 0.9 D, +20 deg | low angle raking along the map wall from the window side: an actor at `boss_mark` looms near (head 280 px), the hero stands beyond, ceiling boards and the sign run to a vanishing point, the track stays visible; horizon at 0.73 H |
| `eye_two_shot` | (1.45, -6.2, 2.55) | (1.3, -0.5, 2.3) | 2.55 D, -2 deg | eye level; hero at the wall, near actor 1.39 x larger at screen right |
| `high_two_shot` (retuned) | (1.8, -5.9, 3.7) | (1.35, -0.6, 1.55) | 3.7 D, -22 deg | high angle two-shot: floor patch, bar shadows, almost no ceiling; horizon at 0.25 H (was 3.6 D and -15 deg, which still showed a quarter frame of ceiling) |
| `high_steep` (new) | (2.1, -4.6, 4.75) | (1.3, -0.9, 1.2) | 4.75 D, -43 deg | steep high angle: the floor fills the frame, the horizon is above the frame, a pendant shade hangs into the top left |
| `wide_high` (retuned) | (-1.9, -8.6, 4.4) | (0.7, -1.2, 0.7) | 4.4 D, -25 deg | back-left corner: whole room, window wall and sky at right, desk and chair dark in the foreground (was -19 deg with a third of the frame empty ceiling) |
| `desk_fg` | (-1.6, -5.8, 2.25) | (-0.55, -0.3, 2.15) | 2.25 D, -1 deg | over the foreground desk (typed sheet, pencil, ink bottle, banker lamp 1.2 to 1.8 D from the lens) |
| `top_down` | (0.9, -1.45, 4.8) | (0.9, -0.95, 0) + `up` (0, 1, 0) | 4.8 D, -84 deg | above the marks; flat cards look flat from here, tilt them back for this view |
| `window_side` | (-3.2, -2.6, 2.1) | (1.2, -0.9, 2.0) | 2.1 D, -1 deg | from the left wall across the marks to the window and the sky |

The vanishing point of the floor and ceiling boards measured on the renders (Hough lines) agrees with the camera matrix to 1 to 2 px where it lies in or near the frame. Parallax for a 0.5 D sideways move: `eye_two_shot` 63 px at the map, 93 px at the near head, 110 px at the pendant lamp; `low_rake` 103 px against 141 px; one 2D similarity transform explains only 15 to 46 percent of the matched features.
Keep cameras out of: the desk block (x -3.5..-1.4, y -5.05..-3.7, below z 2.2), the chair (x -3.05..-1.85, y -6.3..-5.2, below z 2.65), the ceiling beams (y -1.9, -4.4, -6.9, above z 4.94) and the pendant lamps (`A["lamps"]`, shade radius 0.47, z 4.0..4.8).

## 5. Light model and what the integrator must do

Scene-linear, Standard view: `pixel = artwork x gain x KEY x visibility + (artwork x SHADE x shade_mul + LIFT) x F`.
- SHADE (0.28, 0.255, 0.48) is a flat violet ambient, injected as emission, so shade is noise-free. LIFT (0.024, 0.016, 0.040) is a flat plum term that keeps the darks plum instead of black. KEY (2.30, 1.65, 0.74) is the one Sun (`key_sun`, energy pi x 2.30, angle 0.45 degrees).
- F (added in the review) = (1 + dot(face normal, form)) x (1 + falloff_y x y / 9), with form = (0.14, -0.04, 0.26) and falloff_y = 0.34. In shade a top face is 26 percent lighter than neutral, a face turned to the window 14 percent lighter, a face turned away 14 percent darker, an underside 26 percent darker, so boxes and the room corners read as volumes; and the ambient falls by a third from the map wall to the camera-side wall, so the foreground is the darkest layer. Floor, rug, ceiling and map carry no orientation term (they were calibrated as they are). F only scales emission: no noise, no cost.
- The diffuse colour of every lit material is divided by the true cosine to the sun, so every face that sees the sun gets the full key whatever its orientation. Visibility is ray traced: real hard cast shadows.
- gain is per material so that nothing lit exceeds scene-linear 1.0: floor and rug 1.0, wallpaper 0.95, wood 0.7, map 0.30, paper 0.27. Shade multipliers: wallpaper 2.0, wood 0.85, map 0.56, floor 0.78, ceiling 2.6. Only the bulbs (emission 6) and the banker lamp slit (3.6) are above 1.0, so only they bloom.
- No fill light, no area light, no vignette, no denoiser.

Actor cards: emission-only material gated by `Light Path > Is Camera Ray` plus alpha cut-out (as `office3d.mat_card(name, png)` does), standing on the floor at a mark. Then call `S.no_bounce(card)`. Reason: Cycles always traces one extra bounce ray that can only pick up emission; here every surface emits its ambient, so that ray adds grain, fireflies from the bulbs and an uncontrolled fill. `build()` hides every set object from those rays and `setup_render()` shortens the ray to 1 mm (fast GI "replace" with AO distance 0.001).
Cards pass through the grade like everything else: a head authored `#fef7f6` displays `#fff5f3` (V 1.00, S 0.047) and ink `#3a2832` displays `#3f2837`. The bloom adds at most 1 to 3 levels in a 24 px ring around a head and 4 to 5 levels on it, so heads do not glow; around a pendant bulb the halo reaches 16 to 24 px beyond the core.
Hand registration: the card stands 0.37 D in front of the map, so a tip that should touch map point M as seen from camera C must sit at `S.line_up(M, C, card_y)` on the card plane.
Shadows on the track: bodies and heads standing at the three marks with the arms down never shadow the track or the N.Y. label (`track_shadow_report()` ok for hero at `hero_mark`, boss at `boss_mark`, either at `near_mark`). An arm that reaches across the map does: every shadow on the map lies 0.29 D to the left of what casts it. With the two unregistered v2 story poses the hero's forearm and pencil shadow 5 of 41 track samples (u 0.62 to 0.73) and 10 percent of the label, and the chief's rubbing arm and eraser shadow u 0.90 to 1.0 and 24 percent of the label. For the hero, keep the hand on or left of the line; the chief's forearm crosses the line from the right, so a thin arm shadow over the stretch he is rubbing is physically right and cannot be staged away. Check a new staging with `track_shadow_report()`. From a camera left of the hero (`low_medium`) his head also hides the New York end of the track; shoot the drawing beat from `eye_two_shot`, `desk_fg`, `low_rake` or `insert_rake`.

## 6. Command line

```
python3 office3d.py stills [final|preview]   # v3/set3d/still_<cam>.png for every camera, no actors, track fully drawn
python3 office3d.py timing                   # final-quality seconds per frame (wall and CPU), eye_two_shot with two placeholder cards
python3 office3d.py spike [final|preview]    # v3/out/spike_low.png, spike_eye.png, spike_high.png with placeholder actors
python3 office3d.py staged [final|preview] [dir]   # every camera with placeholder actors (default v3/tmp/set3d/staged_<cam>.png)
python3 measure_light.py [cam] [hero|wall|two_shot|none] [final|preview]   # the builder's ratio and edge tool
python3 review/review_render.py <job> <outdir> ...   # the reviewer's passes: staged, passes, bloom, parallax, anchors, track, digest, timing
python3 review/review_analyze.py light|heads|bloom|parallax|vp <dir> [cam]   # the reviewer's measurements on those passes
python3 review/tone_table.py img ...          # tone targets with ref/crops/env/tools/metrics.py and spec/measure_color.py
```

## 7. Measured on our own renders (final quality: 720x1280, 16 samples, no denoiser, 4 threads)

The full tables, with the reference values measured by the same scripts and the values before the repair, are in `REVIEW.md`. Summary of the reviewed set:

| quantity | eye_two_shot | low_medium | high_two_shot | reference / target |
|---|---|---|---|---|
| same surface in cast shadow / lit, linear luminance: floor, map, wallpaper, wainscot | 0.16, 0.29, 0.30, 0.30 | 0.16, 0.31, 0.30, 0.31 | 0.15, 0.28, 0.30, 0.29 | 0.08 to 0.25 measured on a/t32.0, a/t13.5, a/t34.0, a/t58.5; brief 0.11 to 0.33 |
| the same as display luma | 0.43, 0.57, 0.58, 0.57 | 0.42, 0.58, 0.59, 0.57 | 0.42, 0.56, 0.58, 0.56 | 0.29 to 0.52 |
| hue, lit -> cast shadow | floor 14 -> 302, map 14 -> 238, wallpaper 356 -> 326 | 17 -> 313, 7 -> 251, 355 -> 327 | 15 -> 300, 13 -> 238, 356 -> 326 | 27 -> 252, 354 -> 251, 24 -> 246 |
| cast-shadow edge width 10-90 percent, p10 / median / p90 / max | 2.0 / 5.0 / 8.5 / 11.8 px | 2.0 / 9.6 / 15.5 / 21.8 px | 2.5 / 5.3 / 7.3 / 11.8 px | 1.7 to 12.6 px measured; brief 4 to 21 px |
| wall luminance in a ring around the heads (far, near) | 114, 74 | 97, 69 | 114, 81 | 95 to 170 |

Tone over the ten cameras with two placeholder actors: mean saturation 0.43 to 0.51, luma p1 0.12 to 0.15, p5 0.15 to 0.17, p50 0.22 to 0.30, p95 0.55 to 0.80, darkest tenth `#2d1f42` to `#4d1e35` (hue 255 to 331, S 0.42 to 0.61), Canny 60/140 edge density 0.081 to 0.085 on seven cameras (0.075 `low_medium`, 0.070 `top_down`, 0.056 `insert_rake`; reference interiors 0.077 to 0.114), featureless 40 px blocks 0.02 to 0.08.
Cost: 16.0 to 16.5 CPU seconds per final frame with two placeholder cards; 3.8 to 4.2 s wall on four threads while no other job ran, 6.1 to 7.9 s while another agent's render used about two cores.
Sun angle: 0.45 degrees (the spec says 1.5, the first build used 0.7). The glazing bars are 5 to 8 D from the surfaces they shadow; at 0.7 degrees their edges measured up to 32 px in the low medium shot.
