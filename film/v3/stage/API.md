# v3/stage: puppets on cards in a true-3D Blender scene

Directory: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/stage/`
bpy 5.3.0 as a Python module, Cycles on CPU, headless. No Freestyle, no EEVEE. v2 is imported read-only (`v2/puppet/puppet.py`).

| File | What it is |
|---|---|
| `sprites.py` + `sprite_page.js` | puppet pose -> transparent RGBA PNG through one persistent Chromium page. No bpy. |
| `actors.py` | `Actor`: card, shadow proxy, contact decal; placement; pose + pinned hands; `world_to_local` and its inverses |
| `camrig.py` | the 22 mm camera, keyed poses, `drift` / `snap` / `whip*` / `shake`, `cam_for` |
| `render.py` | `setup`, `render_frames`, `world_to_screen` |
| `stubroom.py` | the small test room (floor planks, grid wall at y = 0, a box, one hard sun). Not the office. |
| `tests/` | `example.py` (section 8), `test_stills.py`, `test_move.py`, `test_edge.py`, `timing.py`, `stage_common.py` |
| `test_low.png`, `test_eye.png`, `test_high.png`, `test_stills_vs_ref.jpg`, `test_move.jpg`, `test_*.json` | test results (section 9) |
| `REVIEW.md`, `review/` | independent review: nine checks with their own scripts (`review/c*.py`, `review/run_all.sh`), results before and after the repairs |

Import one of two ways, never both in one process (each style has its own module objects):

    sys.path.insert(0, ".../v3/stage");  import actors, camrig, render, sprites, stubroom
    sys.path.insert(0, ".../v3");        from stage import actors, camrig, render, sprites, stubroom

## 1. Conventions

- 1 Blender unit = 1 D = outer head diameter. Z up, floor z = 0, map wall = plane y = 0, room toward negative y, x = 0 = centre of the wall map, +x to the right when facing the wall.
- Camera: 22 mm, sensor 36 mm, fit AUTO, 720x1280: focal length 782.2 px; size 1 D at planar depth z covers 782.2 / z px. 30 fps. View transform Standard.
- Frame numbers are Blender frame numbers and must be 1 or more (v2's output frame g is 0-based: use g + 1). Sprite file of frame f: `<sprite_dir>/<actor name>_%04d.png`.
- Screen pixels: x from the left edge, y from the TOP edge, continuous (centre of the top-left pixel = (0.5, 0.5)), always in 720x1280 units whatever the render scale.
- Puppet-local coordinates (unchanged from v2): head centre (0, 0), x right, y DOWN, D units. Card coordinates = puppet-local minus the feet point. All anchors and hand targets handled by this package are coordinates of the FINISHED drawing (after squash, mirror and the upper-body stretch of section 3.3).

## 2. Order of work for a shot

1. `render.setup(scene, ...)`, build the set, `cam = camrig.make_camera(scene)`.
2. `Actor(name, cast).build(canvas, sprite_dir)` for each actor.
3. Key the camera (`cam_for` + `key_pose` / `drift` / `snap` ...) and the actors' floor positions (`actor.place`).
4. For every frame to render: `actor.pose(frame, pose, hands=..., camera=cam)`. This needs steps 3 finished, because a pinned hand and the round-head stretch depend on the camera and the placement of that frame.
5. `actor.render_sprites(px_per_D)`.
6. `render.render_frames(frames, out_dir)`.

If the camera or a placement changes afterwards, repeat 4 to 6 (unchanged drawings come from the sprite cache).

## 3. sprites.py

```python
sprites.DEFAULT_CANVAS = {"hero": (-1.8125, -4.3125, 1.8125, 0.125),      # 3.625 x 4.4375 D, 928 x 1136 px at 256 px per D
                          "boss": (-1.9375, -4.7500, 1.9375, 0.125)}      # 3.875 x 4.8750 D, 992 x 1248 px at 256 px per D
sprites.GRID = 1 / 16
sprites.render_sprites(jobs, mode="canvas", cache_dir=None, verbose=False) -> [result, ...]
sprites.sprite_svg(cast, pose, px_per_D, canvas=None, overlay="", underlay="", upper_k=1.0) -> (svg_text, result_without_file_fields)
sprites.solve_hands(cast, pose, hands, upper_k=1.0) -> (pose2, info)
sprites.feet_of(cast, pose=None) -> (x, feet_y)          # feet point in puppet-local D; does not depend on the arms
sprites.hip_y(cast, pose=None) -> y                      # hip line in puppet-local D
sprites.bbox_card(cast, pose=None) -> (x0, y0, x1, y1)   # drawing bbox relative to the feet, y down
sprites.canvas_for(cast, poses=(), margin=0.08, base="default") -> canvas
sprites.canvas_px(canvas, px_per_D) -> (w, h, exact_canvas)
sprites.local_to_px(local_xy, feet, canvas, px_per_D) -> (px, py)
sprites.warp_y(y, y_hip, k), sprites.unwarp_y(y, y_hip, k)
sprites.close()                                          # closes the Chromium page (also done at exit)
sprites.puppet                                           # the v2 puppet module
```

### 3.1 Canvas
A canvas is `(x0, y0, x1, y1)` in D, RELATIVE TO THE FEET POINT (`anchors["feet"][0]`, `feet_y`), x right, y down. It is fixed for an actor, so the card mesh never changes and the soles are always the same pixel: a crouch or a squash moves the head inside the sprite, never the feet. The defaults hold raised and sideways arms with pencil or eraser, hats, steam, sweat, tears, the Z of `asleep`, squash 0.8 to 1.15, crouch, wide legs, and an upper-body stretch up to about 1.25. They do not hold a pointer held sideways (2.4 D) or `legs="lean"` past 20 degrees: use `canvas_for(cast, poses)`; `base=None` gives a tight canvas for close-ups (smaller, faster, sharper). Canvases are snapped to 1/16 D; use `px_per_D` in multiples of 16 so the pixel size is exact. `result["clipped"]` is True when a drawing leaves its canvas.

### 3.2 Jobs and results
```python
job = {"cast": "hero" | "boss", "pose": {...v2 pose...}, "px_per_D": 256, "out": "/abs/hero_0001.png",
       "canvas": (x0, y0, x1, y1),        # optional, default DEFAULT_CANVAS[cast]
       "upper_k": 1.0,                    # optional, section 3.3
       "overlay": "<svg fragment>", "underlay": "<svg fragment>"}      # optional, puppet-local D units
result = {"out", "size": (w, h), "canvas": exact rectangle of the PNG relative to the feet, "px_per_D",
          "origin_px": pixel of the feet point, "feet": (x, feet_y), "feet_y",
          "anchors": {name: (x, y)},      # puppet-local D: hand_r, hand_l, prop_tip_r, prop_tip_l, foot_r, foot_l, feet, head,
                                          # head_top, hat_top, shoulder_*, elbow_*, knee_*, hip, chest, mouth, eye_*
          "bbox", "clipped", "upper_k", "hip_y", "hash", "cached", "ms"}
```
PNG: straight alpha, sRGB. `px_per_D`: 1.3 to 2 times the largest on-screen head of the shot (256 for wide and medium shots, 384 to 512 for close-ups with a tight canvas). Identical drawings are rasterised once (sha1 of the SVG): the PNG is `<dir of out>/_cache/<hash>.png` and every `out` is a hard link to it. `mode="canvas"` (default, 31 ms per 928x1136 sprite) draws the SVG into a 2D canvas; `mode="screenshot"` (119 ms) is the v2 capture path. Both use the same rasteriser and differ only in a few edge pixels.

### 3.3 Upper-body stretch `upper_k`
The card is vertical (section 4.2), so a camera that looks up or down at it foreshortens the drawing vertically and the head would become an ellipse. A real 3D figure keeps a round head and a full torso; only its legs change. So the drawing above the hip line is drawn taller by `upper_k`, scaled about the hip line, legs untouched (two clipped copies of the figure in one SVG; the seam is one antialiased row). `Actor.pose()` computes the factor for the camera of the frame (1.00 at eye level, 1.02 to 1.09 at the low angle, 1.07 to 1.15 at the high angle) and gives the same factor to `solve_hands`, so pinned tips stay exact. Anchors come back already stretched.

### 3.4 `solve_hands`
```python
hands = {"r": {"tip": (lx, ly), "prop": "pencil", "angle": -55, "stretch": 1.1},    # tip of a held prop (or of the bare hand if prop is None)
         "l": {"hand": (lx, ly)}}                                                    # the hand itself
pose2, info = sprites.solve_hands("hero", pose, hands, upper_k=k)
info["r"] == {"target": (lx, ly), "reached": (x, y), "error": D, "anchor": "prop_tip_r"}
```
Targets are puppet-local points of the finished drawing (what `actors.world_to_local` returns). `"r"` / `"l"` are the pose keys `arm_r` / `arm_l`, the limbs of the UNMIRRORED figure; with `pose["mirror"]` the checked anchor has the other letter (`info[side]["anchor"]`). `angle` is the prop angle as it must look on screen (SVG degrees, 0 right, -90 up). Extra keys (`stretch`, `bend`, `sharp`, `layer`, `preset`) go to the arm. `error` above 0.01 means the arm cannot reach: an arm is 0.74 D (times `stretch`), a pencil adds 0.36 D.

## 4. actors.py

```python
actors.Actor(name, cast, tilt=0.0, max_slant=50.0)
actor.build(canvas, sprite_dir, scene=None, shadow="proxy", contact=None, interpolation="Cubic", pattern=None, alpha_gamma=1.0) -> card object
actor.place(frame, floor_xyz, scale=1.0, flip=False, interp="LINEAR", easing="AUTO") -> actor
actor.pose(frame, pose, hands=None, camera=None, upper_k=None) -> (solved_pose, info)
actor.render_sprites(px_per_D, frames=None, overlay=None, mode="canvas", verbose=False) -> [sprite results]
actor.jobs(px_per_D, frames=None, overlay=None) -> [sprite jobs]
actor.sync(camera=None, scene=None)            # orient for the scene's current frame (render_frames does it)
actor.bake_facing(frames, camera=None, scene=None)      # key everything sync() sets, per frame, for other render loops
actor.set_hidden(hidden=True); actor.objects() -> [card, proxy, contact]
actor.sprite_path(frame); actor.reload_sprites(); actor.flip_at(frame); actor.feet_at(frame); actor.basis(camera) -> (X, Y, Z)
# reload_sprites(): empty Blender's and Cycles' sprite caches (automatic in render_sprites and sync, see 4.1)
# attributes: actor.root, .card, .proxy, .contact, .material, .canvas, .poses, .upper_k, .feet,
#             .tilt, .max_slant, .yaw_fixed, .round_head, .shadow_max_angle, .shadow_light, .shadow_twist, .depth_bias

actors.world_to_local(actor, camera, world_point, frame=None, feet=None) -> (lx, ly)
actors.local_to_world(actor, local_xy, frame=None, feet=None, camera=None) -> Vector
actors.local_to_screen(actor, camera, local_xy, frame=None, feet=None) -> (x_px, y_px_from_top, depth)
actors.upper_stretch(actor, camera, frame=None, pose=None, limit=1.6) -> k
actors.card_state(actor, camera, frame=None) -> (origin, X, Y, Z, scale)
actors.sync_all(scene=None, camera=None); actors.clear_registry(); actors.REGISTRY
actors.card_material(name, image=None, interpolation="Cubic", alpha_gamma=1.0) -> (material, image texture node)
actors.contact_material(name, color="#252432", opacity=0.5) -> material
```

### 4.1 What `build` makes
One empty at the feet, `<name>_root`, carries the keyed position and scale (never a rotation). Its children:

- `<name>_card`: a quad exactly the size of the canvas, origin at the feet point. Material: Image Texture (PNG sequence, straight alpha, Cubic or Linear, extension CLIP) -> Emission strength 1, mixed with Transparent by the alpha. No BSDF, `emission_sampling = 'NONE'`, `visible_diffuse = False`: the scene cannot light, tint or shadow it and it lights nothing. Measured on screen: head fill `#fef7f6`, ink `#3a2832`, exact, at all three test angles (with the bloom compositor on: `#fff8f7`).
- `<name>_shadow` (`shadow="proxy"`, default): the same sprite on a second card that only shadow rays see (`visible_camera`, `visible_diffuse`, `visible_glossy`, `visible_transmission`, `visible_volume_scatter` False). The visible card then has `visible_shadow = False`. The proxy is a grid with a twist modifier (`feet_twist`) and has two zones:
  - above `actor.shadow_twist[1]` (default 0.9 x the standing hip height: hero 1.02 D, boss 1.34 D above the feet) it stands vertically and is turned about Z from the stage-front orientation (normal toward -y) toward the key light until the light's horizontal direction is at most `actor.shadow_max_angle` (40 degrees) off its normal. Result: a full-figure hard shadow for any light azimuth, and a body shadow that does not depend on the camera.
  - below `actor.shadow_twist[0]` (0.12 D: ankles and feet) it lies exactly in the visible card, so the shadow starts AT the drawn feet for every camera yaw; over the legs it twists linearly from one orientation to the other. (Review repair. Before it, the proxy was one rigid quad turned about the feet centre and the shadow's feet stood 3 to 18 px away from the drawn feet, 59 px in a reverse shot; now 0.0 px in every tested case.) The leg shadows therefore follow the feet when the camera yaws; the body shadow does not.
  - `actor.shadow_twist = None` gives the rigid proxy back. If the camera looks from the far side (away from the map wall, a reverse shot) the stage-back orientation is used, so the shadow is never the mirror image of the figure the camera sees.
  - The light is the first visible SUN of the scene; with no sun, the strongest other visible light that casts shadows; or `actor.shadow_light` (a point lamp is followed per frame).
  - `shadow="card"`: the visible card casts the shadow itself (it turns with the camera and vanishes when the light is edge-on to it: measured shadow area 0.00 of the normal one, against 0.83 to 0.96 with the proxy). `shadow=None`: no cast shadow.
- `<name>_contact` (`contact=True` or `dict(width=0.9, depth=0.42, color="#252432", opacity=0.5)`): a soft ellipse lying 0.004 D above the floor, a Transparent BSDF whose colour falls from the shadow colour to white, so it multiplies whatever floor is under it. Default off.

The sprite files may be written after `build`; the image is attached at the first `sync`. `sync` raises `FileNotFoundError` when a visible actor has no sprite for the current frame.

Stale sprites (review repair). Two caches hold a sprite once it has been rendered: Blender's decoded frames of the image sequence, and Cycles' persistent render data, which keys a texture by its FILE PATH and does not read the file again when the same frame is rendered a second time. Neither `Image.reload()` nor an update tag nor a new image datablock empties the second one (measured: render frame f, re-pose f, `render_sprites`, render f again showed the OLD drawing in the first version of this package). So:

- Persistent data is now off by default (section 6), which removes the second cache altogether; the guard below is for `setup(persistent=True)`.
- `Actor.render_sprites()` and `Actor.sync()` compare the PNGs of the frames this actor has already shown (inode, time, size) with the files on disk. When one has changed they call `Actor.reload_sprites()`, which reloads the image and, if persistent data is on, switches it off and on once. The next rendered frame then rebuilds the set's BVH and textures (one-off cost, as on the first frame of a process). New frames cost nothing: writing sprites frame by frame while rendering never triggers it.
- This also covers sprites written through `sprites.render_sprites(actor.jobs(...))` or by another process.
- If you render without `sync()` (Blender's own animation loop) after rewriting files by hand, call `actor.reload_sprites()` yourself.

`bake_facing(frames)` keys, CONSTANT per frame, everything `sync()` sets: card rotation and depth offset, proxy rotation, offset and twist angle, decal rotation. Once an actor is baked, every later `sync()` rewrites the keys of the frame it sets, so `render_frames` and Blender's own loop always agree (checked: 12 moving frames, largest pixel difference 0).

### 4.2 Card orientation: vertical, yaw only (tested against a/t16.0 and a/t58.5)
The card's width axis is the camera's horizontal right axis; the card stays upright. Numbers for the boss with a 190 px head:

| Camera | Card | Head W/H on screen | Figure height in head widths, against the flat puppet | Notes |
|---|---|---|---|---|
| a/t16.0: 1.16 D above the floor, pitched up 15 deg | vertical | 1.081 | x1.093 | legs nearer the lens and longer |
| | fully facing | 1.000 | x1.000 | no stretch; card leans 15 deg toward the lens, the head grows to 232 px |
| | vertical + `upper_k` 1.091 (chosen) | 0.999 | x1.146 | reference: 3.41 / 3.05 = x1.118 |
| high: 2.75 D above the head, pitched down 15 deg | vertical | 1.167 | x0.749 | head visibly flattened |
| | fully facing | 1.000 | x1.000 | leans back 15 deg: the head is 0.75 D behind the feet and cuts into a wall the actor stands at |
| | vertical + `upper_k` 1.153 (chosen) | 0.998 | x0.817 | round head, body foreshortened as a 3D figure's |

Reasons for the vertical card: it reproduces the low-angle leg stretch of a/t16.0; the soles lie on the floor line for every camera (measured gap between the lowest ink pixel and the projected sole line: 0.0 to +1.3 px over three angles and two actors; the review's matte measurement gives -1.2 to 0.0 px); it never leans into the wall behind an actor, which matters here because the hero works at the wall map; furniture occludes it at the right depth. Its one defect, the flattened head, is removed by `upper_k`. `actor.tilt` (0 = vertical, 1 = parallel to the image plane) and `actor.max_slant` (degrees; a view axis steeper than this leans the card by the excess, default 50) remain available. `actor.yaw_fixed = 0.0` keeps a card parallel to the map wall whatever the camera does. `actor.round_head = False` or `pose(..., upper_k=1.0)` switches the stretch off.

### 4.3 `place`
Keys the feet point and a uniform scale on the root (LINEAR by default; `interp` / `easing` as in `camrig.key`). `flip=True` mirrors the figure from that frame on. It is realised by the puppet's own mirror (`pose["mirror"]`, which keeps the head disc and its crescent unmirrored) inside `actor.pose()`; the card is never mirrored. If you build sprite jobs by hand, set `pose["mirror"]` yourself.

### 4.4 `pose` and pinned hands
```python
pose, info = hero.pose(f, {...}, hands={"r": {"tip": (wx, wy, wz), "prop": "pencil", "angle": -55}}, camera=cam)
```
A 3-tuple target is a WORLD point; it is converted with `world_to_local` for the camera and placement of frame `f`, then solved with `sprites.solve_hands`. A 2-tuple is taken as puppet-local. For a world target `info[side]` also carries `"world"` (the point on the card that covers the target) and `"clearance"` (D along the line of sight by which the card is in front of the target there). A negative clearance means the card stands BEHIND the target at that spot, so the wall the target lies on hides the hand or the tip; `pose` then issues a warning (review addition; see trap 3). The pose is stored (`actor.poses[f]`, `actor.upper_k[f]`, `actor.feet[f]`) and `render_sprites` rasterises every stored frame. `info[side]["reached"]` is the tip in puppet-local D; `local_to_screen(actor, cam, info[side]["reached"], f)` is where it lands on screen.

### 4.5 Registration
`world_to_local(actor, camera, world_point, frame)` cuts the ray from the lens through the world point with the card plane of that frame and returns the puppet-local point there. A tip drawn on that point covers the world point exactly, even though the card stands in front of the wall the point lies on. It sets the scene to `frame`. `local_to_world` and `local_to_screen` are the inverses. Measured (tip marker against wall marker, both found in rendered 720x1280 frames): 0.14 to 0.51 px in the three stills, at most 0.48 px (mean 0.22 px) over the 30-frame move, 0.12 px for a mirrored actor at scale 1.4.

## 5. camrig.py

```python
camrig.LENS = 22.0; camrig.SENSOR = 36.0; camrig.FOCAL_PX = 782.22; camrig.RES_X, camrig.RES_Y = 720, 1280; camrig.FPS = 30
camrig.make_camera(scene=None, name="StageCam", lens=22.0) -> camera object          # becomes scene.camera
camrig.key_camera(frame, loc, look_at=None, rotation=None, lens=None, roll=0.0, cam=None, interp="SINE", easing="EASE_IN_OUT")
camrig.key_pose(frame, pose, cam=None, interp="SINE", easing="EASE_IN_OUT")
camrig.cam_for(subject_point, head_px, height_class="eye", yaw_deg=0.0, D=1.0, floor_z=0.0, screen_x=360.0,
               pitch_deg=None, cam_height=None, lens=22.0, screen_y=None) -> pose
camrig.dolly(pose, right=0.0, up=0.0, forward=0.0, pan_deg=0.0, tilt_deg=0.0) -> pose
camrig.drift(f0, f1, pose0, pose1, ease="sine", cam=None)
camrig.snap(f0, f1, pose0, pose1, peak=1.7, pivot=None, cam=None)
camrig.whip(f0, f1, pose0, pose1, cam=None)
camrig.whip_off(f0, f1, pose, pan_deg, cam=None); camrig.whip_on(f0, f1, pose, pan_deg, cam=None)
camrig.shake(f0, f1, amp_deg=0.45, every=3, seed=1, cam=None)
camrig.key(idblock, path, frame, value, interp="SINE", easing="EASE_IN_OUT"); camrig.fcurves_of(idblock); camrig.clear_keys(idblock)
camrig.look_rotation(loc, look_at, roll=0.0) -> Euler; camrig.basis_rotation(yaw_deg, pitch_deg, roll=0.0) -> Euler
camrig.ease_peak(u, peak=1.7); camrig.ease_sine(u); camrig.ease_quintic(u); camrig.ease_septic(u); camrig.focal_px(lens=22.0)
```

A pose is `{"loc": (x, y, z), "rot": Euler}` or `{"loc": ..., "look_at": (x, y, z), "roll": deg}`, optional `"lens"`. `cam=None` means `scene.camera`. Every key goes through `camrig.key`, the per-keyframe-point helper of `spec/camera_motion.md` 3.3; the interpolation of a key shapes the segment that starts there. Successive rotation keys are kept on one Euler branch.

- `key_camera`: the third argument is `look_at` (world point, level horizon, plus `roll` degrees); give a rotation as `rotation=` (Euler XYZ in radians) or pass a mathutils `Euler` / `Quaternion` in third place. `lens` keys the focal length; leave None to stay at 22 mm. If a shot keys the lens at all, give `lens` on every key of that shot (a single lens key holds for the whole shot).
- `cam_for`: planar depth = 782.2 x D / head_px. `yaw_deg`: direction the camera looks, clockwise from +y seen from above (0 = square on to the map wall, +20 = camera stands to the left and looks toward +x). `screen_x`: column of the head centre. Classes: `"low"` camera 1.2 D above `floor_z`, pitched up 13.5 deg; `"eye"` 0.3 D above the head centre, 3 deg down; `"high"` 2 to 3.5 D above the head (0.417 x depth, which puts the head near 0.60 H at the reference distances), 15 deg down; `"top"` straight down. `pitch_deg`, `cam_height` (world z) override; `screen_y` solves the pitch so the head lands on that row. Returns `loc`, `rot`, `lens`, `look_at`, `depth`, `subject_px`, `pitch_deg`, `yaw_deg`, `height_class`. For a 190 px head at z = 2.5: low puts it at y = 574, eye at 656, high at 824, so pass `screen_y` for a high angle on a near subject (heads belong between y = 300 and 760).
- `drift`: two keys. `"sine"` = SINE in-out (rest at both ends), `"cubic_out"` = moving on f0 and settling at f1 (shot that starts on a cut), `"quad_out"`, `"linear"`. The camera holds after f1. After a snap use `"sine"`: the snap ends at rest.
- `snap`: one key per frame (LINEAR between them), ease in-out between sine and quintic whose peak speed is `peak` times the mean (1.571 = sine, 1.875 = quintic, up to 2.19). Measured on the test move: 1.69. With `pivot` (the subject's world point) the distance to it changes geometrically and the camera swings around it; without, the position moves on a straight line. Rotation is slerped, lens geometric.
- `whip`: sine in-out between two poses. `whip_off`: pan away by `pan_deg` (positive = right), accelerating; cut on f1 + 1. `whip_on`: start `pan_deg` short of the pose and brake into it. The streak blur is added outside Blender.
- `shake`: random pan and tilt keys every `every` frames on top of the existing move.
- `dolly`: a pose moved along its own right axis, world up and its horizontal forward axis, then panned and tilted.

## 6. render.py

```python
render.QUALITY = {"draft": dict(samples=4, filter_width=1.5), "final": dict(samples=8, filter_width=1.5)}
render.setup(scene=None, quality="final", bloom=None, samples=None, threads=None, filter_width=None, persistent=False) -> scene
render.render_frames(frames, out_dir, scale=1.0, threads=None, scene=None, camera=None, prefix="f_", sync=True,
                     on_frame=None, verbose=True, check=True) -> [{"frame", "path", "wall", "cpu"}, ...]
render.cards_wrong(path, scene=None, camera=None, skip=()) -> [actor names]     # review addition, see below
render.world_to_screen(camera, point, frame=None, scene=None) -> (x_px, y_px_from_top, depth)
render.drop_cache(scene=None)                  # free Cycles' persistent data (review addition, see below)
```

`setup`: Cycles CPU, fixed sample count, no adaptive sampling, no denoiser, fixed seed (penumbra noise does not boil), `max_bounces` 1, `diffuse_bounces` 0, `glossy_bounces` 1, `transparent_max_bounces` 12, Blackman-Harris 1.5 px, persistent data OFF (review change, `persistent=True` switches it on), Standard / None / exposure 0, PNG RGB 8 bit, 720x1280, 30 fps, Freestyle off, a black world if the scene has none. `bloom=None` leaves the scene's compositor alone (the set or the integrator may own a grade); `bloom=True` or `dict(threshold=1.0, size=0.05, strength=0.5, tint=(1, 0.92, 0.8, 1))` attaches a Glare Bloom on scene-linear values above 1.0 only; `bloom=False` switches compositing off. Measured with bloom on: a strength-8 bulb gets a halo that falls to a tenth about 18 px outside its core, the head fill moves one level (`#fff8f7`), the frame costs about 0.5 s more. A colour grade added by anyone else will move the puppet colours; none is applied here.

Persistent data (review change). The first version switched `use_persistent_data` on. Measured, it saves nothing in this pipeline: 5.52 against 5.53 s per final frame in the stub room, 6.06 against 6.08 s with four 2048 px textures and 13000 extra triangles added. And it is the cause of the stale-sprite defect (4.1) and of the same defect for set textures. It is now off unless `setup(persistent=True)`. With it off, every frame reads its textures from disk and nothing below about `drop_cache` applies.

`drop_cache` (review addition): with persistent data Cycles keys a file texture by its PATH and keeps its pixels; overwriting the file and calling `image.reload()` does not change what is rendered (measured on a wall texture overwritten in place: the old picture was rendered again; after `drop_cache` the new one). The actors handle their sprites themselves. For a SET texture that changes during a shot (the wall map with the track being drawn and rubbed out) write every version to its own file (an image sequence, or one path per version), or overwrite + `image.reload()` + `render.drop_cache(scene)`, which costs one rebuild of the BVH and textures on the next frame.

`check` / `cards_wrong` (review addition): after each frame `render_frames` reads the PNG back and looks at nine points inside every visible actor's head. If all of them are black (the whole card rendered as a black rectangle; this happened on 2 consecutive frames out of roughly 5000 renders during the review, with persistent data on, was never reproduced in 21 repeats of the same script, and its cause was not found) or magenta (Cycles' colour for a texture it could not read), the sprite and render caches are emptied and the frame is rendered once more. The frame's entry then has `"retried": [names]`, and `"still_wrong": [names]` if the second render is the same (something dark really is in front of that head; that actor is not retried again in the call). Costs one PNG decode per frame (about 25 ms). Not done for border renders or with `check=False`.

`render_frames`: for each frame `scene.frame_set`, `on_frame(frame)` if given, orient every actor, render, write `<out_dir>/f_0001.png`. `scale=0.5` renders 360x640. `threads=n` sets FIXED n threads; None keeps the scene setting (automatic after `setup`). `cpu` is user + system seconds of the whole process for that frame.

## 7. stubroom.py (tests only)

```python
room = stubroom.build(scene=None, tex_dir=None, elev=38.0, az=-55.0, sun_angle=1.5, A=stubroom.A_TEST, K=stubroom.K_TEST)
# -> {"sun", "floor", "wall", "box", "side", "materials", "mark"};  room["mark"](point, name="mark", color="#18c8d8", size=0.05)
stubroom.lit_material(name, albedo_hex="#808080", A=A_TEST, image=None); stubroom.emission_material(name, hex_color, strength=1.0)
```
Lit material = Diffuse (roughness 0) + Emission(albedo x A), `emission_sampling 'NONE'`; sun energy = pi x max(K). `az` is the azimuth of the light's travel direction (0 = travelling +y, -90 = travelling +x). The test values are harder than `INTERIOR_DAY` (floor in shadow 0.33 of sunlit) so that shadows read in the test images; `A_DAY`, `K_DAY` hold the spec's interior preset.

## 8. Worked example (runnable: `python3 tests/example.py`)

```python
import os, sys
STAGE = "/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/stage"
sys.path.insert(0, STAGE)
import bpy
import actors, camrig, render, sprites, stubroom
OUT = os.path.join(STAGE, "..", "tmp", "stage", "example")

# 1. scene, set, camera
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
render.setup(scene, "draft", threads=2)                 # "final" = 8 samples
room = stubroom.build(scene)                            # replace with the real set
cam = camrig.make_camera(scene)

# 2. two actors
hero = actors.Actor("hero", "hero")
boss = actors.Actor("boss", "boss")
hero.build(sprites.DEFAULT_CANVAS["hero"], os.path.join(OUT, "sprites"), contact=True)
boss.build(sprites.DEFAULT_CANVAS["boss"], os.path.join(OUT, "sprites"), contact=True)
hero.place(1, (-0.70, -0.55, 0.0))                      # at the wall
boss.place(1, (1.25, -2.55, 0.0))                       # 2 D nearer the camera
boss.place(5, (1.15, -2.55, 0.0))

# 3. camera move: push in on the hero and truck 0.2 D to the right
head = (-0.70, -0.55, sprites.feet_of("hero")[1])       # head centre = feet_y above the floor
a = camrig.cam_for(head, head_px=150, height_class="eye", yaw_deg=6.0, screen_x=300)
b = camrig.dolly(camrig.cam_for(head, head_px=175, height_class="eye", yaw_deg=6.0, screen_x=300), right=0.2)
camrig.snap(1, 5, a, b, peak=1.7, pivot=head)           # a real snap lasts 14 to 24 frames

# 4. poses; the pencil point is pinned to a world point on the wall
TARGET = (0.32, 0.0, 2.45)
room["mark"](TARGET)
for f in range(1, 6):
    pose, info = hero.pose(f, dict(yaw=0.55, expr="determined", arm_l="hip", blink=2 if f == 3 else 0,
                                   arm_r=dict(preset="reach_up", stretch=1.1)),
                           hands={"r": {"tip": TARGET, "prop": "pencil", "angle": -38}}, camera=cam)
    assert info["r"]["error"] < 0.01
    boss.pose(f, dict(yaw=-0.5, expr="smug", arm_r="hip"), camera=cam)
    print(actors.local_to_screen(hero, cam, info["r"]["reached"], f)[:2], render.world_to_screen(cam, TARGET, f)[:2])   # equal

# 5. sprites, then five frames
hero.render_sprites(256)
boss.render_sprites(256)
render.render_frames(range(1, 6), os.path.join(OUT, "frames"), scale=0.5, threads=2)
```

## 9. Tests and measured results (stub room)

The stills, the edge paths and the move below were run again after the review repairs (twisted shadow proxy, persistent data off, sprite cache guard, post-render card check); the numbers are those of the re-run and differ from the first run only in the shadow rows. The independent review, with its own scripts and a before / after table for nine checks, is in `REVIEW.md`: registration 0.45 px worst over 300 moving frames at five world points, the stale-sprite cases, shadow attachment (0.0 px), colours under five lightings, scale, easing, the card orientation comparison and the cost.

Run from this directory: `python3 tests/test_stills.py`, `python3 tests/test_move.py`, `python3 tests/test_edge.py`, `python3 tests/timing.py 4`. Working files go to `v3/tmp/stage/`.

**Three stills** (`test_low.png`, `test_eye.png`, `test_high.png`; beside a/t16.0, a/t20.0, a/t58.5 in `test_stills_vs_ref.jpg`; numbers in `test_stills.json`). Hero at the wall with the pencil on a marked world point, boss 2 D nearer the camera, final quality.

| | low | eye | high |
|---|---|---|---|
| Registration, rendered tip against rendered wall mark | 0.51 px | 0.14 px | 0.32 px |
| Head fill / ink on screen, hero and boss | `#fef7f6` / `#3a2832` | same | same |
| Lowest ink pixel against the projected sole line | +0.1 to +1.3 px | 0.0 to +0.6 px | +0.3 to +0.5 px |
| Near head / far head | 174 / 128 px = 1.36 | 181 / 128 = 1.42 | 153 / 112 = 1.36 |
| `upper_k` hero, boss | 1.022, 1.069 | 1.001, 1.000 | 1.078, 1.095 |

**30-frame move** (`test_move.jpg`, `test_move.json`): 4 frames drift, 18-frame snap push from a 135 px to a 200 px head with a 0.5 D sideways dolly, 7 frames settling; hero raises an arm, leans, blinks twice with the pencil pinned.

| Check | Result |
|---|---|
| Pinned tip against the wall mark, every frame | max 0.48 px, mean 0.22 px |
| Sprite shown on frame f is the sprite of frame f (colour-coded patch read from the render) | 30 of 30 (each frame rendered once; for a frame rendered again after its sprite changed see `REVIEW.md` check 3) |
| Shadow on a fixed wall point, with actors / without | 0.716 to 0.719 on all 30 frames; lit control point 0.998 to 1.004 (re-run after the review repairs; 0.714 to 0.718 before them) |
| Popping (a frame change over 1.8 times both neighbours) | none |
| Snap, peak speed over mean | 1.69 |

**Edge paths** (`test_edge.json`): mirrored actor at scale 1.4 with a pinned eraser 0.12 px; a sprite sequence starting on frame 12; `shadow="card"`; `yaw_fixed`; top-down and 55 degree views; bloom; whips; `bake_facing` equals `sync`.

**Not covered by these three tests, covered by `review/`:** the same frame rendered again after its sprite changed (`review/c3_sequence.py`: the first version showed the old drawing), the distance between the drawn feet and the shadow's feet (`review/c5_shadow.py`), a reverse shot, deep shade and strong light on the card (`review/c4_colour.py`).

**Timing** (`test_timing.json`; two actors, stub room).

| Step | Time |
|---|---|
| Sprite, 928x1136 or 992x1248 px (256 px per D), `canvas` mode | 31 ms each |
| Sprite at 384 px per D | 46 ms |
| Sprite, `screenshot` mode, 256 / 384 px per D | 119 / 148 ms |
| Pose, pin and stretch solve, two actors | 4 to 7 ms per frame |
| Blender draft, 360x640, 4 samples, 4 threads | 0.42 s wall, 1.6 s CPU |
| Blender final, 720x1280, 8 samples, 4 threads | 2.97 s wall, 11.4 s CPU |
| Same final frame, 2 threads, while another agent's render was running | 5.6 to 6.5 s wall, 10.9 to 11.4 s CPU |

Review timing after the repairs (`review/c9_cost.py`, same scene type, 6-frame move, median of frames 2 to 6, no other job running): draft 0.42 s wall at 4 threads (1.53 s CPU), 0.77 s at 2 threads; final 2.85 s wall at 4 threads, 5.59 s at 2 threads, 10.9 to 11.0 s CPU. Against the first version timed the same way (2.59 s, 5.12 s, 10.05 s CPU) the repairs cost about 0.2 s wall per final frame at 4 threads; in an alternating A/B run (`review/c9c_repair_cost.py`) the twisted shadow proxy accounts for 0.11 s of that and the card check for 0.03 s.

The builder's 4-thread measurement was taken once. Another agent's job (`v3/tmp/set3d/prof.py`, 383 percent CPU) was running when the script started and was no longer listed when the final pass began; the 1-minute load was 3.1 at that moment, so the machine was not idle. Cost is linear in samples (about 1.1 to 1.4 CPU-seconds per sample per 720x1280 frame); the two actors account for about a fifth of it and the sun's shadow rays for about 30 percent. An 8-sample frame differs from a 64-sample frame by 1.2 levels RMS.

## 10. Traps and limits

0. The shadow of a foot whose card is exactly edge-on to the key light (light running along the feet line) is a hairline for the first 0.12 D and appears from the shin upward. That is the price of a shadow that starts at the drawn feet; it needs a light within a few degrees of the image plane's horizontal axis.
1. Two cards in one plane hide each other in Cycles (speckled holes). Every actor therefore sits 0.0025 D deeper than the previous one (`actor.depth_bias`), which the registration takes into account. Do not reset it.
2. An emissive set object that diffuse rays can reach by chance speckles the surfaces around it, even with `emission_sampling 'NONE'`. Give bulbs `visible_diffuse = False` (the cards have it) or multiply their strength by Light Path > Is Camera Ray.
3. The card of an actor close to a wall cuts into it when the camera is far off axis (the card yaws with the camera): the side of the card that swings away from the camera goes back by (distance from the feet centre) x sin(camera yaw). A hand reaching 1 D sideways toward the map is behind the wall plane at 0.55 D from the wall once the camera yaw passes 33 degrees on that side. `pose()` reports it (`info[side]["clearance"]` negative, plus a warning). Stand the actor farther from the wall, shoot from the other side, or set `actor.yaw_fixed`.
4. Top-down and very steep views (view axis beyond 50 degrees) lean the card back; an actor near a wall then disappears into it. Keep actors 2 D clear of walls in such shots or hide them.
5. Frames below 1 are not supported by the image sequence.
6. A pencil tip registered on the wall is drawn on the card, which stands in front of the wall; its cast shadow falls where the card's does, not at the wall point.
7. The head's thick contour side and crescent are at the lower right in the v2 puppet, which suits a key light from camera-left. For a key from screen-right (the office set) set `actor.head_flip = True` (or a dict / callable frame -> bool) before `render_sprites`: the sprite is then drawn with the head disc mirrored (thick side and crescent at the lower LEFT), everything else unchanged; sprite jobs take the same flag as `"head_flip": True`, `sprites.sprite_svg(..., head_flip=True)`. Default False. (Added by the shot integrator in `v3/shots`; it uses the puppet's own `mirror`, which flips everything except the head disc, inside a mirrored group.)
9. With `setup(persistent=True)`: never overwrite a texture file that has already been rendered and expect to see the change; see `render.drop_cache` in section 6. (Not an issue with the default, persistent data off.)
8. Textures are not mip-mapped in Cycles: keep `px_per_D` within about 2.5 times the on-screen head size or thin lines shimmer in moves.
