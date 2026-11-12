# Colour, lighting and post-processing spec

Lens: colour, lighting, post. Reference clip A = "Why Perfect Railroads Don't Work" (flat 2D characters inside a real-time-looking 3D world), clip B = "The Ancient Jar That Warned an Empire" (flat 2D characters over painted 2.5D sets). Frame names are `a/tSS.S` and `b/tSS.S`; pixel coordinates are (x, y) in the 720x1280 frame. All hex values are sRGB as displayed. "Luma" is Rec.709 luma of the encoded values (0..1). "Linear-luminance ratio" is computed after undoing the sRGB curve.

Files written with this spec (all under `PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj`):

| file | purpose |
|---|---|
| `PROJ/spec/color_light_post.md` | this document |
| `PROJ/spec/measure_color.py` | re-measurement tool: `python3 measure_color.py --palette FRAME...` prints every statistic used in the target table (caption band y 850..950, x 120..600 is masked out) |
| `PROJ/spec/lightkit_clp.py` | lighting presets, environment / emissive / character materials, sun and lamp helpers (API-checked in Blender 5.3.0, no render) |
| `PROJ/spec/grade_compositor.py` | compositor grade (bloom, lifted plum black, warm slope, saturation, optional vignette); executed in Blender 5.3.0 as compositor-only runs |
| `PROJ/spec/ffmpeg_grade_finish.txt`, `ffmpeg_grade_finish_bloom.txt`, `ffmpeg_grade_rescue.txt` | fallback ffmpeg filter chains (each executed) |
| `PROJ/ref/crops/color/` | crops, gridded sheets, `stats_all.json` (all 260 reference frames), `stats_sel.json`, `samples.json`, `palette_predicted.json` |
| `PROJ/ref/extra/color/` | consecutive source frames used for grain / halo tests, compositor test outputs in `comp/` |

Method summary: 16 frames were opened at full resolution, about 28 more as gridded sheets and zoomed crops, and all 260 half-second frames (130 per clip) plus both v1 frames were measured with numpy / OpenCV. No 3D render was started. The compositor chain was validated with compositor-only runs on synthetic images and on the two v1 PNGs (0.1 to 0.4 s each, one thread).

---

## 1. Observations

### 1.1 Overall grade and palette

1. The reference is dark-mid, saturated and never pale. Over all frames the median mean-saturation is 0.48 (A) and 0.41 (B), median mid-luma is 0.44 (A) and 0.38 (B). v1 sits at saturation 0.29 and mid-luma 0.65: it is both paler and brighter than three quarters of the reference frames.
2. Interiors are the darkest scenes, not the brightest. Median mid-luma: A train car 0.15 (`a/t27.0`-`t28.5`), B throne room 0.25 (`b/t21.0`-`t26.5`), B hall 0.28 (`b/t00.0`-`t13.5`), A concourse 0.42 (`a/t31.5`-`t35.5`). The v1 office is at 0.64.
3. No large pale neutral area exists anywhere. The biggest k-means cluster in the reference interiors is always a dark saturated colour: navy `#161a42` 31 % (`a/t27.5`), brown `#6b3723` 20 % (`b/t22.0`), plum-black `#221c31` 25 % (`b/t09.0`), wood `#976c4d` 25 % (`a/t34.5`). In v1 the biggest cluster is cream wall `#ddd5ba` 33 %, then tan floor `#b89269` 26 %.
4. Hue families, as a share of the whole frame averaged over each clip (pixels with S > 0.15): warm reds, oranges and browns 52 % in both clips, blue-violet 30 %, magenta 6 to 7 %, green 1 %. Green and teal appear only as accents (hero vest `#50aaa3` in `a/t02.0`, tool box, lamp trim).
5. Blacks are lifted and tinted plum. The burned-in caption outline reaches luma 0.001, but the darkest 0.5 % of the picture itself sits at luma 0.087 (A) and 0.079 (B); the 1st percentile is 0.104 (A) and 0.095 (B). The mean colour of the darkest tenth of each frame is `#3d1c32` (A) and `#392433` (B), hue 318 to 319 degrees. v1's darkest tenth is brown `#48392d`, hue 26.
6. Mid-tones average rose-mauve (`#90646a` A, `#7d656d` B); highlights average warm near-white (`#d1c7c6` A, `#dbc5b1` B). So the grade is a split tone: plum-violet shadows, warm cream highlights. v1 mid-tones are beige `#b5a78d`.
7. Whites are reserved for character heads, paper and light sources. Near-white pixels (V > 0.95) cover a median 3.5 % (A) and 4.5 % (B) of the frame.
8. Surfaces are never flat fills (except one carpet). Local luma detail (std after removing a sigma-12 blur) is 0.03 to 0.14 on wood, rock, stone, quilt, grass (`a/t34.5`, `a/t02.0`, `a/t16.0`, `a/t53.0`, `b/t22.0`, `b/t28.0`, `b/t46.5`). v1 walls and floor are at 0.002.

### 1.2 Key light, shadows, ambient

1. Clip A uses one hard sun. Shadow edges are 4 to 21 px wide (10-90 % rise) at 720 px frame width: 4 px for the building shadow in `a/t34.5`, 6 px for the head shadow in `a/t02.0`, 12 px for the umbrella shadow in `a/t53.0`, 21 px for a character shadow in `a/t34.5`.
2. The key comes from camera-left and above in most shots: sun disc visible at (150, 330) in `a/t16.0`; left side of the canyon wall lit and right side shadowed in `a/t02.0`; shadows run to the right in `a/t53.0`; left tower face lit in `b/t28.0`; jar lit on its left in `b/t00.0` and `b/t46.5` (sun at (20, 230)). `a/t34.5` is the exception (sun behind the set, long shadows towards the camera).
3. Shadows are tinted blue-violet, not grey or brown. On warm surfaces the hue jumps from 16-28 degrees (lit) to 244-259 degrees (shadow): `#d9734d` to `#332d40` (`a/t02.0`), `#ac825e` to `#525065` (`a/t34.5`), `#946645` to `#252432` (`a/t32.5`). Grey ballast stones in shade read blue-purple (`a/t16.0`, around (300, 1100)).
4. Shadow depth depends on the time of day. Noon and interior sun shafts: linear-luminance ratio 0.11 to 0.33 (V ratio 0.29 to 0.59). Late afternoon deck: the shadow keeps the same value as the lit deck and only changes hue, `#9d5975` to `#475895` (V ratio 0.95, luminance ratio 0.67, `a/t53.0`) and `#9d6e9b` to `#7170ad` (`a/t49.0`).
5. The blue channel of a shadow can be higher than the blue channel of the lit surface (`a/t53.0`: lit linear B 0.178, shadow 0.300). Plain lighting plus a per-channel curve cannot do that, so the look includes a luminance-keyed shadow tint or an engine shadow colour. The practical consequence: light with a yellow key and a strongly blue ambient so that the two add up to white.
6. Clip B sets are painted with baked two-tone shading: jar lit `#a2a2a4` to shade `#757482` (V x0.79, luminance x0.49, slight violet, `b/t00.0`), tower sunlit `#e3d3b9` to shade `#bcb2b1` (`b/t28.0`), jar at sunrise `#9b7b68` to `#4f414f` (`b/t46.5`). Shade is always cooler and more violet than the lit side.
7. No 3D rim light exists in either clip. Clip B characters carry a drawn highlight strip, 2 to 4 px wide, just inside the outline on the key-facing side (`b/t28.0`, robe at x 534..536, y 850).
8. "White" props are cream, not white: the newspaper `#fcf4e1` (`a/t32.5`, (240, 740)), a sheet lying on the sunlit floor `#e9d6bb` (`a/t34.5`, (270, 765)), white floor tiles `#efe9ee` (`a/t32.5`, (600, 700)). Only heads and light sources go whiter.

### 1.3 Time-of-day treatments

| treatment | frames | what it looks like (measured) |
|---|---|---|
| noon exterior | `a/t02.0`, `a/t16.0`, `a/t45.0` | sky zenith `#386ec9`-`#4a78cd`, horizon `#92b7e7`; sunlit rock `#e9671d`, ground `#d9734d`; shadows `#332d40`-`#781518`; sun glare 260 px radius when the disc is in frame |
| late afternoon | `a/t49.0`, `a/t53.0` | sky `#4d7dd0` to `#83aee3`; deck rose-mauve `#9d5975`; shadows saturated blue `#475895` at equal value; far mesa `#643c5f`, far mountains `#7788d0` |
| sunset | `a/t61.0`, `b/t31.0` | A: sky `#bdb0b8` (top) to `#eee4cf` to `#f2d8ab` at the horizon, deck `#703b4b`; B: sky `#e16c7e` to `#ff9f8c` to `#ffdc99`, sun disc white with rays, foreground silhouette `#1e081f`, sunlit ground `#d6644a`, cloud tops `#fcd5b1` over undersides `#ca6a9c` |
| night | `b/t34.0`, `b/t41.5`, `b/t44.0` | not dark: V mean 0.59, mid-luma 0.32, saturation mean 0.54, 86 % of the frame is blue-violet; sky `#1748ae`-`#1e2e7b`, walls `#576295`, road `#3d346d`, light-grey jar `#787adf`; moon `#eff8ff` with a blue halo; warm torch and window accents; heads tinted lilac `#fbdaf7` |
| lamp-lit interior | `a/t27.5`, `b/t23.0` | lamps clip to `#fffeec`; walls `#561e37`, seat `#84052e`, ceiling `#c03c12`, carpet `#12183c`; saturation mean 0.73, mid-luma 0.15; candle flame with a warm halo |
| daylight interior | `a/t32.5`, `a/t34.5`, `b/t00.0`, `b/t09.0` | A: warm wood `#ac825e` with hard blue-violet shadows, cream paper `#e9d6bb`, blue sky through the roof `#8797d9`; B: mauve stone `#7e5f65`, navy floor `#3a3858`, red drapes `#9d3e3f`, gold `#f3d26d` |
| brightness dip beat | `b/t03.3`-`b/t03.7` | the whole frame dims for about 0.4 s on a dramatic line (V p95 0.97 falls to 0.75, head `#f8f9fb` becomes `#c6c8b0`), then returns. Optional effect |

### 1.4 Sky gradients and haze

1. Skies are vertical gradients, darker and more saturated at the top, lighter at the horizon, with soft painted clouds (`a/t49.0`: `#4a78cd`, `#5e92e5`, `#7eabe9`, `#92b7e7` from y 20 to y 365).
2. Distance haze pulls everything to the horizon colour. `a/t09.0`: near sand `#e69a4f`, far sand `#e9a695`, farthest mountain layer `#99c1e5`, horizon sky `#88bce6`; the farthest layer is within 5 % of the sky. `a/t58.5`: canyon wall near `#f38d45`, middle `#c45454`, far `#c46068`, far mesa `#8d6fa5`. `b/t46.5`: near tree `#3a4837`, middle trees `#95a34b`, far castle `#c99a80`, far hills `#f9cbb3` against sky `#ffcb9b`.
3. Saturation falls and value rises with distance (B morning: S 0.54 at mid distance to 0.28 far, V 0.64 to 0.98).

### 1.5 Glow and bloom

1. Small emitters have a tight warm halo. Radius where the excess over the background falls to 10 %: ceiling lamp core 32 px, 10 % at 56 px (`a/t27.5`, (85, 265)); small lamp core 16 px, 10 % at 28 px (`a/t27.5`, (605, 385)); street lamp core 8 px, 10 % at 20 px (`a/t61.0`, (50, 508)). So the halo reaches 12 to 24 px beyond the bright core (1.7 to 3.3 % of frame width). Halo colour runs `#d7a273` to `#975937` around the lamp.
2. Clip B glows are painted and larger: torch flame core 8 px, 50 % at 28 px, 10 % at 40 px, colour `#ffc76a` to `#be7b50` (`b/t38.5`); moon disc 36 px with a halo to 84 px, `#5a8af5` fading to the sky (`b/t44.0`); glowing crack core 16 px, 50 % at 88 px, 10 % at 136 px (`b/t63.0`).
3. The sun itself has a very wide soft glare: core (luma > 0.95) 68 px, 50 % at 120 px, 10 % at 260 px (`a/t16.0`); B sunrise and sunset discs 130 to 145 px core with glare to 320 to 350 px (`b/t46.5`, `b/t31.0`).
4. White character heads do not glow. The sky stays flat at luma 0.82 right up to the head outline in `a/t16.0` (row y 560).

### 1.6 Depth of field, vignette, grain, sharpening, motion

1. Depth of field: clip A is deep focus (background Laplacian energy 56 behind a close-up in `a/t55.0`, macro foreground crisp in `a/t40.0`). Clip B blurs the set behind close-ups: background Laplacian energy 6.5 in `b/t04.5` against 135 for the same hall in the wide shot `b/t09.0`; estimated blur sigma 5 to 7 px. B also blurs near foreground objects (`b/t17.0`, banner at left).
2. Vignette: none that can be separated from content. A flat blue wall shows edge/centre 1.03 (`a/t08.0`, rows 40-400); the bottom corners of the 130-frame mean images are within 2 % of the bottom centre in both clips; a flat sky shows a 5 % edge fall-off in `b/t59.0`. Treat the vignette as 0 to 5 %.
3. Film grain: none. High-pass residual in flat sky is 0.3 to 0.5 8-bit levels and temporal residual is 0.05 to 0.3 levels over 8 consecutive frames (`a/t16.0`, `a/t49.0`, `b/t59.0`, `b/t28.0`). The sources are 1.1 to 2.0 Mbit/s H.264, so very fine grain could have been removed by compression; nothing visible remains.
4. Sharpening: none. No overshoot beside the character outline against the sky (`a/t16.0`).
5. Motion blur appears only on fast camera moves in clip A (`a/t10.0`, `a/t51.0`). Not needed for the look.
6. Atmosphere extras, optional: faint light shafts under the glass roof (`a/t34.5`, upper left) and a few floating dust specks in the B hall (`b/t03.5`).

### 1.7 How the 2D characters are lit compared with the environment

1. Clip A characters are unlit. The head fill is the same near-white in every lighting condition: `#fdf7f7` in direct sun (`a/t16.0`), `#fcf8f5` under lamps (`a/t27.5`), `#fdf8f5` inside a shaded window (`a/t29.5`), `#faf9f5` in late-afternoon light (`a/t53.0`): V 0.98 to 1.00, S 0.02 to 0.04. They receive no scene shadows and no shading.
2. The fill is flat. Across the head in `a/t16.0` V stays 0.98 to 0.99; the only variation is a soft inner falloff of about 7 % luma over the 14 px next to the outline (luma 0.89 at the rim to 0.96; head diameter about 185 px).
3. Clip A characters do cast real, hard shadows, because they are flat cut-outs standing in the 3D scene. With the sun side-on the shadow is a thin line (`a/t03.0`, leg shadows running from about (330, 1060) towards (470, 1250)); with the sun in front or behind it is a full silhouette (`a/t32.5`, about (480..720, 945..1075); `a/t34.5`, about (20..160, 690..720)). Shadow colour on wood is `#252432` to `#444153`, V x0.34 to x0.50, linear luminance x0.12 to x0.25, edge width 6 to 21 px.
4. Clip B characters take a uniform per-shot tint and keep full brightness: day `#faf8f3` (`b/t17.0`), candle-lit `#f9f9ea` (`b/t23.0`), throne room `#faded0` (`b/t22.0`), night `#fbdaf7`, `#fcc8d9`, `#e8c3e5` (`b/t34.0`, `b/t44.0`, `b/t38.5`). Tint saturation is 0.13 to 0.21 at night and V stays at or above 0.91 in these samples. A soft radial falloff towards the outline is visible at night; there is no directional terminator.
5. Clip B characters cast only a small soft contact ellipse under the feet: `#4e3225` on road `#cba66f` (V x0.38, luminance x0.10), about 40 px wide with a 20 px soft edge (`b/t28.0`, (565, 921)).
6. Ink lines are dark plum, not black: darkest outline pixels are `#251921` to `#34201d` to `#302535`, luma 0.10 to 0.18 (`a/t45.0`, `a/t02.0`, `a/t16.0`). The burned-in caption is the only pure black in the frame.

---

## 2. Measurements

### 2.1 Global statistics, 25 reference frames and both v1 frames

| frame | scene | S mean | S p50 | S p90 | V mean | V p5 | V p95 | luma p5 | luma p50 | luma p95 | contrast p95-p5 | colourfulness | share S>0.5 | share S<0.15 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| a/t02.0 | canyon noon, hero | 0.653 | 0.764 | 0.933 | 0.599 | 0.314 | 0.961 | 0.101 | 0.337 | 0.619 | 0.518 | 98.1 | 0.702 | 0.073 |
| a/t06.0 | canyon + bridge, wide | 0.577 | 0.579 | 0.861 | 0.686 | 0.376 | 0.902 | 0.157 | 0.402 | 0.701 | 0.544 | 79.8 | 0.656 | 0.011 |
| a/t09.0 | desert noon, wide | 0.445 | 0.506 | 0.655 | 0.882 | 0.780 | 0.945 | 0.558 | 0.666 | 0.789 | 0.230 | 104.1 | 0.511 | 0.081 |
| a/t16.0 | boss low angle, sun in frame | 0.287 | 0.269 | 0.496 | 0.708 | 0.216 | 0.965 | 0.140 | 0.638 | 0.915 | 0.774 | 53.6 | 0.093 | 0.208 |
| a/t19.5 | two-shot, noon | 0.320 | 0.290 | 0.595 | 0.672 | 0.224 | 0.937 | 0.147 | 0.529 | 0.840 | 0.693 | 60.7 | 0.163 | 0.199 |
| a/t27.5 | train car interior, lamps | 0.739 | 0.756 | 1.000 | 0.450 | 0.220 | 0.882 | 0.089 | 0.145 | 0.447 | 0.358 | 102.7 | 0.897 | 0.033 |
| a/t34.5 | concourse interior, daylight | 0.377 | 0.391 | 0.538 | 0.544 | 0.310 | 0.796 | 0.216 | 0.424 | 0.662 | 0.447 | 44.9 | 0.214 | 0.063 |
| a/t40.0 | macro rail, noon | 0.598 | 0.687 | 0.854 | 0.709 | 0.243 | 0.984 | 0.119 | 0.500 | 0.859 | 0.740 | 98.4 | 0.652 | 0.070 |
| a/t45.0 | two-shot by wall | 0.567 | 0.670 | 0.870 | 0.733 | 0.286 | 0.980 | 0.169 | 0.474 | 0.878 | 0.709 | 105.2 | 0.603 | 0.130 |
| a/t49.0 | deck, late afternoon | 0.469 | 0.487 | 0.627 | 0.519 | 0.137 | 0.906 | 0.078 | 0.345 | 0.686 | 0.608 | 66.9 | 0.448 | 0.018 |
| a/t55.0 | hero close-up | 0.489 | 0.493 | 0.850 | 0.730 | 0.243 | 0.984 | 0.171 | 0.542 | 0.908 | 0.737 | 95.6 | 0.493 | 0.176 |
| a/t61.0 | sunset bridge | 0.340 | 0.328 | 0.622 | 0.637 | 0.227 | 0.953 | 0.142 | 0.503 | 0.881 | 0.740 | 55.9 | 0.254 | 0.246 |
| b/t03.5 | hall interior (dimmed beat) | 0.281 | 0.232 | 0.574 | 0.384 | 0.192 | 0.749 | 0.126 | 0.288 | 0.709 | 0.583 | 32.0 | 0.154 | 0.250 |
| b/t09.0 | hall interior, orbit | 0.376 | 0.328 | 0.640 | 0.374 | 0.165 | 0.796 | 0.086 | 0.255 | 0.704 | 0.617 | 41.8 | 0.275 | 0.066 |
| b/t15.0 | army exterior, day | 0.189 | 0.137 | 0.412 | 0.682 | 0.286 | 0.973 | 0.207 | 0.677 | 0.906 | 0.699 | 37.8 | 0.070 | 0.536 |
| b/t22.0 | throne interior | 0.570 | 0.603 | 0.763 | 0.490 | 0.200 | 0.980 | 0.113 | 0.262 | 0.883 | 0.770 | 65.3 | 0.697 | 0.010 |
| b/t28.0 | city gate, day | 0.326 | 0.297 | 0.567 | 0.690 | 0.325 | 0.976 | 0.252 | 0.601 | 0.900 | 0.649 | 59.1 | 0.191 | 0.248 |
| b/t31.0 | sunset hill | 0.484 | 0.455 | 0.742 | 0.723 | 0.114 | 1.000 | 0.050 | 0.639 | 0.975 | 0.925 | 69.1 | 0.362 | 0.040 |
| b/t34.0 | night close-up | 0.573 | 0.565 | 0.846 | 0.569 | 0.200 | 0.957 | 0.109 | 0.271 | 0.812 | 0.703 | 68.0 | 0.669 | 0.071 |
| b/t38.5 | portcullis, night + torches | 0.427 | 0.385 | 0.688 | 0.503 | 0.216 | 0.886 | 0.107 | 0.339 | 0.600 | 0.493 | 57.4 | 0.266 | 0.010 |
| b/t44.0 | night castle | 0.532 | 0.490 | 0.839 | 0.583 | 0.310 | 0.855 | 0.143 | 0.326 | 0.594 | 0.451 | 67.2 | 0.469 | 0.005 |
| b/t46.5 | morning field | 0.413 | 0.412 | 0.573 | 0.708 | 0.322 | 0.996 | 0.276 | 0.606 | 0.906 | 0.630 | 55.7 | 0.247 | 0.026 |
| b/t51.0 | inside jar, lamp | 0.304 | 0.287 | 0.465 | 0.490 | 0.263 | 0.843 | 0.210 | 0.395 | 0.677 | 0.468 | 43.9 | 0.068 | 0.096 |
| b/t60.0 | dusk field | 0.435 | 0.448 | 0.595 | 0.638 | 0.298 | 1.000 | 0.268 | 0.503 | 0.859 | 0.591 | 58.7 | 0.309 | 0.029 |
| b/t63.0 | underground cross-section | 0.473 | 0.405 | 0.750 | 0.716 | 0.275 | 1.000 | 0.122 | 0.587 | 0.895 | 0.774 | 72.1 | 0.406 | 0.012 |
| v1/v1_frame20 | v1 office | 0.293 | 0.266 | 0.477 | 0.723 | 0.322 | 1.000 | 0.249 | 0.654 | 0.927 | 0.678 | 49.7 | 0.063 | 0.140 |
| v1/v1_frame45 | v1 office | 0.295 | 0.267 | 0.481 | 0.713 | 0.306 | 1.000 | 0.239 | 0.635 | 0.947 | 0.707 | 50.3 | 0.069 | 0.156 |

Clip-level distribution over all 130 frames each (median, with 25th to 75th percentile in brackets):

| statistic | clip A | clip B | v1 frame20 / frame45 |
|---|---|---|---|
| S mean | 0.483 [0.410-0.576] | 0.405 [0.320-0.500] | 0.293 / 0.295 |
| S p90 | 0.771 [0.647-0.848] | 0.645 [0.573-0.755] | 0.477 / 0.481 |
| V mean | 0.650 [0.584-0.707] | 0.580 [0.476-0.678] | 0.723 / 0.713 |
| luma p5 | 0.141 [0.108-0.169] | 0.142 [0.109-0.192] | 0.249 / 0.239 |
| luma p50 | 0.442 [0.369-0.514] | 0.375 [0.288-0.530] | 0.654 / 0.635 |
| luma p95 | 0.759 [0.680-0.895] | 0.784 [0.669-0.893] | 0.927 / 0.947 |
| contrast (luma p95 - p5) | 0.610 [0.543-0.738] | 0.616 [0.504-0.699] | 0.678 / 0.707 |
| colourfulness (Hasler-Suesstrunk) | 81.8 [62.8-96.0] | 56.0 [45.1-65.2] | 49.7 / 50.3 |
| share of pixels with S > 0.5 | 0.482 [0.323-0.627] | 0.248 [0.173-0.452] | 0.063 / 0.069 |
| share of pixels with S < 0.15 | 0.090 [0.033-0.145] | 0.066 [0.012-0.218] | 0.140 / 0.156 |
| share of pixels with V > 0.95 | 0.035 [0.014-0.088] | 0.045 [0.021-0.088] | 0.066 / 0.073 |
| black point, luma p1 (median) | 0.104 | 0.095 | 0.153 |
| mean colour, darkest 10 % | `#3d1c32` (H 319, S 0.53) | `#392433` (H 318, S 0.37) | `#48392d` (H 26) |
| mean colour, 40-60 % band | `#90646a` | `#7d656d` | `#b5a78d` |
| mean colour, brightest 10 % | `#d1c7c6` | `#dbc5b1` | `#f4eedd` |

### 2.2 Dominant palettes (k-means, k = 8, Lab space)

| frame | scene | k-means palette (k=8, Lab), hex and area share |
|---|---|---|
| a/t02.0 | canyon noon, hero | `#66121c` 34% `#ed7827` 14% `#907b82` 12% `#835557` 11% `#d13418` 11% `#c56240` 9% `#493545` 6% `#d1e2e0` 2% |
| a/t06.0 | canyon + bridge, wide | `#202c97` 22% `#4e75c7` 19% `#464184` 16% `#6b9bdc` 15% `#96afda` 13% `#4d3854` 6% `#b54d86` 5% `#ac8488` 3% |
| a/t09.0 | desert noon, wide | `#e99e56` 26% `#bec3df` 16% `#9eb9e6` 14% `#6fa3e6` 13% `#d2884c` 12% `#eca67b` 9% `#9ca2ce` 9% `#76689e` 2% |
| a/t16.0 | boss low angle, sun in frame | `#adb8e3` 26% `#ddddf0` 19% `#839edd` 15% `#33283d` 15% `#6a4754` 9% `#90747b` 9% `#615387` 5% `#b89031` 3% |
| a/t19.5 | two-shot, noon | `#aabbe4` 25% `#cdcfdf` 19% `#806065` 18% `#3b2b3c` 15% `#574f8b` 14% `#d27750` 4% `#bb912e` 3% `#9641c1` 3% |
| a/t27.5 | train car interior, lamps | `#161a42` 31% `#bb3b14` 15% `#801621` 14% `#582b44` 13% `#421313` 11% `#b80329` 9% `#78653d` 4% `#e9e5e6` 3% |
| a/t34.5 | concourse interior, daylight | `#976c4d` 25% `#683538` 18% `#ac8a74` 15% `#7f5a4f` 13% `#574450` 13% `#8a747d` 8% `#9f9cc5` 7% `#eaddd1` 1% |
| a/t40.0 | macro rail, noon | `#e88a3e` 25% `#c7572c` 19% `#aa827d` 16% `#70211b` 14% `#f6cba5` 12% `#372331` 10% `#4a8960` 2% `#2152d4` 1% |
| a/t45.0 | two-shot by wall | `#c4341f` 23% `#a67d74` 20% `#e1742f` 16% `#ccc5c1` 14% `#e7a25f` 11% `#493d41` 8% `#831f1a` 7% `#9949b5` 1% |
| a/t49.0 | deck, late afternoon | `#22162d` 28% `#5a83d1` 18% `#4b3149` 18% `#7ca5e3` 13% `#9d6f98` 10% `#854553` 9% `#b6bedc` 4% `#c68a8a` 2% |
| a/t55.0 | hero close-up | `#ad8781` 23% `#e47a32` 17% `#b7331e` 14% `#ded1d2` 14% `#eda570` 13% `#44343f` 10% `#75352d` 6% `#3ea693` 2% |
| a/t61.0 | sunset bridge | `#643544` 24% `#cbc0c8` 19% `#eedcc0` 12% `#986f72` 11% `#3a2334` 11% `#d9ab9a` 11% `#c54a44` 6% `#cc774b` 6% |
| b/t03.5 | hall interior (dimmed beat) | `#584f5c` 27% `#3c2d37` 26% `#7f787d` 14% `#714f42` 11% `#24213c` 9% `#26356a` 7% `#c3bfb9` 5% `#cab26a` 1% |
| b/t09.0 | hall interior, orbit | `#221c31` 25% `#433030` 17% `#443d4e` 16% `#75655f` 13% `#74613d` 11% `#b5a280` 9% `#884630` 5% `#dcbe6c` 3% |
| b/t15.0 | army exterior, day | `#cfc7c2` 23% `#aa9fa3` 16% `#62484c` 15% `#d5e2ef` 13% `#867271` 13% `#aac1df` 8% `#9e4a4c` 6% `#666077` 6% |
| b/t22.0 | throne interior | `#6b3723` 20% `#47231f` 18% `#34253f` 18% `#966136` 15% `#af453d` 13% `#f5dbcb` 7% `#d59d53` 6% `#756277` 3% |
| b/t28.0 | city gate, day | `#daccb9` 24% `#c2a06b` 20% `#a09593` 19% `#94734c` 15% `#584c52` 10% `#669cd2` 5% `#a84038` 5% `#799340` 2% |
| b/t31.0 | sunset hill | `#250d23` 23% `#fdbfa0` 17% `#e9767d` 14% `#f59d8c` 13% `#fedb9d` 12% `#612b3c` 8% `#fff7d9` 8% `#d58096` 5% |
| b/t34.0 | night close-up | `#2142a2` 26% `#444a92` 20% `#26285a` 17% `#6d6fcf` 14% `#2d1c30` 9% `#ebd0f3` 6% `#5c4a56` 4% `#a08b91` 4% |
| b/t38.5 | portcullis, night + torches | `#766793` 24% `#43466d` 23% `#593742` 16% `#8f5f5f` 13% `#2f2247` 12% `#556ed3` 6% `#ceaec7` 3% `#d7946a` 3% |
| b/t44.0 | night castle | `#4c4f90` 27% `#7570b4` 20% `#333068` 16% `#2244ad` 15% `#645d81` 8% `#4f2c3e` 6% `#a97057` 4% `#d9b2cf` 4% |
| b/t46.5 | morning field | `#f1b77d` 18% `#777a41` 17% `#ddb292` 16% `#a79c59` 14% `#926e67` 10% `#fbe9bb` 9% `#534643` 9% `#9c6944` 7% |
| b/t51.0 | inside jar, lamp | `#464353` 28% `#907164` 28% `#b48a6a` 14% `#69595b` 11% `#43332f` 8% `#6f5039` 6% `#eccb95` 4% `#cb8642` 2% |
| b/t60.0 | dusk field | `#657339` 25% `#eea27f` 14% `#9a9453` 13% `#f7d3a7` 13% `#b48a77` 10% `#704f4e` 10% `#9f683f` 9% `#464c3d` 6% |
| b/t63.0 | underground cross-section | `#e8aa8e` 26% `#4c215d` 22% `#dc9397` 14% `#fce0b7` 10% `#8b5d53` 10% `#ca6447` 9% `#62667f` 5% `#b04b6e` 4% |
| v1/v1_frame20 | v1 office | `#ddd5ba` 33% `#b89269` 26% `#72563e` 18% `#99bcdc` 7% `#92a184` 6% `#fbf8f4` 6% `#3b3b39` 5% `#eed26f` 1% |
| v1/v1_frame45 | v1 office | `#dcd5b9` 32% `#b08e67` 28% `#72563e` 18% `#92c1c9` 6% `#fbf9f5` 6% `#393937` 5% `#8baae5` 3% `#edd16e` 1% |

### 2.3 Medians by scene group

| scene group (frames) | n | S mean | S p90 | V mean | luma p5 | luma p50 | luma p95 | contrast | colourfulness | share S>0.5 | warm share | cool share |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A interior car (t27-28.5) | 4 | 0.725 | 1.000 | 0.452 | 0.090 | 0.147 | 0.454 | 0.366 | 101.3 | 0.875 | 0.56 | 0.34 |
| A interior car window (t29-30.5) | 4 | 0.577 | 0.773 | 0.375 | 0.109 | 0.193 | 0.583 | 0.476 | 54.2 | 0.747 | 0.77 | 0.11 |
| A concourse (t31.5-35.5) | 9 | 0.395 | 0.630 | 0.586 | 0.177 | 0.423 | 0.902 | 0.725 | 63.0 | 0.273 | 0.72 | 0.14 |
| A noon canyon chars (t0-3.5,t12-21,t37-47,t55-59.5) | 59 | 0.491 | 0.827 | 0.699 | 0.143 | 0.495 | 0.840 | 0.696 | 93.5 | 0.488 | 0.64 | 0.14 |
| A afternoon deck (t47.5-54.5) | 15 | 0.470 | 0.647 | 0.578 | 0.094 | 0.367 | 0.686 | 0.608 | 75.1 | 0.457 | 0.26 | 0.48 |
| A sunset (t60-64.5) | 10 | 0.377 | 0.675 | 0.679 | 0.175 | 0.494 | 0.880 | 0.701 | 62.1 | 0.301 | 0.62 | 0.02 |
| B hall interior (t0-13.5,t18-19.5) | 30 | 0.324 | 0.619 | 0.470 | 0.123 | 0.282 | 0.769 | 0.647 | 42.9 | 0.230 | 0.51 | 0.29 |
| B throne/banquet (t21-26.5) | 12 | 0.563 | 0.775 | 0.444 | 0.101 | 0.246 | 0.790 | 0.683 | 63.3 | 0.679 | 0.73 | 0.15 |
| B day exterior (t14-17.5,t27-29.5) | 14 | 0.282 | 0.560 | 0.698 | 0.207 | 0.680 | 0.907 | 0.699 | 52.8 | 0.148 | 0.28 | 0.16 |
| B sunset/morning (t30-32.5,t46-48.5,t56-61.5) | 24 | 0.416 | 0.607 | 0.681 | 0.269 | 0.571 | 0.852 | 0.601 | 56.0 | 0.230 | 0.90 | 0.00 |
| B night (t33-45.5) | 26 | 0.544 | 0.828 | 0.586 | 0.116 | 0.324 | 0.605 | 0.492 | 68.1 | 0.476 | 0.05 | 0.86 |
| B jar interior (t49-55.5) | 14 | 0.350 | 0.515 | 0.523 | 0.173 | 0.417 | 0.730 | 0.557 | 49.6 | 0.108 | 0.67 | 0.16 |

### 2.4 Lit versus shadow colour for the same surface

| frame | surface pair (lit xy / shadow xy) | lit | shadow | V ratio | linear-luminance ratio | hue lit -> shadow | S lit -> shadow |
|---|---|---|---|---|---|---|---|
| a/t02.0 | orange ground vs head shadow, noon (550,850 / 640,905) | `#d9734d` | `#332d40` | 0.29 | 0.11 | 16 -> 259 | 0.65 -> 0.30 |
| a/t02.0 | canyon wall, sunlit vs self-shadow (100,600 / 600,600) | `#e9671d` | `#781518` | 0.52 | 0.17 | 22 -> 358 | 0.88 -> 0.83 |
| a/t34.5 | wood floor vs building shadow (400,1000 / 350,660) | `#ac825e` | `#525065` | 0.59 | 0.33 | 28 -> 246 | 0.45 -> 0.21 |
| a/t34.5 | wood floor vs character shadow (250,740 / 60,712) | `#a57860` | `#444153` | 0.50 | 0.25 | 21 -> 250 | 0.42 -> 0.22 |
| a/t32.5 | wood floor vs character shadow (250,1000 / 640,1060) | `#946645` | `#252432` | 0.34 | 0.12 | 25 -> 244 | 0.53 -> 0.28 |
| a/t16.0 | sleeper top vs shaded side (160,1135 / 180,1160) | `#997c77` | `#6c5663` | 0.71 | 0.48 | 9 -> 325 | 0.22 -> 0.20 |
| a/t53.0 | deck vs umbrella shadow, late afternoon (520,850 / 650,760) | `#9d5975` | `#475895` | 0.95 | 0.67 | 335 -> 227 | 0.43 -> 0.52 |
| a/t49.0 | deck vs umbrella shadow (far) (450,560 / 450,505) | `#9d6e9b` | `#7170ad` | 1.10 | 0.88 | 303 -> 241 | 0.30 -> 0.35 |
| b/t00.0 | jar, lit vs shade (cel step) (460,850 / 620,850) | `#a2a2a4` | `#757482` | 0.79 | 0.49 | 240 -> 244 | 0.01 -> 0.11 |
| b/t46.5 | jar, lit vs shade, morning (500,900 / 690,900) | `#9b7b68` | `#4f414f` | 0.51 | 0.27 | 22 -> 300 | 0.33 -> 0.18 |
| b/t46.5 | grass vs frog shadow (550,1180 / 470,1065) | `#878d4c` | `#607640` | 0.84 | 0.64 | 66 -> 84 | 0.46 -> 0.46 |
| b/t28.0 | tower, sunlit vs shade side (20,450 / 120,450) | `#e3d3b9` | `#bcb2b1` | 0.83 | 0.69 | 37 -> 5 | 0.19 -> 0.06 |
| b/t28.0 | road vs contact shadow under feet (520,925 / 565,921) | `#cba66f` | `#4e3225` | 0.38 | 0.10 | 36 -> 19 | 0.45 -> 0.53 |
| b/t41.5 | night floor vs character shadow (150,1000 / 390,1010) | `#85588f` | `#412c5a` | 0.63 | 0.26 | 289 -> 267 | 0.38 -> 0.51 |
| b/t31.0 | cloud, lit vs underside, sunset (550,225 / 560,180) | `#fcd5b1` | `#ca6a9c` | 0.80 | 0.35 | 29 -> 329 | 0.30 -> 0.48 |
| v1_frame20 | v1 desk top vs desk front (150,790 / 100,850) | `#866a4e` | `#523a25` | 0.61 | 0.31 | 30 -> 28 | 0.42 -> 0.55 |
| v1_frame20 | v1 floor near vs far (360,1200 / 450,920) | `#c59c71` | `#90704e` | 0.73 | 0.49 | 31 -> 31 | 0.43 -> 0.46 |
| v1_frame20 | v1 head centre vs head edge (260,560 / 370,610) | `#ffffff` | `#9f968c` | 0.62 | 0.31 | 0 -> 32 | 0.00 -> 0.12 |

### 2.5 Sky gradient stops (top to horizon) and haze

| frame | treatment | stops, top to horizon |
|---|---|---|
| a/t49.0 (x 420) | afternoon | `#4a78cd` y20, `#4d81d5` y100, `#5e92e5` y180, `#6ea0e8` y260, `#7eabe9` y340, `#92b7e7` y365 |
| a/t16.0 (x 620) | noon, looking up | `#878ec2` y30, `#8f9ed5` y150, `#94a9e7` y300, `#87a3eb` y450, `#6c9eeb` y600, `#7caee9` y740 |
| a/t06.0 (x 300) | canyon noon | `#386ec9` y20, `#4278d2` y60, `#7d97d3` y100, `#a8b5da` y140 |
| a/t61.0 (x 620) | sunset | `#bdb0b8` y20, `#c4bbc8` y100, `#d7cad1` y200, `#eee4cf` y300, `#f2d8ab` y380, `#e5c1b2` y425 |
| b/t28.0 (x 300) | day | `#5795d0` y10, `#5b9bd8` y50, `#669ed2` y90, `#91a1bb` y125 |
| b/t17.0 (x 200) | day, balcony | `#9acaf4` y100, `#b6dffd` y200, `#c6e9ff` y300, `#d7f1fa` y400 |
| b/t31.0 (x 200) | sunset | `#e16c7e` y20, `#f27f82` y120, `#ff9f8c` y240, `#fdad89` y330, `#ffc08d` y420, `#ffdc99` y520 |
| b/t46.5 (x 300) | sunrise | `#f2b074` y20, `#f9bd84` y100, `#f8be92` y180, `#fccca6` y260 |
| b/t34.0 (x 620) | night | `#1a3b92` y60, `#1c44a8` y150, `#1748ae` y250, `#204c8f` y350 |
| b/t44.0 (x 300) | night | `#1e2e7b` y10, `#1f2f7a` y40, `#202f7a` y70 |

Haze samples: see 1.4. Rule of thumb from them: mid distance mixes 30 to 50 % towards the horizon colour, the farthest layer 90 to 100 %.

### 2.6 Bloom, radial profiles (display luma)

| source | frame, centre | core radius (luma > 0.95) | radius at 50 % / 25 % / 10 % of excess | halo colours outward |
|---|---|---|---|---|
| ceiling lamp | a/t27.5 (85, 265) | 32 px | 36 / 40 / 56 px | `#d7a273`, `#975937`, `#7a3a2e` |
| small lamp | a/t27.5 (605, 385) | 16 px | 20 / 24 / 28 px | `#d7b49f`, `#6b3a3b` |
| street lamp | a/t61.0 (50, 508) | 8 px | 12 / 16 / 20 px | `#ffe1ac`, `#e2975f`, `#bc614b` |
| sun, noon | a/t16.0 (150, 330) | 68 px | 120 / 192 / 260 px | `#fefeff`, `#edebf7`, `#dcdbf3` |
| torch flame | b/t38.5 (517, 410) | 8 px | 28 / 32 / 40 px | `#ffeba4`, `#ffc76a`, `#feae56`, `#be7b50` |
| moon | b/t44.0 (83, 180) | disc 36 px | 36 / 56 / 84 px | `#c1d5ff`, `#5a8af5`, `#427af3`, `#275ad6` |
| glowing crack | b/t63.0 (355, 1010) | 16 px | 88 / 112 / 136 px | `#fff4c7`, `#fcd8b6`, `#f79893`, `#d25f7a` |
| lamp in jar | b/t51.0 (705, 140) | 8 px | 60 / 96 / 108 px | `#cdb4a2`, `#b49984`, `#947f76` |

### 2.7 Other measured quantities

| quantity | value | evidence |
|---|---|---|
| scene black floor (luma p0.5) versus caption black | 0.087 (A), 0.079 (B) versus 0.001 | all 260 frames, caption band y 860..950 |
| share of pixels below luma 0.04 | 0.12 % (A), 0.15 % (B) | all frames |
| head fill, clip A | `#fdf7f7`, `#fcf8f5`, `#fdf8f5`, `#faf9f5`, `#fef8f8` | a/t16.0, a/t27.5, a/t29.5, a/t53.0, a/t02.0 |
| head fill, clip B | `#f8f9fb` hall, `#faf8f3` day, `#faded0` throne, `#fbdaf7` night, `#fff5f3` sunset | b/t04.5, b/t17.0, b/t22.0, b/t34.0, b/t31.0 |
| head flatness, clip A | V 0.98-0.99 across the fill; rim falloff 7 % luma over 14 px | a/t16.0 row y 560, x 284..300 |
| ink line colour | `#251921`, `#34201d`, `#302535`; luma 0.10-0.18 | a/t45.0, a/t02.0, a/t16.0 |
| shadow edge width (10-90 %) | 4, 6, 9, 12, 21 px | a/t34.5, a/t02.0, a/t53.0 |
| surface detail (luma std, high-pass sigma 12) | wood floor 0.086, canyon wall 0.037, ballast 0.131, deck 0.140, quilt 0.082, wallpaper 0.037, stone wall 0.126, grass 0.093, plum wall 0.031; navy carpet 0.001 | a/t34.5, a/t02.0, a/t16.0, a/t53.0, b/t22.0, b/t28.0, b/t46.5, a/t27.5 |
| surface detail, v1 | wall 0.0018, floor 0.0017, wainscot 0.0021 | v1_frame20 |
| background blur behind close-ups (B) | Laplacian energy 6.5 versus 135 sharp; sigma about 5 to 7 px | b/t04.5 versus b/t09.0 |
| vignette | 0 to 5 % | a/t08.0, b/t59.0, mean images |
| grain | below 0.5 8-bit levels spatial, below 0.3 temporal | a/t16.0, a/t49.0, b/t59.0, b/t28.0 (8 consecutive frames each) |
| source encode | 720x1280, 30 fps, H.264 yuv420p bt709; 1.97 Mbit/s (A), 1.14 Mbit/s (B) | ffprobe |

---

## 3. How to reproduce (Blender 5.3 bpy, Cycles CPU)

### 3.1 The five rules that carry the look

1. Design every large surface as a saturated mid-dark colour (S 0.45 to 0.9, V 0.30 to 0.75 as displayed). Nothing large may be paler than V 0.80 except the sky.
2. Light with a hard yellow key plus a flat blue-violet ambient that add up to white. Shadows then come out blue-violet on their own.
3. Keep characters unlit and flat: emission cut-outs with a `#fcfafa` head fill, plum ink, casting hard shadows but receiving none.
4. Let only real emitters exceed scene-linear 1.0, and bloom only those.
5. Finish with a light grade: plum-lifted black, slightly warm highlights, +12 % saturation. No grain, no sharpening, no meaningful vignette.

### 3.2 Colour management and render settings

| setting | value | why |
|---|---|---|
| view transform | `Standard` | the reference keeps bright colours fully saturated (`#e9671d`, `#ff9f8c`); AgX and Filmic desaturate them. Available in this build: Standard, Filmic, AgX, Khronos PBR Neutral, ACES 2.0, ACES 1.3 |
| look | `None` | contrast comes from the scene, the measured contrast (0.61) is not higher than v1's (0.68) |
| exposure / gamma | 0.0 / 1.0 | |
| display device | sRGB | |
| Cycles | CPU, 24 samples, adaptive sampling on, OpenImageDenoise on, `max_bounces` 1, `diffuse_bounces` 0, `glossy_bounces` 1, `transmission_bounces` 0, `volume_bounces` 0, `transparent_max_bounces` 8, caustics off, `sample_clamp_indirect` 3 | the ambient is emission and diffuse bounces are off, so only direct sun and lamp light is sampled and the emission ambient is not counted twice; this is why 24 samples are enough on 4 cores |
| film | not transparent; default pixel filter (1.5 px) | no sharpening in the reference |
| compositor | CPU device; node group from `grade_compositor.build(scene)` | 0.3 to 0.4 s per 720x1280 frame, one thread |

`lightkit_clp.setup_render(scene)` applies all of the above.

### 3.3 Lighting model and presets

Model, in scene-linear values with the Standard transform:

    displayed = albedo x (A + K x cos(angle to key) x visibility)

- `A` is the flat ambient colour. It is injected as emission in every environment material (emission colour = albedo x A, strength 1), so shadows are exactly `albedo x A`, with no noise and no dependence on room geometry. The world is black with strength 0.
- `K` is the key factor on a surface that faces the light. For a Sun light: `energy = pi x max(K)`, `color = K / max(K)`. A floor receives `K x sin(elevation)`.
- For a point lamp that should add `g x albedo` on a facing surface at distance d metres: `energy = g x 4 x pi^2 x d^2` watts.
- The two photometric formulas are the standard Cycles conventions as I understand them; they were not verified by a render in this pass. First test render: put a white card (albedo 1.0) facing the sun, with ambient off; it must read scene-linear `max(K)` on the brightest channel. Scale the energy if it does not.

Presets (in `lightkit_clp.PRESETS`; `lightkit_clp.apply_preset(scene, name)` sets render settings, black world and the sun):

| preset | ambient A (linear RGB) | key K (linear RGB) | sun energy, colour | sun elevation | sun angle (softness) | shadow / lit luminance | head fill as displayed | modelled on |
|---|---|---|---|---|---|---|---|---|
| `INTERIOR_DAY` | (0.42, 0.40, 0.56) | (0.70, 0.54, 0.15) | 2.20, (1.00, 0.77, 0.21) | 38 deg | 1.5 deg | 0.43 | `#fbf7f5` | a/t32.5, a/t34.5, shade ratio of b/t00.0 |
| `INTERIOR_LAMP` | (0.20, 0.16, 0.30) | none; lamps (1.00, 0.69, 0.31) x 0.9 | no sun | - | lamp radius 0.05 m | 0.21 | `#fbf4ee` | a/t27.5, b/t22.0, b/t23.0 |
| `EXTERIOR_NOON` | (0.10, 0.21, 0.79) | (0.90, 0.79, 0.21) | 2.83, (1.00, 0.88, 0.23) | 50 deg | 1.5 deg | 0.23 | `#fcf8f6` | a/t02.0, a/t34.5 pairs |
| `LATE_AFTERNOON` | (0.20, 0.45, 0.95) | (0.85, 0.50, 0.10) | 2.67, (1.00, 0.59, 0.12) | 20 deg | 1.5 deg | 0.44 | `#faf9f5` | a/t49.0, a/t53.0 |
| `SUNSET` | (0.35, 0.25, 0.45) | (0.80, 0.44, 0.20) | 2.51, (1.00, 0.55, 0.25) | 8 deg | 2.5 deg | 0.36 | `#fff5f3` | a/t61.0, b/t31.0 |
| `NIGHT` | (0.12, 0.13, 0.45) | (0.33, 0.35, 0.75) | 2.36, (0.44, 0.47, 1.00) | 45 deg | 1.5 deg | 0.29 | `#fbdaf7` | b/t34.0, b/t41.5, b/t44.0 |

Notes on the presets:

- `EXTERIOR_NOON`: the ambient is the mean ambient-to-lit ratio of three clip A pairs (`a/t34.5`, `a/t32.5`, `a/t02.0`; per channel 0.05 to 0.20 red, 0.13 to 0.36 green, 0.53 to 1.16 blue). `INTERIOR_DAY` raises the ambient towards the clip B hall shade ratio (0.51, 0.49, 0.62 of lit, `b/t00.0`), because most of a room is ambient-lit and must stay readable. `LATE_AFTERNOON`, `SUNSET` and `NIGHT` are fitted to two or three pairs each and should be treated as starting points.
- Key direction: from camera-left, above, slightly behind the camera. The kit's `az = -55` gives a travel direction of (0.65, 0.45, -0.62) for a camera looking along +Y: shadows fall to screen right and away from the camera. For the office, aim the sun through the window so that a hard patch lands on the floor and the lower wall.
- Sun angle 1.5 degrees gives an 11 px penumbra for an occluder 2 m from the receiver at about 205 px per metre, inside the measured 4 to 21 px. v1 used 8 degrees, which is too soft.
- Lamps: an emissive bulb (`emissive_material`, colour `#fffeec`, strength 8) for the visible glow plus a point light for the pool, `add_lamp(scene, location, (1.0, 0.69, 0.31), gain 0.9, distance)`. At 1.2 m this is 51 W.
- Storm or rain: the reference has no such scene. Extrapolation, not measurement: use `NIGHT` with the saturation of A reduced by about a third, and for lightning multiply A by 3 with colour (0.80, 0.85, 1.00) for 2 to 3 frames.
- Brightness dip beat (optional, 1.3): animate the grade, value x0.75 for 0.4 s.

### 3.4 Materials

Environment (`lightkit_clp.env_material(name, albedo_hex, A, image=None, ao=False, gloss=0.0)`):

    albedo (flat colour or sRGB image texture) -> Diffuse BSDF, roughness 1.0 ----------------+
    albedo -> Mix (Multiply, factor 1) with A -> [optional x AO, factor 0.6] -> Emission, 1.0 -+-> Add Shader -> Surface
    optional: Mix Shader with Glossy BSDF (roughness 0.25) at factor 0.1 to 0.3 for brass, rails, polished wood

- Use Diffuse, not Principled with specular: the reference surfaces are matte, with a narrow highlight only on metal (rail in `a/t19.5`, hat in `a/t16.0`).
- Every large surface needs a texture or drawn pattern with local luma detail of 0.03 to 0.10 (planks, panel lines, wallpaper motif, grain). Draw it in SVG and rasterise it; a flat colour fails the target in 3.8, row 18.
- Optional `ao=True` multiplies the ambient by Cycles ambient occlusion (distance 0.5 m, 8 samples, factor 0.6) for soft contact darkening in corners.

Emitters (`emissive_material(name, hex, strength)`): bulbs and flames strength 8 (colours `#fffeec`, `#ffeba4`); a window pane showing bright sky strength 1.0 to 1.5 with a gradient texture (no bloom below 1.0); a window in direct sun strength 3.

Characters (`character_material(name, image, tint)`):

    image colour x tint -> Emission, strength = Light Path "Is Camera Ray" --+
    Transparent BSDF --------------------------------------------------------+-> Mix Shader (factor = image alpha) -> Surface

- Drawn colours appear exactly as authored before the grade; the character adds no light to the set; the opaque part still blocks the sun, which gives the hard cast shadow of clip A.
- Head fill in the artwork: `#fcfafa` (scene-linear maximum 0.973, below the bloom threshold). Through the default grade it displays `#fcf7f6` (compositor run), against the measured `#fcf8f6`.
- Ink: `#2b1e2a` in the artwork (measured range `#251921` to `#302535`), never `#000000`; through the grade it displays `#322032`.
- Optional soft inner rim on the head: darken by 7 % within 8 % of the head diameter of the outline.
- Per-shot tint (clip B behaviour), optional, multiplied onto the whole character. Compositor-checked values for the head: night lilac (0.97, 0.76, 0.98) displays `#f9d9f6` (measured `#fbdaf7`); night pink (0.99, 0.70, 0.82) displays `#f8cddf` (measured `#fcc8d9`); warm throne room (0.98, 0.80, 0.74) displays `#f5dbd2` (measured `#faded0`). Clip A uses no tint.
- Shadow from the character: the cut-out's own sun shadow is enough when the key is 30 to 60 degrees off the camera axis. If the plane is edge-on to the sun and the shadow becomes a thin line, add a contact ellipse under the feet: width 0.75 of the body width, colour `#252432`, opacity 0.6, edge feather 20 px.

Proposed office palette. Albedos were chosen so that the ambient-lit colour lands on a measured reference colour; the displayed columns were computed by pushing `albedo x light` through the real compositor grade in Blender 5.3 (`PROJ/ref/crops/color/palette_predicted.json`). "Facing the sun" uses the full K; "floor in sun patch" uses 0.62 K.

| material | base colour (albedo) | albedo linear RGB | DAY ambient-lit | DAY facing the sun | DAY floor in sun patch | LAMP ambient | LAMP under lamp |
|---|---|---|---|---|---|---|---|
| wall plaster (mauve) | `#bb9284` | (0.497, 0.286, 0.232) | `#7e5a62` | `#c48361` | `#ad7561` | `#5a384b` | `#c17553` |
| wainscot / doors walnut | `#a05730` | (0.350, 0.096, 0.030) | `#6c2d19` | `#a74100` | `#943a00` | `#4e1b1b` | `#a63700` |
| floor navy-plum | `#423d60` | (0.055, 0.046, 0.116) | `#2c214b` | `#483953` | `#403151` | `#21133a` | `#48344c` |
| desk top wood | `#cc8a4e` | (0.605, 0.256, 0.076) | `#8a522b` | `#d77700` | `#bf6b04` | `#633326` | `#d46900` |
| desk side dark wood | `#6c3a2b` | (0.150, 0.042, 0.024) | `#4b2023` | `#742d17` | `#67281c` | `#371420` | `#732610` |
| brass | `#f6d15c` | (0.920, 0.635, 0.106) | `#a8852f` | `#ffc300` | `#e6ae00` | `#795629` | `#ffaf00` |
| map paper cream | `#f6f6d0` | (0.920, 0.920, 0.628) | `#a8a29f` | `#ffeda5` | `#e6d4a2` | `#796a79` | `#ffd791` |
| map sea | `#a5def6` | (0.378, 0.729, 0.920) | `#628cbc` | `#aad7d1` | `#95bfca` | `#455990` | `#aac5be` |
| cabinet steel-violet | `#8392ba` | (0.227, 0.286, 0.490) | `#51578f` | `#8a8b9f` | `#787b99` | `#39356d` | `#898091` |
| lamp shade green | `#4ab979` | (0.068, 0.487, 0.191) | `#237a5a` | `#37b35a` | `#31a15b` | `#205047` | `#3da553` |
| frames dark plum | `#513d54` | (0.082, 0.046, 0.089) | `#382343` | `#583849` | `#4f3248` | `#291635` | `#573141` |
| red accent | `#e64445` | (0.792, 0.058, 0.059) | `#9c0011` | `#f20000` | `#d70000` | `#710019` | `#ee0000` |
| white paper | `#f6f6e9` | (0.920, 0.920, 0.815) | `#a49eb0` | `#ffebbd` | `#e4d1b9` | `#766787` | `#ffd5a9` |

Composition targets by area, taken from the four reference interiors: about 30 % dark cool (navy, plum: floor, deep shade, frames), 35 to 45 % warm mid-tones (wood, mauve plaster, red), about 10 % brass or tan accents, at most 8 % near-white (heads, the lit part of the map, lamps). Light paper and the map only reach cream (`#e4d1b9` to `#ffebbd`, against the measured sunlit sheet `#e9d6bb`) where the sun patch or a lamp pool hits them; in ambient they are lavender-grey `#a49eb0`, which is what keeps the heads the brightest thing in frame. Paper held by a character is part of the unlit cut-out and stays cream `#fcf4e1`.

### 3.5 Sky, backdrops and haze

- Sky: an emission plane or a window backdrop with an SVG `linearGradient`, top to horizon. Day: `#4a78cd` 0 %, `#5e92e5` 45 %, `#7eabe9` 85 %, `#92b7e7` 100 %. Sunset: `#bdb0b8` 0 %, `#d7cad1` 45 %, `#eee4cf` 70 %, `#f2d8ab` 90 %, `#e5c1b2` 100 %. Night: `#1e2e7b` 0 %, `#1748ae` 60 %, `#204c8f` 100 %. Clouds: soft white shapes at 60 to 80 % opacity with a 6 px blur.
- Haze: bake it into painted backdrop layers instead of volumes (volumes are slow and noisy on CPU). Mix each distance layer towards the horizon colour: nearest backdrop 0 %, mid 40 %, far 90 %, and raise V while lowering S as in 1.4.
- Sun glare when the disc is in frame: a radial-gradient emission card, white core 68 px radius at 720 px width, falling to 50 % at 120 px and 10 % at 260 px, additive.
- Light shafts (optional): two or three additive gradient quads from the window, 5 to 10 % opacity, warm cream `#fae7cc`.

### 3.6 Compositor chain

Built by `grade_compositor.build(scene)`; pass `image=` to grade an existing image. Blender 5.3 node properties are sockets; Color Balance sockets share names and are set by index in the file.

| step | node | parameters |
|---|---|---|
| 1 | Render Layers | - |
| 2 | Glare | Type `Bloom`, Quality `High`, Threshold 1.0, Smoothness 0.1, Size 0.05, Strength 0.5, Saturation 1.0, Tint (1.00, 0.92, 0.80) |
| 3 | Color Balance | Type `Offset/Power/Slope (ASC-CDL)`; Offset colour (0.0075, 0.0035, 0.0095) with offset basis 0; Power 1.0; Slope colour (1.000, 0.985, 0.970) |
| 4 | Hue/Saturation/Value | Saturation 1.12, Hue 0.5, Value 1.0 |
| 5 (optional) | Ellipse Mask, Size (0.80, 0.80) -> Blur, Gaussian 260 px -> Math Multiply Add (x 0.04, + 0.96) -> Mix (Multiply, factor 1) | linear corner factor 0.96; display luma at the corner x0.982. Set `vignette_strength` 0 to disable |
| 6 | Group Output | - |

Validation runs (compositor only, Blender 5.3.0, measured from the written PNGs):

| test | result |
|---|---|
| black, linear 0.0 | `#150919` (luma 0.05, plum) |
| greys, linear 0.02 / 0.05 / 0.18 / 0.50 / 0.90 | `#2e2930` / `#444144` / `#787677` / `#bdbbba` / `#f4f2f1` |
| emitter discs of radius 8 / 16 / 32 px, linear (8, 7, 4), on linear 0.15 | 10 % halo radius 18 / 32 / 50 px (reference 20 / 28 / 56 px); 50 % radius 10 / 20 / 36 px (reference 12 / 20 / 36 px) |
| head-coloured disc, linear (0.955, 0.93, 0.915) | displays `#f7f1ee`; ring just outside equals the background (no bloom on heads) |
| artwork colours through the grade | head `#fcfafa` -> `#fcf7f6`; ink `#2b1e2a` -> `#322032`; cream paper `#fcf4e1` -> `#fef2dc`; bulb `#fffeec` at strength 8 -> `#ffffff` |
| Glare `Bloom` Size sweep at Strength 1.0, emitter radius 32 px | Size 0.05: 10 % at 56 px; 0.10: 74 px; 0.20 and above: 92 px. Use Size 0.20, Strength 1.0 for the larger painted glow of clip B (moon: 84 px) |
| Glare `Fog Glow` | too tight at every size tested (10 % at 34 to 48 px for the 32 px emitter) and 3 to 4 times slower; not recommended |
| cost | 0.10 s for Glare alone, 0.27 to 0.37 s for the full chain, per 720x1280 frame, one thread |
| applied to v1_frame20 / frame45 | S mean 0.293 -> 0.341 and 0.295 -> 0.342; luma p50 0.654 -> 0.622 and 0.635 -> 0.605; colourfulness 49.7 -> 57.7 and 50.3 -> 58.4. The grade alone does not reach the targets |

Depth of field: off by default (clip A behaviour). For close-ups in the clip B manner, render the set and the characters as separate view layers and blur only the set with a Blur node, Gaussian, 6 px, before Alpha Over. Do not use camera depth of field in Cycles for this; it adds noise.

### 3.7 ffmpeg fallback grade

Use these only when the compositor cannot be used. They work on display-referred frames.

`ffmpeg_grade_finish.txt`, equivalent of steps 3 and 4 (black becomes `#140a1b`; on v1 it gives S mean 0.358, colourfulness 61):

    format=gbrp,curves=r='0/0.085 0.3/0.305 1/1':g='0/0.045 0.3/0.30 1/0.99':b='0/0.10 0.3/0.31 1/0.975',eq=saturation=1.25,format=rgb24

`ffmpeg_grade_finish_bloom.txt`, the same plus bloom. The threshold is 0.985 because an 8-bit frame cannot separate a white head from a lamp otherwise: with the threshold at 0.86 the v1 heads and papers glowed. It needs heads at or below `#faf6f3` and emitters at 255. Measured halo: 10 % radius 18 / 26 / 44 px for 8 / 16 / 32 px emitters.

    format=gbrp,split[b][h];[h]curves=all='0/0 0.985/0 1/1',gblur=sigma=8:steps=3,lutrgb=r='clip(val*10,0,255)':g='clip(val*9.2,0,255)':b='clip(val*8,0,255)'[g];[b][g]blend=all_mode=screen,curves=r='0/0.085 0.3/0.305 1/1':g='0/0.045 0.3/0.30 1/0.99':b='0/0.10 0.3/0.31 1/0.975',eq=saturation=1.25,format=rgb24

`ffmpeg_grade_rescue.txt`, a strong split-tone for footage that came out pale. On v1 it reaches S mean 0.53, colourfulness 85, luma p50 0.57, darkest-tenth hue 344, but the frame turns orange and the heads are still shaded spheres. It is not a substitute for the palette and lighting changes.

    format=gbrp,colorbalance=rs=0.06:gs=-0.04:bs=0.14:rm=0.03:gm=-0.03:bm=0.02:rh=0.03:gh=0.0:bh=-0.05,curves=all='0/0 0.25/0.17 0.5/0.40 0.75/0.70 1/1',curves=r='0/0.085 0.3/0.305 1/1':g='0/0.045 0.3/0.30 1/0.99':b='0/0.10 0.3/0.31 1/0.975',eq=saturation=1.45,format=rgb24

Usage: `ffmpeg -i in.mp4 -filter_complex "$(cat ffmpeg_grade_finish.txt),format=yuv420p" -c:v libx264 -crf 16 -c:a copy out.mp4`. Apply the grade before the captions are burned in, so the caption keeps true black and white. The bloom chain was also run inside a real x264 encode (15 frames) without error.

### 3.8 Numeric targets, reference versus v1

Re-measure with `python3 PROJ/spec/measure_color.py --palette frame.png` (rows 1 to 15), and with the stated sampling for rows 16 to 21. Targets are for interior shots of the new clip, set from the four reference interior groups and the clip quartiles. "Interiors" lists the group medians in this order: A train car (`a/t27.0`-`t28.5`), B throne room and banquet (`b/t21.0`-`t26.5`), A concourse (`a/t31.5`-`t35.5`), B hall (`b/t00.0`-`t13.5`, `b/t18.0`-`t19.5`).

| # | quantity | reference | v1 (frame20 / frame45) | target |
|---|---|---|---|---|
| 1 | S mean | interiors 0.725, 0.563, 0.395, 0.324; clip medians 0.483 (A), 0.405 (B) | 0.293 / 0.295 | 0.40 to 0.60 |
| 2 | S p90 | interiors 1.000, 0.775, 0.630, 0.619 | 0.477 / 0.481 | at least 0.62 |
| 3 | V mean | interiors 0.452, 0.444, 0.586, 0.470 | 0.723 / 0.713 | 0.44 to 0.60 |
| 4 | luma p5 | interiors 0.090, 0.101, 0.177, 0.123 | 0.249 / 0.239 | 0.09 to 0.18 |
| 5 | luma p50 | interiors 0.147, 0.246, 0.423, 0.282 | 0.654 / 0.635 | 0.22 to 0.45 |
| 6 | luma p95 | interiors 0.454, 0.790, 0.902, 0.769 | 0.927 / 0.947 | 0.75 to 0.92 |
| 7 | contrast, luma p95 - p5 | interiors 0.366, 0.683, 0.725, 0.647 | 0.678 / 0.707 | 0.60 to 0.75 |
| 8 | colourfulness | interiors 101.3, 63.3, 63.0, 42.9; clip medians 81.8, 56.0 | 49.7 / 50.3 | 55 to 100 |
| 9 | share S > 0.5 | interiors 0.875, 0.679, 0.273, 0.230 | 0.063 / 0.069 | at least 0.25 |
| 10 | share S < 0.15 | interiors 0.028, 0.081, 0.118, 0.201 | 0.140 / 0.156 | at most 0.12 |
| 11 | share V > 0.95 | 0.035 (A), 0.045 (B) | 0.066 / 0.073 | 0.02 to 0.09, heads, lit paper and lamps only |
| 12 | black point, luma p1 | 0.104 (A), 0.095 (B) | 0.153 / 0.153 | 0.08 to 0.12 |
| 13 | mean colour of darkest 10 % | `#3d1c32`, `#392433`; hue 318-319, S 0.37-0.53 | `#4a3a2d` / `#47382c`; hue 26 | hue 250 to 345, S at least 0.35 |
| 14 | mean colour of 40-60 % band | `#90646a`, `#7d656d` | `#b8a98e` / `#b2a58c` | hue 330 to 25 or 230 to 290; V 0.40 to 0.60 |
| 15 | largest palette cluster | dark saturated, 20 to 31 % (`#161a42`, `#6b3723`, `#221c31`, `#976c4d`) | `#ddd5ba` 33 % / `#dcd5b9` 32 % | V at most 0.65 and S at least 0.35 |
| 16 | head fill, sampled at the head centre | `#fcf8f6` typical; V 0.98-1.00, S 0.02-0.04 | `#ffffff` | V 0.97 to 0.995, S at most 0.04, not clipped |
| 17 | head flatness, centre versus 10 px inside the outline | V difference at most 0.07 | V 1.00 versus 0.62 (`#9f968c`) and 0.56 (`#8e7f6e`) | V difference at most 0.07 |
| 18 | surface detail, luma std after high-pass sigma 12, on a 120 px patch of wall and of floor | 0.03 to 0.14 | 0.0018 and 0.0017 | 0.03 to 0.10 |
| 19 | cast shadow on a warm floor, shadow versus lit | hue 244-259 against 16-28; V ratio 0.29-0.59; linear luminance ratio 0.11-0.33 | desk shadow on floor: hue 31 against 31, V ratio 0.91 | hue 230 to 270; V ratio 0.35 to 0.60; a character shadow must be visible |
| 20 | shadow edge width, 10-90 % | 4 to 21 px | not measurable, no hard shadow in frame (sun angle 8 degrees) | 6 to 20 px |
| 21 | bloom around a lamp, 10 % radius minus core radius | 12 to 24 px (A) | none in frame | 12 to 24 px; none around heads |
| 22 | grain / sharpening / vignette | none / none / 0 to 5 % | none / none / none | none / none / at most 5 % |

Calibration loop for the builder: render one still at 50 % size, run `measure_color.py --palette`, and correct in this order: (a) rows 15, 5, 3 with albedos (darker, more saturated walls and floor), (b) rows 19 and 13 with the ambient colour A, (c) rows 16, 17 with the character material, (d) rows 1, 8, 12 with the compositor Saturation (1.05 to 1.25) and Offset.

---

## 4. Differences versus v1, ranked by visual impact

1. Palette and tonal placement. v1 is 59 % pale cream and tan (`#ddd5ba` 33 %, `#b89269` 26 %), mid-luma 0.65, saturation mean 0.29. The reference interiors are led by a dark saturated colour (20 to 31 %), mid-luma 0.15 to 0.42, saturation mean 0.32 to 0.73. This single difference accounts for most of the mismatch: 6.3 % of v1 pixels exceed S 0.5 against 25 to 48 % in the reference. Fix: palette in 3.4.
2. Characters are lit 3D spheres. The v1 head runs from clipped `#ffffff` to `#9f968c` at the edge (V 1.00 to 0.62) with a grey terminator; the reference head is a flat `#fcf8f6` in every light (V range at most 0.07). Fix: unlit emission cut-outs, 3.4.
3. Shadow colour. v1 shadows keep the surface hue (desk top to front: hue 30 to 28; floor shadow: hue 31 to 31) and are brown. Reference shadows swing to blue-violet (hue 244 to 259 on warm surfaces) and the darkest tenth of the frame averages plum `#3d1c32` instead of brown `#48392d`. Fix: yellow key plus blue-violet emission ambient, 3.3.
4. No hard cast shadows. v1's sun has an 8 degree angle and a 250 W area fill, so nothing in frame has a crisp shadow, and the characters cast no readable shadow on the floor (V ratio 0.91). The reference has 4 to 21 px edges and unmistakable character shadows (`a/t32.5`, `a/t34.5`). Fix: sun angle 1.5 degrees, no fill light, sun aimed through the window.
5. Flat untextured surfaces. v1 wall and floor detail is 0.002 against 0.03 to 0.14. Fix: SVG textures on every large surface.
6. Mid-tones and whites are too high. v1 luma p5 0.25, p50 0.65, p95 0.93, and 7 % of the frame is above V 0.95 including clipped heads and papers. Reference interiors: p5 0.09 to 0.18, p50 0.15 to 0.42, and near-white is confined to heads, lit paper and lamps. Fix: ambient 0.40 to 0.56 instead of a 0.6 grey-blue world plus fill, and albedos from 3.4.
7. No emitters, no bloom. The v1 lamp glow is off screen and nothing exceeds 1.0 in a controlled way. The reference shows lamps with a 12 to 24 px warm halo in every lamp-lit shot. Fix: emissive bulbs at strength 8 and the Glare node, 3.6.
8. No grade. v1 is the raw Standard output: black point 0.153 with a brown tint. Reference: 0.08 to 0.12, plum. Fix: compositor steps 3 and 4. This is small next to items 1 to 4: the grade alone moves v1's saturation mean only from 0.29 to 0.34.
9. Ink colour. v1 lines and limbs are near-neutral (`#2e2b2b`, material 0.02 grey); the reference ink is plum (`#251921` to `#302535`). Small, but it shifts the dark-tone hue.
10. No distance or atmosphere cues (window sky gradient, sun patch, light shaft). Minor for an interior, needed for any exterior shot.

Not a difference: overall luma contrast (v1 0.68 to 0.71 against 0.61 median), grain, sharpening and vignette. Do not add contrast, grain or a strong vignette.

---

## 5. Limits and things that could not be determined

- The sources are heavily compressed (1.1 and 2.0 Mbit/s). Fine grain, subtle chromatic aberration or dithering, if any existed, cannot be detected. Chroma subsampling also bleeds colour into thin ink lines, so ink colours are accurate to about 10 levels.
- Vignette could not be separated from picture content; the 0 to 5 % figure is an upper bound from a few flat regions.
- Sun elevations are estimates from shadow lengths (about 50 degrees at noon in `a/t02.0`, low sun in `a/t34.5`); the camera geometry is unknown.
- The Sun and point-light energy formulas in 3.3 were not checked by a render in this pass, because renders were off limits. The white-card check in 3.3 closes that gap in one test frame.
- `LATE_AFTERNOON`, `SUNSET` and `NIGHT` presets are fitted to two or three sample pairs each and to palettes; `INTERIOR_DAY`, `INTERIOR_LAMP` and `EXTERIOR_NOON` rest on more samples. The reference contains no storm or rain scene.
- The predicted office colours in 3.4 assume the lighting model holds exactly, which is why the kit turns diffuse bounces off. If one diffuse bounce is enabled for colour bleed, walls light each other with their emission, the ambient rises by roughly a fifth and shadows lose some blue; lower A and re-check target row 19.
- Clip B is painted artwork, so its "lighting" numbers describe paint, not a light rig. They are used here only for shade ratios, tints and glow sizes.
