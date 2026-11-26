# v8/cast: the DEAD ZONE 09 cast as sheet-style 2.5D paper puppets, lit by the v6 set

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/v8/cast/`.
Only this folder was written. Read-only imports: `v3/stage/sprites.py` (the Chromium SVG rasteriser page), `v6/set` (beauty, render6, presets, kit), `v4/set_expressway` (through v6). `look8.py` is a copy of `v6/look/look.py`; `phone8.py` is a copy of `v4/cast_dz09/phone25.py`. Nothing in v2/v4/v6 was edited.

Every character is drawn by code as SVG layers (no image generation, no paid API). Target look: `uploads/character_sheet.webp`, bands from `spec/sheet_proportions.md`.

## Files

| file | what |
|---|---|
| `draw8.py` | Pure Python drawing. Specs `SPECS["kong" / "kong_wet" / "crew" / "crew_wet" / "driver" / "namnuea"]`, `extras(n, seed)`, `build(spec, pose)` -> layers. Views front / q (3/4) / side / back. Expressions, lip-sync mouth, blink, IK arms and legs, props (cutter, phone, umbrella, bag, helmet), wet variants. |
| `raster8.py` | SVG -> RGBA PNG (Chromium page, SHA-1 cache in `tmp/_cache`), crop to the opaque box, and the per-layer pseudo-normal map (distance transform -> round height profile -> normals; head = sphere dome, face uses the head dome). |
| `stage8.py` | bpy: `Actor8` (layer cards, shared lit card shader `DZ8_card`, shadow proxy, contact/AO decal), `shadow_link()`, `tune()`, `view_for()`. |
| `gait8.py` | Walk and run cycles with planted feet (`Gait(spec, "walk" / "run").pose(t, s, view)`). |
| `walk8.py` | Kong walking 3 s in the v6 set, camera tracking from the front 3/4; foot-drift measurement. |
| `look8.py` | Copy of v6 `look.py` with the puppets swapped in: S06, S13, S20 (same marks, camera formulas, post options). `sheet` writes `in_v6.png`. |
| `lookdev8.py` | Lookdev renders (`neutral`, `seated`, `night`), `sheet` -> `lookdev.png`, `sbs` -> `side_by_side.png`. |
| `measure8.py` | Re-measures the sheet proportions on our Cycles renders -> `out/measure.json`, `out/measure_table.md`, `out/measure/*_measured.png`. |
| `shade_cmp.py` | Shading depth of the actors, v6 bean frame vs v8 frame, same shot -> `out/shade_cmp.json`. |
| `phone8.py` | Phone screen (Namnuea avatar drawn by draw8, Thai line set with libraqm in Kanit, glyph check) -> `tex/phone_screen.png`. |
| `neutral8.py` | Neutral lookdev stage (grey floor, soft key, cool fill, red/orange rim practical). |
| Deliverables | `side_by_side.png`, `lookdev.png`, `in_v6.png`, `walk_kong.mp4`, `out/walk_drift.json`, `out/walk_render.json`, `out/run_drift.json`. |

## Units

- Drawing: 1 D = bare head width including the outline. Figure frame x right, y down, soles at y = 0.
- Set: 1 BU = 0.6 m (v6). `Actor8(height=...)` is soles to hair top in BU; Kong 2.86 BU = 1.72 m (v6's Kong height), so D = 0.664 BU = 0.40 m.
- Facing: 0 faces -Y (v6 convention), +90 faces +X. `s = +1`: the drawing faces screen-right.

## Quick start (inside the v6 set)

```python
import sys; sys.path.insert(0, PROJ + "/v6/set"); sys.path.insert(0, PROJ + "/v8/cast")
import bpy, beauty as B, stage8 as S
A = B.build(); B.setup_render("final", threads=4)
bpy.context.scene.cycles.transparent_max_bounces = 32           # stacked alpha cards
k = S.Actor8("kong", "kong_wet", height=2.86); k.set_pass_index(2)
k.place(A["kong_mark"], facing_deg=30)
cam = ...                                                         # make the camera first: the drawing view follows it
k.pose(dict(expr="determined", arm_n="hold_cutter", prop_n=dict(type="cutter", bars=3, wet=True), legs="wide"), camera=cam)
S.shadow_link([k], key_light)                                     # which light the cast shadow comes from (look8.dominant_light)
B.render6.render(out_noext, frame=7, post_opts={"exposure": 1.6, "sharp_idx": [2]})
k.head_world(); k.foot_world("L"); k.sole_world("leg_L"); k.objects; k.hide(True)
```

Call `pose()` again whenever the camera or the actor moves (the drawing bin and the card turn follow the camera). Only changed layers are re-rasterised (cache).

### Actor8(name, spec, height=2.86, ppd=200, gap=0.05, follow=1.0, pass_index=2, contact=True)

- `spec`: a name from `draw8.SPECS` or a spec dict (e.g. from `draw8.extras()`).
- `ppd`: sprite pixels per D (200 is enough for a 300 px head; 300 for close-ups).
- `gap`: layer spacing in D (0.05 D = 2 cm on Kong). The stack, pack to near arm, is 0.28 D = 11 cm deep: real parallax under a moving camera.
- `follow`: how far the card stack turns toward the camera (stills 1.0). `walk_lock` (degrees) pins the cards to the motion plane for walking (set by `walk8`).
- `view_override`: force `"front" | "q" | "side" | "back"`. Otherwise `view_for(rel)`: front below 20 deg camera-relative yaw, q below 52, side below 128, back beyond.

### Pose keys (draw8.build)

| key | values |
|---|---|
| `view`, `s` | set by Actor8 from the camera, or forced |
| `expr` | Kong: `determined` (sheet), `neutral`, `tired`, `guilty`, `alarmed`, `shouting`, `blink`. Crew: `neutral`, `shouting`, `scared`, `blink`. Driver: `still`, `head_lift`, `lunge`, `bite`. Extras: also `smile worried joy stern sad talk angry surprised`. |
| `mouth` | lip sync: a level 0..1 (open D-shape height 0.035 + 0.17 x level D, teeth from 0.55) or `(shape, level)` with shape `a / o / e` |
| `blink` | 0 open, 1 half, 2 closed |
| `gaze` | (dx, dy) pupil shift |
| `head` | (yaw_extra deg, tilt deg, dx D, dy D) |
| `lean` | upper-body lean, degrees, + toward the facing side |
| `hip` | (dx, dy) hip offset (bob / crouch) |
| `arm_r / arm_l` (front, back) or `arm_n / arm_f` (q, side) | preset `down hang hips hold_cutter phone_ear phone_look point raise wave reach claw claw_up lap wheel cross head pocket carry umbrella shout guard`, or `dict(hand=(dx, dy), elbow=+1/-1, hand_shape="glove/grip/claw/point/open/hand")` relative to the shoulder (+dx outward / forward) |
| `legs` | preset `stand wide step lunge crouch`, `dict(seated=True)`, or `dict(foot_n=(x, y), foot_f=(x, y), toe_n, toe_f)` (sole points, figure frame) |
| `prop_r / prop_l / prop_n / prop_f` | `dict(type="cutter", bars=3/2/1/0, wet)`, `dict(type="phone", screen=<data URI>, scale)`, `umbrella`, `bag`, `helmet` |

Near/far: in q and side drawings facing screen-right the near limbs are the character's LEFT limbs.

### Layers and depth (gap units, + toward the camera)

front: pack -3, leg_R -1.2, leg_L -1.0, torso 0, head 1, face 1.35, hair 1.7, prop_R 2.2, arm_R 2.3, prop_L 2.35, arm_L 2.45.
q / side: pack -3, far prop -2.3, far arm -2, far leg -1.2, near leg -0.6, torso 0, head 1, face 1.35, hair 1.7, near prop 2.3, near arm 2.5.
back: the pack comes to +0.6 (in front of the torso), the face is not drawn, the hair covers the back of the head.

### Card shader (node group `DZ8_card`, shared; `S.tune(AMB=, TOON=, NSTR=, WET=)`)

`base` = the drawn colour. `lit = mix(Diffuse(base, N), Toon(base, N, size 0.5, smooth 0.10), 0.35)` with N from the layer's pseudo-normal map, so every scene light and every scene shadow shades each layer as a rounded form (soft gradient plus a toon terminator). `+ Emission(base x (0.80, 0.80, 0.98) x AMB)` keeps a bold flat-colour floor with a blue-violet cast; AMB = 0.32 (in-set), 0.30 (neutral). Wet specs add `Glossy(0.32) x 0.035`. Everything multiplies the base colour, so ink, hair and black cloth stay black; red/orange practicals rim the outward-tilted edge normals. Alpha-cut with Transparent.

Pseudo-normal radius per layer (D): head = its radius (sphere), face = the head sphere, torso 0.48 (front) / 0.42 (q, side), legs 0.20, arms 0.12, hair 0.16, pack 0.22, props 0.07.

### Shadows

Layer cards do not cast shadows (no self-shadow artifacts between cards 2 cm apart). One hidden proxy card per actor carries the flat silhouette, faces the shadow light horizontally and sits 0.35 D downstream of it, so the actor's own cards are never in its shadow; `shadow_link()` puts the proxies in a blocker collection excluded from every other light (Cycles shadow linking). A soft radial contact/AO decal sits under the feet. Cards receive all scene shadows.

## Cast (draw8)

| spec | build |
|---|---|
| `kong` | 4.31 D tall. Spiky black clump hair (6 clumps, fringe 0.3 D into the face), solid oval eyes 0.08 x 0.20 D, 0.31 D apart, angled bar brows, smile, 11 stubble ticks on the jaw (45-136 deg). Orange short-sleeve rescue shirt with big pointed collar, dark undershirt V, black RESCUE chest panel, grey reflective band, harness straps, chest radio with antenna to chin height, Thai flag on the right sleeve (screen-left), backpack showing screen-left, black belt with light buckle, hip pouch and orange-tabbed holster, wide dark cargo trousers with thigh pouch + strap and knee pads, chunky lace-up boots 0.64 D, white stick forearms, big black gloves. |
| `kong_wet` | darker shirt `#c8581b`, darker trousers and boots, drooping hair with a sheen line and drops, rain drops on the face, glossy card term. |
| `crew` / `crew_wet` | James's proportions (4.49 D), same uniform with long sleeves and no pack, tall dark-brown crest hair (different from Kong's), no stubble, eyes 0.40 D apart, smaller brows under the fringe. |
| `driver` | Khun Tos's build (4.22 D, shoulders 0.82 D, no glasses), pale grey-green skin `#c4cdb2`, side-swept dark hair, white eyes with tiny red pupils and dark under-eye lines, torn light-blue office shirt (rips, stains, jagged hem), loosened red tie, grey slacks, brown belt, low shoes, claw hands. Poses: seated still, head lift, lunge, bite (lookdev row 5). |
| `extras(n=10)` | 10 roles: delivery rider (green jacket, green box with scooter logo, helmet), office woman on the phone, older grey-haired man (moustache, round glasses), teen in a hoodie pointing, auntie with a red umbrella, taxi driver in a cap waving, student with a ponytail (scared), young man in a tee with a phone, bald man with a bag (rect glasses, tie), woman with long hair. `_check_unique` raises unless face, hair, clothes colour and pose all differ. |

## Walk and run (gait8, walk8)

The root moves at constant speed; a planted foot is drawn at `x_land - v (t - t_land)` on a card that lies in the motion plane (`walk_lock`), so it is a fixed world point. The hip is lowered when needed so every planted ankle is reachable by the fixed-length leg (the IK never pulls a planted foot); bone lengths never change with the bob. Arms swing opposite the legs; the run has a flight phase, 12 deg lean and pumping bent arms.

| | period | stance | step | speed |
|---|---|---|---|---|
| walk | 0.92 s | 60 % | 0.70 D | 1.52 D/s = 0.61 m/s (tired plod) |
| run | 0.62 s | 36 % | 1.05 D | 3.39 D/s = 1.36 m/s (jog) |

Foot drift is measured on the drawn sprite: the centre of the lowest three opaque rows of each leg layer, mapped through the card's world matrix, every frame of every stance, compared with the stance's first frame. See the measured table below.

## Measured

### Proportions, re-measured on our Cycles renders (`measure8.py`, front drawing, orthographic, figure 1100 px tall)

Bands = sheet value +/- 6 % (`spec/sheet_proportions.md`). All 45 banded values are inside their band ("ok"). The crew is compared with James, the driver with Khun Tos. After the review the crew legs are 1.74 D (were 1.83: legs / D 1.910 at the top of the band and head / total 0.217); now head / total 0.222 and legs / D 1.813 against James 0.223 / 1.809. Shoulder + pack span is our backpack at the side; James's 1.65 is his delivery box, so the crew has no value.

| measure | Kong sheet | Kong ours | crew vs James sheet | crew ours | driver vs Tos sheet | driver ours |
|---|---|---|---|---|---|---|
| bare head D / total | 0.232 | 0.232 ok | 0.223 | 0.222 ok | 0.237 | 0.235 ok |
| hair top to chin / total | 0.271 | 0.268 ok | 0.279 | 0.282 ok | 0.278 | 0.277 ok |
| figure height in bare heads | 4.307 | 4.319 ok | 4.491 | 4.509 ok | 4.215 | 4.252 ok |
| hair above skull / D | 0.165 | 0.156 ok | 0.253 | 0.259 ok | 0.172 | 0.175 ok |
| hair vertical extent / D | 0.724 | 0.747 ok | 0.900 | 0.948 ok | 0.785 | 0.751 ok |
| hair width / D | 1.236 | 1.286 ok | 1.260 | 1.323 ok | 1.174 | 1.233 ok |
| shoulder width / D | 1.323 | 1.337 ok | 0.936 | 0.964 ok | 0.818 | 0.827 ok |
| shoulders + pack / D | 1.441 | 1.369 ok | 1.647 | - | - | - |
| torso chin-crotch / total | 0.333 | 0.326 ok | 0.316 | 0.315 ok | 0.310 | 0.303 ok |
| torso / D | 1.433 | 1.408 ok | 1.420 | 1.421 ok | 1.307 | 1.287 ok |
| legs crotch-sole / total | 0.395 | 0.405 ok | 0.403 | 0.402 ok | 0.410 | 0.419 ok |
| legs / D | 1.701 | 1.751 ok | 1.809 | 1.813 ok | 1.727 | 1.781 ok |
| trouser leg width / D | 0.441 | 0.456 ok | 0.333 | 0.340 ok | 0.306 | 0.303 ok |
| hand width / D | 0.331 | 0.319 ok | 0.297 | 0.295 ok | - | 0.202 |
| boot/shoe height / D | 0.654 | 0.668 ok | 0.495 | 0.505 ok | 0.322 | 0.316 ok |
| head outline median / D | 0.038 | 0.039 ok | 0.044 | 0.045 ok | 0.039 | 0.037 ok |

Method: total height = silhouette top to sole; D = mean of a circle fit on the lower head contour (residual 0.4 px) and the widest head row; crotch = first opaque row above the gap between the legs on the body centre column; shoulder span = torso + arm layers (ID render) in the band chin + 0.05 to chin + 0.45 D. Boot top, glove width, trouser-leg width and head outline are measured on the layer sprites by their palette and mapped through the card scale. Annotated images: `out/measure/<name>_measured.png`.

### Feet (walk8.py)

| | stances measured | max drift of a planted foot | root travel during one stance (what a sliding foot would show) |
|---|---|---|---|
| walk, 72 frames, rendered in the set | 8 | **0.06 cm** | 33.8 cm |
| run, 72 frames (geometry only) | 10 | **0.06 cm** | 30.4 cm |

Drift is the sole point measured on the rasterised leg sprite (lowest 3 opaque rows), so the residue is pixel quantisation. `out/walk_render.json` / `out/walk_drift.json` / `out/run_drift.json` hold every frame.

### Shading depth vs the v6 bean characters (`shade_cmp.py`, `out/shade_cmp.json`, same shot, graded frame)

depth = 1 - L_p10 / L_p90 inside the class (how far the shadow side falls below the lit side).

| shot | head v6 | head v8 | orange cloth v6 | orange cloth v8 |
|---|---|---|---|---|
| S06 | 0.56 | 0.49 | 0.59 | 0.71 |
| S13 | 0.64 | 0.59 | 0.66 | 0.44 |
| S20 (driver head) | 0.15 | 0.19 | - | - |

### Render cost (4 threads, Cycles CPU, v6 `final` quality)

| render | res | CPU s render + post | wall s |
|---|---|---|---|
| S06 / S13 / S20 in the v6 set (`look8.py`) | 720x1280 | 25.6 + 2.8 / 29.0 + 3.3 / 22.6 + 2.8 | 7.0 / 7.8 / 6.4 (+ 1-4 s pose and raster) |
| walk frame in the v6 set | 360x640 | 8.3 + 0.6 | 3.6 incl. pose + raster |
| lookdev in the set | 360x640 | 7.2-7.7 | 2.7 |
| neutral lookdev (24 spp + OIDN) | 480x800 | - | median 4.2 |

For reference v6 `look.py` with the bean cast: 8-12 CPU s at 360x640. Rasterising a changed pose costs about 0.1 s per layer (Chromium page, cached by SHA-1).

## Commands

```
python3 measure8.py                       # proportions -> out/measure.json, out/measure_table.md
python3 lookdev8.py neutral | phone | seated | night | sheet | sbs
python3 look8.py render --scale 1.0 ; python3 look8.py sheet
python3 walk8.py measure [--kind run] ; python3 walk8.py render --frames 72 --scale 0.5
python3 shade_cmp.py s06 s13 s20
python3 phone8.py                         # Thai glyph check: 21 characters, no notdef, no blank
```

## Gaps

- Turning is three drawn bins (front, q, side) plus a back drawing; swaps pop at 20 / 52 / 128 deg. The side drawing keeps the round head with features near the edge, as in the sheet's style; it is the weakest view (small features, hair at the back has a double spike).
- The walk uses the q drawing on cards in the motion plane, so from a front 3/4 camera the cards are seen about 40 deg off-axis (narrower figure). Planted feet need that; stills turn the cards to face the camera.
- Cast shadows come from one proxy silhouette per actor and one chosen light (`look8.dominant_light`); other lights do not get a proxy shadow. There is no shadow between layer cards (no self-shadow under the chin); the contact decal stands in for foot AO.
- S13: the orange cloth is flatter than the v6 bean (depth 0.47 against 0.66) because the cloth layers are pillows, not a full body volume. Raise `TOON` or the torso normal radius in `draw8` if wanted. Our heads are 0.81x the v6 bean head (sheet proportions), so the S13 MCU shows more body for the same camera.
- S20: the seated driver is drawn at 2.03 BU (smaller than Kong) so his head fits under the sedan roof with the approved camera, as v6 did (DRV_S 0.58).
- The night lookdev is placed at an open patch found by ray casts (`lookdev8.find_spot`, (5.2, 36.0)); figures fill about half the frame height.
- Phone: readable in an insert (`out/lookdev/prop_phone.png`, sprite 900 ppd) but not at body scale in S13; use an insert for the Thai line.
- Hands are mittens and gloves; fingers only for claw, point and open hands. The cutter's D-handle loops over the glove instead of a true grip.
- Not done: a blink/expression timeline helper (blink and mouth are pose keys per frame), the run cycle render (geometry and drift only), 16:9 versions of the three look shots.

## Review pass (independent review, after the builder report)

Defects found and fixed (all in this folder):

1. Wet gloss made black go tan: the card shader's Glossy term was added untinted, so the moon disc reflected in Kong's
   wet hair (S06 crown up to rgb 194,159,115, brows brown).  The gloss is now multiplied by the drawn colour
   (`DZ8_card`: Mix.001/.002); S06 crown raw 70,57,47 -> 36,32,33.  Also added an ink guard on the lit colour
   (`TUNE INK_LUM 0.035, INK_MIN 0.35`: near-black paint keeps at most a third of direct light; colours untouched).
2. Wet-hair sheen: one grey arc over the crown read as a headband (S13).  Now three short sheen ticks on the clumps.
3. Crew hair was dark brown (`#2a1c15`); the sheet (James) and the brief want ink-black clumps.  Now `#1d1d1d`.
4. Crew face was weak: brows hidden under the crest fringe, neutral mouth a 0.13 D dash.  Brows (0.20 x 0.046 D)
   now ride on the hair card with a thin skin halo (`face.brow_over_hair`), eyes 0.08 x 0.18 D, neutral mouth line
   0.9 x mouth_w (all specs; was 0.66), crew mouth_w 0.26 D.  New crew expression `joy` (the sheet's James face),
   used in side_by_side.png.
5. Crew chest text clipped to "RESCU" by the arm in the front view: the panel is narrower on narrow torsos.
6. Crew head too small for James (head / total 0.217, legs / D 1.91 at the top of the band): legs 1.83 -> 1.74 D.
7. Shadow proxy was shifted 0.35 D (14 cm) downstream of its light, so every cast shadow started 14 cm away from the
   soles.  The proxy now stands on the sole line and leans `PROXY_TILT` = 24 deg away from the light: attached at the
   feet, behind the card stack above the boots (no self-shadow on the upper cards).
8. walk8 never called `shadow_link`, so the walker's proxy cast from every lamp including the low camera fill.  It
   now uses one light chosen at the middle of the path (`moon_key`, recorded in `out/walk_render.json`).
   (The dark blob in front of the feet in the old walk is a wet-road patch of the set, not a shadow: it is there with
   the actor hidden.)

Re-measured after the fixes: proportions on fresh `measure8.py` renders (table above; an independent mask-based
re-measure gives Kong / crew / driver head/total 0.230 / 0.216 / 0.234, hair-top-to-chin/total 0.269 / 0.283 / 0.278, shoulder/D 1.35 / 0.98 / 0.83 (widest head row, so D reads about 2 % low));
walk drift 0.059 cm (independent pairwise spread inside each stance 0.061 / 0.070 cm, drawn anchors 0.000 cm);
run drift 0.060 cm; extras: no pair shares face, hair or clothes; phone line 21 chars, no notdef, no blank.

---

# Flat mode (reference E staging) — the film default

`stage8.MODE = "flat"`. Notes and measurements: `PROJ/spec/refE_chars.md`. The earlier look is still there as `mode="round"`.

## What changed in the API (all additions; old calls still run)

- `Actor8(name, spec, height, ppd, gap=None, follow, pass_index, contact, mode=None)`
  - `mode`: `"flat"` or `"round"`. None takes `stage8.MODE` (flat). `stage8.set_mode("round")` switches the default back.
  - `gap=None`: 0.03 D in flat mode, 0.05 D in round mode. `follow` is ignored in flat mode (always 1).
- Flat-mode behaviour of `pose(pose, camera=cam)`:
  - Yaw: the card set faces the camera. The drawing (front / q / side / back) is picked from the camera angle as before.
  - Pitch: the card set is turned parallel to the camera sensor, clamped to `FLAT["PITCH_MAX"]` (40 degrees), about the sole line.
    `actor.pitch_anchor = 0.6` turns it about 60 % of the height instead (use for a seated actor). `actor.pitch_override = deg`
    fixes it. The applied value is in `actor.pitch`.
  - For a true top-down camera the clamp leaves a skew: stage the actor small, or raise `PITCH_MAX`.
  - `walk_lock` still pins the yaw if a caller sets it (walk8 does); leave it None to keep walkers camera-facing.
- `stage8.tune_flat(**kw)`: the shared flat look. Keys and defaults (`stage8.FLAT`, a copy in `stage8.FLAT_DEFAULT`):

  | Key | Default | Meaning |
  |---|---|---|
  | `AMB` | 0.23 | even emissive fill, at exposure 1 |
  | `TINT` | (0.30, 0.45, 1.0) | linear colour of that fill: the scene's shade colour |
  | `EXPO` | 1.0 | the shot's `post_opts["exposure"]`; the fill and glow are divided by it so they grade the same in every shot |
  | `DIR` | 0.20 | share of real scene light on the flat card (set shadows cut across the drawing) |
  | `BACK` | 0.10 | share of light arriving from behind the card |
  | `NSTR` | 0.0 | normal-map strength; 0 = no rounding |
  | `INK_LUM`, `INK_MIN` | 0.014, 0.25 | near-black paint keeps a quarter of the direct light |
  | `GLOW`, `GLOW_COL`, `GLOW_R` | 0.20, (0.70, 0.82, 1.0), 0.16 D | halo behind the figure |
  | `PITCH`, `PITCH_MAX` | 1.0, 40 | pitch gain and clamp |
  | `SELF_R` | 0.45 | radius (in actor heights) inside which the shadow proxy does not shade points above the ground: no self-shadow on the cards |
  | `GAP` | 0.03 | default card spacing in D |

  Per shot: `S.tune_flat(**dict(S.FLAT_DEFAULT, EXPO=post["exposure"]))`, then any override (dark cabin: `AMB=0.40, TINT=(0.72, 0.84, 1.0)`).
- `actor.set_glow(color=None, strength=None)`: halo colour and strength for one actor (warm lamp behind: `(1.0, 0.72, 0.45)`; 0 = off).
  The halo quad is `actor.glow`; it is in `actor.objects`, camera-visible only.
- Shadows: unchanged calls (`shadow_link`, `set_shadow_light`). The proxy stands on the sole line, so the cast shadow starts at the
  feet; the contact decal stays under the feet. A deleted shadow light (a rebuilt work lamp) is now dropped instead of raising.
  Call `shadow_link` again after `beauty.place_work_lamp`.

## New files

| File | What |
|---|---|
| `flat9.py` | S06 / S13 / S20 in the v9 set in flat mode (`render`, `sheet` -> `flat_in_v9.png`); `--only cal` is S13 with the work lamp off |
| `flat9_measure.py` | face / costume / surround samples of those frames -> `out/flat9/measure.json` |
| `flat_test.py` | neutral stage, eye / low / high camera, flat against round -> `tmp/flat/flat_test.png`, `out/flat_test.json` |
| `refE_measure.py` | the reference E samples -> `out/refE_measure.json` |
| `audit8.py` | flat drawings of every view and key pose (`kong`, `crew`, `driver`, `extras`) and `sbs` -> `side_by_side.png` |

## Costume audit against the character sheet (draw8)

- Thai flag patch: stripes were vertical. Now horizontal red, white, blue (double), white, red; the patch tilts at most 22 degrees with the arm.
- Radio (Kong): larger (0.25 x 0.40 D), on the screen-right strap at collar-bone height, thick antenna, blue display, keys.
- Backpack straps: black straps from beside the collar down the chest to under the arms (they were hidden under the sleeves).
- Reflective band: moved low on the jacket, grey centre with light edges. Front and back.
- RESCUE patch: sits between the straps; the back panel is narrower on the crew so the arms no longer cut it to "ESCU".
- Hair: deeper notches between the clumps, the sheet's cowlick on dry Kong, and a spiky back view (it was a smooth cap).
- Wet trousers: 14 % darker than dry (was 30 %), so pockets and knee pads still read at night.
- Rain beads: never on an eye (one read as a tear); the hair beads sit on the hair.
- Cutter: lighter silver jaws. Orange body, black D-handle, white band, 3 green bars unchanged.
- Driver: shirt white (#eef1f3), tie dark red (#7d1d22), slacks grey (#73767d); the back view no longer shows the tie and buttons.
- Crew: neutral is the default expression; `joy` stays as an option. `side_by_side.png` now shows the neutral face.
