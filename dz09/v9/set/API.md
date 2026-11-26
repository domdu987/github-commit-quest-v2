# v9/set: ref-D NIGHT finish for the EP.1 expressway (clear moonlit night in rain)

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`.
The library has the same API shape as v6/set. v4 (`PROJ/v4/set_expressway`) is imported read-only. v6/set is copied, not edited: `beauty6.py` is the v6 beauty module with `render6` pointed at `render9`.
Target: ref D night frames f_076, f_080 and f_082 (`ref/d/night5.png`). Detail and material finish come from f_015-f_020, f_036 and f_115.

## Files

| File | What it does |
|---|---|
| `beauty.py` | v9 entry point. `build()`, `setup_render()`, `set_moon()`, `world9`, `lights9`, `work_lamp`, `m_asphalt9`, `materials9`, `detail9`. It exposes `B.X`, `B.kit`, `B.V`, `B.presets`, `B.render9`, and `B.render6` (alias of render9). |
| `beauty6.py` | Copy of v6 beauty (grime, hero paint, `detail6`: pylons, telecom poles, skyline layer 2, dead billboard, grit). |
| `presets.py` | Unchanged copy of the v6 presets and `foreground()`. |
| `post9.py` | Post chain, retuned. See "Post" below. |
| `render9.py` | `render(out_noext, frame, post_opts)` as in v6, plus `repost(out_noext, **overrides)`, which re-grades from the kept EXRs in about 3 CPU s. |
| `look9.py` | Copy of `v6/look/look.py`, pointed at v9 (v6 cast kept). Outputs go to `look/out/`. Per-shot changes are listed below. |
| `sheet9.py` | Writes `vs_ref_night.png` (v6, v9 and the closest ref frame per shot) and `wide_169.png` (S06 and S24 at 16:9). |
| `measure9.py`, `measure_all.py` | Metrics. Output: `look/measure.json`. |

## Usage (unchanged from v6)

```python
import sys; sys.path.insert(0, PROJ + "/v9/set")
import beauty as B
A = B.build()                       # ~5 s
B.setup_render("final", threads=4)  # 6 spp @ 75 %, adaptive 0.07, 8 transparent bounces
cam = B.presets.use("eye", A)       # or your own camera (see v6 API.md)
B.set_moon(azimuth_deg=30, elevation_deg=17)   # optional, per shot: turns the moon disc, halo, clouds, key and glint together
r = B.render6.render("/abs/out/S06_f0001", frame=1, post_opts={"exposure": 1.6})
B.render9.repost("/abs/out/S06_f0001", toe=0.02)   # re-grade only
```

- Marks, pass indices and the character placement rules are the same as v6/set API.md.
- New anchor: `A["work_lamp"]` (the work-lamp head position).
- Shot exposures written for v6 (1.5-1.7) carry over. post9 multiplies them by `EXPOSURE_SCALE` 0.75 internally.

## What changed against v6

### Light

- **Sky (`world9`)**
  - Clear cornflower gradient, hue 222-232: zenith (0.030, 0.058, 0.170), horizon band (0.10, 0.145, 0.285) linear.
  - The side of the sky toward the moon is lighter.
  - Broken rain clouds: dark blue bodies, with silver-blue rims near the moon.
  - Big soft moon: a 1.9° disc with faint maria, a ~6° halo and a faint 15° glow.
  - No lavender anywhere.
  - Diffuse rays see a cheap copy without the cloud noise (Mix Shader on Is Diffuse Ray), at strength `SKY_FILL` 0.65.
- **Moon key:** `moon_key` SUN, strength 7, angle 1.4°, colour (0.66, 0.78, 1.0), diffuse only.
- **Moon glint:** `moon_glint` SUN, 0.6, 9°, glossy only. It is light-linked to `road_L`/`road_R` only (collection `MOON_GLINT_RECEIVERS`). This gives a moon sheen on the wet road that cars, debris and poles cut with long shadows, without blowing out car glass.
- **Sodium spots:** 6.5 kW, colour (1, 0.60, 0.28), radius 0.15 (crisp), 80° cone.
- **Other practicals:**
  - Flood: 36 kW, radius 0.08, cool.
  - Headlights: 4.2 kW, radius 0.04.
  - Beacons and hazards: radius 0.05.
- **Work lamp (new):** a warm halogen work lamp on a tripod in lane 1 behind the rescue, at (-3.5, 40.6), head 2.25 D, 6 kW spot, 110°, radius 0.06, colour (1, 0.64, 0.34). It has a lit lens, a small spill light and a cable to the truck. This is our campfire: a warm pool against the cool moonlight, a background practical in S13 and S24, and long radial shadows toward the lens.
- **Ambient:** the fake ambient emission is cut from 0.3 to 0.10. GI and the sky do the fill.

### Materials

- **`asphalt_v9`**
  - Lighter dry aggregate (#40414a-#5a5b63), so light pools and cast shadows read.
  - Damp sheen: roughness 0.28-0.52.
  - Standing water about 30 %: roughness 0.02, dark mirror.
  - Rain rings: one ring per drop cell at a random age, re-seeded each frame.
  - Thinner tar-sealed crack network, resurfaced patches, 2-4 cm aggregate bump, grit, ruts, oil strips, worn lane paint.
- **Glass shards:** roughness 0.02, for sparkle.

### Detail

All of this is in `detail9`, in the `DETAIL_V9` collection.

- **Trees:** about 60 Bangkok roadside trees, rain trees (lumpy crowns, one mesh each) and palms, both sides at o ±32-75. Their crowns rise just above the deck, so they make dark silhouettes against the lighter sky. They play the role of the ref's tree lines.
- **Billboards:** 4 uni-pole billboards. 3 are dark silhouettes and 1 has a dim poster. The v6 dead billboard panel is now a dark back, and its spot is down to 1.8 kW.
- **Back skyline:** 44 towers behind the deck start (y -1100 to -2600) for reverse angles (S18, S20).
- **Ground scatter:**
  - 1,300 small glass shards (dense around the door) and plastic fragments;
  - 180 wet leaves;
  - two rubber skid arcs behind the hero car.

### Post (`post9.process`, info keys as in v6 plus the ones below)

- **Haze:** far-only aerial blue. `haze_z0` 1400 D (v6: 420), luminous blue HAZE_BASE, lamp-glow pollution at 0.12 (v6: 0.30), rain mist only near lights at 0.05 (v6: 0.10).
- **`sparkle`** (default 1.0, `sparkle_n` 160): 1-2 px wet-road glints weighted by local light, with a few 4-point stars. Applied before DOF.
- **`clarity`** (0.35): mid-frequency local contrast on luminance.
- **Shafts:** `shaft_gain` 0.3 (v6: 0.6).
- **Rain:** v4 streaks at density 0.9, plus `splashes()` (`splash_n` 70): drop crowns with flying droplets, lit by local light.
- **Bloom:** 0.5 tight on lights, `bloom_wide` 0.18.
- **Grade**
  - Gains (0.97, 0.99, 1.06) × exposure × 0.75, saturation 1.10.
  - Shadows: R is pulled hard, G a little, so they stay cornflower (225-235) rather than violet.
  - Highlights pulled 10 % toward white.
  - Toe `c²/(c + 0.014)` for true blacks, shoulder from 0.56.
- **Vignette:** 0.20.
- **Hue clamp `no_violet`:** 252-342° goes to 238° (v6 sent it to 250°).

## look9.py: per-shot changes (framings unchanged)

- **S18:** `moon_key` × 0.55 and exposure 1.15. The low moon and the brighter sky made the white bonnet blow out.
- **Samples:** `SPP_SHOT = {"s09": 4, "s24": 5}`. The macro is 90 % lens blur, and S24 is the heaviest frame. All other shots render at 6 spp.

## Measured (`look/measure.json`; 720x1280; v6 stills were rendered at 360x640 and upscaled for measuring)

### Time per frame (CPU s, 4 threads)

Measured while another worker was rendering (load average 4-5).

| Frame | Render | Post | Total |
|---|---|---|---|
| S06 | 31.4 | 3.3 | **34.7** |
| S09 (4 spp) | 27.1 | 3.2 | **30.3** |
| S13 | 33.6 | 4.5 | **38.2** |
| S18 | 16.4 | 3.5 | **20.0** |
| S20 | 26.4 | 3.4 | **29.8** |
| S24 (5 spp) | 36.2 | 2.9 | **39.1** |
| S06 16:9 | 30.5 | 3.6 | **34.1** |
| S24 16:9 (5 spp) | 33.5 | 2.9 | **36.4** |

The same s24 camera in the v6 set measured 42.5 CPU s at 6 spp.

### Look

| | L mean | deep shadow (L<0.05) | L p95 | blue % | orange % | red % | magenta % | violet % | shade hue (median) | edge density | local contrast |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ref f_076 | 0.392 | 0.087 | 0.79 | 88.6 | 4.9 | 2.1 | 0.6 | 3.5 | 238 | 0.087 | 0.117 |
| ref f_080 / 082 | 0.23 | 0.23 | 0.70 | 100 | 0 | 0 | 0 | 0 | 222 | 0.071 | 0.088 |
| v6 S06 / v9 S06 | 0.273 / 0.364 | 0.046 / 0.061 | 0.86 / 0.86 | 67.8 / 69.1 | 2.2 / 6.0 | 28.4 / 24.3 | 0.3 / 0.1 | 1.1 / 0.05 | 240 / 226 | 0.023 / 0.034 | 0.087 / 0.105 |
| v6 S09 / v9 | 0.521 / 0.491 | 0.025 / 0.034 | 0.96 / 0.91 | 20.3 / 21.6 | 11.9 / 16.2 | 57.5 / 48.5 | 0.2 / 0.1 | 0.6 / 0.01 | 238 / 224 | 0.003 / 0.004 | 0.061 / 0.060 |
| v6 S13 / v9 | 0.260 / 0.377 | 0.112 / 0.116 | 0.77 / 0.91 | 65.7 / 59.7 | 3.8 / 22.0 | 27.0 / 18.0 | 0.4 / 0.2 | 3.0 / 0.04 | 245 / 229 | 0.020 / 0.024 | 0.076 / 0.088 |
| v6 S18 / v9 | 0.367 / 0.406 | 0.044 / 0.050 | 0.79 / 0.93 | 98.8 / 99.1 | 0.7 / 0.8 | 0.2 / 0.1 | 0.0 / 0.0 | 0.3 / 0.01 | 240 / 222 | 0.025 / 0.025 | 0.067 / 0.071 |
| v6 S20 / v9 | 0.446 / 0.481 | 0.062 / 0.044 | 0.93 / 0.90 | 87.4 / 80.8 | 1.7 / 15.0 | 9.9 / 3.6 | 0.2 / 0.2 | 0.8 / 0.03 | 240 / 224 | 0.014 / 0.019 | 0.091 / 0.098 |
| v6 S24 / v9 | 0.236 / 0.304 | 0.058 / 0.068 | 0.67 / 0.83 | 34.2 / 47.1 | 24.3 / 26.0 | 28.4 / 21.2 | 1.6 / 0.8 | 7.5 / 0.2 | 248 / 226 | 0.024 / 0.050 | 0.083 / 0.109 |
| v9 S06 / S24 16:9 | 0.373 / 0.305 | 0.083 / 0.095 | 0.88 / 0.91 | 73.4 / 40.7 | 8.0 / 25.9 | 17.9 / 28.4 | 0.16 / 1.4 | 0.08 / 0.3 | 224 / 226 | 0.043 / 0.059 | 0.114 / 0.130 |

- Hue shares come from `v3/tools/hue_report.stats()`. Shade hue is the median hue of blue-violet pixels with V < 0.5 (`measure9.py`).
- The ref night's shade hue measures 222-238, not 240-260. v9 sits at 222-229 (clear blue). Moving it toward 240 makes the frames read lavender again.
- Red share is mostly the orange vests (hue ~15°) and tail lights. Magenta stays at or below 1.4 % everywhere.

## Still different from ref D

- **Deep-shadow share.** It is 0.03-0.12 against the ref's 0.09-0.24, and the frames are brighter at p95 (0.83-0.93 against 0.70-0.79). There are fewer true-black silhouette masses. The ref gets them from dense conifer walls; ours are cars, tree crowns and barriers. The S18 and S20 foregrounds are the white hero car, which mirrors the bright sky. Raise `toe` (0.02) or lower the exposure with `repost` if wanted.
- **Long cast shadows.**
  - Moon shadows read on the road in S24 (glint sheen cut by debris and poles), and the work lamp casts radial shadows.
  - The bean characters' thin legs throw small shadows, so the striking T13-style figure shadows toward the lens do not happen yet.
  - On dark wet asphalt, diffuse shadows can never be as graphic as on white snow.
- **Edge density.** 0.02-0.06 against 0.07-0.09. Our top thirds are still mostly sky: there is no forest wall. More cables, signage or a denser tree line would close this.
- **Detail.**
  - The road micro detail is good up close.
  - The tree crowns are lumpy low-poly, fine as silhouettes but not up close.
  - No bevel pass was done on the v4 props.
- **Characters** are the v6 cast (to be swapped). The cast shader's own emission and lavender shadow tint are unchanged.

---

# Pass 2 (director's review of `vs_ref_night.png`)

Frames from pass 1 are kept in `look/pass1/`, and the old v6-against-pass-1 sheet is kept as `vs_ref_night_pass1.png`. `vs_ref_night.png` now shows v9 pass 1 | v9 pass 2 | ref for each shot. `wide_169.png` holds S06 and S24 at 16:9 (pass 2).

## Changes

- **Movable work lamp** (`beauty.place_work_lamp(A, base, aim, energy, head_z, cable, hide)`). It rebuilds the tripod lamp, the light and the spill. `look9.shot()` places it for each shot:
  - S06: behind Kong, between the car and the crew, aimed at the lens, 6.5 kW.
  - S13: behind Kong, frame left, 8 kW.
  - S24: beyond the actors at (-5.4, 39.8), aimed back toward the camera side, 8 kW.
  - S18: behind the hero car, 9 kW, head 3 D. The intent was for the cabin shadow to fall on the bonnet; it does not read.
  - S20: in front on the same side, raking along the door, 7 kW. The mirror and pillar throw long shadows across the white panel.
  - S09: default spot.
- **Shadow proxies** (`look9.shadow_proxies`). Each visible character's leg and arm curves are copied at 3.2× (legs) or 1.9× (arms) the bevel thickness. The copies are shadow-only: invisible to camera, diffuse, glossy and transmission rays. The thin bean legs now throw readable shadows.
- **Moon sheen:** the road-only glint sun goes from 0.6 to 1.3 and from 9° to 12°, so the midground road carries a broad, cool sheen.
- **Hero car:** base paint goes from #e4e2dc to #c9c6be, with more mud. S18 has driver fill at 26 W; S20 has driver fill at 20 W.
- **`beauty.bevel_pass()`** (called from `detail9`). Every small hard-edged unique set mesh within 30 D of the action gets a 2-segment, angle-limited Bevel modifier, 3 % of its size and at most 0.035 D. The actual count is in `A["bevelled"]`.
- **New framing kinds in `presets.foreground`:**
  - `beam`: a dark gantry underside across the top.
  - `barrier`: a dark concrete edge in a bottom corner.
  - I tried `beam` in S06 and S13 and removed it: it read as a letterbox bar. Neither kind is used in the shots now.
- **`render9.repost(out, **overrides)`** and **`grade_fit.py`**. grade_fit bisects each frame's exposure toward p95 0.78, then its toe (`toe` info key, grade `c²/(c+toe)`) toward a deep-shadow share of 0.12. Results are in `look/grade_fit.json`, and `look9.render()` applies them automatically.
  - S06 is set by hand to exposure 0.95 / toe 0.03 (16:9: toe 0.012). The backlight flare keeps p95 high.
  - S18 is set by hand to 0.9 / 0.03 for a darker bonnet.

## Pass-2 numbers (720x1280; CPU measured under a parallel worker's load, average 4-5)

| Frame | CPU s render + post | L mean | Deep shadow | L p95 | Blue / orange / red / magenta % | Shade hue |
|---|---|---|---|---|---|---|
| S06 | 31.0 + 3.1 = **34.1** | 0.327 | 0.095 | 0.91 | 59.5 / 16.0 / 24.1 / 0.06 | 224 |
| S09 (4 spp) | 26.4 + 3.1 = **29.5** | 0.368 | 0.119 | 0.77 | 19.7 / 8.2 / 57.4 / 0.18 | 224 |
| S13 | 33.7 + 3.9 = **37.6** | 0.319 | 0.122 | 0.78 | 56.2 / 17.5 / 26.0 / 0.11 | 225 |
| S18 | 17.5 + 3.3 = **20.8** | 0.250 | 0.128 | 0.53 | 99.2 / 0.7 / 0.0 / 0.00 | 222 |
| S20 | 26.1 + 3.2 = **29.3** | 0.341 | 0.121 | 0.82 | 34.5 / 62.9 / 2.4 / 0.04 | 224 |
| S24 (5 spp) | 34.0 + 3.0 = **37.0** | 0.259 | 0.153 | 0.78 | 37.0 / 38.9 / 19.3 / 0.23 | 225 |
| S06 16:9 | 30.3 + 3.8 = **34.1** | 0.319 | 0.112 | 0.86 | 65.7 / 13.8 / 19.9 / 0.08 | 224 |
| S24 16:9 (5 spp) | 32.8 + 2.9 = **35.7** | 0.249 | 0.170 | 0.79 | 31.8 / 33.6 / 30.3 / 0.99 | 226 |

Full table, including the v6 and pass-1 rows: `look/measure.json`.

## Still different after pass 2

- **S06 p95 is 0.91** (target 0.75-0.80). The work lamp sits in frame right behind Kong, and its flare and lit road set p95. Darkening further sinks the sky.
- **S18:** the bonnet is darker but still a flat grey plane. The lamp behind the car does not throw the cabin shadow onto it (it is occluded / out of reach). The driver reads, but softly, through the cracked glass. This shot needs a dedicated light rig or a shadow-casting gobo.
- **Warm share is higher** (orange 16-63 %), by design: these are warm pools against cool moonlight. The ref night is 5 % warm.
- **Character shadows:** the bean figures' shadows now read in S24 and S20. In S06 and S13 the long leg shadows fall mostly under the foreground wheel and debris or into lens blur, so they are less graphic than in ref f_076.
- **Edges and detail density** are unchanged (0.02-0.05 against the ref's 0.07-0.09).
