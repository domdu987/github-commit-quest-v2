# cast18.py: the cast of film 18 ("ไอ้เสมียนวัว", Tian Dan's fire oxen at Jimo, Warring States China, 279 BC, night)

File: `PROJ/v3/cast18/cast18.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. cast18 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to the tables and wraps `_norm`, `_face`, `_moustache`, `_ink_limb`, `_prop` on top of cast10's wrappers; each falls through, so earlier members draw as before. No text appears on any drawing.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast18")
import cast18                      # registers on import (idempotent); import BEFORE sprites / stage.sprites
import puppet                      # same module object: CAST now also has the 10 members below
cast, pose = cast18.STORY18["tiandan_tug_cloth"]
f = puppet.figure(cast, pose, "f")
p = dict(cast18.STORY18["general_arms_wide"][1], mouth=cast18.talk_mouth(g, 1.0), blink=cast18.blink_at(g, 90))     # lip-sync
run = puppet.figure("general", cast18.general_run_frame(g / 16.0, facing=-1), "f")
q = puppet.figure("qi_soldier", cast18.qi_pose(g / 16.0, facing=1), "q")                   # dark silhouette
ox = cast18.ox_figure("dragon", "side", "gallop", phase=(g % 8) / 8.0, flame=g % 3, blades=True, facing=1, uid="ox")
# ox["svg"], ox["bbox"], ox["anchors"], ox["feet_y"] (= 0): the same dict shape as puppet.figure()
```

Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged (pose keys, 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`, cast6 `cycle` / `talk_mouth` / `blink_at`, re-exported here). Head D = 1, plum ink, constant-width ink limbs, flat fills.

## Cast (head top to soles, hat in brackets, in D)

| key | build | height | look |
|---|---|---|---|
| `tiandan` | slim, legs 1.30 | 3.16 (3.38) | thin ex-market clerk: ochre hemp robe to the calf with a **crossed collar** (two trimmed edges in a Y), **dark sash** with a side knot, a bundle of **bamboo tally slips** tucked in the sash (pose `slips=0` hides them), small **black scholar's cap** (guan) with a bone pin on a topknot, calm wry face |
| `general` | stout, big belly, legs 1.30 | 3.47 (3.74) | **dark lacquered lamellar armour** laced with red cord, red robe skirt under two lacquered tassets, bronze belt hook + studs, lamellar shoulder guards, **bronze helmet with a tall red horsehair plume**, lamellar ear flaps, **huge upturned black handlebar moustache**, ruddy cheeks, red trousers |
| `yan_soldier_a` | slim, tall | 3.18 (3.33) | black lacquered lamellar over red, **iron helmet with red tuft** and red brow band |
| `yan_soldier_b` | regular, pear | 2.87 (3.13) | round, bushy moustache, **soft black cloth cap with red band** and a knot |
| `yan_soldier_c` | slim, short | 2.80 (3.03) | freckled, **ear-flap helmet with a red pompom** |
| `old_man` | regular | 2.70 (2.97) | white topknot with a worn headband, **long white beard** + moustache, grey-green hemp robe |
| `woman` | slim | 2.94 (3.25) | black hair in a **bun with a bone pin and red cord**, indigo robe to the ankle, cream sash and trim |
| `child` | child | 2.38 (2.66) | **twin tufts** tied with red cord, rust tunic, red sash |
| `envoy` | regular | 3.00 (3.22) | plain **undyed hemp robe**, plain brown cloth cap, thin moustache, humble |
| `qi_soldier` | slim | 3.18 | crowd figure: draw it with `qi_pose()` (tint + ink `#2a2634`): a dark silhouette, no face detail; **plain dark cloth cap, no red band or tuft** (`helm18=dict(kind="cloth", band=<colour>)`: `band` is a new optional key, default red) |

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them: re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `hat_askew` | -60..60 deg (0) | knocks a cast18 helmet / cap askew about the brow (general run: 24) |
| `fire_frame` | -1, 0, 1, 2 (0) | the lit `torch` flame drawing (3 flicker drawings; -1 = unlit) |
| `pot_ring` | 0..1 (0) | sound rings round a held `bronze_pot` (animate `t`) |
| `cup_tilt` | -120..120 (0) | tilts a held `jue` cup (wine drops fall above 25 deg) |
| `slips` | 0 / 1 (1) | tally slips tucked in the sash (tiandan, `tally18`) |
| `banner_side` | +1 / -1 (1) | which side the `banner` cloth flows to |
| `t` | float | animates silk / sash / banner waves, drips, rings |

CAST keys: costume `robe18` (colors base / dark / trim / sash / sash_l / skirt; `robe_len`, `robe_flare`, `sash_w`, `hem_band`, `tally18`), `armour18` (`armour18=dict(kind="general"|"soldier")`, colors robe / belt), hats `scholar18` (hat_colors cap / cap_l / cap_d / pin), `helm18` (`helm18=dict(kind="general"|"iron"|"cloth"|"flap")`), `bun18`, `tufts18`; `moustache_style="yan18"`, `beard18=dict(color, dark, len)`, `guard18=<size>` (shoulder guards).

## Props (`prop_r` / `prop_l`; `PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | tip | orientation / anchors |
|---|---|---|---|
| `jue` | bronze three-legged wine cup (spout, two posts, loop handle, wine); use `scale` 1.4-1.6 | rim | upright, `cup_tilt`; `cup_r/_l` |
| `spear` | 3.6 D spear: bronze socket, shaft, leaf blade, red tassel | 2.62 | follows `angle`; `grip_far`, `spear_tip` |
| `torch` | stick + reed head bound in red cord + the lit flame (upright) | 1.12 | follows `angle`; `fire_frame`; `torch_flame` |
| `slips` | bundle of 9 bamboo slips with 2 cords, held at the bottom | 0.62 | follows `angle`, -90 = upright |
| `bronze_pot` | round bronze basin, ring handles, hangs from the hand | bottom 0.52 | upright; `pot_ring`; `pot_top`, `pot_side` |
| `mallet` | beating stick with a cloth head | 0.64 | follows `angle`; `mallet` (strike point) |
| `sash` | general's red silk sash, gold stripes, two ends, bronze seal | 0.45 | upright; second hand -> `grip_far` |
| `silk` | crimson silk with a gold border and dragon | 1.0 | follows `angle` (extends from the fist), `t` waves |
| `blade` | short flat bronze blade, red cord wrap | 0.64 | follows `angle`; `blade` |
| `pick` | digging pick | point (1.06, 0.38) | follows `angle`; `grip_far`, `pick_point` |
| `basket` | woven bamboo basket full of earth, hangs from the hand | bottom 0.70 | upright; `basket_bottom` |
| `banner` | plain cloth banner (no text) on a 3 D pole | 2.6 | follows `angle`; `t`, `banner_side` |

Standalone: `flame_svg(uid, frame, scale, lean, sparks, glow)` -> (svg, bbox): the tail / torch flame card, layered tongues core `#fffeec` -> mid `#ffb238` -> edge `#e8561c` (never pure yellow), 3 flicker drawings, a soft glow, 3 sparks; origin at the base middle, up = -y.

## The ox (`ox_figure`, not a puppet)

`ox_figure(state, view, gait, phase=0, flame=-1, blades=False, reed=None, facing=1, coat=1.0, uid="ox", t=0, ink, tint, face=None)` returns `{"svg", "bbox", "anchors", "feet_y"}` in D units, hooves on y = 0, x = 0 about the middle of the body, facing +x (`facing=-1` mirrors it; anchors and bbox mirrored too). Chunky friendly cartoon ox: hump, two curved cream horns (each with a short bronze dagger blade when `blades=True`), ears, dewlap, cloven hooves, big eye, cream muzzle. Length about 3.4 D body, back 2.0 D, hump 2.6 D, horn tips about 3.2 D; with head about 4.5 D long (a puppet is 3 D tall).

| arg | values |
|---|---|
| `state` | `"plain"` brown, black patches / socks, no coat; `"dragon"` **crimson silk coat** with gold border, scalloped hem with tassels and a **gold SERPENTINE dragon** (round 3: a long S-curve body, thick in the middle and thin at the tail and neck, a fin crest of small dark-gold triangles, a tail tuft, three cream cloud swirls, and a SMALL profile head, a long snout with two swept-back horns, a dot eye and no open mouth, about 15 % of the coat height; **the head sits at mid-flank, well behind the ox's own head**, so it never reads as a second head at 40-60 px). `coat` 0..1 = how far it is pulled on (shifted up and back while < 1) |
| `view` | `"side"`, `"three_quarter"` (side-on body, head turned to the viewer), **`"front_three_quarter"`** (new: the ox CHARGES AT THE CAMERA, a little toward screen-right: big low head with two eyes / both horns / both ears, broad chest and neck, hump behind, body running away to the left and smaller, near front legs big, far and hind legs behind; the dragon coat shows its front edge over the chest and the dragon on the visible left flank; tail with reed and flame stands up behind the back; for s21, s22, s26) |
| `gait` | `"stand"`, `"walk"` (12-16 drawings: phase i / N), `"gallop"` (**8 drawings: phase i / 8**; body bob and pitch, tail streaming, head nodding), `"startled"` (eyes wide, legs braced, head up, tail up) |
| `flame` | -1 off; 0 / 1 / 2 = lit flicker drawing. Lighting also ties a **reed bundle** (straw, red cords, charred end) to the tail; the flame sits on its free end, leaning backwards when galloping. `reed=True` shows the unlit bundle |
| `face` | `None` (default): the original friendly face, output byte-identical to before. **`"rage"`**: the raging monster (s21 / s22 reveal): V-shaped angry brows (thick ink, plunging toward the nose), a glaring red-rimmed eye (`#c8342c` rim, flat angled upper lid, small pupil), flared dark nostrils with **2 small white steam puffs**, an **open bellowing mouth** (dark `#3a1018` inside, pink tongue `#e8728c`; teeth hint in 3/4 and front), **head lowered** (side +11 deg, 3/4 +5 deg and 0.10 D down) and **horns swung forward** (side +24 deg, 3/4 / front near horn -20 -> +4 deg, far 18 -> 40 deg). Works in all 3 views, both states, all 4 gaits, with / without flame, any `facing`. **`"panic"`**: wide eyes (as `startled`) and ears pinned back (works with every gait / view / state). Unknown values fall back to the default face. Read at draw time through the module flag `_OXFACE`, reset on every call |
| `blades` | short flat **bronze dagger blades** (round 4, lighter so they read as metal: base `#c8964a`, lighter upper facet `#e2b866`, darker lower edge `#7a5a2c`, **pale specular edge `#f0e2b8`** along the top edge and a **white highlight dot**; still bronze, not steel) **lashed to both horns with three red cord wraps**; about 0.5 long (52 % of the old 0.95 leaf), swung 24 deg forward off the horn line so horn + blade do not read as one spike or a paintbrush |

Anchors: `feet` (0, 0), `head`, `mouth`, `eye`, `back`, `hump` (front view: its own mouth / eye / hump / back anchors), `tail_tip` (the reed end = flame base), `flame_top`. `OX_CANVAS` = (-3.3125, -4.3125, 3.1875, 0.3125) covers every state (side, 3/4 and front 3/4, gallop, lit with reed; the front view's flame reaches y -4.18 at most; mirrored the width is the same). Front 3/4 gaits: `stand`, `walk` (12-16 drawings), `gallop` (8 drawings, phase i / 8: body bob, head nod, roll, legs lifting alternately), `startled` (head up, legs braced, tail and flame up); the tail angle is steeper than the side view so the flame shows above the back. For the stage an ox sprite should be rendered from `ox["svg"]` with that canvas.

## Cycles, lip-sync, blink

`cast18.cycle(cast, phase, mode, facing, base, arms, speed)` (modes `walk` 28 frames, `run` 16, `sneak` 32, `march` 24), `talk_mouth`, `blink_at`: as cast6. `cast18.general_run_frame(phase, facing)` = the general's run (shocked, helmet askew, cup in hand, arm_r re-set; lean reduced to about 5-6 deg, was 12-15: a comic run, not a fall). `cast18.qi_pose(phase, facing, speed)` = Qi soldier silhouette run with a spear (16 frames).
**Mouths move only on the general's two quotes**: `general_arms_wide`, `general_boast` (quote 1), `general_toast`, `general_carve` (quote 2) are tagged `lipsync` in `STORY18_META`: drive `mouth = talk_mouth(g)` there, `"flat"` outside. Everyone else keeps a held mouth (townsfolk beating pots: shout drawing).

## STORY18 (`cast18.STORY18[name] = (cast, pose)`, merged into `puppet.STORY`; notes in `STORY18_META`) - 59 poses

- Tian Dan: `tiandan_stand`, `_walk`, `_tug_cloth` (dressing an ox), `_tie_blade` (lashing a blade to a horn), `_raise_torch`, `_point`, `_calm_smile`, `_accept_sash`, `_read_slips`.
- General: `general_stand`, `general_laugh` (**belly laugh, held drawing**: bounce `squash` (1.02, 0.98) <-> (0.99, 1.02) and `head_dy` 0 <-> 0.06 at ~3 Hz), `_arms_wide`, `_boast` (thumb to chest), `_toast` (cup raised), `_carve` (carving mime, cup tilting), `_jaw_drop`, `_run`.
- Soldiers, suffix `_a` / `_b` / `_c`: `soldier_laugh_point`, `soldier_cheer_cup`, `soldier_mock_moo` (finger horns), `soldier_asleep`, `soldier_freeze`, `soldier_fall_bottom` (comic, unhurt), `soldier_flee` (run frame), `soldier_stand` (spear upright).
- Townsfolk: `old_man_beat`, `woman_beat`, `child_beat` (bronze vessel in one hand, stick in the other, shout face, sound rings), `*_stand`, `*_worried`, `old_man_dig`, `woman_dig` (pick, both hands), `*_carry_basket` (old_man, woman, child), `envoy_stand` (plain banner), `envoy_bow`, `envoy_walk`.
- `qi_run`.

## Canvases (feet-relative, via `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, D)

tiandan (-2.1875, -6.1875, 2.1875, 0.125) (torch); general (-1.875, -5.0, 1.875, 0.125); yan_soldier_a (-1.5, -5.25, 1.5, 0.125); _b (-1.5, -4.9375, 1.5, 0.1875); _c (-1.5, -4.875, 1.5, 0.125); old_man (-1.6875, -4.125, 1.6875, 0.125); woman (-1.6875, -4.375, 1.6875, 0.25); child (-1.5, -3.75, 1.5, 0.125); envoy (-1.625, -5.0625, 1.625, 0.1875); qi_soldier (-3.5, -4.625, 3.5, 0.125). `python3 test_cast18.py canvas` checks every arm preset with jue / bronze_pot / sash / basket at yaw +-0.6, crouch, wide legs, fx, `hat_askew`, yaw +-1.2, every STORY18 pose, 16 phases x 4 modes x 2 facings, `qi_pose`, with >= 0.32 D head room, and head_flip (mirrored anchors) on all 59 poses.

## Files and QA

`cast18.py`, `test_cast18.py` (`sheet` -> `sheet.jpg`: heights front + 3/4; all poses; walk / run cycles; 15 face states per member; props; the ox in both states and all 3 views, stand / walk / startled, the 8-frame gallop side, 3/4 and front 3/4, flame cards; `canvas` (the ox rows of the gallop section now also show `face="rage"` for all 3 views and `"panic"` on the plain ox); `robust`: pose-key garbage on the members + ox garbage + `v2/test_puppet.py --quick`), `sheet.jpg` (sections in `tmp/sec_*.png`).

## Known weaknesses

- The ox's body is a smooth blob in side view (a hump, but no ribs/shoulder modelling); the 3/4 body is a rounded box; gallop legs are tapered tubes with a simple two-bone bend, no overlapping hair.
- Round 3: the dragon is a serpentine body with a small profile head (see `state`). Round 4: `face="rage"` / `"panic"`, brighter bronze blades (changes the look of `blades=True` only; `blades=False` output is unchanged). (Earlier: a bold simple motif, no scales / claws / pearl); in the front 3/4 view only its tail half is visible, the ox head covers the rest. The front view is built from the same head drawing as `three_quarter`, scaled 1.34, so the lifted gallop legs are simple tubes with little foreshortening.
- Lamellar patterns on the soldiers become busy at small sizes.
- `jue` reads like a small lamp at less than scale 1.4; `soldier_mock_moo` hides the helmet sides behind the arms.
- Props held in `layer="front"` are drawn with the arm (as in cast8..10).
