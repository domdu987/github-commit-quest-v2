# cast5.py: the cast of film 5 ("the bird boy", a British coal mine, early 1900s) for the v2 puppet

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj/v3/cast5/cast5.py`
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast4` is edited. On import, cast5 imports cast4 (which imports cast3, cast2, cast_ext and v2/puppet), adds entries to their tables and wraps puppet helpers on top of cast4's wrappers: `_norm` (reads this module's pose keys), `_face` (soot, sideburns, cough puffs), `_prop` (new props) and `figure` / `resolve_pose` / `lerp_pose` (the creature figures). Each wrapper falls through, so every earlier member draws as before.

```python
import sys
sys.path.insert(0, ".../v3/cast5")
import cast5                 # registers on import (idempotent)
import puppet                # same module object: CAST now also has alfie, gaffer, miner1, miner2, miner3
cast, pose = cast5.STORY5["alfie_hold_cage"]
f = puppet.figure(cast, pose, "al")                              # the cage + singing canary in his hand
b = puppet.figure("canary", cast5.CANARY5["fallen"], "cn")       # the canary alone (a creature, not a person)
c = puppet.figure("canary_in_cage", dict(state="perch_sing", notes=5), "cc")
```

Import `cast5` BEFORE `sprites` / `stage.sprites` when you can (cast_ext's import hook copies the canvases either way).
Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged to the five people (pose keys, expressions, `blink`, effects, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`).

## Cast (same head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | height head top to soles (hat top) | look |
|---|---|---|---|
| `alfie` | `boy` (cast2), torso 0.66 x 0.80, legs 0.82 | **2.48 D** (2.61) = 0.77 of the mean adult (3.23) | ginger hair, oversized slate tweed **flat cloth cap** (cast3 flatnews, puff 1.3), **soot smudges on the cheeks** (+ a finger wipe and a forehead smudge). **Oversized brick-red waistcoat** hanging open (lowered hem, lapels, brass buttons, two sewn **patches**: blue and tan with stitching) over a **collarless cream shirt** (neck band, two-button placket), brown **braces** showing in the gap, **rolled sleeves**, leather belt with a buckle, a **small brass oil lamp hanging on the belt** at the hip (lit, tiny flame), dark **short trousers** (bare shins), **big soft boots** |
| `gaffer` | `stout`, round torso 1.24 x 1.14, legs 1.30 | 3.31 D (3.67) | **hard tan leather pit helmet**: tall dome with a raised comb, stitched band, narrow brim, **brass lamp bracket** (plate + hook) on the front; **bushy brown sideburns** and a thick walrus moustache, heavy brows, ruddy cheeks, light soot. **Long navy coat hanging open** (wide lapels, brass buttons, flap pockets, skirt to the knee) over an **ox-blood waistcoat** with a brass watch chain, grey collarless shirt, mustard neckerchief, full coat sleeves, black boots |
| `miner1` | `slim` athletic 0.66 x 1.04, legs 1.42 (tall) | 3.32 D (3.47) | navy knitted cap with a rolled cuff (cast2 skullcap), **heavy soot**, slate-grey collarless shirt, rolled sleeves, braces, belt, charcoal trousers. Prop: pick-axe |
| `miner2` | `regular` 0.94 x 0.98, legs 1.06 (short, stocky) | 2.90 D (3.01) | **red spotted kerchief** tied over the head (knot + tails on the far side), **full dark-brown beard** and bushy moustache, cream shirt with rolled sleeves under a **brown leather jerkin**, belt. Prop: shovel |
| `miner3` | `slim` 0.58 x 1.06, legs 1.46 (lanky, young) | 3.38 D (3.47) | sandy hair, freckles, **flat cap worn back to front** (the peak sticks out behind on the side away from the face), oatmeal shirt, green braces, **red neckerchief**, brown trousers, a smirk |

Distinctness against the references (ref a t0010: blue robe, crossed white collar, yellow belt, striped topknot cap with a pin; ref b t0030: black bowler, grey hair, yellow waistcoat with gold chain): no member wears a bowler, a yellow waistcoat or a robe; the gaffer's hat is a tan leather helmet with a comb and a lamp bracket, his waistcoat ox-blood under a navy coat. Against film 3 (tommy: brown cap, grey-blue jacket, red scarf; foreman: brown derby, brown waistcoat, white sleeves): alfie is ginger, brick-red waistcoat, slate cap, short trousers; the gaffer has sideburns, helmet and coat. Silhouettes: small boy / barrel with helmet / tall beanie / short bearded kerchief / lanky backwards cap. `lineup.png` shows them side by side (tunnel colours).

### New CAST keys (only `_cast5` members use them)
- `soot=dict(color, op, spots)`: soft soot smudges on the face, clipped to the head, drawn under the features. `spots` = `"boy"` (cheek smudge, finger wipe, forehead), `"heavy"`, `"light"` (tables `SOOT_SPOTS`, `SOOT_STREAKS`, positioned from the eyes and mouth, so they follow yaw / pitch / roll).
- `sideburns=dict(color, dark)`: bushy sideburns from the hat to the jaw on both sides; the side the face turns toward narrows.
- Costume `pit`: colours `base` (= shirt), `shirt_d`, optional `susp`/`susp_b` (braces, `susp_x`), optional `vest`/`vest_d`/`button` (waistcoat, gap `vest_gap`, hem drop `vest_hem`, `patches` = ((x, y, w, h, colour, deg), ...)), `belt`/`buckle`, optional `kerchief`/`kerchief_d` (`knot_x`), `pants`; `belt_lamp=True` hangs the small oil lamp at the hip. Costume `gaffercoat`: `base` (= coat), `dark`, `lapel`, `vest`, `vest_d`, `shirt`, `brass`, `kerchief`, `kerchief_d`, `pants`, `coat_len`, `coat_flare`.
- Hats (`hat="newsboy"` + `hat_style`): `leatherhelmet` (colours light/base/dark/shine/brim/brim_l/stitch/brass), `capback` (light/base/dark/shine/visor), `kerchief` (light/base/dark/dot).
- Earlier keys reused: cast3 `sleeve` (rolled), `beard` (miner2 has `_cast3=True`), `moustache_style="bushy"`; cast2 `boots`; cast4 `shorts` (alfie has `_cast4=True`).

## New pose keys (people)

| key | range | effect |
|---|---|---|
| `flame` | 0 .. 2 (default 1) | flame of a held `flame_lamp` (and the belt / held oil lamp): 0 = out (an ember), 1 = normal, 2 = burning bright and tall; the warm glow halo grows with it |
| `flame_blue` | 0 .. 1 | the flame turns pale blue and grows the blue **firedamp cap** above it (gas!) |
| `bird` | canary pose dict or state name | the canary inside a held `cage` (all canary keys below, incl. `swing` = cage swing in degrees about the ring) |
| `cough` | phase 0..1 (or True) | three dust puffs drifting out of the mouth toward the facing side (animate the phase) |
| `t` | float | as before; also flickers the flames and bobs the music notes |

Like cast3's `cigar`, these keys are read from the pose dict at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses (the stage passes pose dicts through unchanged).

## The canary (creature figures, not people)

`puppet.figure("canary", pose, uid)` and `puppet.figure("canary_in_cage", pose, uid)` return the usual dict (`svg`, `feet_y`, `bbox`, `anchors`) and work with the stage (`actors.Actor("bird", "canary_in_cage")`, sprites, head_flip). Scale: the same D as the people (bird body ~0.20 D, cage 0.75 D tall, as big as alfie's torso). For the ECU inserts render the sprites at a high px per D (e.g. `render_sprites(1200)`) or pass `scale` (0.3..4).

Canary pose keys (all optional, garbage falls back to the state's value, never raises):

| key | range | meaning |
|---|---|---|
| `state` | `perch_sing`, `perch_quiet`, `droop`, `fallen`, `revive`, `sing_one` | sets the defaults of the keys below |
| `notes` | 0..5 (rounded) | music notes floating up from the beak (long song 5, then 3, then 1) |
| `beak` | 0..1 | beak open |
| `eyes` | 0..1 | 0 = gently closed (a soft curved lid line, **never X eyes**), 0.5 = half lid, 1 = open with a highlight; `revive`: animate 0 -> 1 |
| `droop` | 0..1 | head sinks, tail and wing hang |
| `ruffle` | 0..1 | ruffled feather tufts |
| `lie` | 0..1 | 0 on the perch, 1 slumped on the floor (belly down, head resting on the floor, legs tucked). In the cage the bird falls from the perch to the cage floor as `lie` goes 0 -> 1 (animate it for the drop) |
| `breath` | 0..1 | chest pump amplitude (3 pumps per unit of `t`, for the reveal's breathing comparison) |
| `t` | float | note bobbing / breathing phase |
| `swing` | -40..40 deg | (cage) swing about the ring |
| `scale`, `mirror`, `tint`, `ink` | | as for people (mirror: faces screen-left) |

States: `perch_sing` (beak open, notes 3; `CANARY5["perch_sing"]` has 5), `perch_quiet` (beak closed), `droop` (eyes 0.38, ruffled, drooping), `fallen` (on the floor, eyes closed), `revive` (half risen, eyes 0.55), `sing_one` (one note, slightly ruffled). `cast5.CANARY5[state]` = ready poses; `cast5.STATES` = their numbers.

Anchors: `feet` (perch / floor point; the cage: base bottom), `hip`, `head` (= `bird_head`), `head_top`, `hat_top`, `chest`, `mouth` (= `beak`, the beak tip), `eye`, `bird_body`, `bird_feet`; the cage adds `ring` (0, 0) = the handle (= `hand_r` / `hand_l`, pin a hand here), `perch`, `cage_floor`, `cage_bottom`, `cage_top`. Standalone canary: origin 0.10 D above the feet line. Cage: origin = ring top, `feet_y` = 0.748 (x cos swing).

`puppet.resolve_pose` / `lerp_pose` accept the creature names (numbers interpolate, `state` and `mirror` switch at t = 0.5).

Standalone pieces (SVG fragments in D units):
- `cast5.cage_svg(state="perch_quiet", uid, ink, tint, **keys)` -> `(svg, anchors)`: the cage with the bird inside, ring top at (0, 0), base bottom at (0, 0.748). `state` may be a full pose dict; keyword keys override.
- `cast5.flame_lamp_svg(uid, flame=1, blue=0, t=0, ink, tint)`: the safety lamp alone for the lamp inserts, ring at (0, 0), bottom at 0.52, flame base at `FLAME_IN` (0, 0.392).
- `cast5.bench_svg(uid, width=1.1, height=0.42)`: a rough bench, top surface at y = 0, legs to y = height (for the oxygen ending).

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` (from the hand) | orientation |
|---|---|---|---|
| `flame_lamp` | Clanny-type flame safety lamp hanging from its ring: brass bonnet, wire-gauze chimney, three pillars, glass with the flame, oil vessel, glow (pose keys `flame`, `flame_blue`); 0.52 D tall (the gaffer's poses use `scale` 1.25) | the flame, 0.34 below | always upright |
| `oil_lamp_small` | little brass "teapot" lamp on a hook, small flame on the spout | spout flame (0.10, 0.04) | always upright |
| `pickaxe` | ash handle (gripped 0.22 from its butt), curved iron head with a point and a chisel end | head centre, 0.80 | follows `angle` |
| `shovel` | shaft with a D-grip, iron socket, rounded steel blade | blade edge, 0.92 | follows `angle` |
| `oxygen_box` | small riveted brass box with a glass window (blue bottle), a dial, a valve wheel and a red rubber tube to a brass nozzle; held by its left handle | nozzle end `OXY_TIP` (+0.606, -0.240) | always upright (mirror the figure for screen-left) |
| `cage` | the brass birdcage with the canary inside (pose key `bird`), hung by its ring from the fist | base bottom, 0.748 below; `hand_for_tip("cage", (x, feet_y), 90)` stands it on the floor | upright, `bird.swing` swings it |

## STORY5 (`cast5.STORY5[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast5.STORY5_META[name]`

| name | cast | what |
|---|---|---|
| `alfie_hold_cage` | alfie | the cage raised beside his face (screen-right hand), bird singing (3 notes), happy, other fist on the hip |
| `alfie_listen` | alfie | ear tilted toward the cage held up close, eyes half shut, worried |
| `alfie_shout_run` | alfie | step, shouting "run!", pointing to the exit (screen-right), the cage swinging back in the other hand (bird fallen) |
| `alfie_run_cage` | alfie | sprint to screen-right, cage held out in front (animate `bird.swing`; alternate the stride) |
| `alfie_worried`, `alfie_determined` | alfie | hands wrung + sweat / wide stance, fist on hip |
| `alfie_revive` | alfie | kneeling, oxygen box in both hands, nozzle = `prop_tip_r`. Meta: stand `canary_in_cage` (`revive`, then `sing_one`) on `bench_svg` so its `beak` anchor is 0.07 D right of `prop_tip_r` (poses.png does exactly this) |
| `gaffer_laugh` | gaffer | eyes shut, mouth wide, tears, hand on belly, lamp hanging from the other hand |
| `gaffer_lift_lamp` | gaffer | lamp raised high beside the head (flame 1.6, bright), the other hand pointing across at it, smug |
| `gaffer_smug` | gaffer | fist on hip, lamp at his side |
| `gaffer_arms_crossed` | gaffer | arms crossed, smug |
| `gaffer_shout` | gaffer | angry, pointing out, mouth open, lamp in the other hand |
| `gaffer_shocked` | gaffer | both hands up, the lamp flaring blue (flame 1.8, flame_blue 0.8) |
| `gaffer_run` | gaffer | running to screen-right, lamp swinging in the front hand |
| `miners_laugh` (+`_miner2`, `_miner3`) | miner1/2/3 | pointing and laughing, tears |
| `miners_mock` (+...) | | both hands cupped at the mouth, smug, mouth open |
| `miners_run` (+...) | | running scared to screen-right, arms up, sweat |
| `miners_push` (+...) | | leaning into a coal tub on screen-right, open hands 0.75-0.85 D in front at hip height (tub = set dressing) |
| `miners_cough` (+...) | | hunched, hand at the mouth, half-shut eyes, `cough` puffs |
| `miners_work` / `_miner2` / `_miner3` | | miner1 pick-axe wind-up (meta `strike` = the blow), miner2 digging with the shovel, miner3 pick lowered |

32 poses (7 alfie, 7 gaffer, 18 miners).

## With the v3 stage

As in `v3/cast4/API.md`. See `stage_test.py` (alfie_hold_cage + gaffer_lift_lamp as actors, key from screen-right, `head_flip` on, Cycles 360x640, 2 threads, 2.6 s wall). The canary is an actor like anyone else: `actors.Actor("bird", "canary_in_cage").build(sprites.DEFAULT_CANVAS["canary_in_cage"], ...)`.

Canvases (feet-relative, added through `cast_ext.CANVAS`, in D):

| member | canvas |
|---|---|
| alfie | (-1.875, -3.875, 1.875, 0.1875) |
| gaffer | (-2.125, -4.75, 2.125, 0.125) |
| miner1 | (-1.9375, -4.875, 1.9375, 0.125) |
| miner2 | (-2.0, -4.3125, 2.0, 0.125) |
| miner3 | (-1.9375, -4.9375, 1.9375, 0.125) |
| canary | (-0.75, -1.125, 0.75, 0.125) |
| canary_in_cage | (-1.0625, -1.3125, 1.0625, 0.25) |

People: every arm preset with every film-5 prop at yaw +-0.6 (and mirrored), flame 2, cage swing +-40 with 5 notes, squash 0.8-1.15, crouch, wide legs, all effects + cough and every STORY5 pose, with 0.33-0.37 D head room. Creatures: every state, mirrored, swing +-40, lie 0/0.5/1, 5 notes, breath. Alfie's arm is 0.62 D: pass `"stretch": 1.3` for reaches.

## Files and QA

- `cast5.py`: the module. `test_cast5.py`: `lineup` (lineup.png, people front and 3/4, head D 120 px), `canary` (canary.png: every state alone at 620 px/D, in the cage, and in the cage mirrored + swinging), `poses` (poses.png: all 32 STORY5 poses; alfie_revive with the bench and cage), `canvas` (+ head_flip on STORY5 and the creatures), `creature` (creature sweeps / garbage / determinism / mirror / resolve / lerp, and the new people pose keys with garbage), `robust` (v2 `test_puppet.py --quick` on the five people).
- `stage_test.py` -> `stage_test.png` (sprites and frames in `tmp_stage/`).
- Results of the last run: see `run_all.log`.

## Known limits

- Coat and waistcoat hems are fixed to the torso (as in cast2-4): in deep crouches and the kneel the legs come out under them.
- The canary is drawn in profile only (facing +x; `mirror` faces left); no three-quarter view. In the cage the front bars are drawn over the bird on purpose (it reads "inside"), so at small sizes the bird is partly covered: use the ECU at >= 600 px/D.
- `lie` between 0 and 1 in the cage is the fall from the perch (the bird hangs in the air mid-way): animate it over a few frames, do not hold it.
- In `gaffer_lift_lamp` the pointing hand crosses the chest under the lamp arm (the stout reach is 0.96 D): the gesture reads, the finger tip is partly hidden.
- Held lamps / cage / oxygen box always hang upright; the cage swings only through `bird.swing`.
- The new pose keys are not carried through `resolve_pose` / `lerp_pose` for people.
