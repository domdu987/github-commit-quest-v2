# cast21.py: the cast of film 21 ("ไอ้ชาวนาบนเนิน", Stirling Bridge, 11 Sept 1297) for the v2 puppet

File: `film/v3/cast21/cast21.py`. Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast21 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to their tables and wraps the puppet helpers on top of cast10's wrappers: `_norm` (pose keys of this module), `_face` (puffed cheeks, grass stalk, splutter spray, wet drops), `_prop` (new props) and `figure` (horse cards, mounted riders, swimming crop cards, floating helmets, colour variants). Each wrapper falls through to the earlier ones, so every earlier member draws exactly as before (`test_cast21.py robust` draws film 8-17 members and compares cast10's admiral with and without cast21).

```python
import sys
sys.path.insert(0, "film/v3/cast21")
import cast21                       # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                       # same module object: CAST now also has the members below
cast, pose = cast21.STORY21["cressingham_pointing"]
f = puppet.figure(cast, cast21.speak(pose, g), "f")                    # lip-sync ONLY through speak(): mouth = talk_mouth(g)
p, dy = cast21.laugh(cast21.STORY21["cressingham_laughing"][1], g)    # laughing + bounce at frame g; lift the card by dy D
h = puppet.figure("horse", cast21.horse_pose(g / 40.0, "walk", "red"), "h")            # side-view horse card
r = puppet.figure("knight_a_mtd", dict(cast21.STORY21["knight_a_mounted"][1], gait=g / 40.0), "r")   # knight parented to the horse
w = puppet.figure("footman_a", cast21.STORY21["footman_a_swim_splutter"][1], "w")      # head and shoulders in the water, cropped at the waterline
c = puppet.figure("scot_a", cast21.run_spear("scot_a", g / 16.0, facing=1), "c")      # run with the spear forward
a = actors.Actor("cre", "cressingham"); a.build(sprites.DEFAULT_CANVAS["cressingham"], sprite_dir, contact=True)
```
For film 21 copy the previous `common.py` and put `cast21` in the path list and the import. Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies: pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`. Actor/sprite use is the same for every key below, including `horse`, the `*_mtd` riders and `helmet_float` (their canvases are in `CANVAS_SPECIAL21`, registered into `sprites.DEFAULT_CANVAS`). All canvases are multiples of 1/16 D.

## Cast (head D = 1, plum ink `#3a2832`, head fill `#fef7f6`)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `cressingham` | `stout` 1.40 x 1.16, legs 1.20 | 3.23 (3.54) | the mocker: stout, ruddy, **clean-shaven double chin**; crimson robe to the shins with **gold trim** down the front and round the hem, **fur collar**, gold belt, **gold chain with a blue stone**, **fat leather coin purse** at the belt (screen-right hip); crimson **fur-trimmed cap** (a fur band, gold brooch, a short feather) |
| `surrey` | `regular` 0.88 x 1.04, legs 1.30 | 3.20 (3.32) | old Earl of Surrey: **grey beard**, **mail coif**, mail sleeves and skirt, **gold-and-blue chequered surcoat** (squares only, no text) |
| `knight_a` | `regular` 1.00 x 1.08 | 3.26 (3.48) | English knight: mail, **red surcoat with a gold lion**, **great helm** (flat-topped steel pot, red plume; face opening kept so every expression reads) |
| `knight_a_open` | same body | 3.26 (3.64) | same, **open-face bascinet** (steel dome, mail aventail, small red plume), moustache |
| `knight_b` | `slim` 0.78 x 1.10, legs 1.42 | 3.38 (3.76) | tall knight: mail, **blue surcoat with a white chevron**, open-face **bascinet** |
| `knight_b_great` | same body | 3.38 (3.60) | same, great helm with a blue plume |
| `footman_a` | `regular` 0.92 x 1.00 | 3.04 (3.36) | English foot soldier: padded **gambeson** (quilted channels, belt, short skirt), **kettle hat**, bushy moustache |
| `footman_b` | `slim` 0.72 x 1.04, legs 1.34 | 3.24 (3.56) | taller, thinner, indigo gambeson, olive-grey kettle hat, no moustache |
| `wallace` | `regular` 0.96 x 1.14, legs 1.58 | 3.59 (3.76) | tall and strong: **long brown hair**, short beard, **mail shirt over a dark-green tunic** (green shows from mid-thigh), leather belt, **long sword on his back** (hilt over the far shoulder, baldric, scabbard tip) |
| `moray` | `slim` 0.80 x 1.06 | 3.32 (3.44) | younger: mail coif, mail, **green surcoat**, black hose |
| `scot_a` | `regular` | 3.18 | Scots spearman, bare head (black hair), bushy moustache, **brown** knee-length tunic with rope belt, no kilt |
| `scot_b` | `slim` | 3.36 (3.60) | **iron cap**, **ochre** tunic |
| `scot_c` | `stout` | 3.07 | ginger hair and beard, **moss** tunic |
| `scot_horn` | `regular` | 3.16 | the horn blower, bare head, **faded red** tunic |
| `horse` | side view | withers 2.55, ears 3.65 | see Horse. Pose keys `gait`, `mode21`, `horse21` |
| `knight_a_mtd`, `knight_a_open_mtd`, `knight_b_mtd`, `knight_b_great_mtd`, `surrey_mtd`, `moray_mtd` | rider + horse | | the knight sits on a horse card (see Riders) |
| `helmet_float` | | | a helmet bobbing on the water (see Splash) |

Colour variants: `footman_a_v1..v3`, `footman_b_v1..v3` (gambeson russet / ochre / indigo / plum / olive, none teal), `scot_a_v1..v3`, `scot_b_v1..v3`, `scot_c_v1..v3` (tunics brown / ochre / moss / faded red). Pose key `variant21` (int) picks one: `figure("footman_a", dict(pose, variant21=2))` draws `footman_a_v2`; `cast21.VARIANTS21["scot_a"]` lists the keys. Costumes are mid-dark: nothing is near-white except faces, the chevron, collars and mail highlights; `sheet.jpg` shows every member on `#6f9a4e` (meadow) and on teal `#2f7f8c`. NO text, NO blood, NO wounds anywhere (the heraldry is lion / chevron / chequers only).

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `puff21` | 0..1 (0) | puffed cheeks (two round bulges at the mouth corners): the horn blower |
| `stalk21` | 0..1 (0) | a **grass stalk** in the corner of the mouth, sticking out toward the facing side (mouth stays closed) |
| `spit21` | 0..1 (0), `t` animates | water spray from the mouth (spluttering) |
| `wet21` | 0..1 (0), `t` animates | drops running down the face |
| `shield21` | `"ochre"` / `"red"` / `"blue"` / `"green"` / `"plain"` | colour of a `shield21` prop in this pose |
| `sheath21` | 0 / 1 (CAST) | Wallace: 0 hides the sword on his back (use it when he holds the drawn sword) |
| `swim21` | 0.4 .. 2.2 | **swimmer**: the figure is cropped at a waterline `swim21` D below the head centre and a foam ring (ellipses, a teal wash, droplets) is drawn at the cut; `feet` anchor and `feet_y` = the waterline, so the actor stands on the water surface. Works on every English member (and any cast21 member); vary it with `t` to bob. Default look 1.0 (head, shoulders, a little chest) |
| `variant21` | int | colour variant (above) |
| `gait`, `mode21`, `horse21` | | horse / rider cards: walk phase 0..1, `"walk"` / `"idle"`, caparison `"red"` / `"blue"` / `"gold"` / `"plain"` |
| `helm21`, `tilt` | `"kettle"` / `"bascinet"` / `"great"` | floating helmet kind and tilt (degrees) |

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended; long axis along +x of the hand frame, `angle` degrees, SVG, -90 = up)

| type | drawing | `prop_tip_*` / anchors |
|---|---|---|
| `spear21` | long Scots / English spear: ash shaft, steel leaf head, iron ferrule, 3.85 D long (butt 1.85 D behind the hand, point 2.0 D ahead). `angle=-90` upright, `-4` level (spear wall) | point (2.0). Anchors `grip_far_r/_l` (0.8 D behind the hand: put the other hand there, see `_grip_hand`), `spear_butt_*`, `spear_tip_*` |
| `shield21` | round shield 1.0 D across (planks, iron rim, boss); always upright, centred on the hand; colour by `shield21` pose key | anchor `shield_*` |
| `horn21` | long curved cow horn, mouthpiece at the hand, bell up to 0.95 D out | tip 0.95; anchor `horn_mouth_*` = mouthpiece |
| `sword21` | long sword (grip, gold crossguard and pommel, steel blade 1.35 D). `angle=-82` raised | tip 1.35 |
| `coin21` | one gold coin pinched between the fingers (`scale` 2.0 reads at phone size) | |

Standalone SVG fragments: `spear_svg`, `shield_svg(uid, col)`, `horn_svg`, `sword_svg`, `coin_svg`; `horse_parts(uid, phase, mode, cap, t)` returns `(svg, bbox, anchors)`.

## Horse (`figure("horse", cast21.horse_pose(phase, mode, cap))`)

Side view facing +x (`mirror=True` faces left). Ground y = 0 (`feet_y` 0, `feet` anchor (0, 0)), body centre x = 0, up is negative y. Body 3.3 D long, withers 2.55 D, ears at 3.65 D. Ink-outlined bay / grey / chestnut / brown coat with mane, tail, bridle, saddle, one rein and stirrup; a **caparison** (cloth with a dagged hem) in `red` (gold lozenges, gold trim), `blue` (white bars, white trim; grey horse), `gold` (red chequers, red trim; chestnut horse) or `plain` (undyed). Hem and tail flutter with the phase.

- `mode21="walk"`: a four-beat lateral walk (near hind, near fore, far hind, far fore), **`gait` = phase, one cycle about 40 frames at 30 fps** (loop `gait = (g / 40.0) % 1`); body bobs 0.03 D twice per cycle, head nods about 6 degrees, tail swishes.
- `mode21="idle"`: legs planted; **head bob** (5 degrees) and **tail swish** driven by `t` (one slow loop per 0..1; use `t = (g / 70.0) % 1`).
- Anchors: `seat` (0.30, -2.50) the rider's hips, `stirrup`, `withers`, `croup`, `tail_root`, `muzzle`, `mouth`, `head`, `head_top`, `hat_top`, `hip`, `feet`.

## Riders (`knight_a_mtd` ... `moray_mtd`)

`figure("knight_a_mtd", pose)` draws the horse and the knight in ONE card: the knight's `hip` anchor is pinned to the horse's `seat` every frame (so the rider rides the bob of the walk), the knight's own pose keys (`expr`, `arm_*`, `lean`, `squash`, `fx`, `mouth` ...) apply as usual, and the horse keys `gait`, `mode21`, `horse21` (default caparison: red for knight_a, blue for knight_b, gold for surrey, plain for moray), `t`, `mirror` apply to the whole card (the rider comes back mirrored with the horse). The default rider pose is three-quarter (`yaw` 0.9), reins hand forward, other hand on the hip, legs hanging in front of the caparison with the feet on the stirrup. Anchors: all of the rider's (`hand_r`, `prop_tip_r` ...), plus `seat`, `horse_head`, `muzzle`, `stirrup`; `feet` = the hooves. Sprites: sized by `CANVAS_SPECIAL21`.

## Expressions, mouths, blink, bounce

`cast21.EXPR21`: `neutral`, `smug`, `smirk`, `laughing` (fixed laugh drawing + tears), `shocked` (round mouth), `jawdrop` (stunned, open `("open", .17, .22)`), `worried`, **`sweat`** (worried + a sweat drop), `tired`, `angry`. `cast21.with_expr(pose, name)`. **The mouth moves only through `cast21.speak(pose, frame, level=1.0)`** (= `mouth = talk_mouth(frame)`, a new drawing every 2 frames); every other face and every story pose holds a closed mouth except the flagged open ones (laughing, shocked, yawn, splutter, jump yells; `STORY21_META[name]["open_mouth"]`). The **Scots, Wallace and Moray never have an open mouth** (the horn blower's cheeks puff on a closed mouth). `cast21.silent(pose)` shuts it. Blink: `blink=cast21.blink_at(frame, period, offset)`.
**Laughing with bounce**: `p, dy = cast21.laugh(pose, g, fps=30, hz=3.0, amp=0.06, phase=0.0)` returns the pose with the laughing face, a breathing `squash`, +-4 degree `head_roll`, a `head_dy` bob and tears, plus the lift `dy` (D, 0..0.06, one hop every 10 frames) to add to the card's height; offset `phase` per character so the camp laughs out of phase. `cast21.bounce_dy(g, ...)` gives the lift alone.

## Cast poses (`cast21.STORY21[name] = (cast, pose)`, also merged into `puppet.STORY`; `cast21.pose(name, **extra)`)

178 poses. Generic English poses exist for each of `footman_a`, `footman_b`, `knight_a`, `knight_a_open`, `knight_b`, `knight_b_great` (name = `<cast>_<pose>`):

| group | poses |
|---|---|
| `cressingham_*` | `neutral`, `smug_belt` (thumbs in the belt, chin up), `counting` (a coin in the fingers), `laughing` (head back, hands on the belly), `pointing` (arm out at the far bank; lip-sync with `speak`), `purse_slap` (hand on the purse, the other arm flung at the bridge), `shocked` (jaw drop, sweat drop), `sweating` |
| `surrey_*` | `standing` (hands clasped low), `tired` (slumped), `listening` (hand at the beard), `shocked`, `worried` |
| English on foot | `stand` (spear upright), `stand_arms_down`, `point_laugh`, `laughing`, `shocked`, `worried`, `yawn` (hand at the mouth), `tiptoe`, `bump` (knocked back, helmet wobble via head roll); footmen also `mime_hoe` (spear held like a hoe) |
| splash / jump | `jump_arms_up`, `jump_pinch_nose` (one hand on the nose, eyes squeezed), `jump_bomb` (knees up, hands on the knees), `splutter` (spray + wet face), `swim_bob`, `swim_splutter`, `swim_arms_up`, `swim_paddle` (the `swim21` crop cards) |
| riders | `<knight_a / knight_b / surrey / moray>_mounted`, and for the first three `_mounted_laughing`, `_mounted_shocked`, `_mounted_suck_belly` (squashed, sweating), `_mounted_yawn`, `_mounted_wobble` |
| `horse_walk`, `horse_idle`, `helmet_float_kettle/_great/_bascinet` | the cards |
| `wallace_*` | `calm` (arms folded), `eyebrow` (one brow raised), `raise_sword` (sword up, sheath hidden), `run_sword`, `stand_spear`, `fold_spear`, `spear_wall` |
| `moray_*` | `stand_spear`, `calm`, `fold_spear`, `spear_wall` |
| Scots (`scot_a/_b/_c`, `scot_horn`; spear poses also Wallace and Moray) | `fold_spear` (stand with the hands crossed on an upright spear), `chew_grass` (the same + stalk), `scratch_nose` (one hand at the nose), `stand_still`, `shield` (round shield on the arm + spear), `spear_wall` (spear level, both hands on the shaft via `grip_far`), horn blower: `scot_horn_blow` (long cow horn at the mouth, cheeks puffed, legs wide), `scot_horn_lower` |

Cycles: `cast21.cycle(cast, phase, "walk"/"run"/"sneak"/"march", facing, base, arms, speed)` (as cast6; `facing=-1` mirrors, so what `base` holds in `prop_r` shows in the screen-left hand), **`cast21.run_spear(cast, phase, facing)`** (run with the spear forward, one arm swinging; 16 frames per cycle), **`cast21.walk_spear(cast, phase, facing, mode="march")`** (spear carried upright). Jumps: the figure's feet stay on the ground line (puppet rule), so **lift the card 0.5 to 0.8 D for the airborne frames** and drop it into the water.

## Splash cards

`swim21` crops any member at the waterline and draws foam; place the card with its `feet` on the water surface (it is already at `feet_y` = waterline). Water colour: the ring uses a teal wash `#2a7f8c` at 55 percent plus near-white foam strokes, so it sits on the set's teal river; at other water colours it still reads. Spray droplets and `wet21` drops are pale blue with ink outlines. `helmet_float` (`helm21`) is a kettle hat (or bascinet / great helm) tilted on a foam ring; `t` bobs it; its `feet` = the waterline.

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D)

`cast21.CANVAS21` per member (about +-3.4 wide because a 4 D spear at any arm angle reaches far; heights 4.0 to 5.3 D above the feet) and `cast21.CANVAS_SPECIAL21` (horse (-3.0625, -4.25, 3.0625, 0.25), riders (-3.0625, -5.4375, 3.0625, 0.25), helmet (-1.625, -1.625, 1.625, 0.4375)). `python3 test_cast21.py canvas` checks that every story pose (and mirrored), every cycle and `run_spear` fit with at least 0.31 D head room (all ok), reports the worst-case sweep of every arm preset with every prop as information, and checks the mirror anchors (0 problems).

## Files and QA

- `cast21.py` is the module; `test_cast21.py`: `sheet` (writes `sheet.jpg` = lineup on meadow and teal, horse walk cycle, riders, cycles, props, the key poses, 13 face states x 14 members; and `sheet_all_poses.jpg` = every pose), `canvas`, `robust` (pose-key garbage on every member and special card, mouth rule, earlier casts draw, v2 `test_puppet.py --quick` on the new members; log in `run_robust.log`) and `pose NAME..` (quick look to `tmp/pose.png`).
- `stage_test.py` renders two frames in the stub room (`stage_test.png` the south bank: Cressingham, Surrey, a footman and a mounted knight; `stage_test2.png` Wallace, Scots, the horn blower, Moray): the cards stand on the floor, the contact decals and the sun's shadows fall on the floor and wall. Needs `bpy` (system python3).

## Known limits

- The great helm is the **face-open** pot with cheek plates (a closed helm with slits would hide every expression); at yaw beyond 0.8 its far cheek plate narrows.
- Riders are the front-facing puppet torso on a side-view horse (three-quarter at best): the legs hang in front of the caparison, they do not wrap the barrel. Reins are one fixed line from the bit to the saddle, not to the rider's hand.
- Horse legs are two-segment strokes with round knee joints; the hind leg's hock bend is a simple 2-bone solve, so at the lift moment the hock can look slightly stiff. The horse has no neck motion beyond the head nod and the hem flutter.
- Jump poses keep both soles on the ground line; the lift is the compositor's job.
- `swim21` is a crop plus an overlay ring, not a 3D water interaction: the cut edge is hidden by the teal wash, which is the same colour for every river.
- The spear is 3.85 D long, longer than the shot-plan "long spears" strictly need; shorten it with the prop `scale` (it scales about the hand). Spear butts can hang slightly below the soles in the folded-arms poses (about 0.1 D).
- Scots faces differ mainly by hair, beard, cap and tunic colour (one puppet head); at 56 px a head the colours carry the identification.
- Wallace's mail covers most of his torso on purpose; the dark-green tunic shows only below the mail (mid-thigh to knee).
