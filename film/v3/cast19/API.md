# cast19.py: the cast of film 19 ("ไอ้ช่างไม้", John Harrison, England 1730s-1773) for the v2 puppet

File: `PROJ/v3/cast19/cast19.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only, deterministic.
Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import cast19 imports cast10 (which chains cast9 .. cast_ext and v2/puppet; it does NOT import cast16), adds entries to their tables and wraps `_norm`, `_face`, `_prop`, `_ink_limb` and `figure` on top of cast10's wrappers; each wrapper falls through for every earlier member, so every earlier pose draws byte for byte as before (`test_cast19.py identity`: 324 earlier STORY poses + 690 member/pose-key combinations, 0 differ, compared in two separate processes with and without cast19).

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast19")
import cast19                  # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                  # same module object: CAST now also has the members below
cast, pose = cast19.STORY19["astro_belly_laugh"]
f = puppet.figure(cast, pose, "f")
p = dict(cast19.STORY19["astro_mock_point"][1], mouth=cast19.talk_mouth(g, 1.0), blink=cast19.blink_at(g, 90))
w = puppet.figure("harrison19", cast19.cycle("harrison19", g / 28.0, "walk"), "w")
l = puppet.figure("astro19", cast19.laugh_cycle((g % 30) / 30.0, cast19.STORY19["astro_belly_laugh"][1]), "l")
a = actors.Actor("har", "harrison19"); a.build(cast19.CANVAS19["harrison19"], sprite_dir, contact=True)
cast19.key19("sailor_a")      # -> "sailor19_a"
```
Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies: pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, the fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`. No text anywhere (the watch dial has tick marks only).

**Name collisions.** `sailor_a/_b/_c` are CAST keys of film 10, whose output must not change, so they carry a suffix: **`sailor19_a`, `sailor19_b`, `sailor19_c`** (`cast19.ALIAS19` / `key19(name)`). STORY19 names keep the spec spelling (`sailor_a_haul`). All other keys are new.

## Cast (head D = 1; heights head top to soles, hat/wig in brackets)

| key | height | build | look |
|---|---|---|---|
| `harrison19` | 3.16 (3.60) | `slim` 0.66 x 1.02, legs 1.28 | lean, kind, determined. Own **greying hair tied back** with a black ribbon (no wig), forehead lines, linen shirt with **rolled sleeves**, **brown waistcoat**, tan **leather apron** with a pocket of tools (file, chisel, pencil) and **honey wood shavings** (pose key `shavings=0` hides them), buff knee breeches, cream stockings, buckled shoes. Variants: **`young=1`** (1730s) brown hair, smoother face; **`old=1`** (about 80) white hair, **spectacles**, **brown coat** over a tan waistcoat (no apron), slight **stoop by default** (lean 8, head_dy 0.05; pass your own `lean`/`head_dy` to override). CAST `harrison19`, `harrison19_young`, `harrison19_old` |
| `william19` | 3.30 (3.52) | `slim` | his son, about 30: **blue coat** with pale cuffs, buff waistcoat with brass buttons, cravat, **tricorne** (black, gold lace, red cockade) over **own brown hair tied back**, cream breeches, stockings, buckled shoes. `hat_off=1`: bare head, the hair and queue show (CAST `william19_bare`); hold the hat with prop `tricorn_held` |
| `astro19` | 3.29 (3.72) | `stout` 1.50 x 1.20, legs 1.22 | **the mocker**: plump, **red cheeks and a flushed nose**, double chin, huge **full-bottomed powdered wig**, **spectacles pushed up on the forehead**, **dark navy gown with small gold stars** over a **crimson waistcoat with brass buttons**, **lace jabot**, cream breeches |
| `astro19_b` | 3.48 (3.91) | `slim` 0.54, legs 1.58 | thin and tall: **grey bob wig**, **black coat**, grey waistcoat, white neckcloth, frown |
| `astro19_c` | 2.79 (3.22) | `regular`, short | short, **bald forehead** under a small **tie wig** set back with a ribboned queue, **green coat**, buff waistcoat, smirk |
| `king19` | 3.22 (3.66) | `regular` | generic Georgian king: **powdered wig with two rows of side curls** and a black-bagged queue, **blue coat** with gold-edged lapels, **silver Garter star** on the breast, **blue sash**, jabot, cream waistcoat, **white breeches**, white stockings, **red-heeled** buckled shoes |
| `captain19` | 3.30 (3.52) | `regular` | Royal Navy: **navy coat with white facings and gold lace**, buff waistcoat, cocked hat (gold lace, black cockade) over tied grey hair, white cuffs. `hat_off=1`: bare head (CAST `captain19_bare`) |
| `sailor19_a` | 3.00 (3.34) | `regular` | **red-and-cream striped** shirt panel, short blue jacket, yellow kerchief, wide **slops**, **knitted cap** (blue and cream, red ribbon), plaits |
| `sailor19_b` | 3.18 (3.28) | `slim` | **blue-and-white checked** shirt, brown short jacket, cream kerchief, slops, **red dotted head-kerchief** |
| `sailor19_c` | 2.92 (3.36) | `regular`, broad | **navy-and-cream striped** shirt, teal short jacket, orange kerchief, slops, black hair tied back, bare feet |

For scale: film 16's Morse is 3.32, film 10's admiral 3.43.

CAST keys of the new members (members of cast19 only): hat_style `wig19` (`wig19=dict(style="full"|"bob"|"king"|"tie"|"tied", hair_dy=<raise the hairline>)`; colours light/base/dark), `tricornhair19` (tricorne over `hair19` colours); costume `georgian19` (`g19=dict(coat, apron, jabot, stars, sash, star, lace, vest_lace, vbtn, cbtn)`, colors base / dark / lapel / vest / vest_b / shirt / neck / lace / sash / apron / apron_d), `slops19` (`g19=dict(check=bool)`, colors base / shirt / stripe / kerchief / belt / button; the slops are the CAST `shorts`); face keys `specs_up19=True` (forehead spectacles), `nose19=<colour>`; legs `stock19=dict(from, to, color, w)` (stockings between breeches and shoe), `shoe19=dict(buckle, heel)` (buckle and red heel).

## Pose keys added (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `young`, `old` | 0/1 (0) | harrison19 only: picks the 1730s / the ~80-year-old variant |
| `hat_off` | 0/1 (0) | william19, captain19: bare head (own hair) |
| `shavings` | 0/1 (1) | harrison19 (apron): the honey wood-shaving curls on the apron |
| `splash` | 0..1 (0) | the water jet thrown from a `bucket19` |
| `glint` | 0..1 (0) | sparkle on the quadrant's mirror box |
| `t` | float | flame lean of the `candlestick19` (loop 0..1) |
| `stool` | 0/1 (0) | **any member**: draws a round three-legged stool behind the hips (`stool_w`, `stool_dx`, `stool_dy`; anchor `seat`). Pair it with `legs=dict(crouch=0.40)`. No earlier pose uses it |

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | follows | anchors |
|---|---|---|---|
| `h4_watch` | **silver round watch, 0.24 D across**, white dial with minute and hour **tick marks only and two hands, NO numerals**, bow ring; hangs from / sits on the hand | upright | `watch_*` |
| `pocketwatch19` | **gold** pocket watch (0.26 D) with a cream tick-mark dial, two hands, a loop of chain | upright | |
| `quadrant19` | brass Hadley quadrant (0.62): scale ticks, index arm, mirror box, sight vane; hold at the apex | `angle` | `quad19_*` (the sight end) |
| `candlestick19` | brass candlestick with a cream candle, flame and glow (`t`) | upright | |
| `tricorn_held` | a tricorne in the hand (black, gold lace, cockade) | upright | |
| `file19` / `chisel19` | file 0.80 (wooden handle, toothed blade) / chisel 0.55 | `angle` | `file_*` / `chisel_*` |
| `quill19` | quill pen 0.70 | `angle` | `quill_*` |
| `scroll19` | rolled sealed decree 0.62 with a red ribbon | `angle` | `scroll_*` |
| `chart19` | unrolled sea chart 0.74 x 0.52 (coast, compass rose, rhumb lines), held by its left edge | upright | `chart_grip_far_*` |
| `h1_clock19` | the big brass H1 sea clock, 1.0 x 0.68 at scale 1 (dumbbell balances, gear, frame); hands at its base | upright | `h1_grip_l_*`, `h1_grip_r_*` |
| `rope19` | hauling rope 1.7 long | `angle` | `rope_*`, `grip_far_*` (the second hand: `cast19._grip2`) |
| `bucket19` | wooden bailing bucket, hangs from the hand; `splash` throws a water jet | upright | |

## Cycles, lip-sync, blink

`cast19.cycle(cast, phase, mode, facing, base, arms, speed)` is cast6's (`walk` ~28 frames, `run` ~16, `sneak` ~32, `march` ~24), `cast19.talk_mouth(frame, level, seed, hold)`, `cast19.blink_at(frame, period, offset)`, `cast19.NOD`. **`cast19.laugh_cycle(phase, base)`**: a laugh pose from a base pose (belly bounce squash 1.03/0.97 <-> 0.99/1.01, three bounces per loop, head-roll rocking, `t` for the tears, expr defaults to laughing); animate phase 0..1.
**Mouths.** `astro_mock_point` holds `talk_b` and may be driven with `mouth = talk_mouth(g)`; every other pose holds one fixed expression mouth (`("open", w, h)` for the jaw drop). Set the mouth to `"flat"` outside a quote.

## STORY19 (`cast19.STORY19[name] = (cast, pose)`, also merged into `puppet.STORY`; `STORY19_META[name]["note" | "shots"]`)

Screen-right is the facing side; use `mirror=True` for left. 46 poses. "shot" numbers are suggestions for the film-19 shot plan.

| name | cast | shot | what |
|---|---|---|---|
| `harrison_idle` | harrison19 | any | standing, calm (1750s: greying hair, apron) |
| `harrison_young_idle` | harrison19 | any | the 1730s Harrison: brown hair |
| `harrison_old_idle` | harrison19 | any | about 80: white hair, spectacles, brown coat, a slight stoop |
| `harrison_hold_h1` | harrison19 | 1 | holding up the big sea clock (H1) overhead with both arms, proud grin (prop h1_clock19; anchors h1_grip_l_r / h1_grip_r_r) |
| `harrison_file_bench` | harrison19 | 2 | filing a brass part at the bench (screen-right): file in the right hand, head bent over the work (the part itself is set art) |
| `harrison_chisel` | harrison19 | 2 | alt at the bench: working with a chisel |
| `harrison_show_h4` | harrison19 | 3 | holding up the H4 watch on his open palm (silver, white dial with tick marks, two hands, no numerals) |
| `harrison_tired_rub` | harrison19 | 4 | tired, rubbing his eyes with the back of one hand (eyes shut: blink 2) |
| `harrison_hopeful_door` | harrison19 | 5 | hopeful at the door (door at screen-right; mirror=True for left): hands clasped at the chest, brows up, small smile |
| `harrison_old_handover` | harrison19 | 6 | old Harrison, stooped, handing over a watch to screen-right (the watch sits on his open palm; mirror=True for left) |
| `william_idle` | william19 | any | standing |
| `william_quadrant_sun` | william19 | 7 | aiming the brass quadrant at the sun (up and screen-right), squinting |
| `william_show_h4` | william19 | 8 | showing the H4 on his open palm |
| `william_cheer_hat` | william19 | 9 | cheering with the tricorne raised in his hand (hat_off=1: own tied hair shows) |
| `astro_idle` | astro19 | any | standing smug, specs up on the forehead |
| `astro_belly_laugh` | astro19 | 1 | BELLY LAUGH (laugh cycle: laugh_cycle(phase, pose)): head back, hands on the belly, tears; bounce squash (1.03, 0.97) <-> (0.99, 1.01) at ~3 Hz |
| `astro_mock_point` | astro19 | 2 | mocking, pointing at Harrison (screen-right); mouth talk_b held, or drive it with talk_mouth(g) |
| `astro_mock_bow` | astro19 | 3 | a mock-royal bow, one arm swept back, holding a gold pocket watch as if timing a shot: the mockery |
| `astro_shrug_fluke` | astro19 | 4 | shrug with both palms up: 'a fluke!' |
| `astro_jaw_drop` | astro19 | 9 | JAW DROP: held wide-open mouth, ring eyes, arms hanging |
| `astro_sour_arms` | astro19 | 9 | SOUR: arms folded across the belly, mouth down |
| `astro_b_idle` | astro19_b | any | standing |
| `astro_b_laugh` | astro19_b | 1 | laughing, hands on the belly (laugh cycle) |
| `astro_b_peer` | astro19_b | 9 | peering down at the watch (screen-right), eyes narrowed, one hand at the chin |
| `astro_c_idle` | astro19_c | any | standing |
| `astro_c_laugh` | astro19_c | 1 | laughing, hands on the belly (laugh cycle) |
| `astro_c_peer` | astro19_c | 9 | peering down at the watch (screen-right), eyes narrowed, one hand at the chin |
| `king_idle` | king19 | any | standing, the Garter star and blue sash |
| `king_watch_squint` | king19 | 10 | holding his gold pocket watch beside the silver H4 (one in each open hand, both at chest height) and squinting at them |
| `king_write_seated` | king19 | 11 | seated at a table (the table is set art), writing with a quill (screen-right) |
| `king_point_decree` | king19 | 11 | pointing a decree (screen-right), the rolled and sealed scroll in the other hand, chin up |
| `captain_idle` | captain19 | any | standing, hands behind his back |
| `captain_peer_chart` | captain19 | 12 | peering at a sea chart held out in both hands (screen-right) |
| `captain_cheer` | captain19 | 13 | pleased, one arm up |
| `sailor_a_idle` | sailor19_a | any | standing |
| `sailor_a_haul` | sailor19_a | 14 | hauling on a rope (screen-right), leaning back with the whole body (the second hand goes on the rope: _grip2) |
| `sailor_a_cheer` | sailor19_a | 15 | cheering, both arms up |
| `sailor_a_bail` | sailor19_a | 16 | bailing water out of the ship, comic: bucket flung to screen-right, a jet of water, worried face |
| `sailor_b_idle` | sailor19_b | any | standing |
| `sailor_b_haul` | sailor19_b | 14 | hauling on a rope (screen-right), leaning back with the whole body (the second hand goes on the rope: _grip2) |
| `sailor_b_cheer` | sailor19_b | 15 | cheering, both arms up |
| `sailor_b_bail` | sailor19_b | 16 | bailing water out of the ship, comic: bucket flung to screen-right, a jet of water, worried face |
| `sailor_c_idle` | sailor19_c | any | standing |
| `sailor_c_haul` | sailor19_c | 14 | hauling on a rope (screen-right), leaning back with the whole body (the second hand goes on the rope: _grip2) |
| `sailor_c_cheer` | sailor19_c | 15 | cheering, both arms up |
| `sailor_c_bail` | sailor19_c | 16 | bailing water out of the ship, comic: bucket flung to screen-right, a jet of water, worried face |

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D)

`cast19.CANVAS19[member]`: astro19 (-1.5, -4.0, 1.5, 0.1875); astro19_b (-1.375, -4.125, 1.375, 0.1875); astro19_c (-1.3125, -3.375, 1.3125, 0.1875); captain19 (-1.6875, -3.6875, 1.6875, 0.1875); harrison19 (-2.0, -4.25, 2.0, 0.1875); king19 (-1.375, -3.8125, 1.375, 0.1875); sailor19_a (-2.1875, -3.5625, 2.1875, 0.1875); sailor19_b (-2.125, -3.5625, 2.125, 0.1875); sailor19_c (-2.25, -3.625, 2.25, 0.1875); william19 (-1.1875, -4.0, 1.1875, 0.1875). The variants (young, old, hat_off) share the member's card. `test_cast19.py canvas` checks every STORY19 pose (mirrored too), 16 phases x 4 modes x 2 facings of every cycle, yaw sweeps and the laugh cycle: 0 outside, smallest margin 0.06 D. `python3 test_cast19.py canvas print` prints a fresh table.

## Files and QA

- `cast19.py` the module; `test_cast19.py` (`story`, `identity`, `canvas`, `robust`, `sheet`, default = all).
- Sheets (PNG through the puppet's own renderer `puppet._raster`): `lineup.png` (height ruler, 12 figures), `expressions.png` (16 face states x 13 faces), `poses.png` (every STORY19 pose), `props.png`, `cycles.png`.

## Known limits

- The wigs and the tied hair are hat-layer shapes: powder and curls read as outlines and a few strokes, not as strands; the 'tied' hair of Harrison reads a little like a cap. The queue hangs beside the neck on the back side of the head.
- The apron and the coats are the standard torso with a drawn skirt: no folds that follow the pose; a strong `lean` (the mock bow) skews the long gown.
- Seated poses (`king_write_seated`) are the puppet's crouch plus a drawn stool: thighs are not foreshortened; frame from the chest up or hide the legs behind the set's table.
- The H4 watch is 0.24 D, so its tick marks are visible only in close-ups (hand to the chest of the frame, D above about 200 px); in a medium shot it reads as a silver disc with hands.
- The H1 clock is a simplified sea clock (frame, gear, two dumbbell balances), not an exact reproduction.
- `astro19_c` bald forehead is the wig set back on a high hairline; there is no shiny highlight on the dome.
- Faces are the standard puppet disc; the "kind, determined" Harrison is carried by brows, the smile mouth and the forehead lines.
- `head_flip` (stage/sprites mirrored head disc check) was not run: no Blender stage in this session.
