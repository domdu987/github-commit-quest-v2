# v11/set: the v9 expressway with the reference-E finish

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Spec: `PROJ/spec/refE_look.md`.
v9/set is copied, not edited (`beauty.py`, `beauty6.py`, `presets.py`, `post9.py`, `render9.py`, `grade_fit.py` are copies; v4 is still imported read-only). Same API shape as v9: everything in `v9/set/API.md` still holds unless listed here.

## Files added

| File | What it does |
|---|---|
| `finish11.py` | The finish layer, called at the end of `beauty.build()`: light design, practicals, cones, glare guard, POV dressing. Tunables in `finish11.P`. |
| `post11.py` | post9 plus ink outlines, wet streaks, coloured halo, lit rain, tilt-shift, blue shadow floor, stronger vignette. Same `process()` signature. |
| `render11.py` | render9 pointed at post11 (`render()`, `repost()`). |
| `look11.py` | Copy of look9: the six look stills with the v8 paper puppets; `render`, `repost key=value`, `sheet`. |
| `vs_refE.png` | v9, v11 and the closest reference-E frame for each of the six shots. |
| `analysis/` | Reference-E measurement scripts and JSON. `look/measure11.json`: v9 and v11 frame metrics. |
| `tex/exit_sign_v11.png`, `tex/poster_v11_{0,1,2}.png` | Code-drawn sign and wordless billboard art. |

## Usage

```python
import sys; sys.path.insert(0, PROJ + "/v11/set")
import beauty as B
A = B.build()                         # v9 build + finish11.apply(A)
B.setup_render("final", threads=4)    # "final" is now 5 spp at 75 %
cam = ...                             # as in v9
B.place_work_lamp_safe(A, cam, heads=[kong.head_world()], base=(x, y), aim=(x, y, z), energy=8000.0)
r = B.render6.render(out_noext, frame=f, post_opts={"exposure": 1.6})   # B.render6 is render11
B.render11.repost(out_noext, vignette=0.55)
```

## API changes against v9

- `B.render6` is `render11` (post11). `B.render9` / `post9` remain importable for the old look.
- `B.SPP["final"]` is 5 (v9: 6). The alpha-card cast and the extra lights cost about 8 CPU s; 5 spp brings the frame back under 40.
- `B.place_work_lamp(...)` unchanged, and it now also moves the lamp's rain cone.
- New: `B.place_work_lamp_safe(A, cam, heads, base, aim, energy=None, head_z=None, cable=None, min_frac=0.16)` returns `(head position, metres slid or None)`. It slides the lamp along camera-right / left until its lens is at least `min_frac` of the frame width from every head on screen.
- New: `B.glare_check(cam, heads, min_frac=0.16)` returns `[(emitter, head index, distance / W)]` for the work lamp, the truck flood and visible headlights. Empty list = no glare behind a head. Call it after any camera or actor move.
- New: `B.pov_windscreen(A, on=True)`: bonnet dressing (leaves, glass crumbs, water streaks, a buckled crease, placed by ray cast on the bonnet) and two cabin practicals (`pov_dome` warm 160 W, `pov_dash` teal 45 W). `on=False` removes it.
- New: `B.add_cone(name, loc, aim, length, r0, r1, col)`: a post light cone (rain shaft) for any light. `B.practical(light_name, gain)`: per-shot gain on a set light.
- New anchor `A["exit_sign"]`; flag `A["v11"]`.
- Asphalt: `beauty.WET` (puddle threshold 0.50, damp from 0.34, roughness 0.50 - 0.34 x damp): more standing water and a glossier damp deck than v9.

## What the finish changes

- **Surround.** Moon key 7.0 -> 3.6, moon glint 1.3 -> 1.0, sky fill 0.65 -> 0.42, sky seen by the camera x 0.60, flood 36 -> 20 kW. Pools now stand out of a dark blue surround.
- **Practicals with pools.**
  - Beacons: the dome lights x 2.2 (red) and x 4.0 (blue), plus `beacon_throw_red` / `beacon_throw_blue` spots at the light bar aimed over the rescue zone. A driver ties each throw to its dome, so they flash together.
  - Hazards x 5 (amber, peak 1.3 kW). Tail lamps x 1.6.
  - Sodium 7.5 kW, deeper orange, crisper edge.
  - Gantry signs: emission 2.6 and a 16 kW green pool under each.
  - A lit green exit sign on two posts at the left barrier (s 53), with its own 900 W green pool: the mid-ground green practical.
  - Three of the four uni-pole billboards are lit, wordless posters (emission 2.4-3.0); the scaffold billboard is lit at 0.9 with a 5.2 kW spot.
  - Skyline windows x 2.6.
  - Work-lamp lens emission 40 -> 12, so the lens is a readable shape rather than a white blob.
- **Cones in the rain.** New post cones for the work lamp, both beacon throws, the headlights and the gantry signs. `shaft_gain` default 0.3 -> 0.8. Rain streaks brighten inside lit volumes (`rain_lit` 1.6).

## post11 info keys (all optional; defaults shown)

| key | default | effect |
|---|---|---|
| `ink`, `ink_zmax` | 0.55, 110 | outlines on set objects from depth and object-index edges, fading out by `ink_zmax` D; actors and foreground props are skipped; off for macros |
| `streak`, `streak_len` | 0.55, 240 | vertical wet-road reflections under every bright source (road pixels only) |
| `halo`, `halo_px` | 0.30, 95 | wide glow in the source's colour |
| `rain_lit` | 1.6 | rain brightens in light |
| `tilt` | 1.0 | tilt-shift: bottom 22 % and top 14 % blur (off for macros) |
| `lift` | 0.45 | saturated blue floor in the shadows |
| `vignette` | 0.50 | corners fall to navy (v9 0.20) |
| `saturation`, `toe` | 1.55, 0.008 | cool hues only; warm hues (uniform orange, skin, sodium) stay at `post11.WARM_SAT` 1.12 so costume colours do not shift |
| `shaft_gain`, `bloom`, `bloom_wide` | 0.8, 0.55, 0.10 | |
| `violet_keep` | 0.42 | the v9 violet clamp only applies below this value, so beacon and sign light may mix to magenta while shadows stay blue |

`post11.EXPOSURE11` 0.74 multiplies every shot exposure (on top of post9's 0.75).

## look11.py shot changes against look9

- Cast: `v8/cast` `Actor8` puppets (imported read-only, in whatever state that folder is in). The seated driver gets `pitch_override = 0`: the flat mode otherwise leans the card back for a high camera and tips him out of the seat.
- Work lamp: S06 and S13 keep it out of frame as a back / side light; S24 beside the action; all through `place_work_lamp_safe`.
- S09 uses `presets.use("macro", A)` on the 3D cutter gauge (the puppets' cutter is a drawing).
- S18 re-framed: 48 mm from 2.0 D in front of the windscreen, 0.30 D above the head; driver's face about 0.28 W; bonnet about 15 % of the frame; `pov_windscreen`, a 170 W front fill, sodium x 0.5, vignette 0.55.

## Cost (720x1280, 4 threads, CPU s render + post)

| S06 | S09 (4 spp) | S13 | S18 | S20 | S24 (4 spp) |
|---|---|---|---|---|---|
| 32.7 + 4.4 = 37.0 | 25.3 + 6.2 = 31.5 | 35.0 + 5.0 = 40.0 | 25.3 + 4.4 = 29.7 | 26.7 + 5.6 = 32.3 | 33.3 + 4.1 = 37.4 |

These were measured on the last full render. The warm-hue grade pass was added afterwards and only timed inside `repost`; expect about 0.3 s more post, which puts S13 just over 40.

## Measured look (`look/measure11.json`, same script as the reference numbers)

| | luma p5 | p50 | p95 | saturation | shadow hue | corner / centre |
|---|---|---|---|---|---|---|
| ref E night | 0.04-0.09 | 0.16-0.20 | 0.43-0.93 | 0.58-0.64 | 230-271 | 0.25-0.69 |
| S06 | 0.073 | 0.224 | 0.669 | 0.467 | 246 | 0.60 |
| S09 | 0.068 | 0.285 | 0.609 | 0.421 | 246 | 0.76 |
| S13 | 0.061 | 0.252 | 0.583 | 0.390 | 249 | 0.86 |
| S18 | 0.080 | 0.234 | 0.763 | 0.325 | 230 | 1.23 |
| S20 | 0.105 | 0.251 | 0.817 | 0.402 | 248 | 0.72 |
| S24 | 0.085 | 0.273 | 0.884 | 0.366 | 260 | 0.40 |

## Known gaps

- Saturation is 0.33-0.47 against 0.58-0.64. The set still has neutral greys (asphalt, concrete, white car); reference E has none.
- Ink line density is 0.3-0.7 % against 1.6-2.8 %. The post outlines only follow depth and object edges; drawn interior detail lines would need line art in the materials.
- Materials are still the v9 photographic ones (grime, aggregate), not flat drawn colour fields.
- S18: the driver now reads, but the bonnet strip is still a plain pale band (the dressing sits in the blurred bottom of the frame and does not show), and surfaces behind the glass are grainy at 5 spp.
- S20: the white door still fills half the frame.
- The red / blue beacon throws and the green pools were not checked in a frame that shows them clearly; none of the six look cameras points at the truck. Stills are frame 7 of the beacon cycle.
- Only 9:16 was rendered in v11. `look11.py` keeps look9's 16:9 branches but they are untested here.
- Shadow hue reaches 260 in S24 (target: no drift past 255).

## v12 clarity levels (`post11.LEVELS`): less rain, no veil

User feedback on draft v1: the rain made the scene look blurry. `post11.LEVELS` holds master levels; each MULTIPLIES the matching per-shot option, so shot scripts are unchanged. The defaults below are the new look; `post11.LEVELS_V1` (all 1.0) is close to the draft-v1 look.

Tune three ways: a post option of the same name per shot / frame (`return {"exposure": 1.6, "RAIN": 0.7}`), a whole run (`run.py --levels RAIN=0.6,DOF=0.5`, or `--levels v1`), or `post11.set_levels(RAIN=0.6)`. They also work in `render11.repost(out, RAIN=0.6)`.

| level | default | draft v1 | what it scales |
|---|---|---|---|
| `RAIN` | 0.40 | 1.0 | streak count (v1: 94 mid + 76 far + 18 near per frame; now 38 + 31 + 0) |
| `RAIN_NEAR` | 0.0 | 1.0 | the blurred near-lens streak sheet (1.5-6 D from the lens) |
| `RAIN_OPACITY` | 0.75 | 1.0 | streak brightness where light is behind it (headlights, lamps, neon) |
| `RAIN_DARK` | 0.25 | 1.0 | the unlit floor of a streak (0.04 linear): streaks over dark sky and shade |
| `RAIN_FACE` | 0.12 | 1.0 | streak opacity left in front of actors (object index 2) |
| `RAIN_LEN`, `RAIN_WIDTH` | 0.70, 0.5 | 1.0 | streak length; width (2 px -> 1 px at 720x1280) |
| `SPLASH` | 1.0 | 1.0 | road splash crowns (kept; 110 per frame) |
| `HAZE` | 0.45 | 1.0 | depth haze, lamp glow veil, lit rain mist (gain x, haze distance 1400 D / level) |
| `SHAFT` | 0.55 | 1.0 | light cones in the rain (x `shaft_gain` 0.8) |
| `BLOOM`, `BLOOM_R`, `BLOOM_WIDE` | 0.70, 0.60, 0.35 | 1.0 | bloom strength, radius (3 / 9 / 20 px), the 60 px wide glow |
| `HALO`, `HALO_R` | 0.50, 0.60 | 1.0 | coloured halo gain and radius (95 px) |
| `DOF` | 0.40 | 1.0 | lens blur radius (x `coc_k` and `coc_max` from the camera) |
| `DOF_BAND` | 0.35 | 0.0 | sharp zone behind focus: nothing nearer than focus / (1 - band) = 1.54 x the focus distance is blurred; blur at infinity = `coc_k` x DOF x (1 - band) |
| `DOF_MACRO` | 0.70 | 1.0 | lens blur for macro inserts (`coc_k` >= 20: S01, S08, S09), no band |
| `TILT` | 0.30 | 1.0 | tilt-shift blur radius (bottom 22 %, top 14 %) |
| `CLARITY` | 1.3 | 1.0 | local contrast (x `clarity` 0.35) |
| `SHARPEN` | 0.35 | 0.0 | unsharp mask, sigma 1 px, limited to +-25 % of local luma; makes up for the 75 % render scale |

Also changed in v12:
- Depth and object-index passes are salt-and-pepper behind smoke cards and glass at 5 spp. The old lens blur hid the resulting stipple; `process()` now replaces depth / index by a 5 px median in those regions and `ink()` fades outlines there (`quiet` mask).
- `post9.dof(..., band=0.0)`: new optional argument (default = old behaviour).
- Not changed: wet asphalt, puddles, ripple rings (materials), `streak` (wet-road reflections), `sparkle`, the grade (`saturation`, `lift`, `toe`, `no_violet`), vignette, lights.
- The final tier still renders at 75 % (37-42 CPU s per frame). `run.py --pct 100` renders at full scale: Laplacian variance x 1.3, 65-67 CPU s per frame.
