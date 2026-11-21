# cast_ext.py: six more cast members for the v2 puppet

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/cast/cast_ext.py`
Python 3 standard library only, deterministic. `v2/puppet/puppet.py` is not edited. On import, this module adds entries to it and wraps a few of its helpers.

```python
import sys
sys.path.insert(0, ".../v3/cast")
import cast_ext                      # registers on import (idempotent); also puts v2/puppet on sys.path
import puppet                        # the same module object, now with 8 cast members
f = puppet.figure("senior_b", {"yaw": -0.4, "expr": "smug", "arm_l": "point"}, "sb")
```

Everything in `v2/puppet/API.md` applies unchanged: pose keys, presets, expressions, effects, anchors, `lerp_pose`, `resolve_pose`, `place_svg`, `hand_for_tip`, `mirror`, `tint`, `rim`.
Hero and boss output is byte-identical with and without this module (checked).

## Cast

All the new members have the same head (D = 1, measured outline, crescent, face vocabulary), ink `#3a2832`, ball hands and rubber-hose limbs as hero and boss.

| name | build | height (head top to soles) | hat | face extras | costume (elements) | limb_w |
|---|---|---|---|---|---|---|
| `senior_a` | `regular` egg 0.78 x 1.04, legs 1.30 | 3.21 | camel felt fedora: pinched crown, centre crease, dark band with a knot, flat snap brim 1.24 D | round wire spectacles, heavy brows, silver hair, frown, age lines | brown herringbone tweed waistcoat: pale-blue shirt and pointed collar, navy tie with mustard bars, 4 horn buttons, chest welt pocket with a red fountain pen, 2 flapped pockets, grey flannel trousers | 0.062 |
| `senior_b` | `stout` pear 1.06 x 0.98, legs 1.16 (short and round, 0.4 D shorter than the boss) | 3.01 | pale dove-grey bowler (LOOK_SPEC 2.6 recipe), white hair tufts poking out at both sides | white walrus moustache, age lines | burgundy rib-knit cardigan: shawl collar, button band, 3 leather buttons, 2 patch pockets (briar pipe in one), ribbed hem, white shirt, navy knit tie | 0.068 |
| `clerk` | `slim` 0.55 x 1.00, legs 1.30 (lanky; review: was 1.18, same height and silhouette as the hero) | 3.16 | green celluloid eyeshade (band + translucent visor) over slicked dark hair with a parting | none | blue-pinstriped shirt: white pointed collar, burnt-orange tie with a brass clip, chest pocket with two pencils, pearl buttons, brown belt with a brass buckle, grey trousers, **red sleeve garters drawn on the upper arms** | 0.055 |
| `beach_man` | `regular` athletic 0.70 x 1.00 (wide shoulders), legs 1.24 | 3.10 | straw boater, red ribbon with two navy stripes, flat bow | pencil moustache | 1930s one-piece bathing suit: navy with cream hoops, scoop neck, deep arm holes (bare skin = head white), red club badge with anchor, white canvas belt + brass buckle, navy trunks | 0.058 |
| `beach_woman` | `slim` hourglass 0.52 x 0.90, legs 1.16 | 2.92 | wide cream sun hat (1.56 D), navy ribbon, bow and two ribbon tails behind the head | waved chestnut bob outside the head contour, lashes, pink cheeks, smile | coral polka-dot summer dress: Peter Pan collar, 3 white buttons, navy sash with a side bow, A-line skirt drawn over the hips with a white hem trim and two folds | 0.055 |
| `beach_kid` | `child` pill 0.50 x 0.72, legs 0.70, arm 0.54 | 2.28 in D, i.e. **1.82 D when drawn at `scale_hint` 0.8**: 0.59 of the father | sailor cap: white flat top, navy band with a gold stripe, two ribbon tails | freckles, pink cheeks, blond fringe curl, smile | white middy blouse: navy sailor collar with two white stripes, red neckerchief knot and tails, gold star, navy waistband, navy shorts with a 2-button flap | 0.057 |

The child is drawn with the same head (D = 1) and child proportions. Use `CAST["beach_kid"]["scale_hint"]` (0.8) as the stage scale: `actor.place(frame, feet, scale=0.8)`. The sheet and the lineup apply it. Puppet-local coordinates (hand targets, anchors) stay in its own D, as for every member.

Reading apart at head D = 110 px (`lineup.png`): the boss is tall with a mid-grey homburg plus feather and a green pinstripe. `senior_a` is a mid-height egg with a camel pinched fedora, round glasses and brown tweed. `senior_b` is short and round with a pale bowler, white tufts, a white walrus moustache and burgundy. The two seniors and the boss differ in silhouette (hat crown shape, height, torso shape), main hue (green, brown, burgundy) and face (moustache chevron, glasses, walrus).

Beach separation on sand `#d9b27a`, sea `#5d7fa3` and sky `#9aa3b5` (`sheet.png` rows 4-6, `lineup.png`): every figure carries the ink contour. The boater straw `#ead17e` is yellower than the sand and its red band reads against the sky. The cream sun hat and the white sailor top are lighter than all three. The navy-and-cream suit, the coral dress and the red-orange pail read against all three.

### CAST keys added by this module (all optional, only the new members use them)

| key | meaning |
|---|---|
| `hat_style` | `"fedora"`, `"bowler"`, `"eyeshade"`, `"boater"`, `"sunhat"`, `"sailor"`. The new members carry `hat="newsboy"` as the dispatch slot (puppet.py only knows newsboy / homburg / None), and the wrapped `_hat_newsboy` draws `hat_style` instead. `hat=None` still gives a bare head |
| `costume` | new values `"tweed"`, `"cardigan"`, `"clerk_shirt"`, `"bathing"`, `"dress"` (+ `waist_y`, `skirt_len`, `skirt_w`), `"sailor"` |
| `glasses` | round spectacles over the eyes (rims narrow with the eye spacing when turning) |
| `moustache_style` | `"walrus"` (with `moustache=True`, which also pushes the mouth down as for the boss); colour `colors["moustache"]` |
| `pencil_moustache` | thin moustache above the mouth, mouth not pushed down |
| `lashes`, `cheeks` (`"#rrggbb"`), `freckles` | face additions |
| `garters` | sleeve garters on both upper arms, colour `colors["garter"]` |
| `hair["style"]` | `"cap"` (hair over the crown above an eyeshade, with a parting) or `"curl"` (fringe lock) |
| `scale_hint` | suggested stage scale (child 0.8) |
| `age_lines` | review addition: under-eye bags (inside the lens with `glasses`, none with ring eyes) and, without a moustache, a crease beside each side of the mouth; the two seniors use it |

## New arm preset and builds

- `"shade"` (every build, hero and boss included): the hand shades the eyes at the hat brim, drawn in the `top` layer with an open hand. Use it with `yaw` 0.5 to 0.7 and `pitch` -0.2 for "looking out to sea" (`STORY["father_looks"]`).
- New builds in `puppet.ARM_PRESETS`: `"regular"` (the mean of slim and stout) and `"child"` (slim scaled to the 0.54 arm). Every preset name of `API.md` 5 exists for them.

## New props (`prop_r` / `prop_l`)

| type | drawing | working point `prop_tip_*` (`PROP_TIP`) |
|---|---|---|
| `bucket` | red-orange lithographed tin sand pail with a yellow band, blue dots, tin rim and a bail handle; it **always hangs upright** from the hand (gravity), whatever the arm or `angle` | bottom centre, 0.47 D below the hand. `hand_for_tip("bucket", tip, 90)` is exact |
| `newspaper` | folded daily paper 0.47 x 0.32: masthead bar, headline, photo box, text columns; follows the forearm or `angle` like `paper` | far edge, 0.44 |
| `forecast` | Weather Bureau forecast sheet 0.55 x 0.42: blue `FORECAST` header, rain cloud, the word `RAIN`, table lines, dog-ear | far edge, 0.52 |
| `mug` | cream enamel coffee mug with a blue rim, coffee and a steam wisp; **always upright**, handle on the +x side (it flips with `mirror`), the hand ball covers its front | the hand (0.0) |

`puppet.PROP_TYPES` and `puppet.PROP_TIP` are extended, so `_prop_spec`, `lerp_pose`, `hand_for_tip` and the tests accept the new types.

## Stage

`cast_ext` adds a feet-relative canvas per member to `sprites.DEFAULT_CANVAS`, whatever the import order. Members already imported as `sprites` / `stage.sprites` are patched at once, and a module imported later is patched by a small import hook. If a process imports sprites by an unusual name, call `cast_ext.register_stage(module)`.

| name | canvas (x0, y0, x1, y1), D | head room above the pose range |
|---|---|---|
| senior_a | (-1.875, -4.625, 1.875, 0.125) | 0.39 |
| senior_b | (-1.9375, -4.375, 1.9375, 0.125) | 0.34 |
| clerk | (-1.8125, -4.5625, 1.8125, 0.125) | 0.38 (review: taller for the longer legs) |
| beach_man | (-1.8125, -4.5, 1.8125, 0.125) | 0.37 |
| beach_woman | (-1.8125, -4.3125, 1.8125, 0.125) | 0.37 |
| beach_kid | (-1.4375, -3.625, 1.4375, 0.125) | 0.32 |

The pose range checked is every arm preset with every prop at yaw +/-0.6, squash 0.8 to 1.15, crouch, wide legs, steam, Z, sweat and tears (`python3 cast_ext.py canvas`). The head room matches the 0.32 to 0.34 D that the hero and boss defaults keep for the upper-body stretch.

Checked through `sprites.render_sprites` with two poses each, one of them with `upper_k` 1.12: 12 sprites at 128 px per D, none clipped, 56 ms per sprite (`v3/tmp/cast/sprite_check.jpg`, script `v3/tmp/cast/sprite_check.py`).

## Story poses added to `puppet.STORY`

`seniors_agree` (senior_a, smug, pointing), `walrus_scoffs` (senior_b, hands behind), `clerk_runs_in` (clerk, shocked, striding with the newspaper), `father_looks` (beach_man shading his eyes), `kid_bucket` (beach_kid with the pail, waving).

## How it plugs in (for maintainers)

`puppet.figure()` looks its helpers up as module globals at call time. This module replaces these, and each replacement falls through to the original for anything it does not handle:
`_torso` (costume dispatch, skirt drawn over the torso bottom), `_hat_newsboy` (`hat_style` dispatch), `_face` (glasses, lashes, pencil moustache, cheeks, freckles), `_moustache` (walrus), `_hair` (cap, curl), `_ink_limb` (garters on the two arm limbs only), `_prop` (new props), `_norm` (records the cast being drawn, for the two hooks that do not receive it). The originals are kept in `cast_ext._O`.

Hanging ribbons and the sun-hat bow sit on the side away from the face. They cross-fade between the two sides over yaw -0.16 to 0, because a hard switch at yaw 0 measured as a pop. Head seeds were chosen so that each head reads as round as the hero's and the boss's: `cast_ext.head_seed_metrics(seed)`.

## Command line and QA

```
python3 cast_ext.py sheet     # sheet.svg + sheet.png: per member 3 views (front, 3/4, near-profile), 4 expressions
                              # (neutral, smug or amused, worried, shocked), 3 poses (standing, pointing or shading the eyes, startled)
python3 cast_ext.py lineup    # lineup.png: all 8 members, same scale, office wall #b5484c and sand #d9b27a, head D 110 and 220 px
python3 cast_ext.py test      # v2 test_puppet.py run on the 6 new names (+ canvas check); --full for the dense grid
python3 cast_ext.py canvas    # sprite canvas check
python3 measure_ext.py        # v2 measure.py (LOOK_SPEC 2.2 / 2.3 ranges) on the new members
python3 strip_ext.py          # 30-frame turn strip per member (yaw -1 -> +1, arm up, prop swinging): pixel pop check
```

Usage notes (review): with `arm_*="shade"` or `"chin"` a held prop is drawn at the hand, i.e. in front of the face; drop the prop for those presets. The bucket and the mug ignore `angle` and stay upright, so on a raised arm the pail hangs beside the head.

Independent review: `REVIEW.md` (results after the repairs, `review_compare.jpg`). Builder's results of the last run before the review:
- `test`: 1,994,570 checks, 0 failed. Slowest pose 1.16 ms per `figure()` call.
- `measure_ext`: 203 measurements, 0 outside the spec range. These cover head D 0.98 to 1.01, outline bins, crescent, eye spacing and size, eye-to-mouth distance, brows, torso width per build, contour 0.020 to 0.028 left and 0.038 to 0.045 right, limb and hand size, arm and leg length, height, foot stub, and the hat edge on the head. The child has its own body ranges, and the woman's torso height is not measured because the skirt covers it.
- `strip_ext`: largest frame-to-frame change is 1.06 to 1.32 times the median (limit 2.2), and the largest anchor step is 0.080 D (limit 0.12).
