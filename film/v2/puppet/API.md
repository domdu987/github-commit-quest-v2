# puppet.py: character puppet API (v2, pure 2D SVG)

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v2/puppet/puppet.py`
Python 3 standard library only. Deterministic (no random, no time, no `hash()`), 0.5 to 1 ms per `figure()` call.
Reviewed and repaired (see `REVIEW.md`; robustness tests: `python3 test_puppet.py`). Everything in this file that existed before the review still works with the same names; additions are marked "(review)".

## 1. Conventions

- Unit = D, the outer ink-to-ink head diameter. x to the right, y DOWN.
- Puppet local frame: head centre at (0, 0). Head top y = -0.51, chin y = +0.51. Soles of a standing figure: hero y = +2.46, boss y = +2.87 (read `feet_y`, never hard-code it).
- Everything returned is an SVG fragment (no outer `<svg>`). All ids start with the `uid` you pass (`uid_hg`, `uid_tc`, ...), so give every figure in one document its own uid.
- `"r"` / `"l"` always mean the screen-right / screen-left limb of the unflipped figure.
- Angles are SVG angles in degrees: 0 = pointing right, 90 = pointing down, -90 = pointing up; positive rotation is clockwise on screen.

## 2. Functions

```python
import puppet

puppet.CAST                                   # {"hero": {...}, "boss": {...}}
f = puppet.figure(cast_name, pose=None, uid="p")
#   f["svg"]      '<g id="uid_fig" transform="scale(sx sy)"> ... </g>' in D units, head centre at the origin
#   f["feet_y"]   y of the soles for this pose (D)
#   f["bbox"]     (x0, y0, x1, y1) in D, includes hat, limbs, props, steam and Z; focus lines are NOT included
#   f["anchors"]  dict name -> (x, y) in D, see section 6
puppet.contact_shadow(width_D, uid="cs", color="#252432", opacity=0.6)   # soft ellipse centred on (0, 0)
puppet.place_svg(f, x, y, scale, anchor="feet")   # wraps f["svg"] so the feet (or anchor="head": the head centre) sit on (x, y)
puppet.hand_for_tip(prop_type, tip_xy, angle, scale=1.0)   # hand target that puts a held prop's tip on tip_xy
puppet.resolve_pose(cast_name, pose)          # presets -> plain numbers (same drawing)
puppet.lerp_pose(cast_name, pose_a, pose_b, t)   # in-between pose, 0 <= t <= 1
puppet.STORY                                  # {"hero_draw": (cast, pose), "boss_rub": ..., "hero_shock": ...}
```

Unknown cast names raise `KeyError`. Nothing else raises: unknown or wrongly typed presets, expressions, props, effects and pose values fall back to the default (a pose that is not a dict counts as `{}`).
Non-finite or out-of-range numbers are clamped (ranges below). The caller's pose dict is never modified.

### Cast

| name | build | costume | hat | limbs | height (head top to soles) |
|---|---|---|---|---|---|
| `hero` | slim pill, torso 0.57 x 1.01 D, legs 1.10 D, hips +/-0.22 | cobalt sweater vest `#3b6fda` with argyle row, cream shirt collar, ochre tie `#e3a93a`, charcoal trouser bowl | ochre tweed 8-panel newsboy cap `#dca63e` with a cream windowpane check and brown seams, visor follows yaw; auburn hair crescents `#a8492a`; red map pencil behind the screen-right ear | 0.054 D, hand ball 0.12 D | 2.99 D (+0.07 cap) |
| `boss` | stout egg, torso 1.00 x 1.06 D, legs 1.45 D, hips +/-0.14 | forest-green double-breasted waistcoat `#2f8b58` with chalk pinstripes, dark shawl lapels, white shirt V, red bow tie `#c9352e`, six brass buttons in two columns, white pocket square | grey felt homburg with ribbon band, flat bow and a small orange feather, brim 1.12 D wide dipping to the brows; grey hair on the far side when turned; ink moustache | 0.068 D, hand ball 0.14 D | 3.40 D (+0.21 hat) |

Cast design (review): the first colourway of the hero (slate-blue cap with light lines, brown hair) and the first boss costume (five centre buttons, watch chain, three welt pockets, dots) were recolours of the reference hero's head and of the reference boss's waistcoat. Both were replaced by the designs above; build, hats' shapes, faces and every API name are unchanged.
At head D = 110 px the two read apart by silhouette (short and slim with a flat cap against tall and stout with a brimmed hat: `sheet.png`, bottom row) and by colour (ochre + cobalt against grey + green + red).

Backgrounds (bottom rows of `sheet.png`): heads, costumes and hats separate on `#a8663f`, `#55291a` and `#1f2a55`. The ink limbs are dark by design (as in the reference) and nearly vanish on `#55291a` and `#1f2a55`: either keep a mid-value surface behind the legs, or pass the `rim` pose key (review), which draws a thin light halo behind arms, hands, legs and feet only where they leave the body silhouette, e.g. `rim="#8f9bd8"` on the navy floor, `rim="#d9a27a"` on the dark wainscot.

## 3. Pose keys (all optional)

| key | type, range | default | effect |
|---|---|---|---|
| `yaw` | float -1.2 .. 1.2 | 0 | negative faces screen-left. 0 front, +/-0.5 three-quarter, +/-1 near-profile (1.2 = extreme). Face slides 0.12 x yaw, eye spacing 0.26 - 0.075 x abs(yaw), far eye scale 1 - 0.14 x abs(yaw), far-side hair patch grows, near-side one vanishes, cap visor slides 0.30 x yaw, torso narrows to 1 - 0.15 x abs(yaw), costume centre line slides to the facing edge (0.06 D inside it at +/-1), feet and knees turn to the facing side |
| `pitch` | float -1.5 .. 1.5 | 0 | features move 0.07 D per unit; -0.9 = proud / low angle (angry brows touch the brim), +1 = looking down (sad) |
| `head_roll` | degrees -75 .. 75 | 0 | rolls face, hair and hat about the head centre (absolute, does not inherit `lean`). The head disc, its thick lower-right contour and its shadow crescent stay screen-fixed, as measured |
| `head_dx`, `head_dy` | float -0.8 .. 0.8 | 0 | head offset from the torso axis. The head stays at the origin; torso and limbs move by (-dx, -dy) |
| `lean` | degrees -75 .. 75 | 0 | torso lean, positive = head to the right of the hips (clockwise). The torso rotates about the head centre; feet stay under the hips (use `legs="lean"` for a rigid whole-body tilt) |
| `squash` | float or (sx, sy), 0.3 .. 2.5 | 1 | whole-figure squash and stretch about the head centre. `feet_y`, bbox and anchors are scaled accordingly, so re-plant the feet every frame |
| `expr` | one of the 20 names in section 4 | `"neutral"` | face drawing (discrete, never tweened) |
| `mouth` | name from MOUTHS, or `("open", width, height)` | None | overrides the mouth of `expr` (lip-sync). width 0.05..0.34, height 0.03..0.20 |
| `blink` | 0, 1, 2 | 0 | 0 open, 1 half (ring eye becomes the 0.22 x 0.08 almond, half-lid pupil shortens), 2 closed (flat line) |
| `gaze` | float or (gx, gy), -1 .. 1 | 0 | pupil shift, 0.03 D per unit |
| `arm_r`, `arm_l` | preset name or dict | `"down"` | section 5 |
| `legs` | preset name or dict | `"stand"` | section 5 |
| `prop_r`, `prop_l` | type name or dict | None | section 5 |
| `fx` | list of names or dicts | [] | section 7 |
| `t` | float | 0 | default phase (0..1 loop) for the animated effects |
| `tint` | `"#rrggbb"` or (r, g, b) | None | multiplies every fill (head, costume, hat, hair, props, effects) by this colour: night `#fbdaf7`, warm interior `#faded0`. Ink is not tinted |
| `ink` | `"#rrggbb"` | `#3a2832` | outline, limb and feature colour (night: `#1e142e`) |
| `limb_w` | float 0.035 .. 0.09 | per cast: hero 0.054, boss 0.068 (review) | arm and leg stroke width; the hand ball scales with it (diameter 0.13 x (limb_w / 0.060)^0.75). The reference draws the boss heavier than the hero (0.058-0.089 against 0.040-0.065 D) and thinner limbs in close shots (0.043 at D = 350 px): pass about 0.8 of the default for a close-up |
| `rim` (review) | `"#rrggbb"` or None | None | light halo behind arms, hands, legs and feet, for dark backgrounds. Drawn as one group behind the whole figure, so it never crosses the torso or the head |
| `rim_w` (review) | float 0.004 .. 0.05 | 0.014 | halo width on each side of the limb (D) |
| `rim_opacity` (review) | float 0 .. 1 | 0.6 | opacity of the halo group |
| `mirror` | bool | False | mirrors the whole figure (costume asymmetry included) but keeps the head disc unmirrored. Anchors and bbox come back already mirrored and r/l swapped. Prefer this over `scale(-1,1)` in the compositor |

Continuity: every numeric key is continuous (checked by `python3 puppet.py test` and by `python3 test_puppet.py`: every numeric key swept through its whole range in 40 and 240 steps, hand and foot targets on circles from 0.02 D to 50 D around the joint root and on straight lines through it). Since the review there is no dead zone and no flip at the joint root: hand, elbow, foot and knee anchors are continuous for EVERY target. Only a direction is still undefined when a hand target sits exactly on its own shoulder: a prop held without an explicit `angle` (it follows the forearm) turns over there, so give the prop an `angle` if the hand must pass through the shoulder.
Discrete choices that switch instantly by design: `expr`, `mouth` name, `blink`, prop type, hand shape, arm layer. Change `expr` behind a blink (half, closed, half: one frame each), as the reference does.

## 4. Expressions and mouths

`EXPRESSIONS` (the 20 measured recipes): `neutral`, `unimpressed`, `smirk`, `determined`, `angry`, `furious`, `smug`, `talking`, `shocked`, `stunned`, `excited`, `happy`, `laughing`, `worried`, `asleep`, `shouting`, `grinning`, `wink`, `sad`, `blink`.

| name | eyes | brows | mouth | usual extras |
|---|---|---|---|---|
| neutral | half-lid | two (hero: solid domes, boss: heavy strokes) | hero dash, boss arch frown | |
| unimpressed | half-lid | one, flat, over the near eye | arch frown | |
| smirk | half-lid, gaze +0.02 | none | smirk | |
| determined | half-lid | both +15 deg | arch frown | |
| angry | half-lid tilted 10 deg | both heavy, +24 deg, touching the lids | arch frown | `pitch=-0.9` |
| furious | as angry | as angry | clenched teeth | `fx=["anger_fill","steam"]` |
| smug | half-lid | one raised, -7 deg | flat bar | |
| talking | half-lid | one raised | wide-open talk mouth | cycle `mouth` |
| shocked | ring, 0.033 pupils | none | "O" | `fx=["sweat"]` |
| stunned | ring, 0.06 pupils | one short raised | dash | |
| excited | ring, 0.06 pupils | none | grin with four teeth | |
| happy | happy arcs | both raised 0.20 | small smile | |
| laughing | happy arcs | both raised | wide grin | `fx=["blush","tears"]`, `head_roll=15` |
| worried | half-lid | both -9 deg | wavy | `fx=["sweat"]` |
| asleep | closed lines | flat, low | tilted dash | `fx=["zzz"]` |
| shouting | squeezed `> <` | none | clenched teeth | |
| grinning | dot eyes | thin raised | grin | |
| wink | far eye arc, near eye half-lid | one raised high | smirk | |
| sad | half-lid | both -28 deg | wavy | `pitch=1` |
| blink | closed lines | neutral | default | same as `blink=2` on neutral |

`MOUTHS`: `default`, `none`, `dash`, `frown`, `smirk`, `smile`, `grin`, `flat`, `talk_a` (half open 0.28 x 0.085), `talk_b` (wide open 0.285 x 0.17), `talk_o` (round 0.18 x 0.13), `o` (shock egg), `clench`, `wavy`.
Lip-sync cycle from the spec: silent = `flat`, low = `talk_a`, loud = `talk_b`, "oo/w" = `talk_o`; new drawing every 2 frames on average, eyes and brows held.
The boss's moustache is always drawn; it sits 0.03 above the mouth line and pushes the mouth 0.058 down.
One-brow expressions put the brow over the near eye: the right eye for yaw <= 0.05, the left eye for yaw >= 0.25, cross-fading in between (no pop while turning).

## 5. Arms, legs, props

### Arms
Preset names (`ARM_PRESETS`, per build): `down`, `hip` (hand on the hip, soft V elbow, as A t16.0), `akimbo` (review: its own preset now, a smooth jug-handle arc as A t44.0; it used to be an alias of `hip`), `point` (index finger), `raised` (open hand), `behind` (drawn behind the torso), `forward` (offering / handshake, open hand), `reach_up` (up and out, for drawing on the wall), `rub` (up beside the head, for the eraser), `shrug` (open hands), `chin` (hand on the chin, drawn over the head), `wave`.

Dict form (any subset):

| key | meaning |
|---|---|
| `hand` | (x, y) target in local D units. Solved by two-bone IK: arm length 0.74 D (0.37 + 0.37). The hand is the target itself, clamped to the arm length (at full reach the arm is straight). Closer than 0.25 of the arm length to the shoulder the rubber hose retracts (the elbow offset fades out), so nothing jumps when a target passes through the shoulder (review; before, the reach was clamped to 0.12 .. 1.0 and the elbow flipped). Read `anchors["hand_r"]` for the hand actually reached |
| `preset` | start from a preset and override single fields |
| `bend` | -1 .. 1, signed size of the elbow offset (rubber hose: abs < 1 = shallower). +1: elbow on the outside for a hand below the shoulder (akimbo). -1: elbow low / outside for a hand level with or above the shoulder (pointing, raised). Default when only `hand` is given: continuous in the hand height, +1 for a hand 0.4 D below the shoulder, 0 at 0.1 D below it, -1 from 0.2 D above it |
| `sharp` | 0 .. 1, 0 = one smooth arc through the elbow, 1 = sharp V (default 0.25) |
| `stretch` | 0.5 .. 1.3, arm length factor for a rubber-hose reach (`reach_up` uses 1.06) |
| `layer` | `"front"` (over the torso, under the head: default), `"back"` (behind legs and torso), `"top"` (over head and hat) |
| `shape` | `"ball"` (ink ball, 0.12 D hero / 0.14 D boss), `"point"` (ball + index stroke along the forearm), `"open"` (ball + four finger strokes) |

### Legs
Preset names (`LEG_PRESETS`): `stand`, `wide` (the reference hero stance), `narrow`, `step` (stride toward the facing side, knees bent), `lean` (legs rigidly follow the torso lean), `crouch`.
Dict form: `preset`, `spread` (extra distance of each foot from its hip, -0.2 .. 0.8), `stride` (-1.5 .. 1.5, right foot forward by 0.34 D per unit, left back by 0.26), `crouch` (0 .. 0.75, fraction of the hip height dropped: knees bend), `lift_r`, `lift_l` (0 .. 1.5, foot raised 0.30 D per unit), `foot_r`, `foot_l` ((x, y) absolute local targets), `knee_r`, `knee_l` (-1 .. 1, +1 = knee toward +x), `toe_r`, `toe_l` (-1 .. 1, foot stub direction and length), `rigid` (bool).
Both feet are kept on one ground line (the hip that drops bends its knee); `feet_y` is the lower sole. Leg length is clamped like the arm. Standing legs carry a constant 0.012 D outward bow.

### Line quality of the limbs (review)
Arms and legs are no longer constant-width vector strokes. Each limb is a core stroke (0.86 of the width, round caps and joins) plus a filled ribbon whose width breathes by about +/-10 percent along the limb and whose centre line wavers by 0.06 of the width, like the hand-inked limbs of the reference (boss legs 13 to 17 px at D = 191 px). The variation depends only on the position along the limb and on a fixed per-limb seed, so it travels with the limb and never boils; joints and anchors are not displaced. The foot stub is its own round-capped stroke.

### Props
`prop_r` / `prop_l`: `"pencil"`, `"eraser"`, `"pointer"`, `"paper"`, or `{"type": ..., "angle": degrees, "twist": degrees, "scale": 1.0}`.
`angle` omitted = the prop continues the forearm (plus `twist`). `anchors["prop_tip_r"]` is the working point: pencil point (0.36 D from the hand), centre of the eraser's felt face (under the hand), pointer tip (1.17 D), far edge of the paper (0.58 D). Distances are in `PROP_TIP`. With no prop, `prop_tip_*` is the fingertip (index tip for `shape="point"`, edge of the ball otherwise).
The prop is drawn in the same layer as its arm, under the hand ball. The pencil is the red map pencil of the story.

## 6. Anchors (local D units, after squash and mirror)

`hand_r`, `hand_l`, `prop_tip_r`, `prop_tip_l`, `shoulder_r`, `shoulder_l`, `elbow_r`, `elbow_l`, `head_top` (top of the head disc, under the hat), `hat_top`, `head` (0, 0), `mouth`, `eye_r`, `eye_l`, `chest` (centre line at y = 0.8 of the torso), `hip`, `knee_r`, `knee_l`, `foot_r`, `foot_l` (ankles), `feet` (midpoint between the ankles, on the sole line: the point to plant on the floor).

## 7. Effects (`fx`)

Each entry is a name or a dict `{"type": name, ...}`:

| type | parameters | notes |
|---|---|---|
| `sweat` | `side` (-1..1, default: temple beside the leading eye), `scale` | pale drop with a slate outline, tucked under the hat |
| `anger_fill` | `level` 0..1 (default 1), `t` | purple liquid rising from the chin (animate level 0 to 1 over 8 frames), wavy surface and bubbles while rising, specular arc when full |
| `steam` | `t` 0..1 loop | three puffs per side pumping up and out from brim height |
| `blush` | | two soft pink ellipses under the eyes |
| `focus_lines` | `seed` (pass the frame number: redrawn every frame), `n` (default 30) | white radial streaks behind the figure, radius 0.85 to 2.7 D; not in the bbox |
| `tears` | `t` 0..1 loop | laugh tears flying from the outer eye corners |
| `zzz` | `t` 0..1 loop (one spawn period = 0.65 s) | three Z rising above the head |

## 8. Worked examples

World frame of the set: floor contact line y = 0, x = 0 at the centre of the wall map. Camera = (cx, cy, zoom px per D), frame 720 x 1280: `screen = ((wx - cx) * zoom + 360, (wy - cy) * zoom + 640)`. A runnable version of examples 1 and 2 is `example_scene.py` (writes `tmp/example_scene.png`).

### Example 1: plant a figure on the floor with a contact shadow

```python
import puppet
cx, cy, zoom = 0.0, -1.95, 150.0
def w2s(x, y): return ((x - cx) * zoom + 360.0, (y - cy) * zoom + 640.0)

f = puppet.figure("boss", {"yaw": -0.5, "expr": "smug", "arm_r": "hip"}, uid="boss")
wx = 1.05                                             # where he stands (world D)
fx, fy = w2s(wx, 0.0)
svg  = '<g transform="translate(%.2f %.2f) scale(%.3f)">%s</g>' % (fx, fy, zoom, puppet.contact_shadow(0.9, "boss_sh"))
svg += puppet.place_svg(f, fx, fy, zoom)              # feet on the floor point, whatever the pose
# world position of any anchor: origin = (wx - f["anchors"]["feet"][0], -f["feet_y"]); world = origin + anchor
```

### Example 2: story pose, the hero draws the red track (pencil point on a map position)

```python
pose = dict(puppet.STORY["hero_draw"][1])             # yaw 0.55, determined, arm_r "reach_up", red pencil
probe = puppet.figure("hero", pose, "probe")
origin = (-0.75 - probe["anchors"]["feet"][0], -probe["feet_y"])        # head centre in world D when he stands at x = -0.75
track_end = (0.25, -2.75)                             # world point on the map
tip_local = (track_end[0] - origin[0], track_end[1] - origin[1])
pose["arm_r"]  = {"hand": puppet.hand_for_tip("pencil", tip_local, -48), "stretch": 1.08}
pose["prop_r"] = {"type": "pencil", "angle": -48}
f = puppet.figure("hero", pose, "hero")
tip = f["anchors"]["prop_tip_r"]                      # equals tip_local when the arm can reach; draw the red line up to here
```

### Example 3: the boss rubs it out, the hero is shocked, with blink and in-betweens

```python
rub = dict(puppet.STORY["boss_rub"][1])               # yaw -0.5, smug, arm_l "rub" + eraser, arm_r on the hip
for frame in range(24):                               # scrub: move the eraser hand on a small circle, features held
    import math
    a = frame / 6.0 * 2 * math.pi
    p = dict(rub, arm_l={"preset": "rub", "hand": (-0.82 + 0.10 * math.cos(a), 0.05 + 0.07 * math.sin(a))},
             prop_l={"type": "eraser", "angle": -140 + 8 * math.sin(a)})
    boss = puppet.figure("boss", p, "boss")

a = {"expr": "neutral", "yaw": -0.2, "arm_r": "down", "arm_l": "down"}
b = puppet.STORY["hero_shock"][1]                     # wide-eyed, sweat drop, open hands, squash (0.97, 1.04)
for i in range(7):                                    # 7-frame change of expression hidden behind a blink
    p = puppet.lerp_pose("hero", a, b, i / 6.0)       # numbers interpolate, the drawing switches at t = 0.5
    p["blink"] = {2: 1, 3: 2, 4: 1}.get(i, 0)         # half, closed, half
    hero = puppet.figure("hero", p, "hero")
night = puppet.figure("hero", dict(b, tint="#fbdaf7", ink="#1e142e"), "hero_n")     # clip B night grade
```

## 9. Command line

```
python3 puppet.py sheet     # sheet.svg + sheet.png: 5 yaw states x 2, 20 expressions x 2, 10 body poses (3 story poses), swatches, tints, rim, silhouettes
python3 puppet.py compare   # compare.svg + compare.jpg: 9 reference crops beside our figures at the same head size in px
python3 puppet.py test      # determinism, NaN, continuity sweeps, speed, resolve/lerp consistency
python3 puppet.py bench
python3 measure.py          # re-measures the Chromium render against the spec ranges (numpy + Pillow, QA only)
python3 test_puppet.py [--quick] [--strip]   # (review) robustness: sweeps, IK targets, garbage input, speed; --strip renders tmp/rv/turn_strip.png
python3 review.py compare   # (review) review_compare.jpg: 10 reference crops beside our figures, same head size in px, same background colour
python3 review.py measure   # (review) tmp/rv/measure.txt: one image-analysis tool run on the reference frames AND on our render
node raster_multi.js jobs.json   # (review) many SVG files in one Chromium launch
python3 example_scene.py    # the two-shot of examples 1 and 2
node raster.js in.svg out.png|jpg W H [deviceScaleFactor]
```

## 10. Where the two specs differ, and what was chosen

| item | character_anatomy.md | face_expressions.md | used |
|---|---|---|---|
| ink | `#3a2832` | `#3a2a30` | `#3a2832` |
| head contour | two ellipses, 0.030 upper-left to 0.055 lower-right | per-angle table 0.019 left to 0.070 lower-right, wobbly polygons | review: a per-angle table re-calibrated by running ONE tool on the reference and on our render (0.052 right, 0.071 lower right, 0.050 at 120 degrees, 0.036 at 150, 0.027 left; the face-spec table read 0.010-0.015 D too thin on the lower left with that tool), periodic spline between the nodes, smooth closed curves, baked wobble with a fixed seed per character. The fill disc is normalised so that the lower-arc circle fit is exactly R = 0.463 D about the fill centre for every character |
| head fill | radial gradient to `#ecdeed` at the rim | flat `#fef7f6` plus one lavender crescent `#e9dceb` lower-right | flat fill plus crescent (lit disc r 0.42 at (-0.029, -0.034), soft edge 0.04) |
| face slide at near-profile | 0.25 to 0.30 D | 0.08 to 0.14 D measured, formula 0.12 x yaw | 0.12 x yaw (yaw may go to 1.2 = 0.144 D) |
| origin | centre of the outer ellipse | centre of the white fill disc | ink bounding box centred on (0, 0); the fill centre is at (-0.012, -0.023) |
| wobble | feTurbulence displacement | feTurbulence displacement plus polygons | no filters at all: baked geometry only (filter noise would swim under camera moves) |
| limb width | 0.065 (0.055 to 0.075; 0.043 in the close shot) | not covered | review: per cast, hero 0.054 and boss 0.068 (the measurements in anatomy 2.3 differ by character), width breathing +/-10 percent; pose key `limb_w` for close shots |
| foot stub | 0.15 to 0.20, "use 0.12 to 0.15" in the known gaps | not covered | 0.14 |
