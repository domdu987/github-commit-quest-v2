# ep1/cast: the EP.1 cast, props, crowd and motion cycles

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/ep1/cast/`.
Everything is drawn by code as SVG layers on top of `v8/cast` (imported, not edited; read `PROJ/v8/cast/API.md` first: pose keys, layers, flat mode). No file in `v8`, `v10/film` or `v11` was written: the raster cache of this package is `ep1/cast/tmp/_cache` (`rast9` redirects `raster8.CACHE`).

## Files

| File | What |
|---|---|
| `draw9.py` | Patches the `draw8` module in the importing process (`install()`): new face (asymmetric brows, new eyes / mouths, Tos's glasses, face wounds), hair styles, outfit overlays (suit, coat, rider, guard), neck wound, torn sleeve, blood, watch, crowbar on the pack, new props, figure-frame arm targets. Old specs draw as before, with one exception: the pale rain beads on wet faces are off (`NO_FACE_BEADS`, the film's own decision). `watch_svg()` is the insert drawing. |
| `specs9.py` | The specs (below), `tos()`, `junior()`, `kong_ep1()`, `pale()`, `wet9()`, `infected(i)`, `infected_crowd(n)`, `check_unique9()`, static poses `poses(spec, name)`, `press_wound()`, `tos_hold()`, `HEIGHTS`. Re-exported by `draw9`. |
| `gait9.py` | Motion, pure Python: `Run`, `Sprint`, `SupportWalk`, `Seq` (stepped actions), `stagger_back`, `raise_crowbar`, `throw_flare`, `pull_out`, `bang_glass`, `roof_run`, `hold`. |
| `stage9.py` | bpy: `actor()`, `pose()` (adds card roll), `Take` (a cycle on a straight line), `measure()` / `drift()`, `Sil` (far silhouette card), `PropCard` (free prop with a light), `film()` (loads `v10/film/stage.py` as a module for its skin shader). |
| `rast9.py` | Rasteriser wrapper: `flat(spec, pose, ppd)`, `silhouette(rgba, col, rim)`. |
| `proofs.py` | `sbs`, `lookdev`, `crowd` -> `side_by_side.png`, `lookdev.png`, `crowd.png`, `out/crowd_unique.json`. |
| `measure9.py` | Proportions against the sheet bands -> `out/measure9.json`, `out/measure9_table.md`, `out/measure/*_measured.png`. |
| `cycles9.py` | `measure` (sole drift, no render) -> `out/drift.json`, `out/drift_table.md`; `render --part i/n`; `mp4` -> `cycles.mp4`, `out/cycles_sheet.png`. |

## Quick start

```python
import sys; sys.path.insert(0, PROJ + "/ep1/cast")
import stage9 as S9, draw9 as D9, gait9          # stage9 imports bpy; draw9 / gait9 / specs9 do not
FS = S9.film()                                   # optional: the film's skin shader and fast Actor8 methods
a = S9.actor("praew", "praew_wet")               # Actor8, flat mode, height from D9.HEIGHTS
a.place((x, y, 0), facing_deg)
S9.pose(a, dict(expr="focused", mouth=0.6, blink=0), cam)
tk = S9.Take(a, gait9.Run(a.spec, "praew"), start, direction)   # per frame: tk.frame(t, cam)
```

In a film `Stage`, the specs can be passed straight to the film's `Act(F, name, spec, height)`: import `draw9` before the first `Act` is posed.

## Specs (`D9.SPECS[...]`)

| Spec | What |
|---|---|
| `praew`, `praew_wet` | Dr. Praew. Bun (`hair.style="praew"`, `loose` 0..1), open white coat over light-blue scrubs, stethoscope, badge without text, blue gloves, white shoes. Wet: loose strand, dirt on the knees. Faces: `focused`, `alarmed`, `shouting`, `doubtful`, `calm`. |
| `tos`, `tos_wet`, `tos_torn`, `tos_soaked`, `tos_bleed` (or `D9.tos(state, side)`) | Khun Tos. Rectangular glasses, navy jacket with lapels over a white shirt, khaki trousers, brown belt, silver watch. `torn` = sleeve ripped lengthwise, `soaked` = cuff dark with blood, `bleed` = drops off the arm. Faces: `arrogant`, `panicked`, `shouting`, `evasive`. Hold pose: `D9.poses(spec, "tos_cross", view=, s=)`. |
| `james` | The sheet figure (bare head). `james_helmet` / `james_wet` = the EP.1 look: white open-face helmet, pose key `visor="up" / "down"`. No delivery box. Faces: `cheerful`, `terrified`, `shouting`, `urgent` (use with `arm_n="point"`). |
| `crew_bitten`, `crew_treated`, `crew_grey1..3`, `crew_dying` (or `D9.junior(state, pale_level, gauze, blood)`) | The junior after the bite: neck wound, blood down the chest, gauze pad with soak 0..1, skin steps toward the infected colour (`D9.pale(spec, 0..4)`). Faces: `pain`, `fading`, `out`; eyes closing = `blink` 0 / 1 / 2. Hand on the wound: `D9.press_wound(view, s)`. Shiver: `gait9.hold(spec, pose, shiver=1)`. |
| `crew_infected` | Same uniform and wound, grey-green skin, white eyes with red pin pupils, dried blood on the collar, gloved claw hands. Faces: `snap_open`, `searching`, `lunging`, `moan`, plus draw8's `bite`. |
| `kong_ep1_02 / 03 / 04 / 05 / 06 / 06b`, `kong_ep1_clean` (or `D9.kong_ep1(scene, blood, crowbar, watch)`) | `kong_wet` plus: watch on the left wrist, blood on gloves and right forearm (fading by scene), from 04 the crowbar through the pack's left loops with the hook over the left shoulder; `06b` = crowbar in the hands. Canvas enlarged for raised tools. |
| `guard` | Cap, pale-blue shirt with epaulettes and a plain shield, dark tie, torch prop (off). For the gate use `rast9.silhouette()` or `S9.Sil(..., poses=[...])`. |
| `D9.infected(i)`, `D9.infected_crowd(n <= 14)` | 14 infected designs (table in `crowd.png`). Each has `extra_pose` (idle arms) and `run_style` for `gait9.Sprint`. |

Sides are anatomical. `neck_wound.side`, `tear.side`, `watch.side`, `blood_forearm` are the character's own left / right; `D9.label_of()` maps them to draw8's limb labels, which are mirrored in the q / side drawings.

**The junior's bite is locked to the anatomical LEFT side of the neck.** The hook draws no wound, but in S21 and S23 the camera is on his left and the driver comes at that side, so that is the side a viewer was shown. Consequence: it is visible when he is drawn facing screen-left, in the front drawing it is on screen-right, and facing screen-right it is on the far side (only a stained collar edge shows).

## New pose keys

| Key | Meaning |
|---|---|
| arm dict `fig=(x, y)` | hand target in the figure frame (hands on a fixed point while the body moves) |
| arm dict `grab=dict(arm="n" / "f" / "R" / "L", t=0..1)` | hold the other arm's forearm |
| arm dict `fig_rel="neck" / "mouth"` | hand to the neck wound / over the mouth |
| `hand_shape` | adds `claw_glove`, `press`, `fist_side` |
| `z={"arm_f": 2.6}` | layer depth override (far arm in front of the torso) |
| `visor`, `coat_sway` | helmet visor; coat hem trailing in a run |
| props | `crowbar` (`angle`), `medbag`, `flare` (`lit`, `flick`), `torch`, `helmet9`, `gauze` (`soak`), `phone` with `glow=0..1` |

Static poses: `D9.poses(spec, name, s=, view=, ...)` with `sit_wheel` (`slump`, `limp`), `crouch_hide`, `seated_cab` (`role="driver" / "front" / "rear"`), `bang_glass`, `pulled`, `pull`, `phone_chest`, `tos_cross`.
Lip sync and blinks: `mouth` (level or `(shape, level)`) and `blink` work on every new spec, including the helmet and the glasses (rows in `lookdev.png`).
Watch insert: `D9.watch_svg(sec, blood=True, smear=False)` in a 2.7 x 2.0 box; `sec` = seconds since the bite (the drop is on the 12 mark).

## Motion (`gait9`)

Every cycle has `.root(t) -> (x, z)` in the actor's D and `.pose(t, s, view)`; a planted sole is a fixed point of the motion plane and the hip drops until the leg reaches it. `S9.Take.frame(t, cam)` places the root and sets `walk_lock`, so the card lies in the motion plane (as the hook's S19 walk does).

| Call | Use |
|---|---|
| `Run(spec, "kong" / "james" / "praew" / "tos")` | survivor runs, own period, stride, lean and arms each |
| `Sprint(spec, phase=, style="trail" / "reach" / "flail" / "one_up", seed=)` | infected: longer faster stride, trunk about 30 degrees forward, head leading, arms loose instead of pumping; period and stride vary per figure |
| `SupportWalk(kong_spec, junior_spec, sc_k, sc_j)` | `.pose(t, s) -> (pose_kong, pose_junior)`, `.root_b(t)` for the junior; stage his card about 0.4 BU nearer the camera |
| `stagger_back`, `raise_crowbar`, `throw_flare` (`.t_release`), `pull_out`, `bang_glass` | stepped takes (`Seq`) |
| `roof_run(spec, profile, x0, x1, stride, speed)` | footfalls planned on a height profile from ray casts; `.falls` lists them |
| `hold(spec, pose, dur, shiver, breath)` | a static pose as a take |

Tos pulled from the tipped car: pose `pulled`, then `actor.roll_deg = 80; actor.roll_about = 0` before `S9.pose()` (see `cycles9.mk_pull`, which also pins his wrists to Kong's hands).
`S9.Sil(name, spec, phases=8)`: one dark card with a thin rim, eight pre-rastered sprint phases, `frame(t, loc, cam)`.

## Measured

### Planted feet (`cycles9.py measure`, every frame at 24 fps, sole point read from the rastered leg sprite, world space)

| take | actor (spec) | frames | stances measured | max sole drift cm | root travel m | speed m/s | unreachable stances |
|---|---|---|---|---|---|---|---|
| run_kong | run_kong (kong_ep1_03) | 36 | 5 | 0.067 | 4.45 | 3.05 | 0 |
| run_james | run_james (james_wet) | 36 | 6 | 0.025 | 4.96 | 3.40 | 0 |
| run_praew | run_praew (praew_wet) | 36 | 6 | 0.055 | 4.18 | 2.87 | 0 |
| run_tos | run_tos (tos_wet) | 36 | 5 | 0.052 | 3.84 | 2.63 | 0 |
| sprint_infected | inf_junior (crew_infected) | 36 | 6 | 0.068 | 7.35 | 5.04 | 0 |
| sprint_infected | inf_2 (inf02) | 36 | 5 | 0.064 | 6.46 | 4.43 | 0 |
| sprint_infected | inf_6 (inf06) | 36 | 6 | 0.025 | 6.37 | 4.37 | 0 |
| sprint_infected | inf_9 (inf09) | 36 | 6 | 0.067 | 6.31 | 4.32 | 0 |
| support_walk | kong_s (kong_ep1_02) | 54 | 5 | 0.062 | 0.84 | 0.38 | 0 |
| support_walk | jun_s (crew_treated) | 54 | 5 | 0.048 | 0.84 | 0.38 | 0 |
| sit_wheel | sit_wheel (crew_grey2) | 30 | 2 | 0.000 | 0.00 | 0.00 | 0 |
| stagger_back | stagger_back (kong_ep1_02) | 42 | 6 | 0.079 | 0.60 | 0.35 | 0 |
| crouch_hide | crouch_hide (kong_ep1_04) | 24 | 2 | 0.000 | 0.00 | 0.00 | 0 |
| roof_run | james_r (james_wet) | 96 | 13 | 0.723 | 6.29 | 1.59 | 0 |
| roof_run | inf_r (inf06) | 96 | 12 | 0.536 | 7.69 | 1.94 | 0 |
| bang_glass | bang_glass (crew_infected) | 40 | 2 | 0.000 | 0.00 | 0.00 | 0 |
| pull_out | kong_p (kong_ep1_03) | 40 | 4 | 0.057 | 0.47 | 0.29 | 0 |
| throw_flare | throw_flare (kong_ep1_04) | 36 | 3 | 0.068 | 0.23 | 0.15 | 0 |
| raise_crowbar | raise_crowbar (kong_ep1_06b) | 40 | 3 | 0.057 | 0.22 | 0.14 | 0 |

Pass mark 1 cm. The roof run is the only take above 0.1 cm. Re-measured by the checker after the run / sprint rewrite (see "Checker's pass").

### Proportions (`measure9.py`, ours / sheet, band +/- 6 %)

| measure | praew (vs Praew sheet) | tos (vs Tos sheet) | james (vs James sheet) | james_helmet (vs James sheet) | crew_infected (vs James sheet) | guard (no sheet figure) |
|---|---|---|---|---|---|---|
| bare head D / total | 0.228 / 0.223 ok | 0.237 / 0.237 ok | 0.227 / 0.223 ok | 0.229 / 0.223 ok | 0.230 / 0.223 ok | 0.233 |
| hair top to chin / total | 0.264 / 0.258 ok | 0.277 / 0.278 ok | 0.284 / 0.279 ok | 0.278 / 0.279 ok | 0.274 / 0.279 ok | 0.268 |
| figure height in bare heads | 4.379 / 4.480 ok | 4.220 / 4.215 ok | 4.396 / 4.491 ok | 4.364 / 4.491 ok | 4.339 / 4.491 ok | 4.289 |
| hair above skull / D | 0.157 / 0.160 ok | 0.168 / 0.172 ok | 0.247 / 0.253 ok | 0.214 / 0.253 **OUT** | 0.189 / 0.253 **OUT** | 0.153 |
| hair vertical extent / D | 1.215 | 0.790 / 0.785 ok | 0.931 / 0.900 ok | 1.179 / 0.900 **OUT** | 0.978 / 0.900 **OUT** | 0.722 |
| hair width / D | 1.419 | 1.171 / 1.174 ok | 1.287 / 1.260 ok | 1.268 / 1.260 ok | 1.291 / 1.260 ok | 1.408 |
| shoulder width / D | 0.906 / 0.920 ok | 0.842 / 0.818 ok | 0.939 / 0.936 ok | 0.939 / 0.936 ok | 0.938 / 0.936 ok | 0.995 |
| torso chin-crotch / total | 0.318 / 0.320 ok | 0.303 / 0.310 ok | 0.314 / 0.316 ok | 0.316 / 0.316 ok | 0.319 / 0.316 ok | 0.320 |
| torso / D | 1.391 / 1.430 ok | 1.280 / 1.307 ok | 1.380 / 1.420 ok | 1.380 / 1.420 ok | 1.383 / 1.420 ok | 1.372 |
| legs crotch-sole / total | 0.418 / 0.421 ok | 0.419 / 0.410 ok | 0.401 / 0.403 ok | 0.404 / 0.403 ok | 0.407 / 0.403 ok | 0.411 |
| legs / D | 1.828 / 1.880 ok | 1.769 / 1.727 ok | 1.765 / 1.809 ok | 1.765 / 1.809 ok | 1.764 / 1.809 ok | 1.761 |
| trouser leg width / D | 0.313 / 0.320 ok | 0.305 / 0.306 ok | 0.329 / 0.333 ok | 0.329 / 0.333 ok | 0.333 / 0.333 ok | 0.361 |
| boot/shoe height / D | 0.325 / 0.330 ok | 0.313 / 0.322 ok | 0.489 / 0.495 ok | 0.489 / 0.495 ok | 0.168 / 0.495 **OUT** | 0.361 |
| head outline median / D | 0.040 | 0.040 / 0.039 ok | 0.042 / 0.044 ok | 0.044 / 0.044 ok | 0.044 / 0.044 ok | 0.038 |

- Praew is not in `spec/sheet_proportions.md`; her sheet values were read for this pass from gridded 4x crops (D 111 px, total 497 px, chin y 307, crotch y 466, sole y 675) and are less exact than the three measured there.
- `james_helmet` and `crew_infected` fall out of the hair rows by construction (a helmet; wet drooped hair as in the hook's `crew_wet`). The `crew_infected` shoe row is a failed colour match on the wet boot, not a changed boot.

### Crowd

14 designs, 91 pairs, no pair shares face, hair, clothes or wound signature (`out/crowd_unique.json`).

### Render cost

- `cycles.mp4` (checker's re-render): 14 takes at 360x640, draft tier (2 spp + denoise); runs and the sprint on twos, slow actions and holds on fours; 26.8 s. 10.4 CPU s per frame in the Blender process (Chromium rastering is a child process and is not in that number); wall 37 s per frame with the hook final on all 4 cores.
- Final tier, 720x1280, 5 spp at 100 %: `out/final_trio_720.png` (Praew, Tos, James) 68.2 CPU s, `out/final_duo_720.png` (infected junior, Kong) 67.7 CPU s; peak memory 1.48 GB per process. This matches the plan's class A figure (68.2 CPU s).

## Checker's pass (what changed after the builder's report)

- **Runs and sprint rewritten** (`gait9.Stride`, new `RUNS`). The first presets gave a stance sweep under 1 D at 4 steps a second: the legs never opened and it read as a shuffle. Now: stance sweep 1.3-1.5 D, a flight phase, heel kick, knee drive, bigger arm pump. Speeds went up: Kong 3.05, James 3.40, Praew 2.87, Tos 2.63, infected 4.3-5.0 m/s. Any shot timing that assumed the old speeds (2.1-2.5 and 3.3-3.8 m/s) must be redone.
- **Travelling figures must be staged near side-on.** `cycles9.track_cam` now stands about 15 degrees off the card's normal. The first proof stood 48 degrees ahead of the runner, so every card was seen at two-thirds width (oval heads). The card still lies in the motion plane; a run seen from the front quarter will look narrow again.
- Support walk: the junior trails Kong by 1.0 D (was 0.6; the two heads and trunks merged), camera centred on the pair.
- Sprint take: four infected with different gaits are in frame; the far silhouettes are hidden in this take (they read as black smears at that distance).
- `press_wound`: the fist now sits on the collar by the wound in both drawings (it covered the mouth in the 3/4 drawing).
- `arrogant` (Tos): bold dot eyes, as on the sheet (half lids read as two T marks behind the glasses). `cheerful` (James): no brow bars over the laughing arcs.
- Proof sheets: a cell is as wide as its label (labels overlapped).
- `cycles9.py render` resumes only over PNGs that decode; `mp4` holds each drawing for its real gap.
- The builder's files are kept in `tmp/builder/`.

## Gaps

- **Runs are seen on a card that lies in the motion plane** (the same trade as the hook's S19 walk; planted feet depend on it), so a travelling figure is not camera-facing: stage it within about 20 degrees of side-on. Runs were judged on frame strips, not in playback.
- **`cycles.mp4` was checked on its contact sheet and frame strips; nobody has watched it in playback.** `stage9.Sil` silhouettes are proven only as stills in `crowd.png`, not in motion.
- Roof run: sole drift 0.72 cm (James) and 0.54 cm (infected), ten times the other takes; cause not found (the sole point is read from the lowest sprite rows, and something else in the leg layer probably reaches lower in some frames). It is one bound per footfall, no hands on the roof edge, at 1.6-1.9 m/s average; for the proof the car `l1_a` was slid 5.7 BU toward `l1_e` inside the render process, because no two cars in the set are close enough to jump.
- Tos: the sheet's fully crossed arms are not reproduced; `tos_cross` is one arm folded across the belly and the other hand closed on its cuff, which can read as a man looking at his watch. Tear side: `continuity.md` says the left forearm, the cast brief said the right sleeve. The default follows continuity (left); `D9.tos(state, side="R")` gives the other. With the tear on the left the silver watch is dropped.
- Tos against the driver: glasses, navy jacket, khaki trousers, paper-white skin and a high combed-back hairline against no glasses, white torn shirt, red tie, grey slacks, grey-green skin and a fringe. The hair colour is the same dark brown (the sheet's), and the build is the same; from behind at distance the jacket is the only difference.
- Praew: coat narrower than the sheet's, sleeves are full length (the sheet rolls them), her brows are bolder than the sheet's thin ones (the standing decision asks for bold brows). The wet coat is light grey.
- James: the sheet shows him bare-headed; EP.1 needs the helmet on, and the worn helmet is an open-face design of this package (the sheet's is full-face and would hide the face).
- The bite side contradicts nothing drawn in the hook, but draw8's Thai flag patch is on the opposite anatomical arm in q / side drawings than in the front drawing (an old mirror quirk), so flag and wound are on the same side in some drawings and opposite in the front one.
- Support walk: the junior's card is in front of Kong's; Kong's supporting arm is hidden. Pull-out: Kong is half out of frame and Tos is partly behind the car in the proof camera.
- Sit against the wheel, crouch-hide, cab seats, bang on glass: staged on open deck, not against a wheel, cover, cab or window. Seated cab poses exist only as drawings (`lookdev.png`, last row); nothing was rendered behind glass.
- Flare: the lit prop is a drawing with a painted halo; `S9.PropCard(..., light=((1, 0.2, 0.15), watts))` gives a real light but the thrown flare's flight was not staged or rendered. Phone on the chest: painted halo only.
- Guard: a full puppet and a silhouette treatment; bars in `lookdev.png` are painted on the proof, not the set's gate.
- Crowd: 14 designs; uniqueness is checked on spec signatures (face, hair, clothes, wounds), and the sheet was looked at once. Roles 02 and 11 (hoodies) are the closest pair by eye. No wet variants of the crowd. Crowd memory and cost in one frame were not tested.
- Proportions were measured on flat rasters, not on Cycles renders; the heights in `HEIGHTS` come from the sheet's pixel ratios (Praew 2.60, James 2.61, Tos 2.67 BU against Kong 2.86) and were not checked against the set's cars and doors.
- Not built: stairs gait, kneeling, the junior's gauze lying on the ground as a prop card, Tos's briefcase, James's phone with a map, blink / lip-sync timeline helpers (use the film's `common.blink` and `common.mouth`).
