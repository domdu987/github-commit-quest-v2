# cast6.py: the cast of film 6 ("the 13th loaf", a medieval English market town, 1260s) for the v2 puppet

File: `PROJ/v3/cast6/cast6.py` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`).
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast5` is edited. On import, cast6 imports cast5 (which chains cast4, cast3, cast2, cast_ext and v2/puppet), adds entries to their tables and wraps puppet helpers on top of cast5's wrappers: `_norm` (this module's pose keys), `_face` (flour, pale), `_face_layout` (small eyes), `_hair` (bald fringe), `_hand` (counting fingers), `_prop` (new props) and `figure` (the pillory overlay, basket anchors). Each wrapper falls through, so every earlier member draws as before.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast6")
import cast6                 # registers on import (idempotent); import it BEFORE sprites / stage.sprites when you can
import puppet                # same module object: CAST now also has the nine members below
cast, pose = cast6.STORY6["kit_hold_loaf"]
f = puppet.figure(cast, pose, "kit")                                     # the 13th loaf on his palm
w = puppet.figure("henry", cast6.cycle("henry", g / 28.0, "walk"), "h") # frame g of henry's walk
a = actors.Actor("kit", "kit"); a.build(sprites.DEFAULT_CANVAS["kit"], sprite_dir, contact=True)   # as in film5/s01/shot.py
```

Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged (pose keys, the 20 expressions, `mouth`, `blink`, `gaze`, effects, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`).

## Cast (head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `kit` | `boy`, 0.64 x 0.80, legs 0.82 | **2.48** (2.70) = 0.78 of the mean adult | the apprentice: floppy linen cap slouching back (flour on it), chestnut hair **dusted white with flour**, a flour smear + speckles on one cheek, **oversized linen apron to the shins** (bib, floury patches, waist ties), slate-blue tunic with rolled sleeves, brown hose, soft boots |
| `henry` | `stout`, 1.38 x 1.10 (round as a loaf), legs 1.00 | 2.97 (3.18) | Uncle Henry: **bald with one curly tuft** and a low grey-brown fringe, **huge bushy moustache**, **small eyes** (`eye_scale` 0.70), red cheeks; brick-red tunic, rolled sleeves, big floury apron, **fat coin purse** on the apron strings |
| `inspector` | `slim`, 0.62 x 1.10, legs 1.50 (tall, thin) | 3.46 (3.72) | variant A: long **brown hooded cloak** closed with a brass ring, **face in the hood's shadow** (only two eye glints and the mouth read), tall boots |
| `inspector_royal` | same body | 3.46 | variant B, hood down: black hair (grey at the temples), age lines, stern; **royal tabard (three gold lions on red)**, navy sleeves, **gold chain of office** with a crowned medallion, the brown cloak thrown back over the shoulders, hood bunched at the neck |
| `guard1` | `slim`, 0.70 x 1.04, legs 1.40 | 3.30 (3.62) | steel **kettle hat**, mail shirt (ring pattern) + mail skirt, **red tabard with one gold lion**, belt, sword, hose, tall boots; spear (`SPEAR`) |
| `guard2` | `regular`, 0.92 x 0.98, legs 1.12 (stocky) | 2.97 (3.30) | **conical nasal helmet over a mail coif**, red beard + bushy moustache, same tabard / mail / sword |
| `woman1` | `slim` hourglass | 2.94 (3.09) | linen veil / wimple framing the face (white barbette band), green bodice, tan shawl, long brick-red skirt |
| `man1` | `regular` pear | 3.06 (3.21) | farmer: battered **wide straw hat**, sandy short beard, olive smock tunic with a rope belt and patch, rolled sleeves, short hose |
| `baker2` | `slim`, 0.56 x 1.00, legs 1.34 (thin) | 3.20 (3.35) | the other baker: droopy, sad wavy mouth, pencil moustache, age lines, white linen coif, a little flour, grey-green tunic, apron |

Distinct from the references (ref a: blue robe / yellow belt / topknot; ref b: bowler, yellow waistcoat) and from films 2-5. `lineup.jpg`, top band, shows them side by side, front and 3/4.

## New pose keys (read at draw time; like cast5's keys, `resolve_pose` / `lerp_pose` drop them: re-add them to tweened poses)

| key | range | effect |
|---|---|---|
| `basket` | dict(loaves=0..13 (12), tilt=-120..120 deg (0), pour=0..1 (0)) | the held `basket` prop: loaves piled 5-4-3 (+1 on top = 13); tilt rotates it about the handle (positive = clockwise); pour = phase of six loaves tumbling out of the low lip (animate it as a loop while counting `loaves` down) |
| `hood` | 0..1 (1) | `inspector` only: 1 = hood up, lower values slide it back off the head and fade it, < 0.5 the cloak shows the hood bunched on the shoulders |
| `pale` | 0..1 (0) | blood drains from the face: cold lavender-blue wash from the crown + four gloom lines (every cast6 member) |
| `fingers_r`, `fingers_l` | 0..5 | counting hand: that many fingers up, fanned along the forearm (henry_count) |
| `pillory` | True or dict(top=y, x=x, post=bool) | locks the figure in the pillory: an oak board (two planks, neck + wrist holes, iron hinges, padlock) is drawn over the body at `head + 0.40`, a post runs down to the feet line, and the head (everything above the board top + the head disc) and both hands are drawn again on top, so they poke through. Put the hands at `(+-0.56, cast6.PILLORY_WRIST_Y)`. Extra anchors: `pillory_top`, `pillory_neck`, `pillory_wrist_l`, `pillory_wrist_r`. Works for any person (baker2, henry) |
| `t` | float | as before (tears, steam phases) |

CAST keys (only `_cast6` members): `flour=dict(op, side)`, `eye_scale`, `hair.style="fringe"` (+ `hair.top`), `purse`, costume keys below.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` | orientation |
|---|---|---|---|
| `loaf` | round crusty cob, 0.34 D wide, scored cross, shine, flour dust; sits on the palm | loaf centre (0.145 above the hand) | upright |
| `basket` | wicker basket hanging from its arched handle (rim 0.84 wide, 0.66 tall), 12 loaves visible (pose key `basket`) | rim centre; anchors `basket_lip` (low lip, where loaves fall), `basket_centre`, `basket_base`, `basket_base_far` are added to the figure | upright, `basket.tilt` |
| `cabbage` | rotten cabbage (olive-brown, limp leaves, brown spots, stink lines), 0.38 D | centre | upright |
| `tomato` | over-ripe tomato with a bruise, wilted calyx, 0.15 D | centre | upright |
| `spear` | ash shaft 2.4 D (gripped 0.95 from the butt), steel leaf blade, butt ferrule | the point, 1.45 D ahead | follows `angle`; `cast6.SPEAR` = dict(type="spear", angle=-88) (held upright) |

Standalone pieces (SVG fragments in D units, for set dressing, flying veg, the scale pans):
- `loaf_svg(uid, r=0.17, seed)` centre (0, 0), base at y = 0.53 r.
- `loaf_pile_svg(uid, n=12, r=0.10)` pile of n loaves (5-4-3-1 rows) resting on y = 0: put it on the big scale's pans (12 / 13).
- `basket_svg(uid, loaves=12, tilt=0, pour=0)` -> (svg, anchors): handle top (0, 0), rim y 0.40, base y 0.66.
- `cabbage_svg(uid, r=0.15, rotten=1, rot)`, `tomato_svg(uid, r=0.075, rotten=1, rot, squash=0..1)` (squash 1 = the splat with drops).
- `pillory_svg(uid, post_h=2.0)` -> (svg, anchors neck / wrist_l / wrist_r / board_top / post_foot): the empty pillory, board top at y = 0.

## Cycles, lip-sync, blink

- `cast6.cycle(cast, phase, mode="walk", facing=1, base=None, arms="both", speed=1.0)` -> pose dict for one frame. `phase` 0..1 is one full cycle (two steps): `phase = frame / N` with N about 28 (walk), 16 (run), 32 (sneak), 24 (march). Modes `walk`, `run` (lean 12, pumping bent arms, high knees), `sneak` (tiptoe crouch), `march` (stiff, guards). `facing=-1` walks to screen-left by setting `mirror=True` (what `base` holds in prop_r then shows in the screen-left hand). `base` keeps expr / mouth / props / fx; `arms="l"` swings only the left arm (keep a loaf or spear in the right: then set `arm_r` yourself after the call). The feet stay planted: slide the actor along the floor about 0.62 x leg length x stride per half cycle (walk ~0.5 D per step for an adult, kit ~0.35 D).
- `cast6.talk_mouth(frame, level=1.0, seed=0, hold=2)` -> mouth name (`flat` / `talk_a` / `talk_b` / `talk_o`), a new drawing every 2 frames, deterministic. Put it in `pose["mouth"]` while the line plays; `level` 0 = silent.
- `cast6.blink_at(frame, period=96, offset=0)` -> 0 / 1 / 2 (half, closed, half on frames 0-2 of every period); or use `anim.blink` as film 5 does.
- `cast6.NOD` = pitch keys of one slow nod (inspector_nod).

## STORY6 (`cast6.STORY6[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast6.STORY6_META[name]["note"]`

| name | cast | what |
|---|---|---|
| `kit_watch_steam` | kit | looking up happily at the steam, hands clasped |
| `kit_hold_loaf` | kit | the 13th loaf held up on the palm (screen-right), grinning |
| `kit_slip_loaf` | kit | sneaking the loaf into a customer's basket, glancing back |
| `kit_hold_basket` | kit | basket of 13 hanging from his hand |
| `kit_scared` | kit | cowering while henry yells |
| `kit_think` | kit | hand on the chin (re-weighing in the afternoon) |
| `kit_shout_run` | kit | running, shouting, loaf held high |
| `kit_put_loaf` | kit | placing the loaf on the scale pan (prop_tip_r = loaf centre) |
| `kit_proud`, `kit_run`, `kit_sneak` | kit | fists on hips / run frame / sneak frame with the loaf |
| `henry_yell` | henry | furious, pointing, steam + anger fill 0.55, mouth talk_b |
| `henry_laugh_smug` | henry | belly laugh, eyes shut, tears; meta `smug` = the smug variant keys |
| `henry_count` | henry | counting on 3 fingers (fingers_r), other fist on the hip |
| `henry_pale` | henry | shocked, `pale` 1, hands up |
| `henry_dragged` | henry | arms out to both sides (guards hold hand_r / hand_l), heels in, pale |
| `henry_shoo` | henry | shooing kit away |
| `henry_in_pillory` | henry | in the pillory, pale, sweating |
| `henry_add_13th` | henry | the ending: puts the 13th loaf in, smiling |
| `henry_walk` | henry | walk frame |
| `inspector_hooded`, `inspector_buy`, `inspector_walk` | inspector | the hooded stranger (buy: takes the basket of 12) |
| `inspector_hood_drop` | inspector | both hands throwing the hood back (`hood` 0.45; animate 1 -> 0, then cut to inspector_royal on a blink) |
| `inspector_reveal`, `inspector_stern`, `inspector_nod`, `inspector_royal_walk` | inspector_royal | revealed / pointing "short weight!" / the slow nod (`NOD`) / walk |
| `inspector_pour` | inspector_royal | pours the basket onto the big scale (screen-right): tilt 62, pour 0.35, loaves 7; left hand lifts `basket_base`, loaves fall from `basket_lip` |
| `guard_stand`, `guard_drag`, `guard_point`, `guard_march` (+ `_guard2`) | guard1 / guard2 | spear upright / hauling (open hand grabs henry's hand) / pointing / march frame |
| `town_laugh`, `town_point`, `town_raise_veg`, `town_throw`, `town_walk` (+ `_man1`) | woman1 / man1 | laughing + pointing / jeering point / raising a rotten tomato (woman1) or cabbage (man1) overhead / release frame of a throw (fly `tomato_svg` / `cabbage_svg` from prop_tip_r) / walk |
| `baker2_pillory`, `baker2_pillory_flinch` | baker2 | locked in the pillory, sad / flinching as veg hits |
| `baker2_sad`, `baker2_swear` | baker2 | head down / "my bread was exact!" |

51 poses.

## With the v3 stage

Exactly as cast5 (see `stage_test.py` -> `stage_test.png`: kit with the loaf, henry in the pillory, the hooded inspector, key from screen-right, `head_flip` on, Cycles 360x640, 2 threads). Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D):

| member | canvas |
|---|---|
| kit | (-1.5625, -3.875, 1.5625, 0.1875) |
| henry | (-1.8125, -4.375, 1.8125, 0.125) |
| inspector, inspector_royal | (-1.6875, -4.875, 1.6875, 0.125) |
| guard1 | (-1.6875, -5.5, 1.6875, 0.125) |
| guard2 | (-1.75, -5.0625, 1.75, 0.125) |
| woman1 | (-1.6875, -4.3125, 1.6875, 0.25) |
| man1 | (-1.75, -4.4375, 1.75, 0.125) |
| baker2 | (-1.6875, -4.5625, 1.6875, 0.125) |

Checked: every arm preset with loaf / basket (13, tilt +-90, pouring) / cabbage / tomato at yaw +-0.6 (mirrored, squash 0.8-1.15), guards also with the spear upright and at -70, crouch, wide legs, all effects + pale, yaw +-1.2, the pillory, hood 0..1, every STORY6 pose and 16 phases x 4 modes x 2 facings of the cycles, >= 0.34 D head room. A spear held level (pointing at someone) is 2.4 D long and is cut by the canvas: pass a wider canvas to `Actor.build` for such a shot.

## Files and QA

- `cast6.py`: the module. `test_cast6.py`: `lineup` -> `lineup.jpg` (one sheet: heights front + 3/4; all 51 STORY6 poses; walk ->, run ->, walk <- cycles at 8 phases for every member; mouths talk_a / talk_b / talk_o / flat, blink 1 / 2, angry, laughing, shocked, pale for every member; all props), section PNGs in `tmp/`; `canvas` (+ head_flip anchor check); `robust` (pose-key garbage on the nine members + v2 `test_puppet.py --quick` on them).
- `stage_test.py` -> `stage_test.png`.

## Known limits

- The hood shadow is a hard band over the upper face (eye glints drawn on it); `hood` between 0.15 and 0.5 is a transition (slides back, fades): animate it over a few frames, do not hold it.
- The pillory re-draws head and hands from the same figure through a `<use>` clip (Chromium renders it; the sprite pipeline uses Chromium). Hands not at the wrist holes still get drawn over the board (circles 0.115 D around hand_r / hand_l).
- Falling loaves of `pour` are drawn inside the figure (max ~0.6 D below the lip); for a long fall onto the scale, fly `loaf_svg` sprites instead.
- Apron / cloak / tabard skirts are fixed to the torso: in deep crouches the legs come out under them; kit's run is mostly read through the lean, the arms and the feet below the apron.
- `cycle()` drives legs, arms, lean and head bob only; the actor's travel along the floor is the shot's job.
