# cast4.py: the cast of film 4 ("the drunk pagoda", old Japan) for the v2 puppet

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/cast4/cast4.py`
Python 3 stdlib only, deterministic. Nothing in `v2/puppet`, `v3/cast`, `v3/cast2` or `v3/cast3` is edited. On import, cast4 imports cast3, which imports cast2, cast_ext and v2/puppet. It then adds entries to their tables and wraps two puppet helpers (`_ink_limb`, `_prop`) on top of cast3's wrappers. Each wrapper falls through to the previous one, so every earlier member draws as before (the new limb drawing only runs for CAST entries with `_cast4=True`).

```python
import sys
sys.path.insert(0, ".../v3/cast4")
import cast4                 # registers on import (idempotent)
import puppet                # same module object: CAST now also has kenta, master, merchant, woman2, farmer
cast, pose = cast4.STORY4["master_laugh"]
f = puppet.figure(cast, pose, "ms")
```

Import `cast4` BEFORE `sprites` / `stage.sprites` when you can (cast_ext's import hook copies the canvases either way).
Everything in `v2/puppet/API.md`, `v3/cast/API.md`, `v3/cast2/API.md` and `v3/cast3/API.md` applies unchanged: pose keys, expressions, `blink`, effects, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`.

## Cast (same head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | height head top to soles (hat top) | look |
|---|---|---|---|
| `kenta` | `boy` (cast2), torso 0.64 x 0.80, legs 0.82 | **2.48 D** (2.72) = 0.80 of the mean adult (3.11) | spiky black hair over the crown, **white twisted hachimaki** with the knot and two tails on the side away from the face. **Indigo short happi** closed left over right, white collar bands, white crest on the chest (a well-frame in a ring, "maru ni igeta"), short wide happi sleeves to mid-arm with a white edge, rust cord belt with a bow, two white bands near the hem. Dark-brown **short trousers** to the knee (bare ink shins), **straw waraji** |
| `master` | `stout`, round torso 1.24 x 1.14, legs 1.30 | 3.31 D (3.62) | **square black cap** (stiff box, flat top, straight flaring sides, stiff band), grey hair at the temples, **thick eyebrows** (brow_th 0.082), ruddy cheeks, no moustache. **Long dark-brown coat** to the ankles, open over a **grey kimono** (grey strip down the middle with a charcoal "y" collar and a black obi), dark lapel bands, small cream crests on the chest, gold tie cords; wide brown coat sleeves; straw sandals with dark thongs |
| `merchant` | `regular` (pear) 0.86 x 1.02, legs 1.18 | 3.06 D (3.24) | shaved crown with a **topknot (chonmage)** lying forward, dark side hair; **grey pinstriped kimono** to the ankles, navy collar, brown obi, **green money pouch (kinchaku)** with a gold coin hanging at the obi; smirk |
| `woman2` | `slim` hourglass 0.58 x 0.92, legs 1.14 | 2.92 D (3.29) | black hair swept up into a **round bun** with a red comb and two coral sticks, side wings over the ears, lashes; **rose kimono with cream blossoms**, red under-collar, wide teal obi with a gold cord, dark rose hem band; long hanging sleeves; red-thonged sandals |
| `farmer` | `slim` athletic 0.66 x 1.00, legs 1.30 | 3.16 D (3.45) | **wide conical straw hat (sugegasa)** with a chin cord; olive work kimono to mid-thigh, cord belt, **rolled (tied-up) sleeves**, dark-grey leggings, waraji |

Distinctness against the reference court characters (ref/a t0010, t0040, t0062, t0080: blue robe with crossed white collar, yellow belt, black striped topknot cap with a gold pin and green bead): no member wears blue robes, a yellow belt or a pin-and-bead cap. The master's cap is a square box, not a round net cap; the merchant's topknot is bare hair. Colours: indigo + white (kenta), brown + grey + black (master), grey stripes + green (merchant), rose + teal (woman2), olive + straw (farmer). `lineup.png` shows them side by side.

### New CAST keys (only `_cast4` members use them)
- `ksleeve=dict(color, dark, cuff, len, w, drop, roll)`: kimono / happi sleeve over the first `len` of each arm, `w` wide, with the sleeve bag hanging under it (`drop` D, times how horizontal the arm is). The bag is the convex hull of the outer two thirds of the sleeve and the same points dropped, so it is continuous for every arm target. `roll=True` = tied-up work sleeve with a rolled cuff (no bag). Drawn on both arms in the arm's own layer.
- `shorts=dict(color, dark, cuff, len, w)`: trouser tube over the first `len` of each leg (cast3's sleeve drawing, used on the legs).
- `sandals=dict(color, dark, strap)`: waraji: flat straw sole on the sole line under the foot stub, two thongs over the foot.
- Hats are `hat="newsboy"` plus `hat_style`: `hachimaki`, `squarecap`, `chonmage`, `hairbun`, `sugegasa`. Costumes: `happi`, `kimono` (keys `kimono_len` = "long" (to `hem_frac` of the leg) or a skirt length in D, `obi_h`, `obi_y`, `obi_knot`, `obi_cord`, `skirt_flare`; colours `pattern` = "stripe" / "flower", `pat`, `pat2`, `pat_op`, `collar`, `under`, `obi`, `obi_d`, `hem`, `pouch`), `mastercoat`.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` (from the hand) | orientation |
|---|---|---|---|
| `mallet` | kizuchi: wooden handle, barrel head across its end with iron hoops | head centre, 0.40 | follows `angle` |
| `chain` | a coil of iron chain hanging from the fist (three loops) | bottom of the coil, 0.40 below | always upright |
| `chain_up` | vertical chain: 3.2 D above the hand, 0.55 D below it to an end ring | the hand (0.0) | ignores `angle`. Like cast2's `bell_rope`: put it on the LOWER hand, the other hand on the same x higher up; the top is cut at the canvas edge on purpose |
| `plank` | sawn plank, 1.6 D, gripped 0.55 D from its back end, end grain on the far end | far end, 1.05 | follows `angle` |
| `plaster_trowel` | kote: wooden grip, gooseneck, flat steel blade with white plaster on its edge | blade end, 0.32 (pass `scale` 1.3 for a close shot, as `master_plaster` does) | follows `angle` |
| `lantern2` | chochin: paper lantern on a short cord, black caps, ribs, red band, warm glow | body centre, 0.36 below | always upright |

`cast4.rubble_svg(uid, width=2.4, height=0.55, ink, tint)`: the pile of broken tower timber (mound, beams, a snapped post, tiles) as an SVG fragment in D units, top of the pile (where the feet go) at (0, 0), foot of the pile on the ground at y = height. Draw it at the figure's px per D.

## STORY4 (`cast4.STORY4[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast4.STORY4_META[name]`

| name | cast | what | meta |
|---|---|---|---|
| `kenta_hammer` | kenta | half crouch, mallet raised over the shoulder (wind-up), other hand forward | `strike`: arm_r/prop_r of the blow frame (mallet head ~0.7 D in front at hip height) |
| `kenta_hang_chain` | kenta | leaning back, both fists on a vertical chain just right of his head (chain x = 0.64 D), pulling, teeth clenched | chain_up on arm_l (the lower hand) |
| `kenta_point_pagoda` | kenta | points up to screen-right, excited, other fist on the hip | |
| `kenta_run_shout` | kenta | sprint frame to screen-right, one hand cupped beside the open mouth, worried, sweat | alternate the stride sign |
| `kenta_determined` | kenta | wide stance, fist on hip | |
| `kenta_worried` | kenta | hands wrung at the chest, sweat | |
| `master_laugh` | master | eyes closed (blink 2), mouth wide open, tears, leaning back, hands on the belly | animate `t` for the tears |
| `master_smug` | master | hands on hips, smug, chin up | |
| `master_arms_crossed` | master | arms crossed, smug | |
| `master_point_tower` | master | points up-left at his tower, smug, other hand on the hip | tower screen-left (or `mirror=True`) |
| `master_pat_shoulder` | master | grinning, screen-right hand out and down onto a shorter person's shoulder, other hand on the hip | pin `hands={"r": {"hand": world, "stretch": 1.3}}` to kenta's `shoulder_l` anchor 0.06 D higher (see stage_test.py) |
| `master_plaster` | master | trowel (scale 1.3) pressed on a wall about 1 D right of the head, other hand on the hip | `stroke`: the lower frame of the stroke |
| `master_shocked` | master | both hands up, ring eyes, "O" mouth, sweat | |
| `master_rubble_look` | master | standing, looking straight up (pitch -1.2), stunned, mouth "o", arms hanging | `lift` 0.45: the pile height; poses.png draws it on `rubble_svg()` |
| `town_laugh_point` (+ `_woman2`, `_farmer`) | merchant / woman2 / farmer | pointing and laughing, tears (woman2 mirrored: points screen-right) | |
| `town_mock_shout` (+ `_woman2`, `_farmer`) | ... | both hands cupped beside the open mouth, smug brows (woman2 mirrored) | |
| `town_run` (+ `_woman2`, `_farmer`) | ... | running to screen-right, arms up, shocked, sweat | |
| `town_shelter` (+ `_woman2`, `_farmer`) | ... | hunched, arms over the head (layer top), half-shut eyes; the farmer crouches deep, the long kimonos only bend the knees a little | |

26 poses (6 kenta, 8 master, 4 x 3 townspeople).

## With the v3 stage

Use it as in `v3/cast3/API.md`. See `stage_test.py`:

```python
import cast4                                   # first
import actors, camrig, render, sprites, stubroom
kenta = actors.Actor("kenta", "kenta"); kenta.build(sprites.DEFAULT_CANVAS["kenta"], sprite_dir, contact=True)
kenta.head_flip = True                          # key light from screen-right
kp, _ = kenta.pose(1, cast4.STORY4["kenta_worried"][1], camera=cam)
sh = sprites.puppet.figure("kenta", kp, "q")["anchors"]["shoulder_l"]
target = actors.local_to_world(kenta, (sh[0], sh[1] - 0.06), 1)
master.pose(1, cast4.STORY4["master_pat_shoulder"][1], hands={"r": {"hand": tuple(target), "stretch": 1.3}}, camera=cam)
```

Canvases (feet-relative, added through `cast_ext.CANVAS`, in D):

| member | canvas |
|---|---|
| kenta | (-1.9375, -3.9375, 1.9375, 0.25) |
| master | (-2.1875, -4.875, 2.1875, 0.1875) |
| merchant | (-2.125, -4.625, 2.125, 0.1875) |
| woman2 | (-2.0625, -4.5625, 2.0625, 0.25) |
| farmer | (-2.0625, -4.8125, 2.0625, 0.125) |

They hold every arm preset with mallet, chain, plank, plaster_trowel and lantern2 at yaw +-0.6 (and mirrored), squash 0.8-1.15, crouch, wide legs, all effects and every STORY4 pose, with 0.35-0.40 D head room. They are wider than cast3's because of the plank (1.05 D in front of the hand). `chain_up` is cut at the canvas top on purpose. Shots outside that range need `sprites.canvas_for(cast, poses)`.
Kenta's arm is 0.62 D: pass `"stretch": 1.3` for reaches.

## Files and QA

- `cast4.py`: the module.
- `test_cast4.py` (same checks as test_cast3): `python3 test_cast4.py` writes `lineup.png` (every member front and 3/4, head D 120 px, heights in D) and `poses.png` (all 26 STORY4 poses, the rubble pose on `rubble_svg`). It then runs the canvas check, a head_flip check (26 poses) and v2 `test_puppet.py --quick` on the five names. Subcommands: `lineup`, `poses`, `canvas`, `robust`, `compare` (compare.jpg: ref A t0010 / t0040 crops beside the lineup).
- `stage_test.py` writes `stage_test.png`: kenta and the master as actors on cards in the stub room, key from screen-right, `head_flip` on, Cycles 360x640, 2 threads. The master's screen-right hand is pinned to a world point on kenta's shoulder (error 0.0 D, clearance +0.24 D: the master's card stands 0.10 D in front of kenta's, so no warning).
- Results of the last run (`run_all.log`):
  - robustness: 1,675,943 checks, 0 failed, slowest pose 1.01 ms
  - canvases: ok (head room 0.35-0.40 D)
  - head_flip: ok, 0 problems in 26 poses
  - lineup / poses rasters: rc 0
  - stage frame: 1.9 s wall, pinned hand error 0.0 D

## Known limits

- Kimono, happi and coat skirts are fixed to the torso (as in cast2/cast3): in a run or a deep crouch the legs come out under a long skirt, and a deep crouch would push a long hem below the soles; that is why `town_shelter` crouches only the farmer.
- The sleeve bag hangs "down" in the figure frame; with a big `lean` it hangs along the lean, not along true gravity.
- Kimono sleeves are drawn in the arm's layer: an arm in `layer="top"` (shelter) puts the sleeve over the face, which is intended there; for hands near the mouth keep `front` and put the hand outside the head disc, as `kenta_run_shout` / `town_mock_shout` do.
- The master's square cap is drawn as a front view whose side edge slides with yaw; at |yaw| near 1 it does not turn into a true side view.
- The money pouch is part of the merchant's costume (not a prop): it cannot be handed over.
