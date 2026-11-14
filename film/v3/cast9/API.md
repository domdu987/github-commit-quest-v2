# cast9.py: the cast of film 9 ("ไอ้ช่างขนม", sticky-rice mortar, a Ming city wall ~1370s) for the v2 puppet

File: `PROJ/v3/cast9/cast9.py` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`).
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast8` is edited. On import, cast9 imports cast8 (which chains cast7 .. cast_ext and v2/puppet), adds entries to their tables and wraps puppet helpers on top of cast8's wrappers: `_norm` (this module's pose keys), `_face` (goatee, rain on the face), `_moustache` (style `long9`), `_ink_limb` (armour shoulder guards), `_prop` (new props) and `figure` (dust cloud). Each wrapper falls through, so every earlier member draws as before.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast9")
import cast9                 # registers on import (idempotent); import it BEFORE sprites / stage.sprites (as film8/common.py does with cast8)
import puppet                # same module object: CAST now also has the 7 members below
cast, pose = cast9.STORY9["lin_stir"]
f = puppet.figure(cast, pose, "f")                                     # stirring the cauldron; f["anchors"]["blade_l"] = blade in the pot
w = puppet.figure("lin", cast9.cycle("lin", g / 16.0, "run"), "f")     # frame g of the run
p = dict(cast9.STORY9["general_mock"][1], mouth=cast9.talk_mouth(g, 1.0), blink=cast9.blink_at(g, 90))
a = actors.Actor("gen", "general"); a.build(sprites.DEFAULT_CANVAS["general"], sprite_dir, contact=True)
a = actors.Actor("genf", "general"); a.build(cast9.CANVAS9_FALL["general"], sprite_dir, contact=True)   # fall / helmet flying / dust
```

For film 9 copy `film8/common.py` and replace `cast8` by `cast9` in the path list / import (cast9 imports cast8, cast7, cast6 itself; `sys.modules["cast8"]` stays available). Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged (pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx `sweat` / `tears` / `zzz` / `blush` / `anger_fill`, cast6 `pale`, cast7 `sweat` / `lie` / `panel_grip` / `panel_side`, cast8 `pour` / `pour_side` / `pour_len` / `bucket_water`, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`).

## Cast (head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `lin` | `slim` 0.70 x 0.98, legs 1.26 | 3.10 (3.37) | young Ming mason: black hair in a **topknot bun**, light **cloth headband** tied at the back (tails), simple **blue cross-collar tunic** to mid-thigh, black sash, rolled sleeves with light cuffs, dark trousers, cloth shoes |
| `general` | `stout` 1.46 x 1.30, legs 1.36 | 3.53 (4.16) | big Ming general: iron **helmet** (gilt ribs, brow band with a jewel plaque, spike finial, **big red tassel plume**, lamellar **ear flaps**); **long drooping black moustache** + goatee, heavy brows; gilt-bronze **lamellar armour**, brass **chest mirror** on straps, iron **shoulder guards** with beast masks, red belt with jade plaques and a beast-face buckle, armoured skirt flaps + front apron over a **red robe**, red trousers, black boots |
| `worker_a` | `slim`, tall | 3.20 (3.45) | conical straw hat (cast4 `sugegasa`), ochre tunic |
| `worker_b` | `regular` pear | 2.86 (3.13) | round, bushy moustache, topknot + white headband, brown tunic, sacking-coloured sash |
| `worker_c` | `slim`, short | 2.78 (3.05) | wiry, topknot + red-brown headband, grey-green tunic, red sash |
| `gunner_a` | `regular` | 2.96 (3.31) | enemy gunner: purple felt cap with a fur brim and red tassel (`furhat9`), teal robe under a brown padded coat, moustache, boots |
| `gunner_b` | `slim` | 3.04 (3.39) | enemy gunner: red-brown fur-brim cap, blue tassel, brown robe under a drab coat |

`lineup.jpg`, top band, shows them side by side, front and 3/4.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them: re-add them to tweened poses)

| key | range | effect |
|---|---|---|
| `helmet_off` | 0..1 (0) | general (`helmet9`): 0 = helmet on. 0 < v < 1 = the head is bare (topknot with a little gilt crown) and the helmet flies along an arc up and back over the shoulder away from the facing side, spinning (v = progress; speed lines). v >= 1 = helmet gone (draw `helmet_svg()` in the rubble yourself). Animate 0 -> 1 over ~18 frames. Needs `CANVAS9_FALL` |
| `wet` | 0..1 (0) | rain on the face (cast9 members): water runs down the cheeks, drops fall beside the head / off the chin (animate `t`) |
| `dust` | 0..1 (0) | dust cloud (any cast while cast9 is loaded): merged puffs along the ground line + flying grit (animate `t`); with `lie` the cloud sits 0.35 D higher and swallows the lower body. Widens the bbox: use CANVAS9_FALL for the general |
| `trowel_mortar` | 0..1 (1) | the dollop of lime mortar on the trowel |
| `paddle_soup` | 0..1 (1) | rice soup coating the paddle blade (> 0.3: a drip falls from it, animate `t`) |
| `match_glow` | 0..1 (1) | the linstock's smouldering match (0 = dead, no smoke); smoke wisp animated by `t` |
| cast8 `pour`, `pour_side`, `pour_len`, `bucket_water` | as cast8 | also drive `soup_bucket` |
| cast7 `panel_grip`, `panel_side` | as cast7 | also how a hand holds `brick9` / `brick_stack` |
| cast7 `lie` | as cast7 | used by `general_fall` (lie=42) |

CAST keys (only `_cast9` members): hat_style `helmet9` (hat_colors light/base/dark/deep/shine, `plume9` colour), `topknot9` (hat_colors band/dark -> headband; none = bare topknot; `band_tails`), `furhat9` (hat_colors light/base/dark/shine/fur/fur_l/tassel); costume `armour9` (colors base/dark/light = armour, pauldron/pauldron_d, robe, strap, belt, jade; robe_len, robe_flare, sash_w, sash_y); `moustache_style="long9"` (+ `tache_scale`, `tache_len`), `goatee9=True`, `pauldron9=<size>`.

New anchors (only while the piece is held): `grip_far_r/_l` (where the other hand goes: paddle shaft, linstock staff, far edge of a brick / brick stack, soup bucket base while pouring), `blade_r/_l` (paddle blade centre), `trowel_tip_r/_l`, `match_r/_l` (the glowing linstock match), `piece_centre_r/_l` (bricks), `pour_lip_*` / `pour_end_*` / `bucket_base_*` (soup bucket, as cast8). Mirror and squash applied (not rotated by `lie`).

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` | orientation |
|---|---|---|---|
| `paddle` | big wooden cauldron paddle, 1.8 D (butt -0.22 .. blade end 1.57), blade coated with rice soup | blade centre (1.34) | follows `angle`; other hand -> `grip_far_*` (0.50 along). Use `scale` 1.2-1.4 for the giant cauldron |
| `trowel` | mason's pointed steel trowel, wooden handle, brass ferrule, mortar dollop | the point (0.47, 0.075) | follows `angle`; `trowel_mortar`. Story poses use `scale=1.35` |
| `brick9` | grey fired Ming wall brick 0.46 x 0.16 D (top + side faces, kiln mottle, maker's stamp) | brick centre | upright, `panel_grip` / `panel_side` |
| `brick_stack` | three bricks stacked | stack centre | as brick9; carried two-handed |
| `soup_bucket` | cast8's wooden bucket full of milky rice soup | bottom / pour lip | as cast8 `bucket`: `pour`, `pour_side`, `pour_len`, `bucket_water` |
| `linstock` | wooden staff, brass fork, slow match with a glowing ember, smoke wisp rising | the match end (1.18, 0.03) | follows `angle`; `match_glow`, `t` |

Standalone pieces (SVG fragments in D units): `helmet_svg(uid, rot, yaw, plume)` -> (svg, top) (head frame: worn on a D = 1 head at (0, 0); rotate for the flying / lying helmet), `paddle_svg(uid, soup)`, `trowel_svg(uid, mortar)`, `linstock_svg(uid, glow, t, smoke)`, `brick_svg(uid, w, h)` -> (svg, bbox), `brick_stack_svg(uid, n)` -> (svg, bbox), `soup_bucket_svg(uid, pour, side, water, pour_len)` -> (svg, anchors base/lip/end).

## Cycles, lip-sync, blink

Re-exported from cast6 (work for every member): `cast9.cycle(cast, phase, mode, facing, base, arms, speed)` with modes `walk` (~28 frames per cycle), `run` (~16), `sneak` (~32), `march` (~24); `cast9.talk_mouth(frame, level, seed, hold)`; `cast9.blink_at(frame, period, offset)`; `cast9.NOD`. Keep props / `wet` / `sweat` in `base`; with `arms="l"` set `arm_r` afterwards (lin_carry_bucket does).

## STORY9 (`cast9.STORY9[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast9.STORY9_META[name]["note"]`

| name | cast | what |
|---|---|---|
| `lin_stand`, `lin_walk`, `lin_run` | lin | stand / walk frame / run frame (worried, mouth open) |
| `lin_stir` | lin | **stirring the giant cauldron** (screen-right) with the paddle (`prop_l`, scale 1.35), lower hand on `grip_far_l`, anchor `blade_l`; animate both hands on a small ellipse |
| `lin_pour` | lin | **pouring the rice-soup bucket into the mortar** (screen-right), pour 0.85, stream to his ground line, other hand on the base |
| `lin_lay_brick` | lin | **laying a brick**: crouched, left hand pressing the brick from above (`panel_grip="top"`), trowel tapping it; anchor `trowel_tip_r` |
| `lin_trowel` | lin | spreading mortar along the course with the trowel |
| `lin_calm` | lin | **calm confident smile**, arms folded |
| `lin_rain` | lin | **looking up worried at the rain**, palm out, `wet=1` |
| `lin_watch` | lin | **watching calmly** (screen-right), hands behind the back |
| `lin_explain` | lin | open palm, talking |
| `lin_carry_bucket` | lin | walk frame carrying the soup bucket |
| `general_stand`, `general_walk` | general | akimbo, smug / walk frame |
| `general_laugh` | general | **big belly laugh**, head back, hands on the belly |
| `general_mock` | general | **pointing and mocking** (screen-right), mouth talk_b: lip-sync with talk_mouth() |
| `general_wall_laugh` | general | **arms akimbo laughing on top of his wall**, head thrown back, tears |
| `general_rain_shout` | general | **shouting in the rain** (`wet=1`), pointing screen-right, other fist up; lip-sync |
| `general_fall` | general | **comic fall** (no injury): `lie=42`, arms flailing, shocked "O", helmet flying (`helmet_off=0.45`), dust cloud; canvas `CANVAS9_FALL` |
| `general_land` | general | sitting in the rubble dust, helmet gone (topknot), still laughing |
| `workers_laugh` (+`_b`, `_c`) | worker_a / _b / _c | laughing and pointing (screen-right; `mirror=True` for left) |
| `workers_point` (+`_b`, `_c`) | " | jeering point, talk_a |
| `workers_carry` (+`_b`, `_c`) | " | **carrying a stack of bricks** in front with both hands, sweat |
| `workers_walk` (+`_b`, `_c`) | " | walk frame |
| `gunner_light` (+`_b`) | gunner_a / _b | **touching the linstock to the cannon** (screen-right, low), crouched; anchor `match_r` |
| `gunner_ears` (+`_b`) | " | **covering both ears**, eyes squeezed shut, ducking |
| `gunner_stand` (+`_b`) | " | standing with the linstock upright |

38 poses. No name collides with earlier STORY entries or CAST keys.

## With the v3 stage

Exactly as cast6/7/8 (see `stage_test.py` -> `stage_test.png`: the general mocking, lin stirring, a gunner with the linstock; key from screen-right, `head_flip` on, Cycles 360x640, 2 threads). Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D):

| member | canvas |
|---|---|
| lin | (-1.875, -4.5, 1.875, 0.125) |
| general | (-1.6875, -5.25, 1.6875, 0.125); fall / land / helmet flying / dust: `CANVAS9_FALL["general"]` (-5.4375, -5.75, 5.4375, 0.3125) |
| worker_a | (-1.4375, -4.5625, 1.4375, 0.125) |
| worker_b | (-1.5, -4.25, 1.5, 0.125) |
| worker_c | (-1.4375, -4.1875, 1.4375, 0.125) |
| gunner_a | (-1.875, -4.375, 1.875, 0.125) |
| gunner_b | (-1.8125, -4.4375, 1.8125, 0.125) |

Checked (`python3 test_cast9.py canvas`): every arm preset with soup_bucket / brick9 / brick_stack / trowel (side and bottom grip) at yaw +-0.6 (mirrored, squash 0.8-1.15), pours both sides, crouch, wide legs, all effects + wet, yaw +-1.2, every STORY9 pose (except the fall set) and 16 phases x 4 modes x 2 facings of the cycles, >= 0.32 D head room; the general's fall set (fall, land, mirrored, helmet_off sweep, dust) against CANVAS9_FALL. head_flip: 38 poses, 0 problems. The long tools (paddle, linstock) are covered only in the story poses: swung elsewhere at full reach they can exceed the canvas: pass a wider canvas to `Actor.build`.

## Files and QA

- `cast9.py`: the module. `test_cast9.py`: `lineup` -> `lineup.jpg` (heights front + 3/4; all 38 STORY9 poses; walk ->, run ->, walk <- cycles at 8 phases for every member; mouths talk_a / talk_b / talk_o / flat, blink 1 / 2, angry, wet, sweat, laughing, shocked, pale for every member; props + helmet), section PNGs in `tmp/`; `canvas`; `robust` (pose-key garbage on the 7 members + v2 `test_puppet.py --quick`, see `run_robust.log`).
- `stage_test.py` -> `stage_test.png`.

## Known limits

- The flying helmet is drawn in the head frame, so it rolls with `head_roll` and rotates with `lie`; for a precise arc across the set, use `helmet_off=1` and animate `helmet_svg()` as a separate card.
- `dust` is drawn in front of the whole figure (semi-opaque); the rubble itself belongs to the set.
- Held pieces are drawn in the arm's layer (see cast8); in `lin_stir` the lower hand on the shaft sits over the blue tunic and reads weakly at small sizes.
- `resolve_pose` / `lerp_pose` drop the cast7/8/9 keys: re-add `helmet_off`, `wet`, `dust`, `trowel_mortar`, `paddle_soup`, `match_glow`, `pour*`, `lie`, `panel_grip`, `panel_side` to tweened poses.
