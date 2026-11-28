# Reference C: light, colour and atmosphere, with targets for the EP.1 night-rain expressway

Source: `ref/c/ref.mp4` (720x1280, 30 fps). Frame ids are `frames2/f_NNN.png`, time = (NNN-1)*0.5 s. Video frames were read directly for the rain timing test (t = 34.00, 34.03 and 34.07 s). Values are sRGB as encoded. "Luma" is Rec.709 luma of the encoded values (0 to 1). "Y" is linear luminance after undoing the sRGB curve. The caption band (x 140-580, y 855-940) is masked out. The measuring scripts are in `scratchpad/rcl/m1.py` to `m4.py`, outside the project.

Frames viewed at full resolution: f_011 (sunny day), f_064 (rain with fires and smoke), f_067 (night), f_103 (snow at dusk), `frames/f_017` and `f_018`, plus 2x crops of the f_067 lamp area and wet road, of the f_011 ground shadow, and of three consecutive video frames of rain at t = 34 s.

## 1. Sections and global numbers

| section | frames | luma mean | luma p1 / p50 / p99.5 | sat mean | V<0.25 | V>0.97 (clipped) | sky / ground luma |
|---|---|---|---|---|---|---|---|
| sunny day | f_009-017, f_028-031, f_059-061 | 0.52 | 0.03 / 0.52 / 0.98 | 0.34 | 13 % | 6.6 % | 1.9 |
| overcast rain + fires | f_062-065, f_068-076 | 0.46 | 0.08 / 0.43 / 0.95 | 0.21 | 13 % | 0.9 % | 2.6 |
| **night (moon, lamp, wet road)** | **f_066, f_067** | **0.27** | **0.00 / 0.19 / 0.85** | **0.33** | **48 %** | **0.4 %** | **4.1** |
| snow at dusk | f_098-117, f_127-137 | 0.61 | 0.11 / 0.64 / 0.97 | 0.22 | 4 % | 11 % | 1.5 |

The true night section lasts only about 1 s (t 32.5-33.0). t 30.5-32 is overcast with fires and smoke, and t 33.5-38 is overcast daytime rain. Rain is measured on the day frames. The night grade is measured on f_066 and f_067.

Tonal bands (shadows luma < 0.25, mids 0.25-0.6, highs ≥ 0.6), mean colour and hue share of chroma in percent (red/orange/yellow/green/cyan/blue/violet/magenta):

| section | shadows | mids | highs |
|---|---|---|---|
| day | 22 %, `#312524` h2 s0.26 (24/29/2/2/1/29/6/7) | 37 %, `#786d60` h33 (19/40/6/9/1/24/1/1) | 41 %, `#d9ccbd` h33 s0.13 (6/77/…) |
| rain | 19 %, `#352d2a` h15 (50/19/5/4/1/7/7/8) | 50 %, `#6a6254` h39 | 31 %, `#c4c0c0` neutral (40 orange / 50 blue) |
| night | 58 %, `#19171d` h262 s0.20 v0.11 (10/13/8/0/0/58/9/2) | 29 %, `#6e6d80` h244 s0.15 (blue 88 %) | 13 %, `#aca9b3` h256 s0.06 (orange 22 / blue 74) |
| snow/dusk | 10 %, `#352740` h273 s0.40 (blue 34, violet 45, magenta 8) | 30 %, `#7e6d87` h280 (violet 54, magenta 14) | 60 %, `#d6bbb9` h4 (red 41, orange 27, magenta 22) |

Output of `hue_report.stats` (red/orange/yellow/green/cyan/blue/violet/magenta, then sat, val, dark): night 66-67 = 10/17/0/0/0/71/1/0, 0.31, 0.33, 0.46. Rain 68-76 = 9/55/8/3/0/17/4/4, 0.24, 0.53, 0.11. Day 10-17 = 19/48/3/6/0/22/0/1, 0.28, 0.61, 0.10. Snow 100-117 = 28/21/3/2/0/13/28/5, 0.22, 0.69, 0.03. Ref C has less saturation than refs A and B (0.21-0.34 against their 0.38-0.48). The night frames sit outside the house band on purpose: they are 71 % blue and 46 % dark.

## 2. Key light, shade, ambient

- **Day (f_011).** A sun high and from camera-right-back gives medium-hard shadows. The building-shadow edge on the cobbles rises 10-90 % over about 16-24 px at 720 px width, which is softer than refs A and B at 4-21 px. The surface in shade has 0.44 of the lit Y. Lit cobble is `#c4ae9e` (h25 s0.19 v0.77) and shaded cobble is `#97735a` (h25 s0.40 v0.59). **The shade keeps its hue and gains saturation.** It does not turn blue here, so ambient bounce is warm and AO is strong in the gaps between cobbles. Sky is `#ddd3d1` with clouds lit to near white, and the highs are cream (h33 s0.13), never pure white.
- **Overcast rain (f_068-076).** No cast shadows. Contact AO only: dark wet ruts and puddle edges. The sky is a flat neutral grey `#c1bdc0` (luma 0.75). The grass foreground is the only saturated area (`#534a2a` s0.49).
- **Night (f_067).** The moon is a key from upper left (disc at (183,153), radius 32 px, `#d7cab7`). It lights the cloud tops `#989cae` but casts no visible shadows on the ground. All local shading comes from one warm practical: a lamp on the gantry (bulb `#fdf9c9`, luma 0.97). The night shade is near black and slightly violet: road in shade `#201f25` h249, tank shadow side `#080708` luma 0.03. Grass is not lit and goes to `#12120e` (luma 0.07). The ambient is a dim blue, about 0.05-0.08 linear.
- **Snow/dusk.** Shade turns blue-violet (`#352740` h273 s0.40) and highs pink-cream. This is the only section that matches the house rule "shade hue 240-260".
- **Flat puppets are never relit.** At night the head reads `#e0d6dd` (luma 0.85, a faint lilac cast from the grade only). By day it reads `#efe9e8`. Keep puppet cards emission-only and let only the post grade tint them, by 5-10 %.

## 3. Practicals, bloom, wet surfaces (f_067, crops)

- **Lamp halo.** Luma at radius r from the bulb centre: r0 0.98, r4 0.96, r8 0.84, r12 0.74, r16 0.67, r24 0.47, r32 0.41, background 0.36. The halo reaches half height at about 14 px and is gone by 35-40 px, so a tight bloom of 2-5 % of frame width. The moon has **no** bloom: it drops from 0.74 to 0.58 within 4 px.
- **Warm pool.** The ground under the lamp is `#74421e` (h25 s0.74 v0.46), with a radius of about 1.5-2 vehicle widths, and the falloff runs from saturated orange to black within about 120 px. Tank faces facing the lamp pick up orange rims (`#180907`, h8 s0.72 overall, with specular spots up to 0.83).
- **Wet road.** It is a glossy mirror of the sky: open wet asphalt `#2d3554` (h228 s0.46 v0.33), far road strip `#282d4a`. Puddles mirror cloud gaps at luma up to 0.93. Orange lamp reflections are stretched along the road towards the camera (vertical anisotropic smear). Wheel ruts have bright specular rims. Small dark debris and drops sit on the surface as normal-map dots. Blue for the road holds within h 228-249.
- **Fires (f_064).** Flame `#e2bb6c` (h40 s0.52) with a clipped core `#ffffd0` and a small, weak glow: fires do not light the scene strongly by day.

## 4. Fog, smoke, depth

- **Aerial perspective, day rain (f_069, right half).** Luma by distance: foreground grass 0.29 (std 0.056, defocused), near road 0.36 (std 0.13), mid tanks 0.43 (0.165), far field 0.48 (0.11), horizon haze 0.54 (0.10), sky 0.75. Saturation falls from 0.49 to 0.04 at the horizon. Haze adds about +0.25 luma and pulls colour to neutral grey over the depth of the set.
- **Night fog (f_067).** It is inverted: a bright fog band at the horizon `#34333b`-`#7c777d` (luma 0.20-0.47), with far vehicles as dark silhouettes against it (`#0a0a11`, luma 0.04). The mid ground is `#27232c` (luma 0.14). Smoke and steam plumes are lighter than the ground (`#86838e`, luma 0.52, h254), rise in columns 40-70 px wide and soften towards the top. There are 4-6 of them across the far rows.
- **Smoke at day (f_064).** Dark plumes `#8e8b90` (h286) against a lighter sky, plus a lighter low smoke layer `#7b7574`.
- **Depth of field (Laplacian variance per 160 px band, top to bottom).** f_067: 11 / 1722 / 2023 / 1718 / 4633 / 13389 / 12978 / 5964. The sky is soft and the focus plane is on the near road and character. f_064: 40 / 1621 / 1255 / 1588 / 659 / 1041 / 85 / 18, a strongly defocused foreground tank. The sky and the nearest foreground are always out of focus, and the actor's plane is sharp.

## 5. Rain (f_062-065 and f_068-076, plus video frames at t = 34.0 s)

- **Streaks.** Vertical (median angle 0°, interquartile range 0 to 2.7°), thin (median width 1.85 px at 720 px), brighter than the background: a median of +0.17 luma over the local background, p90 +0.41, cores near white 0.85-0.95 against dark cloud.
- **Length** at 720 px width: p10 12, median 21, p90 80 px. In the densest frames (f_068-070) the median is 28-30 and p90 is 94-96 px. Long streaks fall in the foreground and short ones far off. There is no fixed size layering beyond that.
- **Density.** The detector finds 100-150 streaks per frame in heavy moments (f_064, f_065, f_068-070, f_076) and 53-94 in lighter ones. Streak pixels cover 1.4-2.3 % of the frame in heavy moments and 0.8-1.2 % in light ones. The detector undercounts faint ones, so roughly 150-250 are visible.
- **Timing.** Each video frame (30 fps) has a new random set of streaks. Streak positions do not carry over between consecutive frames, so rain is a per-frame regenerated layer with no continuous drop motion. Splash ticks are not visible at this size.
- **At night (f_067)** only a few streaks show (56 found, 0.45 % coverage, contrast +0.22): only drops against lit fog or near the lamp read.

## 6. Numeric targets: EP.1, Bangkok expressway, night, heavy rain

Measure the final graded frames with the scripts above. In the "ref" column, f_066 and f_067 give the grade and f_068-070 give the rain density.

| item | target | ref |
|---|---|---|
| luma mean, whole frame | 0.24-0.32 | 0.27 |
| luma p50 / p5 / p99.5 | 0.16-0.22 / ≤ 0.03 / 0.85-0.97 | 0.19 / 0.004 / 0.85 |
| share of pixels with V < 0.25 | 35-48 % (outside the house band 8-15 %: night exception) | 48 % |
| clipped V > 0.97 | 0.3-1.5 % (lamp cores, sirens, headlights only) | 0.4 % |
| saturation mean | 0.30-0.40 | 0.33 |
| chroma share by hue family | blue 50-65, orange (sodium) 15-25, red (emergency) 8-15, violet ≤ 6, magenta ≤ 3, green ≤ 2 | blue 71, orange 17, red 10 |
| shadows (luma < 0.25) mean | `#17161d`-`#1e1c26`, h 245-262, s 0.15-0.25 | `#19171d` h262 |
| midtones mean | `#62637a`-`#6e6d80`, h 236-250 | `#6e6d80` h244 |
| highs mean | near-neutral cool `#aca9b3`, warm only at practicals | h256 s0.06 |
| sky vs ground luma | sky 2.5-4x the ground; the cloud deck is the brightest large area | 4.1 |
| sky | top band `#4a4f76`, gaps `#989dbd`, h 228-236. Optional sodium-polluted cloud undersides near the city horizon, h 25-35 at s ≤ 0.25, under 10 % of the frame | moonlit |
| sodium lamps | core `#fdf9c9`-`#ffd27a`, above 1.0 linear (bloom). Ground pool `#74421e` h 22-30 s 0.65-0.8. Pool radius 6-10 head units at the sodium post spacing. Falloff to black within 1 pool radius | gantry lamp |
| bloom | threshold scene-linear 1.0. Half-height radius 12-16 px at 720 width, tail out to 35-40 px. Moon and puppet heads never bloom | r12 0.74, r32 0.41 |
| emergency red (not in ref, story palette) | sRGB `#ff1a1a`-`#e0201c`, h 355-5. Strobe 2-3 Hz. Spill on wet road h 0-10 s ≥ 0.7 within 3-5 head units, reflection smeared along the road. Red chroma share 8-15 %, so it never becomes the key | - |
| key / ambient | moon or sky key from upper left or back, giving no hard ground shadows. World ambient blue h 230-240 at 0.05-0.08 linear. All local contrast comes from practicals (sodium, red beacons, headlights), each casting hard shadows (light radius 0.05-0.15 m) | f_067 |
| shade on lit surfaces | under a sodium lamp, out of the pool = near black blue-violet at 0.05-0.12 of the pool's Y. Car bodies facing a lamp get an orange rim; the opposite side is `#080708`-`#15141c` | f_067 |
| wet asphalt | base `#2d3554` / `#282d4a` (h 228-240, s 0.4-0.5, v 0.28-0.35) where it mirrors the sky. Roughness 0.05-0.12 in puddles covering 30-45 % of lanes, 0.3-0.45 between them. Specular hits up to luma 0.93. Lamp and beacon reflections stretched 3-6x along the view direction (anisotropic, or a vertical blur on a reflection pass) | f_067 road |
| flat puppets | emission card unlit. Graded head `#dcd3dc`-`#e6dee4` (luma 0.82-0.88), a 5-10 % lilac cast only | head `#e0d6dd` |
| fog (volume) | horizon band luma 0.18-0.30 (brighter than the far cars), far cars as silhouettes at luma 0.03-0.06. Contrast std per band: near 0.15-0.17, mid 0.09-0.11, far ≤ 0.10. In Cycles a world/volume scatter density of about 0.01-0.02 per metre (expressway at 1 BU = 1 head) with anisotropy 0.3-0.5, so lamps get soft cones | f_067 bands |
| smoke/steam | 3-6 plumes from wrecks, `#86838e` luma 0.45-0.55, lit from behind by the sky and sodium. Width 40-70 px at mid distance. Density higher at the base, fading upward over about 150 px | f_067 |
| rain streaks | per-frame regenerated (new random set each frame). Vertical ±3° (up to 8° if wind is shown). Width 1.5-2 px at 720 width, length median 25-30 px, p90 80-95 px (foreground). 150-250 visible per frame (detector 120-150). Coverage 1.5-2.5 % of pixels. Additive over the background +0.15 to +0.4 luma. Near lamps and beacons, streaks take the light colour (sodium orange, red) and are brightest. Against unlit black ground, streaks almost vanish (opacity 20-30 %) | f_068-070, f_067 |
| rain extras (for "heavy") | ripple and splash dots on puddles (normal-map rings 3-6 px, 30-60 per frame), mist layer 0-0.5 m above the road at luma +0.03-0.05 | not resolvable in the ref, recommended |
| depth of field | sky and far rows soft (Laplacian var under 50 in the top 160 px band). Actor plane sharp. Optional defocused foreground object in the bottom 15 % of the frame | f_067, f_064 |
| shade hue rule | dark tones h 240-262: passes the house rule. Watch the magenta drift from red beacon light mixing into violet fog (keep magenta ≤ 3 %, and violet h 270-300 ≤ 6 %) | - |

**Where ref C differs from the bundled look:** day shade stays warm, the house band leans blue, overall saturation is lower (0.21-0.34) and the penumbra is softer. For EP.1 night rain, follow the night column above. Use the bundled blue-violet shade rule for the dark tones; ref C's night already lands there (h 244-262).
