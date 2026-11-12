# Character construction and anatomy spec (lens: character anatomy)

Reference: clip A "Why Perfect Railroads Don't Work" (`ref/a/tSS.S.jpg`), clip B "The Ancient Jar That Warned an Empire" (`ref/b/tSS.S.jpg`), 720x1280.
All pixel values are in the 720x1280 frames. `D` = head diameter (outer, including outline; for clip B the head WIDTH). Positions written as `(x, y)` in D units are relative to the head centre, +x to screen right, +y DOWN.
Evidence crops and measurement scripts: `ref/crops/anatomy/` (`meas.py`, `grid.py`, `G_*.jpg` gridded crops, `sheet*.jpg` contact sheets). Extra 30 fps frames: `ref/extra/anatomy/`.
Prototype of recipe (b), already rasterised with Chromium: `spec/character_puppet_proto.py`, `spec/character_puppet_proto.png`, side-by-side with reference and v1: `spec/character_puppet_proto_compare.jpg`.

Measurement accuracy: JPEG/video compression blurs edges by about 1-2 px, and the artwork itself changes by roughly 5-10 percent between shots (cap height, torso length, head roundness are not constant). Treat ratios as +/- 0.03 D. Where a value was read from a gridded crop instead of computed, it is marked "(grid)".

---

## 1. Observations

### 1.1 Overall read: flat 2D ink-and-fill cut-outs, not shaded 3D
- Characters are drawn artwork: a dark hand-inked contour with visible wobble and thick-thin variation, flat colour fills, thin inner detail lines, a few painted highlights. They sit in front of fully rendered/painted environments (A t02.0, t16.0, t44.0; B t03.0, t22.0).
- Evidence against 3D shading: the head is flat white with only a faint lilac rim (A t16.0 centre `#fdf8f6`, bottom rim `#eedfec`, right rim `#f0e4ed`; A t55.0 top `#fcfbf7`, bottom `#ecdeed`); there is no terminator, no specular, no ambient occlusion where head meets torso. The bowler highlight is a painted grey streak (`#cac8e2` on `#463f4e`, A t16.0), identical in shape regardless of the sun position in the scene.
- Evidence of soft 2D shading (so it is not pure flat vector either): torsos carry a left-to-right airbrush gradient, light on the left, dark on the right: boss waistcoat `#ddba4f` -> `#c79d2d` -> `#936e1e` (A t44.0), hero vest `#43ceb4` -> `#3dbda6` -> `#2e8678` (A t55.0), inventor robe has a pale highlight stripe just inside the left edge `#90a7cc` on `#4b76b9` (B t03.0). The waistcoat also has a faint dot pattern (A t44.0).
- Characters are tinted by the scene grade as a whole: night scenes turn the white head lilac (`#a888b0` B t44.5, `#b8aee7` B t42.0) and the ink dark indigo (`#1b1534` B t42.0). Extreme close-ups are defocused with bokeh (B t21.0).
- They never foreshorten like a 3D body: in low-angle and high-angle shots the figure stays a frontal drawing parallel to the screen (A t16.0 low angle, B t33.0 high angle). Depth is suggested only by scale, overlap and by swapping to a different drawn view.
- No held frames: all 12 consecutive 30 fps frames sampled at A t15.9-t16.3 differ in the character region (`ref/extra/anatomy/a16_*.jpg`), so motion is not visibly stepped on twos. The camera moves at the same time, so character motion and camera motion could not be separated.
- Cannot be determined: whether the source is a vector rig or generated video. Shapes drift slightly between frames, so a builder should match proportions and line character, not pixel-exact shapes.

### 1.2 Head
- A near-circle. Clip A is circular within about 2 percent: circle fits to the visible lower arc give rms 1.65-1.88 px at R about 88-92 px (A t02.0, A t16.0), and chord widths on A t55.0 give the same centre from three rows (cy 290.4, 291.5, 292.7 for R = 174.5 px).
- Clip B heads are wider ovals and usually tilted: inventor B t03.0 outer about 234 x 208 px (W/H 1.12, fitted ellipse of the white area 207 x 221 px rotated, minor/major 0.93); guard B t42.0 about 202 x 186 (1.09); emperor B t22.0 about 321 x 257-275 (1.17-1.25, top hidden).
- No neck. The head overlaps the top of the torso by 0.10-0.15 D; the torso outline simply disappears behind the head (A t16.0, B t03.0). The head is free to tilt (+/- 5 to 15 degrees is normal) and to slide off the torso axis when a character leans (A t14.0, A t15.0, B t06.0).
- No nose, no ears, ever.

### 1.3 Outline (ink)
- Colour is a dark warm plum, neither pure black nor navy: centre of thick strokes `#382731`, `#3a2932`, `#382630` (A t44.0), `#3c2129`, `#372228` (B t21.0). Use `#3a2832`.
- Limbs are drawn with the same ink, so legs/arms/hands and the contour are one colour.
- The head contour is thin on the upper-left and thick on the lower-right, in both clips: A t16.0 3.5-4 px (left) to 7-12 px (right, lower-right) at D = 191; A t55.0 10 px to 16.5-17 px at D = 349; B t03.0 2-6 px to 16-18 px at W = 234; B t22.0 6 px to 22-25 px at W = 321.
- The torso contour is thinner than the head contour and much thinner than the limbs: 4 px on hero A t02.0, 4-5 px (left) and 9 px (right) on boss A t16.0.
- Inner detail lines (V-neck, pocket boxes, button rings, strap stitching) are thinner again: about 5 px at D about 310 (A t44.0), about 3 px at D = 191 (A t16.0).
- Line edges are slightly irregular (felt-pen wobble), not mathematically clean.

### 1.4 Torso
- One closed rounded shape, no shoulders, no waist. Three body types appear:
  - slim "pill": hero (A t02.0, A t55.0), newspaper kid, workers. Straight, nearly parallel sides, fully rounded bottom.
  - regular egg: tycoon (A t27.0), clip B capsules (B t03.0, B t42.0).
  - stout egg/pear: boss (A t16.0, A t44.0). As wide as the head, widest in the lower half.
- The bottom 0.14 D is a separate dark "trouser bowl" (hero `#624b44`/`#3e2b32`, boss `#45404d`), divided from the garment by an ink line; legs come out of it (A t02.0, A t16.0, A t44.0).
- Clip B replaces trousers with a long robe skirt: a trapezoid drawn behind the capsule, hem wider than the top, with its own outline (B t03.0, B t22.0, B t42.0).

### 1.5 Limbs, hands, feet
- Arms and legs are single ink strokes of constant width with round ends: "rubber hose". No anatomy, no sleeves.
- Arms start at the top corners of the torso, exactly where it emerges from behind the head. Elbow at mid-length. Relaxed arms are smooth arcs (both arms akimbo, A t44.0); gesturing arms have a soft V elbow (hand on hip A t16.0; pointing B t03.0).
- Legs start under the trouser bowl. Standing legs are straight or very slightly bowed with no knee (A t16.0, A t44.0); knees only appear when sitting, walking or crouching, then as a clear bend at mid-length, folded into a Z when squatting (A t58.0, A t37.0, A t13.0).
- Hands are a filled ink ball about twice the stroke width (A t16.0, A t44.0). Fingers are added only for a gesture: one stroke for a pointing index (B t03.0), three or four short strokes for an open hand (A t20.0), a small bump for a thumb or pinky when holding a cup (A t28.0). Sometimes a 1-2 px white speck highlight sits on the ball (A t44.0, A t21.0).
- Feet are not shoes. Clip A: the leg stroke turns into a short stub at the ankle (A t21.0), often half lost in the ground. Clip B: a short horizontal bar under the leg, giving an inverted T or L (B t03.0, B t42.0).

### 1.6 Hats and hair (hats replace the top of the head, they are not perched on it)
- Bowler (boss A t16.0, A t46.0; grey variant on the newspaper kid A t32.0): dome plus curled brim, drawn over the top quarter of the head; the brim front dips to the eyebrows, which touch it. Painted highlight arc on the upper left of the dome.
- Striped engineer cap (hero A t02.0, A t55.0): low puffy dome, slightly narrower than the head, with white stripes fanning from a top button, a dark band and a short grey-blue visor. It covers the top 26-36 percent of the head and adds almost no height.
- Top hat (tycoon A t27.0, A t28.0, A t53.0): tall black cylinder, thin flat brim, gold band.
- Peaked cap (foreman A t23.0): flared flat-topped navy crown, gold double band with badge, black visor; tilts with the head.
- Emperor crown (B t22.0, B t24.0): small dark cap base on top of the head, a long thin board across it tilted about 8 degrees, gold bar, two short columns of coloured beads hanging at each end.
- Guard helmet (B t42.0): the top 35 percent of the head outline recoloured grey-blue with ridge lines, a tan rim band slightly wider than the head, a cheek plate on one side, a red plume.
- Inventor hair (B t03.0): black hair band along the top arc, a striped bun above it, gold hairpin with a green bead.
- Court official cap (B t23.0, B t28.0): black wedge rising to a point at the back, tan base band. Estimated from small figures only.
- Hair patches: flat coloured crescents lying inside the head contour directly under the hat, with no ink line on their inner edge: hero brown `#9b6d49` on both temples in front view (A t55.0), boss grey on one side (A t14.0, A t46.0). Old workers get a white beard drawn over the lower face (A t13.0).

### 1.7 Costume detail (all drawn as thin ink line plus flat fill inside the torso shape)
- Hero (A t02.0, A t55.0): teal vest `#3dbda6`; red bandana triangle `#af2d3d` with pale dots hanging from the chin; two dark brown suspender straps `#483a38` with a dashed stitch line and small gold buckles at both ends; two pale round buttons on the centre line; one outlined pocket rectangle; brown trouser bowl.
- Boss (A t16.0, A t44.0): mustard waistcoat `#c79d2d`; white shirt V `#e7dcdb` with a grey centre line; five gold buttons `#d7c374` with ink rings on the centre line; watch chain of overlapping small gold ovals hanging in a curve from the second/third button to a fob at the side; three olive welt pockets `#8e6f2c`; cane with gold ball `#b9963f`.
- Tycoon (A t27.0): purple suit `#885285`, V with dark tie, two buttons, two welt pockets, teacup.
- Foreman (A t23.0): navy coat `#2f4171`, gold buttons, black belt with gold buckle.
- Inventor (B t03.0): blue robe `#5078bb`, white crossed collar bars, gold sash `#e0b05c`, darker blue skirt `#20346e`.
- Emperor (B t22.0): dark purple robe `#462c3b`, red and gold crossed collar `#bc372d` / `#f3b862`, thin gold line and red belt.
- Guard (B t42.0): armour capsule of small grey-blue tiles, red belt with yellow buckle, dark red skirt.

### 1.8 Views
- Five yaw states are used: front, three-quarter left/right, near-profile left/right. No back view was found in the sampled frames.
- The head stays a full circle in every view. Turning is shown by sliding the face toward the facing side (both eyes always remain visible, even in near-profile, A t19.0, A t03.0), by letting one hair patch grow into a large back-of-head shape covering a quarter to a third of the head (A t03.0, A t19.0, A t20.0), and by pointing the cap visor past the head contour.
- The torso narrows a little and its centre details move to the facing edge: one suspender and the button row sit near the front edge in near-profile (A t19.0); the boss's button row and chain shift and curve in three-quarter (A t14.0, A t46.0).
- Front: A t02.0, A t16.0, A t55.0, B t17.0, B t24.0. Three-quarter: A t14.0, A t20.0, A t46.0, B t03.0, B t22.0, B t25.0. Near-profile: A t03.0, A t19.0, B t23.0, B t44.5.

### 1.9 Pose catalogue
| Pose | Frames |
|---|---|
| Standing, both hands on hips / arms akimbo | A t02.0, A t44.0 |
| Standing, one hand on hip, other on cane | A t16.0, A t16.5 |
| Standing neutral, arms hanging along the torso | A t55.0, A t56.0, B t24.0, B t28.0 |
| Leaning in toward camera, torso tilted 35-45 degrees, head thrust forward | A t14.0, A t15.0, A t15.5 |
| Shouting, body arched back, fist on hip | A t17.0, A t18.0, A t18.5 |
| Walking / striding in near-profile, knees bent, legs scissored | A t03.0, A t19.0, B t44.0, B t45.0 |
| Arm extended forward, handshake / offering | A t19.5, A t20.0, A t20.5 |
| Pointing or reaching with one straight arm | A t21.0, B t03.0, B t04.0, B t41.0-t43.0 |
| Arm raised to hat / head | A t12.5, A t37.0 |
| Sitting on an edge, legs dangling with bent knees | A t12.0, A t13.0 |
| Sitting in a chair, legs crossed, holding cup | A t27.0, A t28.0, A t53.0, B t22.0 |
| Kneeling / squatting, legs folded in a Z | A t37.0, A t45.0, A t58.0, A t59.0 |
| Holding a large prop in front of the body with both hands | A t32.0, A t33.0, A t35.0 |
| Laughing, head thrown back or tilted, body curved | B t06.0, B t07.0, B t23.0 |
| Whole body tilted about 25 degrees | A t23.0 |
| Head only (window) | A t29.0, A t30.0 |

---

## 2. Measurements

### 2.1 Head, outline, colours
| Quantity | Value | Frame |
|---|---|---|
| Head outer D, hero medium shot | about 190 px (inner circle fit R 92.1, rms 1.88 px) | A t02.0 |
| Head outer D, boss medium shot | 191 px (x 256-446) | A t16.0 |
| Head outer D, hero close shot | 349 px (x 162-510) | A t55.0 |
| Head aspect W/H, clip A | 1.00-1.05 (circle fit rms 1.65 px at R 87.6) | A t16.0 |
| Head aspect W/H, clip B inventor | 1.12 (outer about 234 x 208 px; white area 223 x 200) | B t03.0 |
| Head aspect W/H, clip B inventor | 1.06 (white area 261 x 246) | B t04.0 |
| Head aspect W/H, clip B guard | 1.09 (about 202 x 186 px) (grid) | B t42.0 |
| Ink colour | `#382731`, `#3a2932`, `#382630` | A t44.0 |
| Ink colour | `#3c2129`, `#372228` | B t21.0 |
| Ink colour at night | `#1b1534` | B t42.0 |
| Head fill centre / bottom rim / right rim | `#fdf7f7` / `#eedfec` / `#f0e4ed` | A t16.0 |
| Head fill top / bottom rim | `#fcfbf7` / `#ecdeed` | A t55.0 |
| Head fill centre / right rim | `#f8faf3` / `#f3edfa` | B t03.0 |
| Head outline width, left to right | 3.5-4 px to 7.2-11.8 px = 0.018-0.062 D | A t16.0 |
| Head outline width, left to right | 10 px to 16.5-17.2 px = 0.029-0.049 D | A t55.0 |
| Head outline width, left to right | 2-6 px to 16-18 px = 0.01-0.075 D | B t03.0 |
| Head outline width, left to right | 6 px to 22-25 px = 0.02-0.078 D | B t22.0 |
| Torso outline width | 4 px = 0.021 D | A t02.0 |
| Torso outline width, left / right | 4-5 px / 9 px = 0.02-0.047 D | A t16.0 |
| Torso outline width | 9-10 px at D about 310 = 0.03 D | A t44.0 |
| Torso / skirt outline width | 4-7 px / 10 px = 0.02-0.043 D | B t03.0 |
| Inner detail line (V-neck) | 5 px at D about 310 = 0.016 D | A t44.0 |

### 2.2 Torso
| Quantity | Value | Frame |
|---|---|---|
| Boss torso width down the body | 155 px at shoulder line, 176, 182, 190 (max), 187, 176 px, bottom at y 795-798 | A t16.0 |
| Boss torso max width | 190 px = 0.99 D | A t16.0 |
| Boss torso visible height (chin y 620-628 to bottom y 795-798) | 167-178 px = 0.87-0.93 D | A t16.0 |
| Boss torso width, close shot | 310 px (x 205-515) | A t44.0 |
| Hero torso width | 110 px = 0.58 D | A t02.0 |
| Hero torso visible height | 163 px = 0.86 D (garment 0.71 D + trouser bowl 0.14 D) | A t02.0 |
| Hero torso width / height, crouched | 187 px = 0.54 D / 252 px = 0.72 D | A t55.0 |
| Tycoon torso width / height | 100 px = 0.78 D / 120 px = 0.94 D (grid) | A t27.0 |
| Inventor capsule width / visible height | 152 px = 0.65 D / 221 px = 0.94 D (grid) | B t03.0 |
| Inventor skirt length, top width, hem width | 275 px = 1.18 D, 172 px = 0.74 D, 210 px = 0.90 D (grid) | B t03.0 |
| Guard capsule width | about 120 px = 0.6 D | B t42.0 |
| Trouser bowl height | 26-28 px = 0.14-0.15 D | A t02.0, A t16.0 |
| Torso shading, left / centre / right | `#ddba4f` / `#c79d2d` / `#936e1e` | A t44.0 |
| Torso shading, left / centre / right | `#43ceb4` / `#3dbda6` / `#28897a` | A t55.0 |

### 2.3 Limbs, hands, feet
| Quantity | Value | Frame |
|---|---|---|
| Leg stroke width, hero | 10-13 px = 0.055-0.065 D | A t02.0 |
| Arm stroke width, hero | 10-13 px = 0.055-0.065 D | A t02.0 |
| Leg stroke width, boss | 13-17 px = 0.07-0.08 D | A t16.0 |
| Leg stroke width, boss close | 18-22 px at D about 310 = 0.058-0.07 D | A t44.0 |
| Leg stroke width, hero close | 14-16 px = 0.04-0.046 D | A t55.0 |
| Arm stroke width, guard | 12 px = 0.06 D | B t42.0 |
| Arm stroke width, inventor | 13-15 px = 0.055-0.064 D | B t03.0 |
| Arm length, shoulder-elbow-hand | 69 + 67 px = 0.71 D | A t16.0 |
| Arm length | 66 + 80 px = 0.77 D (grid) | A t02.0 |
| Arm length | 76 + 108 px = 0.79 D (grid) | B t03.0 |
| Leg length | 203 px vertical, 215 px along the stroke = 1.07-1.13 D | A t02.0 |
| Leg length | about 290 px = 1.52 D | A t16.0 |
| Hip spacing (leg centres) | 85 px = 0.45 D (legs at the torso's bottom corners) | A t02.0 |
| Hip spacing | 52 px = 0.27 D; 96 px = 0.31 D | A t16.0; A t44.0 |
| Hand ball diameter | 26.0 px and 24.8 px = 0.13-0.136 D | A t16.0 |
| Hand ball diameter | 43.6 px = 0.14 D | A t44.0 |
| Fist diameter (plus index stroke) | 16 px = 0.07 D | B t03.0 |
| Foot bar length | 56 px = 0.24 D (grid) | B t03.0 |
| Foot stub length | about 0.2 D (grid, +/- 0.05) | A t21.0 |

### 2.4 Hats (positions relative to head centre, D units, +y down; head top is y = -0.50)
| Quantity | Value | Frame |
|---|---|---|
| Bowler dome widths by row | 79, 117, 141, 153, 159 px at y 410, 420, 430, 440, 450; top y 403 | A t16.0 |
| Bowler dome | half-width 0.42 D, top at y = -0.68, base at y = -0.37 | A t16.0 |
| Bowler brim | 213 px = 1.12 D wide at y 462 (y = -0.37); spans y 455-482; underside front dips to y = -0.26 | A t16.0 |
| Bowler colours | dome `#463f4e`, dark `#2d2935`, highlight `#cac8e2`, brim `#3b2f3a` | A t16.0 |
| Striped cap extent | x -0.42..+0.42, y -0.55..-0.24 (292 x 109 px) | A t55.0 |
| Striped cap extent | x -0.42..+0.43, y -0.47..-0.15 (161 x 61 px) | A t02.0 |
| Striped cap dome height / visor width | 80 px = 0.23 D / 265 px = 0.76 D (grid) | A t55.0 |
| Cap stripes | 12-14 white stripes across mid-dome, each 9-11 px = 0.03 D | A t55.0 |
| Cap colours | navy `#44598b`, white `#dee9fb`, band `#362a3b`, visor `#989eb6` | A t55.0 |
| Top hat crown | 107 x 73 px = 0.84 x 0.57 D (grid) | A t27.0 |
| Top hat brim | 146 px = 1.14 D wide, about 10 px thick, bottom 0.23 D below head top; gold band `#dabc64` 8 px (grid) | A t27.0 |
| Peaked cap | crown about 1.0 D wide x 0.35 D tall, visor about 0.6 D wide (grid, rough) | A t23.0 |
| Emperor crown | base 197 px = 0.61 D wide; board 343 px = 1.07 D long x 18 px = 0.055 D thick, tilted about 8 degrees; beads 16 px = 0.05 D (grid) | B t22.0 |
| Guard helmet | dome height about 70 px = 0.35 D, same width as head; rim 4-5 px thick, tilted about 10 degrees; cheek plate about 26 x 50 px (grid) | B t42.0 |
| Inventor bun / pin | bun about 90 px = 0.38 D wide; pin 163 px = 0.70 D long; bead about 20 px = 0.085 D (grid) | B t03.0 |

### 2.5 Whole figure and on-screen size
| Quantity | Value | Frame |
|---|---|---|
| Hero height, cap top to feet | 556 px = 2.93 D = 0.43 of frame height | A t02.0 |
| Boss height, hat top to feet | 683 px = 3.58 D = 0.53 of frame height (head top to feet 3.39 D) | A t16.0 |
| Inventor height, bun top to foot | 780 px = 3.33 D = 0.61 of frame height (head top to foot 3.07 D) | B t03.0 |
| Close shot head | D 349 px = 0.48 of frame width | A t55.0 |
| Close shot head (white width) | 355 px; 311-327 px; 341 px; 394 px | A t15.0; A t46.0-t47.5; B t05.0; B t33.0 |
| Medium shot head | D 190 px = 0.26 of frame width; 191 px | A t02.0; A t16.0 |
| Medium shot head (white width / outer) | 194 px; 192 px; outer 234 px; 204-232 px | A t21.0; A t29.0; B t03.0; B t24.5-t26.5 |
| Wide shot head (white width) | 89-140 px; 124 px; 127-132 px; 117-174 px; 112 px | A t12.0-t13.0; A t27.0; A t58.0-t59.0; B t06.5-t07.0; B t36.0 |
| Background figures (white width) | 24-27 px; 31-37 px; 20-75 px | A t22.0; A t35.0; B t27.0-t28.0 |

### 2.6 v1 (`v1/v1_frame20.png`) for comparison
| Quantity | v1 | Reference |
|---|---|---|
| Head D | 229 px | 190 px in the comparable medium shot (A t02.0) |
| Outline width | 3-5 px = 0.013-0.022 D, uniform | 0.02-0.06 D thick-thin on the head |
| Outline colour | `#282928` neutral black | `#3a2832` plum |
| Head shading | `#fffdf8` to `#d6cabc` sphere shading at the bottom | flat, rim only `#fdf8f6` to `#ecdeed` |
| Torso width, hero / boss | 0.45 D / 0.46 D | 0.58 D / 0.99 D |
| Torso height | 0.49-0.67 D, flat top and bottom | 0.86-0.93 D below the chin, rounded |
| Leg width | 17-21 px = 0.075-0.09 D, shaded cylinders | 0.055-0.08 D flat ink |
| Arm width | 11-14 px = 0.05-0.06 D (thinner than legs) | same width as legs |
| Leg length | 201 px = 0.88 D | 1.07-1.52 D |
| Hip spacing | 27 px = 0.12 D | 0.27-0.45 D |
| Height, head top to feet | 2.35 D | 2.9-3.4 D |
| Cap dome width | 256 px = 1.12 D | 0.85 D |
| Hands / feet | none / 3D ellipsoid shoes | ink ball 0.13 D / stub or bar 0.2 D |

---

## 3. How to reproduce

### 3.1 Canonical proportions (D = 1)
| Part | Value |
|---|---|
| Head | ellipse rx 0.50, ry 0.48-0.50 (use 0.49); tilt -8 to +8 degrees at rest |
| Head fill | radial gradient, centre at 45 percent / 40 percent: `#fffaf6` 0, `#fdf8f6` at 0.72, `#ecdeed` at 1.0 |
| Ink | `#3a2832` for every contour, limb and hand |
| Head contour | 0.030 D on the upper-left, 0.055 D on the lower-right |
| Torso contour | 0.03 D |
| Inner detail lines | 0.012-0.022 D |
| Limb stroke | 0.065 D (allowed 0.055-0.075), round caps, arms and legs equal |
| Torso top | y = +0.36 (0.13 D hidden behind the head; chin is at y = +0.49) |
| Torso size, slim / regular / stout | width 0.57 / 0.78 / 1.00; total height 0.99 / 1.04 / 1.06 |
| Torso profile, stout (fraction of half-width, fraction of height, top to bottom) | (0.50, 0.02) (0.82, 0.10) (0.93, 0.25) (0.98, 0.38) (1.00, 0.58) (0.98, 0.77) (0.93, 0.84) (0.72, 0.95) (0.40, 0.995) |
| Torso profile, slim | (0.60, 0.02) (0.90, 0.10) (0.97, 0.25) (1.00, 0.50) (1.00, 0.70) (0.96, 0.85) (0.75, 0.96) (0.40, 1.00) |
| Trouser bowl | bottom 0.14 D of the torso, dark fill, 0.022 D ink line above it |
| Torso shading | horizontal gradient: base x 1.12 at the left edge, base at 35 percent, base x 0.72 at the right edge |
| Shoulders | at the torso's top corners: x = +/-(torso half-width - 0.045), y = +0.42 to +0.56 |
| Arm | upper 0.37, forearm 0.37 (total 0.71-0.79); elbow at the middle |
| Hand | ink disc, diameter 0.13 (clip A) or 0.08-0.10 (clip B) |
| Hips | x = +/-0.14 (stout, regular) to +/-0.22 (slim), y = torso bottom - 0.04 |
| Leg | 1.10 (slim hero) to 1.50 (boss); default 1.25; knee at the middle |
| Foot | stub 0.15-0.20 long continuing the stroke at about 100 degrees to the shin (clip A) or a horizontal bar 0.24 long (clip B) |
| Total height, head top to feet | 3.0 (range 2.9-3.4); a hat adds 0 to 0.2 |

Pixel widths at 720x1280 for a medium shot with D = 190 px: head contour 6 px (left) to 10-11 px (right), limbs 12 px, torso contour 6 px, detail lines 2.5-4 px, hand ball 25 px, buttons 13 px. For a close shot with D = 350 px multiply by 1.84.

### 3.2 Hat recipes (D = 1, relative to head centre, +y down). Draw hats over the head.
- Bowler: dome = upper half of an ellipse rx 0.42, ry 0.31 sitting on y = -0.37 (top at -0.68), fill `#463f4e`, ink 0.035. Brim = crescent from x -0.56 to +0.56, upper edge y about -0.385 at the tips and -0.345 at the centre, lower edge dipping to y = -0.26 at the centre, tips curled up; fill `#3b2f3a`, ink 0.03. Highlight = one arc stroke `#cac8e2`, 0.022 wide, from (-0.30, -0.50) to (0.05, -0.635). Rotate the whole hat -3 to -8 degrees. Eyebrows touch the brim.
- Striped engineer cap: dome = ellipse centre (0, -0.385), rx 0.44, ry 0.165 in ink, inner fill rx 0.415, ry 0.14 navy `#44598b`; 21 white `#dee9fb` wedges fanning from the top button (spacing 0.062 at the dome's lower edge, 0.012 at the top, each 0.032 wide at the bottom) so that 12-14 are visible; button ellipse 0.06 x 0.03 at (0, -0.54); band `#362a3b` from y -0.30 to -0.25, 0.82 wide, bowed down 0.06 in the middle; visor crescent `#989eb6` 0.76 wide reaching y = -0.15 to -0.20 at the centre, ink 0.022.
- Top hat: crown rectangle 0.84 wide x 0.57 tall with a very slight flare upward, base at y = -0.33, fill `#393440` with a vertical lighter stripe `#7d7482` near the left edge; gold band `#dabc64` 0.06 tall at the base; brim ellipse 1.14 wide x 0.08 tall centred at y = -0.30.
- Peaked cap: flared crown 1.0 wide at the top, 0.8 at the band, 0.35 tall, `#445b93`; gold double line and badge on a 0.06 band; black visor 0.6 wide x 0.10.
- Hair patch (front view): crescent inside the head contour on each temple from the hat edge down to y = +0.08, max width 0.085, fill `#9b6d49`, no inner ink line. Three-quarter and near-profile: one patch only, on the side facing away, grown to cover the back quarter to third of the head with a slightly ragged inner edge.

### 3.3 Views to build
Front, three-quarter and near-profile, mirrored for left and right (five yaw states). For three-quarter slide the face and hat front 0.12-0.18 D toward the facing side, narrow the torso to 0.93 of its width and shift its centre-line details 0.10-0.15 D the same way. For near-profile slide the face 0.25-0.30 D, keep both eyes, narrow the torso to 0.85 and put the button row or the single visible suspender 0.06 D inside the facing edge.

### 3.4 Recipe (b): procedural 2D SVG puppet. This is the closest match and the recommended route.
Working code: `spec/character_puppet_proto.py` (run `python3 character_puppet_proto.py out.svg 300`, then `google-chrome --headless --no-sandbox --screenshot=out.png --window-size=1080,1170 file://.../out.svg`). Its output is `spec/character_puppet_proto.png`.

Draw order, back to front: back arm, legs and feet, torso ink silhouette, torso fill and costume (clipped to the torso inset by 0.015), front arms and hands, head ink ellipse, head fill, hair patches, face, hat, props.

Key constructions:
1. Thick-thin head contour without stroke tricks: ink ellipse `rx 0.50 ry 0.49` at (0, 0), then the fill ellipse `rx 0.458 ry 0.448` at (-0.012, -0.012). That yields 0.030 on the upper-left and 0.054 on the lower-right.
2. Torso: closed Catmull-Rom path through the profile points of section 3.1, filled with ink; the same path inset by 0.015 becomes the clip for the gradient fill and the costume. This gives a 0.03 contour.
3. Limbs: `<path d="M S Q C H">` with `stroke-width 0.065`, `stroke-linecap round`, where S is the shoulder or hip, H the hand or ankle, and C = E + bend x (E - (S+H)/2) with E the elbow or knee. bend 0.75-1.0 for relaxed arms, 0.5 for hand on hip, 0 with `stroke-linejoin round` for a sharp knee. Hands: `<circle r="0.065">` in ink at H.
4. Reference poses in D units (head centre origin):
   - boss, hand on hip (A t16.0): S (+0.36, +0.39), E (+0.66, +0.60), H (+0.40, +0.84);
   - hero, hand on hip (A t02.0): S (-0.24, +0.55), E (-0.46, +0.86), H (-0.28, +1.24);
   - inventor pointing up (B t03.0, head-width units): S (+0.21, +0.50), E (+0.38, +0.77), H (+0.63, +0.39).
   These three poses were read from gridded crops, so +/- 0.03.
5. Wobble: wrap the whole figure in `feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2"` plus `feDisplacementMap scale="0.035"` (values in D units because the group is scaled by D). Change the seed per character, not per frame.
6. Raster size: close shots reach D = 350-390 px on screen, so rasterise sprites at D = 512 px. A full figure needs a 2.4 D x 4.2 D canvas, about 1230 x 2150 px, with transparent background.
7. In Blender: put each sprite on a plane with an emission-only material (Image Texture colour to Emission strength 1.0; Mix Shader with Transparent BSDF using the image alpha as factor; image alpha mode straight). Make the plane copy the camera rotation so it stays parallel to the sensor, as the reference figures do. Use the Standard view transform for the character pass, or the whites turn grey.
8. Articulation that works in Blender without re-rasterising every frame: sprites for head (one per view and hat), face (one per expression), torso (one per view); limbs as Blender curve objects in the same plane (poly or bezier spline through S, E, H, `bevel_depth` = 0.0325 D, `use_fill_caps` on, ink emission material) and hands as ink discs. Stack layers 1-2 mm apart in depth in the draw order above. Keyframe the curve points for limb motion and the sprite transforms for head tilt, torso lean and squash.

Known gaps of the prototype against the reference (visible in `character_puppet_proto_compare.jpg`): the cap dome should be puffier and sit lower, with fewer, bolder stripes; feet stubs are too long (use 0.12-0.15 for clip A); costume line weights are a little heavy; no dot pattern on the waistcoat; face is a placeholder.

### 3.5 Recipe (a): 3D meshes with toon shading and outlines
Only worth it if characters must rotate freely. To stop it reading as 3D like v1, every material must be light-independent and the forms must be shallow.
- Scale: v1 uses head radius 0.44 m, so D = 0.88 m. Then limb radius 0.029 m, head contour 0.026-0.048 m, torso width 0.50 / 0.69 / 0.88 m, torso height 0.87-0.93 m, leg 0.97-1.32 m, hand radius 0.057 m.
- Head: UV sphere scaled (0.50, 0.35, 0.49) D so it is shallow in depth. Material: Layer Weight (Facing, blend 0.5) -> ColorRamp (`#fdf8f6` from 0 to 0.72, `#ecdeed` at 1.0) -> Emission 1.0. No Principled BSDF, no lights on the character.
- Torso: lathe the section 3.1 profile (Screw modifier, 48 steps), scale depth to 0.6. Material: Texture Coordinate (Object) X -> Map Range (-half-width..+half-width to 0..1) -> ColorRamp (base x 1.12, base at 0.35, base x 0.72) -> Emission. Costume details come from a front-projected texture rasterised from the same SVG as recipe (b); there is no practical way to get the thin inner ink lines from geometry.
- Outline by inverted hull, in world units so it scales with the figure exactly as in the reference: Solidify modifier, thickness 0.045 D (head) or 0.03 D (torso, hats), offset +1, `use_flip_normals` on, `use_rim` off, `material_offset` 1. Ink material in slot 2: Geometry node `Backfacing` as the factor of a Mix Shader, shader 1 = Emission `#3a2832`, shader 2 = Transparent BSDF. For thick-thin, shift a separate hull copy by (+0.012, +0.012) D toward lower-right in camera space, or drive Solidify thickness with a vertex group weighted 0.55 upper-left to 1.0 lower-right. All of these API names exist in bpy 5.3 (checked without rendering).
- Limbs: curve objects with round bevel 0.0325 D and ink emission, no outline needed. Hands: spheres of diameter 0.13 D in ink. Feet: one more curve point.
- Hats: bowler = half ellipsoid (0.42, 0.42, 0.31) D with its base at 0.13 D below the head top, tilted forward 8-10 degrees so the brim front reaches the brows; brim = flattened torus of major radius 0.56 D. Emission `#463f4e`, highlight as a painted texture streak, hull 0.035 D. Striped cap = squashed ellipsoid 0.85 D wide x 0.3 D tall with a stripe texture, lowered so its bottom edge is 0.26-0.36 D below the head top.
- Remaining risk: perspective parallax between head, hat and limbs and any real shading will still read as 3D. Recipe (b) avoids that entirely.

---

## 4. Differences vs v1, ranked by visual impact

1. Rendering model. v1 is lit 3D plastic: sphere shading on the head (`#fffdf8` to `#d6cabc`), glossy cylinder legs, soft shadows. The reference is flat ink-and-fill artwork with only airbrush gradients. This alone accounts for most of the mismatch. Fix: emission-only materials or 2D sprites.
2. Outline. v1: 3-5 px at D = 229 (0.013-0.022 D), uniform, neutral black `#282928`, no inner lines. Reference: 0.02-0.06 D thick-thin on the head, 0.03 D on the torso, plum `#3a2832`, plus thin inner detail lines everywhere.
3. Torso. v1: a bare flat-topped cylinder 0.45 D wide and 0.49-0.67 D tall with one colour. Reference: rounded pill or egg, 0.57-1.00 D wide and 0.86-0.93 D tall below the chin, with trouser bowl, gradient and a full costume (buttons, straps, bandana, chain, pockets). The v1 boss is half the reference width (0.46 D against 0.99 D).
4. Hats. v1 hats are separate shaded 3D objects; the cap dome is 1.12 D wide with a plain blue fill and a flat disc visor. Reference hats are drawn over the top quarter to third of the head, narrower than the head for the cap (0.85 D), with stripes, band, visor and painted highlight, and the brim touches the eyebrows. Hair patches under the hat are missing in v1.
5. Limbs. v1: rigid straight cylinders, arms (11-14 px) thinner than legs (17-21 px), no elbows or knees, no hands, ellipsoid shoes. Reference: ink strokes of one width (0.065 D) with rubber-hose bends, ball hands 0.13 D, stub or bar feet, and expressive poses (hands on hips, leaning, crouching).
6. Proportions. v1 is 2.35 D from head top to feet, with legs 0.88 D long and only 0.12 D apart. Reference is 2.9-3.4 D, legs 1.1-1.5 D, hips 0.27-0.45 D apart.
7. Neck and junction. v1 has a visible white collar cylinder that acts as a neck. Reference has none: the head overlaps the torso by 0.10-0.15 D.
8. Acting. v1 bodies are vertical and static. Reference torsos lean and tilt, heads tilt 5-15 degrees and slide off the body axis, and three drawn views are swapped as characters turn.
9. Framing. v1 heads are 229 px in a two-shot, close to the reference medium range (150-250 px), so size is acceptable; the reference also cuts to closes at 300-390 px and wides at 100-145 px.
