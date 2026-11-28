# cast2.py: the cast of film 2 (Brescia 1769) for the v2 puppet

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/cast2/cast2.py`
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` is edited: on import it adds entries to their tables and wraps three puppet helpers on top of cast_ext's wrappers (each falls through to the previous one, so hero, boss and the cast_ext members draw as before).

```python
import sys
sys.path.insert(0, ".../v3/cast2")
import cast2                 # registers on import (idempotent); imports cast_ext (and so v2/puppet) first
import puppet                # the same module object: puppet.CAST now has nico, padre, baker, woman, old, soldier
cast, pose = cast2.STORY2["padre_laugh"]
f = puppet.figure(cast, pose, "pd")
```

Import `cast2` BEFORE `sprites` / `stage.sprites` when you can; if sprites is already imported the canvases are copied into it at once (cast_ext's import hook handles a later import either way).
Everything in `v2/puppet/API.md` and `v3/cast/API.md` applies unchanged: pose keys, expressions (swap whole drawings), `blink` 0/1/2 (half, closed, half = three frames; change `expr` behind it), effects, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`.

## Cast (all: same head D = 1, flat fill + one lavender crescent, plum ink `#3a2832` thick on the lower right, no neck, rubber-hose ink limbs, ball hands)

| key | build | height head top to soles (hat top) | look |
|---|---|---|---|
| `nico` | `boy` (new: slim presets scaled to arm 0.62), torso 0.64 x 0.80, legs 0.82 | **2.48 D** (2.66) = 0.79 of the mean adult (3.13) | short brown felt skull cap with rolled cuff and stalk, dark-brown hair patch, oversized rust-orange tunic flaring over the hips with a ragged hem, rope belt with knot and frayed ends, ochre patch with cross stitches, ink legs, small soft brown boots. Default face for the story: `expr="determined"` |
| `padre` | stout, round torso 1.06 x 1.12, legs 1.36 | 3.35 D (3.53) | black cassock buttoned with a row of small red buttons down to the hem, white collar tab, fascia with two hanging ends, skirt to just above the ankles, saturno (flat round black brim 1.62 D, low crown, cord), rosy cheeks, grey hair patch, black shoes. CAST key `limb_edge` draws a thin violet-grey edge round his arms and hands so they read over the black cassock |
| `baker` | regular 0.84 x 1.04, legs 1.22 | 3.12 D (3.22) | blue-grey flat cap with a short peak, sage-green shirt, white bib apron (ties, pocket, flour smudge), brown bowl, boots |
| `woman` | slim hourglass 0.58 x 0.92, legs 1.18 | 2.96 D (3.14) | dark-blue dotted headscarf framing the face, knot + tails on the far side, wine bodice, ochre fringed shawl crossed on the chest, long dark-teal skirt |
| `old` | regular 0.74 x 1.00, legs 1.18 | 3.04 D (3.26) | red knitted stocking cap flopping to the back with a tassel, white hair tufts, age lines, long grey-green coat open over a brown waistcoat; uses the `stick` prop |
| `soldier` | slim athletic 0.66 x 1.02, legs 1.30 | 3.18 D (3.44) | black tricorn with white lace and red cockade, blue coat with red facings and turnbacks, white cross belts with brass plate, white breeches, tall black boots, pencil moustache |

New CAST keys (only these members use them): `boots=dict(color, cuff, h, toe, soft)` (boot drawn at each ankle, sole on the sole line), `limb_edge="#rrggbb"`, `tunic_len`, `tunic_flare`, `hem_frac`, `skirt_flare`. Hats: `hat="newsboy"` + `hat_style` in `skullcap`, `saturno`, `flatcap`, `headscarf`, `stocking`, `tricorn` (cast_ext dispatch). Costumes: `tunic`, `cassock`, `baker`, `shawl`, `oldcoat`, `soldier`. Skirts, tunic and coat tails are fixed to the torso: in a deep crouch or kneel they do not fold (the legs come out under them).

## Props (`prop_r` / `prop_l`, `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` (distance from the hand) | orientation |
|---|---|---|---|
| `rod` | iron rod 2.6 D, 0.04 thick, pointed tip, forged ring near the base, rust specks; gripped 0.9 D from the base | the point, 1.70 | follows `angle` (-90 = held vertically, point up: base 0.9 D below the hand) |
| `rod_mid` | the same rod gripped at its middle (carrying) | the point, 1.30 | follows `angle` |
| `hammer` | wooden handle, iron head | head centre, 0.36 | follows `angle` |
| `bell_rope` | hemp rope, always vertical: 3.6 D above the hand, 0.75 D below to a knotted frayed end | the hand (0.0) | ignores `angle`. Put it on the LOWER hand's arm (`prop_l` when `arm_l` is the lower hand) and the other hand at the same x higher up. The top is cut at the sprite canvas edge on purpose: let the set's rope or the frame edge continue it |
| `book` | open book held upright by the lower outer corner of its left page; left page shows a lightning bolt striking a pointed rod, right page text | the second hand's grip point: hand + (0.50, 0) | always upright |
| `lantern` | tin lantern hanging from the hand, warm glass, flame, soft glow | glass centre, 0.30 below | always upright |
| `stick` | walking stick 1.4 D with a crook handle | its foot, 1.40 | follows `angle`; `hand_for_tip("stick", (x, feet_y - 0.035), 92..96)` plants it |

## STORY2 (`cast2.STORY2[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast2.STORY2_META[name]`

| name | cast | what | meta |
|---|---|---|---|
| `nico_determined` | nico | wide stance, fist on hip, determined half-lid | |
| `nico_worried` | nico | hands wrung at the chest, worried, sweat | |
| `nico_hold_rod` | nico | rod upright, base on the floor by his foot | |
| `nico_carry_rod` | nico | striding, rod_mid carried on a slant | |
| `nico_hammer` | nico | kneeling (front knee up, back shin on the roof), left hand holds the upright rod with its base on the roof, right hand raises the hammer | `strike`: arm_r/prop_r of the strike frame (hammer head on the rod); feet point = the roof surface |
| `nico_climb` | nico | near-profile, one hand high, one low, knee raised | hands at x 0.52-0.60 local: put the ladder rungs there |
| `nico_pull_rope` | nico | both hands up on the bell rope, clenched, legs dangling | `lift` 0.32: place the actor 0.32 D above the floor |
| `nico_read` | nico | holding the open book, looking down | |
| `padre_order` | padre | pointing up, angry, low pitch | |
| `padre_point_up` | padre | pointing up, smug | |
| `padre_laugh` | padre | eyes closed (laugh arcs + blink 2), mouth wide open, blush, tears, leaning back, hands on belly | animate `t` for the tears |
| `padre_smug` | padre | both hands on hips, smug half-lid | |
| `padre_arms_crossed` | padre | arms crossed, smug | |
| `padre_smug_hand_rod` | padre | offers the rod upright at arm's length, smug | |
| `padre_ring` | padre | pulling a bell rope beside him | |
| `extras_point_laugh` | baker | pointing up, laughing, tears | |
| `extras_point_laugh_woman` | woman | pointing, hand at the chin, laughing | |
| `extras_point_laugh_old` | old | laughing, leaning on the stick | |
| `extras_ring` | baker | pulling a bell rope | |
| `extras_ring_woman` | woman | pulling a bell rope, worried | |
| `old_stick` | old | standing on the stick | |
| `soldier_guard` | soldier | at ease, hand behind | |
| `soldier_lantern` | soldier | holding the lantern | |

## With the v3 stage (`v3/stage`)

```python
import cast2                                   # first
import actors, camrig, render, sprites, stubroom
nico = actors.Actor("nico", "nico"); nico.build(sprites.DEFAULT_CANVAS["nico"], sprite_dir, contact=True)
nico.head_flip = True                           # key light from screen-right: thick ink side + crescent away from it
cast, pose = cast2.STORY2["nico_pull_rope"]
nico.place(1, (x, y, cast2.STORY2_META["nico_pull_rope"].get("lift", 0.0)))
nico.pose(1, pose, camera=cam)                  # or hands={"r": {"hand": world_xyz, "stretch": 1.3}} to grab a world point
nico.render_sprites(256)
```

Canvases (feet-relative, added to `sprites.DEFAULT_CANVAS` through `cast_ext.CANVAS`): nico (-1.6875, -3.875, 1.6875, 0.125), padre (-1.75, -4.75, 1.75, 0.1875), baker (-1.6875, -4.5, 1.6875, 0.125), woman (-1.625, -4.375, 1.625, 0.25), old (-1.6875, -4.4375, 1.6875, 0.125), soldier (-1.6875, -4.5625, 1.6875, 0.125). They hold every arm preset with hammer / book / lantern at yaw +-0.6 (and mirrored), squash 0.8-1.15, crouch, wide legs, all effects and every STORY2 pose, with 0.35-0.39 D head room. A rod_mid swung round with an arbitrary arm preset, or a rod held high, needs `sprites.canvas_for(cast, poses)`.
Pinning: `nico`'s arm is 0.62 D; pass `"stretch": 1.3` in the hands dict for reaches and pin the `"hand"` (not `"tip"`) when he grabs something without a prop (a bare-hand tip is the edge of the ball).

## Files and QA

- `cast2.py`: the module. `test_cast2.py`: `python3 test_cast2.py` writes `lineup.png` (every member front and 3/4 on one ground line, head D 120 px, head-top and hat-top heights in D) and `poses.png` (every STORY2 pose; the pull-rope pose drawn lifted), then the canvas check, a head_flip check (23 poses) and v2 `test_puppet.py --quick` on the six names. `python3 test_cast2.py compare` writes `compare.jpg` (reference crops A t0010, B t0030 beside the lineup at the same head size).
- `stage_test.py` -> `stage_test.png`: nico and padre as actors in the stub room, key from screen-right, `head_flip` on, Cycles 360x640; padre offers the rod, nico's right hand is pinned to a world point on it (error 0.0 D).
- Results of the last run: robustness 1,998,890 checks, 0 failed, slowest pose 1.0 ms; canvases ok; head_flip ok; all lineup/poses rasters rc 0.

## Known limits

- Kneeling, climbing and dangling legs are explicit foot targets in the story poses (there is no kneel preset); the cassock / skirt / tunic do not follow a kneel, they stay on the torso.
- The bell rope is cut at the sprite canvas top; "feet off the ground" is a placement offset (`STORY2_META[...]["lift"]`), not part of the drawing.
- The torso gradient stays light-left / dark-right with `head_flip` (as for every v2 puppet); only the head disc flips.
- `padre`'s `limb_edge` is a light edge round the arms everywhere, also over light backgrounds (thin, but visible).
