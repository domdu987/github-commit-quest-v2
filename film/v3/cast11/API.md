# cast11.py: the cast of film 11 ("ไอ้หมอวัว", Edward Jenner and cowpox, Berkeley, Gloucestershire, May 1796) for the v2 puppet

File: `PROJ/v3/cast11/cast11.py` (+ `cow11.py`, the cow; PROJ = the `film/` folder of the repo). Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast11 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to their tables and wraps the puppet helpers on top of cast10's wrappers: `_norm` (this module's pose keys), `_face` (pockmarks, fever flush), `_ink_limb` (stockings / bare shins, buckles), `_prop` (new props) and `figure` (stool, yoke with pails, upper-arm anchors, and the cow). Each wrapper falls through, so every earlier member draws exactly as before: `python3 test_cast11.py identity` draws every earlier CAST member (3 poses each) plus every earlier STORY pose with and without cast11 loaded in two fresh interpreters and compares the SVG text: 531 drawings, 0 differ.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast11")
import cast11                # registers on import (idempotent); import it BEFORE sprites / stage.sprites (as film10/common.py does with cast10)
import puppet                # same module object: CAST now also has the 11 members + "blossom"
cast, pose = cast11.STORY11["jenner_lancet_up"]
f = puppet.figure(cast, pose, "f")                                              # f["anchors"]["lancet_r"] = blade tip
p = dict(cast11.STORY11["towndoc_point_mock"][1], mouth=cast11.talk_mouth(g, 1.0), blink=cast11.blink_at(g, 90))
w = puppet.figure("jenner", cast11.cycle("jenner", g / 28.0, "walk"), "f")
b = puppet.figure("blossom", dict(chew=g / 12.0, tail=0.6 * math.sin(g / 9.0)), "b")        # the cow: same contract (svg, feet_y, bbox, anchors)
a = actors.Actor("jen", "jenner"); a.build(sprites.DEFAULT_CANVAS["jenner"], sprite_dir, contact=True)
a = actors.Actor("bed", "james"); a.build(cast11.CANVAS11_LIE["james"], sprite_dir, contact=True)       # lying in bed
a = actors.Actor("yk", "sarah"); a.build(cast11.CANVAS11_YOKE["sarah"], sprite_dir, contact=True)       # carrying the yoke
```

For film 11 copy `film10/common.py` and put `cast11` in place of `cast10` in the path list and the import. Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies unchanged: pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx (`sweat`, `tears`, `blush`, ...), cast7 `sweat` / `lie`, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`.

**Blossom (the cow) is a CAST key too (`blossom`) but not a human puppet**: `puppet.figure("blossom", pose, uid)` returns the usual dict. Her anchors are `feet`, `head`, `mouth`, `muzzle`, `eye`, `ear`, `back`, `withers`, `udder`, `teat_l`, `teat_r`, `pail_spot`, `milker_feet`, `tail_tip`, `tail_root`, `flank`. The human anchors (`hand_r`, `shoulder_r`, ...) exist as harmless placeholders. Do not call `head_flip` / expression code on her: build her Actor with `head_flip=False` if the pipeline offers it, and use `mirror=True` to face screen-left.

## Cast (head D = 1, same proportions and plum ink as cast9/10)

Heights are head top to soles in D, with the hat / wig in brackets; the head top is what has to stay above y 880 of the 1280 frame.

| key | build | head top to soles (hat) | canvas (feet-relative x0, y0, x1, y1) |
|---|---|---|---|
| `jenner` | regular | 3.12 (3.26) | (-1.75, -4.5, 1.75, 0.125) |
| `james` | boy | 2.34 (2.53) | (-1.25, -3.75, 1.25, 0.125) |
| `sarah` | slim | 2.92 (3.13) | (-1.75, -4.3125, 1.75, 0.125) |
| `milkmaid2` | slim | 2.96 (3.14) | (-1.5, -4.375, 1.5, 0.125) |
| `towndoc` | stout | 3.25 (3.70) | (-2.75, -5.375, 2.75, 0.125) |
| `mother` | slim | 2.92 (3.13) | (-1.5, -4.3125, 1.5, 0.125) |
| `villager_a` | regular | 3.00 (3.06) | (-1.375, -4.375, 1.375, 0.125) |
| `villager_b` | slim | 2.94 (3.15) | (-1.5, -4.3125, 1.5, 0.125) |
| `villager_c` | regular | 2.81 (3.02) | (-1.375, -4.1875, 1.375, 0.125) |
| `villager_d` | slim | 3.16 (3.42) | (-1.25, -4.5625, 1.25, 0.125) |
| `villager_e` | slim | 2.80 (3.01) | (-1.25, -4.1875, 1.25, 0.125) |
| `blossom` | cow | back 2.68 above the floor (hooves y = 1.82), head carried at about 2.1 | (-4.5625, -3.1875, 4.5625, 0.125) |

Looks:
- `jenner` (~47): dark blue tailcoat (cast7 `frock7`, buff waistcoat, white cravat, white sleeve ruffles), buff breeches with a garter, **white stockings**, black **buckled** shoes, his own grey-brown hair swept back off the forehead with side curls and a **queue** tied with a black ribbon that hangs behind the head when he turns (`queue11`, visible for |yaw| > 0.1); kind clever face with smile lines.
- `james` (James Phipps, 8): messy brown mop (`messy11`), freckles, linen shirt with a laced neck, **braces**, short brown breeches, **bare shins** (skin-coloured), brown boots. Sleeves are short and rolled (`sleeve len 0.26`) so the upper arm is bare for the lancet.
- `sarah` (Sarah Nelmes): frilled **mob cap** over auburn hair, blue short gown over a **red-and-cream striped petticoat**, cream apron with a bib, rolled sleeves, rosy **clear smooth** face.
- `milkmaid2`: **straw hat** with a blue ribbon, long golden hair in two locks, green short gown, **blue-and-cream striped petticoat**, apron, clear face.
- `towndoc` (the mocker): stout, **powdered bob wig** (two tiers of sausage curls each side), black **tricorn** with gold lace and a red cockade (pose `hat_off=1` removes it), **plum velvet coat** with gold buttons, gold cuffs, cream waistcoat, gold watch chain, cravat, plum breeches, white stockings with gold garters, gold-buckled shoes, ruddy face, double chin, thick brows. Prop `cane` = gold-headed ebony cane.
- `mother`: plain frilled **cap** (cream, brown ribbon), grey-brown gown, **dusty-rose shawl** crossed on the chest, long plain skirt, grey-brown hair, age lines.
- `villager_a` (flat cap, bushy moustache, brown waistcoat), `villager_b` (woman, mob cap with a blue ribbon, ochre gown, brown-striped petticoat) and `villager_c` (old, grey hair and moustache, green waistcoat): **POCKMARKED** (CAST `pocks11 = 1`): 16 dark-red scars each in a pale pink halo on forehead, cheeks, nose and chin, readable at 360-px phone size, comic not gory. `villager_d` (tall young man, straw farm hat, braces) and `villager_e` (woman, mob cap with a green ribbon, teal gown): plain.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `pocks` | 0..1 (CAST `pocks11`, 0 for plain members) | the pockmarks, any cast11 member; they appear one by one as the value rises. 0 forces a clear face |
| `flush` | 0..1 (0) | fever: red cheeks and forehead, a damp shine. Use with cast7 `sweat=1` (sweat drops round the head) and `expr="sad"` |
| `horns`, `cow_ears` | 0..1 (0) | **the gag**: two small cow horns / two brown cow ears with pink insides grow out of the hair (`messy11`, i.e. `james`). 0.7 and up is full size. Works on any james pose, e.g. `james_horns` |
| `hat_off` | 0 / 1 (0) | towndoc: take the tricorn off (the wig stays) |
| `stool` | 0 / 1 (0) | draws a **three-legged milking stool** behind the figure, seat 0.10 D below the hip (`stool_drop`), `stool_w` 0.95 wide, `stool_dx`. Anchor `stool_top`. Also switches women's skirts to the seated shape (below). Use the leg presets `_sit(cast)` / `_sit_front(cast)` in the story code (crouch 0.45, feet under the knees) |
| `sit_front` | 0 / 1 (0) | with `stool`: the three-quarter sit (knees to the viewer, short vertical skirt: milking). 0 = the side sit (thighs forward to screen-right: mother by the bed, James on the stool) with the skirt spread over the lap |
| `yoke` | 0 / 1 (0) | a **shoulder yoke** across the shoulders with a rope and a milk **pail** at each end. `yoke_w` 0.86 (half width), `yoke_rope` 0.50, `milk` 1. Anchors `yoke_l/_r`, `pail_l/_r` (pail centres). Put the hands at (+-0.66, 0.62). Needs `CANVAS11_YOKE` |
| `flame` | 0..1 (1) | the candle flame height; animate with `t` for the flicker |
| `lie` | cast7 key | `james_in_bed`: `lie=90` (head to screen-left) with `head_roll=72` keeps the face upright like a head propped on a pillow; for the other side `lie=-90`, `head_roll=-72`. Needs `CANVAS11_LIE` |
| `t` | float | drives the flame sway and the tears |

New anchors on every cast11 member: `upper_arm_r`, `upper_arm_l` (80 % of the way from shoulder to elbow: where the lancet scratches the boy).

CAST keys (cast11 members only): hat_style `queue11` (hat_colors light / base / dark / streak / ribbon), `wig11` (`wig_colors` light / base / dark, hat_colors = the tricorn: base / dark / light / shine / lace / cockade / brass, `tricorn11`), `mobcap11` (hat_colors light / base / dark / band; the maid's hair is `hair.color`), `bonnet11` (hat_colors light / base / dark / band; `locks`, `brim`, `crown_h`), `messy11` (`hair` colour / shine / dark); costume `shirt11` (colors base / pants / brace / vest + CAST `vest_on`, `patch`), `gown11` (colors base / skirt_a / skirt_b stripes / apron / fichu; CAST `shawl`, `skirt_len`, `skirt_flare`); `leg11 = dict(breeches, shin, garter, buckle)` (stocking or bare-shin colour from the knee down); `pocks11`. The knee breeches are cast4 `shorts` with `len=0.5`.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` | orientation / anchors |
|---|---|---|---|
| `lancet` | Jenner's lancet 0.77 D long: tortoiseshell handle, brass collar, short steel blade, a glint star at the tip | blade tip (0.64) | follows `angle`. Anchor `lancet_r/_l` = the tip |
| `jar` | small glass specimen jar, cork, pale cloudy fluid | none | always upright, held at its lower side. Anchor `jar_r/_l` = its centre |
| `notebook` | small pocket notebook held open towards the viewer, leather cover, cream **blank** pages, red ribbon | none | follows `angle` (extends along the forearm). Anchor `notebook_r/_l` |
| `quill` | goose quill, nib at +x, feather behind the hand | the nib (0.30) | follows `angle` (nib along the angle). Anchor `quill_r/_l` = the nib |
| `pail` | wooden milk pail on a bail, two hoops, milk with foam | bottom (0.42) | always upright, hangs from the hand. Anchors `pail_bottom_*`, `pail_rim_*` |
| `candle` | brass chamberstick with a ring handle, candle, flame and a warm glow | none | always upright, beside the hand on the outer side. Anchor `flame_r/_l`. Keys `flame`, `t` |
| `cane` | gold-headed ebony cane 1.5 D long | the ferrule (1.52) | follows `angle` (angle 96 = planted on the floor). Anchor `cane_r/_l` |
| `blister_hand` | an open **hand with six big cowpox blisters** (pale yellow domes in red halos), back to the viewer, 0.6 D long | fingertips (0.56) | follows `angle`, wrist at the hand. Use `scale` 1.25-1.3 for reveals. Anchor `blister_hand_r/_l` |

Standalone pieces (SVG fragments in D units, for the set): `cast11._lancet_body(k)`, `_jar_body(k)`, `_pail_body(k, milk)`, `_candle_body(k, side, flame, t)`, `_cane_body(k)`, `_blister_hand_body(k)` where `k = puppet._Ctx(uid, puppet.INK, None)`.

## Blossom (pose keys, all optional; `cow11.py`)

| key | range (default) | effect |
|---|---|---|
| `head_turn` | -0.4..1 (0) | 0 = head forward and a little down; 1 = turned down and back towards the flank (looking at the milkmaid) |
| `head_down` | -0.5..1 (0) | extra nod / grazing |
| `ear` | -1..1 (0) | near-ear flick; animate +1, -0.3, 0 over about 6 frames |
| `tail` | -1..1 (0) | tail swish (the tail bends progressively); animate with a sine |
| `chew` | phase (None = mouth shut) | jaw and muzzle chew once per unit of phase: pass `frame / 12.0`; `chew_amp` 0..1.5 |
| `blink`, `mirror`, `tint`, `ink`, `squash` | as the humans | |

Look: Gloucester-ish dark red-brown with a white belly, flank patches, white blaze, white socks and white tail tuft; pink muzzle and a **visible pink udder with four teats**. The milkmaid fits beside her: `sarah_milk` (stool=1, sit_front=1) planted on Blossom's anchor `milker_feet` reaches the teats (`teat_l` / `teat_r`) with her hands; the pail goes on `pail_spot`. `python3 test_cast11.py sheet` shows this composition in the cow section. Blossom's canvas is 9.1 D wide so the stool and the maid can be baked into one sprite; the usual way is two sprites.

## Cycles, lip-sync, blink

Re-exported from cast6 and working for every member: `cast11.cycle(cast, phase, mode, facing, base, arms, speed)` with `walk` (28 frames per cycle) / `run` (16) / `sneak` / `march`, `cast11.talk_mouth(frame, level, seed, hold)`, `cast11.blink_at(frame, period, offset)`, `cast11.NOD`. For `sarah` with the yoke use `base=dict(yoke=1, ...)`; the yoke walk checks out in `CANVAS11_YOKE`.

**Mouths** move only on quoted lines: the three poses tagged **lip-sync** below (`jenner_explain`, `towndoc_point_mock`, `towndoc_point_door`) hold `mouth="flat"` and are meant to get `mouth = talk_mouth(g)` while the figure speaks a quoted line; all other poses hold one fixed mouth. The laugh poses hold an open laugh mouth that does not move.

## STORY11 (`cast11.STORY11[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast11.STORY11_META[name]["note"]`

| name | cast | what |
|---|---|---|
| `jenner_neutral` | jenner | standing, kind and calm, arms at his sides |
| `jenner_explain` | jenner | explaining: right hand open and out, left hand low; set mouth = talk_mouth(g) on quoted lines, else flat **lip-sync** |
| `jenner_lancet_up` | jenner | the lancet held up beside his head (glint at the tip); anchor lancet_r = the blade tip |
| `jenner_jar_up` | jenner | holds the small glass jar up to the light; anchor jar_r = jar centre |
| `jenner_scratch_arm` | jenner | bends towards the boy (screen-right) and scratches his upper arm: put anchor lancet_r (blade tip) on James's anchor upper_arm_l (James faces screen-left in james_sit_sleeve). Move arm_r['hand'] to land it exactly |
| `jenner_examine_hand` | jenner | peering at the milkmaid's hand (screen-right), both hands cupping it; her hand_r (blister_hand) goes between his hands |
| `jenner_write` | jenner | writes in his notebook (screen-left hand) with a quill (right hand); anchor quill_r = the nib. No text on the pages |
| `jenner_proud` | jenner | proud smile, chin up, one hand on his waistcoat, the other on his hip |
| `jenner_wince` | jenner | wince: sucks air through his teeth, hands half up (the day-nine fever worry) |
| `jenner_walk` | jenner | one walk frame (phase 0.30); animate with cycle('jenner', frame / 28.0, 'walk') |
| `james_sit_sleeve` | james | sits on the stool (stool=1) facing screen-left towards Jenner, sleeve rolled to the shoulder; the upper arm to scratch is anchor upper_arm_l. Mirror (mirror=True) for the other side |
| `james_brave` | james | brave: chin up, lips pressed, steady |
| `james_scared` | james | scared: hunched, worried, a drop of sweat, hands clenched in his lap |
| `james_in_bed` | james | sick in bed on his back (lie=90, head to screen-left; for the other side lie=-90 AND head_roll=-72; head_roll=72 keeps the face upright like a head propped on a pillow), flushed cheeks, sweat drops; anchor feet = middle of the body on the mattress line. Canvas CANVAS11_LIE |
| `james_jump_up` | james | jumps out of bed: arms up, both feet off the floor (raise the sprite by hand, or use it as the mid-jump key) |
| `james_play` | james | playing in the garden: a skip with one arm up |
| `james_run` | james | one run frame (phase 0.30); animate with cycle('james', frame / 16.0, 'run') |
| `james_laugh` | james | laughing, hands on his tummy |
| `james_horns` | james | GAG: the mocker's imagined 'he will grow horns': small cow horns + brown cow ears. Pose keys horns / cow_ears (0..1) work on any james pose **GAG** |
| `sarah_milk` | sarah | milking on a stool (stool=1, sit_front=1: three-quarter, knees to the viewer), head and hands towards screen-right, hands at udder height (about 0.65 D above the floor). Plant her feet on the cow's anchor milker_feet (hands then reach the teats teat_l / teat_r; pail on pail_spot). Pace the hands: arm_r / arm_l hand y 1.20 / 1.26, +-0.06 in antiphase |
| `sarah_smile` | sarah | smiling, hands folded in front of the apron |
| `sarah_yoke` | sarah | carries two milk pails on a yoke (yoke=1): anchors pail_l / pail_r; yoke_w, yoke_rope, milk keys. Canvas CANVAS11_YOKE |
| `milkmaid2_milk` | milkmaid2 | milking on a stool (stool=1, sit_front=1: three-quarter, knees to the viewer), head and hands towards screen-right, hands at udder height (about 0.65 D above the floor). Plant her feet on the cow's anchor milker_feet (hands then reach the teats teat_l / teat_r; pail on pail_spot). Pace the hands: arm_r / arm_l hand y 1.20 / 1.26, +-0.06 in antiphase |
| `milkmaid2_smile` | milkmaid2 | smiling, hands folded in front of the apron |
| `milkmaid2_yoke` | milkmaid2 | carries two milk pails on a yoke (yoke=1): anchors pail_l / pail_r; yoke_w, yoke_rope, milk keys. Canvas CANVAS11_YOKE |
| `sarah_show_hand` | sarah | holds out her right hand, back to us, with the cowpox blisters (prop blister_hand: six big pale blisters in red halos); anchor blister_hand_r = the fingertips. Her face stays clear and smooth |
| `sarah_show_hand_close` | sarah | the same, hand straight up and scaled 1.3 for the close reveal (blisters readable at phone size) |
| `sarah_walk` | sarah | walk frame with the yoke; animate cycle('sarah', f / 28.0, 'walk', base=dict(yoke=1, ...)), arms=None |
| `towndoc_laugh_big` | towndoc | BIG belly laugh: head thrown back, mouth open wide, tears, hands on the belly (fixed laughing mouth) |
| `towndoc_point_mock` | towndoc | points and mocks (screen-right), cane in the other hand. lip-sync: mouth = talk_mouth(g) on his quoted lines, else flat **lip-sync** |
| `towndoc_point_door` | towndoc | accusing finger out to the door (screen-right), cane planted. lip-sync as above **lip-sync** |
| `towndoc_scoff_crossed` | towndoc | scoffs with his arms crossed, nose in the air |
| `towndoc_shocked` | towndoc | shocked: jaw dropped, sweat, hands up |
| `towndoc_sleeve_sheepish` | towndoc | ENDING: sheepishly rolling up his sleeve in the vaccination queue (right hand at the left cuff), blushing |
| `towndoc_walk` | towndoc | one walk frame; animate with cycle('towndoc', f / 28.0, 'walk') |
| `mother_sit_worried` | mother | sits (stool=1) by the bed, hands clasped, worried; yaw 0.4 = looks screen-right (mirror for the other side) |
| `mother_sit_relieved` | mother | relieved: a smile, one hand to her heart |
| `mother_stand_worried` | mother | standing, wringing her hands |
| `villager_a_laugh` | villager_a | pocked villager laughing, head back, hand on the belly |
| `villager_a_point` | villager_a | pocked villager pointing and jeering (screen-right) |
| `villager_a_whisper` | villager_a | pocked villager whispering behind a hand to a neighbour (screen-right) |
| `villager_a_queue` | villager_a | pocked villager standing patiently in the vaccination queue (mirror for the other direction) |
| `villager_b_laugh` | villager_b | pocked villager laughing, head back, hand on the belly |
| `villager_b_point` | villager_b | pocked villager pointing and jeering (screen-right) |
| `villager_b_whisper` | villager_b | pocked villager whispering behind a hand to a neighbour (screen-right) |
| `villager_b_queue` | villager_b | pocked villager standing patiently in the vaccination queue (mirror for the other direction) |
| `villager_c_laugh` | villager_c | pocked villager laughing, head back, hand on the belly |
| `villager_c_point` | villager_c | pocked villager pointing and jeering (screen-right) |
| `villager_c_whisper` | villager_c | pocked villager whispering behind a hand to a neighbour (screen-right) |
| `villager_c_queue` | villager_c | pocked villager standing patiently in the vaccination queue (mirror for the other direction) |
| `villager_d_laugh` | villager_d | plain villager laughing, head back, hand on the belly |
| `villager_d_point` | villager_d | plain villager pointing and jeering (screen-right) |
| `villager_d_whisper` | villager_d | plain villager whispering behind a hand to a neighbour (screen-right) |
| `villager_d_queue` | villager_d | plain villager standing patiently in the vaccination queue (mirror for the other direction) |
| `villager_e_laugh` | villager_e | plain villager laughing, head back, hand on the belly |
| `villager_e_point` | villager_e | plain villager pointing and jeering (screen-right) |
| `villager_e_whisper` | villager_e | plain villager whispering behind a hand to a neighbour (screen-right) |
| `villager_e_queue` | villager_e | plain villager standing patiently in the vaccination queue (mirror for the other direction) |
| `blossom_stand` | blossom | standing, head down and forward, udder visible |
| `blossom_chew` | blossom | chewing: jaw and muzzle move once per unit of the chew phase (pass frame / 12) |
| `blossom_turn_head` | blossom | head turned down and back to look at the milkmaid |
| `blossom_ear_flick` | blossom | near ear flicked |
| `blossom_tail_swish` | blossom | tail swung back, chewing |

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D)

The default per-member canvases are in the first table (`cast11.CANVAS11`). Special ones: lying in bed `cast11.CANVAS11_LIE["james"]` = (-1.5, -1.5, 1.5, 0.25); the yoke `cast11.CANVAS11_YOKE["sarah" / "milkmaid2"]` = (-1.875, -3.5625, 1.875, 0.125). Blossom: `CANVAS11["blossom"]`.

`python3 test_cast11.py canvas` checks, per member: every arm preset with the member's own props at yaw +-0.6 (mirrored, squash 0.8-1.15), crouch, wide legs, fx, flush / horns / ears, yaw +-1.2, every STORY11 pose (lying and yoke ones against their own canvas), 16 phases x 4 modes x 2 facings of the cycles, and the cow's head / ear / tail / mirror range. All fit with at least 0.32 D of head room; 0 problems; the mirror-anchor check (head_flip) over 63 poses has 0 problems.

## Files and QA

- `cast11.py` (members, hats, costumes, props, story), `cow11.py` (the cow), `test_cast11.py`, `sheet.jpg`, `run_robust.log`.
- `test_cast11.py` modes: `identity` (earlier casts byte-identical, above), `canvas`, `robust` (garbage pose keys 4800 + v2 `test_puppet.py --quick` on the 11 members), `sheet` -> `sheet.jpg`: heights (front + 3/4, dashed head-top line), every STORY11 pose, 16 face states per member (talk shapes, blinks, expressions, fever, pocks on / off), every prop plus stool, yoke, the gag, pockmarks and the fever, Blossom's poses with the milking composition, and at the bottom the 360-px-wide phone strip (head D = 75 px, i.e. D = 150 in the 720 x 1280 frame).
- No Blender stage test was rendered (no shots, as asked).

## Known limits

- Blossom is a flat side-view sprite. `head_turn` rotates the head about the neck (it does not turn the face to the camera); she has no front or three-quarter view.
- The seated skirts are fixed shapes for the two leg presets (`_sit`, `_sit_front`); other sitting leg targets may leave the skirt short or long.
- A lying James (`lie`) is a rotated standing puppet: the bed, blanket and pillow are the set's job (his body is the lower half; draw the blanket over it).
- Pockmarks sit on the face layer under the eyes and brows, so a thick moustache (villager_a, villager_c) can cover a mark or two; the marks do not follow `head_roll` beyond what the face does.
- `blister_hand` is a prop hand: the figure's ink ball hand still sits at the wrist under it (hidden at the usual angles).
- `jenner_scratch_arm` places the lancet tip by eye; for an exact touch move `arm_r["hand"]` until `lancet_r` equals James's `upper_arm_l` (both are anchors).
- `resolve_pose` / `lerp_pose` drop the cast7..11 keys. Re-add `pocks`, `flush`, `horns`, `cow_ears`, `hat_off`, `stool`, `sit_front`, `yoke*`, `flame`, `sweat`, `lie`, `t` to tweened poses.
