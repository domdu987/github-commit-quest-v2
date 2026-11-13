# lt_cast.py: cast of "ช่างเชื่อมสายฟ้า" for the v2 puppet

File: `/tmp/claude-0/-home-user-github-commit-quest-v2/9c3eda1a-2051-532f-961a-8e1f745caea6/scratchpad/r3d/v3/ltcast/lt_cast.py`
Python 3 standard library only, deterministic. `v2/puppet/puppet.py` and `v3/cast/cast_ext.py` are not edited. On import, the module registers on top of both. Hero, boss and the six cast_ext members produce byte-identical output with or without it (checked with an SHA-1 over svg, bbox, anchors and feet_y).

```python
import sys; sys.path.insert(0, ".../v3/ltcast")
import lt_cast                     # imports cast_ext (which puts v2/puppet on sys.path), then registers
import puppet                      # same module object: 14 members now
f = puppet.figure("welder", dict(lt_cast.POSES["welder_shocked"][1]), "w")
```

Everything in `v2/puppet/API.md` and `v3/cast/API.md` still applies: pose keys, presets, expressions, fx, anchors, `mirror`, `tint`, `rim`, `place_svg`, `hand_for_tip`.

## Members (head D = 1, ink #3a2832, no nose or ears, rubber-hose limbs, ball hands, pink cheeks)

| name | build | look | main hue |
|---|---|---|---|
| `welder` (คุณ) | slim pill 0.57 x 1.01, legs 1.14 | short black hair with a jagged fringe; dark-blue tee (sleeves on the arms); brown leather apron with a bib, stitched chest pocket, neck straps, waist ties and scorch marks; boots | blue + brown |
| `hong` (เจ๊หงส์) | stout pear 1.04 x 1.00, legs 1.06 | dark curly perm outside the head contour, gold hair pin; magenta flower blouse, puffed sleeves, heavy gold chain with an amulet, money belt-bag, dark trousers, sandals | magenta |
| `kim` (เฮียกิม) | slim 0.50 x 0.98, legs 1.16 | white wiry hair standing straight up, round wire glasses, grey brush moustache, age lines; cream rib singlet, khaki shorts, tool pouch, sandals | cream / khaki |
| `nurse` | slim hourglass 0.52 x 0.90, legs 1.14 | white cap with a red cross, dark bun; white dress with light-blue piping and belt, name tag, fob watch, A-line skirt; white shoes | white |
| `nb_man` | regular, pear belly 0.84 x 1.00 | black flat-top; green football jersey, red-check pha khao ma tied at the waist, navy shorts, flip-flops | green |
| `nb_woman` | slim hourglass 0.54 x 0.92 | long black hair with a fringe and a yellow clip; yellow tee, long indigo batik sarong, red sandals | yellow + indigo |

## New pose keys (read by the hooks; puppet's own normaliser ignores them, so `lerp_pose` / `resolve_pose` drop them: copy them back yourself)

| key | values | effect |
|---|---|---|
| `hair_state` | `"normal"` / `"bolt"` | welder, nurse: hair blown straight up into jagged lightning spikes (the nurse's cap floats on top) |
| `bolt_sparks` | bool, default True | small yellow spark marks around bolt hair |
| `mask` | None / `"down"` / `"up"` | welder's welding mask: down covers the face (green glass slit), up sits on the crown |
| `zap` | list of `"hair"`, `"finger_r"`, `"finger_l"`, `"torch_r"`, `"torch_l"`, `"body"` | electric effects: crackle around the hair; spark burst at the fingertip or prop tip; welding arc with glow and a spray of sparks at the torch nozzle; yellow body glow with zigzag bolts. `t` (0..1) flickers them |
| `hug_trunk` | True or `{"x": torso-local x, "w": width}` | a tree trunk with a three-colour sash drawn in front of the torso, under the arms (scenery, not counted in bbox) |
| `stool` | bool | red plastic soi stool under the hips; pair it with sitting legs (see `welder_sit_stool`) |

New expression: `scream` (ring eyes with tiny pupils, raised brows, mouth open 0.30 x 0.20).
New arm presets (every build): `fist_up`, `up_point` (both drawn over the hair), `finger_up`, `cup_mouth`, `cheeks`, `crossed`, `fists`, `torch`, `hold`.
New props (`prop_r` / `prop_l`): `torch` (red hose hangs from the grip), `calculator`, `cash` (fan of Thai notes, always upright), `handfan`, `screwdriver` (red handle), `phone` (screen to camera). Tips are in `puppet.PROP_TIP`.

## Named poses: `lt_cast.POSES` (also merged into `puppet.STORY`)

welder: `welder_idle` (mask up, torch), `welder_idle_bolt`, `welder_welding`, `welder_shocked`, `welder_proud`, `welder_point_spark`, `welder_sad`, `welder_angry`, `welder_hug_tree`, `welder_sit_stool`.
hong: `hong_idle_fan`, `hong_shout_up`, `hong_count_money`, `hong_crossed_smug`, `hong_angry_shout`, `hong_calculator`.
kim: `kim_explain`, `kim_shout_cupped`, `kim_point`. nurse: `nurse_idle`, `nurse_surprise`, `nurse_bolt`. neighbours: `nb_man_phone`, `nb_woman_phone`.

## Sprite cards (transparent PNG)

```python
info = lt_cast.render_png("welder", pose, "out.png", 512)                  # one card
infos = lt_cast.render_pngs([{"name": ..., "pose": ..., "out": ..., "height_px": 512}, ...])   # many, one Chromium launch
svg, info = lt_cast.sprite_svg(name, pose, 512)                             # SVG text only
# info: w, h, D_px, feet_px (pixel of the sole point), anchors_px, ms_per_png
```

`fit="canvas"` (default) uses the member's fixed feet-relative canvas `lt_cast.CANVAS` (also put into `sprites.DEFAULT_CANVAS` through cast_ext). D in pixels and the feet pixel are therefore the same in every frame, so cards do not swim: in Blender, pin the card's pivot at `feet_px`. A 512 px card gives D of about 115 to 122 px. `fit="bbox"` crops tightly around one pose instead.

Time per card (512 px, this container): `figure()` 1.3 ms. `render_png` alone is about 0.55 s, mostly the Chromium launch. `render_pngs` takes about 110 ms per PNG for a batch of 24 including the one launch, and about 90 ms per PNG after the launch. `python3 lt_cast.py bench` measures it again.

## Command line / QA

```
python3 lt_cast.py lineup   # lineup.png + lineup_s.jpg: 7 columns (welder twice: normal and bolt), D 110 and 220, night #4a4a8a and soi #d8c8b0
python3 lt_cast.py poses    # poses.png + poses_s.jpg: 24 named poses, then 9 head rows x (7 expressions + 3/4 view)
python3 lt_cast.py png welder_shocked out.png 512
python3 lt_cast.py test     # v2 test_puppet.py --quick on the 6 names: 2,045,546 checks, 0 failed (+ determinism)
python3 lt_cast.py canvas   # re-derives the sprite canvases from a pose sweep
python3 lt_cast.py bench
```

On the night background the sheets pass `rim="#9a9ae0"`, because ink limbs nearly vanish on `#4a4a8a`. Do the same on night sprite cards, or light the set so that a mid value sits behind the legs.

## Hooks (for maintainers)
The module adds its costumes to `cast_ext.COSTUMES` and its hair, hat and mask styles to `cast_ext.HATS`. It wraps `puppet._norm` (to record the raw pose), `_torso` (trunk), `_face` (scream mouth), `_moustache` (`brush`), `_ink_limb` (sleeves, shorts legs, boots, sandals, shoes) and `_prop`, and replaces `puppet.figure` with a wrapper that adds the `zap` and `stool` overlays. Every wrapper falls through to the previous function for every member outside this cast. A caller that grabbed `puppet.figure` before importing lt_cast does not get the overlays.
