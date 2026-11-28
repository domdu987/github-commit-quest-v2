# Reference C: modelling detail and materials

Source: `ref/c/frames2/f_NNN.png` (720x1280, frame n at (n-1)*0.5 s) and `ref/c/frames/f_017.png` (night rain, t=32 s).
Frames read at full resolution: f_003, f_011, f_020, f_029, f_048, f_066, f_070, f_101, f_108, f_130, frames/f_017. Measured only: f_035, f_055, f_062, f_074, f_121, f_106, f_110.
Measuring scripts: `scratchpad/work_refC/m1.py`, `m2.py`; zoom crops `scratchpad/work_refC/crops.png`; frame index `work_refC/idx0.png`, `idx1.png`.
We copy the look only: no WW2 tanks, characters, logo or captions. Each target below ends with what it means for the EP.1 expressway set.

Pixel figures are at 720x1280. At our 360x640 test size, halve them.

## 1. Measured table (caption band y 855-935 masked)

| frame | content | Canny edge % top/mid/bot third | Laplacian var top/mid/bot | mean S | mean V | % V<0.25 | % V>0.9 |
|---|---|---|---|---|---|---|---|
| f_003 | high shot, tank yard, mud | 5.9 / 4.3 / 6.7 | 235 / 255 / 368 | 0.39 | 0.36 | 35 | 0.9 |
| f_011 | Tiger on blocks, gantry, cobbles | 2.4 / 10.4 / 22.7 | 572 / 2073 / 9721 | 0.24 | 0.65 | 10 | 23 |
| f_020 | workbench medium shot | 4.5 / 10.4 / 12.3 | 313 / 1460 / 476 | 0.32 | 0.49 | 20 | 5 |
| f_029 | two puppets, fence, brick hall | 3.4 / 12.0 / 9.4 | 158 / 3080 / 1255 | 0.37 | 0.58 | 15 | 16 |
| f_035 | wide yard, low key | 4.2 / 3.5 / 2.2 | 141 / 469 / 122 | 0.39 | 0.35 | 38 | 0.3 |
| f_048 | road-wheel close-up, motion | 3.0 / 1.5 / 1.6 | 259 / 162 / 48 | 0.53 | 0.38 | 42 | 1.4 |
| f_055 | wheat field + tape icon | 5.2 / 3.2 / 4.2 | 577 / 361 / 211 | 0.58 | 0.70 | 1.5 | 13 |
| f_062 | burning convoy, dusk | 2.4 / 7.0 / 12.5 | 1567 / 991 / 1192 | 0.32 | 0.55 | 13 | 11 |
| f_066 | **night, wet road, sodium lamp** | 2.1 / 5.6 / 6.7 | 1052 / 752 / 1778 | 0.33 | 0.33 | **47** | 0.5 |
| f_070 | **day rain, wet road, wrecks** | 3.9 / 8.6 / 7.0 | 1815 / 2191 / 1544 | 0.20 | 0.50 | 11 | 1.1 |
| f_074 | rain, puppet medium | 2.7 / 3.7 / 1.6 | 556 / 692 / 298 | 0.21 | 0.52 | 6 | 0.8 |
| f_101 | snow road, column of 9 vehicles | 13.0 / 18.7 / 17.7 | 2460 / 5747 / 4472 | 0.23 | 0.73 | 1.7 | 28 |
| f_108 | snow, rows to horizon | 1.5 / 17.4 / 35.0 | 27 / 3285 / 12728 | 0.21 | 0.69 | 5 | 20 |
| f_121 | snow, close wreck | 1.7 / 4.8 / 31.0 | 189 / 411 / 15358 | 0.27 | 0.56 | 21 | 10 |
| f_130 | two puppets, snow | 1.0 / 10.7 / 23.7 | 220 / 3245 / 11736 | 0.22 | 0.72 | 8 | 27 |

Reading: the sharp detail sits in the middle and lower thirds (edge 7 to 35 percent) and the top third is soft sky (edge 1 to 6 percent, Laplacian under 600). In a still, aim for edge density about 2 to 6 percent top, 6 to 18 percent mid, 8 to 30 percent bottom. When the camera moves fast (f_035, f_048), every band falls to 1.5 to 4.5 percent because of motion blur. That is fine.

Sharpness by 160 px row band (Laplacian variance, top to bottom):
- f_011 `1, 573, 1285, 1656, 2298, 10788, 16096, 1767`
- f_029 `25, 216, 203, 2048, 3503, 5901, 1684, 385`
- f_108 `0, 14, 960, 4232, 3291, 3615, 12691, 14196`
- f_121 `13, 335, 312, 656, 204, 7109, 20132, 10519`
- f_130 `12, 158, 897, 4433, 3005, 4985, 18740, 5775`

Target: the focus plane sits at about 0.55 to 0.85 of the frame height. The background is 5 to 30 times softer than the focus band, and the band right at the lens is also soft (f_011, f_029, f_130: the last band drops 4 to 9x). In Blender, focus on the actor or the cutter and use f/2.8 to f/4 equivalent on the 22 mm lens, so that the near foreground, the far horizon and the sky all go soft. Do not put the whole frame in focus.

## 2. Vehicles and hard-surface geometry

Seen at full resolution in f_003, f_011, f_020, f_048, f_101, f_130:
- **Bevels on every edge.** Hull and turret edges carry a 1 to 3 px highlight line in medium shots and 4 to 8 px in the close-up f_048. No knife-sharp CG edges appear anywhere. Target: a bevel modifier of about 0.02 to 0.04 of the object size with 2 to 3 segments, or a bevel shader of the same width.
- **Panel lines and parts.** f_048 has recessed grooves about 3 to 5 px wide, raised tow rings, hatch rings, bolt dots of 4 to 6 px, a separate fender lip and an undercut shadow gap below it. f_003 has an engine grille of about 8 slats on a 6 to 8 px pitch, louvre plates, a stowed log or tube, a turret ring hole with teeth, and stencilled numbers and star decals (decals are flat-colour textures). Target: at least 15 separate sub-parts on each hero vehicle (doors, handles, mirrors, bumpers, grille, lamps, number plate, wipers, roof rack or light bar, wheel arches, sills, fuel cap) and at least 5 on each background vehicle.
- **Wheels.** Road wheels are modelled as rim, dish, hub boss, bolt circle and a separate black rubber tyre ring (about 18 px thick at 240 px radius in f_048). Running gear is fully modelled: sprockets with teeth (f_011, f_020), individual track links, and wheels stacked as props (f_011, f_020, about 30 wheels in stacks). For our cars: a tyre with a sidewall bulge and a tread band, a 5 to 10 spoke alloy or steel rim, a visible brake disc, and wheel-arch gaps that read dark.
- **Glass.** Building windows have mullions, a frame depth and a dark reflective pane that shows a soft sky gradient (f_011, f_020). For our cars: windscreens dark, with a sky or lamp reflection streak across them, rain droplets and smeared wiper arcs on the hero car. Crash damage: spiderweb cracks as a texture plus a few missing panes.
- **Materials on vehicles.** Painted metal is mid-rough (roughness about 0.45 to 0.6) with a broad soft sheen (f_011 grey hull) plus dirt and wear. The gun barrel is near polished metal: a sharp white highlight strip 6 to 10 px wide in f_011, roughness about 0.2 to 0.3. Camouflage is large soft blotches (f_101) and mud is darker in the lower 20 to 30 percent of the body (f_003, f_121). Target for cars: car paint roughness 0.3 to 0.45 with clearcoat, chrome and steel trim at 0.15 to 0.25, black plastic and rubber at 0.6 to 0.8, a wet-coat roughness reduction of 0.1 to 0.2 from the rain, and a dirt mask on the lower 25 percent.

## 3. Buildings and structures

- The brick hall (f_003, f_029) has gables, ledge cornices that stand 6 to 10 px proud, arched windows with a red brick surround, drainpipes and downspouts, and solar panels on the roof (f_029). At these distances individual bricks barely resolve. The FFT period on the wall (f_029 [380:470,300:500]) is about 30 px vertical with no clean horizontal period. The wall reads as orange-red colour with vertical **grime streaks under every ledge** (dark, 10 to 40 px long). Target: put dirt and wetness streaks under ledges, joints and barriers. That matters more than a high-resolution brick map.
- The white render warehouse (f_011, f_020) has a corrugated roof edge, deep window reveals, an exposed steel gantry crane with a hanging chain and hook, and pipes.
- Wooden fences (f_011, f_029) are individual pickets about 10 to 14 px wide, with rails and rough tops.
- For EP.1: modelled jersey or F-shape concrete barriers with a bevelled top, drain slots and rain grime. Expressway lamp masts as repeated instances with a sodium head. An overhead sign gantry (truss). Expansion joints across the deck. Kerb and gutter. Distant Bangkok towers as low-detail blocks with lit-window emission textures.

## 4. Ground surfaces (texture scale on screen)

| surface | frame / region | measured or read size |
|---|---|---|
| cobble / paver, near (bottom 15 percent) | f_011 [1100:1280,0:400] | stones about 22 to 28 px wide and 18 to 20 px deep. Dark grout 2 to 3 px. Every stone bevelled, with its own top highlight and a slight tone variation |
| cobble, mid (y 860-1000) | f_011 [860:1000,450:650] | stones about 10 to 13 px. Perspective fall-off is real geometry or a correctly scaled texture, not a flat tile |
| cobble near (other shot) | f_029 [1050:1270,0:260] | stones about 40 x 22 px, with mud patches on top (decals as dark irregular blots of 30 to 120 px) |
| mud / dirt | f_003, f_029 right half | dark brown with straw and twig scatter (hundreds of 5 to 20 px sticks) and blue water puddles reflecting the sky (f_003) |
| wet asphalt, night | f_066 / f_017 road | V mean 0.24, std 0.20 to 0.23. 3 to 5 percent of road pixels are V>0.7 with S<0.3 (specular). A broad warm reflection pool under the sodium lamp, about 250 x 120 px. Tyre-tread tracks as a repeating ribbed stripe about 10 to 14 px pitch. Grit specks 2 to 4 px |
| wet asphalt, day rain | f_070 | a puddle strip mirrors the sky (V about 0.75, low S). Darker edges where the surface is drier. A mud rut runs down the centre |
| grass verge | f_070 [950:1270,330:720] | separate modelled grass clumps 20 to 50 px, about 1 clump per 60x60 px near. Dark olive base |
| grass blades in mud | f_029 | single tall blade clusters, 60 to 150 px tall near the camera, very saturated green, out of focus in the foreground |
| snow with grass | f_108, f_130 | instanced straw tufts 30 to 100 px near (period about 100 px), thousands of tiny bumps far off (a 12 px vertical period in f_108's near band), and a bright surface with blue-violet shade |
| wheat field | f_055 | high-saturation yellow (S 0.58), stripes of rows receding |

Targets for the expressway deck:
- Asphalt aggregate texture at 2 to 4 px near the camera.
- Lane paint 18 to 30 px wide near, worn and broken.
- Puddles covering 15 to 30 percent of the road, at roughness 0.02 to 0.08, against 0.35 to 0.5 for damp asphalt and a normal-mapped grain.
- 3 to 6 percent of road pixels in specular highlights at night.
- Every emissive source (sodium lamps, red strobes, tail lights) drawn as a long vertical reflection streak on the deck.
- Debris scatter: glass cubes, plastic bumper shards, leaves, paper. At least 50 instances in the near third.

## 5. Detail density: distinct props per frame

These are counts made by eye on the full-resolution frames.
- f_003: about 25 objects (4 hulls and turrets, 1 tractor, 2 track runs, 10+ shells, a fence, a barrel, a teapot, a hall with 4 arches, trees, straw, puddles).
- f_011: about 20 kinds and 80+ instances (hull, turret on crane with chain and hook, sprocket, 2 cribbing blocks, a step box, a bench, about 30 stacked wheels, about 15 fence pickets, a downpipe, trees, mud blots, grass).
- f_020: about 15 kinds (desk with drawers and handles, wheel with tyre, vise, red tray, magnifier, gears, hull and sprocket, about 30 wheels behind, a windowed door, a fence, trees).
- f_066 / f_017 night: about 20 (a gantry crane with a lamp and hook, 3 near wrecks, 4 distant vehicles, 3 poles with 5 wires, 2 bollards or cans, a rifle, 6 smoke columns, a treeline, a wall).
- f_070: 7 vehicles, 9 trees, 4 poles with wires, a puddle strip, a can, about 40 grass clumps, and 86 rain streaks.
- f_101: a column of 9 vehicles with 9 small figures beside it, a sled and crate, an engine, about 20 wheels on the ground, 5 poles, 6 trees, and icons.
- f_108: 3 near wrecks (one turret in mid-air), 5 mid-distance vehicles (blob width 21 to 45 px) with smoke, a row of about 25 hay bales or bushes at the horizon, trees, and dense ground instancing.

Targets for each shot of the EP.1 expressway:
- At least 12 distinct prop kinds.
- At least 40 visible instances.
- At least 3 depth layers: foreground blurred clutter, the action layer, and a background repeating row.

Prop list to build:
- Crashed and abandoned cars: sedan, pickup, tuk-tuk, motorbike, minivan, bus, taxi. Use 4 to 6 models with colour and damage variants.
- Open doors, deployed airbags, broken glass piles.
- Traffic cones, barrier sections, a knocked-down sign, bags, a phone.
- Scattered shoes, a rescue bag, cables.
- Emergency light bars.
- Lamp masts, a gantry, a sound wall, and the skyline.

## 6. How far the world extends

- Every exterior shot reaches the horizon. Wide shots repeat objects in rows: poles at a fixed spacing (f_066, f_070, f_101), vehicle rows getting smaller (f_101 runs from 400 px down to about 30 px wide over 9 instances; f_108 shows 5 vehicles at 21 to 45 px on a second row), a treeline or hay row at the horizon, then a hazy plane.
- Aerial perspective: distant layers lift toward the fog colour. Night sky mean RGB is about (125,129,155), a cool slate blue.
- Target for EP.1:
  - The expressway runs to a vanishing point within the frame in wide shots.
  - At least 20 stalled cars, receding from 60 percent of the frame width down to under 15 px.
  - Lamp masts every 30 to 40 m (instances).
  - The city skyline at the horizon with sparse lit windows.
  - Volume fog or a mist-plane density so the far third loses 40 to 60 percent of its contrast.
  - Smoke columns from 2 to 4 burning wrecks.

## 7. Rain, wetness, atmosphere (f_066, f_070-f_074, frames/f_017)

- Rain streaks are thin bright vertical lines, 1 to 2 px wide, with a median length of 29 to 48 px and a 90th percentile of 38 to 108 px. There are 31 to 86 streaks per frame in day rain (f_070: 86) and only about 9 detected at night (f_066), where they are lit mainly near lamps. The streaks run at a slight tilt (under 5 degrees) and some are out of focus near the camera. Target: 40 to 90 streaks per frame at 720x1280, lit by the warm lamp near it and the cool sky far from it, plus splash rings on puddles.
- Night palette (frames/f_017, f_066): 47 percent of pixels at V<0.25, mean V 0.32, about 11 percent warm (hue 340 to 50 at S>0.25) against about 29 percent cool (hue 190 to 260). p99 V is 0.88 to 0.96, from the lamp core and the specular. One warm practical (a lamp on the gantry) drives a 250 px orange pool on the wet road. The moon and sky stay cool. Smoke and steam columns are lit grey against the blue. Target for EP.1: the same ratio of 10 to 15 percent warm (sodium and fire) against 25 to 35 percent cool, with red strobes adding 3 to 6 percent of red. Keep shade at hue 240 to 260.
- Note: `v3/tools/hue_report.py` currently crashes because its bundled references (`ref/a/t*.jpg`) are missing, so I measured the hues directly with OpenCV. Fix that tool or point it at existing references before relying on it.

## 8. Puppets in the world

Heights are measured on the full-resolution frames, head top to feet, as a fraction of frame height H=1280, ±10 px.

| frame | shot | puppet height / H |
|---|---|---|
| f_003 | high wide | 0.125 |
| f_011 | medium-wide | 0.21 |
| f_066 / f_017 / f_070 | wide night and rain | 0.16 |
| f_029 | medium two-shot | 0.30 and 0.24 |
| f_130 | medium two-shot | 0.28 and 0.25 (one stands on top of a vehicle) |
| f_020 | medium close | 0.47 |
| f_101 | background extras | about 0.05 |

- Head diameter in the medium two-shot (f_029) is about 120 px (0.094 H).
- Target: the hero at 0.15 to 0.30 H in establishing and medium shots, so that the world dominates. Use 0.45 or more only for dialogue inserts. Use background extras or zombie silhouettes at 0.03 to 0.08 H to sell the scale.
- Grounding:
  - Feet are thin ink legs ending in small dark shoes.
  - Contact shadows are soft and low-contrast: an ellipse 1.2 to 1.6 times the stance width, at 0.6 to 0.8 of the local ground value (f_029, f_130).
  - In night shots (f_066) the puppet is unlit flat colour and casts a faint dark shadow away from the lamp.
  - On wet ground, add a dim, blurred mirror of the card in the puddle (the reference shows ground reflections on wet asphalt for objects; extending it to cards is our choice).
  - Puppets interact with geometry: one stands on a step box (f_011), one leans on a fence (f_029), one stands on a vehicle (f_130). Furniture and fences hide parts of the puppets. Target: in every shot Kong touches or is hidden by real geometry, such as the car door he cuts, a barrier or a bonnet.
- The puppets stay sharp while the world gets depth of field and motion blur (f_003, f_048 neighbours). Keep the existing render-layer split.

## 9. Flat graphic overlays (for completeness)

- f_099 to f_105: red X marks about 100 to 130 px wide.
- f_101 to f_125: green ticks about 80 to 100 px.
- f_053 to f_055: a yellow tape-measure ribbon with a black label box ("0.9 MILE" style).
- f_115 to f_117: yellow trajectory arcs.

These sit on the 3D ground plane with perspective (the tape, the X row) or in screen space (the ticks). Use our own icons: a red X on infected cars, a green tick on the "cleared" lane, and a yellow distance tape to the exit ramp.

## 10. Short target list for the EP.1 expressway set

1. Hero car and cutter area:
   - Bevelled, panel-lined, 15 or more sub-parts.
   - Wet clearcoat (roughness 0.3 to 0.45).
   - Chrome at 0.15 to 0.25.
   - Mud and dirt on the lower 25 percent.
   - Cracked glass.
2. Deck:
   - 2 to 4 px aggregate.
   - Puddles at roughness 0.02 to 0.08 over 15 to 30 percent of the area.
   - Long vertical reflections of every light.
   - 3 to 6 percent specular pixels.
3. At least 12 prop kinds and at least 40 instances per shot, in 3 depth layers.
4. Rows to the horizon:
   - At least 20 cars.
   - Lamp masts every 30 to 40 m.
   - The skyline.
   - Fog that cuts far contrast by 40 to 60 percent.
5. Edge density about 2 to 6 / 6 to 18 / 8 to 30 percent (top, mid, bottom) in stills.
6. Depth of field with the focus band at 0.55 to 0.85 H and 5 to 30x softness in the background.
7. Rain: 40 to 90 streaks of 1 to 2 px x 30 to 110 px per frame.
8. Night: about 47 percent of pixels at V<0.25, 10 to 15 percent warm, 25 to 35 percent cool, shade hue 240 to 260.
9. Kong at 0.15 to 0.30 H, with a soft contact shadow and touching geometry.
