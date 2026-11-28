# refD_beauty: set beauty, light and materials of reference D, and how to give the night-rain expressway the same finish

Lens: how the set is lit, and the materials, atmosphere and grade. Not about characters or camera, except where lighting touches them.
Reference: `ref/d/ref.mp4` (720x1280, 71 s). Frame ids: **h###** = `ref/d/frames2/f_###.png` (every 0.5 s, t = (n-1)*0.5 s). **T##** = `ref/d/frames/f_0##.png` (every 3 s, t = (n-1)*3 s).
We copy the look only. We do not copy the WW2 Finland subject, the uniforms, the "SEGMENT ZERO" mark or the captions.
Tools: `spec/refD_beauty_tools/measure.py` (all statistics below) and `spec/refD_beauty_tools/beauty_test.py` (A/B render on the v4 set; it does not change v4 files).
Evidence: `spec/refD_evidence/contact_05s.png` (all 142 frames, numbered), `beauty_night.png` (T13 | T14), `beauty_day.png`, `beauty_int.png`, `zoom_*.png`, and `beauty_ab_eye.jpg` (ref T13 | our v4 eye final | our eye with the section 4 settings).

Conventions are as in LOOK_SPEC_C section 0. L is Rec.709 luma on encoded sRGB, from 0 to 1. S is HSV saturation. Hue families come from hue_report. Statistics on the reference mask out the caption band (y 855-940) and the watermark.

---

## 1. Shot groups in ref D (from contact_05s.png)

| Group | Frames | Light |
|---|---|---|
| night (our analogue) | h073-h082: campfire h074-h079 (T13), moonlit forest h080-h082 (T14) | moon behind the subject, sky dome, one warm practical |
| dusk / low sun | h009-h016, h069-h071, h123-h127, h137-h140 | low warm sun, pink-violet sky |
| day snow | h045-h068, h084-h122 (T8, T11, T12, T15-T20) | high sun with crisp shadows, blue sky fill |
| warm interior | h027-h044 (T5-T7) | lamp key, orange bounce, dark corners |
| 2D inserts (excluded) | h021-h026, h135-h136 | n/a |

**The night group is the target for EP.1.** The other groups show the house finish: GI bounce, contact AO, a soft-shouldered tone curve and dense mid-frequency detail.

## 2. Measurements

### 2.1 Tone and colour (group means)

| Group | L p1 | L p5 | L p50 | L p95 | L p99 | S mean | S p90 | blue | orange+red | shadow RGB (L<p20) | mid RGB | highlight RGB (>p90) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ref night h073-h082 | **0.002** | **0.014** | 0.303 | **0.735** | 0.868 | **0.405** | 0.629 | **0.918** | 0.044 | **(0.053,0.060,0.131)** | (0.283,0.298,0.409) | **(0.709,0.744,0.867)** |
| ref campfire h074-h079 | 0.002 | 0.017 | 0.397 | 0.802 | 0.925 | 0.336 | 0.572 | 0.864 | 0.073 | (0.073,0.074,0.136) | (0.385,0.388,0.508) | (0.786,0.804,0.892) |
| ref forest h080-h082 | 0.001 | 0.004 | 0.093 | 0.685 | 0.841 | 0.534 | 0.701 | 0.998 | 0.000 | (0.004,0.012,0.062) | (0.061,0.097,0.171) | (0.635,0.707,0.893) |
| ref dusk | 0.166 | 0.263 | 0.582 | 0.795 | 0.856 | 0.258 | 0.418 | 0.262 | 0.605 | (0.316,0.316,0.379) | (0.636,0.565,0.592) | (0.899,0.780,0.694) |
| ref day | 0.076 | 0.170 | 0.625 | 0.849 | 0.917 | 0.251 | 0.482 | 0.573 | 0.383 | (0.222,0.252,0.291) | (0.610,0.625,0.663) | (0.884,0.849,0.812) |
| ref interior | 0.050 | 0.150 | 0.374 | 0.879 | 0.958 | 0.513 | 0.780 | 0.011 | 0.938 | (0.299,0.155,0.104) | (0.518,0.350,0.230) | (0.931,0.875,0.715) |
| **ours v4 eye final** | **0.102** | **0.139** | 0.278 | **0.509** | 0.762 | **0.278** | 0.419 | **0.557** | 0.376 | **(0.171,0.150,0.174)** | (0.289,0.275,0.345) | **(0.633,0.519,0.448)** |
| ours v4 high final | 0.116 | 0.135 | 0.192 | 0.431 | 0.801 | 0.234 | 0.414 | 0.268 | 0.606 | (0.144,0.138,0.173) | (0.206,0.185,0.214) | (0.618,0.456,0.336) |
| ours v4 top_down | 0.121 | 0.128 | 0.152 | 0.315 | 0.678 | 0.264 | 0.333 | 0.653 | 0.286 | (0.126,0.127,0.175) | (0.148,0.149,0.196) | (0.442,0.347,0.291) |
| ours v4 ots | 0.081 | 0.096 | 0.174 | 0.759 | 0.832 | 0.331 | 0.525 | 0.264 | 0.679 | (0.109,0.100,0.145) | (0.217,0.175,0.226) | (0.896,0.736,0.655) |

What the numbers say:
1. **Blacks.** The ref night has true blacks: p1 is 0.002 and the far tree line has p5 0.003 (T13 y 290-340). Our p1 is 0.10-0.12 on every preset, so the whole frame looks milky. The cause is `post.FOG_BASE` (0.023 linear, which encodes to about 0.165) together with the mist layer. Fog lifts the darks; it does not just fade them toward the sky.
2. **Highlights.** The ref night reaches p95 0.735 on lit surfaces (snow, heads, sky). Ours reaches only 0.43-0.51. Our lit surfaces are too dim, and the only bright pixels are the lamps themselves.
3. **Hue.** The ref night is a single cool key: 92 % of the chroma mass is blue, and warm is 4-7 %, confined to the fire pool. Ours is 27-56 % blue and 29-61 % warm, because the sodium lamps (26 kW, colour (1, 0.45, 0.12)) and the tail lights wash the whole frame. In the ref, highlights are cool white (B/R 1.22). Ours are warm (B/R 0.71).
4. **Shadow colour.** The ref shadows are deep, saturated blue: B/R 2.5 in the night group, (0.004, 0.018, 0.072) in the forest of T14. Ours are neutral to magenta grey: B/R 1.0 at L 0.15.
5. **Saturation.** The ref night has S mean 0.40. Ours has 0.23-0.33.

### 2.2 Light: key, fill, bounce, AO (night frames T13 and T14, day T8)

- **Key = moon, used as a back or three-quarter-back light.** In T13 the moon sits at (435, 160), and in T14 at (880-720, 150), above the subject and in front of the camera. Every cast shadow runs toward the camera, diagonally across the foreground (T13 y 780-1280). Shadows are crisp at the caster: box and tripod contacts are 2-4 px wide (zoom_fire_contact.png). They widen to about 40 px some 300 px from the caster, along row y 1050 (10-90 % transition over 3-4 samples of 12 px). That fits a sun lamp of angle **about 2-4 deg**.
- **Fill = sky dome.** Shadowed snow in T13 still reads L 0.23-0.34, a saturated blue (0.32, 0.38, 0.55), against 0.52 on lit snow. The key-to-fill ratio is therefore about 1.6:1 in luma, or **about 2.5:1 in linear**. The fill is strong and coloured. Our v4 world is black to diffuse rays and fakes the fill with a flat ambient emission.
- **Bounce and AO (GI).** Heads are not flat. In T14 the head reads L 0.72 at the top and 0.50 at the bottom (-30 %), cool white (0.705, 0.723, 0.818). Under the hat brim it drops 27 % (row 545: 0.53). In T8 the head picks up a warm-pink lit side (0.96, 0.92, 0.87) and a cool snow bounce below it. Contact AO under feet, boxes and logs is clearly visible: a dark rim 3-8 px wide at the touch line. This is a path-traced look with at least 2 diffuse bounces, not ambient-only.
- **Warm practicals are small and local.** The T13 fire pool is warm only within r ≈ 30 px of the flames: (0.49, 0.39, 0.25) at r 30 turns back to blue (0.43, 0.34, 0.34) at r 50 and to sky blue beyond r 80. The bloom around the fire is tight (no glow beyond r 40). The bloom around the moon is wide: L 0.93 core, 0.87 at r 40, 0.72 at r 80, 0.54 (sky level) from r 120, so the halo radius is about 100 px at 720 w.
- **Sky gradient (T13, x 560-640).** From the top down: L 0.52 (0.43, 0.52, 0.76), 0.58 at y 80, 0.72 at y 200 (moon glow and horizon), then the tree line. A periwinkle sky, brighter toward the moon and horizon, with soft cumulus wisps (L +0.05). T14: 0.59 at the top, 0.68 at y 160. **The sky is the brightest large area in the night frames.** Ours is 0.24-0.40.

### 2.3 Atmosphere

- The ref has **no grey fog on darks**. The far tree line keeps p5 0.003, the mid trees 0.005 and the near trees 0.007. Depth reads by **size and density, not by lifted blacks**. Haze appears only as a luminous horizon band (sky L +0.1 behind the tree line), as snow-spray glow near the camera in T11/T13, and as sparkle particles (1-2 px white specks, about 40 per frame, in h080-h082).
- Our skyline (eye, y 520-640) has p5 0.167. That is the fog lift, and it turns the skyline into grey cut-outs.

### 2.4 Detail density and micro detail

| | Canny edge density, all | top / mid / bottom third | local contrast (σ16 std) |
|---|---|---|---|
| ref night | **0.096** | 0.096 / 0.129 / 0.057 | **0.104** |
| ref campfire | 0.108 | 0.110 / 0.135 / 0.074 | 0.119 |
| ref day | 0.070 | 0.106 / 0.075 / 0.021 | 0.114 |
| ours v4 eye final | **0.020** | 0.005 / 0.045 / 0.011 | **0.055** |
| ours v4 high final | 0.039 | 0.028 / 0.055 / 0.032 | 0.063 |

- The ref is **3-5x denser** in edges. Its top third is full: about 40 conifer silhouettes, power lines and cloud edges (T13). Ours is an empty sky (0.005) over a very sparse foreground.
- Ref micro detail on the ground: wind ripples and sastrugi (normal scale about 20-60 px of streaks), footprint dents, ski tracks (T14) and snow sparkle. Material texture scale is about 1/30-1/60 of the frame width. Snow-cap blobs on trees have soft SSS-like gradients.
- Materials read as matte to satin (roughness about 0.5-0.8). The only spec is on metal and wet edges. There is no hard clearcoat.

### 2.5 Grade, vignette, grain

- **Tone curve:** a soft toe (blacks crushed to 0.00-0.01 but still blue) and a filmic shoulder: p99 is 0.84-0.92 in every group, and bright skies never clip flat except at the moon core. Ours is a Standard view with a hard clip.
- **Lift/gamma/gain:** night has shadows biased to blue (B +0.07 over R at L 0.05), mids blue (B/R 1.45) and highlights near-white cool (B/R 1.22). Interior and day keep the same structure, with the bias set by the key colour. This is a split-tone, not a single overall tint.
- **Vignette (mean frame, corner / centre):** 0.87 over all non-insert frames; night 0.68 (campfire 0.85). Ours is 0.735 over the drafts. Keep ours, with corners at 0.75-0.85 of the centre.
- **Grain:** residual std in flat areas 0.001-0.005 (ref) against 0.001 (ours). The ref is essentially clean, and only the night campfire shows 0.005 of noise from sparkle and compression. **Add no grain**, or at most σ 0.004 luma.
- **Bloom:** wide and soft on the moon and sky emitters (radius about 100 px), tight on practicals. Ours (0.55) is fine; lower it to 0.45 once the shoulder is in.

## 3. Diagnosis of v4 set_expressway (sheet_916.jpg, compare_ref.jpg)

1. `setup_render`: **`diffuse_bounces = 0`** means no GI, no bounce and no contact AO. All fill comes from a flat ambient emission (`kit.AMBIENT` (0.030, 0.040, 0.088) times albedo). The result is the flat CG-plastic look in sheet_916, with dark car flanks of a single value.
2. The world has strength `0.72 * (1 - IsDiffuseRay)`, so the sky does not light anything. With `sampling_method = NONE` it cannot be a light.
3. There is **no moon key lamp.** The moon is only a disc in the world, so there are no long cast shadows and no rim on car roofs or Kong.
4. The sodium spots (26 kW) dominate the hue, so the frame goes orange and magenta.
5. `post.fog` with `FOG_BASE` 0.023 linear lifts every dark to L 0.10-0.17. The grade has only a tiny offset (+0.004) and a hard clip.
6. The foreground road is a dark, glossy, empty plane: the bottom third of eye and low has edge density 0.011.

## 4. What to change (tested: `refD_beauty_tools/beauty_test.py`, evidence `beauty_ab_eye.jpg`)

### 4.1 Cycles settings (tested, inside budget)

```python
cy.max_bounces = 4; cy.diffuse_bounces = 2; cy.glossy_bounces = 2
cy.transmission_bounces = 1; cy.volume_bounces = 0; cy.transparent_max_bounces = 14
cy.sample_clamp_direct = 0.0; cy.sample_clamp_indirect = 3.0; cy.blur_glossy = 0.7
cy.use_light_tree = True; adaptive_threshold 0.05; OIDN albedo+normal (unchanged)
quality "final" = 8 spp @ 75 % (Lanczos up) ; "final12" = 12 spp @ 75 % for holds
```

- Measured at a load average under 1: **beauty final8 = 22.6 CPU s render + 2.1 post = 24.7 CPU s per 720x1280 frame** (v4 base: 19.8 + 2.5). **Beauty final12 = 30.4 + 2.2 = 32.6 CPU s.** Both are inside 40 CPU s. The v4 timing.json figure of 50-54 s was taken at a load average of 10 and is inflated by contention.
- Do not use `use_fast_gi` (AO-replace): the 2 real diffuse bounces cost only +14 % and give real contact AO.

### 4.2 Lights

| Light | Setting |
|---|---|
| **moon_key** (new) | SUN, `angle` 3 deg, colour (0.62, 0.74, 1.0) (about 8000 K blue-white), strength **2.5** (tested; 1.2 is too weak). It travels toward the camera: direction (0.35, -0.80, -0.48) for the eye/low/dutch presets, so shadows of cars, barrier posts and Kong run toward the lens as in T13. Set `ob.visible_glossy = False`, otherwise the sun makes a huge streak on the wet road; the world moon disc stays in reflections. For each preset, keep the moon 15-35 deg above the horizon and within ±40 deg of the view axis. |
| **sky fill** | World diffuse visibility on: set the SUBTRACT(1, IsDiffuse) node to a constant of 1, multiplier **1.1** (was 0.72 camera-only). `world.cycles.sampling_method = 'MANUAL'`, `sample_map_resolution = 256`. Target key:fill about 2.5:1 linear on the road and cars. |
| **ambient emission** | `Emission Strength` 1.0 to **0.3** on every kit material (the GI now does the fill). Use 0.0 on Kong-adjacent hero props if they read flat. |
| **sodium spots** | 26 kW down to **9-12 kW**, colour (1.0, 0.62, 0.30) (less red), `shadow_soft_size` 0.12 up to **0.4**. Goal: warm pools of about 3-5 m radius under each lamp, as with the fire in T13, not a frame-wide wash. Warm hue mass ≤ 0.25 of the frame. |
| **flood key** (rescue pickup) | Keep 30 kW but `shadow_soft_size` 0.06 up to **0.35**: penumbra 2-4 px at contact, about 30 px at 300 px. Colour (0.95, 0.97, 1.0), cool LED, not warm. |
| beacons, hazards, headlights | Keep. They are the story's red, amber and white accents. Red and amber mass is allowed up to about 0.15. |

### 4.3 Materials

- **Wet road**: give a large area **diffuse response** so moonlight and shadows read. Base asphalt (0.10, 0.10, 0.11) linear, roughness 0.55 on dry patches and **0.08 in puddles**. Use a puddle mask from noise (scale about 3 m features), covering 35-45 % of the area. Add an aggregate bump (scale 2-4 cm, strength 0.15), tyre-track darkening strips, and lane-paint wear (paint roughness 0.4, edges chipped with noise). The aim is for the bottom third to reach edge density ≥ 0.04 and to show 3-6 long moon-shadow stripes.
- **Car paint**: coat 0.4-0.6 with coat roughness 0.08, base roughness 0.45. Add rain-bead normal detail (`tex/` droplet map, scale about 1.5 cm) on roofs and bonnets. Dirt AO in panel lines comes from the existing panel-line map, multiplied into the base at 0.7.
- **Concrete barrier and pillars**: roughness 0.8, a vertical streak/stain map (rain run-off) at 0.15 contrast, a bump at about 1/40 of the frame.
- **Skyline**: material values from about 0.04 to 0.08 linear, so the towers become dark blue silhouettes that keep their lit windows (5-15 % of windows lit, warm and cool mix). Do not grey-fog them.
- Kong and the cards (character lens, noted here for consistency): ref characters are lit, with -30 % top-to-bottom shading and -27 % under brims. The v4 cards are emission-only and flat (Kong reads as violet-grey). At minimum, multiply the card emission by a baked gradient of 1.0 at the top to 0.72 at the bottom, a contact-AO darkening of 0.75 on the lowest 6 % of the body, and a 1-2 px cool rim (0.62, 0.74, 1.0) on the moon side.

### 4.4 Atmosphere (post.py)

- `FOG_BASE` (0.0232, 0.0232, 0.0368) becomes **(0.010, 0.012, 0.024)**, and `fog_z0` 300 becomes **450**. Keep the horizon band `HAZE`: it is the ref's luminous horizon.
- Mist layer: halve it to (0.005, 0.005, 0.010).
- Add rain-lit volume only around lights (the existing shaft splat), not globally.
- Targets for the far skyline: p5 L 0.04-0.07. The deep foreground can go to 0.00-0.02.

### 4.5 Grade (replaces `post.grade`; tested in beauty_test.py)

```python
def grade(rgb):
    c = rgb * np.array([1.0, 1.0, 1.04]) * 1.25            # exposure +0.32 EV, slight blue gain
    l = lum(c)[..., None]; c = l + (c - l) * 1.15            # saturation 1.15
    sh = np.clip(1 - l / 0.06, 0, 1)                         # toe: crush R/G in the deep shadows, keep blue
    c = np.maximum(c - 0.004 * np.array([1, .8, 0]) * sh, 0) + sh * np.array([0, .001, .004])
    k = 0.62; c = np.where(c > k, k + (1 - k) * (1 - np.exp(-(c - k) / (1 - k))), c)   # filmic shoulder
    return np.maximum(c, 0)
```
Keep the vignette as it is (corners at 0.73 of the centre). Bloom 0.45. No grain.

### 4.6 Sky (world)

Move the gradient stops up by about 1.6x in linear: zenith #4a5690, cloud gaps #9aa6d0, a lighter horizon band, and the moon halo `POWER` 900 down to 300, so the halo radius is about 100 px at 720 w. **Target sky L 0.40-0.55** (ref 0.52-0.72; keep it lower for rain), B/R about 1.7.

### 4.7 Detail to add (top third and foreground)

The top third needs edge density ≥ 0.05. Add power and tram wires, gantry trusses, lamp-post arms, a second skyline layer with antennas, billboards on scaffolding, and cloud edges (raise the cloud noise contrast `cl` multiplier from 3 to 5). For the foreground, add debris, glass crumbs (the existing shards), puddle ripples, cones and their shadows.

## 5. Results and targets (eye preset, 9:16)

| Metric | ref night | v4 eye | eye + 4.1-4.2 + 4.4-4.5 (tested) | **target** |
|---|---|---|---|---|
| L p1 / p5 | 0.002 / 0.014 | 0.102 / 0.139 | 0.061 / 0.128 | **≤ 0.02 / 0.03-0.06** |
| L p50 | 0.30 | 0.28 | 0.34 | 0.28-0.36 |
| L p95 / p99 | 0.74 / 0.87 | 0.51 / 0.76 | 0.57 / 0.85 | **0.65-0.75 / 0.85-0.92** |
| S mean | 0.41 | 0.28 | 0.33 | **0.36-0.42** |
| blue / orange+red | 0.92 / 0.04 | 0.56 / 0.38 | 0.63 / 0.30 | **≥ 0.70 / ≤ 0.22** |
| shadow tint B/R | 2.5 | 1.0 | 1.04 | **≥ 1.8** |
| highlight tint B/R | 1.22 | 0.71 | 0.81 | 1.0-1.2 off the practicals |
| Edge density | 0.096 | 0.020 | 0.026 | **≥ 0.07** (top third ≥ 0.05) |
| Local contrast | 0.104 | 0.055 | 0.066 | **≥ 0.09** |
| CPU s / frame | n/a | 22.3 | 24.7 (final8), 32.6 (final12) | ≤ 40 |

The tested subset (bounces, moon key, sky fill, ambient cut, new fog and grade) raised S, highlights and blue mass. It did not reach the shadow tint or the black point: the road is still lifted by sodium and tail-light reflections and by the mist. Steps 4.2 (sodium), 4.3 (road), 4.4 (mist) and 4.6 (sky) are what close those gaps. Step 4.7 (detail) is the main fix for edge density and local contrast. None of them adds render cost beyond about 10 %.
