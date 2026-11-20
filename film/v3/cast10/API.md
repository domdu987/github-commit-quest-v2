# cast10.py: the cast of film 10 ("ไอ้ช่างม้าลาย", dazzle camouflage, a British naval dockyard, 1917) for the v2 puppet

File: `PROJ/v3/cast10/cast10.py` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`).
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast9` is edited. On import, cast10 imports cast9, which chains cast8 .. cast_ext and v2/puppet. It then adds entries to their tables and wraps the puppet helpers on top of cast9's wrappers: `_norm` (this module's pose keys), `_face` (paint spots), `_moustache` (style `walrus10`), `_ink_limb` (epaulettes, paint-splattered trousers), `_hand` (white gloves), `_prop` (new props) and `figure` (the hanging plank and the periscope). Each wrapper falls through to the earlier ones, so every earlier member draws exactly as before. The test confirms that all 38 STORY9 poses give byte-identical SVG.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast10")
import cast10                # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                # same module object: CAST now also has the 6 members below
cast, pose = cast10.STORY10["painter_paint_stroke"]
f = puppet.figure(cast, pose, "f")                                          # f["anchors"]["brush_r"] = bristles
p = dict(cast10.STORY10["admiral_point_mock"][1], mouth=cast10.talk_mouth(g, 1.0), blink=cast10.blink_at(g, 90))
w = puppet.figure("admiral", cast10.cycle("admiral", g / 28.0, "walk"), "f")
a = actors.Actor("adm", "admiral"); a.build(sprites.DEFAULT_CANVAS["admiral"], sprite_dir, contact=True)
a = actors.Actor("admp", "admiral"); a.build(cast10.CANVAS10_PLANK["admiral"], sprite_dir, contact=True)   # on the plank
```

For film 10, copy `film8/common.py` and put `cast10` in place of `cast8` in the path list and the import. Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies unchanged: pose keys, the 20 expressions, `mouth` including `("open", w, h)`, `blink`, `gaze`, the fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose` and `hand_for_tip`.

**The painter's CAST key is `painter10`.** `painter` is film 7's copyist and is left unchanged.

## Cast (head D = 1, the same proportions as cast9)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `painter10` | `slim` 0.62 x 1.00, legs 1.34 | 3.20 (3.38) | Norman: lean, a dark navy **beret** flopped to one side, a **small dark moustache**, a blue work shirt with **rolled sleeves**, cream painter's **bib overalls splattered** with black, white and grey paint (bib and trouser legs), brown boots |
| `admiral` | `stout` 1.48 x 1.28, legs 1.28 | 3.43 (3.68) | **big belly**; navy **double-breasted coat** with two converging rows of **gold buttons**, peaked lapels, white shirt and black tie, medal ribbons and a knee-length skirt; gold-fringed **epaulettes**; gold cuff rings; **white gloves**; navy **peaked cap with gold oak-leaf braid** on the peak, a gold chin cord and an anchor badge; a **huge white walrus moustache**, white hair, ruddy cheeks, a double chin |
| `sailor_a` | `slim`, tall | 3.20 (3.42) | **white sailor cap** (rolled brim), white jumper, **blue square collar** with three white tapes, black silk with a white tape bow, navy bell-bottoms |
| `sailor_b` | `regular`, pear-shaped | 2.88 (3.10) | round, bushy brown moustache, the same uniform, cap tipped the other way |
| `sailor_c` | `slim`, short | 2.78 (3.00) | ginger hair, freckles, the same uniform |
| `uboat_captain` | `regular` | 3.02 (3.27) | **grey peaked cap** (black band and peak, small cockade), a **short dark beard** with a moustache, a dark grey leather double-breasted coat to mid-shin over a white roll-neck, a belt, black boots |

For scale, film 9's lin is 3.10 and its general 3.53. The `sheet.jpg` top band shows them at the right of the row.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `paint_spots` | 0..1 (0) | black paint splats on the face, the moustache and the peaked cap, plus a run down the cheek (any cast10 member). They appear one by one as the value rises: 1 = all of them |
| `brush_paint` | 0..1 (1) | the paint load on `bigbrush`; > 0.3 adds runs on the ferrule and drips falling from the lowest bristle corner (animate with `t`) |
| `brush_col` | "black" / "white" / "grey" ("black") | the colour of the brush paint |
| `bucket_paint` | 0..1 (1) | the paint in `paint_bucket` (black) |
| `plank` | 0 / 1 (0) | draws a **hanging painter's plank** behind the figure, with its top at the soles, two hemp ropes rising `plank_rope` D and paint drips. Set it to 0 when the set provides its own plank. Anchors `plank_l` / `plank_r` |
| `plank_w`, `plank_rope` | D (2.40, 3.90) | the plank's width and the rope length above the soles |
| `periscope` | 0 / 1 (0) | draws the **U-boat periscope**: a steel column from y = `SCOPE_TOP` (-1.30, head frame) to the floor, set `SCOPE_DX` (0.44) beyond the eye on the facing side; a handle bar with grips at the height of the hand on a grip; and an eyepiece box with a rubber cup **over the facing eye**, drawn in front of the face. The hands on the grips are redrawn over the bar. Mirror is supported. Anchors `scope_eye` / `scope_top` |
| `t` | float | drives the drips (as in cast9) |

New expression: **`squint`**: both eyes squeezed (`><`), determined brows and a frown. It is added to `puppet.EXPRESSIONS` only if missing. The captain uses it at the periscope, where the eyepiece covers one eye and the other shows squeezed shut.

CAST keys (cast10 members only): hat_style `peaked10` (hat_colors crown / crown_l / crown_d / band / visor / visor_l / badge / badge_c; `braid=True` gives the gold braid and the anchor badge) and `dixie10` (hat_colors light / base / dark); costume `overalls10` (cast7 overalls7 colours + splatter), `admiral10` (colors base / dark / lapel / shirt / tie; `coat_len`, `coat_flare`), `sailor10` (colors base / dark / collar / tape / silk / pants), `ucoat10` (colors lapel / sweater / sweater_d / button / belt; `coat_len`, `coat_flare`); `moustache_style="walrus10"` (with `tache_scale` and colors moustache / moustache_l); `epaulette10=<size>`; `gloves10=<colour>`; `splat10=True`. The captain's beard is cast6's `beard`.

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` | orientation / anchors |
|---|---|---|---|
| `bigbrush` | a big wall brush 1.6 D long: wooden handle (-0.56 .. 0.62), broad tin ferrule, thick flat bristle block **dripping black paint** | bristle ends (1.02) | follows `angle`. Anchors `brush_r/_l` (the bristles) and `grip_far_r/_l` (the other hand, on the handle at -0.42). Keys `brush_paint`, `brush_col`, `t` |
| `paint_bucket` | a galvanised pail hanging from its wire bail, black paint in it and runs down its side | bottom (0.52) | always upright. Anchor `bucket_bottom_*` |
| `binoculars` | field glasses **seen from the front** (blue glass, glints, a focus wheel) | glasses centre | always upright. The hand grips the outer barrel. Anchors `binoc_*` (centre) and `grip_far_*` (the other barrel, for the second hand) |

Standalone pieces (SVG fragments in D units): `bigbrush_svg(uid, paint, col)`, `paint_bucket_svg(uid, paint, col)`, `binoculars_svg(uid)`, `plank_svg(uid, w, rope)` -> (svg, bbox), `periscope_svg(uid, top, bottom, handle_y, eye)`. The last one is for the periscope seen from outside, poking out of the water: draw only its top.

## Cycles, lip-sync, blink

These are re-exported from cast6 and work for every member: `cast10.cycle(cast, phase, mode, facing, base, arms, speed)` with the modes `walk` / `run` / `sneak` / `march`, `cast10.talk_mouth(frame, level, seed, hold)`, `cast10.blink_at(frame, period, offset)` and `cast10.NOD`.

**Mouths:** every story pose holds one fixed mouth shape. Only the three poses marked `STORY10_META[name]["lipsync"] = True` are meant to have `mouth = talk_mouth(g)` driven during the admiral's quotes (boss line about 11.0-17.6 s, false line about 31.0-33.2 s): `admiral_point_mock`, `admiral_finger_up_promise` and `admiral_shout`. Outside the quotes, set their mouth to `"flat"`. The laugh poses hold an open laugh mouth that does not move. The walrus moustache is drawn under the mouth, so the lip-sync shapes stay readable.

## STORY10 (`cast10.STORY10[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast10.STORY10_META[name]["note"]`

| name | cast | what |
|---|---|---|
| `painter_paint_stroke` | painter10 | **big brush raised and sweeping** (screen-right), both hands on the handle, drips. Animate arm_r from (0.70, 0.55) / angle -20 to (0.66, -0.30) / angle -62 |
| `painter_step_back_proud` | painter10 | a step back, chest out, smug smile, brush hanging at his side, hand on hip |
| `painter_calm_smile` | painter10 | calm smile, brush upright at the shoulder, bucket in the other hand |
| `painter_on_plank` | painter10 | **on the hanging plank** (`plank=1`), painting the hull (screen-right), bucket in hand. Canvas `CANVAS10_PLANK` |
| `painter_grin` | painter10 | grinning, arms folded (shot 20) |
| `painter_walk` | painter10 | walk frame with the brush on his shoulder |
| `admiral_laugh_big` | admiral | **big belly laugh**, head back, gloved hands on the belly, tears |
| `admiral_point_mock` | admiral | **pointing and mocking** (screen-right), other hand on hip. **lip-sync** |
| `admiral_finger_up_promise` | admiral | **index finger up**, chest out, other hand on the chest. **lip-sync** |
| `admiral_arms_akimbo` | admiral | smug, arms akimbo |
| `admiral_binoculars_up` | admiral | **binoculars at the eyes** (placed on the eye midpoint), both hands |
| `admiral_shout` | admiral | **shouting** on the bridge, pointing out to sea, binoculars in the other hand. **lip-sync** |
| `admiral_jaw_drop` | admiral | **jaw dropped** (held open mouth), eyes wide, arms hanging, binoculars dangling |
| `admiral_binoculars_lowered` | admiral | binoculars just **lowered** to the chest, shocked eyes |
| `admiral_plank_sheepish` | admiral | **ending**: on the plank (`plank=1`) with the brush, `paint_spots=1` (face, moustache, cap), sheepish smile, blush and sweat, scratching the back of his head. Canvas `CANVAS10_PLANK` |
| `admiral_walk` | admiral | walk frame (shot 5 stride) |
| `sailor_point_laugh` (+`_a/_b/_c`) | sailor_a / _b / _c | pointing and laughing (screen-right; `mirror=True` for left). Names: `sailor_point_laugh_a`, `_b`, `_c` |
| `sailor_laugh_hold_belly_*` | " | doubled over laughing, eyes shut, holding the belly |
| `sailor_idle_*` | " | standing, one hand behind the back |
| `uboat_periscope` | uboat_captain | **at the periscope** (`periscope=1`): eye at the eyepiece, the other eye squeezed (`squint`), both hands on the grips |
| `uboat_aim` | uboat_captain | aiming: eye still at the eyepiece, one hand on the grip, the other fist raised (mouth shut) |
| `uboat_stand` | uboat_captain | standing, hands behind the back |

That makes 28 poses. No name collides with earlier STORY entries or CAST keys.

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D)

| member | canvas |
|---|---|
| painter10 | (-1.875, -4.625, 1.875, 0.125); on the plank: `CANVAS10_PLANK` (-1.875, -4.625, 1.875, 0.3125) |
| admiral | (-1.8125, -5.0, 1.8125, 0.125); on the plank: `CANVAS10_PLANK` (-1.8125, -5.0, 1.8125, 0.3125) |
| sailor_a | (-1.5, -4.5625, 1.5, 0.125) |
| sailor_b | (-1.5, -4.25, 1.5, 0.125) |
| sailor_c | (-1.4375, -4.1875, 1.4375, 0.125) |
| uboat_captain | (-1.875, -4.375, 1.875, 0.125); at the periscope: `CANVAS10_SCOPE` (-1.875, -4.375, 1.875, 0.1875) |

`python3 test_cast10.py canvas` checks:
- every arm preset with paint_bucket and binoculars at yaw ±0.6 (mirrored, squash 0.8-1.15);
- crouch, wide legs, all the fx, paint spots and yaw ±1.2;
- every STORY10 pose without plank or periscope;
- 16 phases x 4 modes x 2 facings of the cycles;
- the plank set and the periscope set, mirrored too.

All of them fit with at least 0.32 D of head room. head_flip: 28 poses, 0 problems. The long `bigbrush` swung outside the story poses can exceed a canvas: pass a wider canvas to `Actor.build`. The plank's ropes stop `plank_rope` D above the soles: shorten them, or set `plank=0` and let the set's plank and ropes carry it.

## Files and QA

- `cast10.py` is the module.
- `test_cast10.py` has three modes:
  - `sheet` -> `sheet.jpg`: heights front + 3/4 next to film 9's lin and general; every STORY10 pose with the lip-sync ones tagged; 18 face states per member (neutral, talk_a / talk_b / talk_o / flat, blink 1 / 2, happy, laughing, grinning, smug, angry, shouting, shocked, worried, squint, sheepish, paint spots); every prop. Each image is labelled underneath on a neutral grey ground.
  - `canvas`: the canvas check above.
  - `robust`: pose-key garbage on the 6 members plus v2 `test_puppet.py --quick`. Result: 2400 + 2 049 684 checks, 0 failed (`run_robust.log`).
- `backup/`: snapshots of the module, the test and the sheet after each fix round (v1 .. v4).
- No Blender stage test was rendered (no shots, as asked). The canvases go through the same `cast_ext.CANVAS` → `sprites.DEFAULT_CANVAS` path as cast9.

## Known limits

- The admiral's navy sleeves on the navy coat are a lighter navy with gold cuffs and white gloves; even so, an arm crossing the coat reads weaker than cast9's red-on-gold at small sizes.
- The captain's cast6 beard is full and dark: talk shapes barely show on it. He has no lip-sync, so this is acceptable; his `laughing` and `grinning` mouths still read.
- The binoculars are always drawn from the front (objectives to the viewer), even when held low; at chest or belly height they read a little like a brooch at small sizes.
- The periscope is a figure-level overlay in the puppet's 2D plane. The eyepiece is placed on the facing eye for yaw around 0.5; at other yaws or with a strong `head_roll` the cup may sit off the eye. For an outside view of the periscope above the water, use the 3D set prop or `periscope_svg`.
- `paint_spots` positions follow the face layout, not the moustache outline: at yaw near ±1 some spots fall off the moustache.
- Held pieces are drawn in the arm's layer (as in cast8/9).
- `resolve_pose` / `lerp_pose` drop the cast7..10 keys. Re-add `paint_spots`, `brush_paint`, `brush_col`, `bucket_paint`, `plank*`, `periscope` and `t` to tweened poses.
