# cast22.py: the cast of film 22 ("ไอ้ช่างวงจร", Harry Beck's Underground diagram, London 1931-33) for the v2 puppet

File: `PROJ/v3/cast22/cast22.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast10` is edited. On import, cast22 imports cast10 (which chains cast9 .. cast_ext and v2/puppet), adds entries to their tables and wraps the puppet helpers on top of cast10's wrappers: `_norm` (this module's pose keys), `_face` (flushed red face, puffed cheeks), `_ink_limb` (knee socks), `_prop` (the new props) and `figure` (drafting board, desk, typewriter, pillar). Each wrapper falls through to the earlier ones, so every earlier member draws as before: `test_cast22.py identity` hashes every `puppet.STORY` pose and three poses of every older CAST member in a cast10-only subprocess and in a cast22 process: 531 SVGs, identical.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast22")
import cast22                      # registers on import (idempotent); import it BEFORE sprites / stage.sprites
import puppet                      # same module object: CAST now also has the 10 members + 16 crowd variants below
cast, pose = cast22.STORY22["off_stamp"]
f = puppet.figure(cast, pose, "f")                                              # f["anchors"]["stamp_r"] = the stamping face
p = dict(cast22.STORY22["off_wave_sheet"][1], mouth=cast22.talk_mouth(g, 1.0), blink=cast22.blink_at(g, 90))
w = puppet.figure("beck", cast22.walk_carry_roll(g / 28.0), "f")               # the walk with the roll under his arm
name, pose = cast22.crowd_member(i, "pass_walk")                                # person i of the crowd, never cloned
a = actors.Actor("off", "official"); a.build(sprites.DEFAULT_CANVAS["official"], sprite_dir, contact=True)
```

Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged: pose keys, the 21 expressions (incl. cast10's `squint`), `mouth` incl. `("open", w, h)`, `blink`, `gaze`, the fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`. Re-exported from cast6: `cycle(cast, phase, mode, facing, base, arms, speed)` (modes walk / run / sneak / march), `talk_mouth`, `blink_at`, `NOD`.

## Cast (head D = 1, the same head, ink weight and proportions as cast10; 1930s London)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `beck` | `slim` 0.60 x 1.00, legs 1.26 | 3.12 (3.19) | Harry Beck: neat dark **side-parted hair** (parting on the screen-left, swept fringe), **round wire glasses**, clean-shaven, white shirt with **rolled sleeves** (rolled cuff) and **black sleeve garters**, dark grey **waistcoat**, the **red tie**, grey trousers, a yellow **pencil behind the ear** (on the side away from where he looks) |
| `official` | `stout` 1.26 x 1.10, legs 1.42 | 3.39 | the publicity official: **comb-over** (five ginger strands across a shiny bald crown, ginger tufts over the ears), huge ginger **handlebar moustache**, ruddy cheeks, double chin, **navy pinstripe three-piece** (cast7 frock/lounge suit with chalk pinstripes on coat, waistcoat and skirt), gold **watch chain**, **yellow bow tie**, red **carnation**; navy trousers |
| `clerk_a` | `slim` 0.55, lanky | 3.16 | thin young man: slicked dark hair under a **green eyeshade**, teal-striped shirt, mustard tie, pencils in the pocket, red **sleeve garters** |
| `clerk_b` | `slim` hourglass 0.54 | 2.92 (2.99) | the woman typist: 1930s **bob** with a straight fringe and a gold slide, **mustard cardigan** (button band, pockets) over a cream blouse with a Peter Pan collar and a red bow, belt, **teal A-line skirt** to mid-calf, red shoes |
| `clerk_c` | `stout` pear 1.08 | 2.95 (2.98) | chubby older man: **bald** with grey side tufts, **round spectacles**, age lines, cream shirt, **maroon knitted vest**, navy bow tie, brown trousers |
| `pass_man` | `regular` 0.86 | 3.18 (3.38) | passenger: **bowler hat** (brown hair under it, not white tufts), grey-blue **overcoat** with peaked lapels and watch chain, red waistcoat, pencil moustache |
| `pass_woman` | `slim` 0.58 | 2.94 (3.10) | passenger: red **cloche hat** (yellow ribbon band, white flower), **teal coat** with a tan collar and gold buttons, belt, mid-calf hem |
| `pass_child` | `boy` 0.62 x 0.78 | 2.44 (2.60) | child: bottle-green **school cap** (yellow piping, badge, short peak), red school jumper with yellow V-trim, green-and-yellow tie, grey **shorts** and cream **knee socks** (green band), freckles |
| `old_gent` | `regular` 0.80 | 3.00 (3.04) | elderly gentleman: **white beard**, white tufts, a **monocle** (gold, with chain), age lines, bottle-green frock coat, gold waistcoat, red cravat, watch chain |
| `porter` | `regular` pear 0.88 | 3.10 (3.36) | Underground staff: **navy tunic** (gold buttons, red patches, red-blue **roundel** on the chest), **peaked cap** with the red-blue roundel badge, moustache, yellow cuffs |

Crowd: `crowd22_00` .. `crowd22_15` are CAST entries too (6 men, 7 women, 3 children) with their own coats, hats (bowler in black / brown, fedora in tan / grey / blue-grey, cloche in 8 colours, school caps in 4), waistcoats, ties, hair and jumpers, and each carries the canvas of its base member. `cast22.crowd_member(i, pose="pass_walk", phase=None, mirror=False)` returns `(cast_name, pose)`:
- `pose="pass_walk"`: a walk-cycle frame (phase spread by `i` unless given) with props varied per person: men carry a briefcase / furled umbrella / folded daily newspaper / nothing, women a handbag / umbrella / nothing, children nothing.
- `pose=<STORY22 passenger pose name>`: that pose on a variant of the right kind (man, woman, child), so `crowd_member(i, "pass_tap_map")` taps a map in a different coat for every i.
- `pose=<dict>`: that pose on a variant of `pose["kind"]` (default `pass_man`).

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended; follow the forearm or `angle`, `scale`)

| type | drawing | `prop_tip_*` | notes |
|---|---|---|---|
| `ruler` | 0.92 D boxwood ruler with ticks | far end 0.70 | |
| `pen` | fountain pen: navy barrel, gold band, clip, gold nib | nib 0.36 | anchor `pen_r/_l`; use `scale` 1.4 on a drawing board |
| `set_square` | amber 45 degree set square with the cut-out and a "45" mark (legs along +x and -y from the grip) | 0.50 | |
| `t_square` | long blade 1.2 D with the dark crosshead | 1.10 | |
| `roll` | rolled drawing: white paper, red tie band, the spiral end with red / blue / green / yellow lines peeking out | end 0.42 | 0.84 D long, centred on the hand: lay it along an arm for "under the arm" |
| `sheet` | **big diagram sheet**: flat cream card 0.96 x 0.68 with a navy title band and a bright red / blue / green / yellow Beck diagram; held by its left edge | far edge 0.96 | waves with `angle` |
| `stamp` | red rubber stamp: turned knob, wood block, red rubber pad | pad 0.29 | face along +x; `angle` 90 stamps downward |
| `pocketmap` | **small folded pocket map**: cream cover, red-blue roundel, `UNDERGROUND` | 0.34 | |
| `pocketmap_open` | the map opened: navy header, 4 panels, a bright little diagram | 0.64 | |
| `fork` | fork with wooden handle; pose key `fork_map=1` spears a little folded map on the tines | tines 0.50 | |
| `knife` | table knife with a wooden handle | 0.50 | |
| `letter` | letter marked `NOTICE` (red band, text lines, red stamp mark) | 0.48 | |
| `circuit` | blue-print circuit sheet: white wires, yellow resistor / capacitor / lamp / solder dots | 0.84 | |
| `daily` | folded daily newspaper: black masthead `THE DAILY`, headline, photo box, columns | 0.54 | the old `newspaper` of cast7 shows the Mona Lisa: use this one |
| `briefcase` | brown leather case hanging from the hand by its handle | bottom 0.43 | always upright |
| `handbag` | red handbag hanging from the hand, gold clasp | bottom 0.39 | always upright |
| `umbrella` | furled black umbrella with a crook handle, strap, brass ferrule | 1.12 | follows the forearm or `angle` |
| `teacup` | cup with tea and steam (`t`), handle on the +x side | the hand | always upright |
| `magnifier` | magnifying glass: wooden handle, brass ring, glass with a glint | lens centre 0.47 | |
| `handtruck` | porter's two-wheeled sack truck carrying a `MAPS` crate with a roundel; hand at the top of the handle | wheel bottom `1.30 x scale` below the hand | upright; the crate is on the +x side; `scale` makes the wheel touch the floor (`porter_push_crate` computes it) |

Standalone pieces (SVG fragments in D units): `prop_svg(kind, uid, ink, tint)` (`kind` any prop, plus `"fork_map"`), `board_svg(uid)`.
Anchors set by the new props: `<type>_r` / `<type>_l` (for example `pen_r`, `stamp_r`, `pocketmap_l`).

## New pose keys (read at draw time; `resolve_pose` / `lerp_pose` drop them, so re-add them to tweened poses)

| key | range (default) | effect |
|---|---|---|
| `flush` | 0..1 (0) | the face goes red (laughing official: 1.0). Features stay readable on top |
| `puff` | 0..1 (0) | puffed cheeks: two round ruddy bulges beside the mouth (`off_buried_eat`) |
| `napkin` | 0 / 1 (0) | `official` only: a red-checked napkin tucked into the collar over the chest |
| `fork_map` | 0 / 1 (0) | a little map speared on the `fork` tines |
| `board` (+ `board_x`, `board_y`, `board_s`) | 0 / 1 (0) | draws the tilted **drafting board** with the diagram in progress BEHIND the figure on the facing side (x = head + `board_x` (0.25), y = `board_y` (0.55), scale `board_s`; mirrors with `mirror`). Anchor `board_c` |
| `desk` (+ `desk_x`, `desk_y`, `desk_w`, `desk_drawer`) | 0 / 1 (0) | an office **desk in front of the figure** (green leather top, drawer pedestal, brass handles) from `desk_y` (1.30) to the floor, `desk_w` wide (2.2), `desk_x` from the head (0.5); `desk_drawer` 1 pulls the top drawer open with papers. Anchor `desk_top`. Hands in the `front` layer sit above the top |
| `typewriter` (+ `tw_x`, `tw_y`) | 0 / 1 (0) | a typewriter BEHIND the hands (`tw_x` 0.40, `tw_y` 1.45) |
| `pillar` (+ `pillar_x`, `pillar_w`) | 0 / 1 (0) | a stone pillar IN FRONT of the figure on the screen-left side, its edge at `pillar_x` (-0.12) from the head, `pillar_w` wide (1.3): the figure peeks out (`off_peek`). Anchor `pillar_edge` |
| `t` | float | drives the teacup steam |
| `sweat` | 0..1 | cast7's sweat drops (works on every cast22 member) |

CAST keys added: hat styles `hair22` (CAST `hair22=dict(style="parted" / "comb" / "bald" / "bob" / "white", color, shine, pencil, strands, slide)`), `cloche22`, `schoolcap22`, `porter22` (cast10 peaked cap + the roundel badge), `bowler22` (cast_ext's bowler with hair-coloured side tufts); costumes `vest22` (shirt + waistcoat or knit vest; `vest_style`, `vest_v`, `neck` "tie" / "bow"), `woman22` (cardigan or coat, `coat=True`), `suit22` (frock7 + pinstripes + `napkin`), `porter22` (uniform7 + roundel); `socks22=dict(color, band)` knee socks on the legs. Existing keys reused: `glasses`, `monocle`, `beard`, `garters`, `moustache_style="handlebar"`, `cheeks`, `lashes`, `freckles`, `age_lines`, `chins`.

## STORY22 (`cast22.STORY22[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast22.STORY22_META[name]`

"lip-sync" = the pose accepts `mouth=talk_mouth(...)` during the speaker's quote (the poses with `STORY22_META[name]["lipsync"] = True`; the official's boss line is about 11.0-17.6 s and the false-payoff line about 31 s). Outside the quote set `mouth="flat"`. Only quoted speakers move mouths.

| name | cast | what |
|---|---|---|
| `beck_rule_line` | beck | leaning in over the **drafting board** (`board=1`), ruler laid on it in one hand, pen drawing along its edge in the other |
| `beck_set_square` | beck | 45 degree set square held up beside his face |
| `beck_hold_circuit` | beck | holds a circuit-diagram sheet beside him and studies it |
| `beck_thumb_push` | beck | pushes a station point along the board with his open hand, pen in the other |
| `beck_carry_roll` | beck | walk frame with the roll under his arm; animate `cast22.walk_carry_roll(phase)` (28 frames per cycle) |
| `beck_present_roll` | beck | lays the roll on a desk (`desk=1`), hopeful (happy eyes, small smile) |
| `beck_sag` | beck | shoulders down, head low, sad, walking away with the roll hanging; animate `cast22.walk_sag(phase)` |
| `beck_knock` | beck | knocking on a door (screen-right) with his fist, roll under the other arm |
| `beck_read_notice` | beck | reads the `NOTICE` letter in both hands, head bowed, sighing (mouth `o`) |
| `beck_proud` | beck | the ending: arms folded, chin up, small proud smile |
| `off_sit_glance` | official | at his desk (`desk=1`, legs bent behind it), glancing at the sheet, smug |
| `off_stamp` | official | red rubber stamp raised high (anchor `stamp_r` = the pad) |
| `off_laugh_back` | official | rocking back laughing, tears, **red face** (`flush=1`), hands on the belly. **lip-sync** (talk_b held; use `talk_mouth` in the quote) |
| `off_wave_sheet` | official | waves the diagram like a flag, talking. **lip-sync** (animate the prop angle -38 <-> -18) |
| `off_eat_mime` | official | holds the sheet to his open mouth as if biting, talking. **lip-sync** |
| `off_toss_drawer` | official | flicks the sheet into the open drawer of a desk (`desk=1`, `desk_drawer=1`, desk on the screen-right) |
| `off_smug_rub` | official | rubbing his hands, smug, talking. **lip-sync** |
| `off_peek` | official | peeks from behind a pillar (`pillar=1`), smirking, looking right |
| `off_jaw_drop` | official | shock: jaw dropped (held `open` mouth), ring eyes, sweat drops, hands open |
| `off_buried_eat` | official | the ending: napkin in the collar, knife and fork, a folded map speared on the fork, **puffed cheeks**, sweat, mouth shut |
| `off_sneer` / `off_sulk` / `off_walk` | official | sneer with arms folded / sulky defeat, head low, a little red / walk frame |
| `clerk_type_a/_b/_c` | clerk_a, _b, _c | typing at a typewriter on a desk (`typewriter=1`, `desk=1`) |
| `clerk_laugh_point_a/_b/_c` | " | laughing and pointing at Beck (screen-right, `mirror=True` for left), tears |
| `clerk_laugh_belly_a/_b/_c` | " | doubled over laughing, hands on the belly, eyes shut |
| `clerk_sit_a/_b/_c` | " | seated at a desk, chin on hand, bored |
| `pass_walk_man` / `_woman` / `_child` | pass_man / pass_woman / pass_child | walk frame (briefcase / handbag / nothing); `cast22.walk(cast, phase)` or `crowd_member(i, "pass_walk")` animates |
| `pass_squint` | pass_man | nose almost on the wall map (screen-right), squinting, hands behind his back |
| `old_squint` | old_gent | peers at the old map through the magnifying glass and the monocle, squinting |
| `pass_unfold_map` | pass_woman | unfolds the pocket map with both hands (open map, cover in the other) |
| `pass_read_map` | pass_man | reads the open pocket map held up, briefcase in the other hand |
| `pass_tap_map` | pass_woman | taps a station on the map with her finger |
| `pass_read_paper` | pass_man | reads the daily newspaper in both hands |
| `pass_point` | pass_man | points the way (screen-right), folded map in the other hand |
| `pass_smile_board` / `pass_smile_board_woman` | pass_child / pass_woman | confident step toward the train, smiling, the folded map in the fist |
| `pass_bump` | pass_man | bumped: stumbling, **bowler askew** (`head_roll -16` tilts the hat with the head), arms flung out, briefcase swinging |
| `porter_hand_map` | porter | hands a folded pocket map to a passenger (screen-right), spare open map in the other hand |
| `porter_push_crate` | porter | pushes a `MAPS` crate on a sack truck (`handtruck`), leaning into it |
| `porter_walk` | porter | walk frame |

`cast22.pose_for(name, cast=None)` resolves the brief's generic names: `pose_for("clerk_type", "clerk_b")` = `STORY22["clerk_type_b"]`, `pose_for("pass_walk")` = the man's walk frame (`"pass_woman"` / `"pass_child"` for the others).

That makes 51 poses. No name collides with earlier STORY entries or CAST keys. All of them are mirror-safe (`python3 test_cast22.py canvas` runs the head-flip check: 51 poses, 0 problems).

## Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D)

| member | canvas |
|---|---|
| beck | (-2.0, -4.8125, 2.0, 0.125) |
| official | (-2.1875, -5.0625, 2.1875, 0.125) |
| clerk_a | (-2.0625, -4.875, 2.0625, 0.125) |
| clerk_b | (-2.0625, -4.625, 2.0625, 0.1875) |
| clerk_c | (-2.1875, -4.5, 2.1875, 0.125) |
| pass_man | (-2.125, -4.75, 2.125, 0.125) |
| pass_woman | (-2.0625, -4.625, 2.0625, 0.125) |
| pass_child | (-1.9375, -3.9375, 1.9375, 0.375) |
| old_gent | (-2.125, -4.5625, 2.125, 0.125) |
| porter | (-2.125, -4.6875, 2.125, 0.125) |
| crowd22_NN | the canvas of its base member |

`python3 test_cast22.py canvas` checks every arm preset with the briefcase / umbrella / sheet (and the hand truck for the porter) at yaw +-0.6 (mirrored, squash 0.8-1.15), crouch, wide legs, all the fx incl. flush / puff, yaw +-1.2, every STORY22 pose WITHOUT a set piece (`board` / `desk` / `typewriter` / `pillar` are drawn by the figure for the sheet and for tests; the real set supplies its own, so set `board=0` etc. and use the set's desk), 16 phases x 4 modes x 2 facings of the cycles, and the 16 crowd walkers: all fit with at least 0.32 D of head room. Poses with a set piece extend further (the desk and board are 1.5-2.3 D wide): pass a wider canvas to `Actor.build` if a set-piece pose is baked into a sprite.

## Files and QA

- `cast22.py` is the module.
- `test_cast22.py` modes: `sheet` -> `sheet.jpg` (see below), `canvas`, `identity` (earlier casts byte-identical), `robust` (pose-key garbage on the new members and 2 crowd variants, determinism, v2 `test_puppet.py --quick` on the 10 new names), and no argument = everything, printing `ALL OK` when all pass (`--lite` skips the slow v2 test_puppet run).
- `sheet.jpg`: row 1 heights (front + 3/4, head D = 92 px, the film 10 admiral and painter at the right for scale); then **every STORY22 pose twice, labelled, on a mid-grey ground (left cell) and on a dark-blue ground with the `rim` halo (right cell)**, lip-sync poses tagged; 18 face states per member (neutral, 4 mouths, blinks, happy, laughing, grinning, smug, sneer, shocked, worried, squint, sad, red face, puffed); every prop and set piece on grey and blue; the 16-person crowd on grey and blue.

## Known limits

- The board, desk, typewriter and pillar are figure-level overlays in the puppet's 2D plane (board / typewriter BEHIND the figure, desk and pillar in FRONT of it, in a fixed order); hands in the `front` layer are drawn with the figure, so hands on a desk must be above `desk_y`.
- `resolve_pose` / `lerp_pose` drop the cast22 pose keys (`flush`, `puff`, `napkin`, `fork_map`, `board*`, `desk*`, `typewriter`, `tw_*`, `pillar*`, `t`): re-add them to tweened poses.
- The official's dark navy suit and Beck's dark waistcoat have low contrast with a very dark blue ground: put the `rim` pose key on (as the sheet does, `rim="#a8bcff"`, `rim_w` 0.02) for dark sets.
- `pocketmap` / `letter` / `daily` text is tiny (`UNDERGROUND`, `NOTICE`, `THE DAILY`): readable at 1 D = 100 px and above, a texture below that.
- Held pieces are drawn in the arm's layer (as in cast8 .. cast10). `off_wave_sheet` and `off_stamp` use `layer="top"` so the prop passes over the head side.
- The old `newspaper` prop (cast7) has a Mona Lisa photo: use `daily` in film 22.
