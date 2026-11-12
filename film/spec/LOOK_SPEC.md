# LOOK_SPEC: one build specification for the reference look (v2)

Target: a 65 s, 720x1280, 30 fps short that looks like reference clip A ("Why Perfect Railroads Don't Work") and clip B ("The Ancient Jar That Warned an Empire").
Tools allowed: Blender 5.3 as a Python module (headless, Cycles on 4 CPU cores), code-drawn SVG rasterised by Chromium (Playwright), ffmpeg 6.1, numpy / OpenCV / Pillow. No internet except PyPI and npm.

## 0. Sources, conventions, status of each number

Inputs read in full (all six analyst files were present, none is missing): `character_anatomy.md`, `face_expressions.md`, `color_light_post.md`, `environment_materials.md`, `camera_motion.md`, `production_forensics.md`, plus `captions.md` from the main session. All are in `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/spec/` (called `SPEC/` below; `PROJ/` is its parent).

Frames I opened myself to judge the claims (full size: a/t16.5, t19.5, t40.0, t46.5, b/t06.5, t09.0, t24.5, t33.5; on reduced contact sheets or gridded crops: a/t03.0, t09.0, t14.5, t19.0, t27.5, t32.5, t34.5, t53.0, b/t03.0, t28.0, t41.5, t44.5); `v1_frame20.png`, `v1_frame45.png`; the three analyst prototypes (`character_puppet_proto_compare.jpg`, `face_proto/cmp_ref_vs_proto.jpg`, `env_proto/proto_overview.jpg`); two analyst evidence crops (`G_hats1.jpg`, `a_take_f405_655_strip.jpg`).

Checks I ran in this session (no Blender render was started):

| Check | Result | Files |
|---|---|---|
| Per-frame 2D composite in one persistent Chromium page (1440x2560 plate + foreground plate + SVG puppets with a displacement filter + blurred shadow + 2D camera move, 720x1280 screenshot) | 0.33 s per frame as PNG, 0.09 s per frame as JPEG q95, single process | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/lookdev_tmp/bench.js`, sample frame `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/lookdev_tmp/frames/f_0060.png` |
| v1 render cost, read from the v1 log | 16.2 s per 720x1280 frame (24 samples, 4 bounces, Freestyle, denoise) | `PROJ/render/office/anim.log` |
| Resolved office palette (section 3.2) painted into the environment prototype, two puppets on top, measured with `SPEC/measure_color.py` | section 3.5, last column | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/lookdev_tmp/office_v2pal_chars.png`, `palswap.py` |
| The grade model used for every "predicted" colour below (slope, offset, saturation 1.12) against the colour analyst's compositor-run table | within 3 levels per channel on 14 colours | `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/lookdev_tmp/pal.py` |
| bpy 5.3.0 API names used below (`world_to_camera_view`, `is_holdout`, `visible_camera`, `visible_shadow`, `film_transparent`, Solidify fields, Freestyle build flag, `compositing_node_group`) | all exist; lens 22 mm on the 36 mm sensor gives a focal length of 782.2 px | python check, no render |
| Colour and line-width samples on a/t16.5, a/t46.5, b/t24.5 | head `#fdf7f7` / `#fdf8f6`, crescent `#eadded`, ink `#402834` to `#452f3a`, hero hair `#5f3d24`, boss vest `#d6aa32` left to `#97721a` right. Head ink along rays from a circle fit: boss a/t16.5 0.021 to 0.026 D on the left against 0.069 to 0.073 D at 45 to 90 deg; hero a/t46.5 0.035 D at 3 o'clock rising to 0.065 D at 60 deg | python check |

Conventions:
- Frame 720x1280, 30 fps, 1950 frames for 65 s. W = 720, H = 1280.
- `D` = outer head diameter, ink to ink. **1 Blender unit = 1 D** for every set and camera number (v1 used D = 0.88 m; drop that).
- Puppet coordinates: origin = head centre, x to screen right, y DOWN, units of D. Angles around the head: 0 deg = 3 o'clock, 90 deg = bottom.
- Hex colours are sRGB as displayed in the final frame unless the column says "albedo".
- Frame references: `a/tSS.S`, `b/tSS.S` are the half-second stills in `PROJ/ref/a`, `PROJ/ref/b`.
- Status words: "measured" = an analyst measured it on the reference; "checked" = I confirmed it in this session; "predicted" = computed, not rendered; "judgement" = my call or an extrapolation. Unmarked numbers come from an analyst's measurement or verified prototype.

---

## 1. Production-method verdict

Both clips are conventionally produced, deterministic animation, not AI video (forensics lens: 88 percent confidence). Clip A is a real 3D world built from primitives, procedural shaders and typeset textures (the wall calendar shows the correct day grid for May 1880, the caliper scale counts 0 to 16, a newspaper keeps every glyph across 30 frames at 0.5 px reprojection error, the one wrong text is a clean mirror image, which is a flipped-UV bug and not garbling); clip B is illustrated plates moved with pan and zoom plus a few 3D inserts. In both, the characters are unlit toon puppets whose faces switch between discrete drawings, and shots are joined in an editor with short dissolves.

What it means for us: the reference is the same kind of pipeline as ours, so every property is reachable with Blender plus SVG and no generative step. v1 missed on art direction, not on technology: lit 3D characters, an empty pale room, a parked camera, no facial animation. Clip B also proves that flat 2D characters over rendered or painted plates is inside the style, which is what makes the cheap layered pipeline of section 6 legitimate.

---

## 2. Character system

### 2.1 Decision: hybrid. Procedural 2D SVG puppet, registered to the Blender set by exported camera data, composited over Cycles plates in Chromium

Every character pixel is drawn as SVG. Blender never renders a character. Pseudo-3D behaviour (turning, looking up, hats seen from above) is a set of parameters of the drawing.

Reasons, each tied to evidence:

1. The properties that carry the likeness are screen-space properties. The head outline is thin on the left and thick on the lower right and keeps that orientation when the sprite is mirrored (b/t05.0); the lavender crescent stays on the lower right in every lighting condition; features do not foreshorten, they slide by at most 0.14 D (read again on gridded crops: a/t16.5 -0.135 D, a/t03.0 -0.11 to -0.125 D). A 3D sphere with a decal fights all three, which is exactly how v1 failed (sphere shading `#ffffff` to `#9f968c`, features wrapping, a uniform 1.8 percent Freestyle line).
2. A sphere projects to a disc from every direction, so a flat disc loses nothing for the head, which is about half of a full figure's area (0.79 of about 1.5 to 1.9 square D) and most of what a close shot shows.
3. It is proven. The face prototype was rasterised in Chromium and re-measured with the reference scripts (eye spacing 0.264 against 0.26, outline bins within 0.3 percent of D except the bottom one, see `SPEC/face_proto/cmp_ref_vs_proto.jpg`). The 3D recipe (inverted hull, facing-ratio rim) was never rendered by anyone and has known unsolved parts: thick-thin ink, thin inner costume lines.
4. The reference animates faces on ones: three-frame blinks, a mouth drawing every 2 to 6 frames, an expression swap behind every blink. In a 3D render that forces a Cycles frame for each of 1950 frames (v1: 16.2 s each, 8.8 hours). As SVG it costs 0.1 to 0.33 s per frame.
5. Clip B characters are flat puppets beyond doubt (robe and skirt are flat shapes with an airbrush gradient, b/t24.5), and they share the face system and the ink with clip A.

What I concede to the forensics lens: clip A characters do behave as volumes in places (bowler seen from above at a/t14.5, peaked cap and top hat with real perspective, grey hair wrapping the back of the head at a/t19.0, torso leaning toward the lens). Those are covered by drawing parameters: a hat pitch parameter (2.6), a hair patch that grows with yaw (2.7), torso lean as rotation plus a width factor. The one thing lost is continuous free rotation, which the script does not need.

What 3D would have given for free, and how the hybrid gets it back:

| Lost | Replacement |
|---|---|
| Hard cast shadow on the ground (seen at a/t32.5, a/t34.5) | shadow polygon projected in the compositor from the same camera and sun (2.10) |
| Occlusion by furniture | depth matte rendered with each plate (2.10) |
| Hat and torso perspective under camera pitch | pitch parameter on hats, 0.93 to 0.85 torso width factors |
| Scene bloom over characters | not wanted: reference heads never glow (sky stays flat up to the head outline at a/t16.0) |

Fallback kept in reserve: the same sprites as emission cards inside Blender (`lightkit_clp.character_material`), only if a shot needs a character shadow falling across complex geometry.

### 2.2 Dimension table (D = 1; origin head centre; y down)

| Part | Value | Notes, frame |
|---|---|---|
| Head | circle, outer diameter 1.00; white fill radius 0.463 | clip A heads are circular within 2 percent (a/t16.0, a/t55.0). Clip B ovals (W/H 1.06 to 1.12) are not used |
| Head ink width by angle (0, 30, ... 330 deg) | 0.044 0.054 0.070 0.068 0.040 0.025 0.019 0.018 0.019 0.021 0.026 0.034 | cosine-interpolate between entries. Values from 210 to 330 deg (top) are an assumption: the top is always under a hat |
| Head wobble | fill radius(t) = 0.463 + 0.006 cos(2t + 0.9 s) + 0.007 Wb(t, s); ink radius = fill + width(t) + 0.005 Wb(t, s + 2.3); Wb(t, s) = 0.6 sin(3t + s) + 0.5 sin(5t + 1.7 s) + 0.3 sin(8t + 0.6 s) | one seed s per character, never per frame: the reference line does not boil (profile correlation 0.99 to 1.00 across 16 frames) |
| Quick head (circles only, no wobble) | ink disc r 0.499 at (0.014, 0.022); fill r 0.463 at (0, 0) | gives 0.022 left, 0.050 right, 0.062 lower right |
| Crescent | lavender band on the lower-right rim: 0.09 wide at 50 deg, 0.07 at 0 and 90 deg, 0.045 at 135 deg, gone by 180 deg, absent upper left; inner edge feathered over 0.04 | build: fill the disc with the crescent colour, then a lit disc r 0.420 at (-0.029, -0.034), Gaussian blur 0.016, clipped to the fill |
| Neck | none. Torso top at y = +0.36, chin at y = +0.49 | head overlaps the torso by 0.13 |
| Torso, slim pill (hero, kids, workers) | width 0.57, total height 0.99 | visible below the chin 0.86 (a/t02.0) |
| Torso, regular egg (extras) | width 0.78, total height 1.04 | a/t27.0 |
| Torso, stout egg (chief) | width 1.00, total height 1.06 | widest in the lower half (a/t16.0) |
| Stout profile (fraction of half-width, fraction of height, top to bottom) | (0.50, 0.02) (0.82, 0.10) (0.93, 0.25) (0.98, 0.38) (1.00, 0.58) (0.98, 0.77) (0.93, 0.84) (0.72, 0.95) (0.40, 0.995) | closed Catmull-Rom path through the points, mirrored |
| Slim profile | (0.60, 0.02) (0.90, 0.10) (0.97, 0.25) (1.00, 0.50) (1.00, 0.70) (0.96, 0.85) (0.75, 0.96) (0.40, 1.00) | regular = average of the two |
| Trouser bowl | bottom 0.14 of the torso, dark fill, 0.022 ink line above it | a/t02.0, a/t16.0 |
| Torso contour | 0.030 | draw the path in ink, then the same path inset 0.015 as the clip for fill and costume |
| Inner detail lines | 0.012 to 0.022 | V-neck, pockets, button rings, stitching |
| Torso shading | horizontal gradient: base x 1.12 at the left edge, base at 35 percent, base x 0.72 at the right edge | checked: boss vest `#d6aa32` left, `#97721a` right (a/t16.5). It is paint, not light: it never follows the sun |
| Shoulders | x = +/-(half-width - 0.045), y = +0.42 to +0.56 | arms start where the torso leaves the head |
| Arm | upper 0.37 + forearm 0.37 (total 0.71 to 0.79), elbow at the middle | one ink stroke, round caps |
| Limb stroke | 0.062 (allowed 0.055 to 0.075; 0.070 on the stout build); arms and legs equal | a/t02.0, a/t16.0, b/t03.0 |
| Limb curve | `M S Q C H`, C = E + bend x (E - (S + H) / 2); bend 0.75 to 1.0 relaxed, 0.5 hand on hip, 0 with a round join for a sharp knee | S shoulder or hip, E elbow or knee, H hand or ankle |
| Hand | ink disc, diameter 0.13 | fingers only for a gesture: one stroke 0.10 x 0.035 for a pointing index, three or four short strokes for an open hand, a bump for a thumb around a held object |
| Hips | x = +/-0.14 (stout, regular) to +/-0.22 (slim), y = torso bottom - 0.04 | |
| Leg | 1.10 (hero), 1.25 (default), 1.50 (chief); knee at the middle | straight when standing; a knee appears only when walking, sitting, crouching |
| Foot | stub 0.12 to 0.15 long continuing the stroke at about 100 deg to the shin, pointing outward | clip A manner; the prototype's feet were too long |
| Height, head top to feet | hero 2.9, default 3.0, chief 3.4 | head centre is 2.4 D (hero) to 2.9 D (chief) above the floor |
| Held prop sizes | newspaper 1.08 x 1.4 (measured, a/t32.0); cane 2.2 long with a 0.12 gold ball, cup 0.3, pencil 0.5 x 0.04, eraser 0.25 x 0.12 (judgement) | a/t32.0, a/t16.0 |

Reference poses for calibration (hand on hip): chief S (+0.36, +0.39), E (+0.66, +0.60), H (+0.40, +0.84); hero S (-0.24, +0.55), E (-0.46, +0.86), H (-0.28, +1.24). Pose catalogue to support: standing arms akimbo, one hand on hip, arms hanging, leaning in 35 to 45 deg with the head thrust forward, shouting arched back, striding in profile with scissored legs, arm extended (offering, pointing, drawing on the map), arm raised to the hat, sitting with legs dangling, sitting cross-legged with a cup, crouching with legs folded in a Z, holding a sheet with both hands, whole body tilted 25 deg.

### 2.3 Line system and widths in pixels at 720x1280

| Element (D) | wide, D = 120 px | medium, D = 200 px | close, D = 340 px |
|---|---|---|---|
| Head ink, left 0.020 / right 0.050 / lower right 0.066 | 2.4 / 6.0 / 7.9 | 4.0 / 10.0 / 13.2 | 6.8 / 17.0 / 22.4 |
| Limb stroke 0.062 | 7.4 | 12.4 | 21.1 |
| Torso contour 0.030 | 3.6 | 6.0 | 10.2 |
| Inner detail 0.012 to 0.022 | 1.4 to 2.6 | 2.4 to 4.4 | 4.1 to 7.5 |
| Hand disc 0.13 | 16 | 26 | 44 |
| Lid bar 0.030 thick, 0.178 long | 3.6, 21 | 6.0, 36 | 10.2, 61 |
| Eye spacing 0.26 | 31 | 52 | 88 |
| Set-object ink (not scaled with D) | 3 (allowed 2 to 5) | 3 | 3 |
| Set detail lines | 1.5 | 1.5 | 1.5 |

Hierarchy to keep in every frame: character ink : set-object ink : set detail = about 8 : 3 : 1.5 px in a medium shot. All ink scales with the character (it is part of the drawing). Edge roughness: bake the wobble into the path geometry (as `PROJ/v2/puppet/puppet.py` already does) or wrap the figure in `feTurbulence baseFrequency 3.2 numOctaves 1` into `feDisplacementMap scale 0.012` (D units). Background figures with heads under 60 px: drop inner detail lines thinner than 1 px, keep contour, limbs, eyes and mouth.

### 2.4 Character colours (display values; the puppet is composited after the grade, so these hexes are literal)

| Item | Hex |
|---|---|
| Ink: every contour, limb, hand, eye, brow, mouth line | `#3a2832` |
| Head fill / crescent | `#fef7f6` / `#e9dceb` |
| Mouth interior / tongue and inner dashes / teeth | `#4d2433` / `#7b626c` / `#fef9f8` |
| Hero: vest left, base, right | `#43ceb4`, `#3dbda6`, `#2e8678` |
| Hero: neckerchief or tie triangle, its dots | `#af2d3d`, pale dots (about `#f3d9d0`, judgement) |
| Hero: suspenders, buckles, buttons, trouser bowl | `#483a38`, `#d7c374`, `#e7dcdb`, `#624b44` |
| Hero: hair patch | `#603e25` |
| Hero: cap navy, stripe white, band, visor | `#44598b`, `#dee9fb`, `#362a3b`, `#989eb6` |
| Chief: waistcoat left, base, right | `#ddba4f`, `#c79d2d`, `#936e1e` |
| Chief: shirt V and centre line, buttons, welt pockets, trouser bowl | `#e7dcdb` with a grey line (about `#9a8f96`, judgement), `#d7c374`, `#8e6f2c`, `#45404d` |
| Chief: bowler dome, dark side, highlight streak, brim | `#463f4e`, `#2d2935`, `#cac8e2`, `#3b2f3a` |
| Chief: hair patch | `#948c95` |
| Extras: suit bodies | navy `#2f4171`, purple `#885285` (both measured); brown `#6d4a3a`, grey-blue `#5a6a8c` (judgement) |
| Sweat drop: fill, light half, outline | `#b6e3ff`, `#def9ff`, `#5c647a` (slate, not ink) |
| Blush | `#f8d7e1`, blur 0.018 |

Per-shot tint, multiplied onto the whole figure (clip B behaviour; clip A daylight uses none): warm lamp-lit interior (0.99, 0.91, 0.84); night with a lamp (0.99, 0.81, 0.88); night or storm without a lamp (0.71, 0.71, 0.94), where the ink also shifts to `#1e142e`. The crescent stays 8 to 12 percent darker than the tinted base in every case.

### 2.5 Costume detail rules

1. One closed torso shape carries everything. Costume = flat fills plus thin ink lines inside the torso clip, over the left-to-right gradient. No sleeves, no collar geometry, no shoes.
2. Each named character gets 5 to 7 readable costume elements: a neck shape (V with a centre line, or a hanging triangle), a centre-line button row (2 for the hero, 5 for the chief, each a gold or pale disc with an ink ring, diameter 0.065), one or two straps or a chain (suspenders with a dashed stitch line and small buckles; a watch chain of 12 or 13 overlapping ovals hanging in a curve from the second button to a fob), 1 to 3 pocket rectangles (outlined box for the hero, olive welt bars for the chief), the dark trouser bowl, one hat, one hair patch.
3. One hue per character, complementary to the other lead and absent from the walls behind them: hero teal, chief mustard. Extras stay in muted navy, purple, brown.
4. A painted highlight is allowed only on hats (one streak) and on the hand ball (a 1 to 2 px speck). Nothing else is glossy.
5. Hats replace the top of the head. Their lower edge crosses the head at y = -0.21 to -0.29, so the top 20 to 30 percent of the head is never seen and the brows sit right under the brim.
6. Our cast (judgement, period-fitted to a 1938 weather office while keeping the reference silhouettes): FORECASTER = slim pill, teal vest, red tie triangle, suspenders, two buttons, pocket with a pencil, striped flat cap, brown hair. CHIEF = stout egg, mustard waistcoat, shirt V, five buttons, watch chain, welt pockets, bowler, grey hair, optional cane. OTHER FORECASTERS = regular egg in navy, purple, brown with a green eyeshade or a bare hair cap. BEACH PEOPLE = slim or regular builds, striped bathing costume as the single torso pattern, straw hat or bare hair cap.

### 2.6 Hats and hair (relative to head centre, D units, y down; head top is y = -0.50)

| Hat | Front view recipe | Colours |
|---|---|---|
| Bowler | dome = upper half of an ellipse rx 0.42, ry 0.31 sitting on y = -0.37 (top at -0.68 to -0.70), ink 0.035. Brim = crescent from x -0.56 to +0.56, upper edge y -0.385 at the tips and -0.345 at the centre, lower edge dipping to -0.24 at the centre, tips curled up, ink 0.03. Highlight = one arc stroke 0.022 wide from (-0.30, -0.50) to (0.05, -0.635). Rotate the hat -3 to -8 deg. Angry brows touch the brim | section 2.4 |
| Striped flat cap | puffy dome 0.90 wide x 0.34 tall covering y -0.58 to -0.24 (checked on a/t46.5: 0.95 x 0.36; the anatomy prototype at 0.85 x 0.31 was too small); 12 to 14 visible white stripes 0.034 wide fanning from a top button (ellipse 0.06 x 0.03); dark band 0.05 tall bowed down 0.06 in the middle; visor crescent 0.76 wide reaching y = -0.15 to -0.20 | section 2.4 |
| Eyeshade (extras) | band 0.05 tall at y = -0.27, translucent green visor crescent 0.80 wide reaching y = -0.14 | band `#362a3b`, visor `#2d7a52` |
| Bare hair cap (extras) | flat patch inside the head outline covering the top 25 percent, ragged lower edge, no ink line on it | any hair colour |
| Top hat (optional) | crown 0.84 wide x 0.57 tall, base at y = -0.33, band 0.06 tall, brim ellipse 1.14 x 0.08 at y = -0.30 | `#393440`, stripe `#7d7482`, band `#dabc64` |

Hat pitch parameter (judgement; it reproduces what a/t14.5, a/t03.0 and a/t46.5 show, it was not fitted): let p = elevation of the camera above the hat in degrees, from -15 (seen from below) to +35 (seen from above). Brim: draw the full ellipse rx 0.56, ry = 0.56 x sin(p + 12 deg), clamped to 0.05 to 0.30, and hide its back half behind the dome when p < 20. Dome: keep rx, set its visible height to 0.31 x cos(p), and slide its base up by 0.10 x sin(p). Cap: grow the dome to 0.95 x (0.34 + 0.10 x sin(p)), move the button from the top edge toward the dome centre by 0.25 x sin(p), and let the visor show 0.12 to 0.18 beyond the dome on the facing side. Use p = 0 for eye-level shots, +25 for high wides, -10 for the low-angle chief.

Hair patch: a flat colour inside the head outline, directly under the hat, with a ragged (torn-edge) inner border and no ink line there. Front view: a crescent on each temple from the hat edge down to y = +0.08, maximum width 0.085. Turned: see 2.7.

### 2.7 View handling

Yaw is a number in [-1, 1]; positive = facing screen right. There is no back view.

| View | yaw | Face slide (eye midpoint) | Eye spacing | Far-eye scale | Hair | Torso | Hat |
|---|---|---|---|---|---|---|---|
| Front | 0 | 0 | 0.26 | 1.00 | two temple crescents | full width, details centred | symmetric |
| Slight | 0.25 | 0.03 | 0.24 | 0.97 | far temple crescent 1.5 x wider | details shift 0.03 | visor centre shifts 0.04 |
| Medium | 0.5 | 0.06 | 0.22 | 0.93 | one patch on the side away from the face, covering 0.18 of the head width | width x 0.96, details shift 0.07 | visor shifts 0.08 |
| Three-quarter | 1.0 | 0.12 (up to 0.14) | 0.185 | 0.86 | one patch covering a quarter of the head | width x 0.93, button row and chain shift 0.10 to 0.15 and curve | visor or brim front points past the head contour by 0.12 |
| Near-profile (walking, pointing along the screen) | 1.0 for the face | 0.12 to 0.14, both eyes stay visible | 0.17 to 0.185 | 0.85 | patch grows to a third of the head (the back of the head) | width x 0.85, button row 0.06 inside the facing edge, one suspender, legs scissored | visor points 0.20 past the contour |

Formulas: slide = 0.12 x yaw; spacing = 0.26 - 0.075 x |yaw|; far-eye scale = 1 - 0.14 x |yaw| (the far eye is the leading eye of the slide); brows and mouth slide with the eyes (0.85 to 1.0 of the eye slide). Near-profile is sold by the hair patch, the hat and the body, not by more slide: the anatomy lens's 0.25 to 0.30 slide is not supported by the frames (a/t03.0 re-measured at -0.11 to -0.125).

Pitch: looking up, proud or low camera moves every feature up 0.09 (eye line at y = -0.06); looking down or sad moves it down 0.07.
Roll: rotate the whole head group, hat included. Rest pose -8 to +8 deg, 10 to 20 deg on each new phrase, up to 30 deg for an extreme. An upright head is the exception in dialogue.
Never mirror the head disc: the thick side of the outline and the crescent stay on the lower right when the character faces left. Mirror features, hair, hat and body only.

Draw order, back to front: far arm, legs and feet, torso ink, torso fill and costume, near arm and hands, head ink, head fill, crescent, hair patch, face features, blush, sweat and tears, hat, held props, steam and Z.

### 2.8 Face: placement, building blocks, expression list

Placement (D units; eye "centre" = centre of the eye's bounding box):

    eyes at (slide - spacing / 2, eye_y) and (slide + spacing / 2, eye_y);  eye_y = +0.03 + 0.07 x pitch  (pitch -1.3 proud .. +1 down)
    brows 0.135 above their eye (neutral);  mouth at (slide, eye_y + 0.185)

Building blocks (cx, cy = eye centre; mx, my = mouth centre; all strokes ink with round caps):

| Block | Size (w x h) | Recipe |
|---|---|---|
| Half-lid eye (the DEFAULT eye) | 0.178 x 0.10 | lid bar from (cx - 0.074, cy - 0.035) to (cx + 0.074, cy - 0.035), stroke 0.030; pupil = ellipse centre (cx + gaze, cy - 0.013) rx 0.043 ry 0.062 clipped to y >= cy - 0.035; gaze -0.03 to +0.03. Anger: rotate the whole eye 10 deg so the inner end of the bar drops |
| Ring eye (surprise, excitement) | diameter 0.222 | circle r 0.0985, stroke 0.025, inside = head fill; pupil r 0.030 excited or 0.0165 frightened, offset up to 0.03. The two rings leave a 0.038 gap |
| Happy eye | 0.16 x 0.06 | `M cx-0.068,cy+0.016 Q cx,cy-0.048 cx+0.068,cy+0.016`, stroke 0.029 |
| Closed eye | 0.16 x 0.029 | line cx - 0.068 to cx + 0.068, stroke 0.029 |
| Blink half frame | 0.22 x 0.08 | ink ellipse rx 0.111 ry 0.040 with two fill-coloured ellipses (rx 0.022, ry 0.013) at +/-0.055 |
| Dot eye (rare) | 0.08 x 0.115 | ink ellipse rx 0.041 ry 0.0575 |
| Squeezed eye, left one (mirror for the right) | 0.17 x 0.09 | line (cx - 0.080, cy - 0.062) to (cx + 0.070, cy - 0.010) stroke 0.033; line (cx - 0.085, cy + 0.032) to (cx + 0.070, cy + 0.016) stroke 0.030 |
| Brow, hero dome | 0.16 x 0.04 | filled `M bx-0.08,by+0.02 Q bx,by-0.06 bx+0.08,by+0.02 Z` |
| Brow stroke | length 0.17 | thickness 0.045 (chief), 0.038 (hero), 0.033 (light). Angle: +15 deg determined, +24 deg angry (inner end down, length 0.19, thickness 0.052, only 0.10 above the eye so it touches lid and brim), -8 deg raised (0.20 to 0.25 above), -28 deg sad (outer end down) |
| Single brow rule | | when only one brow is drawn it sits over the near (larger, more central) eye |
| Mouth, dash | 0.10 x 0.034 | line 0.07 long, stroke 0.034 |
| Mouth, arch frown | 0.125 x 0.04 | `M mx-0.045,my+0.008 Q mx,my-0.014 mx+0.045,my+0.008`, stroke 0.034 |
| Mouth, smirk | 0.11 x 0.056 | `M mx-0.042,my-0.018 Q mx-0.018,my+0.026 mx+0.042,my+0.015`, stroke 0.032 |
| Mouth, small smile | 0.145 x 0.055 | `M mx-0.055,my-0.012 Q mx,my+0.040 mx+0.055,my-0.012`, stroke 0.034 |
| Mouth, grin | 0.42 x 0.13 | ink crescent `M mx-0.21,my-0.055 Q mx,my-0.005 mx+0.21,my-0.055 Q mx,my+0.185 mx-0.21,my-0.055 Z`; four teeth 0.057 wide at x = mx - 0.111, -0.037, +0.037, +0.111, clipped by the inner crescent `M mx-0.155,my-0.035 Q mx,my+0.008 mx+0.155,my-0.035 Q mx,my+0.110 mx-0.155,my-0.035 Z` |
| Mouth, flat bar | 0.286 x 0.058 | filled ink ellipse rx 0.143 ry 0.029 |
| Mouth, talking set (4 drawings) | 0.25 x 0.045, 0.28 x 0.085, 0.285 x 0.17, round 0.18 x 0.13 | the first is the flat bar; the others are ellipses filled with the mouth-interior colour, ink stroke 0.018, two faint dashes 0.05 long inside |
| Mouth, "O" | 0.19 x 0.17 | egg, narrower at the top, interior colour, stroke 0.018, tongue dash near the bottom |
| Mouth, clenched teeth | 0.18 x 0.13 | rounded rect rx 0.032, stroke 0.024, teeth-coloured, one horizontal and three vertical ink lines 0.013 (a 4 x 2 grid) |
| Mouth, wavy worried | 0.26 x 0.09 | `M mx-0.105,my+0.020 Q mx-0.070,my-0.045 mx-0.030,my-0.005 Q mx,my+0.022 mx+0.030,my-0.005 Q mx+0.070,my-0.045 mx+0.105,my+0.020`, stroke 0.040 |

No nose, no ears, no lashes, no cheek line, ever.

Expression list (eyes / brows / mouth / extras):

| # | Expression | Geometry | Reference |
|---|---|---|---|
| 1 | Neutral | half-lid / two brows 0.13 above / dash | a/t46.0 hero |
| 2 | Unimpressed | half-lid / ONE flat brow over the near eye, 0.136 above, thickness 0.037 / arch frown | b/t05.5 |
| 3 | Smirk, cocky | half-lid with gaze +0.03 / none / smirk | a/t02.0 |
| 4 | Determined | half-lid / both brows +15 deg, 0.12 above / arch frown | a/t13.5 |
| 5 | Angry | half-lid rotated 10 deg / heavy brows +24 deg touching lids and brim / arch frown 0.02 higher / pitch -0.9 | a/t16.0, a/t16.5 |
| 6 | Furious | as 5 with clenched teeth; purple head fill and steam (2.9) | a/t18.0 |
| 7 | Smug | half-lid / one raised brow over the near eye at -7 deg, thickness 0.048 / flat bar or smirk | a/t46.0 chief |
| 8 | Talking | any eye set held still / mouth cycles the talking set | a/t46.5 |
| 9 | Shocked | ring eyes, 0.033 pupils / optional short brows 0.2 above / "O" (or dash for a frozen stare) / sweat drop | a/t54.0 |
| 10 | Stunned, realising | ring eyes, 0.06 pupils / none / dash or tiny "o" 0.08 x 0.04 | a/t56.0 |
| 11 | Excited grin | ring eyes, 0.06 pupils / none / grin | a/t55.0 |
| 12 | Happy, content | happy arcs / both brows raised 0.20 above at -7 deg / small smile | a/t27.5 |
| 13 | Laughing with tears | happy arcs / brows 0.21 above / grin 0.43 wide / blush, two tears left and three right, head rolled 15 to 20 deg | b/t06.5 (checked) |
| 14 | Worried | half-lid or ring eyes / brows at -9 deg, 0.13 above / wavy mouth / sweat drop beside the far eye | a/t37.0 |
| 15 | Asleep | closed lines 0.02 lower / flat brows / small dash tilted 20 deg / three Z | b/t33.5 (checked) |
| 16 | Shouting | squeezed eyes / none / clenched teeth or the wide talking mouth | a/t03.0 (checked) |
| 17 | Grinning | dot eyes, closed arcs or half-lid / thin brows 0.14 above at -10 deg / grin | a/t45.0 |
| 18 | Wink | far eye happy arc, near eye half-lid / one brow 0.24 above the open eye / default mouth | b/t26.5 |
| 19 | Sad | half-lid or closed / brows -28 deg, 0.16 to 0.19 above / wavy mouth / pitch +1 | b/t44.5 (checked) |
| 20 | Blink frames | half = almond, closed = line; insert half, closed, half (one frame each) | a f1651 to f1655 |

For this script add one composite (judgement): WHISTLING = happy arcs, brows raised, round "o" 0.08 x 0.06, head bobbing; the reference has no musical-note glyph, so do not draw one.

### 2.9 Effects on characters

| Effect | Geometry (D) | Timing |
|---|---|---|
| Sweat drop | teardrop 0.075 x 0.115, stroke 0.014, lighter blob on its left half; at (0.33 x sign of yaw, -0.12), straddling the outline, under the hat layer | appears with the expression |
| Steam | puff = 5 overlapping circles r 0.045 to 0.065 in `#fffeff` over the same circles 0.014 larger in ink, underside `#e3e3f5`; three per side stepping up and out from the brim: (-0.36, -0.11) (-0.49, -0.24) (-0.57, -0.42) and (+0.56, -0.14) (+0.67, -0.29) (+0.75, -0.50) | spawn the inner puff, move each to the next position over 6 frames, fade the outer one; loop |
| Purple face | radial gradient centred (-0.07, -0.09), r 0.56: `#b769e1` 0, `#a152cd` 0.55, `#7c35a8` 1; arc highlight r 0.40 from 188 to 228 deg, stroke 0.012, `#f0b2ee` | rises from chin to top in 8 frames with a 0.02 wavy band `#d49ff9` and three ring bubbles |
| Sleep Z | bold italic Z, fill `#dbd1fa`, outline `#221a3f`; three on screen 0.33 apart, zig-zag +/-0.1 | rise 0.5 D/s, grow from 0.10 to 0.13, new one every 0.65 s |
| Laugh tear | ellipse 0.11 x 0.06, fill `#b8e4dc`, stroke `#383f36` 0.012; chain outward from the eye corner, each 0.8 x the last | fade over 4 frames |
| Hair on end | 8 or 9 ink strokes 0.25 to 0.3 long, 0.035 thick, fanned over the top half of the head | held 10 frames while the body jumps 1 D and lands |
| Focus lines | 25 to 35 white wedges 1 to 3 px wide, 60 to 250 px long, pointing at the character, over the background | redrawn every frame, 10 frames |
| Brightness dip | whole frame value x 0.75 | 0.4 s on one dramatic line (b/t03.3 to t03.7) |

Not in the reference and therefore not to be used: impact stars, speech bubbles, vein marks, question or exclamation marks.

### 2.10 Putting the puppet into the scene

1. Anchor. Each character has a world position on the floor (its feet). For every frame Blender exports, per character, the screen position of the feet and the depth z of the hips with `bpy_extras.object_utils.world_to_camera_view`. The puppet is drawn upright in screen space from the feet with `D_px = 782.2 / z` (lens 22 mm; z in D), inside the 2D camera group so that plate zoom and pan apply to it automatically. The figure is a billboard: it never tilts with the camera.
2. Occlusion. With each plate render a depth plate: same camera, `view_layer.material_override` = an emission material showing Camera Data > View Z Depth / 40, 1 sample, no denoise, view transform `Raw`, `scene.render.use_compositing = False`, 16-bit BW PNG (these names exist in bpy 5.3). In the build step threshold it at the character's depth minus 0.1 D, blur 1 px, and use it as an SVG mask on that character. One render handles any furniture layout. (Predicted, not yet run: verify the edge quality on the first plate; the fallback is a separately rendered foreground plate with `film_transparent`.)
3. Contact shadow, always: ellipse 0.9 D wide x 0.16 D tall under the feet, fill `#252432`, opacity 0.5, Gaussian blur 0.03 D. Mask the shadow layer with the same depth plate thresholded 1 D nearer than the character, so furniture in front hides the shadow and the floor itself never does.
4. Cast shadow, only where the character stands in direct sun (beach, office sun patch): project the puppet's silhouette points onto the floor along the sun direction (F = X - sun_dir x X.z / sun_dir.z, X on the billboard plane), then through the camera; fill the polygon with `mix-blend-mode: multiply` in the colour `encode(A / (A + K x sin(elevation)))` of the shot's preset so it matches the set's own Cycles shadows: `#648beb` for `EXTERIOR_NOON`, `#abddfb` for `LATE_AFTERNOON`, `#bac3ee` inside the office sun patch, `#9e9fb4` at night. Blur 2 to 4 px (reference edge 4 to 21 px). The reference's own character shadows correspond to multiply colours `#3c64d4` (noon ground, a/t02.0) and `#405ab9` to `#7a9dff` (station floor, a/t32.5, a/t34.5), so the noon value is in family.
5. Tint and focus. Multiply the per-shot tint of 2.4. In the two or three clip B style close-ups blur the plate, never the puppet (section 4.2 step 8).
6. Raster size. Draw the puppet as live SVG in the compositor page at its on-screen size (no sprite cache needed at 0.33 s per frame). If sprites are cached, rasterise at D = 512 px.

---

## 3. Environment system

### 3.1 Rules for both sets

Construction approach: **build each set once as real 3D geometry in Blender (boxes, cylinders, planes, cards; 1 BU = 1 D), texture every surface with SVG rasterised by Chromium, render it with Cycles as still plates per camera setup, and move those plates in 2D** (section 6). A pure-SVG painted backdrop would be cheaper for one angle but would need the perspective redrawn by hand for every camera; the 3D build gives every angle, the sun patch, hard set shadows and lamp bloom from one description. Flat explanatory artwork (map close-up, newspaper, telegram, storm track at sea) is pure SVG with pan and zoom, as clip B does with its cross-section.

Material classes:

| Class | Graph | Use |
|---|---|---|
| `lit` | Diffuse BSDF (albedo, roughness 1) + Emission (albedo x A, strength 1), Add Shader. `lightkit_clp.env_material(name, albedo_hex, A, image=...)` | architecture, floor, furniture, ground, houses: receives the sun patch and cast shadows |
| `painted` | Emission only, colour = ungrade(display colour), strength 1.0 | paper, map, dials, signs, small brass and gold, sky panes and far cards (value at most 0.92 so heads stay brightest) |
| `emitter` | Emission, strength 8 | bulbs and flames (`#fffeec`, `#ffeba4`); the only surfaces above scene-linear 1.0 |
| `ink` | inverted hull: Solidify (`offset` 1, `use_flip_normals` True, `use_rim` False, `material_offset` 1); slot 2 = Mix Shader by Geometry > Backfacing between ink Emission and Transparent BSDF | 3 px silhouette on box-like props |

No Principled BSDF, no specular, no bump, no procedural noise as visible texture. Optional Glossy mix 0.1 to 0.3 (roughness 0.25) only on rails and polished brass.

Authoring rule for `lit` colours (this resolves the palette conflict in section 8): **design a surface by the colour it should DISPLAY in ambient light, T, then compute albedo = ungrade(T) / A per channel, clamped to 0.92.** Where the clamp bites the target is unreachable in ambient light and the surface belongs in `painted`. `ungrade` = sRGB decode, then the inverse of the grade of 4.2 step 5 (HSV saturation / 1.12, minus the CDL offset, divided by the slope); it is implemented in `pal.py` (section 0). The tables below give T, the albedo and the predicted sunlit colour.

Outlines:
- Man-made set objects: 3 px ink at 720 px frame width, colour `#2a1712` in warm or daylight scenes, `#1d1449` at night or in the storm. Hull thickness for a 3 px line = 0.00384 x camera distance (D units; 0.015 at 4 D, 0.03 at 8 D), set once for the main shot of that prop. Freestyle (`select_by_collection`, silhouette + border + crease, 3 px absolute) is allowed for plates only and never for per-frame renders.
- Interior detail lines (plank seams, panel insets, brick joints, clapboard): 1.5 px, drawn in the SVG texture, colour = surface x 0.68 (x 0.45 at night). Stroke width in texels = 3 x texture px across the surface / screen px the surface covers in the widest shot.
- Never outline: sky, clouds, sea, sand, haze cards, light shafts, glow cards. Far objects: 1.5 px, lightened toward the haze colour.
- Contrast trim on every piece of furniture: a lighter front-edge strip on tops (top colour x 1.25, 0.06 D high) and a darker inset line on panels and drawers (colour x 0.6). This is what replaces ink in clip A and it survives small scale.

Texture resolution: at least 1 texel per screen pixel at the closest shot; 2048 px for a wall or floor, 1024 px for a prop face, 512 px for a small card. Furniture is sized to the big heads, not to the thin bodies (desk top 1.45 D high, chair back 1.37 D wide).

Brightness structure of every interior frame: the wall band behind the heads reads luminance 95 to 170 of 255 (aim 120), the top of frame 60 to 80, the bottom 40 to 70. Paint this into the set: multiply a soft plum gradient (`#1a1025`, not grey) into the ceiling, the upper wall and the floor toward the camera. Never apply it as a full-frame vignette, because the heads must stay near white wherever they are.

### 3.2 Interior: the 1938 weather-bureau office

Style: clip B drawing (inked props, patterned flat fills, 20 to 26 objects, light pooled on the middle band) plus three things from clip A: one hard sun patch from the window, glowing lamp bulbs with a tight halo, contrast trim.

Shell (normals inward; build the ceiling and both side walls, the 22 mm lens shows them):

| Part | Size in D | Notes |
|---|---|---|
| Floor | 9 wide x 8 deep | planks run toward the back wall |
| Back wall | 9 x 4.8 | carries the map, centred |
| Side walls | 8 x 4.8 | window in the left wall: 2.0 x 2.8, sill at 1.6 |
| Ceiling + 3 cross beams 0.3 x 0.35 | 9 x 8 | |
| Carpet runner | 3.4 wide (the width used in the measured mock-up; the environment lens had 2.2), from the back wall to the camera, 0.01 above the floor | the cool block of the frame |

Surfaces (T = display target in ambient light; albedo and sun colour predicted for `INTERIOR_DAY`; "lamp" = ambient-only colour under `INTERIOR_LAMP`):

| Surface | T | Albedo | In the sun patch | Lamp ambient | Pattern |
|---|---|---|---|---|---|
| Wallpaper base (1.6 to 4.2 D) | `#9c5257` | `#e48f7d` | `#d46a4e` | `#703344` | vertical stripes 0.08 D wide at 0.16 D pitch in `#914c51`; diamonds 0.32 x 0.38 D pitch, staggered, `#bd7a6e` with a 1 px `#6a3c40` line (diamonds are `painted`) |
| Frieze (4.27 to 4.8 D) | `#7a4548` | `#b27564` | `#a65942` | `#582b39` | plain |
| Picture rail (4.2 to 4.27 D) | `#c9a878` | `painted` | - | - | inked |
| Wainscot (0.15 to 1.5 D) | `#62281a` | `#8f4c2a` | `#863400` | `#46181b` | raised panels `#6e2f1f` every 0.9 D, 2 px inset line `#33180f`, 1.5 px highlight under the top edge |
| Chair rail (1.5 to 1.6 D) / baseboard (0 to 0.15 D) | `#84402a` / `#3b1c12` | `#c17349` / `#533004` | `#b45209` / `#502406` | `#5f2725` / `#2c1216` | inked top edge |
| Floor planks | `#6a4640` | `#9a7257` | `#915c3b` | `#4c2c33` | planks 0.28 D wide, each x 0.90 to 1.08 at random; seam `#33201e` at 7 percent of the plank width; butt joints staggered every 3 to 6 D; two or three grain streaks per plank at x 0.86 to 0.90 |
| Runner field / border / line | `#26395e` / `#7a2430` / `#b98f45` | `#405f78` / `#b2524b` / `painted` | `#3a5065` / `#a72c1f` | `#1d2248` / `#581428` | border 0.15 D, gold line 0.04 D, red diamonds with a gold outline every 1.5 D |
| Ceiling / beams | `#35232b` / `#281a20` | `#493830` / `#33271a` | - | `#281624` / `#1f111d` | plank lines 1.5 px |
| Desk body / top / edge strip / drawer fronts | `#5b2e1c` / `#8a522b` / `#ad7142` / `#6b3621` | `#845129` / `#c9894c` / `painted` / `#9c5f36` | `#7c3c07` / `#bd6b03` / - / `#924607` | `#421c1c` / `#633326` / - / `#4d211f` | side in shade x 0.72; knobs `#e2a630` |
| Filing cabinets / drawer fronts | `#51578f` / `#5c63a0` | `#8391ba` / `#95a4d0` | `#777999` / `#8789ab` | `#39356d` / `#413d79` | inset line x 0.6, label cards `#f3e7c9`, pulls `#e2a630` |
| Lamp shades / sign board | `#2d7a52` / `#1c403d` | `#54b96f` / `#27624a` | `#3ea051` / `#22553e` | `#255041` / `#182930` | sign lettering `#e9d9b0` slab capitals |
| Teletype, telephone | `#2b2630`, `#1c1a22` | `#393b36` | - | `#211827` | keys `#e9d9b0`, roll `#d9c9a8` |
| Window frame / coat / cork | `#6f3522` / `#3b3350` / `#7a5a34` | `#a25f38` / `#575465` / `#b28f4f` | - | - | |

Composition by area in a wide shot: about 25 to 30 percent dark cool (runner, cabinets, ceiling plum, deep floor), 40 to 45 percent warm mid-tones (rose wall, walnut, plank), about 10 percent brass and tan accents, at most 8 percent near-white (heads, lit paper, bulbs). The walls stay in the rose to walnut family so the teal hero and the mustard chief both separate from them (checked in the mock-up: the earlier orange-brown wallpaper `#a8663f` swallowed the mustard waistcoat). Green is confined to lamp shades, the sign and eyeshades.

Props (every item inked 3 px unless noted):

| # | Prop | Size in D | Build | Colours |
|---|---|---|---|---|
| 1 | Wall map in frame (hero prop) | 4.2 x 2.6 outer, centre 3.0 above the floor | box frame 0.15 wide + `painted` SVG card 2048 px | frame `#3d1c12`, gold inner line `#cb9f48`, land `#cdb98f`, sea `#86aec6` (a soft lighter pool painted in at the top centre, up to `#e4d6ae` and `#a8c8da`), isobars `#6f93a8` 1.2 px, grid `#8fb0bf` 0.8 px, storm track `#c2311e` 5 px with arrowhead, labels `#3d2a22`. In full-frame inserts the paper may go to `#f1e3c0` |
| 2 | Sign "U.S. WEATHER BUREAU" | 3.8 x 0.4, above the map | SVG card | as above |
| 3 | Desks, 2 or 3 | 3.0 x 1.5 x 1.45 high | box body + top slab + 3 drawer insets + knee-hole | as above |
| 4 | Chairs, 2 | back 1.4 wide, top at 2.6, seat at 1.2 | boxes | desk colours |
| 5 | Pendant lamps, 2 or 3 | shade 1.0 across, bulb 0.42, centre 4.0 above the floor | cone + sphere + cord | shade green, bulb `emitter` |
| 6 | Banker's lamps, 2 | shade 0.7 x 0.6 | half cylinder + stem + base | green, brass, emissive slit |
| 7 | Teletype on a stand 1.3 high | 1.3 x 1.0 x 0.8 | box + sloped top + key strip + roll + paper card + tape 0.08 wide hanging 1.5 | paper `#f6efe2` with grey lines `#9a8f86` |
| 8 | Filing cabinets, 2 to 4 | 1.1 x 1.2 x 3.0, 4 drawers | box + insets | steel-violet; a box `#b08a52` and a paper stack on top |
| 9 | Banjo barometer | 0.55 x 1.4, dial 0.5 | SVG card | board `#6d3a1f`, dial `#f3e7c9`, ring `#e2a630`, column `#c2311e` |
| 10 | Wall clock | 0.9 across | cylinder + SVG face | rim `#3d1c12`, face `#f3e7c9` |
| 11 | Tear-off calendar | 0.8 x 1.1 | SVG card | header `#b61d32` with `#f3d9a8` capitals, page `#f6efe2`, numeral `#b61d32` |
| 12 | Notice board, 3 pinned sheets | 0.9 x 1.2 | SVG card | cork, sheets `#f6efe2`, pins `#c2311e` |
| 13 | Coat stand with hat and coat | 3.4 high | cylinder + SVG card | pole `#6d3a1f`, coat `#3b3350`, hat `#4a3a2c` |
| 14 | Window | 2.0 x 2.8 | frame boxes + `painted` gradient pane `#7da5e6` (top) to `#b9d3ee`, strength 1.0 to 1.5 + optional additive shaft card `#ffe2a8` at 13 to 16 percent | |
| 15 | Small dressing, 8 to 10 pieces of 0.2 to 0.8 D | telephone, ink bottle `#26395e`, paper stacks, red pencil, wastebasket `#7a5a34`, rolled charts `#f1e3c0`, wall thermometer, second small chart, radiator `#5d5560` | boxes and cards | |

Density: 20 to 26 distinct objects in any wide frame, at least 8 behind the characters in a two-shot, at least three hue families. Four to six glowing points visible in a wide shot. Bloom halo ends at 1.3 to 1.6 bulb radii.

Lighting variants of the same set: DAY (`INTERIOR_DAY`, sun through the left window so a hard patch with the mullion shadow lands on the floor and the lower back wall); GREY MORNING (judgement: `INTERIOR_DAY` with the sun off, pendant lamps on, pane `#a79da6` to `#dfdfe7`); EVENING or STORM (`INTERIOR_LAMP`, pane `#32336c`, lamps as key).

### 3.3 Exterior: the beach town

Style: clip A staging and light (a real ground plane to a horizon at 0.34 to 0.50 H, gradient sky with soft un-inked clouds, hue shift with distance, one hard sun with blue-plum shadows, saturated warm ground against blue). Terrain, sea and sky carry no ink; man-made objects keep the 3 px ink so the beach and the office read as one film (judgement by the environment lens, kept).

Geometry:

| Part | Size in D | Build |
|---|---|---|
| Sand | 300 x 300, 64 x 64 subdivisions | plane + Displace (Clouds, scale 6 D): 0.3 D everywhere, 1.5 to 3 D in a dune band 15 to 40 D inland |
| Sea | from the shoreline to 600 D out, 0.1 D below the sand edge | plane; no Ocean modifier |
| Wet sand and foam | strips 1.5 D and 1 D wide along the shoreline | `#c9a07a`, `#f1eef7` |
| Sky | emissive dome or backdrop card with an SVG gradient, 4 to 6 soft cloud cards, one sun-glow card | never the Sky Texture node |
| Far headlands | 2 cards at 400 to 600 D, about 4 percent of frame height | lavender `#8d78b0`, farther one `#7393d0` |
| Houses, 5 to 8 | 7 wide x 6 deep, eaves at 4.2, ridge at 6 | box + gable roof + porch slab + door 1.4 x 3.7 + 2 windows 1.2 x 1.2 with shutters + chimney |
| Telegraph poles, 6 to 8 | 9 high, radius 0.15, spaced 14 | cylinder + crossarms 2.2 and 1.6 + 4 insulators + wire curves sagging 0.7 (1.3 px) |
| Dressing | rowboat 6 long, striped umbrella 3.85 across, deck chair, 6 fence posts 1.5 high with rope, crate 1.2, bucket, sign 2.6 x 1.0, picnic basket, towels | simple meshes or cards |
| Scatter | 150 to 400 pebble and shell specks 0.03 to 0.12, denser near the camera; 40 to 80 dune-grass tufts 0.8 to 1.2 high; 12 to 16 footprints | instances or cards |

Surfaces (T = display target in sun under `EXTERIOR_NOON`; albedo and shade predicted):

| Surface | T (sunlit) | Albedo | Predicted shade | Recipe |
|---|---|---|---|---|
| Sand light / mid / dark | `#f3ad6f` / `#e79a4f` / `#d28a50` | `#f6c888` / `#f6b56f` / `#e8a369` | `#535f7b` / `#575765` / `#524d61` | Noise (scale 0.4 per D, detail 4) into a ramp of the three; ripples = Wave bands (scale 1.5 per D, distortion 3) x 0.9 to 1.0 at factor 0.12; distance tint by Camera Data > View Distance (20 D to 150 D) toward `#e78c6d`, then `#f0b98c` |
| Wet sand | `#c9a07a` | `#deb588` | `#49547b` | |
| Sea | near `#2f55b8`, far `#6f9fe6`, a 10 px pale band `#b9d3ee` at the horizon | `painted` with the distance factor | - | swell streaks: Wave bands parallel to the shore (scale 0.5 per D, distortion 4) through a narrow ramp step, mixed `#e6eefc` at 0.6; matte |
| House cream / red / blue-grey | `#ebddc8` / `#b84735` / `#7f8fbf` | `#f6f6d2` / `#cd6650` / `#96a5c5` | `#7988a1` / `#4a2d4b` / `#3d5296` (cream and blue-grey with the pale-surface ambient, see below) | clapboard lines 1.2 px at 0.21 D pitch in body x 0.68; gable end = body x 0.92; doors = roof x 1.1; panes `#9cc0f0` |
| Roof maroon / slate | `#5b211d` / `#4d3e3f` | `#622d1f` / `#52453d` | `#261527` / `#1d1d3c` | |
| Pole wood / fence / boat hull / dune grass | `#6d3a1f` / `#8a5a35` / `#c2311e` / `#8aa23a` | `#784828` / `#996a42` / `#d85a48` / `#9cb34c` | `#2d222c` / `#373240` / `#4e2544` / `#345846` | rope `#d9c9a8`, insulators `#b9d7e4`, gunwale `#f6efe2`, grass strokes also `#67832c`, `#4f6b2a` |
| Sky, day | `#4b74c2` zenith, `#6197e5` at 60 percent, `#99bee9` horizon | `painted` | - | clouds `#e6e9f8` with tops `#f4f3fb`, edges blurred 20 px or more, 20 to 35 percent of the sky |

Albedo clamp: light and mid sand need an albedo above 0.92 in red, so under this preset they top out near `#deb175` and `#de9c53`; accept that or raise K by a tenth.

Pale-surface ambient (my correction, predicted): with the noon ambient A = (0.10, 0.21, 0.79) a cream wall in shade comes out `#406ebc` and white foam `#2c65dc`, a saturated blue the reference never shows on pale paint. For any `lit` material whose albedo saturation is under 0.25 use A = (0.22, 0.28, 0.55) instead; the cream wall then shades to `#7988a1`.

Depth: mix far cards and far ground toward `#a0bfec`, up to 60 percent at the horizon (mid distance 30 to 50 percent, farthest layer 90 to 100 percent toward the sky colour). Let the nearest 15 percent of the frame fall to about half brightness (a dune or fence in shade). Density: 12 to 18 distinct objects in a wide shot plus the scatter.

Variants (palettes extrapolated; the reference has no sea, rain or storm):

| Beat | Sky top to horizon | Sea | Sand | Notes |
|---|---|---|---|---|
| Sunny last swim | `#4b74c2` to `#99bee9` | `#6f9fe6` to `#2f55b8` | `#f3ad6f` | `EXTERIOR_NOON` or `LATE_AFTERNOON` |
| Grey drizzle morning | `#a79da6` to `#dfdfe7` | `#83757a` to `#a79da6` | `#b9a48f` | no sun, no cast shadows, object saturation halved, thin rain strokes at 15 percent added in the compositor |
| Storm arriving | `#32336c` to `#7673b5` | `#183ca1`, wave face `#285bc9`, base `#261735` | `#68609f` | `NIGHT` preset values, ink `#1d1449`, foam `#c7afde` to `#eef2fe`, lit windows `#ffd995`, puppets tinted (0.71, 0.71, 0.94) |

The wave: layered effect over an unchanged plate, as the reference does its explosion and dust plume. First a pale flat band on the horizon (`#c9bfbd`, the "fog bank"), then two or three overlapping bands with wavy top edges and speckle, at least 8 D high at house depth (ridge is 6 D), darkening to `#183ca1` as they near, with a scalloped foam crest. Draw them as SVG layers in the compositor, each scaled by its own depth.

### 3.4 Text-bearing props and flat inserts

- One or two lines large and legible, everything else greeked (grey bars); a thin ruled border. The wall map carries at most two legible labels (the date and one city) and the storm track is the most saturated mark on the wall.
- Sizes: a held sheet is 1.08 x 1.4 D; headline cap height about 0.10 of the sheet width, spanning 85 percent of it; a calendar month name is twice the cap height of its header; a featured banner's cap height is about 11 percent of frame width.
- Colours: paper `#fff5df`, printed ink `#836d4e` (never black), red `#b61d32`, navy `#081148`, cream lettering on colour `#edb48c` to `#f3d9a8`.
- Type: headlines and signs in bold slab or fat-face capitals with 1 to 2 px letter spacing, mastheads in mixed-case old-style serif, teletype output in a typewriter face. Installed now: DejaVu Serif Bold, Liberation Serif, Courier 10 Pitch. Reachable on npm (version 5.3.0 each, not yet installed): `@fontsource/abril-fatface`, `@fontsource/alfa-slab-one`, `@fontsource/rye`, `@fontsource/old-standard-tt`, `@fontsource/im-fell-english`, `@fontsource/special-elite`. Use correct real data (dates, weekday grids).
- A prop insert is shown by pushing into the real prop (0.3 x to 1.4 x area in about 12 frames) and whipping back out, or as a full-frame SVG with pan and zoom. In flat SVG artwork use no colour darker than the ink `#3a2832` except caption black.

### 3.5 Acceptance checks for a frame with characters in it

| Check | Pass | Reference | v1 | Resolved-palette mock-up (ungraded SVG, checked) |
|---|---|---|---|---|
| Canny edge density (60/140), caption band masked | at least 0.05 | A 0.060, B 0.067 | 0.016 | 0.055 with puppets, 0.048 for the empty plate: add fine detail |
| Featureless 40 px blocks | at most 0.30 (office 0.25) | A 0.30, B 0.27 | 0.64 | 0.30 |
| Mean luminance of the top eighth / brightest of the middle rows / bottom eighth of the frame | 40 to 90 / 105 to 150 / 30 to 70 | checked: b/t24.5 40 / 115 / 50, b/t06.5 65 / 127 / 72, a/t27.5 89 / 83 / 27 | 212 / 206 / 163 | 65 / 145 / 33 |
| Luminance in a ring around each head | 95 to 170 | A 120, B 136 | 134 to 145 (passes; v1 fails on the bands above) | 135 and 149 |
| Set objects in a wide shot | office 20 to 26, beach 12 to 18 | B 25 to 35, A 4 to 16 | 5 | about 25 (hand count) |
| Surface detail (luma std after a sigma-12 high-pass, 120 px patch of wall and of floor) | 0.03 to 0.10 | 0.03 to 0.14 | 0.002 | floor 0.056, runner 0.038 |


---

## 4. Lighting, colour and post

### 4.1 Numeric targets (measure with `python3 SPEC/measure_color.py --palette frame.png`; caption band masked)

Targets are for interior shots; the exterior ranges are the clip quartiles in the "reference" column. The last column is the resolved-palette mock-up of section 0 (ungraded SVG with two puppets), which shows what is already met and what the grade and the sun patch still have to add.

| # | Quantity | Reference | v1 | Target | Mock-up (checked) |
|---|---|---|---|---|---|
| 1 | Saturation mean | interiors 0.725, 0.563, 0.395, 0.324; clip medians 0.483 (A), 0.405 (B) | 0.293 | 0.40 to 0.60 | 0.41 |
| 2 | Saturation p90 | interiors 1.000, 0.775, 0.630, 0.619 | 0.477 | at least 0.62 | 0.65 |
| 3 | Value mean | interiors 0.452, 0.444, 0.586, 0.470 | 0.723 | 0.44 to 0.60 | 0.44 |
| 4 | Luma p5 | 0.090, 0.101, 0.177, 0.123 | 0.249 | 0.09 to 0.18 | 0.109 |
| 5 | Luma p50 | 0.147, 0.246, 0.423, 0.282 | 0.654 | 0.22 to 0.45 | 0.263 |
| 6 | Luma p95 | 0.454, 0.790, 0.902, 0.769 | 0.927 | 0.75 to 0.92 | 0.846 |
| 7 | Contrast, luma p95 - p5 | 0.366, 0.683, 0.725, 0.647 | 0.678 | 0.60 to 0.75 | 0.737 |
| 8 | Colourfulness (Hasler-Suesstrunk) | 101, 63, 63, 43; clip medians 82, 56 | 49.7 | 55 to 100 | 48 (not yet met) |
| 9 | Share of pixels with S > 0.5 | 0.875, 0.679, 0.273, 0.230 | 0.063 | at least 0.25 | 0.34 |
| 10 | Share of pixels with S < 0.15 | 0.028, 0.081, 0.118, 0.201 | 0.140 | at most 0.12 | 0.078 |
| 11 | Share of pixels with V > 0.95 | 0.035 (A), 0.045 (B) | 0.066 | 0.02 to 0.09; heads, lit paper and lamps only | 0.039 |
| 12 | Black point, luma p1 | 0.104 (A), 0.095 (B) | 0.153 | 0.08 to 0.12 | 0.083 |
| 13 | Mean colour of the darkest 10 percent | `#3d1c32`, `#392433`; hue 318 to 319, S 0.37 to 0.53 | `#4a3a2d`, hue 26 | hue 250 to 345, S at least 0.35 | `#201822`, hue 288, S 0.28 (S not yet met) |
| 14 | Mean colour of the 40 to 60 percent band | `#90646a`, `#7d656d` | `#b8a98e` | hue 330 to 25 or 230 to 290; V 0.40 to 0.60 | `#593f3c`, hue 6, V 0.35 (slightly dark) |
| 15 | Largest palette cluster (k-means, k = 8) | dark saturated, 20 to 31 percent (`#161a42`, `#6b3723`, `#221c31`, `#976c4d`) | `#ddd5ba` 33 percent | V at most 0.65 and S at least 0.35 | `#372223` 23 percent |
| 16 | Head fill at the head centre | `#fcf8f6` typical; V 0.98 to 1.00, S 0.02 to 0.04 | `#ffffff` clipped | V 0.97 to 0.995, S at most 0.04 | `#fef7f6` by construction |
| 17 | Head flatness, centre against 10 px inside the outline | V difference at most 0.07 | 1.00 against 0.62 | at most 0.07 (crescent side only) | by construction |
| 18 | Surface detail, wall and floor patches | 0.03 to 0.14 | 0.002 | 0.03 to 0.10 | floor 0.056, runner 0.038 |
| 19 | Set shadow in a sunlit exterior, shadow against lit on warm ground | hue 244 to 259 against 16 to 28; V ratio 0.29 to 0.59 | brown, V ratio 0.91 | hue 230 to 270, V ratio 0.35 to 0.60 | exterior only, see 4.2 step 3 |
| 20 | Shadow edge width, 10 to 90 percent | 4 to 21 px | none (sun angle 8 deg) | 6 to 20 px | - |
| 21 | Bloom around a lamp: 10 percent radius minus core radius | 12 to 24 px | none | 12 to 24 px; none around heads | - |
| 22 | Grain / sharpening / vignette | none / none / 0 to 5 percent | none | none / none / at most 4 percent | none |
| 23 | Character ink width / head diameter | 0.02 (left) to 0.066 (lower right), plum | 0.018 uniform, `#272727` | as 2.2 | by construction |

Do not add contrast: v1's luma contrast (0.68) was already at the reference level (0.61 median).

### 4.2 The recipe

**Step 1. Colour management and Cycles (plates and true-3D frames).** `lightkit_clp.setup_render(scene)` plus the values below.

| Setting | Value |
|---|---|
| View transform, look, exposure, gamma | `Standard` (the bpy default is `AgX`, which desaturates), `None`, 0.0, 1.0; display sRGB |
| Engine | Cycles, CPU, 4 threads |
| Samples | plates 48, true-3D frames 16; adaptive sampling on; OpenImageDenoise on for plates |
| Bounces | `max_bounces` 1, `diffuse_bounces` 0, `glossy_bounces` 1, `transmission_bounces` 0, `volume_bounces` 0, `transparent_max_bounces` 8; caustics off; `sample_clamp_indirect` 3 |
| Film | not transparent for plates; default pixel filter; no motion blur in Cycles |
| World | black, strength 0 (the ambient lives in the materials) |

**Step 2. Lighting model.** In scene-linear values: `displayed = albedo x (A + K x cos(angle to key) x visibility)`. A is a flat ambient colour injected as emission in every `lit` material, so shade is exactly `albedo x A`, noise-free. K is the key on a surface facing the light: Sun `energy = pi x max(K)`, `color = K / max(K)`. A point lamp that should add `g x albedo` at distance d: `energy = g x 4 x pi^2 x d^2` (d in Blender units; colour (1.00, 0.69, 0.31), g = 0.9, radius 0.05; pair it with an `emitter` bulb for the visible glow). These two photometric formulas have not been confirmed by a render: see 4.3.

| Preset | Ambient A (linear) | Key K (linear) | Sun energy, colour | Elevation, azimuth | Sun angle | Head as displayed | Puppet shadow multiply (2.10) |
|---|---|---|---|---|---|---|---|
| `INTERIOR_DAY` | (0.42, 0.40, 0.56) | (0.70, 0.54, 0.15) | 2.20, (1.00, 0.77, 0.21) | 38 deg, through the window | 1.5 deg | `#fef7f6` | `#bac3ee` in the sun patch |
| `INTERIOR_LAMP` | (0.20, 0.16, 0.30) | lamps only | no sun | - | - | tint (0.99, 0.91, 0.84) | contact shadow only |
| `EXTERIOR_NOON` | (0.10, 0.21, 0.79); pale surfaces (0.22, 0.28, 0.55) | (0.90, 0.79, 0.21) | 2.83, (1.00, 0.88, 0.23) | 50 deg, -55 deg | 1.5 deg | `#fef7f6` | `#648beb` |
| `LATE_AFTERNOON` | (0.20, 0.45, 0.95) | (0.85, 0.50, 0.10) | 2.67, (1.00, 0.59, 0.12) | 20 deg, -70 deg | 1.5 deg | `#fef7f6` | `#abddfb` |
| `SUNSET` | (0.35, 0.25, 0.45) | (0.80, 0.44, 0.20) | 2.51, (1.00, 0.55, 0.25) | 8 deg, -80 deg | 2.5 deg | `#fff5f3` | `#e2e8f8` |
| `NIGHT` (also the storm) | (0.12, 0.13, 0.45) | (0.33, 0.35, 0.75) | 2.36, (0.44, 0.47, 1.00) | 45 deg, -55 deg | 1.5 deg | tint (0.71, 0.71, 0.94) or lamp tint (0.99, 0.81, 0.88) | `#9e9fb4` |

`INTERIOR_DAY`, `INTERIOR_LAMP` and `EXTERIOR_NOON` rest on many reference samples; the other three on two or three pairs each and are starting points.

**Step 3. Key direction and shadow character.** The key comes from camera-left, above and slightly behind the camera, so shadows fall to screen right and away (azimuth -55 deg for a camera looking along +Y). Sun angle 1.5 deg gives a penumbra of about 11 px for an occluder 2 D from the receiver in a medium shot (D = 200 px), inside the measured 4 to 21 px (v1 used 8 deg and a 250 W area fill: remove both). No fill light, no rim light, no bounce. In the exterior, cast shadows on warm ground must swing to blue-violet (target row 19); in the office the room is mostly ambient-lit, so the violet comes from the palette (runner, cabinets, plum ceiling and falloff), from the grade's plum black point and from the puppet shadows, not from the light (section 8, item 9).

**Step 4. Sky, haze, glare.** Sky = emission card or dome with an SVG `linearGradient`. Day: `#4a78cd` 0 percent, `#5e92e5` 45, `#7eabe9` 85, `#92b7e7` 100. Sunset: `#bdb0b8` 0, `#d7cad1` 45, `#eee4cf` 70, `#f2d8ab` 90, `#e5c1b2` 100. Night: `#1e2e7b` 0, `#1748ae` 60, `#204c8f` 100. Clouds: soft white shapes at 60 to 80 percent opacity, 6 px blur or more, no outline. Haze is baked into far cards and the distance tint, never a volume. Sun in frame: additive radial card, white core 68 px radius at 720 px width, 50 percent at 120 px, 10 percent at 260 px.

**Step 5. Compositor on every plate and true-3D frame** (`grade_compositor.build(scene, preset={'vignette_strength': 0.0})`):

| Order | Node | Parameters |
|---|---|---|
| 1 | Glare | Type `Bloom`, Quality `High`, Threshold 1.0, Smoothness 0.1, Size 0.05, Strength 0.5, Saturation 1.0, Tint (1.00, 0.92, 0.80). For large painted glows (moon, storm lightning) Size 0.20, Strength 1.0 |
| 2 | Color Balance, ASC-CDL | Offset (0.0075, 0.0035, 0.0095), basis 0; Power 1.0; Slope (1.000, 0.985, 0.970). Black renders `#150919` |
| 3 | Hue/Saturation/Value | Saturation 1.12 (tuning range 1.05 to 1.25) |
| 4 | Vignette | off. The fall-off is painted into the set (3.1); a lens vignette of at most 4 percent is the allowed maximum |

Cost: 0.3 to 0.4 s per 720x1280 frame, one thread (measured by the colour lens). No grain, no sharpening, no chromatic aberration.

**Step 6. 2D compositor page (Chromium), layer order bottom to top:** graded plate (or true-3D frame, or flat SVG artwork) inside the camera group; multiply layer with contact and cast shadows; puppets back to front, each with its depth-matte mask and tint; foreground plate if the shot uses multiplane; effect layers (steam, Z, focus lines, rain, wave bands, flash); nothing on top except the caption, which ffmpeg burns in last. The puppets and flat SVG artwork are authored in final display colours and get no grade of their own. `mix-blend-mode: multiply` on sRGB-encoded values equals a linear multiply by the decoded colour for a pure power-law curve (the sRGB toe makes it approximate in deep shadow), which is why the shadow colours of 2.10 are given encoded.

**Step 7. Lamp-lit and night shots.** Bulbs `#fffeec` at strength 8 clip to white with a 12 to 24 px warm halo; four to six visible in a wide office shot. Night is not dark: value mean about 0.59, saturation mean 0.54, 86 percent of the frame blue-violet, small warm window accents.

**Step 8. Depth of field.** Deep focus by default (clip A). In at most two or three dialogue close-ups blur the plate layer only: Gaussian sigma 5 px (measured range 3.6 to 7 px), so the background Laplacian energy is about one tenth of the character's. Never use Cycles depth of field.

**Step 9. Motion blur.** Only on the plate layer and only on frames where the plate moves more than 40 px in one frame (snaps, crash zooms, whips). Draw the plate group 5 times at interpolated sub-frame camera transforms with opacities 1, 1/2, 1/3, 1/4, 1/5 (a uniform average, one screenshot). Characters stay sharp, as in the reference (sharp at 250 px per frame, a f1736 to f1740).

**Step 10. Captions and encode.** Work Sans Black 50 px (`PROJ/fonts/WorkSans-Black.ttf`), white fill, 4 px black stroke, soft shadow 1.5 at 50 percent, centred at x = 360, y = 900, 1 to 3 words (at most about 16 characters), 0.2 to 0.6 s each, hard swap, no animation. Burn in with ffmpeg `ass` after the dissolves so the caption keeps true black and white. Encode libx264, crf 16 to 18, yuv420p, 30 fps, `+faststart`. `PROJ/assemble.py` defaults to 24 fps: pass 30.

### 4.3 Calibration loop (do this before building shots)

1. White card: a `lit` card with albedo 1.0 facing the sun, ambient off. It must read scene-linear max(K) on the brightest channel; scale the sun energy if it does not. Same once for a point lamp.
2. One office still at 50 percent size with two puppets composited; run `measure_color.py --palette`.
3. Correct in this order: rows 15, 5, 3 with albedos; rows 13 and 19 with A (and the pale-surface A outdoors); rows 16, 17, 23 are fixed by the puppet; rows 1, 8, 12 with Saturation (1.05 to 1.25) and Offset.
4. Then the checks of 3.5.

---

## 5. Camera, staging, animation, transitions

### 5.1 Global

- 30 fps, 720x1280, on ones. 1950 frames.
- One lens for every 3D camera: `lens = 22`, `sensor_width = 36`, `sensor_fit = 'AUTO'`: focal 782 px, 49.4 deg horizontal, 78.6 deg vertical (measured on clip A: 622 to 870 px, median 787). Allowed 18 to 24 mm. v1's 32 mm flattened the floor and hid the vanishing point.
- Roll 0 always. No Dutch angles.
- bpy 5.3: `action.fcurves` no longer exists; set `bpy.context.preferences.edit.keyframe_new_interpolation_type` before keying or walk `action.layers[].strips[].channelbag(slot).fcurves` (helper in `SPEC/camera_motion.md` 3.3).

### 5.2 Distances, heights, framing (lens 22 mm; distance = 782 x D / on-screen D)

| Shot size | On-screen D | Camera to character | Head centre y | Use |
|---|---|---|---|---|
| Extreme close | 390 to 440 px | 1.8 to 2.0 D | 0.30 to 0.40 H | reaction beat, 0.4 to 1 s |
| Close | 300 to 350 px | 2.2 to 2.6 D | 0.36 to 0.51 H | one face, chest under the caption |
| Medium (default) | 170 to 230 px | 3.4 to 4.6 D | 0.45 to 0.51 H | figure 0.43 to 0.61 H tall |
| Wide | 110 to 135 px | 5.8 to 7.1 D | 0.49 to 0.57 H | figure plus place |
| Establishing | 30 to 75 px | 10 to 26 D | 0.55 to 0.60 H | place, crowd |

Camera height presets (standing subject):
- Eye level, the dialogue default: camera at head-centre height plus 0 to 0.3 D, pitched 2 to 5 deg down. Horizon at 0.40 to 0.50 H.
- Low angle, for the chief and for authority: camera 1.2 D above the floor, 4 D away, pitched 15 deg up. Horizon at 0.67 H, head centre at 0.43 H, ceiling or sky behind the head (a/t16.0).
- High angle, for wides and for a character who has lost: camera 3 to 5 D above the floor, 6 to 7 D away, pitched 5 to 15 deg down. Horizon at 0.34 to 0.44 H, head centre at 0.57 to 0.62 H.

Framing rules:
1. Head centre between y = 450 and y = 760 (0.35 to 0.59 H). No face may cross y = 880 to 930: the caption sits at y = 900 and crosses the chest in close shots, the legs in medium shots, the ground in wides.
2. Fill the area under the caption with ground that carries perspective lines to the horizon (floorboards, runner, desk edge, sand ripples, boardwalk). Never a blank lower quarter.
3. Single subject within 0.16 W of the centre line; two thirds of all main heads sit in the centre third.
4. Two-shot staged in depth, not side by side: listener nearer and lower, speaker farther and higher. Near head 210 to 310 px at x = 150 to 250, far head 150 to 230 px at x = 470 to 490 and 125 to 135 px higher; size ratio 1.36 to 1.40. In D units of the near character: 1.0 to 1.4 D apart in depth, 0.9 to 1.1 D sideways. The equal-size profile two-shot (both heads about 180 px, same height, the outer figure may be cropped by the frame edge) is for confrontation only.
5. Background figures: heads of 30 to 75 px, at least 10 D behind the principal.
6. Interior eye line (vanishing point) at 0.42 to 0.45 H; exterior horizon at 0.34 to 0.50 H.

### 5.3 Camera moves

The camera almost never rests: fully static frames are 4 to 6 percent of the reference, and static holds of 6 frames or more total about 1 s per clip. Two kinds of move exist.

Shot template (frames at 30 fps, N = shot length):

    [0 .. 5]      incoming dissolve tail, camera already moving
    [0 .. N-12]   primary move: one eased key pair, velocity reaches 0 at N-12
    (optional)    one snap of 14 to 24 frames on a narration accent
    [N-12 .. N]   near still (0 to 3 percent per second); outgoing dissolve starts at N-6

| Move | Size | Duration | Easing |
|---|---|---|---|
| Drift push-in or pull-out | 6 to 10 percent per second, total x1.15 to x1.45 or the inverse over a 2 to 3 s shot | whole shot minus 12 frames | sine in-out; cubic ease-out when the shot starts on a cut |
| Drift slide or pan | 20 to 60 px per second | same | same |
| Snap push or pull | x1.5 to x3 or the inverse, plus 150 to 700 px of pan or tilt | 14 to 24 frames | sine in-out (peak speed 1.57 x mean; measured 1.56 to 2.09) |
| Crash zoom | x3 to x10 or the inverse | 15 to 25 frames | quintic in-out, plate motion blur on |
| Whip pan | 600 to 1300 px, peak 2000 to 6000 px per second | 7 to 20 frames | sine in-out, plate motion blur on |
| Orbit or truck (true 3D only) | background slides 90 to 210 px per second, about a quarter turn in 5 to 6 s | 5 to 6 s | Bezier |
| Shake (storm, wave, train) | 5 Hz, 12 px per frame standard deviation, 86 px peak to peak | 1 to 1.5 s | random keys every 3 frames |
| Hold | 0 | 6 to 14 frames, at most three or four in the film | - |

As a 2D move on a plate: scale s(u) = s0 x (s1 / s0)^e(u) and pan p(u) = p0 + (p1 - p0) x e(u), with e(u) = 0.5 - 0.5 cos(pi u) for sine in-out. As a 3D dolly: a push of r per second at distance Z moves at r x Z (8 percent per second at 4.1 D is 0.33 D per second).

Conventions: alternate direction from shot to shot (in, out, slide); open a new scene with the bigger move and let it settle; the framing changes every 1.2 to 1.5 s over the whole film when dissolves, cuts and snaps are counted together. For this story use the calmer clip B profile: about 22 shots of 2 to 3.5 s (range 0.4 to 7.7 s), one snap in every second shot, and three or four clip A style crash moves on the big beats (the erased line, the storm accelerating, the wave).

### 5.4 Transitions

- Four of five transitions are cross-dissolves: 11 frames with a smoothstep mix (P x P x (3 - 2P)); 9 frames for quick continuity, 13 to 16 for a change of place or time. Render 6 extra frames at the head and tail of each shot; both shots keep moving through the dissolve. Blend in numpy, or with ffmpeg `xfade=transition=custom:duration=0.4:offset=<shot_end-0.4>:expr='A*(P*P*(3-2*P))+B*(1-P*P*(3-2*P))'` (verified on ffmpeg 6.1.1 by the camera lens).
- Two or three plain hard cuts, each on a line that lands like a punch.
- One or two whip pans: a 4-frame eased pan-off, then a 4-frame pan-on in the same direction, plate blurred.
- One object wipe: something large crossing the lens (the wave).
- One flash: 5 frames to white on the impact.
- One punch-in cut with focus lines for a shock (b f146 to f147).

### 5.5 Character animation

1. Bodies move by smooth eased interpolation on ones; faces change by instant swap. Never tween between two face drawings. The ink does not boil.
2. The speaker moves, the listener freezes. Speaker: one lean or nod every 1.0 to 1.5 s, head 0.15 to 0.30 D sideways and 0.08 to 0.15 D vertically, eased over 8 to 12 frames, with a new head roll of 10 to 20 deg; the torso follows at half amplitude. Listener: under 0.04 D of travel, blinks only, mouth still.
3. Blink = half, closed, half, one frame each (the closed frame may hold two). Every 0.7 to 1.2 s in close-ups, about every 2 s otherwise, and at every change of thought; offset the timing between characters; skip blinks inside a short line.
4. Every change of expression is hidden behind a blink: swap eyes and mouth on the closed frame. One to three swaps per second during a reaction. Optional 2 to 3 frame squash of 0.03 D on the swap.
5. Mouth: only on the character whose line the narrator is voicing. Cycle the four talking drawings, a new drawing every 2 to 6 frames (about 7 per second; measured 4.9 to 9.8), driven by the narration loudness: 33 ms RMS against its running median, lag 0 to 1 frame; silent = bar, low = half open, high = wide open (held up to 4 frames), "oo" or "w" = round. Eyes and brows hold still while talking. Phoneme accuracy is not needed (measured correlation with loudness 0.36 to 0.57).
6. Walk: head bob 0.47 D peak to peak, period 0.68 s (20 frames), sideways sway 0.13 D, legs alternating on the same period, near-profile view.
7. Entrances: pop up or slide in from the frame edge over 4 to 8 frames, then small nods.
8. One gesture per shot (an arm raise, a point, the eraser wipe), eased over 8 to 10 frames and timed to the caption word.
9. Jump scare: squash blink 2 frames, leap 2, hang 2, land 2.

---

## 6. Render-cost budget

### 6.1 Measured anchors

- v1, full 3D per frame: 16.2 s per frame on these 4 cores (`PROJ/render/office/anim.log`). 1950 frames would take 8.8 hours, and every acting change would cost it again. Even an optimistic 6 s per frame is 3.25 hours per take.
- 2D composite in Chromium: 0.33 s per frame as PNG, 0.09 s as JPEG q95, single process (section 0). 1950 frames take 11 minutes in one process; three parallel pages should bring that to about 4 minutes (not measured).
- Compositor grade: 0.3 to 0.4 s per frame (colour lens).

### 6.2 Recommendation: layered stills with 2D camera moves, true 3D only for a few signature moves

Four shot tiers:

| Tier | What Cycles renders | Camera move | Share of screen time |
|---|---|---|---|
| F, flat | nothing: full-frame SVG artwork (map, newspaper, telegram, storm diagram) | 2D pan and zoom | about 10 percent |
| P, plate (default) | one still per camera setup plus its depth plate | 2D zoom and pan of plate and puppets together, as 43 percent of clip B does | about 65 percent |
| M, multiplane | P plus one or two foreground layers rendered separately with `film_transparent` (other objects `visible_camera = False` so they still cast shadows) | each layer scaled about the frame centre by s = d / (d - delta) for its own depth d and a virtual dolly delta; the puppet uses its own depth | about 15 percent |
| T, true 3D | the set only, every frame, no characters | real camera animation; puppets follow through the exported per-frame anchors; a T move always starts or ends on a plate camera so it can hand over to a P plate with a 3-frame mix | at most 8 s (240 frames) |

Plate sizes: 1080x1920 (1.5 x) for shots whose 2D zoom stays within x1.5; 1440x2560 (2 x) for shots with a snap. Beyond the plate's native scale, either accept soft pixels for the few blurred frames at the peak of a snap, or hand over to a second, tighter plate inside the snap.

Budget for one full build (plate and true-3D costs are estimates scaled from the v1 measurement; they must be gated, see 6.3):

| Stage | Unit cost | Count | Total |
|---|---|---|---|
| SVG textures and flat artwork | 0.3 to 1 s each | about 60 | 1 min |
| Plates with depth plates | about 40 to 60 s at 1.5 x, 65 to 110 s at 2 x (estimate) | 16 setups, plus about 6 foreground layers at 15 s | about 22 min |
| True-3D set frames | target 6 s or less (estimate) | at most 240 | at most 24 min |
| 2D composite | 0.33 s (measured) | 1950 plus 22 x 12 dissolve handles, about 2210 | 12 min in one process (about 4 min expected on three pages) |
| Dissolves, captions, encode | - | - | 2 to 3 min |
| Total | | | about 60 min |

Targets: **an average of 2 s or less per final frame over the whole build (65 minutes for 1950 frames); hard ceiling 3 s (100 minutes); an animation-only retake (no Cycles) in 12 minutes or less.** Per tier: F and P frames 0.5 s or less each after their one-off plate; T frames 6 s or less.

### 6.3 Gates

1. Time three frames of the first T shot. Over 6 s: drop Freestyle if it was on, go to 12 samples without the denoiser (the ambient is noise-free emission, only sun penumbrae need samples), then render at 540x960 and upscale with Lanczos (T shots are fast moves), then convert the shot to M.
2. Time the first plate. Over 120 s at 2 x: use 1.5 x and split snaps over two plates.
3. Cap T at 240 frames in the film.

### 6.4 Compositor implementation notes (checked in this session)

- One HTML page per shot; load plates as `<image>`; step frames with `page.evaluate(setFrame, i)` and screenshot each one. No CSS animation, no timers, no randomness without a fixed seed.
- Write the HTML to disk and open it with `page.goto('file://...')`. A page created with `page.setContent` cannot load `file://` images: the plate silently becomes a broken image (this happened in my first run).
- Viewport 720x1280, device scale factor 1. PNG encoding is the bottleneck (0.33 s against 0.09 s for JPEG q95); run three pages in parallel or write JPEG q95 intermediates.

---

## 7. Changes from v1, ranked by the likeness they buy

| Rank | Change | How | Expected gain |
|---|---|---|---|
| 1 | Replace the lit 3D characters with the flat SVG puppet | sections 2.2 to 2.8: unlit `#fef7f6` head with one lavender crescent, thick-thin plum ink 0.02 to 0.066 D, rounded torso 0.57 to 1.00 D wide with gradient and 5 to 7 costume elements, rubber-hose limbs 0.062 D with ball hands and stub feet, height 2.9 to 3.4 D, half-lid default eye 0.178 D wide (v1: 0.05 D dots), eye spacing 0.26 D (v1: 0.15), hats covering the top quarter of the head, hair patches | the largest single step: removes the "3D render" read. Fixes target rows 16, 17, 23 by construction |
| 2 | Rebuild the set dark, saturated, patterned and full | section 3: no large pale surface (wall value 0.61 with saturation 0.47 instead of 0.88 / 0.16), one cool block, drawn pattern on every surface, 20 to 26 inked props, visible glowing lamps, dark top and bottom | edge density 0.016 to about 0.06, featureless area 0.64 to 0.30 or less, rows 3, 5, 9, 15 into range (mock-up: S mean 0.41, luma p50 0.26, 34 percent of pixels above S 0.5) |
| 3 | Direct the camera | section 5: 30 fps, 22 mm, staging in depth (size ratio 1.36 to 1.40), a framing change every 1.2 to 1.5 s, eased drifts and snaps, 11-frame smoothstep dissolves, low, eye and high camera heights | removes the "parked camera" read; v1 was one linear 0.63 m dolly at 24 fps |
| 4 | Animate the faces and the acting | section 5.5: three-frame blinks, expression swaps behind blinks, loudness-driven mouth every 2 to 6 frames, head rolls of 10 to 20 deg, speaker moves and listener freezes | v1 had one face swap and one arm rotation in 3 s |
| 5 | Light and grade for plum shade and warm light | section 4.2: emission ambient plus one hard sun (angle 1.5 deg), no fill, bloom on real emitters only, CDL offset to a plum black point, saturation 1.12 | rows 12, 13, 19 to 21; small next to items 1 and 2 (the grade alone moved v1's saturation mean only from 0.29 to 0.34) |
| 6 | Move to the layered pipeline | section 6: plates, depth-matte occlusion, puppet and camera in 2D | makes items 3 and 4 affordable: about 1 hour per build instead of 8.8 hours, retakes in minutes |
| 7 | Ground the characters | section 2.10: contact shadow always, projected hard shadow in sun, occlusion behind furniture | removes the pasted-on look; v1 characters cast no readable shadow |
| 8 | Typeset the story props and inserts | section 3.4: the map as a framed hero prop with two legible labels and a saturated storm track, calendar, sign, newspaper and telegram as SVG with period faces, pushed-into inserts | the reference tells its story through readable props; v1's pastel map merged with the wall |
| 9 | Add the cartoon effects | section 2.9: sweat drop on the temple, steam, purple face, focus lines, brightness dip, layered wave and rain | supplies the gag beats the reference relies on (a sweat drop alone appears in 10 of the sampled stills) |
| 10 | Captions | section 4.2 step 10: Work Sans Black 50 px, 4 px stroke, y = 900, hard swap | v1 used DejaVu Sans Bold 46 with a pop-in at y = 915 |

---

## 8. Contradictions between the analysts, how I resolved them, and open questions

### 8.1 Contradictions and resolutions

| # | Disagreement | Resolution, and what I looked at |
|---|---|---|
| 1 | Production method. Forensics: conventional render, 88 percent. Environment: mirrored chalk and unreadable small text "suggest generated footage". Camera: "shots look like separately generated 2 to 8 s clips". Anatomy: "shapes drift slightly between frames". | Forensics stands. On a/t40.0 I read the caliper digits 0 to 16 in order and "CALENDAR for the Year 1880 / MAY"; on a/t46.5 the same crate shows "JULY", its lid lettering and the chalk mark are whole, geometrically flipped words. Clean mirroring is a UV bug, not garbling. The "drift" claim is contradicted by the face lens's measurement (outline profile correlation 0.99 to 1.00 over 16 frames): no boil. |
| 2 | Are clip A characters flat 2D cut-outs (anatomy, face, colour) or 3D proxies (forensics)? | Both are partly right. a/t14.5, a/t19.0 and the hat crops show volume behaviour (bowler from above, hair wrapping the back of the head), so "they never foreshorten" is too strong. But the head is view-invariant, the face is a flat sliding drawing, and clip B characters are flat. Decision in 2.1: a 2D puppet with pseudo-3D parameters. |
| 3 | Outline. Forensics: uniform 4.2 to 5.7 percent of D, attached hull. Anatomy and face: thin left, thick lower right, 2 to 6.6 percent. | Thick-thin. My ray measurement on a/t16.5 gives 0.021 to 0.026 D on the left and 0.069 to 0.073 D on the lower right; on a/t46.5 0.035 D at 3 o'clock rising to 0.065 D at 60 deg. Forensics averaged the thick side. Use the face lens's angular table. |
| 4 | Ink colour: `#3d2933`, `#3a2832`, `#3a2a30` against the colour lens's `#2b1e2a`. | The first three are stroke-centre samples of the displayed frame (mine: `#402834`, `#452f3a`); the last is a pre-grade artwork value for cards rendered inside Blender. Puppets are composited after the grade, so use `#3a2832`. Use `#2b1e2a` only in the card fallback. Same logic for the head: `#fef7f6` in the compositor, `#fcfafa` for a card. |
| 5 | Head shading: radial rim gradient all round (anatomy) against one crescent on the lower right only (face). | Crescent. Visible on a/t46.5; my sample of the lower-right rim is `#eadded` against `#fdf8f6` at the centre. |
| 6 | Three-quarter and profile slide: up to 0.14 D (face) against 0.25 to 0.30 D for near-profile (anatomy). | 0.14 D maximum. a/t16.5 measures -0.135, a/t03.0 (the anatomy lens's near-profile example) -0.11 to -0.125. Profile is conveyed by hair, hat and body. |
| 7 | Cap size: 0.85 x 0.31 D (anatomy) and its prototype looked small. | 0.90 x 0.34 D, 12 to 14 stripes 0.034 D wide (a/t46.5 measures 0.95 x 0.36). |
| 8 | Office style. Environment: clip B treatment, inked, painted light, no hard shadows. Colour: hard sun through the window, characters casting hard shadows, no pale paper. | Clip B drawing plus one hard sun patch and lamp bloom. Characters get a soft contact shadow everywhere and a projected hard shadow only inside the sun patch. a/t32.5 confirms hard character shadows in clip A; b/t24.5 confirms none in clip B. |
| 9 | The colour lens's own target 19 (cast shadow hue 230 to 270 on a warm floor, V ratio 0.35 to 0.60) against its `INTERIOR_DAY` preset. | They are incompatible: I computed the preset on a warm plank (sun `#915c3b`, shade `#6a4640`: hue 9 deg, V ratio 0.73). With a nearly neutral ambient the shade keeps the surface hue. Row 19 is kept for exteriors (where `EXTERIOR_NOON` gives it) and replaced indoors by palette, grade and puppet-shadow colour. |
| 10 | Office palette. Colour: mauve plaster, navy-plum floor, steel-violet cabinets. Environment: orange-brown wallpaper, wood planks with a navy runner, green cabinets. | Environment's structure and props, colour's hue logic: rose wallpaper `#9c5257` (the orange-brown merged with the mustard waistcoat in my mock-up), plum-brown planks with a wider runner (3.4 D), steel-violet cabinets (green stays an accent, it is 1 percent of the reference and the hero is teal). Measured on the mock-up: table 4.1. |
| 11 | Albedo or display colour. The colour lens lists albedos that display much darker; the environment lens lists colours as if displayed. | One rule: author the ambient-lit display target T, compute albedo = ungrade(T) / A (3.1). Environment hexes are treated as T. Bright paper cannot be reached under ambient, so paper, map and dials are `painted` and capped at value 0.92 (the colour lens's point that nothing large may be pale is kept: the wall map is toned down to `#cdb98f` / `#86aec6`). |
| 12 | Noon ambient on pale surfaces. Nobody flagged it. | `EXTERIOR_NOON` gives `#406ebc` in the shade of a cream wall. Added a pale-surface ambient (0.22, 0.28, 0.55), predicted `#7988a1`. |
| 13 | Dissolve length: 5 to 9 frames (forensics) against 9 to 17, median 11 to 13 (camera). Shot counts 14 / 19 against 16 / 22. | Camera lens: it fitted the mix curve frame by frame (smoothstep, whose tails are invisible to a difference metric) and found the hidden cuts. 11 frames, smoothstep. |
| 14 | Mouth rate: a new drawing every 1 to 3 frames (face) against every 3 to 5 frames, about 7 per second (camera) and 2 to 4 (forensics). | About 7 per second, hold 2 to 6 frames: the camera lens's explicit count is 12 states in 48 frames. |
| 15 | Expression change: hidden behind a blink (face) against instant swap with optional squash (camera). | Compatible: swap on the closed frame of a blink. |
| 16 | Lens: 18 to 20 mm from floor tiles (environment, 30 percent error) against 22 mm from seven vanishing-point fits (camera). | 22 mm. |
| 17 | Vignette: none, do not add (colour) against a painted plum vignette and floor fall-off in the prototype (environment). | Compatible: the fall-off is painted into the set under the characters; the lens vignette is off. |
| 18 | Background blur in close-ups: sigma 5 to 7 px (colour), 3.6 px (environment), "6 to 8 px radius" (camera). | Sigma 5 px on the plate layer, tuned to a Laplacian ratio of 0.1; two or three shots only. |
| 19 | Motion blur: "not needed for the look" (colour) against "on every fast move" (camera, forensics). | Plate-only blur on frames moving over 40 px; characters never blurred. |
| 20 | Hero hair: `#9b6d49` (anatomy) against `#634025` (face). | `#603e25`; my sample on a/t46.5 is `#5f3d24`. |
| 21 | Limb stroke: 0.065 D (anatomy) against 0.060 in the in-progress `PROJ/v2/puppet/puppet.py`. | 0.062 (median of the measured 0.055 to 0.075); 0.070 on the stout build. |
| 22 | Head roll: -19 to +30 deg in use (face) against +/-5 to 15 (anatomy) and "a few degrees" (camera). | +/-8 at rest, 10 to 20 on a phrase accent, 30 for an extreme. |

### 8.2 Open questions

1. The Sun and point-lamp energy formulas have never been confirmed by a render. The white-card test of 4.3 settles it in one frame.
2. Plate and true-3D render times with the new light kit are estimates scaled from v1's 16.2 s. Gates in 6.3.
3. The depth-matte occlusion (2.10) and the 5-tap plate motion blur (4.2 step 9) are designs, not yet run. Fallbacks: a separately rendered foreground plate; a directional `feGaussianBlur`.
4. The mock-up still misses three targets before grading: colourfulness 48 (target 55), saturation of the darkest tenth 0.28 (target 0.35), mid-band value 0.35 (target 0.40). The saturation 1.12 grade, the sun patch and stronger red and brass accents should close them; confirm on the first graded still.
5. The pale-surface ambient and every predicted shade colour in 3.3 are computed with my grade model, not rendered.
6. `LATE_AFTERNOON`, `SUNSET`, `NIGHT` rest on two or three sample pairs each. The grey-drizzle and storm palettes, the sea, the rain and the wave are extrapolations: the reference has no such scene.
7. The top of the head outline has never been seen without a hat; the values from 210 to 330 deg are assumed. The hat pitch model is my construction.
8. Whether clip A characters are true 3D rigs or drawn views cannot be decided from pixels. It does not block the build.
9. Mouth animation needs the narration audio (loudness envelope). Until it exists, drive the mouth from the caption word timings.
10. The crescent sits at 50 deg on most heads but nearer 100 deg on a/t14.0 and a/t20.0; no rule was found. Keep 50 deg.
11. The period fonts are reachable on npm but not installed. The script's last image (the forecast on the kitchen table) has no set design from any analyst; treat it as a flat insert or a small plate built with the office rules.
12. Freestyle or inverted hull for set ink on plates: the hull is specified as primary because it is identical in plates and true-3D frames; check hull artefacts on concave props on the first plate.

---

## Appendix. Reusable code and build order

Reusable, already written: `SPEC/face_proto/faces_ref.py` (faces, verified), `SPEC/character_puppet_proto.py` (body), `PROJ/v2/puppet/puppet.py` (production puppet in progress, same conventions as section 2), `SPEC/lightkit_clp.py` (presets and materials), `SPEC/grade_compositor.py`, `SPEC/measure_color.py`, `SPEC/env_proto/gen_styleframes.py` (per-surface SVG generators), `SPEC/face_proto/raster.js` (Playwright rasteriser; `NODE_PATH=/opt/node22/lib/node_modules`), `PROJ/assemble.py` (pass fps 30), `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/lookdev_tmp/bench.js` (frame-stepped compositor loop), `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/lookdev_tmp/pal.py` (target-to-albedo and shadow-colour calculator).

Build order:
1. Calibration (4.3): white card, then one office plate at 50 percent with two puppets; measure against 4.1 and 3.5.
2. Puppet module to the numbers of section 2; contact sheet of the 20 expressions and the five views; compare with a/t46.5, a/t16.5, b/t24.5 side by side.
3. Office set and its plates (DAY, GREY MORNING, LAMP); beach set and its plates (SUNNY, DRIZZLE, STORM); depth plates; timing gates of 6.3.
4. Flat inserts (map, newspaper, telegram, storm diagram).
5. Shot list of about 22 shots with tier, plate, camera keys, puppet poses and face tracks; export per-frame anchors.
6. Compositor pass, dissolves, captions, encode; re-measure three stills per set.
