# cast3.py: the cast of film 3 (Boston, January 1919) for the v2 puppet

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/cast3/cast3.py`
Python 3 stdlib only, deterministic. Nothing in `v2/puppet`, `v3/cast` or `v3/cast2` is edited. On import, cast3 imports cast2, which imports cast_ext and v2/puppet. It then adds entries to their tables and wraps five puppet helpers on top of their wrappers. Each wrapper falls through to the previous one, so every earlier member draws as before.

```python
import sys
sys.path.insert(0, ".../v3/cast3")
import cast3                 # registers on import (idempotent)
import puppet                # same module object: CAST now also has tommy, foreman, worker1, worker2, kid1, kid2
cast, pose = cast3.STORY3["foreman_laugh"]
f = puppet.figure(cast, pose, "fm")
```

Import `cast3` BEFORE `sprites` / `stage.sprites` when you can. cast_ext's import hook copies the canvases into `sprites.DEFAULT_CANVAS` either way.
Everything in `v2/puppet/API.md`, `v3/cast/API.md` and `v3/cast2/API.md` applies unchanged: pose keys, expressions, `blink`, effects, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`.

## Cast (same head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | height head top to soles (hat top) | look |
|---|---|---|---|
| `tommy` | `boy` (cast2), torso 0.64 x 0.80, legs 0.82 | **2.48 D** (2.66) = 0.78 of the mean adult (3.18) | dark-brown soft flat newsboy cap (puffy top over a short peak, top button), sandy hair, rosy winter cheeks. Oversized grey-blue work jacket hanging open with lapels, a chest pocket with a pencil stub, big patch pockets and a skirt to mid-thigh. **Rolled jacket sleeves** (the sleeve stops past the elbow with a cuff roll). Cream shirt, brown suspenders, brown trousers, **red knitted scarf** with cream stripes (band round the neck plus one fringed end down the chest), soft brown boots |
| `foreman` | `stout`, round torso 1.16 x 1.10, legs 1.30 | 3.27 D (3.58) | chocolate-brown derby (tall crown, wide band with a bow, rolled brim), **thick dark-brown "bushy" walrus moustache**, ruddy cheeks, heavy brows. Brown waistcoat (V neck, five buttons, welt pockets, brass pocket-watch chain swagged to the right pocket) over a white collarless shirt with a stud. **Rolled white shirt sleeves** to above the elbow. Optional cigar (pose key `cigar=True`) |
| `worker1` | `slim` athletic 0.66 x 1.02, legs 1.34 (lanky) | 3.22 D (3.39) | grey flat cap, dark hair, brick-red plaid work shirt with rolled sleeves, denim-blue bib overalls (straps, brass buttons, bib pocket, yellow stitching) |
| `worker2` | `regular` 0.88 x 1.00, legs 1.18 (stocky) | 3.04 D (3.22) | olive flat cap, **full ginger-brown beard** and moustache, slate-blue shirt with rolled sleeves, brown canvas bib overalls |
| `kid1` | `child` (cast_ext) 0.54 x 0.72, legs 0.70 | 2.28 D (2.44) | boy: brown leather aviator cap with cream fleece trim and ear flaps, freckles, mustard winter coat (big collar, double row of buttons, belt, patch), full sleeves |
| `kid2` | `child` 0.52 x 0.72, legs 0.70 | 2.28 D (2.64 with pompom) | girl: orange knit hat with cream stripes and a pompom, two brown plaits with teal ties, lashes, long teal winter coat with cream collar, buttons and hem band |

All six are drawn at scale 1 (no `scale_hint`); the kids are simply shorter than tommy.
Distinctness: no member reuses a film-2 hat or costume. The foreman's derby is dark brown, unlike senior_b's pale bowler with tufts and the black bowler of reference B, and his waistcoat is brown, not yellow. Tommy (grey-blue, red scarf, flat cap) and nico (rust tunic, skullcap) are told apart by colour and silhouette (`lineup.png`).

### New CAST keys (only the members that set them use them)
- `sleeve=dict(color, dark, cuff, len, w, roll)` draws a sleeve over the first `len` (fraction) of each arm, `w` D wide, with a rolled cuff (`roll=True`) or a plain cuff. It follows the rubber-hose curve, and the ink forearm comes out of it. Both arms get one in every layer.
- `beard=dict(color, dark)` draws a full beard on the lower face, clipped to the head fill. The mouth is drawn over it.
- `moustache_style="bushy"` (with `moustache=True`) draws a thick drooping walrus in `colors["moustache"]`, sized by `tache_scale`.
- `cigar_ok` lets the pose key `cigar` work on this member (foreman only).
- `cap_puff` sets how puffy the `flatnews` cap is.
- `coat_len` / `coat_flare` and `jacket_len` / `jacket_flare` set the coat or jacket skirt.
- Hats are `hat="newsboy"` plus `hat_style`: `flatnews`, `derby`, `earflap` or `knit`. Costumes are `workjacket`, `foreman`, `overalls` (plaid when `colors["check"]` is set) and `wintercoat`.

### New pose key
`cigar=True` (foreman) draws a cigar at the mouth corner on the facing side, with an ember and a smoke wisp. It is **only drawn while the mouth is closed and the eyes are not closed**: talk, grin and o mouths drop it.
Limit: `resolve_pose` / `lerp_pose` drop unknown keys, so re-add `cigar` to tweened poses. The stage passes pose dicts through unchanged.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` (from the hand) | orientation |
|---|---|---|---|
| `tin_bucket` | small galvanised tin bucket hung from the hand by its wire bail, two ribs, a dent | bottom centre, 0.47 below | always upright; `hand_for_tip("tin_bucket", (x, feet_y), 90)` stands it on the floor |
| `bucket` | **for the six film-3 members it is the same tin bucket**; for every other member it is still cast_ext's red sand pail | 0.47 | upright |
| `paintbrush` | wide flat brush: wooden handle, tin ferrule, bristles 0.15 wide with brown paint on the tips | bristle edge, 0.46 | follows `angle` (or the forearm) |
| `paintpot` | small tin paint pot on a wire bail, label, brown paint on the rim and running down | bottom centre, 0.38 below | always upright |
| `wrench` | big monkey wrench, wooden grip, adjustable jaws | jaw centre, 0.58 | follows `angle` |

`cast3.bucket_svg(uid, fill=0..1, overflow=0..1, puddle=None, ink, tint)` returns the bucket standing on the ground as an SVG fragment in D units, with its bottom centre at (0, 0) and the bail laid back. `fill > 0` shows a molasses surface at the rim. `overflow` grows molasses runs down the sides and a pool around the foot (pool width `puddle`, default 0.55 x overflow). Use it for the bucket left under the drips and for the overflowing bucket at the end, drawn at the figure's px per D. Molasses colours: `cast3.MOLASSES`, `MOLASSES_L`, `MOLASSES_D`.

## STORY3 (`cast3.STORY3[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast3.STORY3_META[name]`

| name | cast | what | meta |
|---|---|---|---|
| `tommy_bucket_place` | tommy | deep crouch, leaning in, worried, the tin bucket set on the floor beside his front foot | prop_tip_r = the sole line exactly (floor contact) |
| `tommy_listen` | tommy | cupped hand behind the screen-right ear, head tilted that way, worried, sweat, eyes to the side | tank screen-right (or `mirror=True`) |
| `tommy_paint` | tommy | wide stance, brush raised to a wall at screen-right, paint pot hanging from the other hand | `stroke`: arm_r/prop_r of the down-stroke frame |
| `tommy_worried` | tommy | hands wrung at the chest, sweat | |
| `tommy_determined` | tommy | wide stance, fist on hip | |
| `tommy_run` | tommy | sprint frame, leaning, back foot lifted, shocked | alternate by swapping arm and stride signs |
| `foreman_laugh` | foreman | eyes closed (blink 2), mouth wide open, tears, leaning back, hands on belly | animate `t` for the tears |
| `foreman_smug` | foreman | hands on hips, smug, cigar | |
| `foreman_point` | foreman | points out to the side, other hand on the hip, cigar | |
| `foreman_order` | foreman | points up, angry, talking | |
| `foreman_order_paint` | foreman | points up-left at the tank, angry, holds the paintbrush out to the right by the handle | brush tip = prop_tip_r; grab the ferrule 0.30-0.36 D from hand_r along the brush |
| `foreman_kick` | foreman | screen-right boot kicks forward 0.62 D above the floor, arms out for balance, angry | foot_r anchor = the impact point for the bucket |
| `foreman_smug_kick_after` | foreman | smug afterwards, cigar | |
| `foreman_shocked` | foreman | both hands up, shocked, sweat | |
| `foreman_arms_crossed` | foreman | arms crossed, smug, cigar | |
| `workers_laugh` | worker1 | pointing, laughing, tears | |
| `workers_laugh_beard` | worker2 | eyes closed, mouth open, hands on belly | |
| `workers_paint` | worker1 | painting high on the left with the brush | |
| `workers_paint_beard` | worker2 | painting to the right, paint pot in the other hand | |
| `worker_wrench` | worker2 | standing with the wrench | |
| `kids_play` | kid1 | throwing a snowball (arm up), one knee raised, excited | |
| `kids_play_girl` | kid2 | arms out, happy, blush | |
| `kids_run` / `kids_run_girl` | kid1 / kid2 | running, shocked | |

## With the v3 stage

Use it as in `v3/cast2/API.md`. See `stage_test.py`:

```python
import cast3                                   # first
import actors, camrig, render, sprites, stubroom
tommy = actors.Actor("tommy", "tommy"); tommy.build(sprites.DEFAULT_CANVAS["tommy"], sprite_dir, contact=True)
tommy.head_flip = True                          # key light from screen-right
tommy.pose(1, cast3.STORY3["tommy_worried"][1], hands={"l": {"hand": world_xyz, "stretch": 1.3}}, camera=cam)
```

Canvases (feet-relative, added through `cast_ext.CANVAS`, in D):

| member | canvas |
|---|---|
| tommy | (-1.6875, -3.875, 1.6875, 0.125) |
| foreman | (-1.875, -4.6875, 1.875, 0.1875) |
| worker1 | (-1.6875, -4.625, 1.6875, 0.125) |
| worker2 | (-1.75, -4.4375, 1.75, 0.125) |
| kid1 | (-1.5, -3.625, 1.5, 0.125) |
| kid2 | (-1.5, -3.6875, 1.5, 0.1875) |

They hold every arm preset with paintbrush, tin_bucket, wrench and paintpot at yaw +-0.6 (and mirrored), squash 0.8-1.15, crouch, wide legs, all effects and every STORY3 pose, with 0.32-0.39 D head room. Shots outside that range need `sprites.canvas_for(cast, poses)`.
Tommy's arm is 0.62 D. Pass `"stretch": 1.3` for reaches, and pin the `"hand"` when he grabs something.

## Files and QA

- `cast3.py`: the module.
- `test_cast3.py` (same checks as test_cast2): `python3 test_cast3.py` writes `lineup.png` (every member front and 3/4, head D 120 px, heights in D) and `poses.png` (all 24 STORY3 poses). It then runs the canvas check, a head_flip check (24 poses) and v2 `test_puppet.py --quick` on the six names. Subcommands: `lineup`, `poses`, `canvas`, `robust`, `compare`.
- `stage_test.py` writes `stage_test.png`: tommy and foreman as actors on cards in the stub room, key from screen-right, `head_flip` on, Cycles 360x640, 2 threads. The foreman points up-left and holds the brush out; tommy's screen-left hand is pinned to a world point on the brush ferrule (error 0.0 D).
- Results of the last run:
  - robustness: 2,002,922 checks, 0 failed, slowest pose 1.06 ms
  - canvases: ok
  - head_flip: ok, 0 problems
  - lineup / poses rasters: rc 0
  - stage frame: 1.3 s wall

## Known limits

- The stage prints a "clearance < 0" warning for tommy's pinned hand in `stage_test.py`. The target is on the foreman's card, which stands 0.05 D in front of tommy's. The hand still shows (see the png), but in a real shot keep the receiver's card at or in front of the giver's.
- Sleeves are drawn on both arms in the arm's own layer. With `layer="top"` (over the head) the wide sleeve covers the face, so keep raised-to-the-head arms in `front` (as `tommy_listen` does: the hand shows beside the head).
- The jacket and coat skirts are fixed to the torso (as in cast2): in the deep crouch of `tommy_bucket_place` the knees come out under the jacket.
- The tin bucket and the paint pot always hang upright (gravity), whatever the arm angle.
- `cigar` is not carried through `lerp_pose` / `resolve_pose`.
- The beard and cigar are drawn in the head frame (they roll with `head_roll`). The beard clip uses the unrolled head fill, so at large `head_roll` its edge can sit up to 0.01 D off the rim.
