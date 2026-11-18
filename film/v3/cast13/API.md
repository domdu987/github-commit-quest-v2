# cast13.py: the cast of film 13 ("ไอ้แม่แรง", raising the Tremont House, Chicago 1861) for the v2 puppet

File: `film/v3/cast13/cast13.py`. Python 3 stdlib only, deterministic, no text anywhere (newspaper and banknotes are grey rules and ornaments; no Thai or Latin text is needed).
Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast13 imports cast10, which chains cast9 .. cast_ext and v2/puppet, and wraps `_norm`, `_prop` and `figure` on top of cast10's wrappers (each falls through, so every earlier member draws exactly as before: `python3 test_cast13.py robust` compares the SVG hash of all 28 STORY10 poses with and without cast13: identical). It also adds costumes `rich13`, `crinoline13`, `pull13`, the hat `bonnet13`, the expression `dazed`, ten props, and the cast members below.

```python
import sys
sys.path.insert(0, ".../v3/cast13")
import cast13                # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                # same module object: CAST now has all the members below
cast, pose = cast13.STORY13["pullman_blow_whistle"]
f = puppet.figure(cast, pose, "f")                                          # f["anchors"]["whistle_lip_r"] = the mouthpiece
p = dict(cast13.STORY13["rich_mock_point"][1], mouth=cast13.talk_mouth(g, 1.0), blink=cast13.blink_at(g, 90))      # lip-sync frame g
w = puppet.figure("worker13_a", cast13.cycle("worker13_a", g / 28.0, "walk"), "f")
a = actors.Actor("pul", "pullman"); a.build(cast13.CANVAS13["pullman"], sprite_dir, contact=True)   # or sprites.DEFAULT_CANVAS (registered)
a = actors.Actor("rj", "worker13_a"); a.build(cast13.CANVAS13_POSE["worker_turn_bar_A_a"], sprite_dir, contact=True)   # a special pose: its own canvas
```

Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies unchanged: scale and anchor conventions (head D = 1, head centre at the origin, y down, `feet_y`, anchors `feet`, `hand_r/_l`, `mouth`, `eye_r/_l`, `hip`, `head_top`, `hat_top` ... after squash and mirror), pose keys `yaw pitch head_roll head_dx/dy lean squash expr mouth blink gaze arm_r arm_l legs prop_r prop_l fx t tint ink limb_w rim mirror`, the expressions, `lerp_pose`, `hand_for_tip`. Props are attached to the hand ball and drawn in the arm's layer; two-handed props publish `grip_far_r/_l` (put the other hand there). `mirror=True` flips everything (the prop side letters swap, set dressing is mirrored with it; the head disc stays unmirrored).

## Cast (head D = 1; "head top to soles (with hat)" measured on the lineup pose)

| key | head top to soles (hat) | canvas (feet-relative, D) |
|---|---|---|
| `pullman` | 3.22 (3.48) | `(-1.6875, -4.625, 1.6875, 0.125)` |
| `rich` | 3.33 (3.91) | `(-1.8125, -4.9375, 1.8125, 0.125)` |
| `worker13_a` | 3.22 (3.33) | `(-1.625, -4.625, 1.625, 0.125)` |
| `worker13_b` | 3.20 (3.30) | `(-1.625, -4.5625, 1.625, 0.125)` |
| `worker13_c` | 3.04 (3.38) | `(-1.625, -4.4375, 1.625, 0.125)` |
| `foreman13` | 3.27 (3.53) | `(-1.75, -4.6875, 1.75, 0.125)` |
| `lady13` | 2.96 (3.22) | `(-1.625, -4.375, 1.625, 0.3125)` |
| `lady13_seat` | 2.96 (3.22) | `(-1.625, -4.375, 1.625, 0.125)` |
| `gentleman13` | 3.22 (3.48) | `(-1.6875, -4.625, 1.6875, 0.125)` |
| `town_a` | 3.24 (3.30) | `(-1.75, -4.625, 1.75, 0.125)` |
| `town_b` | 2.96 (3.22) | `(-1.625, -4.375, 1.625, 0.3125)` |
| `town_c` | 2.44 (2.56) | `(-1.5, -3.8125, 1.5, 0.125)` |

| key | look |
|---|---|
| `pullman` | young engineer: slim, dark charcoal frock coat (cream turned-back cuffs), ochre waistcoat, teal cravat, low brown derby (bowler look), small brown moustache, calm face. The brass whistle hangs on its chain from a waistcoat button to the pocket (costume `pull13`; pose key `whistle_hang=0` hides it while the whistle is in the hand) |
| `rich` | the mocker: huge round belly (torso 1.62 D wide), loud emerald waistcoat with a yellow check, gold watch chain swagged across the belly with a fob and watch (costume `rich13`), grey mutton-chop whiskers (cast5 `sideburns`), tall black silk top hat with a wine band, ruddy cheeks, double chin |
| `worker13_a` | grey-brown flat cap, cream shirt, blue bib overalls, black moustache |
| `worker13_b` | brick-red cap, big brown beard, teal shirt, brown overalls (a stockier build) |
| `worker13_c` | striped teal knit cap with a pom, ginger side curls and moustache, freckles, cream shirt, brown overalls (short and slim) |
| `foreman13` | broad, brown derby, big dark moustache, rust waistcoat over cream sleeves; holds the whistle |
| `lady13` | crinoline (costume `crinoline13`: dress7 + hoop rings + cream apron panel, wide bell), burgundy jacket and skirt, cream bonnet with a teal ribbon tied under the chin (hat `bonnet13`) |
| `lady13_seat` | the same lady with a shorter, narrower skirt for sitting in the armchair (the crinoline hem is tied to leg length and would hang below the floor of a seated pose) |
| `gentleman13` | cast7 gentleman recoloured: brown frock coat, teal waistcoat, red tie, grey walrus moustache, grey derby |
| `town_a` / `town_b` / `town_c` | townsman (stout, green coat, flat cap, rust waistcoat, brown moustache) / townswoman (mustard bonnet, teal jacket, purple crinoline) / boy (blue cap, brown jerkin, yellow scarf) |

Internal members `<name>_nohat` (bare head) exist for every member above; `figure` swaps to them for the flying hat. They are not meant to be used directly.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `armchair` | 0 / 1 / `"red"` / `"teal"` (0) | draws a velvet armchair BEHIND the figure, seat at the hip; use with `legs=cast13.SEAT` (crouch 0.5). anchor `chair_seat` |
| `jack` | 0 / 1 (0) | with a `jack_bar` prop: draws the cast-iron screw jack standing under the bar's hole (anchor `bar_pivot_r/_l`), base on the figure's floor line. Anchors `jack_collar`, `jack_top`, `jack_base` |
| `jack_turn` | float (0) | slides the screw thread (animate 0 -> 1 per half turn) |
| `mud` | 0..1 (0) | mud puddle under the hips + mud smears on chest, belly, hands, feet, cheek, hat band (smears appear one by one as the value rises) |
| `dizzy` | 0 / 1 (0) | four yellow stars circling above the head; animate with `t` |
| `tumble` | degrees -180..180 (0) | rotates the whole figure about the hip (clockwise positive; mirror-aware). `feet_y` stays the standing sole line, there is no ground contact |
| `hat_fly` | (dx, dy, rot_deg) | the hat leaves the head: the figure is drawn bare-headed and the hat is drawn at (dx, dy) from the head centre, rotated. Hat comes from the member's own `hat_style` (anchor `hat_fly`) |
| `blast` | 0..1 (0) | sound arcs from a held `whistle` (arcs advance with `t`) |
| `whistle_hang` | 0 / 1 (1) | pullman only: the whistle on its chain in the pocket |
| `tea` | 0..1 (1) | tea in the cup (0 = empty); the surface is a flat colour that never ripples |
| `t` | float | phase for the arcs, birdies, mud drops |

New expression: **`dazed`** (ring eyes, one raised brow, wavy mouth), added to `puppet.EXPRESSIONS` only if missing.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | held how | anchors |
|---|---|---|---|
| `whistle` | brass whistle (mouthpiece, chamber with window, ring) + a gold chain that always runs to the waistcoat pocket (0.05, 0.98 in the head frame) | hand grips the chamber; `angle` 0 = mouthpiece toward screen-left (for the right hand at the mouth) | `whistle_r/_l`, `whistle_lip_r/_l` (put this on `mouth`: `cast13._to_anchor`) |
| `plans` | rolled plans: cream paper tube, red ribbons, a blue-print flap curling out of the far end | follows `angle` (-18 for the baton pose); tip 0.42 | `plans_end_r/_l`, `grip_far_r/_l` |
| `teacup` | china cup with a gold band, tea, handle, and the **little finger sticking out** (an ink stroke from the hand) | pinches the handle, cup toward the body, always upright | `cup_r/_l`, `pinky_r/_l` |
| `saucer` | saucer, always upright, hand under it | | `cup_r/_l` (centre) |
| `teacup_saucer` | cup standing on the saucer, hand under the saucer | | `cup_r/_l` |
| `jack_bar` | iron bar 1.30 long, tapered end, knob | follows `angle`; the collar hole of the jack is 1.02 from the hand | `bar_pivot_r/_l`, `grip_far_r/_l` (0.34 along the bar) |
| `iron_jack` | carried cast-iron jack: base plate, housing, thread, cap, bar through the collar | follows `angle` (-62 on the shoulder); tip 0.60 | `grip_far_r/_l`, `jack_top_r/_l` |
| `purse` | fat leather purse hanging from the hand, cord, a banknote poking out | hangs straight down | `purse_bottom_r/_l` |
| `bills` | fan of five banknotes (pale green, ornament, no text) | follows `angle` | |
| `newspaper13` | open broadsheet (grey rules, picture box, NO readable text), upright | hand on the near edge; sheet toward the body centre | `paper_centre_r/_l`, `grip_far_r/_l` (put the other hand there) |

Standalone SVG pieces (D units, hand at the origin): `whistle_svg`, `plans_svg`, `teacup_svg(saucer, pinky, tea)`, `jack_bar_svg`, `iron_jack_svg`, `jack_svg(uid, x, y_collar, y_floor, top, turn)` -> (svg, anchors), `purse_svg`, `bills_svg`, `newspaper_svg`, `armchair_svg(uid, hip_y, floor_y, hw, col)` -> (svg, bbox), `mud_pool_svg`.

## Mouths and lip-sync (same mechanism as cast10)

`cast13.talk_mouth(frame, level, seed, hold)`, `cast13.blink_at(frame, period, offset)`, `cast13.NOD` and `cast13.cycle(cast, phase, mode, facing, base, arms, speed)` are cast6's, re-exported, and work for every member. The mouth names are `talk_a`, `talk_b`, `talk_o`, `flat` (silent), `("open", w, h)`. Only `rich_mock_point` is marked `STORY13_META[name]["lipsync"] = True`: drive `mouth = talk_mouth(g)` during his two quotes (boss line about 19.7 - 28 s and the false line about 36.9 - 43 s of the narration), and `"flat"` outside them. `rich_laugh_big` holds an open laugh mouth that does not move. The whiskers do not cover the mouth (the moustache is short), so all shapes read; `STATES` in the sheet shows neutral / talk_a / talk_b / talk_o / flat / blink 1 / blink 2 for every member.

## STORY13 (`cast13.STORY13[name] = (cast, pose)`, also merged into `puppet.STORY`) and `STORY13_META[name]["note"]`

41 poses; all use the right-hand side as the working side, `mirror=True` for the left.

| name(s) | cast | what |
|---|---|---|
| `pullman_stand_calm` | pullman | calm, one hand behind the back, one on the hip |
| `pullman_point_plan` | pullman | rolled plans held like a baton, pointing |
| `pullman_blow_whistle` | pullman | whistle between the lips, blast arcs, other hand raised as the signal |
| `pullman_hand_on_jack_bar` | pullman | crouched, both hands on the jack bar, jack drawn (canvas `CANVAS13_POSE`) |
| `pullman_look_up_confident` | pullman | chin up, looking at the rising hotel, fists on hips |
| `pullman_nod_smile` | pullman | nod (animate pitch 0.45 <-> -0.05), smile |
| `rich_laugh_big` | rich | head thrown back, hands on the belly, tears |
| `rich_mock_point` | rich | pointing and mocking, **lip-sync** |
| `rich_sit_tea` | rich | in the red armchair, cup lifted with the pinky out, saucer in the other hand (special canvas) |
| `rich_look_window_smug` | rich | standing at the window, smug, hand behind back, cup + saucer with still tea in the other |
| `rich_step_out` | rich | one foot in the air over nothing, eyes wide, arms flung (anchor `foot_r`) |
| `rich_fall` | rich | tumbling (`tumble=28`), arms up, legs kicking, top hat flying (special canvas, wide) |
| `rich_sit_in_mud` | rich | sitting in the puddle, dazed, hat askew, birdies, no injury (special canvas) |
| `rich_pay_sad` | rich | sad, handing over the fat purse, banknotes in the other hand |
| `worker_turn_bar_A_a/_b/_c`, `worker_turn_bar_B_a/_b/_c` | worker13_a/_b/_c | the 2-frame push cycle on a jack bar: bar -16 / +16 degrees about the SAME hole (the jack collar is identical relative to the feet in A and B: tested); loop A, B, A, B; `jack_turn` 0 / 0.5 |
| `worker_carry_jack_a/_b/_c` | workers | walk frame with an iron jack on the shoulder (animate `cycle` and keep `arm_r`, `prop_r`) |
| `worker_stand_a/_b/_c` | workers | standing, hand on hip |
| `worker_cheer_a/_b/_c` | workers | both arms up, laughing mouth |
| `foreman_blow_whistle`, `foreman_stand` | foreman13 | whistle blown / waiting with the whistle in hand |
| `lady_sip_tea` | lady13_seat | in the teal armchair, cup lifted, pinky out (special canvas) |
| `lady_stand` | lady13 | hands folded |
| `gentleman_read` | gentleman13 | in the red armchair reading the (textless) broadsheet (special canvas) |
| `gentleman_stand` | gentleman13 | hands behind the back |
| `town_laugh_point_a/_b/_c`, `town_stand_a/_b/_c` | town_a/_b/_c | pointing and laughing / standing |

## Canvases (feet-relative, D; registered in `cast_ext.CANVAS` -> `sprites.DEFAULT_CANVAS`)

Per member (ordinary poses, all arm presets with the new props at yaw +-0.6, crouch, wide legs, fx, yaw +-1.2, the cycles; at least 0.33 D head room):

| member | canvas |
|---|---|
| `pullman` | `(-1.6875, -4.625, 1.6875, 0.125)` |
| `rich` | `(-1.8125, -4.9375, 1.8125, 0.125)` |
| `worker13_a` | `(-1.625, -4.625, 1.625, 0.125)` |
| `worker13_b` | `(-1.625, -4.5625, 1.625, 0.125)` |
| `worker13_c` | `(-1.625, -4.4375, 1.625, 0.125)` |
| `foreman13` | `(-1.75, -4.6875, 1.75, 0.125)` |
| `lady13` | `(-1.625, -4.375, 1.625, 0.3125)` |
| `lady13_seat` | `(-1.625, -4.375, 1.625, 0.125)` |
| `gentleman13` | `(-1.6875, -4.625, 1.6875, 0.125)` |
| `town_a` | `(-1.75, -4.625, 1.75, 0.125)` |
| `town_b` | `(-1.625, -4.375, 1.625, 0.3125)` |
| `town_c` | `(-1.5, -3.8125, 1.5, 0.125)` |

Special poses that need a wider/other canvas (armchair, jack, mud, tumble: pass to `Actor.build`): `cast13.CANVAS13_POSE`:

| pose | canvas |
|---|---|
| `pullman_hand_on_jack_bar` | `(-1.875, -3.3125, 1.875, 0.125)` |
| `rich_sit_tea` | `(-1.3125, -3.625, 1.3125, 0.125)` |
| `rich_fall` | `(-4.125, -5.375, 4.125, 0.8125)` |
| `rich_sit_in_mud` | `(-1.5625, -3.5625, 1.5625, 0.25)` |
| `worker_turn_bar_A_a` | `(-1.9375, -3.1875, 1.9375, 0.125)` |
| `worker_turn_bar_B_a` | `(-1.9375, -3.1875, 1.9375, 0.125)` |
| `worker_turn_bar_A_b` | `(-1.9375, -3.125, 1.9375, 0.125)` |
| `worker_turn_bar_B_b` | `(-1.9375, -3.125, 1.9375, 0.125)` |
| `worker_turn_bar_A_c` | `(-1.9375, -3.25, 1.9375, 0.125)` |
| `worker_turn_bar_B_c` | `(-1.9375, -3.25, 1.9375, 0.125)` |
| `lady_sip_tea` | `(-0.9375, -3.0625, 0.9375, 0.125)` |
| `gentleman_read` | `(-0.875, -3.25, 0.875, 0.125)` |

`python3 test_cast13.py canvas` re-measures everything and checks head_flip (mirror gives mirrored anchors) and the A/B jack pivot.

## Files and QA

- `cast13.py` is the module; `test_cast13.py` has `sheet` (writes `sheet.jpg`: heights with film 10's admiral for scale / every one of the 41 poses labelled / 16 face states per member / props and set pieces, on neutral warm grey), `canvas`, `robust` (garbage pose keys on all members: 3600 figures; determinism; cast10 hash; v2 `test_puppet.py --quick` on the new members; log in `run_robust.log`).
- Python reproduces the Blender-side pipeline's inputs only; no Blender render was done.

## Known limits

- Rolled sleeves: the cast3 sleeve model cannot show bare forearms; Pullman's "rolled sleeves" are turned-back cream cuffs at the wrist, the workers have short shirt sleeves with a roll at the elbow end (workers only).
- Crinoline ladies are very wide (about 3 D at the hem): they overlap neighbours in a lineup. The seated lady uses the `lady13_seat` variant; a standing lady placed in an armchair would have her hem below the floor.
- The seat is a front view: seated legs are drawn as bent hoses with knees out, not as thighs coming toward the viewer; the armchair is symmetric and drawn behind, so it cannot be turned to 3/4.
- `tumble` rotates the finished drawing (no foreshortening); the sprite canvas for `rich_fall` is 8.25 D wide because the rotated bbox is conservative. Hat and hands may cross the head at extreme angles.
- The jack under the bar is a 2D overlay: the bar passes in front of the collar and the bar hole is not occluded. Its height (collar to thread top 0.95 D) is fixed; it assumes the bar hole sits at about waist height (`worker_turn_bar_*` BAR_P = (1.22, 0.82) in the head frame).
- Held pieces are drawn in the arm's layer (as cast8 .. 10); the little finger is a plain ink stroke, not a real finger.
- The whistle chain always ends at a fixed pocket point of the head frame; at large `lean` it can float a little beside the waistcoat.
- Mutton chops and sideburns read as grey ear-muffs at small size; the mud smears are placed by anchors, not by the costume, so at yaw near +-1 a few land off the cloth.
- `resolve_pose` / `lerp_pose` drop the cast13 keys. Re-add `armchair`, `jack`, `jack_turn`, `mud`, `dizzy`, `tumble`, `hat_fly`, `blast`, `whistle_hang`, `tea` and `t` to tweened poses.
