# cast7.py: the cast of film 7 ("ไอ้มักกะโรนี", the Mona Lisa theft, Paris 1911 / Florence 1913) for the v2 puppet

File: `PROJ/v3/cast7/cast7.py` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`).
Python 3 stdlib only, deterministic. Nothing in `v2/puppet` or `v3/cast` .. `v3/cast6` is edited. On import, cast7 imports cast6 (which chains cast5 .. cast_ext and v2/puppet), adds entries to their tables and wraps puppet helpers on top of cast6's wrappers: `_norm` (this module's pose keys), `_face` (goatee, monocle, sweat drops), `_moustache` (handlebar), `_prop` (new props) and `figure` (lie down, far-grip anchors). Each wrapper falls through, so every earlier member draws as before.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast7")
import cast7                 # registers on import (idempotent); import it BEFORE sprites / stage.sprites (as film6/common.py does with cast6)
import puppet                # same module object: CAST now also has the 14 members below
cast, pose = cast7.STORY7["vincenzo_hide_panel"]
f = puppet.figure(cast, pose, "v")                                              # the panel under the smock (bulge)
w = puppet.figure("vincenzo_smock", cast7.cycle("vincenzo_smock", g / 32.0, "sneak"), "v")   # frame g of the sneak
a = actors.Actor("vin", "vincenzo_smock"); a.build(sprites.DEFAULT_CANVAS["vincenzo_smock"], sprite_dir, contact=True)
```

For film 7 copy `film6/common.py` and replace `cast6` by `cast7` in the path list / import (cast7 imports cast6 itself). Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies unchanged (pose keys, the 20 expressions, `mouth` incl. `("open", w, h)`, `blink`, `gaze`, fx `sweat` / `tears` / `zzz` / `blush` / `anger_fill`, cast6's `pale`, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`, `hand_for_tip`).

## Cast (head D = 1, plum ink, rubber-hose ink limbs, ball hands)

| key | build | head top to soles (hat) | look |
|---|---|---|---|
| `vincenzo` | `slim`, 0.70 x 0.90, legs 1.02 | **2.78** (2.90) = 0.86 of the mean adult: small | Vincenzo, normal clothes: dark grey flat cap, black hair, **black bushy moustache**, charcoal waistcoat with watch chain over a collarless cream shirt (rolled sleeves), brown-grey trousers |
| `vincenzo_smock` | same body | 2.78 (2.90) | the same man in the **white worker's smock** to the knees (band collar, yoke, buttons, chest pocket with a pencil, hip pockets, long white sleeves). Pose key `bulge` = the panel hidden under it |
| `director` | `stout`, 1.10 x 1.12, legs 1.46 | 3.45 (**4.02**) | pompous museum director: **black silk top hat**, black frock coat to the knees, dove-grey waistcoat, purple cravat, red buttonhole flower, watch chain, **big white handlebar moustache, monocle**, age lines |
| `coworker1` | `slim`, 0.64 x 1.04, legs 1.42 | 3.32 (3.43) | tall thin French worker: grey flat cap, ginger hair, pencil moustache, blue bib overalls over a sand shirt |
| `coworker2` | `stout`, 1.08 x 1.00, legs 1.12 | 2.99 (3.05) | stout French worker: olive flat cap, **big black moustache**, short blue worker's blouse (smock7 short), brown trousers |
| `plumber` | `regular` pear, 0.92 x 1.00 | 3.04 (3.16) | friendly plumber: brown cap worn jauntily, ginger moustache, smile, brown overalls over a green check shirt |
| `guard` | `stout`, 1.04 x 1.06 | 3.17 (3.44) | old Louvre guard: **bottle-green kepi** (gold piping + badge), bottle-green double-breasted tunic with brass buttons, red collar patches, belt, grey walrus moustache |
| `painter` | `slim`, 0.60 x 1.04, legs 1.46 | 3.36 (3.54) | the copyist painter: **red beret**, black handlebar + pointed goatee, paint-spattered pale-blue smock, big black floppy artist's bow |
| `police` | `slim`, 0.72 x 1.06, legs 1.38 | 3.30 (3.58) | police agent / inspector: **navy kepi** with silver piping, navy tunic, silver buttons and aiguillette cord, black handlebar moustache |
| `young_painter` | `regular`, 0.80 x 0.94, legs 1.10 | 2.90 (no hat) | generic young painter questioned by the police (no real-person likeness): short and stocky, thick dark hair, big eyes, **navy-striped sailor shirt**, rope belt, brown trousers, espadrilles |
| `dealer` | `stout`, 1.00 x 1.04 | 3.15 (3.35) | Florence art dealer: grey homburg, **pince-nez**, grey walrus moustache + goatee, cream linen double-breasted lounge suit, brown waistcoat, red bow tie |
| `lady` | `slim` hourglass | 2.96 (**3.48**) | **huge Edwardian picture hat** (roses, white ostrich plume, purple ribbon), aubergine bolero over a white high-necked blouse with lace jabot and cameo, long purple skirt to the ankles |
| `gentleman` | `regular`, 0.84 x 1.02, legs 1.34 | 3.22 (3.48) | **black bowler** (derby), slate-grey frock coat, brown waistcoat, blue tie, brown walrus moustache; walking stick in `crowd_stare_gentleman` |
| `newsboy` | `boy` | 2.44 (2.56) = 0.78 of the mean adult | newspaper boy: big olive newsboy cap, ginger hair, freckles, brown work jacket, cream scarf, knee breeches |

`lineup.jpg`, top band, shows them side by side, front and 3/4.

## New pose keys (read at draw time; like cast5/6's keys, `resolve_pose` / `lerp_pose` drop them: re-add them to tweened poses)

| key | range | effect |
|---|---|---|
| `bulge` | 0..1 (0) | the Mona Lisa panel hidden under a `smock7` costume (vincenzo_smock): a stiff rectangle pressing out the cloth over the belly, corner points and stress creases, shaded edge. Fades in with the value (animate 0 -> 1 as he slides it in) |
| `sweat` | 0..1 (0) | nervous sweat on any cast7 member: 1..5 drops round the head + a damp shine on the forehead (more than fx `sweat`, which still works) |
| `lie` | -100..100 deg (none) | the whole figure rotated about the hip and set down: 90 = lying on the back with the head to screen-left, -90 head to screen-right (mirror=True flips the direction). `feet_y` stays; the lowest point of the body rests on it and `anchors["feet"]` is the middle of the body on that line. Use the wider canvas `cast7.CANVAS7_LIE[cast]` for the actor (vincenzo / vincenzo_smock) |
| `panel_grip` | "side" (default), "bottom", "top" | how a hand holds `mona_panel` / `mona_framed` / `newspaper`: middle of the edge / a bottom corner (lifting it off the wall, holding it up) / a top corner (carrying it hanging) |
| `panel_side` | +1 / -1 / 0 (0) | which way the held piece extends from the hand (+1 = screen-right in the unmirrored figure). 0 = toward the body centre line |
| `flip_text` | bool (False) | the newspaper text and the painting are kept unmirrored when the figure is `mirror`ed; with `actor.head_flip = True` (sprites draw the figure mirrored inside scale(-1 1)) set `flip_text=True` so the text reads right (stage_test.py does) |
| `pale`, `t` | as cast6 | `pale` works on every cast7 member (`_cast6` flag) |

CAST keys (only `_cast7` members): `goatee=dict(color, light, len)`, `monocle=True`, `moustache_style="handlebar"` (+ `tache_scale`, colors moustache / moustache_l), `hat_side` (bighat7: +1/-1 side of the roses), `beret_side`, costume keys below.

New anchors (only while a two-handed piece is held): `grip_far_r` / `grip_far_l` = the point where the other hand goes (far edge / far corner of the piece held by that hand), `piece_centre_r/_l`, `piece_hand_r/_l`. Mirror and squash are applied like every other anchor. `prop_tip_*` of a piece = its centre.

## Costumes and hats added to cast_ext

Costumes: `smock7` (`smock_len`, `smock_flare`, `pencil`, `paint`, `bow`; colors smock / dark / collar / button / bow), `frock7` (`coat_len` (short = lounge suit), `coat_flare`, `neck` = cravat / tie / bow / string / none, `chain`, `flower`, `double`, `vest_buttons`; colors lapel / vest / vest_b / shirt / collar / tie / tie_dark / button / dark), `uniform7` (`double`, `cord`, `tunic_len`; colors pocket / button / belt / patch / dark), `stripe7` (colors stripe / pants / rope), `dress7` (`hem_frac`, `skirt_flare`; colors jacket / trim / skirt / skirt_d / belt / cameo / blouse_d), `overalls7` (cast3's overalls with the plaid under its own id -- cast3's id clashed with cast6's pale gradient and filled the face with plaid when pale > 0).
Hats: `tophat7`, `kepi7` (colors band / piping / visor), `beret7`, `bighat7` (colors ribbon / rose / rose2 / plume / plume_d), `bare7` (no hat).

## Props (`prop_r` / `prop_l`; `puppet.PROP_TYPES` / `PROP_TIP` extended)

| type | drawing | `prop_tip_*` | orientation |
|---|---|---|---|
| `mona_panel` | the bare poplar panel 0.50 x 0.72 D (wood edge + thickness, the portrait inset) | panel centre | upright, `panel_grip`, `panel_side`; other hand -> `grip_far_*` |
| `mona_framed` | the panel in its carved gilded frame behind glass (glare streaks), 0.72 x 0.94 D | frame centre | upright, same |
| `newspaper` | **replaces the v2 sheet while cast7 is loaded**: the Mona Lisa front page 0.56 x 0.76 D (masthead "LE GRAND JOURNAL", headline "LA JOCONDE A DISPARU !", her picture, columns) | page centre | upright, same; text unmirrored (see `flip_text`) |
| `key` | big iron skeleton key, 0.33 D (bow in the fist) | the bit | follows `angle` (default: along the forearm); animate angle 0 -> 90 for the turn in the lock |
| `palette` | painter's kidney palette with paint blobs, thumb hole in the hand | far edge | upright |
| `lantern` (cast2), `lantern2` (cast4), `paintbrush` (cast3), `stick` (cast2) | existing, used by the story poses | | |

Use `scale` in the prop dict for bigger pieces (e.g. `dict(type="mona_framed", scale=1.3)`).

Standalone pieces (SVG fragments in D units, centred on (0, 0) unless said): `mona_svg(uid, w, h)` (the painted image only), `mona_panel_svg(uid, back=False)` (back=True: the bare wooden back for the trunk), `mona_framed_svg(uid, glass=True)` -> (svg, anchors hook_tl/tr/bl/br, top, bottom, size), `hooks_svg(uid, ghost=0..1)` -> (svg, anchors): **the empty wall spot with the four iron hooks** (same hook anchors as the framed piece; ghost = paler unfaded rectangle), `newspaper_svg(uid, headline)`, `poster_svg(uid, text="OU EST-ELLE ?")` (kiosk poster / postcard), `key_svg(uid)`, `easel_svg(uid, canvas=True, painted=0..1)` -> (svg, anchors top, canvas_centre; feet on y = 0, 1.9 D tall).

## Cycles, lip-sync, blink

Re-exported from cast6 (work for every cast7 member): `cast7.cycle(cast, phase, mode, facing, base, arms, speed)` with modes `walk` (~28 frames per cycle), `run` (~16), `sneak` (~32), `march` (~24); `cast7.talk_mouth(frame, level, seed, hold)`; `cast7.blink_at(frame, period, offset)`; `cast7.NOD`. Keep `bulge` / `sweat` / props in `base`; with `arms="l"` set `arm_r` afterwards (vincenzo_smug_walk keeps the right hand on the bulge that way).

## STORY7 (`cast7.STORY7[name] = (cast, pose)`, also merged into `puppet.STORY`) and `cast7.STORY7_META[name]["note"]`

| name | cast | what |
|---|---|---|
| `vincenzo_stand`, `vincenzo_walk` | vincenzo | neutral stand / walk frame |
| `vincenzo_mocked` | vincenzo | **hurt by the mockery**: head down, blush, hands fiddling at the belt |
| `vincenzo_glare` | vincenzo | the grudge: side glare at the laughing co-workers, fists |
| `vincenzo_hide_closet` | vincenzo | Sunday night: crouched in the closet with a lantern, sweat |
| `vincenzo_sleep` | vincenzo | **asleep on his back** (`lie=90`, zzz, smiling; canvas CANVAS7_LIE) |
| `vincenzo_peek_bed` | vincenzo | **bent low beside the bed lifting the blanket to peek** at the trunk |
| `vincenzo_offer` | vincenzo | Florence: shows the panel (screen-right) to the dealer |
| `vincenzo_arrested` | vincenzo | **arrested**: hands behind the back, head down |
| `vincenzo_smock_stand`, `vincenzo_smock_walk` | vincenzo_smock | stand / walk frame in the smock |
| `vincenzo_sneak` | vincenzo_smock | **sneak** cycle frame, glancing back |
| `vincenzo_lift` | vincenzo_smock | **lifting the framed painting off the hooks**: both hands under the bottom corners, frame above-right of the head (`prop_l`, `panel_grip="bottom"`, `panel_side=1`, right hand on `grip_far_l`) |
| `vincenzo_carry` | vincenzo_smock | carrying the framed painting, glancing back, sweat |
| `vincenzo_unframe` | vincenzo_smock | crouched in the staircase with the bare panel (both hands) |
| `vincenzo_hide_panel` | vincenzo_smock | **panel hidden under the smock** (`bulge=1`), hands pressing it flat, smirk |
| `vincenzo_sweat` | vincenzo_smock | **locked door: tugging the handle, sweating** (`sweat=1`, `pale=0.5`, bulge) |
| `vincenzo_nervous_smile` | vincenzo_smock | stiff nervous grin back at the plumber, bulge, sweat |
| `vincenzo_smug_walk` | vincenzo_smock | **smug walk out** with the bulge, chin up, hand on it (walk frame) |
| `director_boast` | director | **pompous boast**: chin up, finger to the sky, hand on the lapel, talking |
| `director_proud`, `director_walk` | director | akimbo / walk frame |
| `director_shocked` | director | **shocked**: pale, sweat, both hands up |
| `coworkers_laugh` (+`_coworker2`) | coworker1 / 2 | **laughing**, tears, pointing (screen-right; `mirror=True` for left) |
| `coworkers_point` (+`_coworker2`) | coworker1 / 2 | **mocking point** + jeer, akimbo |
| `coworkers_walk` (+`_coworker2`) | coworker1 / 2 | walk frame |
| `plumber_open_door` | plumber | **turning the key in the lock** (screen-right; key `angle` 0 -> 90) |
| `plumber_greet` | plumber | **friendly 'bonjour' wave** (screen-left), key in the other hand |
| `plumber_walk` | plumber | walk frame |
| `guard_at_ease`, `guard_walk` | guard | hands behind the back / walk frame |
| `guard_shrug` | guard | **shrug**, palms up ('the photographers took it') |
| `guard_yawn` | guard | **huge yawn** (mouth `("open", 0.20, 0.26)`), stretching |
| `painter_ask` | painter | **'where is she?'**: open palms to the wall, head tilted |
| `painter_point` | painter | **pointing up at the empty spot** (screen-right), shocked, palette |
| `painter_paint`, `painter_walk` | painter | brush + palette at the easel / walk frame |
| `police_stand`, `police_walk` | police | stand / march frame |
| `police_search` | police | **searching**: bent forward, lantern held out |
| `police_question` | police | pointing, questioning (screen-left) |
| `police_arrest` | police | **the arrest**: open hand gripping an arm (screen-left), finger raised |
| `young_painter_questioned` | young_painter | **questioned**: hands up, nervous, sweat |
| `young_painter_indignant` | young_painter | **indignant**: 'me?!', pointing at himself, anger fill |
| `dealer_inspect` | dealer | **inspecting the panel** at arm's length (screen-left) through the pince-nez |
| `dealer_signal` | dealer | **secret signal to the police** (screen-right): beckoning hand, wink |
| `dealer_smile`, `dealer_walk` | dealer | welcoming / walk frame |
| `crowd_stare` (+`_gentleman`, `_newsboy`) | lady / gentleman / newsboy | queuing, staring up at the empty wall (gentleman with his stick) |
| `crowd_point` (+`_gentleman`, `_newsboy`) | " | excited pointing up |
| `crowd_walk` (+`_gentleman`, `_newsboy`) | " | walk frame |
| `newsboy_shout` | newsboy | **'extra!'**: Mona Lisa front page waved high, shouting |
| `gentleman_read` | gentleman | reading the front page (both hands), shocked |
| `lady_gasp` | lady | gloved hand to the mouth, gasping |

63 poses. No name collides with earlier STORY entries (cast6 already has `guard_stand` for guard1, hence `guard_at_ease`).

## With the v3 stage

Exactly as cast6 (see `stage_test.py` -> `stage_test.png`: vincenzo_smock lifting the framed painting, the director boasting, the newsboy with the front page, key from screen-right, `head_flip` on + `flip_text=True`, Cycles 360x640, 2 threads). Canvases (feet-relative, through `cast_ext.CANVAS` into `sprites.DEFAULT_CANVAS`, in D):

| member | canvas |
|---|---|
| vincenzo, vincenzo_smock | (-1.5, -4.3125, 1.5, 0.125); lying: `CANVAS7_LIE` (-2.0625, -1.4375, 2.0625, 0.25) |
| director | (-1.5625, -5.0625, 1.5625, 0.125) |
| coworker1 | (-1.5, -4.9375, 1.5, 0.125) |
| coworker2, plumber | (-1.5625, -4.5625, 1.5625, 0.125) |
| guard | (-1.5625, -4.75, 1.5625, 0.125) |
| painter | (-1.4375, -5.0, 1.4375, 0.125) |
| police | (-1.5, -4.9375, 1.5, 0.125) |
| young_painter | (-1.5, -4.375, 1.5, 0.125) |
| dealer | (-1.5625, -4.6875, 1.5625, 0.125) |
| lady | (-1.4375, -4.5, 1.4375, 0.3125) |
| gentleman | (-1.5, -4.8125, 1.5, 0.125) |
| newsboy | (-1.375, -3.8125, 1.375, 0.125) |

Checked: every arm preset with each film-7 prop (panel, framed, newspaper, key, palette, lantern) in side and bottom grip at yaw +-0.6 (mirrored, squash 0.8-1.15), crouch, wide legs, all effects + pale + sweat + bulge, yaw +-1.2, every STORY7 pose and 16 phases x 4 modes x 2 facings of the cycles, >= 0.32 D head room; the lie poses at +-90 against CANVAS7_LIE. A big piece held at arm's length to the far side (panel_side outward with a stretched arm) can still exceed the canvas: pass a wider canvas to `Actor.build` for such a shot.

## Files and QA

- `cast7.py`: the module. `test_cast7.py`: `lineup` -> `lineup.jpg` (heights front + 3/4; all 63 STORY7 poses; walk ->, run ->, walk <- cycles at 8 phases for every member; mouths talk_a / talk_b / talk_o / flat, blink 1 / 2, angry, sweat, laughing, shocked, pale for every member; props), section PNGs in `tmp/`; `canvas` (+ head_flip anchor check: 63 poses, 0 problems); `robust` (pose-key garbage on the 14 members + v2 `test_puppet.py --quick` on them: 4.7 M checks, 0 failed, see `run_robust.log`).
- `stage_test.py` -> `stage_test.png`.

## Known limits

- `bulge` is drawn over the smock front (torso + skirt); arms in `front` layer go over it, which is what the hands-pressing poses want. It belongs to `smock7` only.
- `lie` rotates the finished drawing: the head disc's thick side and the light crescent rotate with it, and fx (zzz) rotate too. The body rests on `feet_y` by its anchors (it may sink up to ~0.15 D into the mattress line, which a blanket card covers).
- Held pieces are drawn in the arm's layer: with `layer="front"` the head stays in front of a piece raised beside it (vincenzo_lift), with `top` the piece covers the face.
- The `newspaper` prop of the v2 puppet (a plain sheet) is replaced while cast7 is loaded: any earlier film that imports cast7 gets the Mona Lisa front page.
- `resolve_pose` / `lerp_pose` drop the cast7 keys (as with cast5/6): re-add `bulge`, `sweat`, `lie`, `panel_grip`, `panel_side`, `flip_text` to tweened poses.
