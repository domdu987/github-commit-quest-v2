# cast25.py: the cast of film 25 (Britain's first tank, Mark I, 1915-16, ending at Flers 15 Sep 1916) for the v2 puppet

File: `PROJ/v3/cast25/cast25.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only, deterministic. Nothing older is edited. cast25 imports cast24 (which chains cast10 .. cast_ext and v2/puppet) and wraps `_norm`, `_face`, `_moustache`, `_ink_limb`, `_prop` on top of cast24's wrappers; everything it does not handle falls through. `python3 test_cast25.py identical` confirms 705 earlier STORY / cycle SVGs (every STORY entry up to film 24, cycles of 40 members) are byte-identical with cast25 imported. Comic and bloodless; no letters, numbers or insignia text anywhere (ribbons, patches, plans and flags are plain colour / plain lines).

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast25")
import cast25                      # BEFORE sprites / stage.sprites
import puppet
cast, pose = cast25.STORY25["general25_point_stick"]
p = dict(pose, mouth=cast25.talk_mouth(g, 1.0), blink=cast25.blink_at(g, 90))          # lip-sync inside his quotes only
w = puppet.figure("tommy_a25", cast25.cycle("tommy_a25", g / 28.0, "walk"), "f")        # walk 28 frames, run 16, march 24
r = puppet.figure("german_b25", cast25.run_away25("german_b25", g / 16.0, facing=1), "f")   # comic flee (arms flailing, helmet bounces)
m = puppet.figure("general25", cast25.march_flag25(g / 24.0), "f")                       # marching behind the tank, flag waving
a = actors.Actor("gen", "general25"); a.build(cast25.CANVAS25["general25"], sprite_dir, contact=True)
a = actors.Actor("p", "pilot25"); a.build(cast25.CANVAS25_POSES["pilot25_lean_look"], sprite_dir, contact=True)   # cockpit crop
```
Everything in `v2/puppet/API.md`, `v3/cast10/API.md` and `v3/cast24/API.md` still applies (pose keys, expressions, `mouth`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `rim`, `lerp_pose`, `hand_for_tip`; `cycle`, `talk_mouth`, `blink_at`, `NOD`, `CYCLE_MODES` are re-exported). Colours are unlit flat mid-to-deep tones per COLOUR_SPEC section 2 (heads, ink, mouth are the puppet defaults).

## Members (head D = 1; height = head top to soles, hat top in brackets)

| key | height | build / look |
|---|---|---|
| `general25` THE MOCKER | 3.27 (3.66) | stout, huge belly, short legs; red cheeks, huge white walrus moustache, white hair, double chin; khaki service dress, brown Sam Browne belt + cross strap, scarlet gorget tabs with brass buttons, 12 plain medal ribbons, box-pleat patch pockets; khaki peaked cap with a broad scarlet band, black peak; breeches and polished tall brown boots |
| `engineer25` THE QUIET HERO | 3.26 (3.36) | slim, young, clean-shaven, sandy hair; rust 8-panel flat cap, red pencil behind the ear; teal waistcoat with brass buttons and a watch chain over a cream collarless shirt, sleeves rolled to the elbow; dark trousers, brown boots. Never speaks (every pose has `mouth="flat"`) |
| `worker_a25` | 3.03 (3.16) | stocky, big black beard, baggy mustard cap, blue denim bib overalls over a rust shirt (rolled sleeves), rag in the pocket |
| `worker_b25` | 2.69 | short and round, bald with a ginger fringe, ginger moustache, long leather apron over a grey-green shirt |
| `worker_c25` | 3.54 (3.56) | tall and lanky, thick brows, tight slate-blue docker cap, olive boiler suit with rope belt, spanner in the chest pocket |
| `tommy_a25` | 3.16 (3.30) | medium, freckled, ginger hair, drab-green Brodie, khaki + buff webbing, water bottle |
| `tommy_b25` | 3.42 (3.56) | tall and thin, sandy khaki, big drooping Kitchener moustache, Brodie with a hessian cover, haversack |
| `tommy_c25` | 2.75 (2.88) | short and round, red wool muffler, tan-green Brodie, ruddy cheeks, round brows |
| `tommy_d25` | 3.18 (3.32) | broad, black bushy moustache + stubble, dark green Brodie worn crooked, entrenching tool, brown-khaki |
| `german_a25` | 3.22 (3.68) | slim, upturned Kaiser moustache, grey cloth-covered Pickelhaube with a plain red patch, feldgrau tunic, brown ammunition pouches, bread bag |
| `german_b25` | 3.50 (3.91) | tall and lanky, round glasses, blond, paler cover with a green patch, greatcoat roll over the shoulder, flask |
| `german_c25` | 2.77 (3.28) | short and stout, double chin, black toothbrush moustache, dark plain cover, tall spike |
| `pilot25` | 3.16 (3.32) | RFC: brown leather flying helmet with ear flaps and goggles pushed up on the forehead, pencil moustache, brown leather coat with a cream fur collar and a long cream silk scarf, tall boots |

Tommies: khaki tunic with four patch pockets, brass buttons, buff webbing (braces, belt, pouches), wrapped puttees (`puttee25` colour; drawn over the lower leg), short ankle boots. Germans: feldgrau tunic with red piping, black Y-straps, belt with a round brass plate, tall black boots.

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | effect |
|---|---|
| `hat_off25` 0/1 | no hat (bare head, hair shows). Use with the `helmet25` prop in the hand, or when the helmet is on a stick |
| `hat_up25` D (-0.5..1.5) | lifts the hat straight off the head (comic double-take, flying helmet) |
| `mg_gy25` y (head frame) | ground line for `mg25`: the sledge skids end on it. Set it to `figure(...)["feet_y"]` of the same legs |
| `paint_col25` | brush / pot paint: `white` (default), `black`, `red`, `green`, `grey` |
| `plan_w25` 0.6..2 | width of the `plan25` sheet (default 1.25) |
| `t` | flag wave phase (0..1 loop), as every animated effect; also the toy tank swing (16 degrees x sin(2 pi t)) and the water-stream drop phase |
| `pour25` 0..1 | tilts `watering_can25` (64 degrees at 1); above 0.5 a thin water stream falls from the rose (full length at 0.7) |
| `dirt25` 0..1 | heap of earth on the `shovel25` blade (above 0.5 crumbs fly above it) |
| `fire25` 0..1 | muzzle flash and smoke puff on `mg25` |
| `glasses_dy25` 0..1 | round glasses (german_b25) slide 0.15 D down the nose |

CAST keys: hats `brodie25` (`cover25="hessian"`), `pickel25` (`patch25` colour, `hat_h`), `peakcap25`, `flatcap25` (`cap_style` baggy / neat / docker), `flyhelm25`; costumes `staff25`, `tunic25` (`kit25` tuple of bottle, scarf, pack, tool, `puttee25`), `waist25`, `work25` (`work_style` bib / apron / boiler), `feld25` (`kit25`: bread, roll, flask), `coat25`; `moustache_style` `walrus25`, `kaiser25`, `kitchener25`, `brush25`; `bigbeard25=dict(color, dark, light)`.

## Props (`prop_r` / `prop_l`, `prop_tip_*`, extra anchor `<name>_r/_l` = the working point)

| type | tip | note |
|---|---|---|
| `hammer25` | 0.66 | riveting hammer (ball-peen); anchor `hammer_r` = the face. Use `scale` 1.3 in close shots |
| `spanner25` | 0.82 | big open-ended spanner; anchor `spanner_r` = the jaws |
| `paint_brush25` | 0.66 | long-handled flat brush, colour by `paint_col25`; anchor `paint_brush_r` = bristles |
| `paint_pot25` | bottom | tin paint pot hanging by its bail, always upright; anchor `paint_pot_r` |
| `bucket25` | bottom | plain galvanised water bucket with water in it, always upright; anchor `bucket_r` = the bottom |
| `ladle25` | 1.12 | long wooden-handled iron ladle; anchor `ladle_r` = the cup |
| `swagger25` | 0.99 | polished swagger stick, brass knob + ferrule, wrist loop; anchor `swagger_r` = the tip |
| `flag25` | 0.88 | little plain red pennant on a pole (swallow-tail), waves with pose key `t`; pole = prop direction (angle -82 = up), cloth flies to the figure's facing side |
| `helmet_stick25` | 2.35 | rifle-length stick (2 D) with a Brodie perched on top; anchor `helmet_stick_r` = the helmet top |
| `helmet25` | top | a Brodie held in the hand, dome up (pair with `hat_off25=1`); anchor `helmet_r` |
| `plan25` | - | rolled-out blueprint hanging to the body side of the hand: blue sheet, white plain lines, a rhomboid tank profile, NO text; anchors `plan_far_r` (second hand, grips the far roll) and `plan_r` |
| `watering_can25` | rose | galvanised can, long spout + rose, arched top handle gripped by the hand, always upright on screen (tilted only by `pour25`, flipped for the left hand); anchor `watering_can_r` = the rose; stream at pour25 > 0.5 |
| `shovel25` | 1.78 | trench spade: wooden D-handle at the hand, ash shaft, steel blade; `dirt25` heaps earth on it; anchor `shovel_r` = the blade tip. Second hand via `_hand_on_stick`-style target |
| `tin_cup25` | rim | enamel tin mug (white, blue rim, dark tea), hand on its handle, mouth up at angle 0 (tip it with `angle`); anchor `tin_cup_r` = the rim centre. Use `scale` 1.3 in close shots |
| `toy_tank25` | toy | tin toy Mark I hanging by a string from the hand (finger and thumb), swings with `t`; anchor `toy_tank_r` = the toy |
| `chalkboard25` | chalk | held slate 1.6 x 1.1 D, wooden frame, dark green-black, hangs to the body side of the gripping hand, upright; white chalk lines only: two ground lines, the trench between, a rhomboid tank straddling it (no letters, no arrows); anchor `chalkboard_l/_r` = the chalk tank (the tapping finger target) |
| `mg25` | 1.14 | Maxim machine gun on its sledge, pointing along the arm angle (use 0); grips at the hand; legs reach `mg_gy25` |

Standalone: `cast25._prop_body(k, kind)` (SVG in D units, hand at origin) and `cast25._upright_body(k, kind)` for the upright ones.

## Helpers

`cast25.cycle(member, phase, mode, facing, base, arms, speed)` for every member (modes walk / run / sneak / march). `cast25.march_flag25(phase, facing=1, t=None)` = the general's knees-up march with the flag. `cast25.run_away25(member, phase, facing=1, flail=1.0, hat_up=0.0)` = comic flee for any member.

## STORY25 (`cast25.STORY25[name] = (cast, pose)`, notes in `STORY25_META[name]["note"]`; also merged into `puppet.STORY`) : 106 poses

- `engineer25`: `blueprint`, `chalkboard_tap`, `chart_hand`, `peek`, `point`, `proud`, `shush`, `sleeves`, `sleeves_roll`, `stand`, `walk`, `whisper`
- `general25`: `cheer`, `field_glasses`, `finger_wag`, `glasses_laugh`, `laugh`, `laugh_b`, `march_flag`, `point_stick`, `shocked`, `stand_smug`, `toy_dangle`, `walk`
- `german_a25`: `mg_crouch`, `peek`, `run_away`, `stand`, `surprised`, `walk`
- `german_b25`: `glasses_slip`, `mg_crouch`, `run_away`, `stand`, `surprised`, `walk`
- `german_c25`: `mg_crouch`, `mg_fire`, `run_away`, `stand`, `surprised`, `walk`
- `pilot25`: `lean_look`, `stand`, `walk`
- `tommy_a25`: `cheer`, `duck`, `helmet_on_stick`, `laugh_point`, `march`, `peek`, `push`, `stand`, `walk`
- `tommy_b25`: `cheer`, `cup_wait`, `duck`, `helmet_on_stick`, `laugh_point`, `march`, `push`, `stand`, `walk`
- `tommy_c25`: `cheer`, `duck`, `helmet_on_stick`, `ladle_tap`, `laugh_point`, `march`, `push`, `stand`, `walk`
- `tommy_d25`: `cheer`, `dig_a`, `dig_b`, `duck`, `helmet_on_stick`, `laugh_point`, `march`, `push`, `stand`, `walk`
- `worker_a25`: `carry_bucket`, `cup_drink`, `hammer_crate`, `nod`, `rivet`, `rivet_strike`, `stand`, `walk`
- `worker_b25`: `carry_pot`, `nod`, `nod_serious`, `paint`, `shocked`, `stand`, `walk`
- `worker_c25`: `carry_bucket`, `mime_drink`, `nod`, `pat_hull`, `pour_can`, `push_barrel`, `spanner`, `stand`, `walk`

Lip-sync: only `general25_point_stick`, `general25_glasses_laugh`, `general25_toy_dangle` (20.06-20.87 s) and `general25_finger_wag` (23.75-25.35 s) have `STORY25_META[name]["lipsync"] = True`: set `mouth = talk_mouth(g)` inside his quotes (18.39-25.30 s and 44.37-46.40 s), `"flat"` outside. Every other pose holds one fixed mouth; the laugh poses hold an open laugh mouth. The engineer never talks. Loop helpers: `general25_laugh` / `general25_laugh_b` alternate every 3-4 frames for the belly bounce; `worker_a25_rivet` <-> `_rivet_strike`; push, cheer and laugh poses bounce by `squash`.

## Shot-plan v2 poses (added)

Mostly waist-up close shots on the full-body cards (the camera crops the legs). All face screen-right; `mirror=True` for left (the German peek in shot 9 is mirrored). The engineer still never talks: `engineer25_proud` uses the closed `smile` mouth. Special canvas: `german_c25_mg_fire` (wider, muzzle flash). `field_glasses25` was NOT added: `general25_field_glasses` already shows a clear pair of binoculars (prop `binoculars`). Held props are placed with the hand on the grip (cup handle, spade D-handle, can arch, string, slate edge). `_hand_to(S, name, key, anchor, off)` is the helper that puts a hand anchor on another anchor (used for the shush finger and the chalk tap).

## Accent colours v2 (default for cast25; earlier films are untouched, `identical` 705/705)

Face and skin whites are unchanged (#fef7f6). Raised: general scarlet band and tabs #ee2418, cheeks #f23a2e, brighter brass (#f6c21c); engineer teal waistcoat #08909c, rust-orange cap #cc5a1a; workers mustard cap #dca412, cobalt denim #2458d0, ginger #d86a1c; Tommies red muffler #e41e1a, richer Brodie greens (a #5f8c2a, c #7e9838, d #3a7a28); Germans vivid red piping and patch #ee2a20, feldgrau pushed slightly bluer (#527a72 / #587a74 / #466e66); pilot scarf #fff8de; flag pennant #ee2a1e. Khaki and feldgrau bases stay readable.

## Ground and feet

Every pose stands on `feet_y` (both soles on the line; `anchors["feet"]` is on it, `test_cast25.py canvas` checks all 106 poses, 0 problems). Crouched poses (`duck`, `helmet_on_stick`, `mg_crouch`, `push`) lower the figure but the soles stay on `feet_y`. `pilot25_lean_look` is an upper-body pose for a cockpit card: its canvas `CANVAS25_POSES["pilot25_lean_look"]` is cut 0.25 D below the hip; the legs are inside the aircraft.

## Canvases (feet-relative, D)

`CANVAS25[member]` (registered in `cast_ext.CANVAS` -> `sprites.DEFAULT_CANVAS`): general25 (-2.125, -4.8125, 2.125, 0.125), engineer25 (-1.9375, -4.8125, ..), worker_a25 (-2.0, -4.4375), worker_b25 (-2.0625, -4.125), worker_c25 (-2.1875, -5.125), tommy_a25 (-1.9375, -4.625), tommy_b25 (-1.9375, -5.0), tommy_c25 (-2.0625, -4.125), tommy_d25 (-2.0, -4.6875), german_a25 (-1.9375, -4.8125), german_b25 (-1.9375, -5.125), german_c25 (-2.0625, -4.1875), pilot25 (-1.9375, -4.625). They hold every arm preset with a hammer or stick, mirrored, squash 0.8-1.15, crouch, wide legs, yaw +-1.2, the hat lifted 1 D, all cycle modes and run_away25. `CANVAS25_POSES[pose_name]` for the poses that exceed them: `general25_march_flag`, `engineer25_blueprint`, `tommy_c25_ladle_tap`, the four `tommy_*_helmet_on_stick` (taller), the three `german_*_mg_crouch` (+-2.25 wide), `pilot25_lean_look` (cropped).

## Files and QA

`test_cast25.py`: `contact` -> `contact.png` (front line-up with a height ruler in D, next to the film 10 admiral and film 24 Yi; walk strips of all 13 + run strips; every STORY25 pose, lip-sync tagged, ground lines dashed red; 18 face states per member; props), `canvas`, `identical`, `robust` (3250 garbage-key figures, 0 failures).

## Known limits

- Feldgrau is a low-saturation green-grey by nature; it is pushed toward green (S about 0.28-0.35) but stays under the 0.45 target on large surfaces.
- Puttees are drawn along the lower leg as an overlay (straight-ish wraps); at yaw near +-1 or deep knee bends they follow the leg curve but the wrap lines stay diagonal.
- `german_*_run_away` frames look best moving; single frames read as a stride with raised arms. `hat_up25` is an offset, not a physics flight.
- The kaiser moustache wings are thin and sit close to the face edge at yaw above 0.8.
- `mg25` and `helmet_stick25` assume the arm angle given in the story pose (0 and about -80); other angles still draw but the sledge legs only touch the ground at angle 0.
- `resolve_pose` / `lerp_pose` drop the cast25 keys: re-add `hat_off25`, `hat_up25`, `mg_gy25`, `paint_col25`, `plan_w25`, `t` to tweened poses.
