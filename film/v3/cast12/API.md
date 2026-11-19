# cast12.py: the cast of film 12 ("ไอ้ร่มเดินได้", London 1750s, Jonas Hanway and the umbrella, rain) for the v2 puppet

File: `PROJ/v3/cast12/cast12.py` (PROJ = the `proj` folder that holds `v2/` and `v3/`). Python 3 stdlib only, deterministic.
Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast12 imports cast10, which chains cast9 .. cast_ext and v2/puppet. It then adds
entries to their tables and wraps the puppet helpers on top of cast10's wrappers: `_norm` (pose keys), `_face` (mutton chops, noses), `_ink_limb`
(white stockings, buckled shoes), `_prop` (umbrellas, whip, cabbage12 ...) and `figure` (mud / wet drips / coach box). Each wrapper falls through to the earlier
ones, so every earlier member draws exactly as before; `test_cast12.py` proves it (324 earlier STORY poses, 28 of them STORY10, + 828 generic poses on 69
earlier members: byte-identical SVG).

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast12")
import cast12                 # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                 # same module object: CAST now also has the 12 members below
cast, pose = cast12.STORY12["hanway_stroll_smug"]
f = puppet.figure(cast, pose, "f")                                        # f["anchors"]["umb_top_r"] = apex of the umbrella
p = dict(cast12.STORY12["coachman_point_mock"][1], mouth=cast12.talk_mouth(g, 1.0), blink=cast12.blink_at(g, 90))      # lip-sync frame g
cast, w = cast12.cycle_frame("hanway_walk_umbrella", g / 28.0, facing=1)  # walk frame (facing=-1: mirror=True)
cast, w = cast12.cycle_frame("crowd_man_a_rush", g / 16.0, facing=-1)     # run frame
a = actors.Actor("han", "hanway"); a.build(sprites.DEFAULT_CANVAS["hanway"], sprite_dir, contact=True)     # contact shadow via the actor contact canvas
box = dict(pose, coach_box=1)                                             # seated figure + its own box seat (see below)
```

For film 12, copy `film10/common.py` and put `cast12` in place of `cast10` in the path list and the import. Everything in `v2/puppet/API.md`
and `v3/cast*/API.md` still applies unchanged: pose keys, the 20 expressions, `mouth` including `("open", w, h)`, `blink`, `gaze`, the fx, anchors,
`mirror` (use it for facing screen-left), `tint`, `ink`, `rim`, `lerp_pose` and `hand_for_tip`.
Earlier casts' prop names stay valid; **the cabbage prop is called `cabbage12`** because film 6 already owns `cabbage`.

## Cast (head D = 1; "head top to soles" standing, hat top in brackets; screen-right is yaw > 0)

| key | build | height | look |
|---|---|---|---|
| `hanway` | `slim`, lean | 3.28 (3.50) | powdered short **wig** with two side curls and a ribboned **queue**, black **tricorn** (grey braid), long mid-navy **frock coat** with brass buttons and white cuffs, buff waistcoat, white stock + lace jabot, dark breeches, **white stockings**, buckled shoes; calm, a little smug |
| `coachman` | `stout` | 3.19 (3.35) | the head coachman: big belly, **red bulb nose and cheeks**, grey **mutton chops** + bushy moustache, low round **felt hat** (brass buckle), drab-olive **greatcoat with 3 capes**, red wool scarf, big boots; the **whip** is a prop |
| `coachman_b` | `slim`, tall | 3.48 (3.83) | thin, **long pink nose**, thin moustache, sagging brown **slouch hat**, brown 2-caped coat, mustard scarf |
| `coachman_c` | `stout`, short | 2.71 (2.82) | round, **bald under a flat cloth cap**, red cheeks and nose, short dull-green 1-caped jacket, blue scarf |
| `crowd_man_a` | `regular` | 3.06 (3.28) | brown frock coat, powdered wig, black tricorn |
| `crowd_man_b` | `slim` | 3.16 (3.38) | burgundy coat, **ginger natural hair** under the tricorn |
| `crowd_man_c` | `stout` | 2.87 (3.09) | grey-green coat, wig, grey moustache, ruddy |
| `crowd_man_d` | `slim`, tall | 3.20 (3.42) | ochre coat, brown hair, brown moustache |
| `crowd_woman_a` | `regular` | 2.91 (3.12) | rose gown, ochre shawl, white fichu and apron, cream bonnet with a teal ribbon |
| `crowd_woman_b` | `slim` | 2.90 (3.11) | teal gown, terracotta shawl, straw bonnet with a red ribbon |
| `passenger_a` | `regular` | 2.96 (3.18) | slate-grey coat, wig, tricorn (coach passenger) |
| `passenger_b` | `regular` | 2.91 (3.12) | plum gown, lilac shawl, cream bonnet (coach passenger) |

Heights stay far above the caption band in medium framings (heads at about 3.0 D: with D = 110 px the head top is 330 px over the soles). Colours were chosen to
sit on the blue-violet rain set: warm rose / ochre / burgundy / olive coats, a mid-navy (not near-black) coat for Hanway, white stockings, wigs and jabot as the
light accents. Tint variants: the crowd is already six different colourways; for more, pass `tint="#c8c4f0"` (dusk) with `ink="#1e142e"`, or the `soaked` key below.

CAST keys of the module: hat_style `tricorn12` (hat_colors base/light/dark/bind/btn/wig/wig_d; CAST `wig=False` = natural hair in `hair.color`), `roundfelt12`, `flatcap12`,
`slouch12`, `bonnet12` (ribbon, frill); costume `frockcoat12`, `greatcoat12` (`capes`, `coat_len`), `dress12`; `chops12=dict(color, light)`; `nose12=dict(kind="bulb"|"long", color, r)`;
`stocking12=dict(color, shade, buckle)`.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `umb_open` | 0..1 (1) | opening of the prop `umbrella_black` / `umbrella_pink` / `umbrella_small`: 0 furled, 0.5 half, 1 open. Animate 0 -> 1 over ~12 frames for the umbrella pop (types `*_closed` are always furled) |
| `umb_col` | black / pink / maroon / green / navy / tan (maroon) | colour of `umbrella_small` |
| `egg_splat` | 0..1 (0) | smashed egg on the dome of the black umbrella: albumen, yolk, shell bits, runs. Animate 0 -> 1 on impact |
| `leaf_stick` | 0 / 1 (0) | a cabbage leaf stuck on the black umbrella's dome |
| `mud` | 0..1 (0) | **mud-splattered variant**: brown splats appear one by one over face, hat, shoulders, coat, knees, stockings, hands, with runs at > 0.6. Works on every member |
| `soaked` | 0..1 (0) | rain-soaked: a mild blue-grey tint (unless `tint` is set) and drips falling from the brim, chin, hands, hem (animate with `t`, 0.4 s loop) |
| `hat_off` | 0 / 1 (0) | no tricorn (the wig / hair stays); use with prop `tricorn_held` to hold the hat over the head |
| `wig_off` | 0 / 1 (0) | bare head (no wig, no hat), for the wig-wringing gentleman |
| `coach_box` | 0 / 1 (0) | draws a coach-box seat behind a seated figure: red hammercloth cushion with gold fringe on a dark-green panel, top 0.06 D under the hip (`box_w` 2.3 D). Anchor `box_top`. Leave 0 when the set provides the box |
| `whip_t` | float (0) | phase (0..1 loop) of the lash's wave |
| `purse_open` | 0..1 (0.5) | coins showing over the mouth of the purse |
| `t` | float | drives the drips and tears |

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended). The hand is the grip; always pass `angle` for umbrellas and the whip

| type | drawing | `prop_tip_*` | orientation / anchors |
|---|---|---|---|
| `umbrella_black` | the **big black umbrella**: dome 2.0 D wide when open (`umb_open`), 8 ribs with light edges, silver tip ferrules, brass finial, steel shaft, wooden crook handle | the apex (1.95) | `angle` = direction of the apex from the hand (-90 up; -100 leans over the person to the left; 96 = held as a cane tip down). Anchors `umb_top_r/l` (apex), `umb_mid_*` (middle of the canopy), `umb_edge1_*`, `umb_edge2_*` (hem ends), `umb_handle_*`. Rain falls on `umb_mid`. A rim sits ~1.4 D above the hand when open, so hold the hand at chest height (y 0.1..0.6 in the head frame) |
| `umbrella_black_closed` | the same furled with a strap and button | apex | as above; used as a cane (angle 90..100, `scale` 0.85) or raised (-60) |
| `umbrella_pink` | **the wife's pink frilled lace umbrella**: hot-pink dome (light ribs), a **lace frill** of white scallops with pink eyelets all round the hem | apex | as the black one. Open or `umb_open` |
| `umbrella_pink_closed` | furled, pink with a frilled hem | apex | |
| `umbrella_small` | a woman's umbrella; colour by `umb_col`; use `scale` 0.78 | apex | angle -100..-105 (tilted back over the shoulder) |
| `whip` | the long coach whip: grip, 1.05 D stock with red bands, a **lash** 1.5 D long that droops and waves (`whip_t`) | the stock tip | follows `angle`. Anchors `whip_stock_*` (stock tip), `whip_tip_*` (end of the lash) |
| `cabbage12` | a cabbage 0.38 D across held on the hand | its centre | anchor `cabbage_*` (spawn the flying cabbage there) |
| `egg` | a hen's egg held in the fingers | centre | anchor `egg_*` |
| `purse` | **coin purse** hanging by its drawstring, coins peeking out (`purse_open`) | bottom (0.37) | always upright. Anchor `purse_bottom_*` |
| `coins` | three gold coins on the palm | above the palm | upright. Anchor `coins_*` |
| `tricorn_held` | the owner's tricorn, held by the brim over the head (use `hat_off=1`, the arm `layer="top"`, hand at about (shoulder.x + 0.1, -0.34), `stretch` 1.25) | | anchor `hat_held_*` |
| `wig` | a soaked wig with a drip (animate with `soaked`/`t`) | | held at chest height |

Standalone pieces (SVG fragments in D units, id-safe with your own `uid`): `umbrella_svg(uid, kind, open_, egg, leaf)` (kind black / pink / maroon ..., grip at (0, 0), apex at y -1.95),
`cabbage_svg(uid, rot)`, `egg_svg(uid, rot)`, `egg_splat_svg(uid, r)`, `purse_svg(uid, open_)`, `coin_svg(uid, r, tilt)`, `whip_svg(uid, t)`, `coach_box_svg(uid, w, h)`.
Use `cabbage_svg` / `egg_svg` for the flying vegetables in a throw arc (rotate it yourself), and `egg_splat_svg` for a splat on a surface.

## Cycles, lip-sync, blink

`cast12.cycle(cast, phase, mode, facing, base, arms, speed)`, `talk_mouth(frame, level, seed, hold)`, `blink_at(frame, period, offset)` and `NOD` are re-exported from cast6 and work for every member.
`cast12.cycle_frame(name, phase, facing, speed)` returns `(cast, pose)` for the cycle that belongs to a story pose (the base pose with the umbrella / hat / soaked state is
stored in `cast12.CYCLE_BASE12[name] = (cast, mode, base, arms)`): `hanway_walk_umbrella`, `hanway_walk_closed`, `hanway_smile_walk`, `crowd_man_{a,b,c,d}_walk_hat` / `_walk_soaked` /
`_rush`, `crowd_woman_{a,b}_walk_umbrella` / `_rush`. Walk = 28 frames per cycle at 30 fps, run = 16. `facing=-1` mirrors (the umbrella then shows in the screen-left hand).

**Mouths:** every pose holds one fixed mouth. Only the head coachman's quote poses are meant to have `mouth = talk_mouth(g)` driven (`STORY12_META[name]["lipsync"] = True`):
`coachman_point_mock` (quote 1, "ผู้ชายกางร่มเหรอ", 12.66-15.5 s, shot 7), `coachman_boast` (quote 1 part 2, "...ร่มลูกไม้สีชมพูของเมียข้าเอง", 15.5-19.0 s, shot 8),
`coachman_shout` (quote 2, 33.0-34.9 s, shot 14), and their `coachman_box_*` seated twins. Outside the quotes set `mouth="flat"` (or keep the pose's own
held mouth for the laughs). All other poses, including every laugh, hold a fixed mouth: no mouth movement outside the quotes.

## STORY12 (`cast12.STORY12[name] = (cast, pose)`, also merged into `puppet.STORY`; `STORY12_META[name]["note"]`): 111 poses

| names | what |
|---|---|
| `hanway_walk_umbrella`, `hanway_stroll_smug`, `hanway_calm_front`, `hanway_smile_walk`, `hanway_walk_closed` | calm walk under the open umbrella; **dry smug stroll** (chin up, hand behind back); standing front; the smiling ending walk; furled umbrella as a cane |
| `hanway_cabbage_flinch` | umbrella knocked back by the cabbage, a leaf stuck on it (`leaf_stick`), unbothered (shots 3, 10) |
| `hanway_egg_tilt` | **egg splat** on the umbrella top (`egg_splat`), umbrella tilted, glancing up (shot 11) |
| `hanway_mud_splash`, `hanway_mud_deadpan` | the **mud-splashed comic pose** (`mud=1`: shocked, umbrella flung, arms out) and the deadpan aftermath (shot 12) |
| `coachman_laugh`, `coachman_box_laugh` | **belly laugh**, hands on the belly, tears (shot 6); the `_box_` twin is seated on the coach box |
| `coachman_point_mock`, `coachman_boast`, `coachman_shout` (+ `coachman_box_*`) | **mocking point** with the whip at Hanway (screen-right), **chest-out boast**, **shout** with the whip raised. All three LIP-SYNC |
| `coachman_gloat`, `coachman_nod`, `coachman_grin_drop` (+ box) | head back grinning, arms akimbo; smug nod; the grin drops (stunned, sweat) |
| `coachman_count_coins`, `coachman_count_coins_sky` (+ box) | **counting coins**: looking down at the purse, coins in the other palm / looking up at the rain, grinning |
| `coachman_throw_windup`, `coachman_throw_release` (+ box) | **throw**: arm back with a cabbage; arm snapped forward, hand open, shouting |
| `coachman_sulk_under_pink_umbrella`, `coachman_sulk_standing` | the ending: **seated on the coach box under the pink frilled umbrella**, chin on his hand, sulking; the same standing |
| `coachman_b_*`, `coachman_c_*` | `laugh`, `point_laugh`, `glare`, `nod`, `roar`, `throw_windup` (cabbage), `throw_release`, `throw_egg_windup` (egg in hand); standing and `_box_` seated |
| `crowd_man_{a,b,c,d}_walk_hat` | **hunched walk, hat held over the head**, soaked tint (animate with `cycle_frame`) |
| `crowd_man_*_walk_soaked`, `_point_laugh`, `_rush`, `_push` | hunched soaked walk; pointing and laughing; **rushing** run frame; **pushing** through the crowd (both arms forward) |
| `crowd_man_{a,c,d}_wring_wig` | a soaked gentleman wrings his wig (shot 5) |
| `crowd_man_{a,c,d}_open_1` / `_open_2` / `_open_3` | **gentleman opening his umbrella, 3 stages**: furled in the hand, staring; half open (`umb_open=0.5`), surprised; fully open overhead, smiling. Animate `umb_open` 0 -> 1 with the type `umbrella_black` (shots 19-20) |
| `crowd_woman_{a,b}_walk_umbrella`, `_dry_pass`, `_point_laugh`, `_rush`, `_push` | women under a small umbrella: walk, passing dry and smug (shot 5), pointing and laughing, rushing, pushing |
| `passenger_{a,b}_seated`, `_peek`, `_laugh` | coach passengers: seated (thighs forward), leaning out to look, laughing |

Seated poses use a `legs` dict with absolute `foot_r` / `foot_l` targets (thighs forward, shins down); the long coats cover the lap, so with the set's coach body in front they
read as seated. Pass `mirror=True` to face screen-left (anchors come back mirrored).

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D; wide because of the whip lash and the umbrella)

| member | canvas |
|---|---|
| hanway | (-3.3125, -5.375, 3.3125, 0.1875) |
| coachman | (-3.6875, -5.3125, 3.6875, 0.25) |
| coachman_b / coachman_c | (-3.3125, -5.625, 3.3125, 0.125) / (-3.4375, -4.75, 3.4375, 0.1875) |
| crowd_man_a / b / c / d | (-3.3125, -5.125, ..) / (-3.3125, -5.25, ..) / (-3.375, -4.875, ..) / (-3.3125, -5.3125, ..), bottom 0.125 |
| crowd_woman_a / b | (-3.3125, -4.9375, 3.3125, 0.25) / (-3.3125, -5.0, 3.3125, 0.25) |
| passenger_a / b | (-3.3125, -5.0, 3.3125, 0.125) / (-3.3125, -4.9375, 3.3125, 0.4375) |

`python3 test_cast12.py canvas` checks every arm preset with cabbage12 / purse / whip (and the black umbrella on the low arm presets) at yaw +-0.6 (mirrored, squash 0.8-1.15),
crouch, wide legs, yaw +-1.2, mud + soaked + tears, every STORY12 pose (mirrored too) and 16 phases x 4 modes x 2 facings of the cycles. All fit with at least 0.32 D of head room.
head_flip (mirror consistency of feet / head / hands anchors): 111 poses, 0 problems.

## Files and QA

- `cast12.py` is the module; `test_cast12.py`: `python3 test_cast12.py` runs regression + canvas + head_flip + garbage robustness, prints `ALL OK`, and writes `sheet.jpg`
  (heights with film 10's admiral for scale / 56 key poses / 18 face states per member / every prop / mud, egg and soaked variants) and `sheet_all_poses.jpg` (all 111 poses).
  Modes: `sheet`, `canvas`, `regress`, `robust` (garbage keys + the v2 `test_puppet.py --quick` on the new members).
- Everything sits on a neutral warm grey ground with a dark label under each image.

## Known limits

- The tricorn is a flat front-view drawing (crown + folded front flap + braid); at yaw beyond about 0.9 the flap point stays frontal. Its black reads well on the warm sheet but is darker than the navy coat: keep a rim light or the `rim` pose key behind it on very dark set areas.
- Hanway's coat is a mid-navy, not near-black, on purpose (the rain set is blue-violet); under a heavy `tint` it can merge with the wet street.
- The umbrella is a front-view dome that rotates with `angle`; it has no real depth: seen from below (high-angle set shots) use the dome silhouette only. The rain / drip effects on the canopy are the set's job (anchor `umb_mid_*`).
- The egg splat sits at a fixed spot on the dome (near the apex); `egg_splat_svg` gives a free-standing splat for other spots.
- Seated poses hide the legs under the coat; the box seat (`coach_box=1`) is a flat cushion + panel, not the 3D coach.
- `soaked` darkens the head skin slightly too (tint multiplies every fill); the wig-wringing pose has a bare head by design.
- Mud splats are a fixed pattern in anchor space (they follow the pose but not the cloth folds); some may sit off the body when arms are far from it.
- `resolve_pose` / `lerp_pose` drop the cast7..12 keys. Re-add `umb_open`, `umb_col`, `egg_splat`, `leaf_stick`, `mud`, `soaked`, `hat_off`, `wig_off`, `coach_box`, `whip_t`, `purse_open` and `t` to tweened poses.
- Prop `umbrella_*` needs an explicit `angle` (the default follows the forearm and points the umbrella sideways).
