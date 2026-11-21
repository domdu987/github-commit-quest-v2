# cast8.py: the cast of film 8 ("ไอ้บ้าน้ำแข็ง", ice in the desert, Persian yakhchal ~1600s) for the v2 puppet

File: `PROJ/v3/cast8/cast8.py` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`).
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast7` is edited. On import, cast8 imports cast7 (which chains cast6 .. cast_ext and v2/puppet), adds entries to their tables and wraps puppet helpers on top of cast7's wrappers: `_norm` (this module's pose keys), `_face` (long beard, double chin, heat, tear streams), `_hand` (rings), `_prop` (new props) and `figure` (anchors of held pieces / the pour). Each wrapper falls through, so every earlier member draws as before.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast8")
import cast8                 # registers on import (idempotent); import it BEFORE sprites / stage.sprites (as film6/common.py does with cast6)
import puppet                # same module object: CAST now also has the 5 members below
cast, pose = cast8.STORY8["farid_pour"]
f = puppet.figure(cast, pose, "f")                                       # pouring the bucket; f["anchors"]["pour_end_r"] = where the water lands
w = puppet.figure("farid", cast8.cycle("farid", g / 16.0, "run"), "f")   # frame g of the run
p = dict(cast8.STORY8["merchant_mock"][1], mouth=cast8.talk_mouth(g, 1.0), blink=cast8.blink_at(g, 90))
a = actors.Actor("far", "farid"); a.build(sprites.DEFAULT_CANVAS["farid"], sprite_dir, contact=True)
```

For film 8 copy `film6/common.py` and replace `cast6` by `cast8` in the path list / import (cast8 imports cast7 and cast6 itself). Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged (pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx `sweat` / `tears` / `zzz` / `blush` / `anger_fill`, cast6's `pale`, cast7's `sweat` (drops) / `lie` / `panel_grip` / `panel_side`, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`).

## Cast (head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `farid` | `slim`, 0.70 x 0.98, legs 1.26 | 3.10 (3.46) | young Persian ice-maker: off-white wrapped **turban**, bold black brows, no beard, undyed linen knee-length wrap tunic (qaba) with a madder-red trim, **indigo sash** knotted at the side, rolled sleeves, dark brown trousers, soft leather shoes |
| `merchant` | `stout`, 1.50 x 1.20, legs 1.18 | 3.25 (**3.92**) | the fat rich water merchant: **huge white silk turban** with gold band, **ruby jewel** + pearls, white aigrette plume, red kulah baton on top; **huge black handlebar moustache**, double chin; saffron silk robe under an **open crimson brocade coat** (gold diamonds, gold trim), **jewelled gold belt** on a green sash, **rings** on both hands, red slippers |
| `woman` | `slim` hourglass | 2.94 (3.11) | townswoman: deep blue **head scarf** (gold trim) over the shoulders, long terracotta dress to the ankles with a dotted trim, ochre sash |
| `oldman` | `regular` pear, 0.80 x 0.98 | 2.92 (3.30) | old man: white turban, **long white beard** + walrus moustache, age lines, grey robe under an open brown cloak |
| `boy` | `boy` | 2.44 (2.59) = 0.81 of the mean adult | boy: indigo felt cap with a red cuff (cast2 `skullcap`), short green tunic, red sash, light trousers |

`lineup.jpg`, top band, shows them side by side, front and 3/4.

## New pose keys (read at draw time; like cast5/6/7's keys, `resolve_pose` / `lerp_pose` drop them: re-add them to tweened poses)

| key | range | effect |
|---|---|---|
| `pour` | 0..1 (0) | tips a held `bucket` about its bail ears by 105 deg x pour toward `pour_side`; the water stream starts at ~0.4 and is full at ~0.75. Animate 0 -> 0.85 -> hold -> 0 |
| `pour_side` | +1 / -1 / 0 (0) | direction the bucket pours (+1 screen-right in the unmirrored figure); 0 = outward from the body (the hand's side) |
| `pour_len` | 0.2..3.0 D (1.0) | stream length from the lip downward (farid_pour sets it so the stream reaches his own ground line) |
| `bucket_water` | 0..1 (1) | water in the bucket (0 = empty: no stream) |
| `jar_hold` | "shoulder" (default), "hang", "hip" | how a hand carries the `water_jar`: sitting on the palm at the shoulder (tilted outward), hanging by the handle below the hand, on the hip |
| `heat` | 0..1 (0) | overheated (cast8 members): red flush on the cheeks + wavy heat shimmer beside the head (animate `t`). Combine with cast7 `sweat` |
| `cry` | 0..1 (0) | laughing to tears (cast8 members): tear streams down both cheeks with a falling drop (animate `t`). Combine with fx `tears`, `expr="laughing"`, `blink=2` |
| `panel_grip`, `panel_side` | as cast7 | also how a hand holds `ice_block` / `mud_brick` (side / bottom / top grip, which side the piece extends to) |
| `lie` | as cast7 | farid_sleep: `lie=90`, use `cast8.CANVAS8_LIE["farid"]` for the actor |
| `pale`, `sweat`, `t` | as cast6/7 | work on every cast8 member |

CAST keys (only `_cast8` members): `turban=dict(w, h, bands, jewel, plume, kulah, band, tail)` (hat_style `turban8`), hat_style `scarf8` (hat_colors light/base/dark/shine/trim), `beard8=dict(color, dark, len, w)`, `chins=True`, `rings=True`; costume `robe8`: `robe_len`, `robe_flare`, `sash_w`, `sash_y`, `sash_knot`, `jewels`, `coat` (colour of an open coat; colors coat_trim / coat_dot), `coat_drop`, `trim_dots`, `hem_band`; colors base / dark / trim / trim_d / sash / sash_d / pants.

New anchors (only while the piece is held): `grip_far_r/_l` = where the other hand goes (far edge of an ice block / brick; the **bucket base** while pouring), `piece_centre_r/_l` (ice_block, mud_brick), `bucket_base_r/_l`, `pour_lip_r/_l` + `pour_end_r/_l` (stream start / end, only while water flows), `saw_mid_r/_l` (the cut point of the ice saw), `jar_mouth_r/_l`. Mirror and squash are applied like every other anchor (not rotated by `lie`).

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` | orientation |
|---|---|---|---|
| `bucket` | **replaces cast_ext's tin sand pail while cast8 is loaded**: wooden stave bucket (0.35 D wide, two iron hoops, rope bail) with water inside | bottom (upright) / the pour lip (pouring) | hangs upright from the bail; `pour`, `pour_side`, `pour_len`, `bucket_water`; other hand -> `grip_far_*` |
| `ice_saw` | long steel ice saw, coarse teeth on the lower edge, wooden handle in the fist, 0.95 D | blade end | follows `angle` (default along the forearm); saw by moving the hand along the angle |
| `ice_pick` | iron spike pick on a 0.52 D haft | the spike point | follows `angle` |
| `ice_block` | translucent blue-white block 0.62 x 0.44 D (front + top + side faces, frosted top, cloudy core, cracks, bubbles, glints) | block centre | upright, cast7 `panel_grip` / `panel_side`; other hand -> `grip_far_*` |
| `mud_brick` | sun-dried straw mud brick 0.44 x 0.17 D | brick centre | as ice_block |
| `coin_purse` | fat leather drawstring purse, gold coins at the neck, tassel | pouch centre | hangs upright from the neck |
| `coin` | gold coin between the fingers | coin centre | along the forearm |
| `water_jar` | terracotta water jar 0.44 x 0.62 D (two handles, painted zigzag band) | the jar mouth | `jar_hold` |
| `fan` | woven palm-leaf hand fan with a red rim | leaf centre | follows `angle`: animate angle +-25 deg every ~4 frames to fan |
| `stick` (cast2), `lantern` (cast2) | existing, used by the story poses | | |

Use `scale` in the prop dict for bigger pieces (farid_pour holds the bucket at `scale=1.25`).

Standalone pieces (SVG fragments in D units): `bucket_svg(uid, pour, side, water, pour_len)` -> (svg, anchors base/lip/end; bail top at (0, 0)), `ice_block_svg(uid, w, h, melt=0..1)` -> (svg, bbox) (melt: dripping), `ice_stack_svg(uid, cols, rows)` -> (svg, top_y) (blocks stacked as in the dome, bottom on y = 0), `mud_brick_svg(uid)` -> (svg, bbox), `coin_purse_svg(uid)`, `coin_svg(uid, r)`, `water_jar_svg(uid)`, `ice_saw_svg(uid)`, `fan_svg(uid)`.

## Cycles, lip-sync, blink

Re-exported from cast6 (work for every member): `cast8.cycle(cast, phase, mode, facing, base, arms, speed)` with modes `walk` (~28 frames per cycle), `run` (~16), `sneak` (~32), `march` (~24); `cast8.talk_mouth(frame, level, seed, hold)`; `cast8.blink_at(frame, period, offset)`; `cast8.NOD`. Keep props / `heat` / `sweat` in `base`; with `arms="l"` set `arm_r` afterwards (farid_carry_bucket, woman_jar_walk do).

## STORY8 (`cast8.STORY8[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast8.STORY8_META[name]["note"]`

| name | cast | what |
|---|---|---|
| `farid_stand`, `farid_walk`, `farid_run` | farid | stand / walk frame / run frame (worried, mouth open) |
| `farid_pour` | farid | **night: pouring the bucket into the channel** (screen-right), bent forward, pour 0.85, other hand on the base, stream to his ground line |
| `farid_carry_bucket` | farid | walk frame with the full bucket hanging from the right hand |
| `farid_saw` | farid | **crouched sawing the ice sheet** (screen-right), other hand bracing it; `saw_mid_r` |
| `farid_pick` | farid | ice pick raised to break the sheet |
| `farid_carry_ice` | farid | **carrying an ice block** in front of the body with both hands, leaning back, sweat |
| `farid_build_wall` | farid | **lifting a mud brick onto the wall** (screen-right, head height), both hands under it |
| `farid_sleep` | farid | **asleep on his back** (`lie=90`, zzz, smile; canvas CANVAS8_LIE) |
| `farid_wake_shocked` | farid | **wakes late: shocked**, pale, sweat, hands flying to the head |
| `farid_smile` | farid | **calm confident smile**, arms folded |
| `farid_explain` | farid | 'I'll sell ice in summer': open palm, talking |
| `merchant_stand`, `merchant_walk` | merchant | akimbo, smug / walk frame |
| `merchant_laugh` | merchant | **big belly laugh**, head thrown back, hands on the belly |
| `merchant_mock` | merchant | **pointing and mocking** (screen-right), mouth talk_b: lip-sync with talk_mouth() |
| `merchant_tears` | merchant | **laughing to tears** (`cry=1`, fx tears, eyes shut), bent, slapping his knee |
| `merchant_sweat` | merchant | **summer heat: sweating, fanning himself** (`sweat=1`, `heat=1`, fan) |
| `merchant_pay` | merchant | **sheepish, paying**: scratching the back of the turban, coin purse held out (screen-right), blush, sweat |
| `town_laugh` (+`_oldman`, `_boy`) | woman / oldman / boy | laughing and pointing (screen-right; `mirror=True` for left) |
| `town_point` (+`_oldman` with his stick, `_boy`) | " | jeering point, talk_a |
| `town_fan` (+`_oldman`, `_boy` flapping an open hand) | " | **fanning themselves, sweating** (sweat + heat) |
| `town_walk` (+`_oldman`, `_boy`) | " | walk frame |
| `woman_jar`, `woman_jar_walk` | woman | **water jar on the shoulder** / walking with it |
| `oldman_stick` | oldman | leaning on his stick |
| `boy_run` | boy | run frame, excited |

40 poses. No name collides with earlier STORY entries.

## With the v3 stage

Exactly as cast6/7 (see `stage_test.py` -> `stage_test.png`: farid pouring, the merchant mocking, the woman with the jar, key from screen-right, `head_flip` on, Cycles 360x640, 2 threads). Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D):

| member | canvas |
|---|---|
| farid | (-1.9375, -4.5, 1.9375, 0.125) (wide: the saw and the pour); lying: `CANVAS8_LIE` (-2.25, -1.5625, 2.25, 0.25) |
| merchant | (-1.6875, -5.0625, 1.6875, 0.125) |
| woman | (-1.5, -4.3125, 1.5, 0.3125) |
| oldman | (-1.5625, -4.3125, 1.5625, 0.1875) |
| boy | (-1.4375, -3.8125, 1.4375, 0.125) |

Checked: every arm preset with the bucket, ice block, mud brick, purse, coin, jar and fan (side and bottom grip) at yaw +-0.6 (mirrored, squash 0.8-1.15), pours both sides, jar hang / hip, crouch, wide legs, all effects + pale + sweat + heat + cry, yaw +-1.2, every STORY8 pose and 16 phases x 4 modes x 2 facings of the cycles, >= 0.32 D head room; farid's lie poses against CANVAS8_LIE. The long tools (ice_saw, ice_pick, stick) are covered only in the story poses: a saw / pick swung at full arm's length in another direction can exceed the canvas: pass a wider canvas to `Actor.build` for such a shot. A long `pour_len` likewise.

## Files and QA

- `cast8.py`: the module. `test_cast8.py`: `lineup` -> `lineup.jpg` (heights front + 3/4; all 40 STORY8 poses; walk ->, run ->, walk <- cycles at 8 phases for every member; mouths talk_a / talk_b / talk_o / flat, blink 1 / 2, angry, sweat+heat, cry, laughing, shocked, pale for every member; props), section PNGs in `tmp/`; `canvas` (+ head_flip anchor check: 40 poses, 0 problems); `robust` (pose-key garbage on the 5 members + v2 `test_puppet.py --quick` on them, see `run_robust.log`).
- `stage_test.py` -> `stage_test.png`.

## Known limits

- The `bucket` prop of cast_ext (the tin sand pail) is replaced while cast8 is loaded.
- The pour tips the bucket rigidly about its ears; the water surface is drawn at the mouth, not kept level. The stream ends in a few drops: the splash on the ground / in the channel belongs to the set.
- Held pieces are drawn in the arm's layer: with `layer="front"` the head (and turban) stays in front of a piece raised beside it; put the piece clear of the turban (farid_build_wall) or use `layer="top"`.
- `lie` rotates the finished drawing; the cast8 anchors (grip_far, pour_*) are not rotated with it.
- `resolve_pose` / `lerp_pose` drop the cast7/cast8 keys: re-add `pour`, `pour_side`, `pour_len`, `jar_hold`, `heat`, `cry`, `sweat`, `lie`, `panel_grip`, `panel_side` to tweened poses.
