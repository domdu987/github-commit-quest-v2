# cast15.py: the cast of film 15 ("ไอ้ปลาดิ้น", Dick Fosbury and the flop; 1963 high-school track, 1968 Olympic stadium) for the v2 puppet

File: `film/v3/cast15/cast15.py`. Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast15 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to their tables and wraps `_norm`, `_ink_limb`, `_prop` and `figure` on top of cast10's wrappers. Everything falls through, so every earlier member draws exactly as before (`python3 test_cast15.py robust` checks hero, boss, all STORY poses and six earlier members byte-identical to cast10 alone).

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast15")
import cast15                  # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                  # same module object: CAST now also has the 19 keys below
p = cast15.pose_for("flop", "dick")                        # preset built for that member, travelling screen-RIGHT
p = cast15.pose_for("flop", "dick", facing=-1)             # travelling screen-LEFT (mirror=True, as cast6.cycle(facing=-1))
f = puppet.figure("dick", p, "f")                          # f["anchors"]["bar"], ["apex"], ["head"], ["hip"] ...
cast, pose = cast15.STORY15["dick_flop"]                   # ready-made (cast, pose) pairs, also merged into puppet.STORY
p = cast15.run_curved("dick", frame / 16.0, facing=1)      # curved approach, one frame of the run cycle
p = cast15.coach_clumsy_run(frame / 16.0)                  # the coach's clumsy run
p = dict(cast15.pose_for("coach_laugh", "coach"), bob=cast15.laugh_bob(frame))   # belly bounce, 3 Hz, 0.06 D
```
`blink_at`, `talk_mouth`, `cycle`, `NOD` are re-exported from cast6. Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies: pose keys, the expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `ink`, `rim`.

## Why there are new pose keys

The puppet torso is rigid and its keys are clamped (`lean` +-75, `head_roll` +-75, `head_dx/dy` +-0.8). The FLOP (an arched bridge) and the STRADDLE (flat, face down) need the torso at 90..135 degrees, so cast15 members accept `body_lean`, `roll2`, `hdx2`, `hdy2` with wide ranges. The flop is built as a bridge from the rigid torso: head low at one end, the hips at the apex, thighs and shins hanging down on the other side, head tipped back with the face up.

## Cast (head D = 1)

| key | build | head top to soles | look |
|---|---|---|---|
| `dick` | slim, torso 0.56 x 1.04, **legs 1.86** | **3.76** (tallest; hair tufts 4.05) | lanky, long thin limbs, **big ears**, short **tousled brown hair** (spikes stick out of the head), friendly face. Costume **school**: maroon vest with gold neck binding, gold chest band and gold hem, white shorts, white socks with maroon/gold stripes, off-white canvas sneakers |
| `dick_olympic` | same body | 3.76 | costume **olympic**: white vest with **straight red and blue chest bands** and solid **navy side bands** (readable on pale foam), navy shorts, white socks, **spikes** (white spiked shoes). Pose key `medal=1` hangs the gold medal on a red/white/blue ribbon |
| `coach` | stout, torso 1.52 x 1.14, legs 0.98 | 2.99 (cap 3.28) | veteran: stocky **belly**, **grey crew cut** at the temples, **big square jaw**, small ears, maroon **cap** (no letters), maroon **windbreaker** (gold side stripes, zip, collar) with **lanyards: whistle and stopwatch** on the belly, grey trousers, black shoes. Prop `clipboard` |
| `coach_stands` | same body | 2.99 (hat, pennant 3.57) | costume **stands**: loud teal tourist shirt with hibiscus blobs, cream trousers, floppy cream hat with a red band and a **red/white striped pennant** on a stick (stripes only, no flag, no letters) |
| `boy1` | slim, legs 1.34 | 3.18 | navy-and-white vest (not Dick's maroon), chestnut crew cut, wide grin |
| `boy2` | slim, legs 1.46 | 3.32 | blue-and-white vest, big black curls, brown skin |
| `boy3` | slim, legs 1.24 | 3.04 | green-and-white vest, blond quiff, ruddy skin |
| `rival1` | slim, legs 1.62 | 3.50 | plain red kit, black crew cut, tan skin, spikes |
| `rival2` | slim, legs 1.70 | 3.60 | plain green kit, ginger quiff, spikes |
| `rival3` | slim, legs 1.56 | 3.42 | plain gold kit with black shorts, curls, dark skin, spikes |
| `official1` | regular, legs 1.30 | 3.19 | 1968 official: navy blazer, white shirt, red tie, grey crew cut, grey moustache, grey trousers |
| `official2` | slim, legs 1.40 | 3.26 | maroon blazer, blue tie, dark quiff, dark trousers |
| `photographer` | regular | 2.97 | 1960s press man: flat cap, shirt sleeves rolled, loosened tie, moustache; prop `presscam` |
| `crowd1` .. `crowd6` | regular / slim | 2.95, 2.91, 2.95, 2.91, 2.58 (small), 2.99 | near-stand spectators: navy cap + striped shirt; woman with a bouffant and a pink top; yellow-vest teen; fedora + brown jacket + moustache; small ginger kid with spiky hair; woman in a red polka-dot kerchief and purple top. Use with the `sit_*` presets |

For scale: cast10's admiral is 3.43, sailor_a 3.20. Hair, hats, ears, jaw, socks and shoes are part of the silhouette on purpose (they read at phone size, see `sheet_phone.jpg`). **Skin tone** (CAST `skin15`: fair / tan / brown / dark / ruddy) recolours the head disc, the neck and the chest opening of the costume; the puppet's head is otherwise always white.

Costumes (`CE.COSTUMES`): `vest15`, `jacket15`, `aloha15`, `blazer15`, `shirt15`. Hats / hair (`CE.HATS`): `hair15` (CAST `hair_style15` = tousle / crew / curly / quiff / bouffant / bald), `cap15`, `tourist15`. Existing `fedora` and `kerchief` are reused. Legs: CAST `shoe15` (`kind` sneaker / spike / dress, `sock`, `sock_stripe`, `sock_len`). Ears: CAST `ears15` (size). Jaw: CAST `jaw15`. These are drawn behind the head disc, in the head frame, and roll with it.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `body_lean` | -200..200 deg (None: `lean`) | torso rotation about the head centre, unclamped. +90 = torso horizontal, hips to the LEFT of the head (head leads to the right). +130 = the flop bridge. -90 mirrors it |
| `roll2` | -200..200 (None: `head_roll`) | head roll, unclamped. In the flop +86 with `yaw` -0.9 turns the face up (belly up); in the straddle +88 with `yaw` +0.9 turns it face down |
| `hdx2`, `hdy2` | -4..4 | torso offset from the head, unclamped (the base keys stop at 0.8) |
| `sawdust` | 0..1 (0) | wood chips on hair / cap / hat and scattered on the costume |
| `buried`, `buried_y`, `buried_w`, `buried_x` | 0/1 (0), D (0.62), D (1.5), D (feet x) | draws a **sawdust mound** over everything below `buried_y` (head frame y of its top, 0.62 = the chin), half width `buried_w`, base at the soles. Arms with `layer="top"` and the head stay above it |
| `medal` | 0/1 (0) | gold medal on a red-white-blue ribbon on the chest (works with every cast15 costume) |
| `flash` | 0..1 (0) | the press camera's flash: star burst at the reflector (`anchors["flash_r"/"flash_l"]`) and a white-hot bulb; animate 1 -> 0 over about 4 frames |
| `thumb_r`, `thumb_l`, `thumb_angle` | 0/1, deg (-90) | a thumb standing up on the hand of that limb (limb r = the unflipped screen-right one; follows `mirror`) |
| `bob` | -0.5..0.5 D (0) | lifts the whole drawing by `bob` D (feet_y is NOT changed, so the card hops when placed by feet). Use `laugh_bob(frame, fps=30, hz=3, amp=0.06)` |
| `bend15`, `bend_y` | -90..90 deg (0), 0.3..0.9 (0.6) | splits the torso in two: the lower segment (hips, legs) rotates by `bend15` about the joint at `bend_y` of the torso length (negative = bends the way the flop arches, with the head on the right). Legs hang from the bent hips (the solver is wrapped); a round cap hides the wedge. Use `J(..., bend=, bend_y=)` so the foot targets use the bent hips |
| `hat_off` | 0..1 (0) | cap flying off: the `cap15` hat lifted up and back and tumbling (coach_clumsy_flop) |
| `t` | float | passed through |

New anchors on every cast15 figure: **`apex`** (the hip joint, the highest point of the flop arch), **`bar`** (the underside of the lower back, where a crossbar passes under a flop; see below), plus the usual `head`, `hip`, `chest`, `hand_*`, `foot_*`, `feet`.

### Where the bar goes in the flop (card coordinates, D, head centre = origin, y down)

`flop` (dick; rival1 / boy2 within 0.02; facing right; head centre at (0, 0), y down, D): the torso is **two segments**. The upper one (chest, shoulders) is fixed to the head (it overlaps the head, no gap, `body_lean` 165 + `hdy2` 0.25); the lower one (lower back, hips, legs) is rotated about a joint by `bend15` = -70 degrees (`bend_y` 0.45 = the joint's place along the torso), and a round cap in the costume colour fills the outside of the bend, so the back is a visible round arch.
- `apex` = the top of the round back: **(-0.26, -1.29)** (1.29 D above the head centre)
- **`bar` = (-0.45, -0.69)**: the horizontal line y = `anchors["bar"][1]` passes **0.13 D below the underside of the back** (the inner corner of the bend), so a gap of air shows between the back and the bar line; x is where the back is lowest-clearance. The head centre hangs 0.69 D below the bar, the feet (`foot_l` (-1.88, 0.17)) about 0.9 D below it.
- `hip` (the hip joint after the bend) = (-0.79, -1.10); knees reach x = -1.9, so the arch is about 2 D wide head to feet (about 1.7 D head to knees).
Other stages (dick): `flop_head` apex (-0.74, -1.00) bar (-0.84, -0.40) feet y 0.64; `flop_back` apex (-0.46, -1.26) bar (-0.62, -0.66); `flop_flick` apex (-0.62, -1.12) bar (-0.74, -0.52) feet y -2.79 (an L). `coach_clumsy_flop` apex (-0.78, -1.49). For a left-facing flop (`facing=-1`) x is negated; anchors come back already mirrored. Read the anchors, do not hard-code them (they scale a little with torso length; the bend cap radius is the torso half-width).

## Pose presets (`cast15.POSE_NAMES`; `pose_for(name, cast, facing=1, **overrides)`)

All are authored for a figure travelling or facing screen-RIGHT (`facing=-1` toggles `mirror`). Limbs are placed in polar form relative to the shoulders / hips of the member passed in, so one preset fits every member. Arm tweening: use plain numbers, never rely on lerp_pose; `cast15.J(cast, ...)` builds poses the same way (`arm_r=(angle, reach, bend[, extra])`, `leg_r=(angle, reach, knee)`; angle 0 = right, 90 = down, -90 = up).

| preset | for | what |
|---|---|---|
| `rock_a`, `rock_b` | jumpers | rocking on the toes at the mark (alternate every ~0.25 s), eyes on the bar |
| (cycle) `run_curved(cast, phase, facing)` | jumpers | curved run: cast6 'run' cycle leaning into the curve (about 18 deg), 16 frames per cycle |
| `plant` | jumpers | last stride, planted forward foot, leaning away from the bar |
| `takeoff` | jumpers | drive leg straight, **knee lifted**, arms thrown up |
| `flop_rise` | jumpers | leaving the ground, turning the back to the bar (lean +48, yaw -0.1) |
| `flop_head` | jumpers | head and shoulders already past the bar (hanging low), hips rising (`bend15` -32), legs trailing nearly straight |
| `flop_back` | jumpers | the arch almost complete (`bend15` -55), knees starting to bend |
| `flop` | jumpers | **THE FLOP**: a round upside-down U, belly up: two-segment torso (`body_lean` 165 + `bend15` -70), head overlapping the shoulder end and looking toward the feet, thighs down and out with the shins hanging (knees bent), arms down along the body. Built by `cast15._arch(...)` + polar legs |
| `flop_flick` | jumpers | legs kicked up and over: jack-knife into an L (legs near vertical above the hips) |
| `land_back` | jumpers | on the back, **knees up**, arms flung out up and down, torso slightly raised (a small bounce), startled (`sawdust` 0.5) |
| `lie_back` | jumpers | lying flat on the back |
| `sit_up` | jumpers | seated, torso upright, one leg flat out in front and the other knee up, sheepish (worried eyes, small smile, sweat), hand scratching the back of his head, `sawdust=1` |
| `straddle_a`, `straddle_b` | jumpers | **STRADDLE roll**: belly DOWN: body horizontal with the head dipped, **face toward the ground**, both arms reaching straight down, one leg kicked high up (a: right leg, b: left leg), the other trailing low |
| `knock` | jumpers | bar knocked: tumbling flail, arms and legs wide, shocked "O" |
| `lie_hands_face` | jumpers | lying on the mat, hands on the face, sad |
| `cheer` | jumpers, boys | arms-up V, excited |
| `podium` | `dick_olympic` | podium wave with the medal (`medal=1`) |
| `thumb`, `sit_thumb` | jumpers | thumbs up (standing / sitting on the foam smiling) |
| `stand` | all | relaxed standing |
| `laugh`, `point_laugh`, `point`, `gape`, `jaw_drop` | boys, crowd, rivals | laugh with hand on belly (use `bob`), point-and-laugh, point, gape (shocked O, shrug, sweat), jaw drop (open mouth, `("open", 0.30, 0.22)`) |
| `sit_cross`, `sit_laugh`, `sit_cheer`, `sit_gape`, `sit_point` | boys, crowd | seated on a bench or bleacher (hips at `anchors["hip"]`; legs bent forward). `sit_cross` = arms crossed, unimpressed |
| `coach_laugh` | coach | belly laugh, head back, hands on belly, tears (drive `bob` ~3 Hz, 0.06 D) |
| `coach_point` | coach | pointing, hand on hip, smug |
| `coach_neck` | coach | both hands at his own neck (broken-neck mime), eyes wide, teeth clenched |
| `coach_wag_a`, `coach_wag_b` | coach | raised index finger, alternate every 3 frames for the wag |
| `coach_jab` | coach | jabbing his own chest with a finger, smug |
| `coach_shout` | coach, coach_stands | shouting: angry, arm pointing; **lip-sync**: set `mouth = talk_mouth(g, 1.0)` inside the quote windows (17.80-23.55 s, 40.38-42.25 s), `"flat"` outside (the preset holds `talk_b`) |
| `coach_jaw` | coach, coach_stands | jaw dropped (held open mouth) |
| `coach_sigh` | coach | sigh: head down, shoulders low, hand to chin, sad |
| (cycle) `coach_clumsy_run(phase, cast, facing)` | coach | clumsy run: heavy forward lean, flapping arms, wobbling head |
| `coach_clumsy_flop` | coach | sagging backwards flop: belly up, hips drooping (`bend15` -34), head dropped, arms thrown wide over the body, one leg kicking up, the **cap flying off** (`hat_off` 1) |
| `coach_buried` | coach | in the sawdust: `buried=1` mound, `sawdust=1`, weak thumbs-up (`thumb_r`), worried small smile |
| `clip` | coach | holding the clipboard |
| `photog_ready` | photographer | crouched, press camera at the eye |
| `photog_flash` | photographer | the same with `flash=1` (burst) |
| `walk_dejected` | all | head down, shoulders slumped, arms hanging, mid-stride (cast6 walk phase 0.25). Animated: `walk_dejected(cast, phase, facing)` (28 frames per cycle) |
| `sit_read` | boys, crowd | **newspaper reader (shot 14)**: seated, holds the open `paper15` wide in both hands at chest height, grinning |
| `official_stand`, `official_raise`, `official_point` | officials | hands behind the back; arms up raising the crossbar; pointing |

`cast15.STORY15[name] = (cast, pose)` (also merged into `puppet.STORY`) gives 47 ready-made pairs such as `dick_flop`, `dick_straddle`, `coach_laugh`, `stands_shout`, `photographer_flash`, `boy1_laugh`, `rival2_flop`, `official1_raise`. `STORY15_META[name]["note"]`, and `["lipsync"] = True` on the two shout poses.

Props: `paper15` (`prop_r={"type": "paper15", "angle": 0, "scale": 1.2}`: an open newspaper 1.3 D wide x 0.95 D, no letters: grey headline bars, a big grey halftone photo of an arched jumper over a bar, column bars; the right hand holds its right edge and the page extends to the left hand at x - 1.3 x scale; anchor `paper_r`), `clipboard` (`prop_r={"type": "clipboard", "angle": 0}`, anchor `board_r`), `presscam` (`{"type": "presscam", "angle": -4, "scale": 1.3}`, anchors `flash_r`, `lens_r`).

## Canvases (feet-relative, D)

Standing and seated poses: `cast15.CANVAS15[name]` (registered into `sprites.DEFAULT_CANVAS` through `cast_ext.CANVAS`), +-2.125 wide, 0.75 D of head room over the figure (dick (-2.125, -4.5, 2.125, 0.125)). **Lying, bridge, straddle, airborne and buried poses:** use `cast15.CANVAS15_WIDE = (-4.25, -4.5, 4.25, 4.0)` and place the card by `anchors["head"]` / `["apex"]` / `["bar"]`, not by the soles (`feet_y` is just the lowest sole there). `python3 test_cast15.py canvas` runs every member x every preset x both facings x 16 run phases against the wide canvas: 0 outside.

## Gotchas

- **Head disc and hair.** The disc never rotates (its shade crescent stays lower-right); only the face, hair and hat roll. In the flop the head hangs at the end of the torso and the hair tufts point away from the body. `hair15` tufts and the pennant stick out of the disc, which is why the bbox is taller than head + 3.76.
- **Face direction in lying poses.** Face up (flop, lie_back, land_back) is `yaw -0.9` + `roll2 +86..88`. Face down (straddle) is `yaw +0.9` + `roll2 +88`. Do not change one without the other.
- **Straddle vs flop at phone size**: the flop is a diagonal bridge (head low at one end, legs hanging on the other, hips highest); the straddle is a flat horizontal bar with a leg sticking up. `sheet.jpg` section 2 puts them side by side, `sheet_phone.jpg` at head D = 34 px. The puppet is front-drawn, so "belly down" is carried by the face and the hanging arms, not by the costume.
- **`bob` and `laugh_bob`** move the drawing, not `feet_y`. A card placed by feet therefore hops by `bob` D. 3 Hz at 30 fps is a period of 10 frames.
- **Skin and `P.HEAD_FILL`.** `figure()` swaps `P.HEAD_FILL` / `P.HEAD_SHADE` during the call and restores them; do not call cast15 figures from threads sharing the module.
- **Mirror.** `facing=-1` = `mirror=True`. Anchors and bbox come back mirrored with r/l swapped. `thumb_r` follows the r limb, so with `mirror` the thumb shows on the left hand.
- `buried=1` draws the mound at the soles' level: `buried_y` is a head-frame y (0.62 = just under the chin), so on a standing figure the mound is as tall as the body (about 3 D). For a smaller heap lower the card into the set's own pit instead and use only `sawdust`.
- `sheepish` is not an expression: `sit_up` uses `worried` + `mouth="smile"` + sweat.
- Fixed picture limits (FACTS.md): no letters or numbers, no national flags. The olympic vest has red and blue chest bands, the pennant and ribbon are stripes only.
- No `reader` member: the newspaper-reader insert (shot 14) is `boy1` (or any crowd member) with `prop_r="newspaper"` (cast_ext) held up. The officials hold no flag (the plan's "one with a flag" is left to the set).
- `resolve_pose` / `lerp_pose` drop all cast15 keys (`body_lean`, `roll2`, `hdx2`, `hdy2`, `sawdust`, `buried*`, `medal`, `flash`, `thumb_*`, `bob`). For tweens interpolate the numbers yourself (all presets use explicit hand / foot targets, so a per-key lerp of the arm and leg dicts works).

## Files and QA

- `cast15.py` is the module, `test_cast15.py` the QA, `flop_strip.jpg` the four flop stages side by side (dick above, rival1 below, red line = bar anchor), `sheet.jpg` the labelled sheet (heights front + 3/4, flop sequence above straddle with the bar line, every preset with the `bar` (red) and `apex` (green) anchors, cycles, props, six face states per member) and `sheet_phone.jpg` the phone-scale sheet (head D = 34 px).
- `python3 test_cast15.py` = sheet + canvas + robust; `sheet`, `canvas`, `robust` separately. Robust: 2380 garbage-key / determinism checks (0 failed) plus the cast10 byte-identity regression (identical).
