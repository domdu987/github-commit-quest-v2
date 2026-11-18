# cast14.py: the cast of film 14 ("ไอ้บ้าผึ้ง", beehive fence against elephants, Kenya) for the v2 puppet

File: `film/v3/cast14/cast14.py` (PROJ = `film/`, derived from the file location: no /tmp path). Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited: cast14 imports cast10 and adds table entries and wrappers (`_face`, `_norm`, `_prop`, `figure`, `resolve_pose`, `lerp_pose`). Every earlier member draws byte-identically (`python3 test_cast14.py unchanged`: 600 drawings compared).

```python
import sys
sys.path.insert(0, "film/v3/cast14")
import cast14                      # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                      # same module object: CAST now has the people, figure() also draws elephants and bees
cast, pose = cast14.STORY14["uncle_stung_nose"]
f = puppet.figure(cast, dict(pose, nose_swell=0.6), "f")                      # swollen nose 0..1
p = dict(cast14.STORY14["uncle_point_mock"][1], mouth=cast14.talk_mouth(g, 1.0), blink=cast14.blink_at(g, 90))   # lip-sync frame g
w = puppet.figure("matriarch", cast14.cycle("matriarch", frame / 48.0, "walk", facing=1), "e")
```
For the stage: `a = actors.Actor("mat", "matriarch"); a.build(cast14.CANVAS14["matriarch"], sprite_dir, contact=True)`. Elephants go through the same `puppet.figure` call as the people, so `sprites` / `actors` work unchanged (anchors `feet`, `hip`, `head`, `hand_*`, ... all exist). Everything in `v2/puppet/API.md` and `v3/cast*/API.md` still applies to the people (pose keys, 20 expressions, `mouth`, `blink`, `gaze`, fx, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`).

## Scale (D = head diameter = 0.583 m)
1 D = 0.583 m (farmer 1.75 m = 3.0 D). Elephant shoulder 3.3 m = **5.66 D** (matriarch); `elephant_b` 0.86, `elephant_c` 0.93, `elephant_d` 0.77 of that, calf 0.36 (1.2 m). `cast14.M_PER_D`, `cast14.S_D` (= D per metre 1.714). `sheet.jpg` top row shows farmer, uncle, matriarch, elephant_c, calf on a metre ruler with the 1.75 m and 3.3 m lines. So an elephant card must be placed at the same px_per_D as the people, and the set's metres convert with 1.714 D/m.

## People (head D = 1, same proportions as cast9/cast10; white heads as in the series)
| key | look |
|---|---|
| `farmer14` | slim 0.60 x 1.00, legs 1.36: short black hair, faded orange tee (worn hexagon print), khaki trousers rolled to the calf, pale rubber sandals, straw beekeeper's hat PUSHED BACK on the head (forehead free) with a net veil rolled on the brim and a gauze curtain hanging behind (hat_style `veil14`) |
| `uncle14` | stout 1.30 x 1.14: grey stubble beard (CAST `beard`), flat cap, teal check shirt, red check **shuka** slung over the left shoulder and across the chest, belt with brass buckle, brown trousers. Pose key `nose_swell` |
| `woman14` | kitenge headwrap (`headwrap14`, knot with two tails), yellow printed blouse, red wrap skirt with green motifs (costume `kanga14`) |
| `kid14` | small boy (`boy` build), mustard flat cap, green tee, rolled blue shorts |
| `oldman14` | white stubble beard, white kofia cap, cream kanzu robe with a green waistcoat |
| `youth14` | lanky, blue cap, red tee, rolled dark trousers |

New CAST keys / registries: costumes `tee14`, `check14`, `kanga14`, `kanzu14` (cast_ext.COSTUMES); hats `veil14`, `headwrap14` (cast_ext.HATS); `CANVAS14` (cast_ext.CANVAS, feet-relative, D).

### New pose keys
| key | range (default) | effect |
|---|---|---|
| `nose_swell` | 0..1 (0) | any cast14 person: the comic stung nose. 0.05 a pink tip, 0.3 a red knob, 0.6 a fat shiny nose with nostrils, 1.0 a long droopy trunk-like swollen nose, about 1.8 D (1.8 head widths) long, curving down past the chin onto the chest, red-pink and shiny, ring wrinkles, two nostrils at the tip, a sting mark near the root, lumps and a rosy halo. Continuous, animate with an ease-out over about 20 frames; `t` sways the tip. Pair with `gaze=(0, 0.6..0.8)`, `expr="shocked"`, `mouth="o"` |
| `stool` | 0 / 1 (0) | uncle: draws a three-legged stool under the soles (top at the soles, legs down `stool_h` 0.78 D, width `stool_w` 1.30). Canvas `CANVAS14_STOOL["uncle14"]` (-2.19, -5.5, 2.19, 0.94) is REQUIRED for every pose with `stool=1` (`uncle_stool_hang`, `uncle_stung_nose`, `uncle_stung_start`): build the Actor with it (`a.build(cast14.CANVAS14_STOOL["uncle14"], sprite_dir)`); the default uncle canvas would clip the stool legs. Anchors `stool_top`, `stool_bottom`. `test_cast14.py stories` renders these poses through `sprites.render_sprites` and fails on `clipped`. Use 0 if the set carries its own stool |
| `t` | float | flame flicker of `torch14` (animate 0..1 loop) |

### Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended; film 2's `hammer` is reused)
| type | drawing | tip | notes |
|---|---|---|---|
| `tophive` | Kenyan top-bar hive hung by two ropes under its corrugated tin shade roof: long trapezoid wooden box 1.5 D x 0.46 D, planks, entrance holes + landing strip, top bar with bars, wire knot | bottom of the box | upright; the HAND HOLDS THE TOP BAR (hive hangs below the hand). Anchors `hive_c_*`, `hive_top_*` (roof), `hive_bottom_*`. Standalone `tophive_svg(uid, roof)`; the wire runs through the top bar centre |
| `hivebox` | the EMPTY hive box: open trough, dark hollow, top bars laid across, rope handle | bottom | same anchors, no roof |
| `wirecoil` | a coil of fencing wire hanging on the forearm, a loose end | loose end | anchor `wire_end_*` |
| `torch14` | wooden stick, rag bundle bound with wire, flickering 3-layer flame (always upright) with a soft glow disc | flame | follows `angle`; anchor `flame_*`; `t` animates. `torch_svg(uid, t)` |
| `pot14` | battered aluminium pot, two ear handles; the hand grips the near ear, the pot hangs to the body side, upright | pot centre | anchors `pot_c_*`, `pot_face_*` (hit point). `pot_svg` |
| `spoon14` | long wooden spoon | bowl end | follows `angle`; anchor `spoon_*` (bowl). `spoon_svg` |
| `stick14` | the uncle's walking stick, crook handle, dark ferrule | ferrule | follows `angle` (80 = planted); anchor `stick_tip_*`. `stick_svg` |

## Elephants: flat 2D puppets (`puppet.figure(cast, pose, uid)`)
Same ink (`#3a2832` rim, 0.03 D), flat fill plus one lower-right crescent like the heads, hide colours with a lavender shade, pink cheeks, big glinting eyes. No injury, no lip-sync. Casts: `matriarch` (big, long tusks, wrinkled), `elephant_b` (cow, short tusks), `elephant_c` (young bull, torn ear, medium tusks), `elephant_d` (small, lilac, tusklets), `calf` (no tusks, big head, tuft of hair, 0.36). They are NOT in `puppet.CAST` (figure(), resolve_pose(), lerp_pose() are wrapped); the names are in `cast14.ELEPHANTS`; specs in `cast14.SPEC14`.
Side view faces screen-right; `mirror=True` for left. Origin = head centre, `feet_y` = distance to the soles, `anchors["feet"]` = middle of the four feet.

| pose key | range (default) | effect |
|---|---|---|
| `view` | "side" / "front" ("side") | two drawings. Front = head-on: two pillar legs, barrel, huge head, two fan ears |
| `phase`, `stride`, `gait` | 0..1, 0..1.6 (0), "walk" / "run" | four-beat lateral walk (stance 62 %): `cycle()` sets these; stride 0 = standing. run = longer, higher steps, body bob |
| `trunk` | hang / sniff / forward / reach / raised / curl / swing / tuck ("hang") | preset; `trunk_a0`, `trunk_a1` (deg, root and tip direction), `trunk_curl` -1.5..1.5 override. `raised` = trumpet pose (flared bell tip). The tip never goes below the ground |
| `ear_flare` | 0..1 (0) | ears from relaxed (hanging over the shoulder) to fully flared (side: swung forward, far ear peeks out and goes pink; front: spread wide) |
| `head_dip`, `head_tilt` | deg (0) | head down (+) / back (-) about the neck; tilt sways the trunk |
| `mouth_open` | 0..1 (0) | open red mouth under the trunk (trumpet) |
| `push`, `lean` | 0..1, deg | weight forward: body tilts about the rear hip, rear legs set back, front legs forward. Anchor `chest_push` = the point that touches the wire |
| `expr` | calm / happy / curious / alarmed / trumpet / shut / grumpy ("calm") | eye, lid, brow, mouth line; `blink` 0/1/2 |
| `tail` | -1..1 | tail swing (`t` adds a sway) |
| `head_turn` | -1..1 | front view: slides the face and the trunk sideways (a fake turn) |
| `crouch`, `squash`, `dust`, `t`, `tint`, `ink`, `mirror` | | as for the people; `dust` 0..1 = red laterite on the feet |

Anchors: the standard puppet names plus `trunk_tip`, `trunk_base`, `tusk_tip`, `chest`, `chest_push`, `shoulder_top`, `rump`, `tail_tip`, `belly`, `ear_tip` (`hand_r` = trunk tip, `hand_l` = trunk base).
**Canvases** (feet-relative, D): `CANVAS14[cast]` = side view, symmetric so it fits both facings and every trunk / flare / phase / push combination (matriarch +-11.3 D wide, 9.3 D up; wide because the trunk can reach 9 D forward); `CANVAS14_FRONT[cast]` for the front view (ears spread); the test checks the whole envelope. Use px_per_D 96..128 for wide shots.
`cycle(cast, phase, mode, facing, base, arms, speed)`: people as cast6 (`walk` 28 frames, `run` 16); elephants: `walk` about 48 frames per cycle, `run` about 28, facing -1 sets `mirror`. `cycle_distance(cast, mode, speed)` = D the elephant body moves per cycle with no foot slip (matriarch walk: 3.4 D).

**Close shot of the gag:** `uncle_stung_close` (head and shoulders, hive in the raised hand, cross-eyed, watering eyes, sweat drop, `nose_swell` 1.0, `limb_w` 0.058). Sprite canvas `CANVAS14_CLOSE["uncle14"]` = (-2.19, -4.0, 2.5, -0.5), px_per_D 384-512. It has `stool=0` (the set's stool is below the frame). Lead into it with `uncle_stung_start` (nose_swell 0.3) and animate `nose_swell` 0 to 1 with an ease-out.

## Bees and the swarm
`bee`: a small gold-and-black card facing +x, 0.20 D long by default (about 8 x life size so it reads at phone size); pose keys `size` (D), `angle`, `t` (wing beat 0..1 loop; blurred ghost wings while flying, `blur` 0..1), `rest` 1 (wings folded, eye closed: the sleeping bees), `mirror`. Anchor `stinger`. Canvas `CANVAS14["bee"]` (1 D square; scale `size` up only with a bigger canvas).
`swarm` (card) and `swarm_svg(uid, n, radius, shape, seed, t, size, ang, length, ink, tint, trails) -> (svg, bbox)`: n bees (1..400), shape `cloud` / `column` (rising from (0, 0), height `length`) / `stream` (a streak along `ang`, the burst from a hive) / `ring`; each bee has its own wing phase, tilt, size +-25 %, optional thin flight trails. Pose keys n, radius, shape, seed, t, size, angle, length. Canvas `CANVAS14["swarm"]`.

## Story poses: `cast14.STORY14[name] = (cast, pose)` (also merged into `puppet.STORY`), notes in `STORY14_META[name]["note"]`
Mouths move only in the two poses flagged `STORY14_META[name]["lipsync"] = True` (`cast14.LIPSYNC14`): `uncle_point_mock` (QUOTE 15.4-22.0) and `uncle_shout_torch` (QUOTE 39.0-40.8): drive `mouth = talk_mouth(g)` during the quote, "flat" outside. Every other pose holds a fixed mouth (villagers laugh and shout with held mouths: no lip-sync).

| name | cast | note |
|---|---|---|
| `bee_fly` | bee | one bee card (size 0.20 D by default: drawn big on purpose), wings beat with t (blurred ghost wings); pose keys size, angle, t, rest, blur, mirror |
| `bee_rest` | bee | a sleeping bee: wings folded, eye closed (the false-calm beat) |
| `calf_ears_flared` | calf | FRONT view, ears fully flared, alarmed face (hold or blend with _turn) |
| `calf_flee` | calf | flees: run gait (phase / 28), trunk up, ears flared, eyes wide, tail up; faces screen-right: use mirror=True when fleeing to the left |
| `calf_front_calm` | calf | FRONT view, calm: arriving at the fence, facing the camera |
| `calf_stand` | calf | standing, relaxed ears, trunk hanging (side view, faces screen-right; mirror=True for left) |
| `calf_trumpet` | calf | trunk up trumpeting (open mouth, bell tip), ears flared, head back; animate t for the sway |
| `calf_turn` | calf | FRONT view, head turned away (head_turn 0.8 = slides the face and trunk), ears half flared: the start of turning to flee; head_turn -1..1 |
| `calf_walk` | calf | one frame (phase 0.10) of cycle('calf', ...): four-beat walk, trunk sniffing; animate phase = frame / 48; ground speed cycle_distance() |
| `elephant_b_ears_flared` | elephant_b | FRONT view, ears fully flared, alarmed face (hold or blend with _turn) |
| `elephant_b_flee` | elephant_b | flees: run gait (phase / 28), trunk up, ears flared, eyes wide, tail up; faces screen-right: use mirror=True when fleeing to the left |
| `elephant_b_front_calm` | elephant_b | FRONT view, calm: arriving at the fence, facing the camera |
| `elephant_b_stand` | elephant_b | standing, relaxed ears, trunk hanging (side view, faces screen-right; mirror=True for left) |
| `elephant_b_trumpet` | elephant_b | trunk up trumpeting (open mouth, bell tip), ears flared, head back; animate t for the sway |
| `elephant_b_turn` | elephant_b | FRONT view, head turned away (head_turn 0.8 = slides the face and trunk), ears half flared: the start of turning to flee; head_turn -1..1 |
| `elephant_b_walk` | elephant_b | one frame (phase 0.10) of cycle('elephant_b', ...): four-beat walk, trunk sniffing; animate phase = frame / 48; ground speed cycle_distance() |
| `elephant_c_ears_flared` | elephant_c | FRONT view, ears fully flared, alarmed face (hold or blend with _turn) |
| `elephant_c_flee` | elephant_c | flees: run gait (phase / 28), trunk up, ears flared, eyes wide, tail up; faces screen-right: use mirror=True when fleeing to the left |
| `elephant_c_front_calm` | elephant_c | FRONT view, calm: arriving at the fence, facing the camera |
| `elephant_c_stand` | elephant_c | standing, relaxed ears, trunk hanging (side view, faces screen-right; mirror=True for left) |
| `elephant_c_trumpet` | elephant_c | trunk up trumpeting (open mouth, bell tip), ears flared, head back; animate t for the sway |
| `elephant_c_turn` | elephant_c | FRONT view, head turned away (head_turn 0.8 = slides the face and trunk), ears half flared: the start of turning to flee; head_turn -1..1 |
| `elephant_c_walk` | elephant_c | one frame (phase 0.10) of cycle('elephant_c', ...): four-beat walk, trunk sniffing; animate phase = frame / 48; ground speed cycle_distance() |
| `elephant_d_ears_flared` | elephant_d | FRONT view, ears fully flared, alarmed face (hold or blend with _turn) |
| `elephant_d_flee` | elephant_d | flees: run gait (phase / 28), trunk up, ears flared, eyes wide, tail up; faces screen-right: use mirror=True when fleeing to the left |
| `elephant_d_front_calm` | elephant_d | FRONT view, calm: arriving at the fence, facing the camera |
| `elephant_d_stand` | elephant_d | standing, relaxed ears, trunk hanging (side view, faces screen-right; mirror=True for left) |
| `elephant_d_trumpet` | elephant_d | trunk up trumpeting (open mouth, bell tip), ears flared, head back; animate t for the sway |
| `elephant_d_turn` | elephant_d | FRONT view, head turned away (head_turn 0.8 = slides the face and trunk), ears half flared: the start of turning to flee; head_turn -1..1 |
| `elephant_d_walk` | elephant_d | one frame (phase 0.10) of cycle('elephant_d', ...): four-beat walk, trunk sniffing; animate phase = frame / 48; ground speed cycle_distance() |
| `farmer_boast` | farmer14 | the hook: he points at his hive and says the bees will chase off the herd (screen-right; no lip-sync) |
| `farmer_calm_smile` | farmer14 | calm smile while the village laughs; a hammer hanging in one hand, the other on the hip |
| `farmer_hammer_post` | farmer14 | hammering a hive hook / post (screen-right); animate arm_r hand (0.78, -0.30) -> (0.70, 0.05) and prop angle -40 -> 15 |
| `farmer_hang_hive` | farmer14 | hanging a hive on the wire: both arms reach up, the top-bar hive (prop tophive, anchor hive_top_r = roof, hive_c_r) at head height on the screen-right |
| `farmer_proud` | farmer14 | standing proud by his fence: chest out, head up, arms akimbo |
| `farmer_tie_wire` | farmer14 | tying the wire: a coil of wire on the left forearm (anchor wire_end_l), the right hand twisting the wire out in front (screen-right) |
| `farmer_walk` | farmer14 | one frame (phase 0.30) of cycle(); animate cycle('farmer14', frame / 28, 'walk', facing, base, arms) |
| `farmer_watch_night` | farmer14 | watches the herd come to the fence at night, a little nervous (screen-right) |
| `matriarch_ears_flared` | matriarch | FRONT view, ears fully flared, alarmed face (hold or blend with _turn) |
| `matriarch_flee` | matriarch | flees: run gait (phase / 28), trunk up, ears flared, eyes wide, tail up; faces screen-right: use mirror=True when fleeing to the left |
| `matriarch_front_calm` | matriarch | FRONT view, calm: arriving at the fence, facing the camera |
| `matriarch_push` | matriarch | pushes the wire with her chest: weight forward, rear legs back, head down; anchor chest_push = the point that touches the wire; push 0..1 |
| `matriarch_sniff_fence` | matriarch | stands at the fence and sniffs the wire: curious face, trunk reaching low |
| `matriarch_stand` | matriarch | standing, relaxed ears, trunk hanging (side view, faces screen-right; mirror=True for left) |
| `matriarch_swatted` | matriarch | the bee burst: startled, trunk curled up and in, ears flared (comic, no injury) |
| `matriarch_trumpet` | matriarch | trunk up trumpeting (open mouth, bell tip), ears flared, head back; animate t for the sway |
| `matriarch_turn` | matriarch | FRONT view, head turned away (head_turn 0.8 = slides the face and trunk), ears half flared: the start of turning to flee; head_turn -1..1 |
| `matriarch_walk` | matriarch | one frame (phase 0.10) of cycle('matriarch', ...): four-beat walk, trunk sniffing; animate phase = frame / 48; ground speed cycle_distance() |
| `matriarch_walk_to_fence` | matriarch | the matriarch walks straight to the fence: calm walk, head forward |
| `swarm_burst` | swarm | the burst of bees streaming out of a hive toward the elephant's eyes (stream along angle) |
| `swarm_cloud` | swarm | swarm helper: pose keys n, radius, shape (cloud / column / stream / ring), seed, t, size, angle, length; also swarm_svg() |
| `swarm_column` | swarm | a rising column of bees from a hive entrance (base at (0, 0), card origin at the feet) |
| `uncle_arms_akimbo` | uncle14 | smug, arms akimbo (the end of the mocking, and 'See?' beats) |
| `uncle_ask_sheepish` | uncle14 | the next morning, asking sheepishly for hives: an EMPTY hive box in one hand (prop hivebox), scratching the back of his head |
| `uncle_laugh_big` | uncle14 | belly laugh at the bee guy: head back, hands on the belly, tears (held open mouth, no lip-sync) |
| `uncle_look_field` | uncle14 | looks at his trampled field, hand on his cap, mouth open (held, not lip-sync) |
| `uncle_point_mock` | uncle14 | QUOTE 15.4-22.0: pointing and mocking (screen-right, mirror=True for left); LIP-SYNC mouth=talk_mouth(g) during the quote, 'flat' otherwise |
| `uncle_shout_torch` | uncle14 | QUOTE 39.0-40.8 at night: shouting 'See? The elephants aren't scared at all!' with a torch held high (animate t for the flame), LIP-SYNC |
| `uncle_stick_idle` | uncle14 | leaning on his walking stick (anchor stick_tip_r on the ground) |
| `uncle_stool_hang` | uncle14 | standing on a stool (stool=1 draws it; CANVAS14_STOOL), hanging his first hive; pair with uncle_stung_nose. The set may carry its own stool: set stool |
| `uncle_stung_nose` | uncle14 | THE GAG: stung on the nose, a shiny swollen trunk-like nose (pose key nose_swell 0..1; animate 0 -> 1 over ~20 frames with an ease-out, `t` sways the  |
| `uncle_stung_start` | uncle14 | the instant of the sting (nose_swell 0.3); blend into uncle_stung_nose |
| `uncle_walk` | uncle14 | one frame (phase 0.30) of cycle('uncle14', ...) with the walking stick in the right hand |
| `villager_kid_bang_pot` | kid14 | the kid bangs a small pot; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_kid_laugh_point` | kid14 | the kid points and laughs (screen-right); mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_oldman_laugh` | oldman14 | the old man cackles, leaning on his stick; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_oldman_wave_torch` | oldman14 | the old man waves a torch; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_woman_bang_pot` | woman14 | bangs a pot with a wooden spoon (spoon_r hits pot_face_l); animate arm_r hand (0.55, 0.32) <-> (0.30, 0.55); mouths here are held shapes (NOT lip-sync |
| `villager_woman_laugh` | woman14 | the woman with the headwrap laughs at the bee guy (hands on cheeks / belly, tears); mouths here are held shapes (NOT lip-sync: only the uncle's quotes |
| `villager_woman_wave_torch` | woman14 | waves a torch (pivot beat); animate t for the flame; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_youth_bang_pot` | youth14 | the youth bangs a pot; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_youth_point_laugh` | youth14 | the youth points and laughs (calls him ไอ้บ้าผึ้ง); mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |
| `villager_youth_wave_torch` | youth14 | the youth waves a torch and yells at the elephants; mouths here are held shapes (NOT lip-sync: only the uncle's quotes are) |

## Files and QA
- `cast14.py` the module; `sheet14.py` builds the sheet; `test_cast14.py`:
  - `python3 test_cast14.py` = unchanged + stories + sheet.jpg (temp files only in `cast14/tmp/`, deleted afterwards is fine)
  - `unchanged`: every earlier CAST member (4 poses each) and every earlier STORY pose, with and without cast14 (two processes), byte compare: 0 differ
  - `stories`: every STORY14 pose renders, deterministic, finite bbox / anchors, inside its canvas; elephant envelope (5 casts x 8 trunk presets x flare x 4 phases x walk/run x mirror x side/front) inside the canvas
  - `sheet`: `sheet.jpg` = scale row, every people pose, every elephant pose, walk strips, bees / swarms / props, faces (nose_swell 0..1, uncle mouths, village faces, elephant expressions)
- Verified through `stage/sprites.render_sprites` (matriarch, bee render; uncle with stool needs `CANVAS14_STOOL`).

## Known weak spots
- Elephants are two flat views only (side, front); the "turn" is a front view with `head_turn` (features slide), there is no 3/4 view. Cut from side to front behind a dust or bee moment.
- The `push` pose reads as weight forward + head down; the contact with the wire is the set's job (anchor `chest_push`).
- Trunk tips of `sniff` / `reach` are plain tapered tubes (no finger lobe).
- People keep the series' white heads; skin tone is carried by hair, hats and costume only.
