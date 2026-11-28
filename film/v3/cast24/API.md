# cast24.py: the cast of film 24 (Korea's turtle ship, Admiral Yi Sun-sin, 1592) for the v2 puppet

File: `PROJ/v3/cast24/cast24.py` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`). Python 3 stdlib only, deterministic. Nothing older is edited. cast24 imports cast10 (which chains cast9 .. cast_ext and v2/puppet) and wraps `_norm`, `_face`, `_moustache`, `_ink_limb`, `_prop`, `figure` on top of cast10's wrappers; everything it does not handle falls through. `python3 test_cast24.py identical` confirms 480 earlier STORY / cycle SVGs are byte-identical with cast24 imported.

```python
import sys
sys.path.insert(0, PROJ + "/v3/cast24")
import cast24                      # BEFORE sprites / stage.sprites
import puppet
cast, pose = cast24.STORY24["jp_cmd24_point_mock"]
p = dict(pose, mouth=cast24.talk_mouth(g, 1.0), blink=cast24.blink_at(g, 90))
w = puppet.figure("ashi_a24", cast24.cycle("ashi_a24", g / 28.0, "walk"), "f")
a = actors.Actor("cmd", "jp_cmd24"); a.build(cast24.CANVAS24["jp_cmd24"], sprite_dir, contact=True)
a = actors.Actor("pl", "jp_cmd24"); a.build(cast24.CANVAS24_POSES["jp_cmd24_plank_cling"], sprite_dir, contact=True)
```
Everything in `v2/puppet/API.md` and `v3/cast10/API.md` still applies (pose keys, expressions, `mouth`, `blink`, `gaze`, fx, anchors, `mirror`, `tint`, `rim`, `lerp_pose`, `hand_for_tip`; `cycle`, `talk_mouth`, `blink_at`, `NOD` are re-exported). Colours: heads / ink / mouth per COLOUR_SPEC section 2 (puppet defaults, unlit); costume colours are mid-to-deep saturated, no tint needed.

## Members (head D = 1; height = head top to soles, hat top in brackets)

| key | height | build / look |
|---|---|---|
| `yi24` | 3.30 (3.58) | slim, tall, calm. Maroon quilted coat-armour with brass studs, blue lining at collar / cuffs / front opening, dark belt with brass plate, knee-length skirt. Black wide-brim hat with brass-bead band, red plume and chin cord. Neat thin moustache, small goatee |
| `jp_cmd24` | 3.13 (3.96) | stout, big belly. Black lacquer plate armour with red lacing, red cord belt, big sode shoulder guards, hip plates. Kabuto with a tall gold crescent. Kabuto sits high (brim above the brows); a small thin handlebar moustache above the mouth (mouth fully visible), thick angry brows, double chin |
| `ashi_a24` | 3.26 (3.64) | tall slim, blue kimono, dark-brown cone hat, thin black moustache |
| `ashi_b24` | 2.71 (2.98) | short and round, brown kimono, red-brown wide cone with a crest, grey stubble |
| `ashi_c24` | 2.96 (3.30) | medium, grey kimono, pale grey cone with a red crest, young clean face, round brows |
| `ashi_d24` | 3.50 (4.06) | lanky, olive kimono, tall black cone, bushy brows and a big moustache |
| `kor_a24` | 3.08 (3.35) | medium, off-white hanbok, topknot, blue-grey collar, red goreum |
| `kor_b24` | 2.79 (2.97) | stout, short small black hat with chin cord, brown moustache |
| `kor_c24` | 2.78 (2.98) | young, short, slim, white headband over spiky hair, freckles, green goreum |
| `kor_d24` | 3.30 (3.57) | tall, topknot with a blue headband, stubble, strong |

All ashigaru wear a riveted chest plate (do) with a short plate skirt over the kimono. Korean workers: jeogori with a crossed collar band, goreum bow, waist band knot, sleeves tied up (rolled, brown tie), baji trousers tied at the ankles.

## New pose keys

| key | effect |
|---|---|
| `sode24` 0..1 | scales the jp_cmd24 shoulder guards (0 in the lying / crawl poses so the face is clear) |
| `wet24` 0..1 | wet look: kabuto locks + drips + seaweed on the crescent (jp_cmd24); plastered fringe + drips (jp_cmd24 only) |
| `hat_rot24` deg, `hat_dx24` D | kabuto askew (rotate / shift) |
| `ground24` y (head frame) | sets `feet_y`, `anchors["feet"]` and `anchors["ground"]` to this line (kneel / crawl) |
| `plank24` 0/1 | draws the floating plank under the figure (`plank_w24` 4.6, `plank_top24`, `plank_dx24`). NOTE: key is `plank24`, not `plank` (cast10 owns `plank` = hanging painter's plank). feet_y = the plank's UNDERSIDE (waterline); anchors `plank_top`, `plank_l`, `plank_r`, `ground` |
| `spike_n24` 2..8 | number of spikes in `spike_bundle24` |

Face CAST keys: `moustache_style="neat24"`, `goatee24`, `stubble24`; hats `gat24`, `kabuto24`, `jingasa24` (`cone_h`, `cone_w`, `mon24`), `smallhat24`; costumes `joseon24`, `samurai24`, `ashigaru24`, `hanbok24`; `sode24=<size>` shoulder guards.

## Props (`prop_r` / `prop_l`, `prop_tip_*`, extra anchor `<name>_r/_l` = the working point)

| type | tip | note |
|---|---|---|
| `katana24` | 1.12 | blade tip; follows `angle` |
| `yari24` | 1.95 | spear, pole -0.55..1.55, red tassel; anchor `yari_r` = spear tip |
| `gunbai24` | 1.04 | war fan: handle + round cream fan with a red sun disc |
| `ladder24` | 1.9 | ladder 2.4 D long (front carrier); `ladder_grip24` draws nothing (rear carrier's hands) |
| `spike24` | 0.55 | single iron spike, head at the hand |
| `spike_bundle24` | 0.55 | bundle of spikes tied with rope (`spike_n24`) |
| `hammer24` | 0.68 | long-handled iron hammer (anchor `hammer_r` = head centre) |
| `mallet24` | 0.62 | wooden mallet |
| `rope24` | 0.40 | rope coil hanging below the hand, always upright |
| `oar24` | 2.3 | oar, grip at 0, blade at the end; anchor `oar_r` = blade |

Standalone: `cast24._prop_body(k, kind)` (SVG in D units, hand at the origin).

## STORY24 (`cast24.STORY24[name] = (cast, pose)`, notes in `STORY24_META[name]["note"]`; also merged into `puppet.STORY`)

Per member (`<cast>_<pose>`):
- `yi24`: `stand_arms_behind`, `nod` (the DOWN key; animate pitch 0 -> 0.28 -> 0), `point_forward`, `satisfied_smile`, `walk`.
- `jp_cmd24`: `laugh_big` (held open mouth), `point_mock` (**lipsync**), `finger_up_promise` (**lipsync**), `shout_forward` (**lipsync**, gunbai in the arm), `plank_cling`, `crawl_a` (left hand + right knee forward), `crawl_b` (opposite), `walk`.
- `ashi_a24 .. ashi_d24`: `laugh_point`, `sword_raise` (katana24), `peer_worried`, `step_back`, `walk`; extras `ashi_c24_yari`, `ashi_d24_ladder_front`, `ashi_b24_ladder_back`.
- `kor_a24 .. kor_d24`: `kneel_hammer` (a, d: hammer24; b: mallet24; c: hammer24 + a spike in the other hand), `stand_carry_spikes` (kor_d also a rope coil), `row_oar` (both hands on the oar), `cheer`, `walk`; extra `kor_c24_stand_rope`.

Lip-sync: only the three jp_cmd24 poses have `STORY24_META[name]["lipsync"] = True`; set `mouth = talk_mouth(g)` inside the quote windows (16.1-21.4 s, 34.8-37.0 s) and `"flat"` outside. Every other pose holds one fixed mouth. The bushy moustache is drawn under the mouth so the shapes read.

## Ground and feet (important for card placement)

- Standing and walking poses: both soles on the feet line (`feet_y`), contact shadow as usual.
- `kor_*_kneel_hammer`: both knees and the toes on the roof; `anchors["ground"]` = `anchors["feet"]` = that line (the figure is drawn lower than standing; place the card with that point on the roof surface). Animate only `arm_r`: raised (0.60, -0.50), prop angle -70, to strike (0.78, 0.62), angle 20.
- `jp_cmd24_crawl_a/_b`: hands, knees and shin ends on the ground line (`anchors["ground"]`, head to screen-right; `mirror=True` flips). Alternate A/B with a forward move (about 0.45 D per half step) for the crawl.
- `jp_cmd24_plank_cling`: the card's ground is the plank's underside (waterline); the plank is part of the card (`plank24`), so the card rides the water as one piece.

## Canvases (feet-relative, D)

`CANVAS24[member]` (registered in `cast_ext.CANVAS`): yi24 (-1.8125, -4.75, 1.8125, 0.125); jp_cmd24 (-2.25, -5.125, 2.25, 0.125); ashi_a (-1.8125, -4.75, ..); ashi_b (-1.875, -4.125); ashi_c (-1.875, -4.375); ashi_d (-1.8125, -5.0625); kor_a (-1.8125, -4.5); kor_b (-1.875, -4.1875); kor_c (-1.8125, -4.1875); kor_d (-1.875, -4.6875). `CANVAS24_POSES[pose_name]` for the poses that exceed them: `jp_cmd24_plank_cling`, `jp_cmd24_crawl_a/_b`, the four `kor_*_kneel_hammer` (bottom 0.1875 below the ground line), the four `kor_*_row_oar` (+-3 wide), `ashi_d24_ladder_front`, `ashi_b24_ladder_back`. `python3 test_cast24.py canvas` checks all of them, mirrored too, plus head_flip (57 poses, 0 problems).

## Files and QA

`test_cast24.py`: `sheet` -> `sheet.jpg` (size line-up with lin and the film 10 admiral for scale; every STORY24 pose, lip-sync tagged, ground lines dashed red; 18 face states per member; props), `canvas`, `identical`, `robust` (3000 garbage-key figures, 0 failures).

## Known limits

- Legs are the puppet's thin ink limbs (the style of the earlier cast); ashigaru legs are dark, Korean baji are thick off-white.
- Crawl / plank poses are built with `lean` 70-72 (cast limit 75): the torso is horizontal, the face a little tilted; the kabuto crescent points up.
- `wet24` hair strands and drips are drawn for jp_cmd24 only.
- `resolve_pose` / `lerp_pose` drop the cast24 keys: re-add `wet24`, `hat_rot24`, `hat_dx24`, `ground24`, `plank24*`, `spike_n24` to tweened poses.
