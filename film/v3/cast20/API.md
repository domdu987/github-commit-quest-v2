# cast20.py: the cast of film 20 ("ไอ้ช่างหมุด", Eiffel's tower and the artists' protest, Paris 1887-1909) for the v2 puppet

File `PROJ/v3/cast20/cast20.py` (PROJ = `/home/user/github-commit-quest-v2/film`). Python 3 stdlib only, deterministic. Same pattern and habits as cast16: imports cast10 (which chains cast9 .. cast_ext and v2/puppet), wraps `_norm`, `_face`, `_prop`, `figure`; nothing earlier is edited (`test_cast20.py identity`: 531 earlier renders, 0 differ).

```python
import sys; sys.path.insert(0, PROJ + "/v3/cast20")
import cast20                         # registers on import (idempotent); import BEFORE sprites / stage.sprites
import puppet
cast, pose = cast20.STORY20["maupassant_quote_point"]
f = puppet.figure(cast, pose, "f")
p = dict(pose, mouth=cast20.talk_mouth(g, 1.0), blink=cast20.blink_at(g, 90))      # lip-sync: Maupassant only
w = puppet.figure("riveter_tongs", cast20.cycle("riveter_tongs", g / 28.0, "walk"), "w")
a = actors.Actor("eif", "eiffel"); a.build(cast20.CANVAS20["eiffel"], sprite_dir, contact=True)
```
Everything in `v2/puppet/API.md` and `v3/cast*/API.md` applies: pose keys, mouths incl. `("open", w, h)`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `ink`, `rim`, `lerp_pose`. Characters face screen-right at positive yaw (`mirror=True` for left). Heads are D = 1; figures stand 3.1 to 3.6 D (child 2.3).

## Cast (CAST key = API name)
| key | who | look |
|---|---|---|
| `eiffel` | hero 1887-89 | regular build, dark bowler (derby style), short neat grey-brown chin beard + bushy moustache, charcoal frock coat, tan waistcoat with watch chain, red tie. `hat_off=1` = bare head (CAST `eiffel_bare`) |
| `eiffel_old` | 1909 | same, white beard + moustache, slightly shorter. Use pose `lean=4..6` for the stoop. `hat_off=1` ok |
| `maupassant` | the mocker | stocky (stout), thick dark walrus moustache, dark wavy side-parted hair (hair20 wavy), dark-blue frock coat, cream waistcoat, red cravat. **Only lip-sync character.** Pose key `napkin=1` tucks a white napkin in the collar |
| `painter20` | artist | red beret, goatee, cream paint-spotted smock |
| `composer20` | artist | wild white hair + white beard, dark-green frock coat |
| `architect20` | artist | khaki top hat (`hat_off=1` ok), brown coat, moustache |
| `poet20` | artist | long chestnut hair, plum coat, white loose cravat |
| `riveter_tongs` / `riveter_hammer` / `riveter_forge` | workers | blue work smocks; navy flat cap / brown flat cap + moustache / red polka-dot kerchief + red-brown beard |
| `telegraphist` | soldier 1909 | red-top kepi with blue band, blue tunic, red trousers, headphones (CAST `headphones20`), moustache |
| `officer` | 1909 | same kepi/colours, gold epaulettes + gold belt, handlebar moustache |
| `official` | 1889 city official | black tailcoat, tricolour sash (blue-white-red, gold fringe knot), black top hat with red band (`hat_off=1`), grey walrus moustache |
| `waiter` | | black waistcoat, white shirt, bow tie, LONG white apron, slicked hair, handlebar moustache |
| `lady20` | Parisian | blue bustle dress (bustle bump on the screen-left side, flips with negative yaw), plumed straw hat |
| `gent20` | Parisian | black top hat (`hat_off=1`), brown frock coat, handlebar moustache |
| `child20` | Parisian | sailor suit + sailor cap |

## Expressions (`puppet.EXPRESSIONS` gains: sneer, laughing20, blissful, avoid, sly, proud, cheer, working, stern, outraged)
`cast20.EXPRS20[char][label]` = pose keys for each character's own set (used by the sheet):
- eiffel: calm (neutral), determined, proud, worried (+sweat), sly. eiffel_old: worried, determined, proud, calm.
- maupassant: sneer, laughing (`laughing20`, eyes squeezed), smug, shocked, blissful (eyes closed, eating), avoid (eyes shut, yaw -0.7, chin up).
- painter20 / composer20 / architect20 / poet20: outraged, laughing, sneering.
- riveter_*: working, cheering (`cheer`, mouth open). telegraphist: focused, listening, relieved. officer: stern, neutral, proud. official: neutral, stern, smiling. waiter / lady20 / gent20 / child20: neutral, smile or smug, amazed (shocked).

**Lip-sync (Maupassant only).** `cast20.MOUTH_SET` = flat, talk_a, talk_b, talk_o, o, ("open", .12, .05), ("open", .20, .10), ("open", .30, .19). Drive with `mouth = talk_mouth(frame, level)`. Quote 1 22.62-25.11 s: `maupassant_quote_point` (alt `_quote_newspaper`, `_quote_chest`). Quote 2 37.12-40.67 s: `maupassant_laugh_quote` / `maupassant_laugh_thumb` (laugh + mouth). Poses flagged lipsync in `STORY20_META[name]["lipsync"]`. Outside the quotes set `mouth="flat"` (or use the `_silent` / non-flagged variants). Other characters hold fixed mouths (the `cheer` and `outraged` expressions have an open held mouth; never animate them).

## Props (`prop_r` / `prop_l`: name or `dict(type=..., angle=..., scale=...)`)
| type | what | follows | anchors |
|---|---|---|---|
| `blueprint` | rolled blueprint (blue-grey, red tie, grid marks, no text), hand at its middle | angle | `blueprint_r/_l` |
| `rivet20` | ordinary rivet, steel | angle | `rivet_*` |
| **`giant_rivet`** | GIANT red-lead rivet: dome head 0.56 across, thick shank (hand holds the shank) | angle | `rivet_*` |
| **`tongs_rivet`** | smith's tongs gripping a GLOWING red-orange rivet with halo (pose key `glow` 0..1 flickers it) | angle | `rivet_*` (the rivet), `grip_far_*` |
| `tongs_cold` | same tongs, empty jaws (heating at the forge, set draws the glow) | angle | `rivet_*`, `grip_far_*` |
| `rivet_hammer` | long-handled riveter's hammer | angle | `hammer_*` (head), `grip_far_*` |
| `hammer20` | small hammer | angle | `hammer_*` |
| `quill` | feather quill pen | angle | `quill_*` (nib) |
| `news20` | newspaper, GREEKED (grey bars, headline bar, photo block) | upright | `news_*` |
| `sheet20` | paper with greeked lines and many signature squiggles (the protest letter) | upright | `sheet_*` |
| `doc_seal` | document with a BIG red wax seal + blue ribbon, greeked | upright | `doc_*` |
| `wine_glass` | wine glass, red wine | upright | `glass_*` |
| `fork20` | fork (pose key `bite` 0/1 puts a morsel on it) | angle | `fork_*` |
| `knife20` | table knife | angle | `knife_*` |
| `cane20` | black cane, gold knob (1.4 long, use scale 0.7 for a hand cane) | angle | `cane_*`, `grip_far_*` |
| `parasol20` | open pink parasol | angle | `parasol_*`, `grip_far_*` |
| `tray20` | silver tray with glass and covered dish | upright | `tray_*` |
| `towel20` | white towel over the forearm (blue stripes) | upright | `towel_*` |
| `morse_key` | Morse key on a walnut base (pose key `key_press` 0..1 lowers the lever) | upright | `key_tip_*` |
| `bowler_held` / `tophat_held` | hat held by the brim | upright | `hat_*` |
Existing props still work (`palette`, `paintbrush`, `paper`, `hammer`, ...). Pose keys: `napkin`, `bite`, `glow`, `key_press`, `hat_off`, `stool` (draws a three-legged stool under the hips; pair with `legs=dict(crouch=0.4)`; for the seated telegraphist, the desk is set art), `t`.

## STORY20 (`cast20.STORY20[name] = (cast, pose)`, merged into `puppet.STORY`; `STORY20_META[name]["note"|"lipsync"]`; 95 poses, see `sheet.jpg`)
- Eiffel: `eiffel_calm`, `_blueprint`, `_blueprint_chest`, `_giant_rivet`, `_giant_rivet_show`, `_hammer`, `_rivet_pinch`, `_worried`, `_sly_hammer_down`, `_hat_off`, `_point_up`. Old: `eiffel_old_calm`, `_worried`, `_point_up` (pointing-up determined), `_proud`, `_hat_off`.
- Maupassant: `_idle`, `_read_news`, `_quote_point`, `_quote_newspaper`, `_quote_chest` (lip-sync), `_laugh_quote` (lip-sync, bounce), `_laugh_thumb` (laughing, thumb jerked over his shoulder: far arm back over the shoulder in the point shape; lip-sync flagged, `_laugh_thumb_silent` for the held laugh), `_laugh_belly`, `_smug_wine`, `_write`, `_shocked`, `_turn_away` (eyes shut, arms crossed, faces screen-left), `_eat` (napkin, blissful, fork with bite, knife), `_eat_chew`, `_eat_back`.
- Artists: `<who>_outraged`, `_laughing`, `_sneering` for painter20 / composer20 / architect20 / poet20 + `painter20_palette`, `composer20_point`, `architect20_plan`, `poet20_quill`, `artists_protest_sheet`.
- Workers: `riveter_tongs_work` / `_cheer` / `_throw`, `riveter_hammer_work` / `_hit` / `_cheer`, `riveter_forge_work` / `_lift` / `_cheer`.
- 1909: `telegraphist_key` (seated, key_press animates), `_listen`, `_stand`, `_cheer`; `officer_stern`, `_salute`, `_point`.
- 1889: `official_doc`, `_stern`, `_smile`, `_hat_off`. Waiter: `waiter_tray`, `_idle`, `_bow`, `_alarmed`. Parisians: `lady_parasol`, `_amazed`, `_idle`, `gent_cane`, `_amazed`, `_idle`, `child_wave`, `_point`, `_idle`.
Animation recipes: laugh bounce = `squash` (1.03, 0.97) <-> (0.99, 1.01) at ~3 Hz and +/-0.06 D on stage; hammer blow = tween `prop_r` angle -70 -> 5 between `riveter_hammer_work` and `_hit`; glowing rivet flicker = `glow` 0.7..1; chewing = alternate `maupassant_eat_chew` mouth `smile` / `("open",.16,.08)`.

`cast20.cycle(cast, phase, mode, facing, base, arms, speed)`: cast6's `walk` / `run` / `sneak` / `march` for every member. Blink: `blink_at`.

## SEATED and BACK cards (added)
- Pose key **`seated=1`** (any member): crouches the legs so the **seat top** (`anchors["seat"]` = hip + 0.16 D) is `seat_h` D above the floor; default `seat_h = 0.60 D` (range 0.30..1.0, clamped to what the leg length allows; Maupassant reaches 0.35..1.04, so a seat of 1.6 D is NOT reachable by leg geometry: scale the card instead, card scale = chair seat height in the set / 0.60 D, or pass the set's seat height in D units of this card). No stool is drawn (the bentwood chair is set art); `stool=1` still draws the walnut stool if wanted. The feet stay planted: **pivot = `anchors["feet"]` at `feet_y`, i.e. the sprite base (Actor with contact=True) sits on the floor mark**; the hips/seat are at `seat` (y above the floor = feet_y - seat_y, shown on the sheet as a red dashed line). Place the chair so its seat top meets that line, the figure's bottom (rear) just over the seat, thighs hidden by the coat.
- Seated poses: `maupassant_seated_eat` (napkin, fork with bite at the mouth, knife, blissful), `maupassant_seated_eat_chew`, `maupassant_seated_toast` (wine glass raised, blissful), `maupassant_seated_toast_smug`, `maupassant_seated_eyes_shut` (new expression `smug_shut`, chin up, arms crossed, faces screen-left), `maupassant_seated_eyes_shut_right`, `maupassant_seated_back` (three-quarter BACK, no face), `maupassant_seated_back_eat` (fork raised).
- Pose key **`back=1`**: the back of the head (hair-coloured, ears, no face, no beard/headphones) and a plain coat/smock back (centre seam, collar band; works for frock7 / smock7 / official costumes, i.e. all artists, Eiffel, Maupassant, gent). Use yaw 0.3..0.5 for a three-quarter back. Standing back cards: `maupassant_back`, `painter20_back`, `composer20_back`, `architect20_back`, `poet20_back`.
- Back cards of costumes other than frock7 / smock7 / official20 (workers, waiter, lady, soldiers) are not covered: they would still show their front costume details.

## Canvases (feet-relative, D units) `cast20.CANVAS20[member]` (through `cast_ext.CANVAS`)
Measured over all poses (plain + mirrored), 16 phases x 4 modes x 2 facings of the cycles and yaw/arm sweeps, +0.12..0.15 D margin: eiffel (-1.69,-3.69,1.69,0.19), maupassant (-1.5,-3.56,1.5,0.19), riveter_tongs (-2.44,-3.44,2.44,0.19), telegraphist (-1.81,-3.75,1.81,0.19), others see the dict. `test_cast20.py canvas`: 0 outside.

## Files and QA
`cast20.py`, `test_cast20.py` (`story` (also checks seat heights and back heads), `identity`, `measure`, `canvas`, `robust`, `sheet`, default all), `sheet.jpg` (lineup with height ruler, all expression sets as head close-ups, Maupassant mouth set, held props, every pose labelled), `sheet_small.jpg` (360 px phone check), `run_log.txt`.

## Known limits
- Hands are balls/open/point only: the "thumb over the shoulder" is a pointing hand behind the shoulder; a salute is a flat hand at the kepi side (arm beside the head).
- The walrus moustache covers the top of Maupassant's mouth: `talk_a` and `flat` are subtle, `talk_b`/`talk_o`/`("open", ...)` read clearly. Eiffel's chin beard + moustache likewise hide most of his mouth, his expressions read through brows/eyes (sweat on worried).
- White beard/hair on the white head fill is carried by its outline only (eiffel_old, composer).
- The seated telegraphist uses the puppet crouch: thighs are not foreshortened (hide behind the set's desk); the key prop floats at hand height, the desk is set art.
- Arms "folded" are two crossing arms in front of the chest (rope-like), not a drawn forearm overlap.
- The giant rivet is a stylised red-lead mushroom/dome (reads as a rivet next to the tower, less so alone). Quill is small.
- Lady's bustle is a rounded bump on one side only; no train. `head_flip` (stage mirrored head disc check) not run: no Blender stage here.
