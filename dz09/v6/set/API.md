# v6/set: beauty pass of the EP.1 expressway (ref D finish, night rain)

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`.
The v4 set (`PROJ/v4/set_expressway`) is imported read-only. v6 calls its `build()`, then overrides the world, lights, materials and render settings, and adds detail, presets, foreground props and its own post (`post6`). Spec: `PROJ/spec/refD_beauty.md` (light, materials, grade) and `PROJ/spec/refD_camera.md` (templates T1, T3, T5, T7).

## Files

| File | What it does |
|---|---|
| `beauty.py` | `build()`, `setup_render()`, `world6` (dark blue horror sky that lights the scene), `lights6` (moon key, softer and less orange sodium, cool flood, ambient cut to 0.3), `materials6` (new wet asphalt, grime on concrete, steel and plastics, dirty white hero sedan), `detail6` (HV pylons and wires, telecom poles and cables, second skyline layer, dead billboard, ground grit). Imports `presets` and `render6`. |
| `presets.py` | The 4 ref-D camera presets (`low`, `eye`, `high`, `macro`) and `foreground()`, which adds framing props in camera space. Also works on the v4 scene. |
| `post6.py` | Post: depth haze, light-lit rain mist, shafts, layered lens DOF (near and far field, disc bokeh, clamp 36 px), two-tier bloom, rain (v4), split-tone filmic grade, vignette, magenta and lavender clamp. |
| `render6.py` | `render(out_noext, frame, post_opts)`: the v4 pass render (EXRs), then post6. Keeps `<out>_info.json` and `_shafts.pkl` so post can be re-run. |
| `ab.py` | Before and after stills of the 4 presets, `repost`, `sheet` (writes `before_after.png` and `out/measure.json`). |
| `before_after.png` | Rows: ref D frames (f2_081, 076, 090, 002, for look only), v4 before, v6 after. All 9:16, 720x1280 frames shown at half size. |
| `out/before/`, `out/after/` | Full frames `<preset>.png`, `_raw.png`, `_depth.png` and EXR passes. `times_*.json`, `measure.json`. |
| `tex/poster_v6.png` | Code-drawn, wordless torn poster for the billboard. |

## How a shot script uses it

```python
import sys; sys.path.insert(0, PROJ + "/v6/set")
import bpy, beauty as B, presets            # beauty puts v4/set_expressway on sys.path (expressway, kit, vehicles, post, shafts)
A = B.build()                               # ~5-6 s; clears the file, v4 build (haze cards off) + v6 overrides; returns v4 anchors (+ A["moon_dir"])
B.setup_render("final", threads=4)          # preview 4 spp | draft 6 @100% | final 6 spp @75% | final8 8 @75% (holds) | final12 | native 16 @100%
cam = presets.use("eye", A, aspect="9:16", scale=1.0)   # camera, resolution, focus/DOF data, preset foreground props
# optional per-shot framing (any number; cleared by the next presets.use):
presets.foreground(cam, "pillar", side="left", cover=0.2, depth=1.2)
# ... place characters (below) ...
r = B.render6.render("/abs/out/S06_f0001", frame=1, post_opts={"exposure": 1.5})
# r["png"] graded frame, r["raw"] composite without post, r["z"] / r["depth_png"] depth, r["rgb"|"env"|"idx"] passes,
# r["cpu_render"], r["cpu_post"]
```

- A v4 preset still works: `B.X.use_camera("ots", "9:16")`. Set `cam["coc_k"]` and `cam["coc_max"]` yourself (otherwise the defaults are 3 and 36), because post6 reads those keys and not v4's `dof_k`.
- Your own camera: call `B.X.make_camera()`, set `loc`, `rot` and `lens`, then set `cam["focus"] = (x, y, z)` (a world point), `cam["coc_k"]` and `cam["coc_max"]`. Retarget the camera-facing cards with the loop in `presets.use`.
- Animation: every light, beacon and hazard is keyframed (v4). The puddle ripples follow `#frame` through a driver. Rain is re-seeded each frame. Call `render6.render(..., frame=f)` once per frame. Build once per process; scene sync is paid every frame.
- Re-grade without re-rendering: `python3 ab.py repost --only macro exposure=1.4 coc_k=60`, or call `post6.process()` on `render6.load_passes()` (about 3 CPU s).

### Placing characters

- Marks are the v4 anchors: `A["kong_mark"]`, `A["crew_mark"]`, `A["kong_phone_mark"]`, `A["driver_seat"]`, `A["driver_head"]`, `A["door_mid"]`, `A["cutter_jaw"]`, `A["cutter_leds"]`, and `A["kong_to_door_deg"]` (the Z rotation that turns a -Y front toward the door). World scale is 1 D = 0.6 m and the deck top is at z = 0. Contact-shadow decals sit at the Kong and crew marks.
- Characters are ordinary lit objects. Set **pass_index 2** on every mesh. post6 blurs index 2 by depth like everything else, so in `macro` a character behind the cutter becomes bokeh. To force actors sharp, pass `post_opts={"sharp_idx": [2]}`.
- Emission-only cards will not take the moon or bounce light. Lit 3D characters will: the moon key comes from `A["moon_dir"]` (the sky's moon), it is in front of the camera on every preset, and it gives cool rims. The sky dome fills from above.
- Stand-ins: `import standins; acts = standins.place(A); standins.pose_all(acts, cam, hide=("kong",) if preset == "macro" else ())`. `ab.py` uses these.
- Index map: 0 sky, 1 road, 2 actors, 3 car bodies, 4 set, **5 foreground framing props**.

### Presets (9:16; 16:9 overrides in `presets.table`)

| Name | Template | Camera | Lens | DOF (`coc_k` / max, px at 1280) | Preset foreground |
|---|---|---|---|---|---|
| `low` | T5/T4 | (-2.55, 30.4, 0.55), looking up at Kong's head; `bike_a` hidden for this preset | 28 | 6 / 24 | `wheel`, left, 42 % |
| `eye` | T3 | (-2.3, 25.2, 2.7) toward (-7.7, 37.5, 2.15), eye height, horizon through Kong | 35 | 4 / 18 | `pillar`, right, 16 % |
| `high` | T7 strong | (3.8, 7.0, 13.0) toward (-8.6, 42, 0), about 27° down; rows stack | 45 | 1.6 / 10 | `pole`, left, 8 % |
| `macro` | T1 | 2.6 D from the cutter's 3-bar LED gauge, from the front quarter; red and blue beacons and the flood behind | 50 | 70 / 36 | `lip`, bottom, 17 % (dark wet bonnet) |

Presets can hide clutter. `hide=[root names]` hides those roots and their children, and the next `use()` restores them.

### Foreground props: `presets.foreground(cam, kind, side="left"|"right", cover, depth, seed)`

These are real geometry placed in camera space at `depth` D from the lens: they are lit, take shadows and reflections, and post6 blurs them as near field, so they spill softly over sharp subjects. `cover` is the fraction of the frame width they take (of the height for `lip`).

| Kind | What it is |
|---|---|
| `pillar` | dark car pillar with a door seal |
| `wheel` | wrecked tyre and rim, three-quarter view |
| `lip` | wet bonnet edge with a chrome trim across the bottom |
| `pole` | galvanised lamp pole with a reflective band |
| `post` | guard-rail post and W-beam |
| `cone` | traffic cone in a corner |
| `fender` | crumpled silver panel. Weak: it reads as a blob, so prefer `wheel`. |

For the template sizes, see refD_camera.md: T5 40 %, T7 25-30 %, T8 40-45 %.

## What changed against v4

- **Light transport**
  - 2 diffuse bounces and 1 glossy bounce (contact AO and bounce), indirect clamp 3.
  - The light tree is off: -11 % CPU measured here.
  - The sky lights diffuse rays: MANUAL sampling, 256 map.
  - The ambient emission term is cut from 1.0 to 0.3.
- **Moon key**: sun lamp, 3° angle, colour (0.62, 0.74, 1.0), strength 2.2. It is aligned with the sky's moon disc, so shadows and rims come toward the lens. `visible_glossy` is off, so there is no streak on the wet road.
- **Other lights**
  - Sodium spots: 26 kW down to 10 kW, colour (1, 0.62, 0.30), shadow softness 0.4.
  - Flood: softness 0.35 and cool LED colour.
  - Bulbs are less orange.
- **Sky**
  - Navy zenith #090924, a deep blue cloud deck with lit edges #46447e (shade hue 241-243 measured), very dark gaps, and a blue horizon glow with a trace of city sodium.
  - Moon halo exponent 300 plus a core glow.
  - No lavender or magenta.
- **Wet asphalt `asphalt_v6`**
  - Roughness: dry patches 0.55, damp 0.28, standing water 0.03 (about 40 %).
  - Rain-ripple rings in the water, driven by the frame number.
  - Tar-sealed crack network, 2-4 cm aggregate and grit, ruts and oil strips, chipped lane paint.
- **Grime** (world-space blotches, vertical run-off streaks, darkening at the foot) on:
  - concrete barriers, slab and piers;
  - steel masts, gantry and W-beam;
  - plastics, cones and cases;
  - row-car paints.
- **Hero sedan**: white, with mud splash on the lower body, scratches and v4 rain beads under a 0.5 coat. It keeps the v4 dents, crumple and see-through cracked glass.
- **Detail**
  - Two high-voltage crossings: 4 lattice pylons, 14 sagging wires.
  - Telecom and CCTV poles with 3 drooping cables per span along the left barrier.
  - 70 nearer skyline towers with roof boxes, antennas, aviation lamps and a few LED crowns.
  - A dead billboard on scaffolding with one lamp still on.
  - 1,400 grit chips around the action.
- **Post6**
  - Haze: geometry fades to deep blue (0.0035, 0.0055, 0.015) with z0 = 420 D, so blacks stay black, plus lamp-glow pollution. Mist only where there is light.
  - DOF: layered, with these properties:
    - Each pixel gathers only from layers blurred no more than itself, so in-focus edges are clean and nothing halos.
    - The radius field is eroded and then blurred, so depth-edge stipple is suppressed.
    - The near field is blurred with its alpha and laid over the result.
    - Big radii use a disc kernel, so lights become round bokeh.
    - Blur goes up to 36 px at 1280.
  - Bloom: tight on practicals, wide (60 px) and cool around the moon and sky.
  - Grade:
    - exposure 1.5, gains (1.0, 0.975, 1.05), saturation 1.05;
    - shadows pushed blue (R and G pulled under L 0.07);
    - bright mids pulled toward neutral white;
    - toe `c²/(c + 0.0035)` and a soft shoulder from 0.62.
  - Vignette 0.22. No grain.
  - Hue clamp 256-342° turned toward 250° or 355°.

## Measured (`out/measure.json`, `out/times_*.json`; 720x1280, 4 threads, load average 1-5)

### Time per frame (CPU s)

| Preset | v4 before (8 spp) | v6 after (6 spp, final) |
|---|---|---|
| low | 16.7 + 2.1 = 18.8 | 17.0 + 3.2 = **20.2** |
| eye | 22.1 + 2.1 = 24.2 | 25.5 + 3.2 = **28.7** |
| high | 24.9 + 2.2 = 27.1 | 31.2 + 2.3 = **33.5** |
| macro | 28.7 + 2.1 (v4 macro_cutter framing) | 22.3 + 3.4 = **25.7** |

Build takes about 5-6 s once per process. Two settings were measured as too expensive for the 40 s budget:
- 8 spp with the light tree: high 48-49 CPU s (`final8` is kept for holds).
- 2 glossy bounces: eye 40 CPU s.

### Look (9:16)

| Metric | ref night | v4 eye | **v6 low / eye / high / macro** | target |
|---|---|---|---|---|
| L p1 | 0.002 | 0.101 | 0.033 / **0.010** / 0.028 / 0.058 | ≤ 0.02 |
| L p50 | 0.30 | 0.31 | 0.15 / 0.19 / 0.17 / 0.35 | 0.28-0.36 |
| L p95 | 0.74 | 0.59 | 0.59 / 0.62 / 0.53 / 0.78 | 0.65-0.75 |
| S mean | 0.41 | 0.30 | 0.50 / 0.41 / 0.38 / 0.23 | 0.36-0.42 |
| blue / warm | 0.92 / 0.04 | 0.49 / 0.42 | 0.89/0.09, 0.74/0.20, 0.50/0.43, 0.39/0.51 | ≥ 0.70 / ≤ 0.22 |
| shadow B/R | 2.5 | 0.97 | 2.7 / 2.8 / 2.7 / 1.5 | ≥ 1.8 |
| edge density | 0.096 | 0.024 | 0.026 / 0.025 / 0.043 / 0.011 | ≥ 0.07 |
| local contrast | 0.104 | 0.064 | 0.065 / 0.073 / 0.083 / 0.073 | ≥ 0.09 |

Shade hue (blue and violet pixels, median): 241 / 243 / 243 / 242. Measured with hue_report `stats()`: magenta 0.2 / 0.4 / 1.8 / 0.7 % and violet 0.5 / 1.3 / 4.3 / 2.1 %.

## Gaps

- **Exposure and detail.** Medians sit at 0.15-0.19, darker than the ref's snow-lit 0.30. That is deliberate for rain horror; raise it with `exposure` (1.5 → 1.9) if wanted. Edge density stays at 0.025-0.045 against 0.096: the ref's top third is conifer forest, and ours is cloud plus wires. Ideas not done: rain-drenched tree-line silhouettes on the city side, more cable runs, signage.
- **Warm share** is still 0.43-0.51 on `high` and `macro`, from tail lights, hazards, the flood on the orange cutter and the sodium pools. For a cooler `high`, drop the row tail-lamp strength.
- **Moon shadows.** No long moon-shadow stripes toward the lens yet: from these angles the cars and barriers shade the action. A per-shot moon tweak needs a world plus sun rotate helper (not written).
- **Characters** are still v4 emission stand-ins, flat and unlit. In `macro` Kong is hidden and the 3D cutter floats with no hand; shots must add the hand or arm.
- **DOF.** Gather-based. A faint ragged edge can remain on alpha-card silhouettes at large blur (the driver card in `macro`). There is no bokeh cat-eye or occlusion inside the near field.
- **Foreground.** `fender` reads poorly. `pillar` and `pole` are plain dark shapes, which works as frame-in-a-frame.
- **Not checked by eye:**
  - 16:9 versions of the 4 presets;
  - frames other than 7 (beacon and ripple timing come from the v4 keys and the driver);
  - the billboard poster up close.
