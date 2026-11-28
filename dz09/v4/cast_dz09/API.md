# v4/cast_dz09: the DEAD ZONE 09 cast as 2.5D layered puppets

Folder: `PROJ/v4/cast_dz09/` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`).
Nothing outside this folder is edited. v2 `puppet.py` (path helpers, CAST/STORY registry), v3 `stage/sprites.py` (the persistent Chromium page) and v3 `tools/hue_report.py` are imported read-only.

User direction: characters are 2.5D, sets are 3D. Every character keeps the flat, hand-drawn look of `uploads/character_sheet.webp` (ink outline, flat fills, simple faces). It is built as a stack of separate drawn layers on parallel cards a few centimetres apart in depth, so a moving camera shows real parallax between body parts.

## Files

| File | What it does |
|---|---|
| `draw25d.py` | Pure Python. Draws the cast as layers (SVG, D units, v2 conventions). Covers views, expressions, arm and leg presets, props, wet variants. |
| `raster25.py` | Turns layer SVGs into RGBA PNGs through the v3 Chromium page (cached by SHA-1). Also writes the per-layer pseudo-normal map that the toon shader uses. |
| `stage25.py` | The bpy part: `Actor25` (layer cards, shadow proxy, contact decal), the shared toon node group, `sync_lights`, `setup_render`. |
| `cast25.py` | Registers the cast in v2 `puppet` using the v3 `cast_ext` pattern: `puppet.figure("kong", pose)` returns the flat composite and STORY poses `dz_*`. |
| `phone25.py` | The phone screen: Namnuea's photo plus `น้ำเหนือ — 4 สายที่ไม่ได้รับ`, set in Kanit with libraqm, with a glyph check. |
| `testset.py` | A small lit test stage, not the EP.1 set. It has wet expressway asphalt with puddles, lane paint, a concrete barrier, 5 crashed cars, a rescue pickup with a red beacon, a sodium lamp, a cool moon and rain streaks. |
| `orbit_test.py` | Proof renders: `still`, `compare` (flat vs 2.5D) and `orbit` (MP4). |
| `sheet25.py` | Contact sheet next to a crop of the character sheet and a ref/c puppet. Also draws the exploded layer stack. |
| `measure25.py` | Measures `parallax` (px), `hue` (rows from hue_report) and `lines` (ink width compared with ref/c). |
| `out/` | Deliverables (below). `tmp/` holds the sprite cache, frames and drafts. |

## 1. Drawing layers (`draw25d`)

```python
import sys; sys.path.insert(0, PROJ + "/v4/cast_dz09"); import draw25d
fig = draw25d.build("kong", {"yaw": 0.5, "expr": "alarmed", "arm_l": "hold",
                             "prop_l": {"type": "cutter", "angle": 96, "bars": 3}})
fig["layers"]   # back to front: {"name", "svg", "z" (depth in gap units, + = toward the viewer), "kind", "shade", "rim"}
fig["feet"], fig["seat"], fig["anchors"], fig["view"], fig["s"], fig["bbox"]
svg = draw25d.flat_svg(fig)                # all layers on one sheet (2D-flat baseline)
```

Cast (`draw25d.CAST25`):

| name | what |
|---|---|
| `kong` | 38. Round white head, tall spiky black hair, stubble dots, determined brows. Orange rescue jacket with two silver reflective bands on body and sleeves, black `RESCUE` chest patch, Thai flag patch on the screen-left sleeve, chest radio with antenna, backpack and straps, collar, belt and buckle. Black cargo trousers with thigh pockets, boots, black gloves. 3.3 D tall. |
| `kong_wet` | Same, wet: darker fabric (jacket `#c8581b`, trousers `#1f1f25`), flatter drooping hair with a sheen line, drips on the hem, hands, hair and trouser streaks. The shader adds specular glints (`Wet` = 1). |
| `crew`, `crew_wet` | Young crew member in the same uniform: no backpack, no stubble, brown hair swept to one side with a long fringe, slimmer build. |
| `driver` | Infected driver. Pale grey-green skin `#b8c3a8`, white eyes with tiny red pupils, dark under-eye lines, thin messy hair. Torn light-blue shirt with a jagged hem, rips and collar stains, loosened tie, grey trousers, claw fingers. |
| `namnuea` | 14, for the phone photo. Ponytail with a red tie, maroon hoodie, grey trousers, red shoes, backpack straps, blush. |

Pose keys:

- `yaw` runs from -1.2 to 1.2. Drawing bins (`VIEW_EDGES` = 0.30 and 0.80): front, three-quarter `q`, side. In a bin the drawing is fixed, and the drawings swap between bins. The stage maps the camera-relative yaw at ±60° to ±1 (`stage25.YAW_RANGE_DEG`), so the swaps fall at 18° and 48° with ±0.04 hysteresis (review: it was ±35°, which put a full profile on screen at a 28° camera offset). `view` forces a drawing.
- Other keys: `expr`, `blink` (0/1/2), `mouth` (talk_a, talk_b, talk_o, shout, flat ...), `gaze`, `lean` (degrees, the upper body turns about the hips), `head_roll`, `head_dx`, `head_dy`, `uid`.
- `arm_r` / `arm_l` take a preset: `down hold phone_ear phone_look point raise reach push guard lap wheel claw drag wave`. Or a dict `{"hand": (x, y), "pref": (dx, dy)}`. The arms use two-bone IK.
- `legs` takes a preset: `stand wide step lunge seated crouch`. Or a dict `{"preset", "crouch", "foot_r", "foot_l"}`.
- `prop_r` / `prop_l` take `"cutter" | "crowbar" | "phone" | "medkit"` or a dict `{"type", "angle", "scale", ...}`.
  - cutter: `bars` 0 to 3 for the battery indicator (green 3, yellow 2, red 1). The indicator sits on top of the orange body in front of the hand, 0.29 x 0.11 D (review: it was 0.17 x 0.07 D on the pack under the glove).
  - phone: `screen_png` (a data URI from `phone25.data_uri`) and `tilt`. The phone always stays upright.

Expressions:

| who | expressions |
|---|---|
| Kong | `neutral determined tired guilty alarmed shouting talk blink` |
| crew | `neutral alarmed shouting pain` |
| infected | `still` (slit eyes, slack), `head_lift` (white eyes, red pupils), `lunge` (wide eyes, open biting mouth with teeth) |
| Namnuea | `smile neutral sad` |

Layers and their depth, in gap units, with `s` = facing sign:

| view | layer depths |
|---|---|
| front | pack -2.4, legs -1.0 / -0.88, torso 0, head 1, face 1.5, hair 2, props 2.3, arms 2.6 / 2.72 |
| q / side | pack -2.4, far prop -1.9, far arm -1.6, far leg -1.1, near leg -0.5, torso 0, head 1, face 1.5, hair 2, near prop 2.3, near arm 2.6 |
| seated | the near thigh comes to +0.6 |

- Far and near follow the yaw: facing screen-right, the screen-right limbs are far.
- Ties are spread by 0.12 so no two cards are coplanar. Coplanar transparent cards drop one card in Cycles; this was seen and fixed.

Line weight:

| | body ink | head ink |
|---|---|---|
| ours | 0.032 D | 0.044 D |
| ref/c f_014, head D = 127 px | 0.025 to 0.03 D (coat) | 0.039 D at the top, 0.055 D at the lower right |

## 2. Stage (`stage25`, bpy 5.3, Cycles)

```python
import stage25 as st, testset
st.setup_render(scene, 360, 640, samples=16, denoise=True, threads=2)
L = testset.build(scene)                           # or your set
st.sync_lights(key="Moon", rims=["Beacon", "Sodium"], shadow="Sodium")   # call again whenever lights move
st.set_toon(exposure=0.92, rim_amt=0.6, wash_amt=0.2, glint_amt=1.6)       # optional
a = st.Actor25("kong1", "kong", gap=0.05, ppd=160, mode="25d", follow=0.5)  # mode="flat": v3-style single sticker
a.place((x, y, 0), facing_deg=0)                   # facing 0 = front toward -Y
fig = a.pose({"expr": "determined", "arm_l": "hold", "prop_l": {"type": "cutter", "bars": 3}}, camera=scene.camera)
bpy.ops.render.render(write_still=True)            # call pose() every frame after moving the camera or actor
a.screen_points(scene, cam, ("head", "hand_l"))   # pixel positions
```

- **Root and cards.** `Actor25` has a root Empty at the feet. Under it is a pivot that turns the stack `follow` (0.5) of the way toward the camera, so cards never go edge-on. Under the pivot sit 12 slot cards (`stage25.SLOTS`), each created as the full canvas (-2..2 x -1.25..3.25 D) and cut down every pose to the opaque box of its sprite plus 3 px (`_fit_card`, quad and UVs; the shadow proxy and the flat card too). Each card is moved to `z * gap` along its normal. `gap` = 0.05 D, about 2.6 cm at D = 0.52 m. The whole stack (pack to near arm) is 0.25 D, about 13 cm.
- **Toon shader.** One shared node group `DZ25_toon`, emission only (`emission_sampling = NONE`):
  - Lit side: the flat fill.
  - One stepped shade band where the silhouette pseudo-normal faces away from the key: fill × (0.50, 0.50, 0.78), which is blue-violet and turns white to hue 240.
  - Rim: for up to 3 point lights, an edge band facing the light, plus a small wash of the light's colour. Each layer has a rim weight: hair 0.45, face 0.3. Rim and wash are multiplied by the fill (`fill * 0.96 + 0.04`, nodes `alb_k`, `alb_floor`), so black ink, hair and trousers stay black; glints are not.
  - Wet: a Blinn half-vector step × a sparse noise mask gives glints.
  - The light positions and colours are copied from objects by `sync_lights`. A light can carry the custom props `rim_gain` and `rim_radius`.
- **Pseudo-normals.** Each layer's alpha is box-blurred three times (radius 0.15 D) into a height field, and its gradient becomes the tangent-space normal map. The inside of each shape stays flat. The head gets the v2 crescent away from the key, and limbs get a round band.
- **Shadows.** The layer cards have `visible_shadow` off. One hidden proxy card with the flat silhouette casts the real shadow. It is turned toward the `shadow` light, at most 70° from the visible cards. A soft dark contact decal sits under the feet. Reflections in wet ground come from the visible cards.
- **Sprites.** Sprites are re-rasterised only when the drawing changes (SHA-1 cache). File names are content hashes, so Blender never shows a stale image.

## 3. Registration in the v2 puppet (`cast25`)

`import cast25` changes nothing in v2 or v3 files:

- adds the names to `puppet.CAST` and wraps `puppet.figure`, so the names give flat composites with the same keys (`svg`, `feet_y`, `bbox`, `anchors`) plus `layers`;
- adds `puppet.STORY["dz_kong_cutter" | "dz_kong_phone" | "dz_kong_call" | "dz_kong_shout" | "dz_crew_shout" | "dz_driver_still" | "dz_driver_lift" | "dz_infected_lunge" | "dz_namnuea_photo"]`;
- adds `sprites.DEFAULT_CANVAS` entries for modules already imported. Call `cast25.register_stage(sprites)` after a later import.

Hero and boss still go to the original `figure`.

## 4. Phone (`phone25`)

- `screen_png(out, w, h, missed=4, state="missed"|"incoming"|"off")` draws the screen: a gradient, the clock, Namnuea's avatar (drawn by draw25d), the name, a notification card with the exact line and a red badge with the count.
- `verify_thai(text)` draws every character and compares it with `.notdef`. Result: 21 distinct characters, 0 notdef, 0 blank.
- `python3 phone25.py` writes `out/phone_screen.png` and `out/phone_insert.png`, the phone prop at insert size.

## 5. Commands

```
python3 sheet25.py                      # out/contact_sheet.png, out/layers_exploded.png
python3 orbit_test.py compare           # out/compare_flat_vs_25d.png (+ tmp/compare/measure.json)
THREADS=2 python3 orbit_test.py orbit 96 kong       # out/orbit_kong.mp4
THREADS=2 python3 orbit_test.py orbit 64 kong_wet   # out/orbit_kong_wet.mp4
python3 orbit_test.py still out.png 25 kong 25d 16 [big]
python3 measure25.py parallax|lines|hue <dirs>
python3 cast25.py                       # registration smoke test
python3 phone25.py
```

## 6. Measured

- **Parallax.** Kong, front drawing locked, camera orbit 0 to ±35° at 6 D distance, 720x1280, head about 166 px:
  - front arm against backpack: ±13.0 px (±3.8 px at ±10°);
  - hair against torso: ±5.1 px;
  - the flat card: 0 px for any two points.
  In the orbit the drawing swaps (front, 3/4, side) add the turn on top.
- **Render time:**

  | render | samples | threads | seconds per frame |
  |---|---|---|---|
  | 360x640, test stage with rain, 2.5D | 16 | 4 | 5.8 |
  | same, flat card | 16 | 4 | 3.1 |
  | 360x640, orbit | 12 | 2 | about 10 |
  | 720x1280 | 16 | 4 | 23 |

- **Colour** (hue_report on our frames). The hue mix holds: red 33 to 42, orange 28 to 31, violet 0.1, magenta 0.3 to 0.5, so there is no magenta drift. The night exterior is darker than the interior band (value 0.25 to 0.28, dark share 0.72 to 0.76) and bluer (blue 30 to 36). That is expected for EP.1 night rain; see QA in the report.
- **Scale.** Kong is 3.3 D from head top to soles; the ref/c puppet is about 3.2 D. At D = 0.52 m, Kong is 1.72 m, a car is 2.8 D tall and 8.4 D long, a lane is about 6.7 D, and the lamp pole is 19 D.

## 7. Known gaps

- The shading is analytic: emission plus a toon model fed with light positions. Set objects therefore do not shadow the puppets; a car's shadow does not darken Kong. Self-shadow between layers is also absent. The real lighting term was not added.
- Turning is limited to front, 3/4 and side drawings with discrete swaps, and they pop. There is no back view. Beyond ±35° the `follow` pivot keeps the cards readable, but the drawing stays a side view.
- Hands are mitten balls. The cutter grip is not a true wrap. The phone in the hand at body scale is too small to read, so use `out/phone_insert.png` for inserts.
- The wet hair of `crew_wet` and `kong_wet` reads a little like a cap.
- The driver is drawn with legs. In the car, use the `seat` anchor and let the door or window occlude the legs.
- The shadow proxy is one rigid card (v3 used a twisted proxy). The feet shadow can detach slightly under a low light; the contact decal hides most of it.
- The rain in `testset` is static streaks, with no motion blur and no fog volumes.

## 8. Independent review (fixes applied)

| Defect | Evidence | Fix |
|---|---|---|
| Rim and wash were added on top of every pixel, ink included: the red beacon drew a red stripe down black trousers and along the head outline, black hair spikes turned rust-brown under the sodium lamp, wet hair turned brown | orbit frames 0, 15, 25 and wet 10, 32 (old copies in `tmp/rv/old_orbit/`) | rim + wash now scale with the fill colour (albedo); glints stay additive |
| Every layer card was a full 4 x 4.5 D quad: each ray through the figure crossed up to 13 transparent quads | same frame 3 times, CPU seconds: 2.5D 22.4-23.5, flat 10.5-10.8 | `_fit_card` crops each quad and its UVs to the sprite's opaque box: 2.5D 11.2-11.5 CPU s, now about 5 % over the flat card (`tmp/rv/bench.py`) |
| Profile drawing at a 28° camera offset (yaw ±35° mapped to ±1); the ref/c puppets stay frontal or 3/4 under orbits | orbit stats: 22 of 96 frames side view | `YAW_RANGE_DEG` 60 |
| Battery indicator hidden under the glove, about 7 px wide at 720x1280 | contact sheet cutter tiles: 3/2/1 bars looked identical | indicator moved onto the cutter body, 1.7 x larger, ink border |
| Contact sheet: labels printed over the drawings (expression row unreadable), raised crowbar cut off at the tile top, cutter tiles cut the blades' label, ref/c crop carried the burned-in caption | `tmp/rv/old_orbit/contact_sheet.png` | label strip under each tile, taller hook-pose and crowbar canvases, ref crop stops above the caption |
| Dry orbit used the old line weights (stale) | builder note | both orbits and the comparison re-rendered with the fixed code |

Checked and left: Thai glyphs (21 characters, no notdef, read at full size), shadow attachment (rendered with a matte floor and only the sodium lamp, `tmp/rv/diag_shadow.py`: the shadow meets both soles at 0° and -30°; in the wet render the leg reflection makes it look detached), `cast25.py` registration, parallax numbers (unchanged).

Re-rendered after the review: `out/orbit_kong.mp4` (96 frames, 9.4 s/frame at 4 threads on a machine with load average 8 to 10 from other jobs; views front 33, 3/4 63, side 0), `out/orbit_kong_wet.mp4` (64 frames, 9.8 s/frame), `out/compare_flat_vs_25d.png`, `out/contact_sheet.png`, `out/layers_exploded.png`. hue_report: magenta 0.4 to 0.5 %, violet 0.1 %; still a darker, bluer night than the interior band (value 0.26 to 0.28). Old versions are in `tmp/rv/old_orbit/`, and the pre-review sources are in `tmp/rv/*_orig.py`.
