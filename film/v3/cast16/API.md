# cast16.py: the cast of film 16 ("ไอ้บ้าลวด", Samuel Morse's telegraph, USA 1825-1845) for the v2 puppet

File: `PROJ/v3/cast16/cast16.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only, deterministic.
Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import cast16 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to their tables and wraps `_norm`, `_face`, `_prop` and `figure` on top of cast10's wrappers; each wrapper falls through for every earlier member, so every earlier pose draws byte for byte as before (`test_cast16.py identity`: 324 earlier STORY poses + 690 member/pose-key combinations, 0 differ, compared in two separate processes with and without cast16).

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast16")
import cast16                  # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                  # same module object: CAST now also has the members below
cast, pose = cast16.STORY16["mocker_boast_chest"]
f = puppet.figure(cast, pose, "f")
p = dict(cast16.STORY16["mocker_mock_point"][1], mouth=cast16.talk_mouth(g, 1.0), blink=cast16.blink_at(g, 90))   # lip-sync, mocker only
w = puppet.figure("morse16", cast16.cycle("morse16", g / 28.0, "walk"), "w")
m = puppet.figure("mule", cast16.cycle("mule", g / 36.0, "walk", 1, dict(harness=1)), "m")      # the mule: own drawing path, same return dict
a = actors.Actor("mor", "morse16"); a.build(cast16.CANVAS16["morse16"], sprite_dir, contact=True)
a = actors.Actor("mul", "mule");    a.build(cast16.CANVAS16["mule"], sprite_dir, contact=True)
cast16.key16("worker_a")      # -> "worker16_a"
```
For film 16 copy `film8/common.py` and put `cast16` in place of `cast8`. Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies: the pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, the fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`.

**Name collisions.** Three spec names are already CAST keys of earlier films, whose output must not change, so they carry a suffix: `worker_a` -> **`worker16_a`**, `worker_b` -> **`worker16_b`**, `clerk` -> **`clerk16`** (the STORY16 names keep the spec spelling: `worker_a_shovel` ...). `cast16.ALIAS16` / `cast16.key16(name)` map them.

## Cast (head D = 1)

| key | height head top to soles (with hat) | build | look |
|---|---|---|---|
| `morse16` | 3.32 (3.56 with his hair mass) | `slim` 0.66 x 1.04, legs 1.42 | Samuel Morse as painter-inventor: lean, **grey-brown swept-back hair** (hat style `mane16`), **long side-whiskers** to the jaw, **high white collar points**, black cravat, brown waistcoat with a watch chain, **dark navy frock coat**, dark trousers. Kind and determined. Variant pose key **`young=1`** (1825 studio): darker hair, shorter whiskers, **cream painter's smock** with paint dabs over the shirt (CAST `morse16_young`) |
| `mocker` | 3.37 (4.18 with the stovepipe) | `stout` 1.64 x 1.26, legs 1.24 | portly congressman (composite, no real likeness): **big belly**, florid cheeks and a red nose, grey **mutton-chop whiskers**, **tall black stovepipe hat** (removable), **black open tailcoat** with silk lapels over a **big gold plaid waistcoat** with brass buttons and a watch chain + fob, brick-red cravat, grey trousers. Variants: **`hat_off=1`** = bald crown with a fringe of hair; **`sash=1`** = postmaster: federal-green **sash** across the chest with gold edges and a medallion, leather **mail bag** on the hip, iron **key ring** on the belt (`belt_keys=0` hides the ring when a prop key ring is held). Combine freely (CAST `mocker`, `mocker_bare`, `mocker_pm`, `mocker_pm_bare`) |
| `congressman_a` | 3.22 (3.48) | `slim` | thin, round **spectacles**, brown derby, federal-green frock coat, cream waistcoat |
| `congressman_b` | 2.95 | `regular`, pear-shaped | **white hair** (no hat), white bushy moustache and side-whiskers, brown coat, brick-red waistcoat, navy tie |
| `congressman_c` | 3.16 (3.74) | `slim` | young **dandy**: tall pale-grey beaver hat tilted, curl lock, pencil moustache, burgundy double-breasted coat, buff waistcoat, cream trousers, flower in the buttonhole, yellow cravat |
| `messenger` | 2.44 (2.56) | `boy` | boy in a brown flat cap, short green jacket, scarf, short trousers; holds the sealed letter |
| `cornell` | 3.12 (3.41) | `regular` | worker-engineer: tan **slouch hat**, bushy moustache, cream shirt with **rolled sleeves**, **braces**, dark trousers, tall **boots**, dirt smudges. `hat_off=1` = bare head (CAST `cornell_bare`) |
| `worker16_a` | 3.06 (3.18) | `regular`, stocky | labourer: grey-brown flat cap, **red plaid flannel shirt**, black braces, rolled sleeves, boots |
| `worker16_b` | 3.28 (3.43) | `slim`, tall | labourer: **straw hat**, bushy moustache, grey-blue shirt, tan braces, rolled sleeves |
| `clerk16` | 3.16 | `slim` (cast_ext clerk build) | thin clerk: green eyeshade, cream shirt, black tie, **red sleeve garters**, pencils, brown belt |
| `mule` | 3.21 (head top) / 3.98 (ears); shoulder (withers) 2.6 | side view | brown mule, long ears, dark short mane and tufted tail, tan muzzle; optional harness |

For scale: film 10's painter is 3.20 and its admiral 3.43.

CAST keys of the new members (members of cast16 only): hat_style `stovepipe16` (tall black, colours light/base/dark/shine/band/brim), `slouch16`, `mane16` (hair mass; `mane_sweep`); costume `tail16` (colors base / dark / lapel / vest / plaid / plaid2 / shirt / collar / tie / sash; `sash16=True`), `braces16` (colors base / dark / collar / brace / brace_l / belt / pants, `plaid`, `dirt16=True`); face keys `whisker16=dict(style="long"|"chops", color, shade, y1, w, wmid)` (side-whiskers that follow the yaw), `collar16=True` (white collar points over the jaw), `nose16=<colour>`. The frock coats, glasses, derby, tophat, fringe hair, curl lock, bushy moustache, eyeshade, flatnews cap, straw hat and garters come from earlier casts.

## Pose keys added (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `young` | 0/1 (0) | morse16 only: the 1825 painter's-smock variant |
| `hat_off` | 0/1 (0) | mocker (bald crown with fringe), cornell (bare head): no hat. Hold the hat with prop `stovepipe_held` / `slouch_held` |
| `sash` | 0/1 (0) | mocker only: postmaster sash + mail bag (+ key ring) |
| `belt_keys` | 0/1 (1) | with `sash`: the key ring on the belt |
| `stool` | 0/1 (0) | **any member**: draws a round three-legged walnut stool behind the hips (seat under `anchors["hip"]`; `stool_w` 0.4..2 (0.95), `stool_dx`, `stool_dy`). Pair it with `legs=dict(crouch=0.40)` to sit. Anchor `seat` |
| `glint` | 0..1 (0) | sparkle + halo on a held `bottle`; blue spark at the poles of a held `magnet` |
| `key_press` | 0..1 (0) | the lever of a held `telegraph_key` pressed down |
| `t` | float | flame lean of the `candle` (loop 0..1) |

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | follows | anchors |
|---|---|---|---|
| `letter` | sealed letter, cream paper, red wax seal, no writing | upright | |
| `wire_coil` | coil of copper wire seen face-on, loose end | upright | |
| `magnet` | red horseshoe magnet, silver poles (spark with `glint`) | `angle`, poles toward +x | `magnet_r/_l` (the poles) |
| `bottle` | green beer bottle 0.8 long, blank label; the hand holds the NECK (lip at +0.29; `angle=90` = inverted, lip down, for capping a pole peg) | `angle` | `bottle_r/_l` (the lip) |
| `money_bag` / `money_bag_empty` | canvas sack with a tied neck, no marks / limp sack with the lining turned out | upright (hangs from the hand) | |
| `telegraph_key` | walnut base, brass lever, black knob under the hand | upright | `key_tip_r/_l` |
| `candle` | brass chamberstick (ring handle at the hand), cream candle, flame + glow | upright | `flame_r/_l` |
| `stovepipe_held` / `slouch_held` | a hat held by the brim, crown up | upright | |
| `keyring16` | iron ring with five skeleton keys, hanging | upright | |
| `cane16` | black cane, gold knob and ferrule (1.4 long; use `scale` 0.6 for a hand cane) | `angle` | `cane_*`, `grip_far_*` |
| `palette16` / `brush16` | artist's kidney palette with paint dabs / fine brush with a red tip (0.8) | `angle` | `palette_*`, `brush_*` |
| `shovel16` / `pick16` | long shovel (2.0) with a D grip / pickaxe (1.6) | `angle` | `blade_*` / `pickhead_*`, `grip_far_*` |
| `pole16` / `pole16_end` | telegraph pole 3.6 long, hand at 1/3 of it / hand at the butt end (3.6 forward) | `angle` | `pole_tip_*`, `grip_far_*` |
| `plough16` | plough handle with the iron beam bracket at 1.2 | `angle` | `beam_*`, `grip_far_*` |

`grip_far_r/_l` (0.55 along the prop) is where the second hand goes: `cast16._grip2(S, name)` does it for a STORY entry.

## The mule (`mule`; own drawing path, same return dict `svg, feet_y, bbox, anchors`)

Side view facing screen-right (`mirror=True` for left). **Origin = the head centre of the neutral pose; the body extends to -x; the hooves stand on `cast16.MULE_G` = 3.00 (`feet_y`).** Hooves are always planted on that line, so Actor placement works as for people. `puppet.CAST["mule"]` is a stub (so name checks pass); use `cast16.cycle("mule", ...)` / `cast16.mule_cycle`, not `lerp_pose`.

| key | range (default) | effect |
|---|---|---|
| `phase` | 0..1 | gait phase (lateral-sequence walk: hind near, fore near, hind far, fore far) |
| `stride`, `lift` | 0..1.2 (0), 0..1.5 (1) | stride size (0 = standing), foot lift |
| `bob`, `head_pitch`, `head_dy` | D, deg (+ = nose down), D | body bob, head nod about the poll |
| `ear` | -1..1 (0) | -1 ears pinned back, +1 forward |
| `tail`, `droop` | -1..1, 0..1 | tail swing, tail hanging |
| `strain` | 0..1 | leaning into the collar: head low, ears back, shorter stride, strained eye |
| `expr` | neutral / strain / blink / sleepy / happy / surprised | eye; discrete |
| `bray` | 0/1 | mouth open (a held shape: the mule never lip-syncs) |
| `harness` | 0 / 1 / 2 | 0 none; **1 plough** (bridle, red padded collar with brass hames, saddle pad with ring, belly girth, breeching, **traces** ending in an iron ring at `trace_end`); **2 buggy** (same, with a **shaft** along the flank ending at `shaft_end`, reins to the saddle ring) |
| `rest` | 0..1 | standing: one hind leg cocked |
| `gaze`, `mirror`, `tint`, `ink` | | as for people |

Anchors: `head`, `head_top`, `hat_top` (ear tips), `mouth`, `eye_r/_l`, `withers`, `hip`, `chest`, `collar`, `tail_tip`, `hoof_fn/ff/hn/hf` (fore near/far, hind near/far), `foot_r/_l` (the fore hooves), `feet` (mean of the four hooves, on y = 3.00), `trace_end`, `shaft_end`.
`cast16.cycle("mule", phase, mode, facing, base)`: `walk` (~36 frames per cycle at 30 fps), `pull` (strained, ~44 frames), `idle` (tail swish, ear flick, cocked hind leg, ~90 frames); `facing=-1` mirrors; `base` keeps your keys (`harness`, `expr`, ...). **A plough team** = two `mule` figures with `harness=1`, one phase offset by 0.25 and its far legs tinted (`tint`) a touch darker; **the buggy** = one mule with `harness=2` and the set's buggy attached at `shaft_end`.

## People cycles, lip-sync, blink

`cast16.cycle(cast, phase, mode, facing, base, arms, speed)` for people is cast6's (`walk` ~28 frames, `run` ~16, `sneak` ~32, `march` ~24), `cast16.talk_mouth(frame, level, seed, hold)`, `cast16.blink_at(frame, period, offset)`, `cast16.NOD`.
**Mouths.** Only the mocker's four lip-sync poses (`STORY16_META[name]["lipsync"] = True`) are meant to be driven with `mouth = talk_mouth(g)`: boss quote 18.32-23.20 s (`mocker_mock_point` 18.32-19.9, `mocker_boast_chest` / `mocker_boast_finger` 19.9-23.2) and false quote 38.46-40.80 s (`mocker_taunt_buggy`). Outside the quotes set their mouth to `"flat"`. Every other pose of every member holds one fixed mouth (expression mouth, `("open", w, h)` for the jaw drop / yawn).

## STORY16 (`cast16.STORY16[name] = (cast, pose)`, also merged into `puppet.STORY`; `STORY16_META[name]["note" | "shots" | "lipsync"]`; `STORY16_SHOTS[shot] = [names]`)

Mapped to the shot plan (`film16/shot_plan.md`). Screen-right is the facing side; use `mirror=True` for left. 70 poses.

| shot | poses |
|---|---|
| 1 | `morse_cap_peg`, `morse_drape_wire` |
| 2 | `morse_proud_point` |
| 3 | `morse_tap_wire_grin` |
| 4 | `morse_young_idle`, `morse_young_paint` |
| 5 | `morse_young_paint`, `morse_young_palette_ready` |
| 6 | `morse_young_read_letter`, `morse_young_palette_drop`, `morse_young_stool`, `messenger_hand_letter`, `messenger_idle` |
| 7 | `morse_show_coil_magnet` |
| 8 | `morse_present_table`, `congressman_a_amazed` |
| 9 | `mocker_mock_point`, `mocker_belly_laugh` |
| 10 | `mocker_boast_chest`, `mocker_boast_finger` |
| 11 | `congressman_a_laugh`, `congressman_b_laugh`, `congressman_c_laugh`, `congressman_a_point`, `congressman_b_point`, `congressman_c_point`, `mocker_belly_laugh`, `morse_clutch_coil`, `morse_snap_up` |
| 12 | `morse_relieved`, `mocker_sour_arms` |
| 13 | `cornell_plough`, `cornell_direct`, `worker_a_shovel`, `worker_b_shovel`, `worker_b_pick` |
| 14 | `cornell_plough`, `worker_a_shovel`, `worker_b_shovel` |
| 15 | `morse_key_press`, `morse_key_wait`, `cornell_wait`, `worker_a_lean_shovel`, `worker_b_lean_shovel`, `worker_a_wait_arms` |
| 17 | `morse_empty_bag`, `worker_a_lean_shovel`, `worker_b_lean_shovel` |
| 18 | `mocker_taunt_buggy`, `mocker_belly_laugh` |
| 19 | `morse_raise_pole`, `worker_a_raise_pole`, `worker_b_raise_pole`, `worker_a_carry_pole`, `worker_b_carry_pole` |
| 21 | `morse_key_wait`, `morse_key_press`, `cornell_hat_over`, `worker_a_wait_arms` |
| 22 | `morse_bottle_sun` |
| 23 | `morse_cap_peg`, `morse_drape_wire` |
| 25 | `morse_cheer` |
| 26 | `morse_read_tape`, `morse_cheer`, `congressman_a_amazed`, `congressman_b_amazed`, `congressman_c_amazed`, `mocker_jaw_drop`, `mocker_hat_in_hand_amazed` |
| 27 | `messenger_wave`, `worker_a_wave`, `congressman_b_wave`, `congressman_c_wave` |
| 28 | `mocker_pm_proud`, `mocker_pm_keys`, `mocker_pm_sour` |
| 29 | `clerk_slide_instrument`, `clerk_idle`, `mocker_pm_proud`, `mocker_horror` |
| 30 | `mocker_stool_candle`, `mocker_stool_candle_nod`, `morse_peek_door` |

Shots 16 and 20 (the cut-away trench, the rain on the poles) and 24 (the macro pulse) have no acting from this cast.

| name | cast | shots | what |
|---|---|---|---|
| `morse_idle` | morse16 | any | standing, calm |
| `morse_cap_peg` | morse16 | 1, 23 | on the ladder (3D rails in the set), arm up, capping the pole-top peg with the INVERTED bottle neck (lip down at anchor bottle_r); glint=1 flashes |
| `morse_drape_wire` | morse16 | 1, 23 | on the ladder, free hand lifting the wire over the glass, coil on the other arm |
| `morse_proud_point` | morse16 | 2 | foot of the ladder, pointing proudly down the line of poles (screen-right) |
| `morse_tap_wire_grin` | morse16 | 3 | taps the wire (screen-right) and grins at it |
| `morse_cheer` | morse16 | 25, 26 | both arms up, laughing with joy |
| `morse_show_coil_magnet` | morse16 | 7 | holds up the horseshoe magnet (blue spark at its poles, glint=1) and the copper coil: the idea |
| `morse_present_table` | morse16 | 8 | presenting the instrument to the tiers: one open hand out (screen-right) |
| `morse_clutch_coil` | morse16 | 11 | laughed at: clutches the copper coil to his chest, hurt but resolute |
| `morse_snap_up` | morse16 | 11 | chin up after 'ไอ้บ้าลวด': coil held, jaw set |
| `morse_relieved` | morse16 | 12 | looking at the money bag on the table, a small relieved smile |
| `morse_key_press` | morse16 | 15, 21 | crouched at the crate, pressing the key (prop telegraph_key, anchor key_tip_r; key_press 0..1 animates the lever); skip the prop when the set shows the key |
| `morse_key_wait` | morse16 | 15, 21 | same crouch, key released, waiting: nothing happens |
| `morse_empty_bag` | morse16 | 17 | turns out the empty money bag (lining sticking out), shoulders down |
| `morse_raise_pole` | morse16 | 19 | heaving a bare pole up with the workers (pole16 at angle -72; anchor pole_tip_r) |
| `morse_bottle_sun` | morse16 | 22 | 'the answer is glass': holds the empty green bottle up to the sun, glint=1 |
| `morse_read_tape` | morse16 | 26 | leans over the table reading the paper tape (dots and dashes are set art) |
| `morse_peek_door` | morse16 | 30 | peeking round the door frame at the end (screen-left), grinning |
| `morse_young_idle` | morse16 (young) | 4 | the 1825 studio Morse standing |
| `morse_young_paint` | morse16 (young) | 4, 5 | painting the big portrait on the easel (screen-right), brush in the right hand, palette on the other arm |
| `morse_young_palette_ready` | morse16 (young) | 5 | brush up, palette in hand, pleased |
| `morse_young_read_letter` | morse16 (young) | 6 | reads the sealed letter (prop letter), the palette starting to tip in the other hand |
| `morse_young_palette_drop` | morse16 (young) | 6 | the palette slips from his fingers (animate prop_l angle 40 -> 90, then drop it in the set; no injury) |
| `morse_young_stool` | morse16 (young) | 6 | sunk on a stool, looking at the small oval portrait (screen-right), hands in his lap |
| `mocker_idle` | mocker | any | standing smug |
| `mocker_belly_laugh` | mocker | 11, 18 (lead-in) | BELLY LAUGH, head back, hands on the belly; the expression's own laughing mouth (no lip-sync); bounce: squash (1.03, 0.97) <-> (0.99, 1.01) at ~3 Hz and +/-0.06 D of hips |
| `mocker_mock_point` | mocker | 9 | **LIP-SYNC.** rising from the desk, pointing at the wire (screen-right), quote 1 'ส่งข่าวทางลวดเนี่ยนะ!'; LIP-SYNC with talk_mouth(g) 18.32-19.9 |
| `mocker_boast_chest` | mocker | 10 | **LIP-SYNC.** thumbs / thumps his own chest, chin up: 'ข้าจะมานั่งเฝ้ามันเอง!'; LIP-SYNC 19.9-23.2 |
| `mocker_boast_finger` | mocker | 10 | **LIP-SYNC.** alt for shot 10: index finger up, other hand on the chest; LIP-SYNC |
| `mocker_taunt_buggy` | mocker | 18 | **LIP-SYNC.** leaning out of the open buggy (hips on the seat: legs crouched), laughing and pointing down at the furrow: 'เห็นมั้ย ลวดของเอ็ง ตายอยู่ใต้ดินแล้ว!'; LIP-SYNC 38.46-40.80 + bounce |
| `mocker_sour_arms` | mocker | 12 | SOUR: arms folded across the belly, mouth down |
| `mocker_jaw_drop` | mocker | 26 | JAW DROP: held wide-open mouth, ring eyes, arms hanging |
| `mocker_hat_in_hand_amazed` | mocker | 26 | hat off in his hand, jaw hanging (variant hat_off=1 shows the bald crown with the fringe) |
| `mocker_horror` | mocker | 29 | HORROR (postmaster, sash on): hands up at the cheeks, ring eyes, sweat; the proud smile has dropped |
| `mocker_pm_proud` | mocker | 28 | POSTMASTER posing: chest out, hand on his sash (federal-green sash, leather mail bag at the hip, iron key ring on the belt) |
| `mocker_pm_keys` | mocker | 28 | dangling a ring of keys from his hand (screen-right) as head of the Post Office |
| `mocker_pm_sour` | mocker | 28, 29 | postmaster, arms folded (sash on) |
| `mocker_stool_candle` | mocker | 30 | ENDING: bald postmaster asleep-eyed on a stool, YAWNING (held wide mouth, hand to the mouth), candle in the other hand (animate t for the flame); tape piling at the boots is set art |
| `mocker_stool_candle_nod` | mocker | 30 | ENDING: head nodding on his chest, candle still in hand |
| `congressman_a_laugh` | congressman_a | 11 | laughing, hands on the belly (bounce: squash 1.03/0.98 at ~3 Hz; the hat bounces with it) |
| `congressman_a_point` | congressman_a | 11 | laughing and pointing at Morse (screen-right; mirror=True for left) |
| `congressman_a_amazed` | congressman_a | 26 | amazed at the tape: ring eyes, hands up |
| `congressman_b_laugh` | congressman_b | 11 | laughing, hands on the belly (bounce: squash 1.03/0.98 at ~3 Hz; the hat bounces with it) |
| `congressman_b_point` | congressman_b | 11 | laughing and pointing at Morse (screen-right; mirror=True for left) |
| `congressman_b_amazed` | congressman_b | 26 | amazed at the tape: ring eyes, hands up |
| `congressman_c_laugh` | congressman_c | 11 | laughing, hands on the belly (bounce: squash 1.03/0.98 at ~3 Hz; the hat bounces with it) |
| `congressman_c_point` | congressman_c | 11 | laughing and pointing at Morse (screen-right; mirror=True for left) |
| `congressman_c_amazed` | congressman_c | 26 | amazed at the tape: ring eyes, hands up |
| `messenger_hand_letter` | messenger | 6 | holds the sealed letter out to Morse (screen-right) |
| `messenger_idle` | messenger | 6 | standing, cap on |
| `clerk_slide_instrument` | clerk16 | 29 | bent forward, both hands sliding the instrument across the table (screen-right) |
| `clerk_idle` | clerk16 | 29 | standing, sleeve garters |
| `cornell_plough` | cornell | 13, 14 | behind the plough, both hands on the handles, leaning into it (screen-right) |
| `cornell_hat_over` | cornell | 21 | holds his slouch hat over Morse in the rain (screen-right); hat_off=1 gives the bare head (the hat is in his hand) |
| `cornell_wait` | cornell | 15 | arms folded, waiting for the register to click |
| `cornell_direct` | cornell | 13 | directing the trench (screen-right) |
| `worker_a_lean_shovel` | worker16_a | 15, 17 | leaning on the shovel, waiting |
| `worker_a_shovel` | worker16_a | 13, 14 | digging / following the plough with the shovel (screen-right) |
| `worker_a_carry_pole` | worker16_a | 19 | carrying a pole on the shoulder (screen-right; pole16 centred on the hand) |
| `worker_a_raise_pole` | worker16_a | 19 | heaving the pole upright with Morse (pole16_end at -75) |
| `worker_b_lean_shovel` | worker16_b | 15, 17 | leaning on the shovel, waiting |
| `worker_b_shovel` | worker16_b | 13, 14 | digging / following the plough with the shovel (screen-right) |
| `worker_b_carry_pole` | worker16_b | 19 | carrying a pole on the shoulder (screen-right; pole16 centred on the hand) |
| `worker_b_raise_pole` | worker16_b | 19 | heaving the pole upright with Morse (pole16_end at -75) |
| `worker_b_pick` | worker16_b | 13 | pick over the shoulder, leaning back |
| `messenger_wave` | messenger | 27 | waving the news on the platform (open hand up; animate hand x +-0.12 at 3 Hz) |
| `worker_a_wave` | worker16_a | 27 | waving the news on the platform |
| `congressman_b_wave` | congressman_b | 27 | waving, delighted, on the platform |
| `congressman_c_wave` | congressman_c | 27 | dandy waving with both hands on the platform |
| `worker_a_wait_arms` | worker16_a | 15, 21 | arms folded, waiting |

Animation recipes: **bounce** (laughs) = animate `squash` (1.03, 0.97) <-> (0.99, 1.01) at ~3 Hz and the stage position +/-0.06 D; the stovepipe bounces with the head. **Palette slip** (shot 6) = tween `prop_l` angle 40 -> 90 from `morse_young_read_letter` to `morse_young_palette_drop`, then drop it in the set. **Key press** = `key_press` 0 -> 1 -> 0 on `morse_key_press`. **Yawn** = `mocker_stool_candle`, then `mocker_stool_candle_nod`; `t` drives the flame.

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D)

`cast16.CANVAS16[member]`: morse16 (-1.8125, -3.875, 1.8125, 0.125); mocker (-1.5625, -4.4375, 1.5625, 0.125); congressman_a (-1.25, -3.625, 1.25, 0.125); congressman_b (-1.25, -3.0625, 1.25, 0.125); congressman_c (-1.25, -3.9375, 1.25, 0.125); messenger (-1.1875, -2.75, 1.1875, 0.125); clerk16 (-1.3125, -3.25, 1.3125, 0.125); cornell (-2.375, -3.5625, 2.375, 0.125); worker16_a (-2.0625, -3.375, 2.0625, 0.375); worker16_b (-2.0625, -4.3125, 2.0625, 0.1875); mule (-3.1875, -4.125, 3.1875, 0.125).
Extra cards: `CANVAS16_POLE` (the carry / raise-a-pole poses of morse16, worker16_a, worker16_b: taller / wider), `CANVAS16_BUGGY["mule"]` (-3.125, -4.125, 3.1875, 0.125, with the shaft; the ordinary mule canvas already holds the traces). The sprites of poses on a `stool` and with a held `cane16` fit these cards; `test_cast16.py canvas` checks every STORY16 pose (mirrored too), 16 phases x 4 modes x 2 facings of every person's cycles, yaw sweeps and 24 phases x 3 modes of the mule (plain, harness 1, strained, bray): 0 outside, smallest margin 0.04 D.

## Files and QA

- `cast16.py` the module; `test_cast16.py` (`story`, `identity`, `canvas`, `robust`, `sheet`, `full` / default); `sheet.jpg` lineup with a height ruler + every STORY16 pose labelled + the mule's gaits + face states + props; `run_log.txt`.
- `identity`: 0 of 1 014 earlier renders differ. The pose key `stool` (new) is the one key that also works on earlier members; no earlier pose uses it.

## Known limits

- Morse's hair mass is a hat-layer shape (`mane16`): it reads as a swept mane but not as individual strands; the face stays the standard puppet disc (the long face is carried by the whiskers and the collar).
- The mocker's coat sleeves are the same black as the coat: an arm crossing the coat reads by its white cuff only. The tails sit behind the hips.
- The mule's hind legs are a two-bone IK (the hock bends backwards): in the extreme forward reach the thigh reads thick. Mule heads do not lip-sync.
- Sitting (`stool`) is the puppet's crouch plus a drawn stool: the thighs are not foreshortened; frame it from the chest up or hide the legs behind the set's table when possible.
- The `money_bag` has no `$` mark (the film has no text anywhere).
- `head_flip` (stage/sprites mirrored head disc check) was not run: no Blender stage in this session.
