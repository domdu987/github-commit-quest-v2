# Camera: angles, framings, moves

The rules in brief:

1. One lens for everything: 22 mm on a 36 mm sensor, fit AUTO, 720x1280. Focal length 782.2 px, 49.4 deg horizontal, 78.6 deg vertical. Roll 0 (no dutch angles).
2. 1 scene unit = 1 D = the outer head diameter. A head D wide on screen at planar depth z is 782.2 / z px wide. Head width in px tells the shot size.
3. Heights have a purpose. Low: camera 1.2 D above the floor, pitched up 13.5 to 16.5 deg (authority, the hero's jab). Eye: head centre + 0 to 0.3 D, 1 to 3 deg down (dialogue). High: 3.3 to 4.4 D above the floor, 20 to 25 deg down (the small or defeated figure, wides). Inserts rake across props from 0.4 to 1.9 D.
4. The camera never parks: at most 6 frames under 0.25 px/frame, never a constant-speed run. Every move is eased in and out.
5. Two kinds of move: drift (6 to 10 %/s push or pull, 20 to 60 px/s slide, dying out before the shot ends) and snap (13 to 25 frames, x1.3 to x3, peak speed 1.6 to 1.9 x the mean).
6. Change the framing every 1.2 to 1.5 s on average (cuts, dissolves and snaps counted together). Film 1 ran faster than this (1.06 s by the picture tool): aim at 1.3 to 1.4 s next time.
7. Head centre between y 450 and 760 (0.35 to 0.59 H). Every whole head above y 880. Keep the caption band, y 880 to 950, free of heads and of picture text.
8. Two-shots are staged in depth: the near head is 1.36 to 1.46 x the far head, sits lower, and is 1.0 to 1.4 D nearer.
9. Fast frames (over 60 px/frame at the frame corners) get a camera streak on the set only. Characters stay sharp.
10. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.

Pictures (all from film 1, graded v1.1 sharp frames, without captions):
- `../../assets/bible/camera_angles.jpg`: low, eye and high, three of each, with the camera name, height, pitch and head widths.
- `../../assets/bible/camera_sizes.jpg`: close to establishing, by head width.
- `../../assets/bible/camera_inserts_map.jpg`: inserts, top views and the map mechanism.

Units used below: px at 720x1280, y from the top. D = head diameter = 1 scene unit. Frames at 30 fps. "g" = 0-based film frame. "%/s" = zoom rate (scale change per second). "px/frame" = corner speed, the largest displacement the camera gives a frame corner in one frame.

---

## 1. Reference (measured)

The two reference clips are clip A (16 shots, 65.2 s) and clip B (22 shots, 64.9 s). Both are 720x1280 at 30 fps. Source: `pipeline/spec/camera_motion.md` unless stated.

### 1.1 Lens, horizon, height, pitch

| Quantity | Clip A | Clip B |
|---|---|---|
| Focal length (vanishing points) | 622 to 870 px, median 787 px = 49 deg horizontal (range 45 to 60 deg) | not measurable (painted one-point sets); the jar orbit shows a moderately wide lens (inferred by the analyst, no number) |
| Horizon height | 0.20 to 0.67 H; 9 of 11 frames within 0.34 to 0.50 H, median 0.44 H | 0.26 to 0.55 H (8 frames) |
| Horizon roll | +0.25, -0.5, +0.2 deg (a/t16.0, t20.0, t21.0) | 0; one rotating top-down shot, -94 deg of roll in 6.5 s (b f1468-1663) |
| Interior eye line | 45 % of H (a/t32.0), 67 % (a/t16.0, low) | 43 % (b/t23.0), 42 % (b/t44.0) (`environment_materials.md`) |

Camera height and pitch measured on single frames (D = head diameter of the subject in that frame):

| Frame | Horizon y | Head centre y | D px | Camera height | Pitch | Class |
|---|---|---|---|---|---|---|
| a/t16.0 | 850-858 | 545 | 191 | 1.16 D above ground | up 15 deg | low |
| a/t20.0 | 594-608 | 650 | 180 | 2.5 D above ground, 0.3 D above head centre | down 3 deg | eye |
| a/t37.0 | 531-564 | 557 | 150 | at head centre (within 0.2 D) | down 5-8 deg | eye |
| a/t27.5 | 611 | 542 | 149 | 0.46 D below head centre (seated) | down 2 deg | chest level |
| a/t58.5 | 563-568 | 792 | 120 | 3.2 D above ground | down 5 deg | high wide |
| b/t44.5 | 625 | 647 | 197 | 0.1 D above head centre | down 1 deg | eye |
| b/t23.0 | 597 | 559 | 135 | 0.3 D below head centre | down 3 deg | eye |
| b/t42.0 | 432 | 794 | 177 | 2.0 D above head centre | down 15 deg | high |
| b/t14.5 | 402 | none | none | balcony view | down 17 deg | high wide |

The extreme low close-up at a/t14.5 to t15.0 (the boss leaning over the lens) is lower and steeper than a/t16.0 but was not measurable.

Share of angle classes (screen time). Every one of the 130 half-second stills of each clip (`__PROJ__/ref/a`, `__PROJ__/ref/b`) classified by eye for this chapter, using the camera height rules above (low: camera under the eyes, sky or ceiling behind the heads; high: floor or ground behind the figures; insert: an object or prop as the subject, no character face; top_down: looking straight down; establishing: place or vista with no character or only tiny ones). Approximate: one classifier, about 1 to 2 stills per class of judgement.

| Class | Clip A | Clip B | Film 1 (plan, 5 classes) | Target next time |
|---|---|---|---|---|
| eye | 38 % (50) | 38 % (49) | 27.2 % | 35-40 % |
| establishing / vista | 28 % (37) | 18 % (23) | (counted inside the other classes) | 15-25 % |
| insert | 17 % (22) | 27 % (35) | 26.6 % | 15-25 %, ceiling 27 %; warm, material objects, not flat diagrams |
| low | 9 % (12) | 2 % (3) | 22.7 % | 5-10 % |
| high | 7 % (9) | 8 % (11) | 16.1 % | 7-10 % |
| top_down | 0 | 7 % (9, the pendulum shot) | 7.4 % | at most one shot, 0-7 % |

Film 1 used low angles two to three times as often as the reference and too few eye-level and establishing frames. Dutch: none in either clip.

### 1.2 Shot size and position in the frame

Sizes are white face widths. Add about 10 % for the outer head diameter D.

| Class | Clip A face width | Clip B face width | Head centre y (median, range) | Offset from centre |
|---|---|---|---|---|
| Close | 283-355 px, median 308 (0.43 W) | 261-313, median 268 (0.37 W) | A 0.36 H (0.24-0.58), B 0.51 H (0.42-0.59) | A 0.05 W, B 0.12 W |
| Medium | 149-228, median 168 (0.23 W) | 148-242, median 177 (0.25 W) | A 0.45 H, B 0.51 H | A 0.16 W, B 0.10 W |
| Wide | 112-118 (0.16 W) | 47-135, median 71 (0.10 W) | A 0.49 H, B 0.57 H | 0.10-0.11 W |
| All heads (n = 45) | | | median 0.50 H, 10th-90th percentile 0.35-0.59 H | 67 % in the centre third |

- Headroom. This was not measured directly. Inferred from the medians above, with D = 1.1 x the face width: the head top sits at about 0.23 H in A close shots, 0.39 H in B close shots, 0.38 to 0.43 H in medium shots, and 0.45 to 0.55 H in wides.
- Caption band. Captions sit centred at x 360 with the text line centred on y 900 (`pipeline/spec/captions.md`). 100 % of head centres are above y 880, and 91 % of heads are wholly above it. The y 900 line crosses the chest in close shots, the thighs or shins in medium shots and the ground in wides. Never leave the lower quarter blank: fill it with ground that carries perspective lines.
- Two-shot in depth (a/t45.0-47.0): near head 210-309 px at x 154-252, far head 153-228 px at x 474-490, size ratio 1.36-1.40, far head 126-134 px higher. The equal-size profile two-shot (a/t20.5: 180 and 182 px, same height) is used only for confrontation.

### 1.3 Distances for the 22 mm lens (depth = 782.2 x D / on-screen D)

| Size | On-screen D | Camera to subject | Head centre y | Use |
|---|---|---|---|---|
| Extreme close | 390-440 px | 1.8-2.0 D | 0.30-0.40 H | reaction beat, 0.4-1 s |
| Close | 300-350 px | 2.2-2.6 D | 0.36-0.51 H | one face, chest under the caption |
| Medium (default) | 170-230 px | 3.4-4.6 D | 0.45-0.51 H | figure 0.43-0.61 H tall |
| Wide | 110-135 px | 5.8-7.1 D | 0.49-0.57 H | figure plus place |
| Establishing | 30-75 px | 10-26 D | 0.55-0.60 H | place, crowd; background figures at least 10 D behind the principal |

### 1.4 How often the framing changes, holds, static share

| Quantity | Clip A | Clip B |
|---|---|---|
| Shots, mean / median length | 16, 3.75 / 3.65 s (0.70-7.73) | 22, 2.62 / 2.45 s (0.40-6.53) |
| Framing change (cuts, dissolves and snaps together) | every 1.19 s median, 1.25 s mean | every 1.26 s median, 1.54 s mean |
| Same, read by the picture tool `score.py` (`deliver/QA_film.md`) | 1.39 s | 1.62 s |
| Fully static frames (zoom under 1.5 %/s and pan under 8 px/s) | 3.8 % | 5.5 % |
| Holds of 6 frames or more | 4, 1.30 s in all; longest 0.47 s = 14 frames (a f1718-1731) | 3, 1.03 s in all |
| Time share: snap / drift / in transitions / near static | 44 / 44 / 8 / 4 % | 17 / 64 / 11 / 8 % |
| Median corner speed | 332 px/s | 150 px/s |
| Zoom rate, 50th / 90th percentile of in-shot frames | 20.8 / 129 %/s | 9.7 / 64 %/s |
| Pan, 50th / 90th percentile | 133 / 787 px/s | 57 / 333 px/s |

Only one shot in 38 is near locked off: b f1315-1376, the inventor walking away (zoom -2.2 %/s, pan 4 px/s). His walk supplies the motion. Clip A shots arrive moving and settle: 645 to 872 px/s in the first 0.8 s of a shot, 66 to 137 px/s in the last 0.8 s. Clip B is flatter: 106 to 207 at the start, 72 to 159 at the end.

### 1.5 Every kind of move, measured

| Move | Measured | Examples |
|---|---|---|
| Drift push or pull | median 7.8 %/s (A, quartiles 2.5-17.5) and 7.6 %/s (B, 3.0-13.6), with 30-33 px/s of pan. A pushes in on 59 % of drift frames and pulls out on 19 %; B pushes 39 % and pulls 45 %. | B throne +30.0 / +6.7 / -1.6 %/s in the first quarter, middle half and last quarter of the shot (f729-802); A sunset +64.8 / +24.3 / -2.3 (f1792-1882). Six of eight sampled drifts end below 3 %/s. |
| Truck or slide | A4 workers: 59 px/s sideways, zoom 0.9 %/s. B9 banquet: slide 42 px/s with a pull of 8.2 %/s. | a/t12.0-13.0, b/t22.5-23.5 |
| Crane | B6: slow crane with tilt up to 100 px/s, zoom 8 %/s | b/t16.5-17.5 |
| Tilt | A15: 521 px/s following the falling train. B12: 158 px/s. B20: 153 px/s combined with a pull of 20 %/s. | a f1897-1930, b/t30.0-31.5 |
| Orbit | B5: background slides 89 px/s (median), zoom 5.5 %/s, 5.7 s; about a quarter turn (angle estimated, not measured) | b/t08.5-11.0 |
| Snap (in-shot reframe) | 0.3-1.1 s. A: 36 snaps, median 24.5 frames (quartiles 13-32). B: 22 snaps, median 13.5 frames (9-20). Scale x1.5 to x3 or the inverse, often with 150-700 px of pan or tilt. | A f418-445: tilt up and push x2.56 into the low-angle close-up. A f541-588: pull x0.50 with a 941 px pan into the two-shot. |
| Crash zoom | x3 to x10 or the inverse in 10-25 frames. Fastest peak corner speed: 5851 px/s (A f1740) and 6811 px/s (B f26). | A f1738-1751: pull-out x0.27 in 14 frames. B f21-30: whip-push x3.59 in 10 frames. B f625-649: pull-out x0.10 in 25 frames. B7: push x3.23 in 0.5 s. |
| Whip pan | B f160-166: 7 frames, the picture shifts 40-190 px per frame, gradient energy falls to 0.38 of sharp. A9: 1335 px in 1.17 s. B21: pull-out x0.20 with 1124 px of pan. | b f160-166 |
| Punch-in cut | B f146-147: a cut to a closer framing with speed lines, held close 0.4 s | b/t05.0 |
| Shake | A f894-930: about 5 Hz, 12 px per frame standard deviation, 86 px peak to peak, on one shot only (the sweating passenger) | a/t28.73-31.03 |
| Hidden cut | A f276-277: a cut inside a fast tilt. A f111-113: the train wipes the lens. | |
| Motion blur | Only on fast camera moves (40-190 px per frame). Characters stay sharp even when they move about 250 px per frame (A f1736-1740). | |

Easing. A snap's speed peaks at 1.71 x its mean (quartiles 1.56-2.09, n = 61), at 0.50 of the move (quartiles 0.33-0.67). For comparison, linear = 1.00, smoothstep 1.50, sine in-out 1.57, quintic 1.88. Drifts are eased too and die out before the cut.

Transitions (for completeness; the transitions chapter owns them). 81 % are cross-dissolves: A 9-17 frames (median 13), B 9-23 (median 10.5), with a smoothstep mix. Both shots keep moving through the dissolve.

### 1.6 Parallax and sharpness

- Parallax. Share of frame pairs 0.5 s apart that a flat 2D zoom or pan explains: A 11-12 %, B 43 % (`v3/shots/qa_parallax.py`, ratio 0.51). The rest show real 3D parallax. B has flat painted shots (the underground cross-section).
- Sharpness. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.

---

## 2. Our build (film 1)

### 2.1 The camera system

Three layers. Every take uses the same 22 mm camera.

**`pipeline/v3/stage/camrig.py`.** Constants: `LENS 22.0`, `SENSOR 36.0`, `FOCAL_PX 782.22`, `RES_X, RES_Y 720, 1280`, `FPS 30`.

| Call | What it does |
|---|---|
| `make_camera(scene, name="StageCam", lens=22.0)` | creates the camera and makes it `scene.camera` |
| `key_camera(frame, loc, look_at, rotation=None, lens=None, roll=0.0, cam=None, interp="SINE", easing="EASE_IN_OUT")` | one key; with `look_at` the horizon is level plus `roll` degrees |
| `key_pose(frame, pose, ...)` | keys a pose dict `{"loc", "rot"}` or `{"loc", "look_at", "roll"}` (+ `"lens"`) |
| `cam_for(subject_point, head_px, height_class="eye", yaw_deg=0.0, D=1.0, floor_z=0.0, screen_x=360.0, pitch_deg=None, cam_height=None, lens=22.0, screen_y=None)` | places the camera so that a head at `subject_point` is `head_px` wide. Classes: `"low"` 1.2 D above the floor, +13.5 deg; `"eye"` head + 0.3 D, -3 deg; `"high"` head + 0.417 x depth (clamped 2 to 3.5 D), -15 deg; `"top"` straight down. `yaw_deg` is clockwise from +y (0 = square on to the map wall). `screen_y` solves the pitch so the head lands on that row. |
| `dolly(pose, right, up, forward, pan_deg, tilt_deg)` | moves a pose in its own axes (truck, crane, push) and pans or tilts it |
| `drift(f0, f1, p0, p1, ease="sine")`; also `"cubic_out"`, `"quad_out"` | two keys. `sine` rests at both ends; `cubic_out` arrives moving and settles (a shot that starts on a cut). The camera holds after f1. |
| `snap(f0, f1, p0, p1, peak=1.7, pivot=None)` | one LINEAR key per frame on an ease whose peak speed is `peak` x the mean (1.571 = sine, 1.875 = quintic, up to 2.19). With `pivot` (the subject's head) the distance changes geometrically and the camera swings round the subject. |
| `whip(f0, f1, p0, p1)`, `whip_off(f0, f1, pose, pan_deg)`, `whip_on(f0, f1, pose, pan_deg)` | whip pans. Off: quadratic ease-in, cut on f1 + 1. On: starts `pan_deg` short and brakes (quartic ease-out). |
| `shake(f0, f1, amp_deg=0.45, every=3, seed=1)` | random pan and tilt keys every 3 frames on top of the existing move (see the warning in recipe 7) |
| `ease_sine`, `ease_quintic`, `ease_septic`, `ease_peak(u, peak)`, `focal_px(lens)`, `fcurves_of`, `clear_keys` | helpers |

**The take runners: what the takes really used.** No take after the hook keys a camera with `drift` or `snap`. Each take's `shot.py` defines a pure function of the film frame g, and the runner keys it on every Blender frame f = g + 1:

| Runner | Takes | Camera contract | How it keys |
|---|---|---|---|
| `pipeline/v3/shots/film.py` (hook) | shots 1-3 (takes A, B) | `cam_a(g)`, `cam_b(g)` -> (loc, look) from `keys(...)` on spherical (distance, yaw, pitch) or loc/look keys, eases `quad_out`, `quint`, `sine`, `hold`; take B mixes a 22 % constant-speed share into every segment (`CREEP = 0.22`) so it never parks | every frame |
| `pipeline/v3/film/s10/otake.py` (office) for 9-13; its copy `s17/otake.py` (grey and storm light) for 17, 18, 25 | 9-13, 17, 18, 25 | `cam(g) -> (loc, look_at, up, lens)`; `up=None` = world z; lens None = 22 | location, rotation and lens keyed every frame, then all keys set to `CONSTANT` |
| `__PROJ__/v3/film/s04/otake.py` (a separate office runner; identical copies in `s06/` and `s14/`) | 4-7, 14 | `cam(g) -> (loc, look)` (mathutils Vectors) | `camrig.key_camera(g + 1, loc, look, interp="LINEAR")` every frame |
| `pipeline/v3/set3d_ext/beach/bshot.py` | 8, 16, 23, 24 | `cam(g) -> (loc, look)` | `camrig.key_camera(f, loc, look, interp="LINEAR")` every frame |
| `pipeline/v3/set3d_kitchen/kshot.py` | 15, 26 | `cam(g) -> (loc, look)` | every frame |
| `pipeline/v3/film/s20/mc.py` (map, shared by s20-s22) and `film/s19/shot.py` | 19-22 | `cam_setup(g) -> {loc, look_at, lens, up, roll}`. Poses are (target t, distance d, direction v, up, roll). `mc.blend(a, b, e)` mixes the target linearly, the distance geometrically (`d0 x (d1/d0)^e`), and the direction and up normalised, so a snap never cuts a corner. Snap ease `mc.snap_e(g, a, b) = smoother(1 - (1 - x)^1.35)`. | every frame |

Shared helpers in every runner: `gf(t) = round((t + 0.1) x 30)` (an in-shot event at narration clock t), `gb(t) = round(t x 30)` (a shot boundary), `smooth` (smoothstep), `smoother` (quintic), `lerp`.

**Named setups.** The set modules return a dict `{loc, look_at, lens}` (+ `up`, `roll`). Make one into a camera with `office3d.make_camera(setup, name)`, which honours `up` and `roll`. Use the dict as the start pose of `cam(g)`. Sources: `A["cams"]` from `office3d.build()`, `PA["cams"]` from `office_props.build(A)` (or `X.all_cams(A, PA)`), `M.cams()` / `M.cam(name)` from `office_mech`, `A["cams"]` from `beach3d.build()` (+ `beach_ext.CAMS`, `cam_pose(name)`), and `A["cams"]` / `kitchen_geom.CAM_*` from the kitchen.

### 2.2 Named cameras and framings, every set

This section is the single list of named cameras for every set; `sets.md` points here and does not repeat it. Actor marks, set coordinates and the zones a camera must stay out of are listed once, in `sets.md` (office 3.3 and 3.5, map 4.1, beach 5.3 and 5.5, kitchen 6.1). All cameras are 22 mm unless a lens is given. "Used in" lists the shots that start from the setup; a take often moves it (see section 3). Every loc / look_at below was printed from the built anchors (`A["cams"]`, `PA["cams"]`, `M.cams()`) of the bundled code. Pitch is the angle of the loc -> look_at axis (+ = up); the horizon row follows from it: horizon y = 640 + 782.2 x tan(pitch) px.

**Office set** (`v3/set3d/office3d.py`, `A["cams"]`). World: map wall = plane y = 0, room toward -y, floor z = 0.

| Name | loc | look_at | Height, pitch | Frames | Used in |
|---|---|---|---|---|---|
| `insert_rake` | (-1.05, -0.62, 2.05) | (0.55, -0.05, 2.28) | 2.05 D, +7.7 deg | 0.7 D from the map, raking: the sheet recedes, track in the middle | family of 5 (end), 11a (`insert_rake_ny`), 25 |
| `low_medium` | (-0.95, -3.45, 1.2) | (-0.45, -0.3, 2.02) | 1.2 D, +14.4 deg | low on the hero mark, head about 240 px (set `API.md`; the code's own note says about 250), horizon 0.66 H | family of shot 2 (hook) |
| `low_rake` | (2.35, -2.5, 0.9) | (-0.25, -0.15, 2.2) | 0.9 D, +20.4 deg | low, raking along the map wall from the window side; actor at `boss_mark` 280 px, the hero beyond, ceiling boards and sign run to a vanishing point; horizon 0.73 H | parent of `low_three` (6) |
| `eye_two_shot` | (1.45, -6.2, 2.55) | (1.3, -0.5, 2.3) | 2.55 D, -2.5 deg | eye-level two-shot, near actor 1.39 x larger at screen right; horizon 0.47 H | parent of G (10, 18, 25) |
| `high_two_shot` | (1.8, -5.9, 3.7) | (1.35, -0.6, 1.55) | 3.7 D, -22.0 deg | high two-shot, floor patch and bar shadows, almost no ceiling; horizon 0.25 H | 3 (family), 11d |
| `high_steep` | (2.1, -4.6, 4.75) | (1.3, -0.9, 1.2) | 4.75 D, -43.2 deg | the floor fills the frame, horizon above the frame, pendant shade top left | not used |
| `wide_high` | (-1.9, -8.6, 4.4) | (0.7, -1.2, 0.7) | 4.4 D, -25.3 deg | back-left corner: whole room, window and sky at right, dark desk and chair in front; horizon 0.21 H | 4 (start) |
| `desk_fg` | (-1.6, -5.8, 2.25) | (-0.55, -0.3, 2.15) | 2.25 D, -1.0 deg | over the foreground desk; lamp and ink bottle 1.2-1.8 D from the lens; horizon 0.49 H | 12 |
| `top_down` | (0.9, -1.45, 4.8) | (0.9, -0.95, 0) + up (0, 1, 0) | 4.8 D, -84.1 deg | above the marks (flat cards look flat from here; tilt them back) | not used |
| `window_side` | (-3.2, -2.6, 2.1) | (1.2, -0.9, 2.0) | 2.1 D, -1.2 deg | from the left wall across the marks to the window and sky | parent of `window_tt` (14) |

Keep-out zones for office cameras and the actor marks: `sets.md` 3.3 and 3.5. The recipes below stand the chief at `boss_mark` and the hero at `gloat_near`. Head centres stand `sprites.feet_of(cast)[1]` above the floor: hero 2.460, chief 2.871.

**Office extensions: props and the shot framings** (`v3/set3d_ext/props/office_props.py`, `PA["cams"]`; "measured" = the module's own stills).

| Name | loc | look_at | What it frames (measured) | Used in |
|---|---|---|---|---|
| `calendar_cam` | (-1.605, -1.152, 3.921) | (-1.84, -0.048, 3.99) | calendar about 410 px wide, 12 deg rake, centre y 551; lens under the lamp shades | 4 (landing) |
| `spinner_rake` | `_aim(storm, 0.92, yaw 48, pitch 10, look_shift=(0.12, 0, 0.14))` = (-0.438, -0.658, 1.459) | (0.355, -0.052, 1.758) | insert_rake family, lens below-left; axis pitch +16.7 deg | 5 (end of fly-in) |
| `coast_rake` | `_aim(track_point(0.42), 1.55, yaw 55, pitch 16, look_shift=(0, 0, 0.12))` = (-1.198, -0.906, 1.578) | (0.022, -0.052, 2.126) | FLA. low left, N.Y. at the top. The props `API.md` still gives an older pose, (-1.058, -0.906, 1.612) -> (0.162, -0.052, 2.159), and measured storm y 924, N.Y. y 424 on it: unverified for the pose the code now builds | 5 (pull-back) |
| `low_three` | (2.40, -6.20, 1.0) | (1.325, -3.540, 1.877): yaw 22 deg off the normal, +17 deg | trio heads 129-142 px, sign above the hats | 6 (take moved it to (1.25, -5.50, 1.0)) |
| `chalk_rake` | `_aim(CHALK_BEND, 0.92, 58, 18)` = (-0.452, -0.514, 1.776) | (0.29, -0.05, 2.06) | raking on the chalk curve | 7a |
| `chalk_wide` | `_aim((0.30, 2.32), 2.05, 12, 4)` = (-0.125, -2.050, 2.177) | (0.30, -0.05, 2.32) | whole western Atlantic, sign edge at top | 7b |
| `high_wide` | (-0.45, -6.45, 4.0) | (-0.5, -0.6, 1.4) | 4.0 D, -24.0 deg; hero 127 px between senior_a 194 px and the chief 198 px; senior_b 211 px cropped at the right edge | 9a |
| `insert_front` | `_aim(track_point(0.42), 1.5, 10, 6)` = (-0.237, -1.521, 1.849) | (0.022, -0.052, 2.006) | storm y 864, N.Y. y 346 | 9b |
| `corridor_cam` (props version) | (0.273, -0.45, 1.398) | `track_point(0.8)` = (0.034, -0.052, 2.407), up (0, -1, 0) | 0.40 D off the paper on the line below the storm; N.Y. (360, 596) | 9c |
| `low_boss` | (1.92, -4.40, 1.2) | (1.45, -0.42, 2.27) | chief 181 px at (333, 536) = 0.42 H | 10 (rejected: hero in frame; the take used L1) |
| `G` (THE GLOAT FRAMING) | (1.55, -4.95, 2.85) | (1.25, -0.40, 2.62) | chief 173 px at (368, 597), hero at `gloat_near` 244 px at (619, 696), ratio 1.41, far head 99 px higher; N.Y. at (178, 637) | 10, 18, 25 |
| `G_prime` | G's loc, lens 30.36 | (0.95, -0.40, 2.80) | x1.38 zoom from G, centred between the chief (442, 623) and the label; hero cut at the right edge. `G_prime_dolly` = the same x1.38 as a dolly: loc (1.481, -3.703, 2.856), look_at (1.05, -0.40, 2.90), 22 mm | 18 |
| `insert_rake_ny` | (-1.30, -0.66, 2.55) | (0.30, -0.05, 2.74) | raking on the N.Y. end of the line | 11a-b |
| `low_two_wall` | (0.40, -3.70, 1.2) | (0.40, 0, 2.12) | hero 224 px at x 147, chief 218 px at x 556, +14 deg. As built the head centres sit at y 430-480 (above the 450-760 band of rule 7) and the feet are out of frame: fine for the waist-up 11c, wrong for a full-figure two-shot. Raising the aim breaks the low-class pitch. For a full-figure low two-shot pull back 1.2 D: loc (0.40, -4.90, 1.2) -> look_at (0.40, 0, 2.40), pitch 14 deg, heads 165-180 px at y 525-570, rug in frame (tested by a cold reader of this skill) | 11c |
| `label_insert` | (-0.249, -1.811, 2.887) | (0.125, -0.05, 2.87) | label about 470 px wide at y 465, arrow head and N.Y. at y 750; 1.84 D, 12 deg rake | 13 |
| `window_tt` | (-3.2, -2.6, 2.1) | (2.6, -1.0, 1.85) | hero 340 px at x 189, chief 146 px at x 479, teletype between | 14a |
| `sheet_full` / `sheet_fill_camera(center, facing, fill)` | `sheet_full` (fill 1.0) = (1.046, -3.139, 2.05), square on, 1.17 D from `sheet_hold` (1.75, -2.20, 2.05) | (1.75, -2.20, 2.05) | the sheet fills `fill` of the width | 14c (fill 0.86) |
| `PA["paths"]["persist_steps"]` | a `insert_rake_ny`, b the same 0.4 D lower, c `low_two_wall`, d `high_two_shot` | | the stepped pull-out | 11 |

**Map mechanism** (`v3/set3d_ext/mech/office_mech.py`; `M.cams()`, `M.cam(name)`). Builders: `M.corridor(u_lens, h, look_u, look_h, a='auto')` (up = wall normal), `M.plan(u_center, dist, a, roll)` (square on, north up), `M.rake(target, dist, elev_deg, az_deg, up)` (az 0 = from due south along the line, + = from the east), `M.world(a, s, h, u)` (a D east of the line, h D proud of the paper, u = track fraction). Values below were computed by the module on disk.

| Name | Definition | loc / look_at | What it frames | Used in |
|---|---|---|---|---|
| `rake_spinner` | rake(world(0.02, u 0.12, h 0.03), 0.80, 30, -55) | (-0.321, -0.48, 1.23) / (0.171, -0.08, 1.718) | spinner 108 px at (352, 750) | 19 (0) |
| `rake_north` | rake(world(0.05, u 0.40), 1.80, 35, -12) | (0.017, -1.082, 0.519) / (0.074, -0.05, 1.993) | both walls, N.Y. at y 520 | 19 (1) |
| `corridor_cam` (mech version, THE CORRIDOR VIEW) | corridor(-0.12, 0.35, 0.85, 0.06, a 'auto' = 0.155 D west of the chord) | (0.104, -0.40, 1.465) / (0.041, -0.11, 2.46), up (0, -1, 0) | N.Y. at (378, 652), clearance 0.027 D; spinner 410-440 px at the bottom right | 19 (2), 20 |
| `corridor_far` | corridor(-0.20, 0.70, 0.95, 0.10) | (0.065, -0.75, 1.371) / (0.056, -0.15, 2.566), up (0, -1, 0) | fallback | not used |
| `plan_view_start`, `plan_view` | plan(0.03, 1.2, roll -12), plan(0.62, 1.2) | (0.214, -1.25, 1.642), (0.008, -1.25, 2.216), up z | N.Y. y 363 (upper third) after the truck | 19 (3) |
| `spinner_high` | rake(world(0, u 0.17), 0.80, 52, -8) | (0.132, -0.68, 1.265) / (0.117, -0.05, 1.757) | spinner 164 px at y 630 | 19 (4) |
| `launch_end` | corridor(u_lens 0.33, ...) | (0.013, -0.40, 1.906) / (0.044, -0.15, 2.726), up (0, -1, 0) | after 0.45 D of travel; follow the line, never blend straight through the bend | 20 (start value) |
| `sign_cam` | from world(-0.04, u 0.42, h 0.30), up (0, -1, 0) = wall normal | (-0.018, -0.35, 1.999) / (0.093, -0.67, 2.231) | beside the speed sign | 20 end (start value) |
| `atlantic_rake` | rake(world(0.35, u 0.55), 1.90, 30, +40, up z) | (1.609, -1.0, 1.141) / (0.353, -0.05, 2.203) | cannot see into the lane (take used elev 62, az +16, 1.30 D) | 21 (replaced) |
| `label_end` | | (0.10, -1.55, 2.85) / (0.10, -0.054, 3.26) | label about 530 px wide | 22 start |
| `whole_map` | | (-0.45, -4.30, 2.55) / (0.05, -0.05, 2.50) | whole map, about 8 deg of yaw, frame, sign edge, ledge | 22 |
| `ny_arrow` | | (-0.05, -1.30, 2.45) / (0.07, -0.05, 2.60) | arrow head at N.Y. and Long Island | 22 end |

Map camera rules (`v3/set3d_ext/mech/API.md` 4): keep every camera south of the walls' south ends (u < 0.05) or above their tops (h > 0.55) unless it is inside the lane. Inside the lane, |a| < 0.08 from the LINE, not the chord. A camera that travels up the corridor follows the line: lens at `M.world(a, 0, h, u=u_lens(t))`, looking at u_lens + 0.3 to 0.6. Check a sight line with `M.sight_margin(...)` (< 0 = a wall hides the target). Wall height 0.50 D with the lens at 0.35 D. Two cameras share the name `corridor_cam`, the props version (shot 9) and the mech version (19, 20). They differ by 0.17 D in x.

**Beach** (`v3/set3d_beach/beach3d.py`, `A["cams"]`; the sea lies toward +y, the cottage row runs along x, sand z = 0).

Pitch, horizon and the head widths at the marks in the first seven rows were computed from the camera matrices (`v3/set3d_beach/REVIEW.md` 2.1).

| Name | loc | look_at | What it frames | Used in |
|---|---|---|---|---|
| `vista_high` | (-13, 8.2, 6.2) | (30, 1.6, 0.6) | -7.3 deg, horizon 0.42 H; high wide down the colony like a/t58.5, all lines to one vanishing point at 0.33 W; heads at `sand_a` / `sand_b` 58 / 49 px | parent of `beach_high` |
| `low_cottages` | (5.4, -11.3, 0.85) | (3.0, 0.0, 3.6) | +13.4 deg, horizon 0.645 H; low from the road; an actor at `road_a` 165 px; the wave towers behind the roofs at wave 1 | not used |
| `eye_beach` | (3.6, 13.2, 2.75) | (1.0, 7.6, 2.15) | -5.6 deg, horizon 0.44 H; eye level from the surf side, heads 117 / 158 px | not used |
| `sea_view` | (1.0, 4.4, 2.75) | (1.0, 30, -1.5) | -9.4 deg, horizon 0.40 H; their point of view; fog and wave come in here | not used |
| `wave_low` | (1.0, 6.4, 0.7) | (1.0, 20, 9.5) | +32.9 deg, horizon 0.895 H; 0.7 D above the sand; the wave face fills the frame at wave 1 | not used |
| `boardwalk_eye` | (-7, 3.85, 2.85) | (30, 3.4, 1.6) | -1.9 deg, horizon 0.48 H; planks, poles and wires to the vanishing point | not used |
| `surf_side` | (-8, 12.6, 2.3) | (30, 8.6, 0.6) | -2.5 deg, horizon 0.47 H; along the surf line | not used |
| `beach_shore_eye` (ext) THE BEACH FRAMING | (-7.4, 7.0, 2.6) | (22, 5.0, 1.054) | azimuth -3.9 deg, pitch -3.0 deg, horizon 0.47 H; sea at left, LONG ISLAND sign mid-right (x 405-555), cottage_07 and poles at right; the man about 5 D ahead | 16, 23 |
| `beach_high` (ext) | (-2.4, 10.0, 5.0) | (9.6, 8.6, 1.30) | 5 D up, -17.0 deg, 12 D from the deck chair, horizon 0.31 H; deck chair and umbrella centred | 8 (the take started 15 D from the chair) |
| `beach_low_wave` (ext) | (-6.0, 7.0, 0.7) | (13.633, 10.816, 3.511): 20 D ahead at azimuth +11 deg, pitch +8 deg | 0.7 D above the sand, the beach axis turned 15 deg seaward | 24 |

`BX.cam_pose(name)` returns the three ext poses (`beach_ext.CAMS`). Keep-out zones for beach cameras: `sets.md` 5.3. `make_camera` sets clip 0.05..5000.

**Kitchen** (`v3/set3d_kitchen/kitchen3d.py`, `A["cams"]`; the same numbers bpy-free in `kitchen_geom.CAM_TABLE`, `CAM_STEEP`, `CAM_WINDOW`).

| Name | loc | look_at | What it frames | Used in |
|---|---|---|---|---|
| `table` THE TABLE FRAMING | (0.225, -2.42, 1.80) | (0.225, -0.30, 1.07) | pitch -19.0 deg (horizon 0.29 H); weather box centred, its Thai between y 300 and 570, ฝนตก 76 px tall (kitchen `API.md`; in the s26 take at g1918 ฝนตก measured 83.5 px with the tail of ฝ, `s26/QA.md`); four-pane window above the paper, cup at right | 15 (end), 26 (after the snap, last frame) |
| `steep` | (0.225, -1.62, 2.30) | (0.225, -0.9439, 1.6178), 0.02 D below the weather-box centre (0.225, -0.9439, 1.6378) | pitch -45.3 deg, tight on the box (ฝนตก about 150 px, kitchen `API.md`) | 15 (start) |
| `window_tight` | (0.25, -1.05, 2.48) | (0.25, 0, 2.50) | pitch +1.1 deg; the four panes fill the frame | 26 (start) |

**Framings defined only inside a take** (code in `__PROJ__/v3/film/sNN/shot.py`, or in the skill where marked "bundled").

| Name | Take | Pose | Frames |
|---|---|---|---|
| `CAM_TWO`, `CAM_FACE` | hook take B (`v3/shots/film.py`, bundled) | (2.10, -5.25, 3.70) -> (1.53, -0.95, 2.05); (2.46, -4.60, 3.32) -> (2.01, -1.60, 2.20) | high two-shot, 3.7 D, -21 deg; the face after the snap push |
| `L1` (low single) | s10 (bundled) | (0.30, -4.10, 1.20) -> (0.70, -0.42, 2.30) | chief alone, 192 px at x 474, 0.40 H; 1.21 D, +16.5 deg |
| `GE` (end of the G push) | s10 (bundled) | (1.85, -4.95, 2.85) -> (1.45, -0.40, 2.62), 28.6 mm | chief 223, hero 317 px |
| grin close-up | s18 | G's position, 41 mm (41.5 in the camera path), aimed at the chief's head | chief 321-325 px |
| rug-level truck | s17 (bundled) | (1.32, -4.5, 0.73) -> (0.79, -4.5, 0.90), +14.5 deg | hero 229-237, chief 175-187 px |

### 2.3 Angle classes and shot sizes in film 1

Screen-time share by camera class (`__PROJ__/plan/shot_plan.json` `grammar_numbers`; target shares from the reference in 1.1: eye 35-40, establishing 15-25, insert at most 27, low 5-10, high 7-10, top_down 0-7 %): eye 27.2 %, insert 26.6 %, low 22.7 %, high 16.1 %, top_down 7.4 % (the newspaper start, the plan view of the corridor, the whole-map reveal), dutch 0. Classes at shot start: insert 7, low 7, eye 6, high 5, top_down 1. Roll appears only in the plan view's landing (-12 deg easing to 0) and in the shakes.

Heights and pitches actually used (from each take's camera path):

| Class | Height above the floor | Pitch | Shots |
|---|---|---|---|
| low | 0.70-1.34 D (0.73-0.90 in the truck of 17; 0.70 at the beach) | +8.7 to +16.5 deg (up to +33 in the beach wave tilt) | 2, 6, 10a, 11c, 17, 24 |
| eye | 2.07-2.85 D (head + 0 to 0.4 D) | -3 to +1.6 deg | 10b, 12, 14a, 16, 18, 23, 25b |
| high | 3.3-4.9 D | -14.6 to -25.3 deg | 3, 4a, 8a, 9a, 11d |
| insert | 0.4-2.2 D from the paper or prop | +4 to +23 deg, raking 10-60 deg off square | 1, 4b, 5, 7, 9b, 11a, 13, 14c, 25a |
| top_down / steep | 0.85-1.2 D from the surface | -45 deg (kitchen) to square on (map) | 15a, 19 (3), 22 |

Head widths (outer D, px) by size in film 1. Measured in the takes' render meta, and in the probe for the beach.

| Size | Film 1 head widths | Frames |
|---|---|---|
| Close | 288-330 px (hook shot 3 after the snap 288-310; s18 grin 321-325; s24 cut-in about 290) | g120, g1124, g1720 |
| Close-medium | 244-317 px near head in G (with 173-223 far) | g650-690 |
| Medium | 145-200 px (s06 trio 145-194; beach man 152-199; low single 192) | g300, g1019, g615 |
| Wide | 96-148 px (s04 wide 96-115; s11 high two-shot 138-148; hero in s09 128-145) | g145, g785, g520 |
| Establishing | 35-64 px (s08 beach vista man 54-64, woman 35-39) | g419, g447 |

### 2.4 Rules the workers were held to, and the thresholds of the tools

| Rule | Threshold | Tool or source |
|---|---|---|
| A "move" (snap, whip, fly-in) | corner speed > 12 px/frame (`MOVE`) | `v3/shots/qa_motion.py` (hook), the same in `otake.cmd_qa`, `film/out/grammar.py` |
| Never static | no run of more than 6 frames under 0.25 px/frame (`STATIC`); map takes use 0.3 px/frame (`mc.runs`) | same |
| Never linear | no run where the speed changes by less than 2 % per frame while above 1 px/frame (hook, office takes); map takes: within 6 % over 7+ frames; beach and kitchen: 8+ frames | `qa_motion.py`, `otake.py`, `mc.runs`, `bshot`, `kshot` |
| How to avoid parking | mix a constant-speed share into the eased keys (`CREEP = 0.22` in the hook; 8 % in s23; "creep" terms in s19-s22) | `v3/shots/film.py` |
| Framing change | every 0.6 to 1.6 s per interval; mean 1.2 to 1.5 s over the film | `v3/README.md`; counted by `film/out/grammar.py` |
| Snap length | 12-16 frames by default, 17-25 for big moves; nothing under 8 frames outside the hook | `__PROJ__/plan/shot_plan.json` notes |
| Streak (camera motion blur) | frame corner faster than 60 px/frame (`STREAK_MIN`); shutter 0.40 frame; the plate only (actors laid over sharp from `render_layers.py`); whole frame only in whips | `v3/shots/post.py`, runners |
| Head position | whole head above y 880; main head centre 0.35-0.59 H; `cam_for` advises y 300-760 | `film/CONVENTIONS.md`, `stage/API.md` 5 |
| Head size | aim for 180 to 310 px in character shots | `v3/README.md` (probe step) |
| Two-shot depth | near / far head ratio 1.36 to 1.46 | `v3/README.md`, `probe.py` |
| Back views | nobody's back to the camera | `film/CONVENTIONS.md` |
| Text in the picture | every Thai text above y 600, clear of the caption at y 900 | `__PROJ__/plan/shot_plan.json` notes |
| Map lens | inside the lane, abs(a) < 0.08 D from the line; `M.sight_margin` >= 0 | `v3/set3d_ext/mech/API.md` |
| Card limits | view axis steeper than 50 deg leans the card back; keep actors 2 D clear of walls in such shots or hide them | `stage/API.md` 10 |
| Parallax | 10 to 45 % of 0.5 s pairs explained by a flat 2D move (a flat film reads about 90) | `v3/shots/qa_parallax.py` (SIFT, RANSAC at 1 px, `RATIO` 0.51, caption rows 830-975 masked) |
| Sharpness | Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. | client decision |

Film 1 measured against these: 51 framing changes (25 transitions + 26 snaps), interval mean 1.26 s, median 1.22 s, range 0.32-2.42 s as conformed (the plan's count: median 1.21 s, range 0.34-2.40 s; `v3/film/out/CONFORM.md`). The picture tool reads 1.06 s (`deliver/QA_film.md`). Static frames 3.2 %, longest hold 12 frames. Zoom median 11.4 %/s, pan median 39 px/s. Snap peak/mean 1.69. Snaps fill 22.9 % of the time. Longest constant-speed run in the conformed film: 21 frames (s21 drift, g1543-1563). Parallax: flat 2D share 31.5 % (shots 4 and 12 the most card-like).

---

## 3. The 26 shots of film 1

Times are film seconds (shot boundary = round(t x 30)). Speeds are the takes' own corner speeds in px/frame unless marked px/s or %/s. Heights are above the floor (office, beach, kitchen) or from the paper (map). Sources: `__PROJ__/plan/shot_plan.json`, each take's `QA.md`, `v3/out/QA.md`, the camera path of each `shot.py`.

| # | Time (g) | Start framing | Class | Moves (frames, speed) | End framing | Reference imitated |
|---|---|---|---|---|---|---|
| 1 | 0.00-1.31 (0-38) | hook raking insert on the pencil at the storm, 1.44-1.84 D, +13 to +23 deg, yaw -39 deg, already moving | insert | snap push g10-46, peak 154 at 0.47 s (peak/mean 2.35); follows the growing line, swinging toward frontal (yaw -39 to -10) | pull-out under way | A1 0.0-1.5 s (push x1.72 in 0.5 s); B1 |
| 2 | 1.31-2.42 (39-72) | the 14-frame pull-out (`PULL` g33-47) swings round the hero | low | lands on the low_medium family: 1.17-1.20 D, +15.2 to +15.9 deg, hero 179-188 px; snap push x1.35 g60-64, peak 110, hero 252 px; whip-off g69-72 (34 deg, quad-in) | whip, cut at g73 | A1 1.5-3.7 s; height of a/t16.0 |
| 3 | 2.42-4.31 (73-128) | whip-on 7 frames (30 deg, quartic out) into `CAM_TWO` | high | high two-shot 3.30-3.73 D, -20.3 to -21.3 deg, near 221-248 / far 158-168 (ratio 1.40-1.47); slow push with CREEP 0.22; snap push g113-116, peak 34, onto the hero's face 288-310 px | `CAM_FACE` | A5 tail (a/t19.0-21.0); B3-4 |
| 4 | 4.31-6.64 (129-198) | `wide_high`, 3.99-4.32 D, -25 deg, heads 96-115 | high, then insert | truck right and push (cam x -2.18 to -1.33); flight g146-158, peak 951 px/s, whole-frame streak g148-156, quintic, under the lamp shades; push about 8 %/s; whip-tilt down-right g195-198 (peak 456 px/s, streaked whole) | `calendar_cam` (calendar 361-423 px wide) | A2 3.8-9.2 (forward flight x2.92); a/t36.0; exit as A f276 |
| 5 | 6.64-9.04 (199-270) | arrives inside the whip-tilt | insert | fly-in g199-226 (peak 298 px/s, quartic out, radial streak g199-207) to 0.92 D from the paper; orbit 5 deg + push 6 %/s (7.45-7.90); pull-back with tilt up g240-255 (peak 48 px/s) dying by 8.7; no snap | `insert_rake` family / `coast_rake` (N.Y. enters the top) | A3 (fly-in x63); B5 end |
| 6 | 9.04-11.21 (271-335) | `low_three` moved to (1.25, -5.50, 1.0), yaw -20 deg | low | crane up 0.25 D (g262-306; height 1.03 to 1.34 D, pitch +12.5 to +8.7) so the sign rises into the top third; push 15 %/s easing to 0 at the whack (g303-323), then 1.2 %/s; nothing over 12 px/frame; heads 145-194 | same, tighter on the chief | A4 (a/t12.0-13.0) seen from a/t16.0's height; B6 crane |
| 7 | 11.21-13.38 (336-400) | `chalk_rake` (0.92 D, yaw 60 to 56, pitch 18) | insert | follow pan on the chalk tip; snap g366-380 (14 f, quintic + sine, peak 226 px/s, plate streak g370-374): pull back and swing toward frontal; drift push 4 %/s | `chalk_wide` (12 deg of yaw kept) | B6 b/t13.5-16.0; A10 a/t38.5; A6 pans |
| 8 | 13.38-16.83 (401-504) | `beach_high` family, 15 D from the chair (4.88 D up, -16.8 deg), man 54-64 px | high, then eye | crane down and push 8 %/s; crash push g448-473 (25 f) to eye level (1.40 D, +0.7 deg) under the umbrella, man 194-199 px at 0.48 H; drift | close-medium on the sleeper | A7 (push x3.05 in 0.83 s, then drift 10 px/s); a/t52.0-54.0 |
| 9 | 16.83-20.32 (505-609) | `high_wide` (3.69 D, -24 deg), near heads 239-265, hero 145 | high, insert, low (worm's eye) | push 12 %/s; crash push g534-547, peak 224, whole-frame streak g538-543, threads between heads to `insert_front` (1.5 D, yaw 10); climbs with the pencil; snap swing g578-588, peak 67, to `corridor_cam` (props version, 0.39-0.40 D off the paper, pitch +65 deg against world z, up = wall normal); drift 10 %/s to near still | corridor view up the red line | A4 a/t11.5-13.0; A10 (push x2.57 into a macro); a/t48.0 |
| 10 | 20.32-23.13 (610-693) | `L1` low single, 1.21 D, +16.5 deg, chief 192 px | low, then eye | slow push accelerating into the snap; snap g628-644 (17 f, quintic, peak 40 at g636): rises 1.6 D to 2.85 D, pans right, 0.12 D crane arc; then zoom 22 to 28.6 mm + truck 0.3 D right, 30 easing to 0 %/s (x1.3) | `GE`: chief 223, hero 317, ratio 1.42 | A5 (a/t16.0, then x0.50 back with a 941 px pan); A11 mirrored; B10 |
| 11 | 23.13-26.41 (694-791) | `insert_rake_ny` (2.49-2.55 D, +7 deg) | insert, low, high | slide down 0.4 D and back (peaks 17 and 14); snap out g737-746, peak 148, whole streak g738-743, to `low_two_wall` (1.20-1.23 D, +14 deg, heads 226-234); snap out and up g765-775, peak 157, to `high_two_shot` (3.67 D, -22 deg, heads 138-148); one static frame g748 | `high_two_shot`, drifting | B14 (stepped pull-out); A5 |
| 12 | 26.41-27.96 (792-838) | `desk_fg` (2.25 D, -1 deg) | eye | pull back along the axis 0.06 D in to 0.56 D back (about 8 %/s) and slide 0.34 D right (about 42 px/s); no snap; near 240-299 px, far 123-144 px | same, wider | B9 (pull 8.2 %/s, slide 42 px/s) |
| 13 | 27.96-28.92 (839-867) | punch-in cut onto `label_insert` from 1.30 x the distance | insert | lands in 4 frames (cubic out, peak 118 at g839, plate streak g839-840); white speed lines 6 frames; 2-frame shake (roll 0.45 deg); drift push 5 %/s | `label_insert` (label about 480 px) | B3 b/t05.0 (punch-in); a/t32.0 |
| 14 | 28.92-31.85 (868-955) | `window_tt` (2.07-2.18 D), hero near 261-336, chief 141-168 | eye, then insert | truck right 0.30 D + push 8 %/s, aim pans back 0.55 D; crash push x3 g899-912 (14 f), peak 416, plate streak g903-908; tilt down 10 %/s from header to the two typed lines; near still from g951 | `sheet_fill_camera` (fill 0.86) | B7 (crash push x3.23 in 0.5 s); a/t31.5 |
| 15 | 31.85-33.77 (956-1012) | `steep`: 0.85 D from the weather box, 44-45 deg down | top_down, then eye | drift in 4 %/s with a slide left (1.3-1.4 px/frame); crash pull-out g977-994 (17 f), peak 67, tilt trailing, small arc, 4 streaked frames; drift push 5 %/s to the cup | `table` (THE TABLE FRAMING) | B7-8 (pull-out from the goblet); a/t36.0 |
| 16 | 33.77-36.19 (1013-1085) | `beach_shore_eye` (2.6 D, -3 deg), man 152 px | eye | truck right 0.3 D + push; snap g1042-1056 (14 f), peak 167: tilt up to +46 deg and 22 deg right (sky, vane and chimney); creep; tilt down g1062-1088 (86 easing to 9 px/frame) to +6 deg; man 248 px | low-tilted medium on the shrug | B7; a/t36.5-38.0; B12 tilt |
| 17 | 36.19-37.42 (1086-1122) | rug-level camera 0.73 D, +14.5 deg | low | truck left 0.53 D while rising to 0.90 D (speed 0.47-4.3 px/frame); no snap; settles as the chief reaches `boss_mark`; hero 229-237, chief 175-187 (ratio 1.26-1.32) | same | A10 tail a/t43.0-44.0; walk of B17 |
| 18 | 37.42-39.62 (1123-1188) | HARD CUT, G's position at 41 mm on the chief's head (321-325 px) | eye | crash zoom-out g1125-1141 (move g1127-1137, peak 73) to G at 22 mm (x0.52); 2.5 %/s lens creep + 0.02 D/s truck; snap g1160-1172 (peak 52) to `G_prime` (30.36 mm); crash push toward the map from g1188 (peak 146) | `G_prime`, then the push into the map | A11 (hard cut, zoom out x0.30, push x1.38); B16 |
| 19 | 39.62-47.30 (1189-1418) | finishing the crash push x6 g1188-1205 | insert, high, low, top_down | lands on `rake_spinner` (0.8 D, 30 deg rake); snap 1 g1225-1238 to `rake_north` (x0.45 back, 35 deg); drift push 10 %/s; snap 2 g1292-1308 to `corridor_cam` (lens 0.345 D, 0.155 D west of the chord); creep u -0.17 to -0.13; snap 3 g1328-1345 to `plan_view_start` (roll -12 to 0 by g1374); truck north 0.6 D to `plan_view`; snap 4 g1372-1385 to `spinner_high` (52 deg, push x2); bonk shakes g1396, g1408 (6 f each); near still from g1413; snap peaks 160-358 | `spinner_high`, near still | B19 (one rotating top-down take); A12 (rail view); A5 (length) |
| 20 | 47.30-50.53 (1419-1515) | `corridor_cam` (0.35 D up) | low (worm's eye on the map) | creep 6 %/s, accelerating; launch snap g1443-1467: the lens rides 0.255 u behind the flung spinner along the line, 0.50 D in 1.1 s; 5 Hz shake on the look point (amplitude 0.010 D, e^(-k/16)); peak 223 at g1470; push with decaying shake to the speed sign (420-435 px) | near `sign_cam` | A12 (travel past a roadside figure); A8 shake; B20 |
| 21 | 50.53-52.37 (1516-1570) | chase view in the lane, 0.30 D up | high (oblique) | whip pull-out g1509-1529, peak 403 at g1517, to a high oblique (rake az +16, elev 62, 1.30 D, up z); drift push 6 %/s north (d x 0.94^t), elevation +1.5 deg/s, azimuth -2 deg/s | high oblique on the streak | B21 first half (whip pull-out x0.20 with 1124 px of pan); A6 |
| 22 | 52.37-55.48 (1571-1663) | travelling north in the lane, rising out (0.33 to 1.5 D off the paper, up turning from the wall normal to z) | low, top_down, insert | peak 248 at g1575; rests on `label_end`; crash pull-out g1593-1609 (x0.36) to `whole_map` (4.20-4.25 D, about 8 deg yaw), whump shake; hold as slow drift 53.70-54.10; snap g1626-1642 push x4.3 to `ny_arrow` (0.98 D); creep decays, near still from g1659 | `ny_arrow` | A13 (push, 0.47 s hold, crash pull-out x0.27); B21 second half |
| 23 | 55.48-57.35 (1664-1719) | `beach_shore_eye` exactly | eye | push 1.55 D along the axis, 1 - (1 - x)^2.2 plus 8 % creep (man 145 to 197 px, x1.36); turns 4.35 deg seaward; 0.2 deg wind shake; 0.4-4.8 px/frame | same axis, tighter | A14 (push 24 %/s easing to 0); B18 |
| 24 | 57.35-59.61 (1720-1787) | HARD CUT, `beach_low_wave` family: 1.3 D, +15 deg, close on two faces (man about 290 px) | low | crash pull-out g1730-1748 (19 f) with tilt up, lens down to 0.70 D, pitch to +31 to +33 deg; 5 Hz shake from g1752 (pitch 3.15 deg, yaw 1.2 deg) | wide low, the wave fills the left 60 % | A13 (crash pull-out x0.27); A15 tilt; B18 |
| 25 | 59.61-62.44 (1788-1872) | `insert_rake` family, lens 1.3 D from its target, creeping in 3 %/s | insert, then eye | tilt-up follow of the spinner (move g1802-1826, peak 70); label reads g1819-1838; snap g1838-1852 (peak 204) pull back into G (22 to about 23.6 mm), not G'; impact g1862; 5 Hz shake 8 frames (look amplitude 0.045 D, decaying) | G | A15 (tilt with the train, flash); A16; A11 framing |
| 26 | 62.44-65.40 (1873-1964) | `window_tight` (1.05 D from the window) | eye | drift in 2 %/s under a 5 Hz shake (look amplitude 0.028 D, decaying to 0 by g1941), 20-35 px/frame; snap g1901-1917 (16 f), peak 223, pull back to 2.42 D (x0.43) with the tilt trailing, streaked whole g1905-1914; settle 0.6 %/s; push g1929-1953, 26 %/s easing to 0; static hold g1954-1964 | `table` (THE TABLE FRAMING) | A16 (pull back x0.37); B22 (pull easing to 0, last 0.4 s still) |

Named callbacks: G (10 -> 18 -> 25, day, grey, storm), THE BEACH FRAMING (16 -> 23), THE TABLE FRAMING (15 -> 26), the corridor view (9 -> 19, 20, 22).

---

## 4. Recipes

Tested: the header plus recipes 1, 2, 3, 4, 5, 7a, 8, 9 and 10 were run with bpy 5.3 against the skill's `pipeline/` folder, without rendering. Recipes 6, 7b and 11 were run as plain Python. The numbers in the comments are the printed results. Use one camera object per take: keys left on a reused camera disturb later recipes.

**Header (shared by the camrig recipes).**
```python
import os, sys, math
PIPE = "<skill>/pipeline"                                   # the skill's pipeline/ folder
sys.path[:0] = [os.path.join(PIPE, p) for p in ("v3/stage", "v3/set3d", "v3/set3d_ext/props",
                                                 "v3/set3d_ext/light", "v3/set3d_ext/mech")]
import bpy
import camrig, render, sprites
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "draft", threads=2)
cam = camrig.make_camera(scene)                             # 22 mm, 782.2 px
HB = (1.30, -0.42, sprites.feet_of("boss")[1])              # chief's head centre at boss_mark, z 2.871
HH = (2.40, -1.70, sprites.feet_of("hero")[1])              # hero's head centre at gloat_near, z 2.460
```

**1. Slow push (drift).** 2 s, eye level, head 170 to 215 px (x1.26, about 12 %/s).
```python
a = camrig.cam_for(HB, head_px=170, height_class="eye", yaw_deg=-4.0, screen_x=380)
b = camrig.cam_for(HB, head_px=215, height_class="eye", yaw_deg=-4.0, screen_x=380)
camrig.drift(1, 61, a, b, ease="sine")      # use ease="cubic_out" when the shot starts on a cut
# head (x, y, width): f1 (380, 650, 170), f31 (380, 656, 190), f61 (380, 664, 215); camera 3.17 D up, -3.0 deg
```
To keep the camera from parking at the end, give f1 the shot's last frame minus 0 to 6, not minus 12, or add a creep (recipe 11).

**2. Snap between two framings.** 16 frames, peak 1.7 x mean, swinging round the subject.
```python
s0 = camrig.cam_for(HB, head_px=150, height_class="eye", yaw_deg=-4.0)
s1 = camrig.dolly(camrig.cam_for(HB, head_px=230, height_class="eye", yaw_deg=-4.0, screen_x=330), right=0.3)
camrig.snap(1, 17, s0, s1, peak=1.7, pivot=HB)
# head 150 px at (360, 644) -> 230 px at (261, 668); measured peak/mean of the head's screen motion 1.78
```
Place the snap so that it ends on the stressed word: start it at gf(word time) minus about 2/3 of its length. Film 1 snaps were 13 to 17 frames.

**3. Crash push to a face.** x2.75 in 16 frames, quintic, ending on a close-up at y 560.
```python
c0 = camrig.cam_for(HB, head_px=120, height_class="eye", yaw_deg=-4.0)
c1 = camrig.cam_for(HB, head_px=330, height_class="eye", yaw_deg=-4.0, screen_y=560)
camrig.snap(1, 17, c0, c1, peak=1.875, pivot=HB)
# head 120 -> 330 px; peak/mean 1.94
```
Frames whose corners move over 60 px/frame need the plate streak: render plate and matte (`v3/shots/render_layers.py` or the runner's `render` command) and run the runner's `post`. In s18, the hard cut in and the crash out were done as a zoom (41 mm to 22 mm from one position). That keeps the near/far ratio of the two-shot.

**4. Whip pan with a hidden cut.** Take A ends with a 4-frame whip-off and the cut falls on the next frame. Take B starts panned the same way and brakes over 7 frames (the hook's g69-79).
```python
pa = camrig.cam_for(HB, head_px=190, height_class="eye")
camrig.whip_off(1, 4, pa, 34.0)                     # take A, last 4 frames; cut on frame 5
pb = camrig.cam_for(HH, head_px=240, height_class="high", yaw_deg=-9.0, screen_y=640)
camrig.whip_on(5, 11, pb, 30.0)                     # take B, first 7 frames (separate camera in its own take)
# view yaw per frame: 0, 3.8, 15.1, 34.0 | cut | -39.0, -23.5, -14.9, -10.9, -9.4, -9.0, -9.0
```
Streak the whole frame on the whip frames (`post.py` does this for the 6 frames round the cut). For a cut hidden in a tilt (shots 4 to 5), do the same with a down-right tilt of 4 frames and a 9-frame braking fly-in.

**5. Crane.** Up 0.25 D over 1.5 s, with a small compensating tilt so the subject stays put while the background drops.
```python
k0 = camrig.cam_for(HB, head_px=170, height_class="low", yaw_deg=-20.0)
k1 = camrig.dolly(k0, up=0.25, tilt_deg=-3.0)       # tilt_deg + = up; 0 lets the subject sink in frame
camrig.drift(1, 46, k0, k1, ease="sine")
# camera 1.20 -> 1.45 D; head (360, 536, 170) -> (360, 535, 173)
```
Shot 6 did the reverse: a crane with the framing rising, so the sign moved from y 408 to 369-381 (top third).

**6. Handheld drift** (shot 23). A push that never parks, plus a 0.2 deg wind sway from two incommensurate sines per axis. The function is runner style: it returns (loc, look) for `bshot.py`.
```python
import math
def direction(az, pi):                      # az from +x toward +y, degrees
    a, p = math.radians(az), math.radians(pi); return (math.cos(p)*math.cos(a), math.cos(p)*math.sin(a), math.sin(p))
LOC0, AZ0, PI0, PUSH, R0, R1 = (-7.4, 7.0, 2.6), -3.9, -3.0, 1.55, 1653, 1720     # THE BEACH FRAMING
def cam(g):
    x = min(1.0, max(0.0, (g - R0) / float(R1 - 1 - R0)))
    s = 0.92 * (1 - (1 - x) ** 2.2) + 0.08 * x                  # fast start easing out + 8 % creep
    d = direction(AZ0, 0.0); loc = tuple(LOC0[i] + d[i] * PUSH * s for i in range(3))
    t, a = g / 30.0, 0.20
    az = AZ0 + a * (0.6 * math.sin(2*math.pi*1.7*t) + 0.4 * math.sin(2*math.pi*2.9*t + 1.3))
    pi = PI0 + a * (0.6 * math.sin(2*math.pi*2.3*t + 0.7) + 0.4 * math.sin(2*math.pi*3.7*t + 2.1))
    dd = direction(az, pi); return loc, tuple(loc[i] + 10.0 * dd[i] for i in range(3))
# pitch sway over the shot: 0.39 deg peak to peak = 5 px
```

**7. 5 Hz shake.**

(a) `camrig.shake` adds random keys every 3 frames (5 Hz). Its default amplitude is far below the reference:
```python
camrig.key_pose(1, pa); camrig.key_pose(31, pa)
camrig.shake(1, 31, amp_deg=0.45, every=3, seed=7)
# measured: head y 17 px peak to peak, 2.5 px frame-to-frame sd  (reference: 86 px, 12 px)
```
Use about `amp_deg=2.3` for the reference's 86 px. This is inferred by linear scaling and was not run.

(b) What film 1 used (s24): a sine shake on the pitch and yaw of `cam(g)`, ramped in over 4 frames.
```python
def shake5(g, g_start, amp_pitch=3.15, amp_yaw=1.2, ramp=4):        # degrees to add to pitch, yaw
    if g < g_start: return 0.0, 0.0
    e = min(1.0, (g - g_start) / float(ramp)); e = e * e * (3 - 2 * e); t = (g - g_start) / 30.0
    dp = e * amp_pitch * (0.8 * math.sin(2*math.pi*5.0*t) + 0.2 * math.sin(2*math.pi*7.3*t + 1.1))
    dy = e * amp_yaw * math.sin(2*math.pi*5.0*t + 1.7)
    return dp, dy
# over 2 s (g_start + 0..60): pitch 5.62 deg = 77 px peak to peak, frame-to-frame sd 24.7 px
```
For an impact, use 8 frames with a linear decay, as s25 does: `a = 0.045 * (1 - k / 8)` D on the look point, `ph = 2*pi*5*k/30`.

**8. Low-angle hero shot** (a/t16.0, film 1 shots 2 and 10).
```python
low = camrig.cam_for(HB, head_px=190, height_class="low", yaw_deg=-6.0, screen_x=380)
camrig.key_pose(100, low)
# camera (1.60, -4.24, 1.20), pitch +13.5 deg; head 190 px at y 501 (0.39 H)
```
Put something bright behind the head: a window, sky or a lamp. In film 1 the low angles looked into a dark ceiling (section 5).

**9. Top view on the map.** The plan view truck of shot 19: north up, the roll easing from -12 deg to 0.
```python
import office_mech as M                                  # numbers need no build(); render needs S.build + X.build + M.build
def smoother(u): u = max(0.0, min(1.0, u)); return u*u*u*(u*(6*u - 15) + 10)
a = M.cam("plan", u_center=0.03, dist=1.2, roll=-12.0)    # plan_view_start
b = M.cam("plan", u_center=0.62, dist=1.2)                # plan_view
for f in range(1, 29):                                    # 0.9 s
    s = M.lerp_setup(a, b, smoother((f - 1) / 27.0))
    camrig.key_camera(f, s["loc"], s["look_at"], roll=(s.get("roll") or 0.0), interp="LINEAR", easing="AUTO")
# f1 camera (0.214, -1.25, 1.642), roll 12 deg; f28 (0.008, -1.25, 2.216), roll 0; N.Y. lands at (396, 377)
```
Actor cards cannot be used from straight above. The view axis is past 50 deg, so a card leans back into the wall. Hide them, or keep them 2 D clear of walls.

**10. Over-the-shoulder two-shot in depth** (G, film 1 shots 10, 18 and 25). The near character's head is cut by the right edge by less than 10 %.
```python
G = ((1.55, -4.95, 2.85), (1.25, -0.40, 2.62))           # office_props 'G'
camrig.key_camera(1, G[0], G[1])
# far chief 173 px at (368, 597); near hero 244 px at (619, 696); ratio 1.41
```
To push on it, zoom (22 to 28.6 mm) and truck 0.3 D right, as `GE` does. A dolly alone grows the near head x1.47 and breaks the ratio. The chief stands 0.0 to 0.1 D from the map.

**11. Runner template** (`cam(g)` for `otake.py`; this is s10's code). It holds a slow push that accelerates into a snap, a quintic snap with the pan trailing, and an eased zoom push.
```python
G0, G1, H_IN, H_OUT = gb(20.317), gb(23.129), 7, 7        # 610, 694
SNAP = (gf(20.82), gf(21.35))                             # 628, 644
L1 = ((0.30, -4.10, 1.20), (0.70, -0.42, 2.30))
GC = ((1.55, -4.95, 2.85), (1.25, -0.40, 2.62))
GE = ((1.85, -4.95, 2.85), (1.45, -0.40, 2.62), 28.6)
def cam(g):
    if g < SNAP[0]:
        u = (g - (G0 - H_IN)) / float(SNAP[0] - (G0 - H_IN)); k = 0.035 * (0.4 * u + 0.6 * u * u)
        return lerp(L1[0], L1[1], k), L1[1], None, 22.0
    l0 = lerp(L1[0], L1[1], 0.035)
    if g < SNAP[1]:
        x = (g - SNAP[0]) / float(SNAP[1] - SNAP[0]); u, ut = smoother(x), smoother(max(0.0, (x - 0.06) / 0.94))
        loc = lerp(l0, GC[0], u); loc = (loc[0], loc[1], loc[2] + 0.12 * math.sin(math.pi * u))
        return loc, lerp(L1[1], GC[1], ut), None, 22.0
    x = (g - SNAP[1]) / float(G1 + H_OUT - 1 - SNAP[1]); e = 1 - (1 - x) ** 2.2
    return lerp(GC[0], GE[0], e), lerp(GC[1], GE[1], e), None, 22.0 * (GE[2] / 22.0) ** e
# camera z at g603 / 636 / 644 / 700: 1.20, 2.16, 2.85, 2.85; lens 22 -> 28.6 at g700
```
`gf`, `gb`, `smoother` and `lerp` come from `otake` (`from otake import gf, gb, smoother, lerp`). Run `python3 shot.py probe` before any render: it prints head widths, positions and registration per frame.

### 4.1 Story beat -> framing and move

| Story beat | Framing | Move | Film 1 shot (reference) |
|---|---|---|---|
| Cold open: the hero's odd act | raking insert on the prop, 1.4-1.8 D, +13 to +23 deg | already moving on frame 0; snap push in the first 0.5 s | 1 (A1) |
| Introduce authority | low, 1.2 D, +13.5 to +16.5 deg, head 180-200 px | slow push or crane with tilt; the snap out on his first word | 6, 10 (a/t16.0, B6) |
| One mocks, one listens | G-type two-shot in depth, eye level, near 1.36-1.46 x far | push 30 easing to 0 %/s as a zoom; the listener frozen | 10, 18 (A11, B10) |
| Shock on a face | from a two-shot, snap push 12-16 frames to 290-330 px | then near still | 3 (B3) |
| A name or label lands | punch-in cut, speed lines 6 frames, 2-frame shake | drift push 5 %/s | 13 (B3) |
| Small, outnumbered or defeated | high, 3.3-4.0 D, -20 to -25 deg | push 12 %/s, or a stepped pull-out | 9a, 11d (a/t58.5, b/t42.0) |
| Show the document or object | crash push x3 in 14-17 frames until it fills the frame | tilt down the text 10 %/s | 14 (B7) |
| Time jump, next morning | tight on a text prop, then crash pull-out 17 frames to the place | drift push 5 %/s | 15 (B7-8) |
| Explain a mechanism | one long take, 4 snaps between named views (rake, corridor, plan, rake), each on the word that names the part | drift 10 %/s between | 19 (B19, A12) |
| Speed, chase | lens rides behind the moving object along its path | launch snap, 5 Hz shake decaying | 20 (A12, A8) |
| Comparison of scale | whip pull-out x0.2 with about 1100 px of pan | drift 6 %/s | 21 (B21) |
| Calm before the disaster | the callback wide at eye level | push 24 %/s easing to 0, 0.2 deg sway, no snap | 23 (A14) |
| Disaster arrives | hard cut close on the faces, 6-frame hold, crash pull-out x0.27 with tilt up from 0.7 D | 5 Hz shake, 86 px | 24 (A13, A15) |
| Impact | the callback two-shot | 8-frame 5 Hz shake, decaying; then the flash | 25 (A15) |
| Ending | pull back to the callback framing of the setup scene | push 20-26 %/s easing to 0; last 12 frames still | 26 (A16, B22) |
| Callback | the same camera name and marks exactly, with the subject in the same place in frame | | G, beach, table |

---

## 5. What the reviews found wrong, and the better choice

| Finding (film 1) | Evidence | Better next time |
|---|---|---|
| The cut is busier than either reference | framing interval 1.06 s (v1) and 1.09 s (v1.1) by the picture tool, against 1.39 (A) and 1.62 (B) | Plan 1.3 to 1.4 s by plan count: about 20 snaps instead of 26 in 65 s, with the same transitions |
| Too little lateral motion | pan median 39 px/s against 40-150 (A 142, B 57) | Give more drifts a sideways truck or pan of 40 to 140 px/s instead of a pure push. Trucking also adds parallax. |
| Card-like shots | flat 2D share: shot 4 3 of 4 pairs, shot 12 2 of 2 | Truck sideways past foreground objects. Do not only push or pull along the axis. |
| Close-ups not close enough | shot 3 "close-up" about 250 px against 300-385 in the reference; hook high two-shot heads 158-248 px against about 120 at a/t58.5 (too tight for a high wide) | Close = 300-350 px head, high wide = 110-135 px |
| Low angles look into a dark ceiling | shot 10; the reference's low angles look up at bright sky | Aim low angles at a window, lamp or sky: a bright area behind the head |
| An empty frame | shot 16: the tilt holds on empty grey sky with half a face at the edge (35.0 s) | Never let a tilt leave the frame without a subject for more than about 6 frames. Time the return so the subject is back by the next word. |
| Callback felt, not seen | shot 23: the man moved from the centre to the left third and the camera sat lower than in shot 16 | Repeat the exact camera and the exact screen position of the subject. Change only the light. |
| Planned close-up became a medium | s18: the zoom-out was x0.52, not x0.30, because G's 173 px head fixed the ratio | Derive crash-zoom ratios from the two head widths before planning: ratio = end head / start head |
| Fly-in reads as a smear | s05: 27 frames, whole-frame radial streak | Keep fly-ins at 15 to 20 frames, or streak only the plate and the first and last few frames |
| Raking macro reads abstract | s09 corridor view at 19.5-20 s (props `corridor_cam`, ceiling in the top third with the wall normal as up) | Use the mech `corridor_cam` with walls in frame, or an up vector that keeps the horizon of the map level |
| Faces in the caption band | s24 runners' heads at y 830-900; s16 head leaves the bottom during the tilt | Check head bottoms against y 880 at the probe stage, not at the conform |
| The reveal is small in frame | s22: the walls-on-the-line reveal; s21 ghost storms illegible | Anything the story needs read must be about 120 px or more |
| The high oblique of the plan could not see the lane | s21: a 30 deg rake from the south-east is hidden by the 0.50 D east wall | Ray-check a new map camera with `M.sight_margin` before planning it; the take used 62 deg, az +16, 1.30 D |
| Constant-speed runs crept in | s21 drift 21 frames (g1543-1563); s12 and s13 drifts 16-17 frames | Never ease with a pure power curve alone over a long drift; mix two curves (as s10 and s23 do) and re-run the runner's `qa` |

Errors in the existing skill text that this chapter corrects:
- `pipeline/v3/stage/API.md` 5 and `camrig.shake` say that 0.45 deg gives "about 12 px standard deviation". Measured: 17 px peak to peak and 2.5 px frame to frame. The reference needs about 86 px. Use recipe 7b.
- `references/look.md` says that `qa_motion.py` "checks each interval against 0.6 to 1.6 s" and lists it as the general tool. The script reads only the hook's `film.py` takes (A and B) and checks no intervals. Takes use their runner's `qa` command. The whole film uses `v3/film/out/grammar.py`.

---

## Sources

Paths are relative to the skill's `pipeline/` folder. `__PROJ__/...` marks files not bundled with the skill.
- `spec/camera_motion.md` (1.1-1.7, 2.1-2.5, 3.1-3.5), `spec/LOOK_SPEC.md` 5.1-5.4 and 8.1, `spec/captions.md`, `spec/environment_materials.md` (eye line)
- `__PROJ__/plan/shot_plan.json` (26 shots, camera, reference, `grammar_numbers`, `grammar_check`, `notes`), `plan/shot_plan.md`
- `v3/stage/API.md`, `v3/stage/camrig.py`; `v3/README.md`; `v3/shots/film.py`, `qa_motion.py`, `post.py`, `qa_parallax.py`; `v3/out/QA.md` (hook)
- `v3/set3d/API.md`, `REVIEW.md`; `v3/set3d_ext/props/API.md`, `office_props.py`; `v3/set3d_ext/mech/API.md`, `office_mech.py`; `v3/set3d_beach/API.md`; `v3/set3d_ext/beach/API.md`, `bshot.py`; `v3/set3d_kitchen/API.md`, `kshot.py`, `kitchen_geom.py`
- `v3/film/CONVENTIONS.md`; `v3/film/s10/otake.py`, `s10/shot.py`, `s10/QA.md`; `v3/film/s20/mc.py`; `v3/film/s11`, `s13`, `s14`, `s17`, `s19`, `s20`, `s24`, `s26` (`QA.md`, `shot.py`); `__PROJ__/v3/film/s04`-`s09`, `s12`, `s15`, `s16`, `s18`, `s21`-`s23`, `s25` (`QA.md`, `shot.py`, `raw/meta`, `work/probe.json`)
- `v3/film/out/CONFORM.md`, `v3/film/out/grammar.py`
- `__PROJ__/deliver/QA_film.md`, `__PROJ__/deliver/QA_film_v1_1.md`
- `references/look.md`, `references/next-film.md`, `references/polish.md`
- Pictures: `__PROJ__/v3/film/out_v11/graded/g_%04d.png` (film frames of version 1.1 without the blur, the picture of `__PROJ__/deliver/film_v1_1_sharp_thai.mp4`), with the labels from the takes' render meta (`raw/meta`, `work/raw/meta`, `v3/out/depth/meta`) and probes.
- Per-shot heights, pitches, lenses and start and end poses in section 3 were computed by evaluating each take's `cam(g)` / `cam_setup(g)` for every frame. Where a take was edited after its render, the render meta wins (`references/polish.md` item 6). Checked frames agree.
