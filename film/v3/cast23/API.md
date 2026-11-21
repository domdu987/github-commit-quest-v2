# cast23.py: the cast of film 23 ("ไอ้กองทัพลูกโป่ง", the Ghost Army, Normandy 1944 / the Rhine 1945)

File: `PROJ/v3/cast23/cast23.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only (Pillow only for the optional gap check), deterministic.
Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. cast23 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to their tables and wraps `_norm`, `_face`, `_moustache`, `_hand`, `_prop` and `figure` on top of cast10's wrappers; each falls through, so every earlier member draws exactly as before.
Comic and bloodless: **nobody holds a weapon**. Flat fills + plum ink, one torso shape, constant-width ink limbs, no neck, period colours (olive drab, khaki, field grey, navy, maroon; no pure black).

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast23")
import cast23                      # registers on import (idempotent); import BEFORE sprites / stage.sprites
import puppet                      # same module object: CAST now also has the 12 members below
cast, pose = cast23.STORY23["gi_paint_star"]
f = puppet.figure(cast, pose, "f")                                   # f["anchors"]["feet"] / ["ground"] = the ground point
p = dict(cast23.STORY23["major_point_quote"][1], mouth=cast23.talk_mouth(g, 1.0), blink=cast23.blink_at(g, 90))   # lip-sync
p = cast23.ride_frame("fr_beret", g / 14.0)                          # bicycle drawn inside the sprite
p = cast23.pump_frame("gi_pump", g / 20.0)                           # pump drawn inside the sprite
info = cast23.sprite("fr_beret", p, "/abs/out.png", 128, canvas=cast23.CANVAS23_WIDE["fr_beret"])   # + out.png.json with the ground pixel
```

Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged (pose keys, the 21 expressions incl. cast10 `squint`, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `ink`, `rim`, cast3 `cigar=True`, cast6 `cycle` / `talk_mouth` / `blink_at` / `NOD`, re-exported here). **`resolve_pose` / `lerp_pose` drop the cast23 keys below: re-add them to tweened poses.**

## Cast (head D = 1; head top to soles, hat in brackets)

| key | build | height | look |
|---|---|---|---|
| `gi_painter` | slim, legs 1.30 | 3.16 (3.32) | ginger hair, freckles, **overseas cap** worn jaunty, rolled sleeves, **white paint on both hands** (`paint_hands23`) |
| `gi_sound` | regular pear, legs 1.10 | 2.92 (2.99) | bare dark curly head with **headphones** (`phones23`), pencil moustache, round |
| `gi_radio` | regular, legs 1.20 | 3.08 (3.31) | **M1 helmet** with net + dangling chin straps, heavy brows, **radio pack + whip antenna on the back** (`pack23`) |
| `gi_pump` | stout pear, legs 1.04 | 2.85 (3.07) | M1 helmet, bushy brown moustache, ruddy, rolled sleeves |
| `gi_designer` | slim, legs 1.28 | 3.16 (3.32) | **round glasses**, neat black hair, overseas cap, smirk |
| `gi_smile` | regular, legs 1.24 | 3.11 (3.33) | big blond lad, M1 helmet, wide eyes: the **dry smiler** of "แข็งแรงมาก" |
| `gi_driver` | slim, legs 1.18 | 3.00 (3.23) | wiry, M1 helmet, thin moustache, age lines, frown: **the Major's driver** |
| `major` | stout, legs 1.30 | 3.43 (3.68) | **khaki officer tunic + brown Sam Browne belt** (cross strap), ribbon bar, peaked cap (olive crown, brown leather peak, gold eagle), **huge ginger-brown handlebar moustache**, cigar, pink-khaki breeches, tall brown boots |
| `fr_beret` | regular | 2.96 (3.14) | navy **beret**, **striped marinière** + red neckerchief, handlebar moustache, blue trousers; rides the **green bike with basket + baguette** |
| `fr_cap` | slim | 3.04 (3.16) | brown **flat cap**, green-grey **waistcoat** over a cream shirt with rolled sleeves; rides the **maroon bike** |
| `ger_tall` | slim, legs 1.36 | 3.26 (3.45) | **grey M43 field cap** (eagle, cockade, short peak), field-grey tunic (dark green collar, pale tabs, scalloped pockets), jackboots, blond |
| `ger_round` | stout | 2.91 (3.09) | same uniform, round, walrus moustache, the sausage eater |

`cast23.GI23` = the 7 GI keys, `cast23.NEW23` = all 12. Every GI has a different face (hair colour, brows, moustache, glasses, eye size, build, hat).

## Pose keys (new; read at draw time)

| key | values | effect |
|---|---|---|
| `hat23` | `"m1"`, `"overseas"`, `"bare"`, `"m43"` | override the member's hat for this drawing (e.g. a GI without helmet) |
| `phones23` | bool | headphones on / off (default: `gi_sound` only) |
| `paint_hands23` | bool | white paint on the hands (default: `gi_painter`) |
| `red23` | 0 / 1 | **red angry face**: swaps the whole face fill (no tween; swap on a blink) |
| `puff23` | 0 / 1 / 2 | puffed cheeks (two drawings) + pursed lips (balloon blowing) |
| `daze23` + `t` | bool | three stars circling above the head (fallen cyclist); `t` turns them |
| `bigsweat23` | bool | one big comic sweat drop at the temple (S03, the dry smile) |
| `spin23` | float | rotation of a held `record23`'s sheen/label |
| `reach23` | 1 .. 1.6 | rubber-hose arm length for this drawing (used by `lift_pose`) |
| `bike23` | `dict(phase, color="green"/"maroon", basket, baguette, state="ride"/"brake"/"fallen")` | the bicycle drawn into the sprite; ground point = wheel contact (see `ride_frame`, `fall_pose`) |
| `pump23` | phase float | the hand pump in front of the figure (see `pump_frame`) |
| `crate23` | `"carry"` / `"seat"` | a wooden crate carried between the hands (hands redrawn over it) / sat on (crate bottom = ground point) |
| `balloon23` | `dict(size 0..1, color "#hex", tilt, pop 0/1)` | a balloon at the mouth, neck at anchor `balloon_neck` |
| `ground23` | `"seat"` | sitting on the ground: the ground point is the lowest body point |
| `t` | float | animates steam, tears, daze, cigar smoke |

CAST keys: costume `gi23` (`pack23`), `major23`, `feld23`, `mariniere23` (colors scarf); hat_style `gi23` (+ `hat23`, `phones23`, `helmet_colors`, `cap_colors`, `net`); `moustache_style="major23"`; `paint_hands23`. The Major's cap is cast10 `peaked10` recoloured; the waistcoat is cast3 `foreman`, the marinière cast7 `stripe7`, the beret cast7 `beret7`, the flat cap cast3 `flatnews`, binoculars cast10.

## Props (`prop_r` / `prop_l`; `PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | anchor (`_r` / `_l`) |
|---|---|---|
| `brush23` | house brush, white-tipped bristles, a white drip | `brush` (bristle tip) |
| `pot23` | paint tin hanging from its bail, white paint, always upright | `pot_bottom` |
| `record23` | 16-inch transcription disc face-on (r 0.55), red label; centre 0.5 D from the hand along `angle` | `record` (centre) |
| `handset23` | field telephone handset + coiled cord | `earpiece` |
| `clipboard23` | clipboard with a pencil sketch of a tank | `clipboard` (centre) |
| `stencil23` | card stencil with a shield cut-out | `stencil` |
| `cigar23` | cigar between the fingers, smoke wisp | `cigar` (ember) |
| `sausage23` | a sausage | `sausage` |
| `chalk23` | chalk stick | `chalk` (tip) |
| `pin23` | big red-headed pin with a glint | `pin` (point) |
| `rag23` | polishing rag | - |
| `oar23` | canoe paddle (1.7 D) | `blade`, `grip_far` (second hand) |
| `binoculars` | cast10 (front view) | `binoc`, `grip_far` |

Standalone SVG fragments for the set (D units): `balloon_svg(uid, size, color, angle, pop)` -> (svg, bbox) (the balloon pile, the last balloon popping), `record_svg(uid, spin)` (the turntable record on the sound truck), `sausage_svg(uid, angle)` (the dropped sausage falling).

## Cycles and builders (all return plain pose dicts; `facing=-1` mirrors)

| function | frames per cycle | notes |
|---|---|---|
| `cycle(cast, g / N, "walk"/"run"/"sneak"/"march", facing, base, arms)` | walk 28, run 16, sneak 32, march 24 | cast6 |
| `pump_frame(cast, g / 20, facing)` | 20 per stroke | handle up/down, body crouches on the push, air puff at the hose end; anchors `pump_handle`, `hose_end` (1.8 D toward the facing side, on the ground: put the tank valve there). Canvas: `CANVAS23_WIDE` |
| `paint_frame(cast, g / 18, facing)` | 18 | brush sweeps; `brush_r` on the surface |
| `ride_frame(cast, g / 14, facing, expr, mouth, color, state, basket, look)` | 14 per crank turn | **wheels spin, cranks turn, feet on pedals, hands on grips**; `state="brake"`: frozen cranks, lean back; `look` 0..1 turns the head to camera. Anchors `bike_rear`, `bike_front`, `basket`, `grip`. Canvas: `CANVAS23_WIDE` |
| `fall_pose(cast, g / 30, facing)` | 30 (daze stars) | sitting on the ground, legs out, bike lying beside him, front wheel spinning; ground = his seat |
| `balloon_frame("major", g, n, per=72, color, seated=True, red=True)` | 24 per breath, 3 breaths per balloon | cheeks swap puff 1 / 2, balloon grows per breath, `n` = balloon number (colour cycles); seated on a crate; red face + steam |
| `laugh_frame(cast, g / 10, base)` | 10 (3 Hz) | belly-laugh bounce: squash (1.02, 0.98) <-> (0.99, 1.02), head_dy 0 <-> 0.06; laugh drawing held |
| `wave_frame(cast, g / 12, facing)` | 12 | open hand waving beside the head |
| `carry_pose(cast, g / 28 or None, facing)` | 28 (walk) | crate in both hands |
| `tiptoe_frame(cast, g / 32, facing)` | 32 | sneak cycle + finger to the lips |
| `paddle_frame(cast, g / 24, facing)` | 24 | kneeling low (legs go behind the gunwale), both hands on the paddle; the blade dips below the ground point on purpose |
| `lift_pose(cast, t, lift_h=LIFT_H, expr, mouth, strain)` | t: wobble | **arms straight up, palms open; the TOP of both hands is exactly `LIFT_H` = 3.45 D above the soles for every GI** (legs bend to fit, rubber-hose arms `reach23=1.6`, head sinks a little). `lift_anchors(cast, pose)` -> the two hand tops. 4 lifters line up under one tank: put the tank's track bottoms at ground + 3.45 D (sheet section "lift") |
| `binocular_pose(cast, expr, t)`, `sit_crate_pose(cast, **kw)` | - | binoculars at the eyes, both hands / sitting on a crate |

**Lip-sync: only the quoted speakers move their mouths**: `major_point_quote`, `major_promise_quote` (S07) and `gi_smile_lift_quote` (S13) are tagged `STORY23_META[n]["lipsync"]`: drive `mouth = talk_mouth(g)` inside the quote window, `"flat"` (Major) / `"grin"` (smile) outside. Every other mouth is one held drawing (the French "chatty" face holds `talk_a`; the radio man holds `talk_a`). Faces swap whole drawings; change `expr` / `red23` / `puff23` on a blink (`blink` 1, 2, 1).

## STORY23 (`cast23.STORY23[name] = (cast, pose)`, merged into `puppet.STORY`; notes in `STORY23_META`): 143 poses

- **GI pose library**, for every GI (`gi_<action>_<member>`, member = painter / sound / radio / pump / designer / smile / driver): `stand`, `salute`, `point`, `shock` (jaw drop), `sweat` (big drop), `laugh`, `wave`, `walk`, `lift`, `carry`, `tiptoe`, `paddle`, `droop`, `grin`.
- Roles: `gi_paint_star`, `gi_painter_stencil` (S10), `gi_sound_carry_record`, `gi_sound_switches` (S09), `gi_radio_talk` (S10), `gi_pump_pump`, `gi_designer_clipboard`, `gi_designer_point`, `gi_smile_lift_quote` (S13, lip-sync), `gi_smile_dry`, `gi_pin_prick` (S03), `gi_polish` (S02), `gi_chalk` (S08 driver chalks the crate), `driver_drive` (jeep).
- Major: `major_stand` (smug + cigar), `major_laugh` (S06), `major_point_quote`, `major_promise_quote` (S07, lip-sync), `major_angry_red`, `major_jaw_drop`, `major_puff` (S19), `major_sit`, `major_walk`.
- French: `fr_ride_*`, `fr_chat_*`, `fr_stare_*` (braking), `fr_jaw_*` (braking), `fr_fall_*`, `fr_stand_*` with `*` = `beret` / `cap`.
- German: `ger_binoc_*`, `ger_surprise_*`, `ger_nudge_*`, `ger_point_*` (`tall` / `round`), `ger_sausage`, `ger_drop_sausage` (S17).

## Ground point (bottom anchor) and canvases

The sprite's feet point (`anchors["feet"]`, `feet_y`; also `anchors["ground"]`) is ALWAYS the ground contact: soles when standing, **wheel contact line** on the bicycle, the **crate bottom** when seated on a crate, the **seat** when sitting on the ground. stage/sprites.py puts it at the fixed pixel `origin_px` = (-x0, -y0) x px_per_D of every sprite, so a card placed with `actor.place(f, (x, y, ground_z))` is ground-snapped. `python3 test_cast23.py ground` renders 1109 sprites (every story pose and cycle frame) and measures the lowest opaque row against the ground row: **-3 .. -1 px at 96 px/D (sole/tyre ink reaches the ground line), no floating gap, nothing clipped.** `cast23.sprite(...)` writes `<png>.json` with `origin_px` and `gap_px` for any single sprite.

Canvases (feet-relative, D, registered into `sprites.DEFAULT_CANVAS` via `cast_ext.CANVAS`, measured over every pose + 0.32 D head room): `CANVAS23[name]` (standard) and **`CANVAS23_WIDE[name]` for bicycle and pump poses** (pass it to `Actor.build` / `make_actor(canvas=...)`); e.g. major (-1.5625, -4.0625, 1.5625, 0.125), fr_beret wide (-1.8125, -3.6875, 1.8125, 0.1875), gi_pump wide (-2.1875, -3.375, 2.1875, 0.125).

## Putting a card in a set3d23 scene

Copy `v3/film8/common.py` to `v3/film23/common.py` and replace `cast8` by `cast23` (path `v3/cast23`, **import cast23 before `actors` / `sprites`**) and the `desert` set by `ghost` (`v3/set3d23`). Then per actor:

```python
a = C.make_actor("maj", "major", sprite_dir)                                        # standard canvas
b = C.make_actor("fr1", "fr_beret", sprite_dir, canvas=cast23.CANVAS23_WIDE["fr_beret"])   # on the bike
gz = GH_scenes.ground_fn(scene)                    # set3d23 terrain height z(x, y) (ghost_scenes.ground_fn)
C.place(b, f, (x, y), z=gz(x, y))                  # the wheel contact sits ON the terrain
b.pose(f, cast23.ride_frame("fr_beret", g / 14.0, facing=1), camera=cam, upper_k=1.0)    # bike: keep upper_k 1 (the handlebar is above the hip line)
```

- 1 Blender unit = 1 D (the set uses the same scale). The rubber M4 decoy (ghost_props.tank_mesh) is about 9 D long and 4.2 D high: for S12/S13 raise the tank so its track bottoms sit at ground + `LIFT_H` (3.45) and space the 4 lifters (`lift_pose`) ~2.3 D apart along its length; their hand tops are the tank's underside.
- The pump's hose end (anchor `hose_end`) is on the ground on the facing side: put the tank's valve there or hide the join behind a set hose.
- The cards are emission-only: never tint them in the shader; use the puppet `tint` / `ink` keys for night (e.g. `tint="#c8ccf0", ink="#1e142e"` at CAMP / RHINE).

## Files and QA

- `cast23.py` the module, `test_cast23.py` (modes `sheet`, `canvas`, `ground`, `robust`; no argument = all).
- `cast_sheet.jpg`: line-up front + 3/4 with heights; every role/story pose (LIP-SYNC tagged); the GI pose library across the 7 faces; the 4-lifter line-up under a tank box at LIFT_H; 15 face states + specials per member (Major red / puff 1 / puff 2 / cigar; cyclists chatty / dazed; dry smile; German surprise); every prop. `cycles.jpg`: 8-frame strips of walk, pump, paint, pedal (both riders, both facings), blow balloon, laugh bounce, wave, carry, tiptoe, paddle, fall + daze, lift strain, with the ground line drawn.
- Results: canvas 0 problems; ground 1109 sprites, gap -3 .. -1 px, 0 problems; robust 920 garbage-pose + determinism checks OK.

## Known weaknesses

- No back views (puppet limit): S17's OTS from behind the observers shows them in 3/4 front; the binoculars are cast10's front-view glasses.
- The bicycle is one fixed side view with the rider's legs over the frame; at `look` > 0.6 the head turns to camera but the bike stays in profile. The fallen bike is a flattened top-ish view (two ellipses), stylised.
- `upper_k` stretch from `Actor.pose` would stretch the handlebar / held tank-free arms above the hip line: keep `upper_k=1.0` for bike, pump and lift poses.
- Seated Major: the long tunic skirt hides the thighs, so the crate reads mostly at the sides and below; the knees still show the sit.
- The lifters' arms are drawn 1.6 x longer (rubber hose) so their hands clear the helmets; the shortest (gi_pump) is at full reach with straight legs.
- The M43 cap's peak is small at < 50 px heads; the pencil moustaches of gi_sound / gi_driver vanish below ~60 px heads (the headphones and the frown still tell them apart).
- The radio man's handset covers the near cheek; his chatter mouth is a held drawing (not a quote).
