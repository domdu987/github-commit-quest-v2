# cast17.py: the cast of film 17 (Bertillon, the card index and the measuring chair, Paris 1882-83) for the v2 puppet

File: `film/v3/cast17/cast17.py`. Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast17 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), then adds entries to their tables and wraps the puppet helpers on top of cast10's wrappers: `_norm` (pose keys `seat17`, `flush17`), `_face` (pince-nez, narrow beard, side-whiskers, stubble, red flush), `_moustache` (style `curl17`), `_hand` (finger shapes `three`, `fist`), `_prop` (new props) and `figure` (chair / bench under a seated figure). Each wrapper falls through to the earlier ones, so every earlier member draws exactly as before (the test draws cast8's `inspector` and film 9's `general` after import).

```python
import sys
sys.path.insert(0, "film/v3/cast17")
import cast17                       # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                       # same module object: CAST now also has the 9 members below
cast, pose = cast17.STORY17["bertillon_measuring"]
f = puppet.figure(cast, pose, "f")                                  # f["anchors"]["calipers_r"] = between the jaw tips
p = cast17.speak(pose, g)                                           # mouth driven by talk_mouth(g): the ONLY way a mouth moves
p = cast17.with_expr(pose, "proud")                                 # one of the 7 named expressions
p = dict(p, blink=cast17.blink_at(g, 90))
w = puppet.figure("gendarme_a", cast17.cycle("gendarme_a", g / 28.0, "march"), "f")
a = actors.Actor("ins", "inspector17"); a.build(sprites.DEFAULT_CANVAS["inspector17"], sprite_dir, contact=True)
```

For film 17 copy `film8/common.py` and put `cast17` in place of `cast8` in the path list and the import. Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies: pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`.

**The CAST key of the chief inspector is `inspector17`**: `inspector` is cast8's police inspector and is left unchanged (same reason as `painter10`). `cast17.KEY` maps the story names (`"inspector"`, `"bertillon"`, ...) to the CAST keys. Pose names keep the short name (`inspector_laughing`).

## Cast (head D = 1)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `bertillon` | `slim` 0.60 x 1.02, legs 1.42 | 3.30 (3.30) | Alphonse Bertillon, 29: thin, tall, serious. Black frock coat, dove-blue waistcoat, white collar and shirt, dark-red tie, dark-brown hair parted at the side (no hat), **narrow dark beard** (a chin tuft tapering below the chin and a thin jaw strap), pencil moustache, steel **pince-nez** on a black cord |
| `inspector17` | `stout` 1.34 x 1.16, legs 1.22 | 3.21 (3.49) | the mocker: big belly, ruddy cheeks, **huge waxed moustache with curled tips** (`curl17`), dark-blue **kepi** (red band, gold piping), dark-blue double-breasted tunic with **brass buttons**, gold collar braid and cuffs, belt, navy trousers |
| `prefect` | `regular` 0.96 x 1.08, legs 1.40 | 3.34 (3.92) | black **top hat**, black frock coat, **tricolour sash** (blue / white / red, knot with a gold fringe at the left hip), khaki waistcoat with a gold watch chain, **grey side-whiskers**, grey hair, a frown |
| `dupont` | `regular` 0.72 x 0.96, legs 1.24 | 3.06 (3.12) | scruffy thief: olive flat cap, ginger hair, **stubble**, a brown jacket with **sewn-on patches** (blue, ochre, green), grubby shirt, red neckerchief, blue-grey trousers |
| `gendarme_a` | `regular` 0.94 x 1.04, legs 1.26 | 3.16 (3.44) | kepi (navy, red band), blue tunic with silver buttons, **navy cape** with a red lining, brown moustache |
| `gendarme_b` | `slim` 0.72 x 1.06, legs 1.40 | 3.32 (3.60) | taller, thinner: **grey-green** kepi (mustard band), tunic and cape with a mustard lining, brass buttons, gold cord, black handlebar moustache |
| `prisoner_a` | `slim` | 3.14 | pale, thin, stubble, no hat, grey-blue jacket, a patch |
| `prisoner_b` | `stout` | 2.99 (3.25) | brown derby, bushy moustache, brown jacket over an olive waistcoat |
| `prisoner_c` | `regular` | 2.94 (3.12) | navy beret, freckles, olive jacket |

The palette keeps large areas mid-dark (navy, black, brown, olive, grey-green); near-white appears only on faces, collars and cuffs (and the small white band of the sash), so every member reads on terracotta / ochre walls and honey wood (`sheet.jpg`, `stage_test.png`). Outlines are the puppet's ink `#3a2832`, as in all earlier casts. **No text** appears on any drawing: the cards carry two photographs and a fingerprint, the ledger a clasp and ribbon.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `seat17` | `"chair"` / `"bench"` / None (None) | draws a seat **behind** a seated figure, sized from the hip anchor: `chair` = the measuring chair (oak, slatted back, iron head rest at head height, arms, 4 legs), `bench` = a plank on two trestles (`seat_w` D wide, 2.0). Combine with `legs=dict(preset="narrow", crouch=0.45, knee_r=0.0, knee_l=0.0)` (hip drops to seat height, knees stay in front). Anchor `seat` = (x, seat top). Set it to None when the set has its own chair / bench |
| `seat_w` | 0.8 .. 4.0 (2.0) | bench width |
| `flush17` | 0..1 (0) | the **red-faced** variant: a red flush over the face (any cast17 member); 1 = furious red |
| `sweat` | 0..1 | cast7's sweat drops (works on all cast17 members) |

New hand shapes for `arm_r` / `arm_l` dicts (`shape=`): **`three`** (index, middle and ring finger up, thumb and little finger tucked: "3 months"; point the hand upward) and **`fist`** (larger ball, for the triumphant fist). New CAST keys (cast17 members only): costume `jacket17` (colors base / dark / lapel / pocket / button / shirt / pants, optional vest, scarf, scarf_d; `patches` = ((x, y, w, h, colour), ..), `patches_low`, `jacket_len`, `jacket_flare`), `cape17` (uniform7 + colors cape / cape_l; `cape_len`, `cape_flare`), `sash17` (frock7 + the tricolour sash), `inspector17` (uniform7 + gold collar braid); face `beard17=dict(color, light)`, `pincenez17=True`, `whiskers17=dict(color, light)`, `stubble17=dict(color, opacity)`; `moustache_style="curl17"`.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

All four have their long axis along +x of the hand frame and follow `angle` (degrees, SVG, 0 = right, -90 = up); `scale` works.

| type | drawing | `prop_tip_*` | anchors |
|---|---|---|---|
| `calipers` | steel sliding calipers: graduated beam (-0.12 .. 0.86), fixed jaw at the far end, sliding jaw with a brass thumbscrew; the jaws hang toward +y of the frame (below the beam for angle 0) | far end (0.86) | `calipers_r/_l` = between the jaw tips |
| `card` | a record card (0.50 x 0.36 D): red tab, two photographs with head silhouettes, a fingerprint, no writing. Held at its edge: `angle=-90` raises it upright | far edge (0.52) | `card_r/_l` = card centre |
| `pen` | dip pen 0.52 D with a quill feather at the back, brass band, steel nib and ink drop | nib (0.52) | `nib_r/_l` |
| `ledger` | bound register 0.70 x 0.54 D, maroon cloth, leather corners, brass clasp band, blue ribbon, cream page edge; spine on the -y side; `angle=-90` carries it upright | far end (0.74) | `ledger_r/_l` = centre |

`cast17.hand_for_anchor(cast, pose, "r", "calipers_l", target_local)` moves a pose's arm dict hand until a prop anchor lies on a local target (e.g. calipers jaws on the inspector's ear; with `mirror=True` the anchor's r/l swap). Standalone fragments (along +x from the hand point, ink and tint arguments): `calipers_svg(uid)`, `card_svg(uid)`, `pen_svg(uid)`, `ledger_svg(uid)`.

## Expressions, mouths, blink, idle

`cast17.EXPR17` = the 7 named faces for every member: `neutral`, `smirk`, `laugh` (laughing + tears, head back), `angry`, `surprised` (shocked, round mouth), `worried`, `proud` (smug, smile, chin up). `cast17.with_expr(pose, name, **extra)` returns a copy of the pose with that face. **Mouths move only when talking**: every face and every story pose holds a *closed* mouth except `laugh` / `surprised` and the poses flagged `open_mouth` in `STORY17_META` (held open shapes). Talking is the one call `cast17.speak(pose, frame, level=1.0)` = `mouth = talk_mouth(frame, level)` (open `talk_a` / `talk_b` / `talk_o`, closed `flat`, new drawing every 2 frames); `cast17.silent(pose)` shuts it again. Blink: `blink=cast17.blink_at(frame, period, offset)` (half, closed, half). Idle bounce: re-exported `cast17.cycle(cast, phase, mode, facing, base, arms, speed)` modes `walk` / `run` / `sneak` / `march`, and `squash=(1.0 + a, 1.0 - a)` breathing at about 0.01 as in cast9/10; `cast17.NOD` is the nod table. Poses marked `lipsync` in `STORY17_META` are meant to be driven by `speak()`; any pose can be.

## Cast poses (`cast17.STORY17[name] = (cast, pose)`, also merged into `puppet.STORY`; notes in `STORY17_META[name]["note"]`)

| member | poses |
|---|---|
| `bertillon` | `bertillon_neutral`, `bertillon_measuring` (arm out holding the calipers; mirror for the ear), `bertillon_writing` (pen + card), `bertillon_holding_card` (card raised), `bertillon_pointing` (ledger under the other arm), `bertillon_triumphant` (fist up), `bertillon_tired` (slumped) |
| `inspector17` | `inspector_laughing` (head back, belly, held open mouth), `inspector_pointing_mock`, `inspector_arms_crossed`, `inspector_shouting` (cupped hand), `inspector_shocked` (jaw drop), `inspector_seated_stiff` (in the chair, `seat17="chair"`), `inspector_red_faced` (`flush17=1`, furious, steam) |
| `prefect` | `prefect_neutral`, `prefect_finger_up_three` (3 months), `prefect_stern` |
| `dupont` | `dupont_innocent` (shrug), `dupont_held` (arms out low), `dupont_sweating`, `dupont_caught` (wide eyes) |
| `gendarme_a` / `_b` | `gendarme_escort_a/_b` (one arm out holding someone's arm, hand at (0.94, 0.78); `mirror=True` for the other side), `gendarme_laughing_a/_b`, `gendarme_standing_a/_b` |
| `prisoner_a/_b/_c` | `prisoner_sitting_a/_b/_c` (`seat17="bench"`), `prisoner_standing_a/_b/_c` |

33 poses; the escort grip: stand the gendarmes `cast17.ESCORT_SPACING` (1.30 D) either side of `dupont_held` (see the group at the top of `sheet.jpg`; the right-hand gendarme uses `mirror=True`). The measuring-chair ending: `inspector_seated_stiff` + `bertillon_measuring` with `mirror=True` and `hand_for_anchor` to put the jaws on the ear (second group on the sheet).

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D; `cast17.CANVAS17`)

bertillon (-1.9375, -4.8125, 1.9375, 0.125); inspector17 (-2.0625, -4.6875, 2.0625, 0.125); prefect (-2.0, -4.9375, 2.0, 0.125); dupont (-1.9375, -4.5, 1.9375, 0.125); gendarme_a (-2.0, -4.625, 2.0, 0.125); gendarme_b (-1.9375, -4.8125, 1.9375, 0.125); prisoner_a (-1.9375, -4.5625, 1.9375, 0.125); prisoner_b (-2.0, -4.375, 2.0, 0.125); prisoner_c (-1.9375, -4.3125, 1.9375, 0.125).
`python3 test_cast17.py canvas` checks every arm preset with every new prop at yaw +-0.6 (mirrored, squash 0.8-1.15), crouch, wide legs, all fx, flush, yaw +-1.2, every STORY17 pose (and mirrored), 16 phases x 4 modes x 2 facings of the cycles: all fit with at least 0.30 D of head room, and the mirror/anchor check is 0 problems.

## Files and QA

- `cast17.py` is the module; `test_cast17.py` has `sheet` (writes `sheet.jpg`: lineup with heights, escort and chair groups, every pose, 13 face states x 9 members incl. the 7 expressions, talk shapes and blinks, props + seats; mid-warm ground, labels under each image), `canvas`, `robust` (pose-key garbage + mouth rule + v2 `test_puppet.py --quick` on the 9 members; log in `run_robust.log`) and `pose NAME..` (quick look to `tmp/pose.png`).
- `stage_test.py` renders two frames in the stub room (`stage_test.png`, `stage_test2.png`, sun from either side): the cards stand on the floor, the contact decal and the sun's cast shadows fall on the floor and wall. Needs `bpy` (run it with the system python3).

## Known limits

- Sitting is drawn frontal: with `legs` crouch and no knee offset the thighs are hidden under the tunic skirt and only the shins and shoes show. A seat seen from the side needs a yaw near 0.6 and gives splayed knees; the bench / chair is a flat 2D drawing, not the set's 3D chair.
- The `fist` is a bigger ink ball (the puppet hand is a ball); the `three` hand shows the three fingers small at D below 60 px.
- Pince-nez, beard and whiskers follow the face layout, not the head outline: at yaw beyond about +-0.8 the far whisker narrows and the beard slides with the mouth.
- The gendarme cape's back flap is drawn behind the arms and over the legs at knee height; at `legs="wide"` the wide stance shows under it.
- `resolve_pose` / `lerp_pose` drop `seat17`, `flush17` and `seat_w`.
