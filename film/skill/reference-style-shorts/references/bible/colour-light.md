# Colour and light

Paths are relative to the skill's `pipeline/` folder unless they start with `__PROJ__` (the film-1 project, not shipped). Hex is sRGB `#rrggbb`. "Albedo" means the artwork colour fed to the material; "displayed" means what lands on screen after light and grade. Light values are scene-linear RGB with Blender's Standard view transform. Sizes are px at 720x1280. Frames are film frames `g` at 30 fps.

Sheets: `../../assets/bible/colour_swatches_by_role.jpg` (palette by role, reference against our build), `../../assets/bible/colour_light_presets.jpg` (one graded frame per light preset, from the sharp v1.1 frames; the set behind the man in the grey_drizzle tile g1045 is the motion streak of the snap g1042-1056, not a depth-of-field blur), `../../assets/bible/colour_hue_per_shot.jpg` (hue make-up of all 26 shots of the sharp v1.1).

## The rules in brief

1. Large surfaces are saturated mid-darks (S 0.45-0.9, V 0.30-0.75 displayed). Nothing large is paler than V 0.80 except sky. Walls warm (crimson-terracotta, brown, gold), one cool dark block (navy rug or floor).
2. One hard key (a Sun, 0.45-1.5 degrees) plus a flat blue ambient injected as emission. Key yellow-orange, ambient blue: shade turns blue-violet (hue 230-260), never magenta, never brown-grey.
3. Tint the ambient per surface (`shade_mul`, 3 numbers) so warm woods shade orange-brown and red walls shade deep crimson, not magenta.
4. Characters are unlit emission cut-outs: head fill `#fef7f6`, plum ink `#3a2832`. They cast the sun's shadow, receive none, never bloom.
5. Only real emitters (bulbs, flames, lightning) exceed scene-linear 1.0; only they bloom (halo 12-24 px beyond the core).
6. Darks are lifted and tinted (navy-plum), black point luma p1 0.08-0.12. Only the caption outline is pure black.
7. Check every set and every take with `v3/tools/hue_report.py`. Band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10 (% of chroma); sat 0.38-0.48; val 0.45-0.63; dark (V < 0.25) 8-15 %.
8. Exteriors, map close-ups, night and storm may leave the band; write why in the take's QA.md.
9. Finish with the v1.1 grade (`v3/film/out_v11/grade.py`): one S-curve, saturation 1.18, bloom on hot sources, red and white protection, soft ceiling 0.985.
10. No grain, no sharpening, vignette at most 5 %.

---

## 1. Reference (measured)

Two clips: A (flat 2D characters in a real-time-looking 3D world), B (flat characters over painted 2.5D sets). Frame names `a/tSS.S`, `b/tSS.S` (one still every 0.5 s). Source: `spec/color_light_post.md`, `spec/environment_materials.md`.

### 1.1 Palette by role (displayed hex, measured)

HSV is computed from the hex (H degrees, S, V 0-1). See `colour_swatches_by_role.jpg`, left half.

| role | hex (frame) | hue | S range | V range |
|---|---|---|---|---|
| walls | `#561e37` (a/t27.5), `#5e1f36` plank wall (a/t27.5), `#7e5f65` mauve stone (b/t00.0 daylight hall), `#5e2221` dark red backdrop (b/t07.0, b/t23.0), `#7d858e` cool grey stone (B), `#c8bdac` day stone exterior (b/t27.5), `#576295` night wall (b/t34.0) | 333, 338, 348, 1, 212, 36, 229 | 0.12-0.67 | 0.34-0.78 |
| floors | `#152a63` falling to `#17153a` navy carpet (a/t27.5), `#3a3858` navy floor (B hall), `#26395e` navy carpet with red border `#562025` (B), wood lit `#ac825e` (a/t34.5), `#946645` (a/t32.5), road `#cba66f` (b/t28.0), sand `#f3ad6f` (a/t09.0) | 224, 243, 244, 220, 28, 25, 36, 28 | 0.36-0.79 | 0.23-0.95 |
| wood | `#976c4d` (a/t34.5, 25 % of frame), `#6b3723` (b/t22.0, 20 %), wainscot `#491309` (a/t27.5), dark wood `#26140a` (B), plank seam `#432219` (a/t32.0) | 25, 17, 9, 21, 13 | 0.49-0.88 | 0.15-0.59 |
| cloth | drapery `#b64f4b`, drapes `#9d3e3f` (B), seats `#a1001c` to `#da0045`, `#84052e` (a/t27.5), rug border `#562025` (B) | 2, 359, 350, 341, 341, 354 | 0.59-1.00 | 0.34-0.85 |
| metal | lamp holder `#e2a630` (a/t27.5), gold `#cb9f48`, `#f3d26d`, `#dcbe6c` (B) | 40-45 | 0.51-0.79 | 0.80-0.95 |
| sky | day `#4a78cd` top to `#92b7e7` horizon (a/t49.0), `#5795d0` (b/t28.0); sunset `#e16c7e` to `#ffdc99` (b/t31.0); night `#1e2e7b`, `#1748ae` (b/t44.0, b/t34.0) | 219, 214, 209, 351, 39, 230, 221 | 0.37-0.87 | 0.48-1.00 |
| skin fill (heads) | A in every light `#fdf7f7`, `#fcf8f5`, `#fdf8f5`, `#faf9f5`; B per-shot tint: day `#faf8f3`, throne `#faded0`, night `#fbdaf7`, `#fcc8d9`, `#e8c3e5` | A 0-48 (near neutral) | A 0.02-0.04, B night 0.13-0.21 | 0.98-1.00 (B night >= 0.91) |
| ink line | `#251921` (a/t45.0), `#34201d` (a/t02.0), `#302535` (a/t16.0), luma 0.10-0.18; anatomy spec value `#3a2832` | 320, 8, 281, 327 | 0.30-0.44 | 0.15-0.23 |
| shade and darks | ground shade `#332d40`, floor shade `#525065`, character shadow `#252432` to `#444153`, late-afternoon shade `#475895`; mean of darkest tenth `#3d1c32` (A), `#392433` (B) | 244-259 on warm floors; 317-320 for the darkest tenth | 0.21-0.54 | 0.20-0.58 |
| accents | hero vest teal `#50aaa3`, `#3ea693`, yellow-green trim `#76712e`, orange ceiling `#c03c12` / `#c53b14`, lamp core `#fffeec`, cream paper `#fcf4e1` | 175, 169, 56, 14, 57, 42 | 0.07-0.91 | 0.46-1.00 |

"White" props are cream, never white: newspaper `#fcf4e1`, sunlit sheet `#e9d6bb`, white tiles `#efe9ee`. Only heads and light sources are whiter.

### 1.2 Hue families and the target band

Share of the whole frame (pixels with S > 0.15), per clip: warm reds, oranges, browns 52 % in both clips; blue-violet 30 %; magenta 6-7 %; green 1 % (green and teal only as accents).

The project's band is measured with `v3/tools/hue_report.py`: frames scaled to 180x320, caption band rows 212-239 (of 320) removed, each pixel weighted by S x V, only pixels with S > 0.15 and V > 0.15 counted, hue families by edges red 345-20, orange 20-50, yellow 50-75, green 75-165, cyan 165-200, blue 200-255, violet 255-290, magenta 290-345; sat = mean HSV S, val = mean V, dark = share of V < 0.25. The reference rows it prints (run in this session on `__PROJ__/ref`):

| set | red | orange | yellow | green | cyan | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| reference A, whole clip | 33.6 | 23.1 | 0.7 | 0.5 | 0.5 | 29.1 | 2.7 | 9.7 | 0.48 | 0.63 | 0.08 |
| reference B, whole clip | 24.5 | 34.1 | 2.4 | 0.7 | 0.2 | 28.6 | 4.5 | 5.0 | 0.41 | 0.57 | 0.08 |
| reference A interiors (t27.0-28.5, t31.5-35.5) | 40.1 | 27.6 | 0.3 | 0.4 | 0.0 | 21.9 | 1.1 | 8.6 | 0.47 | 0.55 | 0.09 |
| reference B interiors (t0-13.5, t18-26.5) | 36.3 | 37.7 | 2.3 | 0.1 | 0.0 | 13.9 | 4.5 | 5.1 | 0.38 | 0.45 | 0.15 |
| clip A exterior frames t09.0 t13.5 t16.0 t48.5 t53.0 t58.5 (from `v3/set3d_beach/API.md`) | 15.3 | 20.0 | 0.1 | 0.0 | 0.0 | 52.8 | 2.5 | 9.2 | 0.42 | 0.70 | 0.07 |
| **target band** (the interiors) | 30-41 | 22-38 | | | | 14-30 | 0-5 | 0-10 (aim 5-9) | 0.38-0.48 | 0.45-0.63 | 0.08-0.15 |

The band is a property of whole scenes with characters; single frames scatter around it, as single reference frames do. Exteriors sit near the clip A exterior row (blue about 53, dark about 7).

### 1.3 Tone (whole-frame statistics, median of 130 frames per clip)

| quantity | clip A | clip B | target used |
|---|---|---|---|
| S mean | 0.483 | 0.405 | 0.40-0.60 |
| V mean | 0.650 | 0.580 | 0.44-0.60 (interiors) |
| luma p5 / p50 / p95 | 0.141 / 0.442 / 0.759 | 0.142 / 0.375 / 0.784 | p50 0.22-0.45 interiors |
| contrast luma p95-p5 | 0.610 | 0.616 | 0.60-0.75 |
| colourfulness (Hasler-Suesstrunk) | 81.8 | 56.0 | 55-100 |
| share V > 0.95 | 0.035 | 0.045 | 0.02-0.09, heads, lit paper, lamps only |
| black point luma p1 | 0.104 | 0.095 | 0.08-0.12 |
| darkest 10 % mean colour | `#3d1c32` (H 319) | `#392433` (H 318) | hue 250-345, S >= 0.35 |
| 40-60 % band mean colour | `#90646a` | `#7d656d` | rose-mauve |
| brightest 10 % | `#d1c7c6` | `#dbc5b1` | warm near-white |

Split tone: plum-violet shadows, rose-mauve mids, warm cream highlights. Interiors are the darkest scenes (median mid-luma: A train car 0.15, B throne 0.25, B hall 0.28, A concourse 0.42). The biggest k-means cluster of every reference interior is a dark saturated colour, 20-31 % of the frame: `#161a42`, `#6b3723`, `#221c31`, `#976c4d`.

Brightness layout (mean luminance 0-255, 8 x 5 grid): top row 119 (A) / 108 (B), middle 120 / 125, bottom 93 / 79. The bottom is darkest and the middle band brightest, from content (dark floors, light pooled on the subject), not a vignette. Wall behind the heads: 95-170 (aim 120).

### 1.4 The light

| item | measured |
|---|---|
| key | one hard sun in clip A, from camera-left and above in most shots (sun disc at (150, 330) in a/t16.0; shadows run to the right in a/t53.0). Exception a/t34.5: sun behind the set. Clip B has painted two-tone shading, no hard shadows, only a soft contact ellipse under the feet (`#4e3225` on road `#cba66f`, 40 px wide, 20 px soft edge) |
| shadow edge (10-90 %) | 4, 6, 9, 12, 21 px (a/t34.5, a/t02.0, a/t53.0) |
| shadow colour | blue-violet: hue jumps from 16-28 (lit) to 244-259 (shade): `#d9734d` -> `#332d40`, `#ac825e` -> `#525065`, `#946645` -> `#252432` |
| shadow depth | noon and interior sun: linear luminance ratio 0.11-0.33 (V ratio 0.29-0.59). Late afternoon: value kept, only hue changes (`#9d5975` -> `#475895`, V ratio 0.95) |
| shade of painted B sets | always cooler and more violet: jar `#a2a2a4` -> `#757482` (luminance x0.49), tower `#e3d3b9` -> `#bcb2b1` |
| rim light | none. B characters carry a drawn highlight strip 2-4 px inside the outline on the key side |
| highlights | lamps clip to `#fffeec`; near-white pixels 3.5 % (A), 4.5 % (B) |
| glow | small emitters: halo reaches 12-24 px beyond the core (ceiling lamp core 32 px, 10 % at 56 px; small lamp 16 / 28 px; street lamp 8 / 20 px), colour `#d7a273` -> `#975937`. B glows are painted and larger: torch 8 px core, 10 % at 40 px; moon disc 36 px, halo to 84 px `#5a8af5`. Sun: core 68 px, 10 % at 260 px. Heads never glow |
| darkest areas | scene black luma p0.5 0.087 (A), 0.079 (B); share below luma 0.04: 0.12-0.15 % |
| characters | A: unlit, head fill V 0.98-1.00, S 0.02-0.04 in every light, soft inner falloff 7 % over 14 px at the rim; they cast hard shadows (`#252432` to `#444153`, V x0.34-0.50, edge 6-21 px). B: one uniform tint per shot (see 1.1), V >= 0.91 |
| vignette, grain, sharpening | 0-5 %, none, none |
| depth | Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. |

### 1.5 Looks by time and weather (measured)

| treatment | frames | look |
|---|---|---|
| day interior | a/t32.5, a/t34.5, b/t00.0, b/t09.0 | A: warm wood `#ac825e` with hard blue-violet shadows, cream paper `#e9d6bb`, blue sky through the roof `#8797d9`. B: mauve stone `#7e5f65`, navy floor `#3a3858`, red drapes `#9d3e3f`, gold `#f3d26d` |
| lamp-lit interior | a/t27.5, b/t23.0 | walls `#561e37`, seat `#84052e`, ceiling `#c03c12`, carpet `#12183c`; S mean 0.73, mid-luma 0.15; lamps clip to `#fffeec` with warm halo |
| exterior sun (noon) | a/t02.0, a/t16.0, a/t45.0 | sky `#386ec9`-`#4a78cd` to horizon `#92b7e7`; sunlit rock `#e9671d`, ground `#d9734d`; shadows `#332d40`-`#781518`; complementary orange ground against blue sky |
| late afternoon | a/t49.0, a/t53.0 | deck rose-mauve `#9d5975`, shadow `#475895` at equal value, far mesa `#643c5f` |
| sunset | a/t61.0, b/t31.0 | A sky `#bdb0b8` -> `#eee4cf` -> `#f2d8ab`; B `#e16c7e` -> `#ff9f8c` -> `#ffdc99`, silhouette `#1e081f`, cloud tops `#fcd5b1` over `#ca6a9c` |
| night | b/t34.0, b/t41.5, b/t44.0 | not dark: V mean 0.59, mid-luma 0.32, S 0.54, 86 % of the frame blue-violet; sky `#1748ae`-`#1e2e7b`, walls `#576295`, road `#3d346d`; moon `#eff8ff` with blue halo; warm torch and window accents; heads tinted lilac `#fbdaf7` |
| haze | a/t09.0, a/t58.5, b/t46.5 | mid distance mixes 30-50 % toward the horizon colour, farthest layer 90-100 %; S falls, V rises with distance |
| brightness dip | b/t03.3-t03.7 | whole frame dims for about 0.4 s on a dramatic line (V p95 0.97 -> 0.75), optional |
| grey weather, storm | none | **the reference has no grey-weather, rain or storm scene.** Everything in this chapter about grey and storm light is our own extrapolation |

---

## 2. Our build (film 1)

### 2.1 The light model (all three sets)

`v3/set3d/office3d.py` `mat_lit`, reused by the kitchen; the beach has its own `mat_lit` with the same terms plus haze:

    pixel = artwork x gain x KEY x visibility / max(cos to key, 0.12)      (toon key: every face that sees the sun gets the full key)
          + (artwork x SHADE x shade_mul + LIFT) x F                       (ambient, as emission: noise-free)
    F = (1 + dot(face normal, form)) x (1 + falloff_y x y / 9)              (office; the kitchen uses falloff_y 1.3 / 1.2)

- SHADE is the flat ambient, LIFT a flat dark lift, KEY = one Sun with `color = KEY / max(KEY)`, `energy = pi x max(KEY)`, `angle = sun_angle` (office3d.py line ~511).
- World black, strength 0. Render: Cycles CPU, `max_bounces` 1, `diffuse_bounces` 0, no denoiser, adaptive off, 16 samples final (12 "fast", 8 at 360x640 "preview"), Standard view, look None (`office3d.setup_render`).
- Compositor grade in the render (`office3d.setup_grade` -> `spec/grade_compositor.py`): Glare Bloom threshold 1.0, strength 0.5, size per preset (0.05); ASC-CDL offset per preset (spec default `(0.0075, 0.0035, 0.0095)`, plum), slope `(1.000, 0.985, 0.970)`, power 1; saturation per preset (spec default 1.12); vignette 0.
- Only bulbs (`#fffeec`, strength 6-12), the banker-lamp slit (`#fff1c4`, 0.6 x bulb), lightning and the drop (`#cfe0ff`, 1.4) go above 1.0.

### 2.2 Light presets

Values from the code (the code wins where an API.md differs; see 6.3). Frames: `colour_light_presets.jpg`.

**Office** (`v3/set3d/office3d.py` `PRESETS`, `v3/set3d_ext/light/office_light.py` `PRESETS`; apply with `OL.apply(name)` after `S.build('INTERIOR_DAY')`)

| | office_day = `INTERIOR_DAY` | office_grey | office_storm | `INTERIOR_LAMP` (built, not used in film 1) |
|---|---|---|---|---|
| used in | shots 1-7, 9-14 | 17-22 (19-22 map-as-terrain) | 25 | - |
| SHADE (ambient) | (0.20, 0.27, 0.54) | (0.20, 0.23, 0.41) | (0.068, 0.082, 0.165) | (0.40, 0.33, 0.52) |
| LIFT | (0.0, 0.010, 0.026) | (0.002, 0.005, 0.014) | (0.003, 0.003, 0.007) | (0.012, 0.008, 0.022) |
| KEY | (2.30, 1.65, 0.74) = energy pi x 2.30, colour (1, 0.717, 0.322) | (0.66, 0.58, 0.50) | (0.12, 0.13, 0.19) | none |
| key_dir (travel) | (-1.0, 1.3, -0.30): through the window on the right wall, from camera-left in the room frame | same | same | same |
| sun angle | 0.45 deg (hard; spec said 1.5, glazing bars 5-8 D away printed 32 px at 0.7) | 3 deg | 3 deg | 0.7 |
| room shell shadows the key | yes: window patch and bar shadows | no: flat wash, no sun patch | no, except on lightning frames | - |
| per-surface ambient tint (`shade_mul`, see 2.3; grey/storm add `surf` on top) | wallpaper (2.8, 2.05, 0.7), frieze 0.8 x that, wainscot/rail/stile (0.62, 0.95, 1.1), planks (1.06, 1.32, 1.38), ceiling (3.8, 3.0, 1.8), beams (3.4, 2.6, 1.4), map 0.56 | x map (1.60, 1.48, 1.18), wallpaper (0.92, 1.0, 1.08), frieze (1.10, 0.95, 0.80), wainscot and warm flats (1.30, 1.50, 0.60), planks (1.45, 1.12, 0.72), rug (1.10, 1.0, 0.88), ceiling (1.15, 1.45, 0.55), beams (1.20, 1.45, 0.55), paper/calendar (1.35, 1.30, 1.10), sign (1.2, 1.15, 1.05), red ink `flat_c8301c` (2.0, 0.35, 0.3) | x the same woods and paper, with wallpaper (1.12, 0.92, 0.62), frieze (1.15, 1.10, 0.55), planks (1.40, 1.25, 0.65), beams (1.15, 1.55, 0.50), warm flats (1.25, 1.60, 0.55), rug (1.15, 1.0, 0.85), red ink (2.8, 0.35, 0.3) | wall_shade 1.0 |
| key gains | wallpaper 0.85, wood 0.7, floor 1.0, rug 1.0, map 0.30, paper 0.27 | x kgain wallpaper 0.60, frieze 0.70, red ink 1.8 | x kgain wallpaper 0.70, frieze 0.75, red ink 4.5 | - |
| form / falloff_y | (0.14, -0.04, 0.26) / 0.30 | same | same | (0.10, -0.03, 0.2) / 0 |
| window sky card | day sky texture, strength 1.0 (`#5f79b4` -> `#93a9cf` -> `#cfd6e2`, clouds `#eef1f6` at 0.55, buildings `#6d7fa8`-`#8fa0c4`) | `sky_grey.png` 1.0 | `sky_storm.png` 1.0, x(1 + 2.2 flash) | 0.12 |
| bulbs (pendants `#fffeec`) | 6 | 8 | 12 | 9 |
| rain card (drizzle, lash) | hidden | (1.0, 0.0), gain 0.9 | (0.35, 1.0), gain 0.55 | - |
| lightning | - | - | Sun `olt_flash` colour (0.82, 0.88, 1.0), 1.2 deg, energy flash x 3.2 x day key; sky x2.2, rain x1.5 | - |
| grade offset / slope / power / sat | (0.002, 0.0045, 0.010) / (1, 0.985, 0.97) / 1 / 1.06 | (0.003, 0.004, 0.008) / (1.005, 1.005, 1.02) / (1.02, 1.01, 1.0) / 0.96 | (0.003, 0.003, 0.006) / (1.0, 0.99, 0.99) / (1.02, 1.01, 1.0) / 1.0 | spec defaults |
| bloom size, strength | 0.05, 0.5 | 0.08, 0.65 | 0.08, 0.7 | 0.05, 0.5 |
| actor card tint | 1 | 1 | (0.86, 0.86, 0.95) | - |

**Beach** (`v3/set3d_beach/beach3d.py` `PRESETS`; plan names via `v3/set3d_ext/beach/beach_ext.py` `LIGHTS`: `beach_sunny`, `grey_drizzle`, `storm_approach`, `storm`)

| | SUMMER_SUN (beach_sunny) | GREY_DRIZZLE (grey_drizzle) | STORM_APPROACH (storm_approach) | STORM (storm) |
|---|---|---|---|---|
| used in | shot 8 | 16 | 23 | 24 |
| A (ambient) / A_pale (albedo S < 0.25) | (0.10, 0.25, 0.98) / (0.21, 0.25, 0.51) | (0.54, 0.555, 0.68) / (0.52, 0.54, 0.67) | drizzle x0.75: (0.405, 0.416, 0.51) / (0.39, 0.405, 0.5025) | (0.06, 0.09, 0.24) / (0.09, 0.115, 0.26) |
| shade_tint, shade_mix | (0.22, 0.20, 0.38), 0.5 | (0.50, 0.52, 0.70), 0.35 | (0.36, 0.36, 0.56), 0.35 | (0.08, 0.10, 0.25), 0.5 |
| K (key) | (0.92, 0.80, 0.24) | (0.16, 0.16, 0.17) | (0.12, 0.12, 0.1275) | (1.75, 1.08, 0.48) |
| key_dir, elevation (computed from key_dir), angle | (0.55, -0.45, -0.70), 44.6 deg, 1.0 deg, toon | (0.25, -0.35, -0.90), 64.5 deg, 14 deg (soft), toon | as drizzle | (-0.80, 0.48, -0.22), 13.3 deg, 0.8 deg, Lambert (grazing warm break from the land side) |
| lift | (0.008, 0.010, 0.026) | (0.010, 0.013, 0.030) | as drizzle | (0.006, 0.010, 0.028) |
| object sat, grade sat | 1.0, 1.04 | 0.92, 1.16 | 0.95, 1.22 | 0.92, 1.08 |
| sky stops (horizon t=0 -> zenith t=1) | `#a9c6ec` 0, `#8ab1ea` 0.12, `#6898e0` 0.45, `#4a78cd` 1; clouds `#b7c2ea`/`#f4f3fb` cover 0.5 | `#c0c6da`, `#aab3cc` 0.15, `#8c96b6` 0.55, `#6f7ba0`; clouds `#8c91ad`/`#c2c4d4` cover 0.75 | `#8d8496` 0, `#a39a8a` 0.05, `#c2b27c` 0.11 (the sick yellow band), `#b3a07e` 0.17, `#8e7f98` 0.24, `#6a5f8e` 0.45, `#3a3466` 1; clouds `#4d4672`/`#7d7398` | `#6672aa`, `#43508c` 0.12, `#27326a` 0.45, `#0f1534`; clouds `#1f2a52`/`#55628f`; glow `#e8a070` at 0.35 toward the key |
| haze colour, max, distance (D) | `#a6c2ec`, 0.62, 25-420 | `#b8bccf`, 0.80, 14-220 | `#8f889f`, 0.75, 16-240 | `#4e5a8e`, 0.55, 18-300 |
| sand light / mid / dark, wet; far tint | `#d47844` `#de8e50` `#e8a462`, `#b6765c`; `#dc7c64` -> `#e6a28a` | `#b8875a` `#c29264` `#cba070`, `#8e6e58`; `#a98878` -> `#b5a39a` | drizzle x0.8 (`#936c48` `#9b7550` `#a2805a`, wet `#725846`); `#7d6f78` -> `#857c8a` | `#9c6a52` `#a6745a` `#b08062`, `#6e5458`; `#7c6478` -> `#5c6290` |
| sea near / far / horizon band, streak, foam | `#3559b0` / `#6f9fe6` / `#b9d3ee`, `#dfe8fb` 0.28, `#f4f1fb` | `#4c5c80` / `#7d87a8` / `#c3c5d6`, `#b9bfd3` 0.30, `#d9dbe6` | `#2e3658` / `#4c5076` / `#a69fae`, `#8d90aa` 0.04, `#b9bccb` | `#102766` / `#2a4890` / `#7684b8`, `#dfe6fa` 0.75, `#e6e8f8` |
| fog top / foot, alpha | `#d2ccd2` / `#b9b6c6`, 0.95 | `#dcdee6` / `#b6bacb`, 0.97 | `#d4cac6` / `#b2a8ad`, 0.98 | `#8890b4` / `#5d6690`, 0.97 |
| headland near / far | `#8d78b0`, `#7393d0` | `#9a93b0`, `#a3a9c4` | `#6e6688`, `#787294` | `#454c84`, `#525ea0` |
| set ink | `#2a1712` | `#2a1d2c` | `#251a30` | `#1d1449` |
| wave ramp (z 0 -> crest), lite, emit / gain | `#15285e` `#1f4f98` `#2f72b8` `#4d97cc` `#8cc2e2` `#d6ecf6` `#f4f8fe`, `#7fb4e0`, 0.62 / 0.30 | `#1f2e55` `#334f86` `#4a6e9e` `#6b8fb6` `#9db8d0` `#e2e8f0`, `#8fa9c8`, 0.70 / 1.2 | as drizzle | `#08122e` `#0f2f5e` `#17507f` `#236f9c` `#4d9cc0` `#b7dcea` `#eef6fb`, `#3f86b0`, 0.78 / 0.16, foam emit 1.0 |
| rain colour | `#cfd6ec` (default) | `#cfd6ec` | `#b9bed6` | `#cfd6ec` |
| states (`STATES`) | fog 0, rain 0, wind 0.15 | fog 0.25, rain 0.3, wind 0.3 (takes use rain 0.35) | fog 0.06-0.9, rain 0, wind 0.04-0.6 | fog 1, wave 1, rain 1, wind 1 |

Terrain, sea, sky, clouds, fog, grass, wave and rain carry no ink; man-made objects carry the hull ink at 0.00384 x distance (distance from the reference point, at least 4 D; width clamped to 0.014-0.07 D: `beach3d.py` ink-width helper).

**Kitchen** (`v3/set3d_kitchen/kitchen3d.py` `PRESETS`; `K.build('kitchen_grey' | 'kitchen_storm')`). `kitchen3d.py` reads `v3/paper/tex/registry.json` at import: build the paper artwork first (`python3 v3/paper/paper.py build`, done by `examples/setup_kit.sh`); without it the import stops with a message saying so.

| | kitchen_grey | kitchen_storm |
|---|---|---|
| used in | shot 15 | shot 26 |
| SHADE | (0.25, 0.27, 0.52) | (0.050, 0.072, 0.20) |
| KEY | (0.56, 0.53, 0.54), 2.0 deg | (0.28, 0.20, 0.125), 4.0 deg (a weak warm lamp-like key) |
| key_dir | (0.42, 0.62, -0.66): front-left, high, from the unseen room side | same |
| LIFT | (0.002, 0.003, 0.014) | (0.001, 0.002, 0.008) |
| form / falloff_y | (0.10, -0.05, 0.22) / 1.3 | (0.10, -0.05, 0.22) / 1.2 |
| wall_shade / wood_shade / cloth_shade | (1.9, 1.5, 0.9) / (0.9, 0.95, 1.1) / (1.4, 1.2, 0.7) default | (2.6, 1.5, 0.55) / (1.8, 1.15, 0.55) / (2.2, 1.3, 0.55) |
| window card | drizzle loop, 1.0 | wave sequence, 0.85 (x1.6 in lightning) |
| lightning | none | second Sun `flash_sun` colour (0.86, 0.88, 1.0), 1.5 deg, `flash_dir` (-0.15, -0.75, -0.62), energy pi x 3.2 x strength. Keys: g1873-1876 1.0, 0.75, 0.45, 0.2; g1889-1894 0.35, 1.0, 0.8, 0.25, 0.6, 0.15; g1935-1936 0.7, 0.3 |
| grade offset / sat, bloom size | (0.002, 0.003, 0.004) / 1.22, 0.05 | (0.0, 0.002, 0.007) / 1.15, 0.05 |

**Spec presets** (`spec/lightkit_clp.py` `PRESETS`, fitted to the reference; not used directly in film 1, but the only night values we have):

| preset | ambient A | key K | sun energy, colour | elevation | angle | modelled on |
|---|---|---|---|---|---|---|
| `INTERIOR_DAY` | (0.42, 0.40, 0.56) | (0.70, 0.54, 0.15) | 2.20, (1.00, 0.77, 0.21) | 38 | 1.5 | a/t32.5, a/t34.5 |
| `INTERIOR_LAMP` | (0.20, 0.16, 0.30) | lamps (1.00, 0.69, 0.31) x 0.9 | no sun | - | lamp radius 0.05 m | a/t27.5, b/t22.0 |
| `EXTERIOR_NOON` | (0.10, 0.21, 0.79) | (0.90, 0.79, 0.21) | 2.83, (1.00, 0.88, 0.23) | 50 | 1.5 | a/t02.0 |
| `LATE_AFTERNOON` | (0.20, 0.45, 0.95) | (0.85, 0.50, 0.10) | 2.67, (1.00, 0.59, 0.12) | 20 | 1.5 | a/t49.0, a/t53.0 |
| `SUNSET` | (0.35, 0.25, 0.45) | (0.80, 0.44, 0.20) | 2.51, (1.00, 0.55, 0.25) | 8 | 2.5 | a/t61.0, b/t31.0 |
| `NIGHT` | (0.12, 0.13, 0.45) | (0.33, 0.35, 0.75) | 2.36, (0.44, 0.47, 1.00) | 45 | 1.5 | b/t34.0, b/t41.5, b/t44.0 |

### 2.3 Material colours, every set

Columns: albedo hex, key gain, ambient multiplier (`shade_mul`), file. Flat colours are made by the local helper `C(hex, gain, shade_mul)` inside `build()`; textures by `TX(name, ...)`.

**Office** (`v3/set3d/office3d.py` `build()`, artwork `v3/set3d/textures.py`, palette `v2/sets/office.py`; `textures.COLOUR` re-binds the v2 names at import)

| object | hex | gain, shade_mul | defined in |
|---|---|---|---|
| wallpaper base `WALL3` / motif `WALL_HI` / darker stripes x0.82 | `#aa3e2c` / `#d59a58` | 0.85, (2.8, 2.05, 0.7) | textures.py `wallpaper()`; office.py `WALL_HI` |
| frieze `FRIEZE` | `#6a2a1e` | 0.85, 0.8 x wall_shade | textures.py `COLOUR` |
| wainscot `WOOD` / panel `PANEL` | `#5e3018` / `#7c4620` | 0.7, (0.62, 0.95, 1.1) | textures.py `COLOUR` |
| chair rail `RAILC`, stiles (`WOOD`) | `#96502c` | 0.7, (0.62, 0.95, 1.1) | office.py |
| baseboard `BASEC` | `#3b1a12` | 1, 1 | office.py |
| picture rail `PRAIL` | `#c9a878` | 0.5 | office.py |
| crown moulding | `#6b3a26` | 1 | office3d.py |
| floor planks `FLOOR` / seams `SEAM` | `#a6764e` / `#2e1d22` | 1.0, (1.06, 1.32, 1.38), no form term | textures.py `COLOUR` |
| rug navy `NAVY` / red `RUGRED` / gold `GOLD` / dots | `#283a74` / `#84222a` / `#cb9f48` / `#d9c9a8` | 1.0 | textures.py, office.py |
| ceiling boards | `#8c5030` | 1, (3.8, 3.0, 1.8) | textures.py `ceiling()` |
| beams body / chamfer / straps / bolts | `#4a2616` / `#5c3220` / `#22222e` / `#6f7488` | 1, (3.4, 2.6, 1.4) | office3d.py, textures.py `beam()` |
| map frame, dark frames, sign frame | `#3d1c12` | 1, 1.25 | office3d.py |
| clock, pinboard, certificate, left board | `#4a2216` | 1, 1.2 | office3d.py |
| map gilt edge `GOLD` | `#cb9f48` | 0.5 | office.py |
| wall map paper (texture) | land `LAND` `#c49b58`, sea `SEA` `#6b9aad` / `SEA_D` `#4d7f93`, print `PRINT` `#836d4e`, `PRINT_D` `#574430`, vignette `#5a2a22` at 0.42 | 0.30, 0.56, no form | office.py |
| red track `RED` / smudge / ghost | `#c8301c` / `#f0a694` (0.4, opacity 0.26) / `#e58d7c` (0.4, opacity 0.3) | 0.55 | office3d.py `_build_track` |
| map ledge wood / lip / brackets | `#7b3b26` / `#a85a38` / `#5c2c1c` | 1 | office3d.py |
| ledge props: eraser, felt, pink rubber, red pencil, blue pencil | `#3a3e4c`, `#b08a52`, `#e58d86` (0.6), `#c8301c` (0.6), `#2f5a8a` | as listed | office3d.py |
| sign board / lettering (U.S. WEATHER BUREAU) | `#1c403d` / `#e9d9b0` | texture | textures.py |
| window frame and bars / sill wood / reveal | `#6f3522` (1, 1.15) / `#7b3b26` / `#b88a68` (0.8) | | office3d.py |
| paper (calendar, papers) | `#f6efe2` | 0.27 | office3d.py |
| brass `BRASS` | `#e2a630` | 0.5 | office.py |
| lamp shades green | `#2d7a52` | 1, 1.2 | office3d.py |
| filing cabinets `STEEL` / `STEEL_HI` / top x1.3 | `#34508c` / `#42609e` | 1 | textures.py `COLOUR` |
| radiators / feet | `#5d6478` / `#3c4458` | 1 | office3d.py |
| teletype body `dark` / iron | `#20263c` / `#2f3444` | 1, 1.2 | office3d.py |
| telephone / ink bottle cap | `#1c1e2c` (1, 1.3) / `#1c1a22` (1, 1.4) | | office3d.py |
| desk sides / top frame / chair | `#5b2e1c` / `#a56a3c` (top texture, 1, 1.5) / `#55291a` | 1 | office3d.py |
| thermometer body / bead | `#f3e7c9` (0.27) / `#c2311e` (0.6) | | office3d.py |
| bin / rolled maps | `#8a6a3e` / `#f1e3c0` (0.27) | | office3d.py |
| bulbs (emission) / banker slit | `#fffeec` x bulb / `#fff1c4` x 0.6 bulb | | office.py `BULB` |
| set ink (hull) | `#2a1712` | emission, camera rays | office.py `INK` |

**Office extensions** (`v3/set3d_ext/props/office_props.py`, `v3/set3d_ext/mech/office_mech.py`)

| object | hex | gain, shade_mul | defined in |
|---|---|---|---|
| chalk curve and arrow head | `#f4f2ec` | 0.42, 1.25 | office_props.py `_build_chalk` |
| six ghost tracks | `#c7d2e6` | 0.38, 1.3, alpha 0.35 rest / 0.75 peak | office_props.py `_build_ghosts` |
| pin heads / pin steel | `#c8301c` (0.6) / `#9aa0ae` (0.5) | | office_props.py |
| ruler wood | `#b9824c` | 0.6 | office_props.py |
| eraser crumbs | `#e58d86` | 0.6 | office_props.py |
| rubber stamp wood / knob | `#7b3b26` (0.7) / `#3d1c12` (0.8) | | office_props.py |
| map-as-terrain walls E (Atlantic) / W (land) | `#c4c6d4` / `#cac6d2` | 0.35 (mech `_lit` default) | office_mech.py `WALL_COL` |
| Latin H | `#2c3f74` | texture | office_mech.py `H_COL` |
| lane / dashes / dashes when red | `#efe7d2` (0.33, 1.15) / `#fbfaf4` / `#d0281c` | | office_mech.py `_build_lane` |
| compass glow / wake / wake glow | `#ff5a3c` / `#ff7a3a` (0.35) / `#ff4a1c` | | office_mech.py |
| pictogram post / sign post | `#6b5a48` (0.4) / `#8a8f9a` (0.45) | | office_mech.py |

**Paper and text** (`v3/paper/paper.py`): paper `#fff5df`; printed ink `#836d4e`; dark ink `#574430`; print red / stamp `#b61d32`; label brush red `#a32413`; track red underline `#c8301c`; navy `#081148`; cream lettering on colour `#f3d9a8`; greeked filler `#9a8f86`. Paper on set surfaces is capped by key gain 0.25-0.30 so lit paper reaches cream, not white.

**Kitchen** (`v3/set3d_kitchen/kitchen3d.py` `build()`, artwork `kitchen_tex.py`; gain 0.85-0.9 unless noted)

| object | hex | shade_mul | defined in |
|---|---|---|---|
| wall paper base / stripes / lines / flower red / flower centre / leaves | `#c4853c` / `#e6b468` / `#8a4a1c` / `#c8352a` / `#f2c86a` / `#4f5d2a` | wall_shade | kitchen_tex.py `kwall` |
| wainscot | office `wainscot.png` | wood_shade | |
| oilcloth base / stripes / checks / lines | `#efd7a8` / `#dc6c26`, `#c9402a` at 0.74 / `#7c2410` at 0.88 / `#7a1a12` | gain 0.72, cloth_shade | kitchen_tex.py `oilcloth` |
| curtain gingham | `#efe3c9` with `#2f56a8` at 0.65 | (1.2, 1.1, 1.0) | kitchen_tex.py `curtain` |
| wood / frame / dark / bread box top / base / chair | `#7b3b26` / `#8a4a2a` / `#3d1c12` (1.25) / `#a85e34` / `#6e3520` / `#9a5432` | wood_shade | kitchen3d.py |
| cup cream / rim navy | `#f1e4cb` (1.25, 1.15, 1.0) / `#2e4686` (1.2) | | kitchen3d.py |
| coffee pot red / rim | `#b8322a` (1.4, 1.1, 1.0) / `#f1e4cb` | | kitchen3d.py |
| plate rim, paper back, steel, brass | `#e9dcc0`, `#efe2c8` (0.8), `#9aa0ae`, `#c89a3c` (0.8) | | kitchen3d.py |
| coffee (unlit) dark / ring | `#22130a` / `#8a5c3a` | | kitchen3d.py `_coffee_mat` |
| toast | `#9a4a1c` crust, `#e8a454`, `#c97a30`, `#f6dc8a` | | kitchen_tex.py `toast` |
| drizzle view: sky / sea / headland / ground / rain | `#8f97a8` -> `#b9bcc4` / `#6c7b8f` -> `#55667c` / `#5d6574` / `#8c7a63` / `#e6e9ef` at 0.45 | | kitchen_tex.py |
| storm view (mixed by lightning L) | sky `#1c2033` -> `#e9e6ff`; water `#13222e` -> `#5a7d92` | | kitchen_tex.py |
| falling drop | `#cfe0ff` emission 1.4 | | kitchen3d.py |

**Beach** (`v3/set3d_beach/beach3d.py`, `beach_tex.py`; terrain colours per preset in 2.2)

| object | hex | defined in |
|---|---|---|
| cottage schemes body / trim / roof / door / shutter | cream `#ebddc8`/`#f6efe2`/`#5b211d`/`#6b2a22`/`#2f6a5a`; red `#b84735`/`#f3e6cf`/`#4d3e3f`/`#3b2a35`/`#f3e6cf`; blue `#7f8fbf`/`#f6efe2`/`#5b211d`/`#5b211d`/`#b84735`; cedar `#a7745a`/`#efe2c8`/`#4d3e3f`/`#2f6a5a`/`#2f6a5a`; yellow `#e3c27a`/`#f6efe2`/`#5b211d`/`#2f5a8a`/`#2f5a8a` | beach_tex.py `SCHEMES` |
| roof shingles maroon / slate | `#5b211d` / `#4d3e3f` | beach_tex.py |
| soffit / ridge / stilts and poles / deck | `#4a2a2a` (0.8) / `#3b1a18` / `#6d3a1f` / `#a8774f` | beach3d.py |
| iron / pole arm / insulators / wire | `#3b3442` / `#7a4a2a` / `#b9d7e4` / `#2a1d26` | beach3d.py |
| boardwalk stringer / fence post / rope | `#5a3526` / `#8a5a35` / `#d9c9a8` | beach3d.py |
| grass | `#67832c`, `#8aa23a`, `#4f6b2a` | beach3d.py |
| umbrella red / cream / pole | `#c2311e` / `#f6efe2` / `#e9dcc0` | beach3d.py |
| boat hull / gunwale / inside / thwart | `#c2311e` / `#f6efe2` / `#9a6a42` / `#7a4a2a` | beach3d.py |
| lifeguard chair / flagpole / flag | `#efe6d4` / `#d8ccb4` / `#c2311e` | beach3d.py |
| sign board / post | `#f6efe2` / `#6d3a1f` | beach3d.py |
| deck chair frame / green / cream | `#8a5a35` / `#2f6a5a` / `#efe2c8` | beach3d.py |
| towel stripes, bucket, spade | `#2f5a8a` + `#f6efe2`, `#2f5a8a`, `#c2311e` | beach3d.py |
| basket / lid / crate / slats / footprints | `#b08a52` / `#c29a5e` / `#a8774f` / `#8a5a3c` / `#b77c4e` | beach3d.py |

### 2.4 Character colours

All cast: head fill `HEAD_FILL` `#fef7f6`, lavender rim crescent `HEAD_SHADE` `#e9dceb`, ink `INK` `#3a2832` (outline, limbs, features), mouth cavity `#4d2433`, tongue `#7b626c`, teeth `#fef9f8` (`v2/puppet/puppet.py` lines 43-46). Options: `tint` multiplies every fill (night `#fbdaf7`, warm interior `#faded0`); `ink` override (night `#1e142e`). Contact shadow `#252432` at 0.6. Cards are emission to camera rays only (`office3d.mat_card`), so drawn colours reach the grade unchanged; office_storm multiplies the card by (0.86, 0.86, 0.95).

| member | file | costume and hat colours |
|---|---|---|
| `hero` | puppet.py `CAST` | vest base `#3b6fda`, dark `#234a9c`, rib `#2f5cc0`, argyle `#8fb2f6`, stitch `#f6ead0`; shirt `#f4ede7`; tie `#e3a93a` / `#b47a22`; pants `#4c4453`; pencil `#d5392f`; newsboy cap light `#f1cf7c`, base `#dca63e`, dark `#b27a26`, visor `#c8932f`, band `#5a3a22`, check `#f7e3a6`, seam `#8a5a22`; hair `#a8492a` |
| `boss` | puppet.py `CAST` | waistcoat base `#2f8b58`, dark `#1e5f3b`, lapel `#1f6641`, pinstripe `#8fd3a8`; shirt `#f1eae5`; bow tie `#c9352e` / `#98241f`; buttons `#e0c063` / `#f1e2a4`; pants `#3d3846`; feather `#e2703a` / `#a84420`; homburg light `#9c96aa`, base `#6b6476`, dark `#474151`, shine `#dedaea`, band `#2c2732`, bow `#474150`, brim `#5d5667`, edge `#b3adbf`; hair `#988c98` |
| `senior_a` | `v3/cast/cast_ext.py` `NEW_CAST` | tweed base `#7b4f33`, dark `#4b2f1f`, fleck `#b98d62`, pocket `#6a432b`; shirt `#d7e3f1`, collar `#eef3f8`; tie `#2f4f8a` / `#1f3563`, stripe `#e2b44a`; buttons `#e0bd84` / `#f4e2bd`; pen `#9e2b25`, clip `#e8c86a`; pants `#575264`; fedora light `#dcb27a`, base `#b8854c`, dark `#7c5530`, shine `#f1dcb2`, band `#3b2a22` / `#5a4030`, brim `#a77543`, edge `#dcb985`; hair `#bdb5b8` |
| `senior_b` | cast_ext.py | cardigan base `#a8383f`, dark `#5c1820`, rib `#7c2630`, band `#76222b`, pocket `#862a32`; shirt `#f0ebe6`; tie `#283a62` / `#18233f`; buttons `#7a4a2a` / `#b07a50`; pipe `#6b3d26`, stem `#3a2a2a`; pants `#3d3a46`; moustache `#efebef`; bowler light `#d6d1d6`, base `#aca6ad`, dark `#6f6973`, shine `#f6f3f7`, band `#2f2a33`, brim `#958f97`, edge `#dcd7dd`; hair `#d4ccd6` |
| `clerk` | cast_ext.py | shirt base `#e6ebf1`, dark `#8a96a8`, stripe `#7a9bd0`, collar `#fbfcfd`; tie `#d65a2c` / `#9e3c1a`, clip `#e3c46a`; pocket `#d6dee8`; pencils `#efc13a`, `#cf3b2c`; buttons `#fbfbfb`; belt `#5b3a26`, buckle `#e3c46a`; pants `#5e5868`; garters `#c0332a`; eyeshade band `#2f2a36`, visor `#2f8a58` / `#9fe0b8`; hair `#4b2c20`, shine `#7d5040` |
| `beach_man` | cast_ext.py | suit base `#354b8e`, hoops `#f1e8d4`; badge `#c7362c`; belt `#f4ecdb`, buckle `#d9b95c`; trunks `#1f2c57`; boater light `#f7e8b4`, base `#ead17e`, dark `#b8954a`, brim `#ecd58a`, weave `#b8984e`, band `#c7362c`, stripe `#22336a`; hair `#5a3826` |
| `beach_woman` | cast_ext.py | dress base `#d84a3a`, dark `#9c2c22`, dots `#fbf2e6`; collar and buttons `#fcf7ef`; sash `#2c4a8a` / `#1d3263`; trim `#fbf2e6`; sun hat light `#fffaee`, base `#f2e6c8`, dark `#c9b48a`, shine `#ffffff`, band `#2c4a8a` / `#1d3263`; hair `#7a4630` |
| `beach_kid` | cast_ext.py | blouse base `#f3f0e8`; navy `#24366b` / `#3e528c`; kerchief `#d23b2e` / `#9c2a20`; star `#e8c04a`; shorts `#24366b`; sailor cap light `#ffffff`, base `#f3f1ea`, dark `#c8c4ba`, band `#24366b`, gold `#e3c04f`; hair `#e0ad4a` |

On screen (measured, `v3/set3d_ext/light/API.md`, COLOUR.md): head fill `#fff6f4` (day, V 1.00, S 0.043), `#fff9fa` (grey), `#eee6f0` (storm, tinted); ink `#3b2b39` hero, `#2d2b39`-`#302b39` boss. After the v1.1 grade: head fill V 0.976-0.984, S 0.036; sampled face (251, 239, 244) = `#fbeff4`.

### 2.5 Captions

`__PROJ__/v3/film/out_v11/film_silent.ass` (104 events; byte-identical to `__PROJ__/v3/film/out/film_silent.ass`, the file burned into `film_v1_1_sharp_thai.mp4`): style `Pop`, Work Sans Black 50, primary `&H00FFFFFF` (white `#ffffff`), outline `&H00000000` (black) 4 px, back `&H80000000` (black at 50 %), shadow 1.5, alignment 5, every event `{\pos(360,900)}{\fnKanit Black\fs88}` + Thai text (fonts `fonts/Kanit_900Black.ttf`, `fonts/WorkSans-Black.ttf`). Reference: white fill, black 4 px stroke, soft dark halo 2-3 px, centre y 900. Burn the captions after the grade, so white and black stay pure.

---

## 3. The v1.1 grade (`v3/film/out_v11/grade.py`)

Entry `grade_frame(img, g) -> img` (PIL RGB 720x1280, g = film frame). Stateless; numpy, cv2, PIL only. Runner: `python3 grade.py SRC DST first last step` (resumable; film 1 ran 3 processes with step 3, about 5-7 min for 1965 frames; 0.21-0.44 s per frame alone). **Tested:** graded g291, g1045 and g1840 from the sharp conform frames `__PROJ__/v3/film/out/frames/` and compared with the delivered sharp v1.1 `graded/` frames: max difference 0, 0.38-0.46 s per frame.

The film clock (`TAKES`, `JOINS`) is film 1's. For a new film replace `TAKES` (take name, first film frame), `JOINS` (incoming take, `"d"` dissolve or `"l"` linear, first, last), `SHOT` and the s23 fog constants (`FOG_G0`, `FOG_G1`, rows 400-680), or the per-shot settings land on the wrong frames.

| # | stage | parameters |
|---|---|---|
| 1 | per-shot correction, cross-faded over every dissolve with the conform weight smoothstep((g-a+1)/(L+1)), linear over wipes and flashes | `DEFAULT` gain 1, lift 0, gamma 1, con 1 (contrast around luma 0.42), sat 1, white balance wr/wg/wb 1 (near-white fills V > 0.86-0.97 with S < 0.04-0.14 excluded), walls 0 (warm key on pale walls: hue 185-300, S < 0.22-0.42, V > 0.35-0.75, lamp colour (1, lamp_g 0.85, lamp_b 0.77) normalised to luma), lowdark 0 (darker lower frame from y 0.55 H), bloom 1, haze 0 at haze_y 0.42, red 0.8, wprot 1, wsat 0.30 |
| 2 | tone curve on luma, hue preserving (pixel scaled by Y'/Y, over-range pixels scaled down) | knots (0, 0) (0.06, 0.052) (0.15, 0.118) (0.35, 0.400) (0.65, 0.785) (0.85, 0.938) (1, 0.985), monotone cubic |
| 3 | saturation around luma, vibrance style | `SAT_GLOBAL` 1.18; boost x (1 - 0.65 S); near-white fills (max 0.78-0.92, S < 0.06-0.16) get none |
| 4 | haze (exteriors) | warm airlight (1, 0.90, 0.76) x clip(0.5 Y + 0.55, 0, 0.98) onto "far" pixels (close to their row's median colour, sigma 0.085, quarter size); vertical profile sigma 0.16 H above, 0.07 H below haze_y |
| 5 | bloom, quarter size, screen blend, tint (1, 0.94, 0.84), no frame-adaptive normalisation | **hot**: input max channel 0.955-0.985 (`HOT_T0`, `HOT_T1`), only pale sources (weight x (1 - smoothstep(S 0.20-0.35))); blobs of max > 0.80; a blob whose 4 px rim is 12-28 % ink (luma < 0.30) keeps 15 % (`BLOOM_FACE`); sigmas 8 / 26 / 80 px, gains 0.80 / 0.70 / 0.30; fades out inside hot areas at density 0.60-0.92. **area**: max 0.78-0.97 after the curve, sigmas 40 / 130 px, gains 0.07 / 0.07, suppressed where bright density within 18 px is 0.42-0.78 (print on paper). Glow clipped at 0.9. No glow inside near-white fills (input max > 0.85, S < 0.15, closed 61 px, holes < 20000 px, eroded 5 px, feather 2 px) |
| 6 | fog bank (s23 only) | `#c9bfd0`, g1677-1719, 40 -> 120 px tall at horizon row 600 -> 612, fade-in g1671-1681, alpha 0.80, x modulation 1 + 0.10 sin(x/47 + 0.02 g) + 0.06 sin(x/19 - 0.05 g); matte keeps dark (V < 0.33-0.38), bright (V > 0.84-0.90), warm saturated (hue 18-200, S > 0.42-0.50) and S > 0.58-0.64 in front |
| 7 | red protect | hue within 10-22 deg of red, S > 0.45-0.65, V > 0.15-0.35: input hue and saturation, graded luminance, weight `red` 0.8 |
| 8 | white protect | input max 0.74-0.86 and S below `wsat` (0.30): keep input colour; glow from outside allowed up to +0.02 |
| 9 | soft ceiling | per pixel, hue preserving: max channel above 0.965 rolled into 0.965-0.993; 1.0 maps to 0.985 |

**Per-shot corrections** (`SHOT`)

| take | settings | why |
|---|---|---|
| s08 sunny beach | gain 0.93, sat 0.94, bloom 0.55, haze 0.16 at 0.40 H | sand already bright (val 0.71) |
| s15 kitchen grey | sat 0.93 | already all warm |
| s16 grey drizzle | gain 0.88, con 1.30, gamma 1.08, sat 1.60, wr 1.04, wb 0.95, lowdark 0.22, haze 0.10 at 0.38 H, bloom 0.7, wsat 0.13 | washed out |
| s19 map | walls 0.80, sat 1.12, wr 1.03, wb 0.95, wprot 0 | cold diagram |
| s20 map | walls 0.85, sat 1.32, wr 1.05, wb 0.93, wprot 0 | cold diagram |
| s21 map | walls 0.75, lamp_g 0.87, lamp_b 0.69, sat 1.60, wr 1.05, wb 0.92, con 1.06, wprot 0 | coldest shot |
| s23 violet beach | haze 0.10 at 0.44 H, plus the fog bank | fog not readable |
| s24 night wave | bloom 0.8 | night |
| s25 office storm | lift 0.06, gamma 0.88, gain 1.04, sat 1.40 | too dark to read |

**Take-level grades before the conform**
- `v3/film/s10/grade.py` on takes s10 and s09 (s11 tested and left ungraded): red family (hue -20..25, tent centred 2.5) rotated toward orange by `shift`, weighted by S 0.15-0.35, sparing pure track red (S > 0.93 and V > 0.85); shadows under V 0.28 lifted by up to `lift`. File defaults `SHIFT` 7.0 deg, `LIFT` 0.035; the take notes say 8 deg and 0.07; the arguments actually used are not recorded. Reason: raw renders read red 43-44 %, dark 0.16 (more wallpaper in frame). Run: `python3 grade.py SRC_DIR DST_DIR [shift lift]` (folders: it grades every `*.png` in SRC_DIR). Tested: imports and grades a frame (mean change 0.9 levels).
- Everything else is graded inside Blender by the set's `setup_grade` (2.1, 2.2).

**Measured effect** (measured by GRADE.md on 448 sharp v1 conform frames, `v3/film/out/frames/`, graded by the pre-fix-round grade.py; the fix round (no glow in near-white fills) was not re-measured there): contrast 0.497 -> 0.623; V > 0.95 0.012 -> 0.036; top third luma 83.7 -> 93.3; middle 104.4 -> 118.2; sat 0.392 -> 0.410; head V 1.000 -> 0.984; black point 0.125 -> 0.101; colourfulness 55.3 -> 66.4. The delivered film (`deliver/film_v1_1_sharp_thai.mp4`, fix round included, captions in), score.py whole film, re-measured for this chapter: index 0.993, contrast 0.621, V > 0.95 0.032, top third 92, middle third 117, sat 0.417, head fill V 0.980, black point 0.094, colourfulness 65.3. No pumping: gain moves smoothly (1.059-1.064 with lamps in shot; 1.097 -> 0.971 over the s15 > s16 dissolve).

---

## 4. Measured result per shot (v1.1)

`hue_report.stats` on the same per-shot frame lists as the v1 review (`__PROJ__/v3/film/out/review/fs/sNN/`), read from the sharp v1.1 graded frames (`__PROJ__/v3/film/out_v11/graded/`, the picture of the delivered `film_v1_1_sharp_thai.mp4`); re-measured for this chapter. Chart: `colour_hue_per_shot.jpg`. "dark" is printed to 2 decimals; a 0.15 marked out of band is 0.150-0.155. The older numbers in `__PROJ__/v3/film/out_v11/review_look/hue_cmp.txt` were measured on the withdrawn frames that carried a background blur; do not use them.

| shot | light | red | orange | blue | violet | magenta | sat | val | dark | out of band |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | office_day | 28.4 | 42.7 | 11.0 | 0.2 | 1.3 | 0.43 | 0.57 | 0.12 | red, orange, blue |
| 2 | office_day | 52.8 | 19.2 | 18.6 | 0.6 | 3.9 | 0.47 | 0.52 | 0.16 | red, orange, dark |
| 3 | office_day | 38.7 | 34.8 | 17.5 | 0.9 | 4.0 | 0.46 | 0.54 | 0.15 | dark |
| 4 | office_day | 44.4 | 14.4 | 30.4 | 1.0 | 7.6 | 0.49 | 0.46 | 0.19 | red, orange, blue, sat, dark |
| 5 | office_day | 36.3 | 29.4 | 11.5 | 0.4 | 2.5 | 0.42 | 0.52 | 0.16 | blue, dark (cyan 19.9: map sea) |
| 6 | office_day | 40.7 | 18.3 | 28.8 | 1.0 | 4.6 | 0.48 | 0.49 | 0.16 | orange, sat, dark |
| 7 | office_day | 26.7 | 33.1 | 13.1 | 0.3 | 1.5 | 0.40 | 0.56 | 0.10 | red, blue (cyan 25.1) |
| 8 | beach_sunny | 31.9 | 27.9 | 36.4 | 2.1 | 1.4 | 0.36 | 0.77 | 0.06 | blue, sat, val, dark |
| 9 | office_day | 31.7 | 29.0 | 20.7 | 0.8 | 3.5 | 0.42 | 0.57 | 0.12 | in band |
| 10 | office_day | 39.1 | 35.1 | 13.5 | 1.1 | 3.9 | 0.45 | 0.55 | 0.15 | blue, dark |
| 11 | office_day | 32.2 | 40.5 | 15.0 | 2.3 | 3.1 | 0.46 | 0.54 | 0.16 | orange, dark |
| 12 | office_day | 37.7 | 24.6 | 24.0 | 0.9 | 5.9 | 0.40 | 0.48 | 0.17 | dark |
| 13 | office_day | 22.0 | 41.4 | 22.7 | 0.2 | 1.4 | 0.45 | 0.57 | 0.14 | red, orange |
| 14 | office_day | 33.1 | 32.3 | 26.1 | 1.6 | 4.2 | 0.37 | 0.61 | 0.14 | sat |
| 15 | kitchen_grey | 47.7 | 44.5 | 6.9 | 0.1 | 0.7 | 0.43 | 0.66 | 0.05 | red, orange, blue, val, dark |
| 16 | grey_drizzle | 33.3 | 6.2 | 57.0 | 1.3 | 1.9 | 0.31 | 0.67 | 0.07 | orange, blue, sat, val, dark |
| 17 | office_grey | 32.7 | 44.3 | 15.4 | 0.8 | 2.8 | 0.43 | 0.52 | 0.17 | orange, dark |
| 18 | office_grey | 44.5 | 32.2 | 12.2 | 0.8 | 3.2 | 0.40 | 0.51 | 0.18 | red, blue, dark |
| 19 | office_grey (map) | 31.6 | 39.3 | 27.4 | 0.4 | 0.9 | 0.38 | 0.53 | 0.12 | orange (at the edge) |
| 20 | office_grey (map) | 27.4 | 33.8 | 31.3 | 1.2 | 6.2 | 0.35 | 0.55 | 0.10 | red, blue, sat |
| 21 | office_grey (map) | 38.6 | 37.4 | 19.3 | 1.1 | 2.2 | 0.34 | 0.60 | 0.12 | sat |
| 22 | office_grey (map) | 28.2 | 33.8 | 30.7 | 1.0 | 3.1 | 0.35 | 0.57 | 0.11 | red, blue, sat |
| 23 | storm_approach | 23.7 | 5.8 | 3.1 | 56.8 | 10.5 | 0.32 | 0.58 | 0.01 | 7 of 8 |
| 24 | storm | 10.5 | 0.4 | 81.0 | 1.7 | 4.2 | 0.47 | 0.46 | 0.09 | red, orange, blue |
| 25 | office_storm | 27.8 | 16.7 | 43.8 | 2.5 | 6.2 | 0.33 | 0.49 | 0.08 | red, orange, blue, sat |
| 26 | kitchen_storm | 49.8 | 20.7 | 22.1 | 0.5 | 1.9 | 0.51 | 0.38 | 0.40 | red, orange, sat, val, dark |
| office shots 1-7, 9-14, 17, 18 | | 35.9 | 31.4 | 18.6 | 1.0 | 3.6 | 0.43 | 0.54 | 0.15 | **dark just over (0.151)** |
| whole film | | 33.9 | 29.5 | 25.1 | 2.4 | 3.3 | 0.41 | 0.55 | 0.14 | **in band** |

**Outside the band by design** (written in each take's QA.md):
- shot 8 (sunny exterior): follows the clip A exterior row (blue about 53, dark about 7).
- shot 15 (kitchen_grey): red-check oilcloth fills the lower 40 %; high-key grey morning; violet 0.1, magenta 0.7.
- shot 16 (grey_drizzle): the plan asks for halved saturation, no cast shadows, flat grey sky; chroma is sky and sea.
- shots 19-22 (map as terrain, office_grey): pale blue-grey walls fill the frame; the grade warmed them into or near the band.
- shot 23 (storm_approach): bruise-violet sky fills the top half, violet 56.8 by design; magenta just over at 10.5.
- shot 24 (storm night wave): night-blue like clip B's night (blue 81.0).
- shot 25 (office_storm): "special light", night-dark storm with lamps on.
- shot 26 (kitchen_storm): deliberate deep darks (dark 0.40); red from the oilcloth; shade blue-violet, magenta 1.9.

Shots 1, 2, 3, 4, 6, 10, 11, 12, 13, 17, 18 are over an edge (hue families by up to 12 points, dark 0.150-0.19 against the 0.15 edge), mostly from framing (more wallpaper or map in frame) and the global warm S-curve; the review saw no visible cast.

---

## 5. Recipes

Tested: 5.2 (run with `bpy` 5.3 as a Python module from the skill folder: materials, key sun, render and grade set up without error), the `hue_report` import snippet, `grade.py` (section 3), `s10/grade.py`, `spec/measure_color.py`. 5.3 and 5.4 give values, not code.

### 5.1 Start palette for a new set (swatches)

Copy these as albedos, then tune with the hue tool (5.6).

| role | start hex | gain | shade_mul (under an INTERIOR_DAY-like ambient) |
|---|---|---|---|
| main wall (warm, saturated) | `#aa3e2c` with motif `#d59a58` | 0.85 | (2.8, 2.05, 0.7) |
| upper band / frieze | `#6a2a1e` | 0.85 | (2.24, 1.64, 0.56) |
| wainscot, rails, doors | `#5e3018`, `#7c4620`, `#96502c` | 0.7 | (0.62, 0.95, 1.1) |
| floor boards / seams | `#a6764e` / `#2e1d22` | 1.0 | (1.06, 1.32, 1.38) |
| cool dark block (rug, carpet, cabinet) | `#283a74`, `#34508c` | 1.0 | 1 |
| ceiling / beams | `#8c5030` / `#4a2616` | 1.0 | (3.8, 3.0, 1.8) / (3.4, 2.6, 1.4) |
| dark frames, furniture edges | `#3d1c12`, `#4a2216` | 1.0 | 1.2-1.25 |
| brass, gold | `#e2a630`, `#cb9f48` | 0.5 | 1 |
| accent green / red | `#2d7a52` / `#c8301c` | 1.0 / 0.55-0.6 | 1.2 / 1 |
| paper and cream props | `#f6efe2` | 0.25-0.30 | 1 |
| bulbs (emission) | `#fffeec` strength 6 | | |
| set ink (hull) | `#2a1712` | | |
| exterior sand / sea / sky | `#d47844` `#de8e50` `#e8a462` / `#3559b0` -> `#6f9fe6` / `#4a78cd` -> `#a9c6ec` | | |

Composition by area (spec targets from the four reference interiors): about 30 % dark cool (navy, plum), 35-45 % warm mids (wood, terracotta, red), about 10 % brass or tan, at most 8 % near-white (heads, lit paper, lamps). Every large surface needs drawn detail (luma std after a sigma-12 high-pass 0.03-0.10).

### 5.2 Light a new interior

Use the office model and register a preset whose name starts with `INTERIOR_` (`build()` deletes old materials only by that prefix; inferred from office3d.py line 329). For a new room in its own file, follow `kitchen3d.build()`: set `S.STATE['P']`, then use `S.mat_lit`.

```python
import sys; sys.path.insert(0, 'pipeline/v3/set3d')
import office3d as S                                   # light model, materials, render, grade
P = dict(shade=(0.20, 0.27, 0.54), key=(2.30, 1.65, 0.74), lift=(0.0, 0.010, 0.026),
         key_dir=(-1.0, 1.3, -0.30), sun_angle=0.45, form=(0.14, -0.04, 0.26), falloff_y=0.30,
         bloom_size=0.05, grade_offset=(0.002, 0.0045, 0.010), grade_saturation=1.06)
S.STATE.clear(); S.STATE['P'] = P; S.STATE['preset'] = 'INTERIOR_MYROOM'
wall = S.mat_lit('INTERIOR_MYROOM_wall', '#aa3e2c', gain=0.85, shade_mul=(2.8, 2.05, 0.7), form=P['form'])
wood = S.mat_lit('INTERIOR_MYROOM_wood', '#5e3018', gain=0.7, shade_mul=(0.62, 0.95, 1.1), form=P['form'])
bulb = S.mat_emit('INTERIOR_MYROOM_bulb', '#fffeec', strength=6.0)
# key sun exactly as office3d.build does it
import bpy, math
from mathutils import Vector
k = max(P['key']); d = bpy.data.lights.new('key_sun', 'SUN'); d.color = tuple(x / k for x in P['key'])
d.energy = math.pi * k; d.angle = math.radians(P['sun_angle'])
sun = bpy.data.objects.new('key_sun', d); bpy.context.scene.collection.objects.link(sun)
sun.rotation_euler = Vector(P['key_dir']).to_track_quat('-Z', 'Y').to_euler()
S.setup_render(bpy.context.scene, 'final'); S.setup_grade(bpy.context.scene)
```

The `rotation_euler` line gives the same rotation as office3d.py lines 511-514 (`(-kd).to_track_quat('Z', 'Y')`, `kd` = normalised `key_dir`): checked, both give (1.3899, 0.0, 0.6557) rad for `key_dir` (-1.0, 1.3, -0.30). Rules: aim the sun through a window so a hard patch lands on floor and lower wall; no fill light, no area light; keep world black; hide set objects from bounce rays (`S.no_bounce`).

### 5.3 Light a new exterior

Start from `beach3d.PRESETS['SUMMER_SUN']` (2.2): blue ambient (0.10, 0.25, 0.98), a separate `A_pale` for pale albedos, `shade_tint` mixed at 0.5 so orange sand shades at hue 235-250 and not magenta, sun 1.0 deg at 40-50 deg elevation, a sky gradient world (camera rays only), haze toward the horizon colour (near 0, mid 30-50 %, far 90-100 %), no ink on terrain and sky. Copy a preset: `P = dict(B.PRESETS['SUMMER_SUN']); P.update(...); B.PRESETS['MY_EXT'] = P; A = B.build('MY_EXT')` (the pattern `beach_ext._storm_approach` uses).

### 5.4 Night, grey or storm version of an existing set

- **Grey / overcast** (office_grey pattern): key x0.29 and neutral-warm (0.66, 0.58, 0.50), not blue (a blue key turned floors and woods to grey mud, orange 10-14 %); angle 3 deg; the room shell stops shadowing the key (no sun patch); the coolness goes into the ambient (0.20, 0.23, 0.41); warm the woods' ambient with more green than red (1.30, 1.50, 0.60) so dark browns land at hue 15-30; cut the wall key (kgain 0.6-0.7) or the crimson wall takes half the chroma; bulbs on (8); grade sat 0.96, bloom 0.08 / 0.65. Beach: GREY_DRIZZLE (2.2).
- **Storm**: ambient about a third of day (0.068, 0.082, 0.165), key x0.083 (0.12, 0.13, 0.19), bulbs 12, rain card, lightning as a second Sun (0.82-0.86, 0.88, 1.0), 1.2-1.5 deg, energy flash x 3.2 x day key, held 1-6 frames with a decaying key list (2.2 kitchen_storm); card tint (0.86, 0.86, 0.95). Keep the lift low and only slightly blue (cutting it took office_storm magenta from 14.5 to 6.1 %). Warm, low-blue shade multipliers on red cloth and wood ((2.2, 1.3, 0.55), (2.6, 1.5, 0.55), (1.8, 1.15, 0.55)) and a neutral-blue grade offset (0.0, 0.002, 0.007) (kitchen_storm magenta 12-27 % -> 5.7 %). Then lift the murk in the grade (s25: lift 0.06, gamma 0.88, gain 1.04, sat 1.40: val 0.33 -> 0.49, dark 33 % -> 8 %).
- **Night** (not built in film 1; reference measured): not dark: V mean about 0.59, 86 % blue-violet; start from `lightkit_clp` `NIGHT` (ambient (0.12, 0.13, 0.45), key (0.33, 0.35, 0.75)); sky `#1e2e7b` 0 % -> `#1748ae` 60 % -> `#204c8f` 100 % (`spec/color_light_post.md`; `lightkit_clp.PRESETS['NIGHT']['sky']` has `#1a3b92`, `#1748ae`, `#204c8f`); warm window and torch accents; character tint `#fbdaf7` and ink `#1e142e` (`puppet` pose keys `tint`, `ink`); moon halo with the compositor Glare bloom at size 0.20, strength 1.0 (`spec/LOOK_SPEC.md` compositor table; `grade_compositor.build(scene, preset=dict(bloom_size=0.20, bloom_strength=1.0))`).

### 5.5 Check a set or a take with the hue tool

`python3 pipeline/v3/tools/hue_report.py <frames or folder>` prints one row per argument and the band; it adds film 1's reference rows only when film 1's reference stills are under `ref/a` and `ref/b` (not shipped). In code, import its `stats` (tested on 50 graded frames of film 1):

```python
import sys, glob; sys.path.insert(0, 'pipeline/v3/tools')
import hue_report as H
fl = sorted(glob.glob('my_take/frames/g_*.png'))
h, s, v, dk = H.stats(fl)
bad = [k for k, (lo, hi) in H.TARGET.items() if not lo <= {'sat': s, 'val': v, 'dark': dk}.get(k, h.get(k)) <= hi]
print({k: round(x, 1) for k, x in h.items()}, round(s, 2), round(v, 2), round(dk, 2), 'OUT:', bad)
```

Measure set stills from the named cameras with stand-in actors, and every take's frames. Also `python3 pipeline/spec/measure_color.py IMAGE` (tested) for black point, darkest-tenth colour (want hue 250-345, not brown), mid-band colour and near-white share.

### 5.6 What to change when it reads wrong

| symptom (hue tool or eye) | cause found in film 1 | change |
|---|---|---|
| magenta > 10, shade looks pink-purple | violet ambient on rose/red walls; plum dark lift; plum CDL offset | ambient bluer (0.28, 0.255, 0.48) -> (0.20, 0.27, 0.54); lift plum (0.024, 0.016, 0.040) -> navy (0.0, 0.010, 0.026); walls rose `#9c4a50` -> terracotta `#aa3e2c`; per-surface shade_mul with low blue on warm surfaces; grade offset (0.002, 0.0045, 0.010). Office opening went magenta 24.8 -> 3.5 |
| magenta on orange sand (exterior) | `art x A` with a blue A gives hue 290 on orange | mix half the shade toward a blue-violet `shade_tint` (0.22, 0.20, 0.38): shade hue 235-250 |
| cold: blue > 30, red/orange low | pale blue-grey walls fill the frame (map shots) or grey-weather ambient | warm key on pale walls in the grade (`walls` 0.75-0.85), wb R 1.03-1.05 / B 0.92-0.95, sat 1.12-1.60 (s19-s21: blue 46/62/67 -> 27/31/19). Better: author warmer walls and light from the room's warm key |
| orange > 38 | woods and floor fill the frame; warm S-curve | rotate less, or more blue in the frame (rug, cabinet), or `s10/grade.py`-type correction the other way |
| red > 41 | crimson wall dominates (framing) | wall key gain 0.6-0.85; or rotate the red family 7-8 deg toward orange (`s10/grade.py`) |
| washed out (sat < 0.38, dark < 0.08, val > 0.63) | soft overcast, pale sky large in frame | contrast 1.30 around luma 0.42, gamma 1.08, sat 1.60, darker lower frame 22 %, gain 0.88 (s16: sat 0.24 -> 0.31, dark 0.01 -> 0.07; still out). Better: frame less sky, add dark foreground, darker wet sand |
| too dark (val < 0.45, dark > 0.15) | storm ambient, deep foreground | lift 0.06, gamma 0.88, gain 1.04 in the grade; or raise the ambient falloff (`falloff_y` 0.34 -> 0.30); keep deep darks only where the story wants them |
| darkest tenth brown or black | grey or neutral lift, no offset | navy-plum lift and CDL offset; black point 0.08-0.12 |
| shadows brown | ambient grey or warm | blue ambient; yellow key so key + ambient add to near white |
| heads tinted or shaded | lit head material, global saturation or white balance on faces | emission card to camera rays only; white protect in the grade; head fill `#fef7f6` |
| lamps are flat white discs | nothing above 1.0, no bloom | bulbs as emission 6-12, Glare bloom threshold 1.0, grade hot-source bloom |

---

## 6. What the reviews found wrong, and the better value next time

### 6.1 Colour and light faults (`__PROJ__/deliver/QA_film.md`, `QA_film_v1_1.md`, `__PROJ__/v3/out/COLOUR.md`)

| fault | where | better value next time |
|---|---|---|
| first office came out magenta 24.8-28 % (client: "the colours are not like the reference") | office, before the colour pass | start from the post-pass values (2.2, 2.3); check `hue_report` on the first stills before rendering takes |
| light at its floor: V > 0.95 3.1 % against 5-6 %, top third 92 against 94-118, contrast 0.622 (edge 0.60) | whole film | more real emitters in frame (lamps, windows in direct sun at emission 3, sun glare card when the sun is in frame: core 68 px, 50 % at 120 px, 10 % at 260 px), and raise the 0.65 knot of `CURVE` or `SAT_GLOBAL` if contrast or sat sit at the edge |
| no sun bloom, no visible haze on the sunny beach | s08 | add a sun glare card when the sun is in or near frame, and keep the grade bloom at 1 instead of 0.55 (inferred; not tried) |
| grey beach washed out, then lavender sky after the grade | s16 | the drizzle sky `#6f7ba0` -> `#c0c6da` drifts to violet under sat 1.60; grade it with lower sat (about 1.3, inferred) and add dark wet foreground and figures instead of tilting to empty sky |
| map-as-terrain cold (blue 46-67 %), then "a diagram, now warm" | s19-s21 | light explainer sequences with the room's warm key; author map walls warm (sand/paper) rather than `#c4c6d4` blue-grey |
| climax in murk (val 0.33, dark 0.33) | s25 | storm ambient about 0.10-0.12 instead of 0.068 (inferred from the grade fix), or keep the s25 grade |
| violet sky flat, fog bank 40-60 px, easy to miss | s23 | keep the sky gradient with a horizon glow; fog bank at least 120 px from the start |
| all-warm kitchen (blue 7 %) | s15 | add a cool block (navy cup rim, blue curtain larger in frame, window) |
| grade ghost face, g740-743 | s11 | white protect and hot bloom must not treat motion-blurred ink as a fill (fixed: `FILL_*` stage and `HOT_SAT`); check fast moves frame by frame after grading |
| shots pushed a few points over an edge by the warm S-curve (s04, s10, s11, s13, s17, s26) | office | measure each take after the grade, not only the aggregate |
| ink limbs vanish on `#55291a`, `#1f2a55` | puppets | keep a mid-value surface behind the legs or use the `rim` pose key |
| caption band brighter after the grade (mean luma 0.378 -> 0.412) | forecast sheet g960-969 | keep paper behind the caption band under luma 0.85, or lower paper gain |

### 6.2 What the reference has that we did not build

Night (b/t34.0-t44.0 look), sunset, late afternoon, lamp-lit interior at mid-luma 0.15 (`INTERIOR_LAMP` exists, unused), clip B per-shot character tint (only office_storm tints cards), painted haze layers and light shafts, the brightness-dip beat.

### 6.3 Documentation that disagrees with the code (code wins)

- Fixed in the skill's copies (they now give the code values): `v3/set3d/API.md` section 5 (light), `v3/set3d_kitchen/API.md` (kitchen_grey key, angle, ambient), `v3/set3d_ext/light/API.md` (office_grey grade offset).
- kitchen_storm: code angle 4.0, s26 QA says 2 deg.
- `v3/film/s10/grade.py` defaults 7 deg / 0.035; its QA says 8 deg / 0.07.
- `v3/shots/qa_light.py` imports `set3d/review/review_analyze` (now bundled with its helper `rmeasure.py`); it renders frames of the opening (`v3/shots/film.py`): copy it and swap the scene for another set.

---

## Sources

Skill `pipeline/`: `spec/color_light_post.md`, `spec/environment_materials.md`, `spec/LOOK_SPEC.md`, `spec/captions.md`, `spec/lightkit_clp.py`, `spec/grade_compositor.py`, `spec/measure_color.py`; `v3/set3d/office3d.py`, `v3/set3d/textures.py`, `v3/set3d/API.md`; `v2/sets/office.py`; `v3/set3d_ext/light/office_light.py`, `v3/set3d_ext/light/API.md`; `v3/set3d_ext/props/office_props.py`; `v3/set3d_ext/mech/office_mech.py`, `v3/set3d_ext/mech/API.md`; `v3/set3d_beach/beach3d.py`, `v3/set3d_beach/beach_tex.py`, `v3/set3d_beach/API.md`; `v3/set3d_ext/beach/beach_ext.py`, `v3/set3d_ext/beach/API.md`; `v3/set3d_kitchen/kitchen3d.py`, `v3/set3d_kitchen/kitchen_tex.py`, `v3/set3d_kitchen/API.md`; `v3/paper/paper.py`, `v3/paper/API.md`; `v2/puppet/puppet.py`, `v2/puppet/API.md`; `v3/cast/cast_ext.py`, `v3/cast/API.md`; `v3/out/COLOUR.md`; `v3/tools/hue_report.py`; `v3/film/CONVENTIONS.md`; `v3/film/out_v11/grade.py`, `v3/film/out_v11/GRADE.md`; `v3/film/s10/grade.py`, `v3/film/s10/shot.py`, `v3/film/s11/shot.py`, `v3/film/s26/QA.md`, `v3/film/s24/QA.md`; `v3/shots/qa_light.py`.
Project `__PROJ__/`: `plan/shot_plan.json` (light per shot); `deliver/QA_film.md`, `deliver/QA_film_v1_1.md`; `v3/film/out/review/fs/sNN/` (per-shot frame lists, hue re-measured on the sharp `v3/film/out_v11/graded/` frames for section 4); `v3/film/out_v11/film_silent.ass`; `v3/film/s15/QA.md`, `s16/QA.md`, `s21/QA.md`, `s23/QA.md`, `s25/QA.md`; `v3/film/out_v11/graded/` (sheet frames g291, g1150, g1862, g418, g1045, g1700, g1755, g966, g1922); `ref/a`, `ref/b` (hue_report reference rows, run this session).
