# LOOK_SPEC_C: build specification for the reference-C look, EP.1 night-rain expressway

Scene: DEAD ZONE 09 EP.1 opening. Bangkok elevated expressway at night in heavy rain. Gridlock of crashed and abandoned cars, red emergency lights, and Kong (rescue worker, orange reflective "RESCUE" vest) with a cordless hydraulic rescue cutter.
Look: flat unlit 2D puppets on emission-only cards (unchanged from v3) inside a much denser, textured, lit 3D world, following reference C (`ref/c/ref.mp4`).
We copy the look only. Do not copy ref C's characters, tanks, logo, captions or the "SEGMENT ZERO" watermark.

This file merges three lens reports. Where they give numbers, this file wins over them for EP.1:
- `spec/refC_materials.md` (M): geometry, materials, density, rain counts, puppets in the world.
- `spec/refC_light.md` (L): light, colour, fog, rain shape, night grade.
- `spec/refC_camera.md` (C): lens, moves, DOF, motion blur, icons, captions.

`spec/LOOK_SPEC.md` (LS), `spec/verify_blender_api.md` (API) and `v3/stage/REVIEW.md` stay in force wherever this file is silent. Section 1 lists every place where this file overrides LS.

Status words, as in LS:
- **measured**: a lens measured it on ref C.
- **resolved**: my merge of conflicting lens numbers (section 2 gives the reasoning).
- **judgement**: my call. No ref measurement backs it.
- **to verify**: a bpy name or cost nobody has run yet. Gate it before building on it.

---

## 0. Units, frame, measuring conventions

- Final frame: 720x1280, 30 fps. Test renders: 360x640 at low samples with OIDN. Pixel numbers below are at 720x1280; halve them for tests.
- 1 BU = 1 D, the outer head diameter (LS). **World scale (judgement): 1 D = 0.6 m.** The hero is 2.9 D tall, so Kong is 1.74 m. A sedan is 4.6 x 1.8 x 1.45 m = 7.7 x 3.0 x 2.4 D. A lane is 3.5 m = 5.8 D. Use this conversion for every real-world dimension below.
- Lens focal length in px = `lens / 36 * 1280` (API row 66): 22 mm = 782 px, 32 mm = 1138 px, 50 mm = 1778 px. A head of D at planar depth z covers `f_px / z` px.
- "Luma" means Rec.709 on encoded sRGB values, 0 to 1. "V" and "S" are HSV on encoded values. Mask the caption band (y 855-940) out of every image statistic.
- Hue families are those of `v3/tools/hue_report.py`: red 345-20, orange 20-50, yellow 50-75, green 75-165, cyan 165-200, blue 200-255, violet 255-290, magenta 290-345.
- Its `__main__` crashes because `ref/a`, `ref/b` are missing (M10). Import `stats()` from it instead: `sys.path.insert(0, ".../v3/tools"); from hue_report import stats`. That function is fine.

---

## 1. What changes against LOOK_SPEC.md (LS)

| Topic | LS (refs A/B, house) | LOOK_SPEC_C (ref C, EP.1 night rain) |
|---|---|---|
| Set materials | `lit` = Diffuse + ambient Emission. No Principled, no specular, no bump, no procedural noise as visible texture | Principled BSDF everywhere, with roughness, clearcoat, normal and bump maps, grime and wetness masks, and procedural or code-drawn textures. The LS ambient-as-emission term stays (A added to Principled Emission) so shade remains noise-free |
| Edges | Inverted-hull ink, 3 px, on props | **No ink on set objects.** Ref C has none: edges read through bevel highlights of 1-3 px (medium) and 4-8 px (close). Ink only on puppets and icons |
| Detail and density | Wide shot holds 12-26 set objects | At least 12 prop kinds and at least 40 instances per shot, in 3 depth layers. At least 20 cars visible in wides. The world reaches the horizon |
| Lens | 22 mm for every camera (18-24 allowed) | **32 mm default.** 22-24 mm at ground level, in a car or POV. 40-60 mm for long-lens gridlock rows and macro inserts |
| Roll | 0 always | 0-1.5 deg drift allowed, up to 3 deg inside whips. 8-15 deg Dutch only after the horror begins (director's brief) |
| Puppet size | Medium head 170-230 px, figure 0.43-0.61 H | **World dominates:** Kong 0.15-0.30 H in wide and medium shots (medium head about 120 px). 0.45 H or more only in MCU and inserts |
| Static holds | 6-14 frames, at most 3-4 per film | 30-60 frames only to read an icon and at the end. Otherwise at most 14 frames (CONVENTIONS still says 6 for the hook: shots in this look use 14) |
| Transitions | 4 of 5 are cross-dissolves | **No dissolves** (ref C has none). Use hard cuts, impact-flash cuts, and fly-through camera moves inside one take. Whips and snaps as transitions at most twice (brief) |
| DOF | Deep focus. Plate blur sigma 5 only in 2-3 close-ups. Never Cycles DOF | Still never Cycles DOF. Depth-driven DOF in post on **every** shot, graded by shot size (section 7.4): wides mild, MCU sigma 2.5-3.5, macro 4-8. Sky and far rows always soft |
| Motion blur | Plate only, characters always sharp | Above 40 px per frame (whips, crash moves) the **whole frame, puppets included**, streaks with a shutter of 0.5 frame. 20-40 px per frame: plate only, actors sharp. Captions and icons always sharp |
| Haze / fog | Baked into far cards, never a volume | Depth-based fog in post from the Z pass (a night "inverted" band), light cones and smoke as cards. Still no Cycles volume (cost) |
| Rain | Extrapolated, no reference | Measured: per-frame regenerated 2D streak layer in post, depth-occluded and lit by local light (section 5.3) |
| Grade | CDL offset (0.0075, 0.0035, 0.0095) (plum), saturation 1.12, vignette 0-4 % | Night CDL offset (0.004, 0.004, 0.008) (blue, hue about 240), saturation 1.00-1.05, vignette -5 to -10 % at the edges |
| Colour band | Red 30-41, orange 22-38, blue 14-30 % of chroma. S 0.38-0.48, V 0.45-0.63, 8-15 % of pixels below V 0.25 | **Night exception:** blue 50-65, orange 15-25, red 8-15 % of chroma. S 0.30-0.40, luma mean 0.24-0.32, 35-48 % of pixels below V 0.25. Shade hue 240-262 as before; magenta ≤ 3 % |
| Bloom | Glare Bloom threshold 1.0, 12-24 px | Threshold 1.0, half height at 12-16 px, tail out to 35-40 px. Heads, moon and painted signs never bloom |
| Cost target | 2 s average per final frame (2D plates), T frames ≤ 6 s wall | ≤ 30 CPU s per final 720x1280 frame (CPU s = wall s x threads), every frame in true 3D. v3 measured 17-20 CPU s on the simple office |
| Icon pop | (brief) 4-frame overshoot 0 → 115 → 100 % | Ref C pops over 2 frames (50 %, then 100 %). The brief's 4-frame overshoot stays allowed because the user asked for it. Icons are world-anchored but drawn after blur, so they stay sharp |

---

## 2. Conflicts between the three lenses and how I resolved them

| # | Conflict | Resolution |
|---|---|---|
| 1 | DOF. M asks for a focus band at 0.55-0.85 H, 5-30x softer background and a soft near foreground on every still. C finds wide shots deep focus (4 % of tiles above sigma 1.5) and real DOF only in MCU and macro. L finds the sky and far rows always soft | Per shot size (7.4). Wides: background sigma ≤ 1.5 px at infinity, background/actor Laplacian ratio 0.28-0.47 (C). Most of the softness comes from fog and rain, not defocus. MCU and macro as C. M's 5-30x ratio is mostly haze plus codec, so it is checked with the band Laplacian in 9, not forced with blur |
| 2 | Puppets in motion blur. M and LS keep puppets sharp. C sees them streak in whips (v0118, v1290) | Above 40 px/frame the whole frame streaks. 20-40 px/frame streaks the plate only. v3's hook already streaks the whole frame in its whip |
| 3 | Rain count. M targets 40-90 streaks. L counts 100-150 detected (150-250 visible) in day rain, and only about 56 at night | Generate 180-240 streaks per frame, then let the light kill most of them: unlit streaks get 20-30 % opacity. Acceptance is measured with L's detector (`scratchpad/rcl/m4.py`): 50-110 detected, coverage 0.6-1.5 %. That sits above the ref night (0.45 %) because the screenplay says *heavy* rain and our frame has more light sources |
| 4 | Puddle coverage. M says 15-30 %, L says 30-45 % of lanes | 25-40 % of lane area. Tune it on the specular-pixel share (3-6 % of road pixels) |
| 5 | Lens. LS/house is 22 mm. The brief says 22 default with 35-50 for inserts. C says 32 default | 32 mm default (the ref C look is the user's new style reference). 22-24 for ground and in-car shots, as the brief's low/POV angles want. 40-60 for long-lens rows and inserts |
| 6 | Transitions. LS uses dissolves. C has none. The brief allows a whip or snap transition at most twice | No dissolves. Joins are hard cuts, 1-2 impact-flash cuts (2-4 frames white star and flash), and continuous fly-through moves inside a take (these are not transitions). At most 2 whip/snap transitions in EP.1. **Director decision flagged:** ref C uses 6 whips in 68 s, the brief caps them at 2 |
| 7 | Red share. M says 3-6 % of pixels. L says 8-15 % of chroma | Both apply. They measure different things: pixel share with hue 350-10 and S > 0.5, and chroma share from `hue_report.stats` |
| 8 | Vehicles in the scene. M lists tuk-tuks and motorbikes | Not allowed on Bangkok expressways, so not on our deck. Use sedans, hatchbacks, pickups, SUVs, taxis, passenger vans, minibuses, 6-wheel trucks, a tour bus and Kong's rescue pickup |
| 9 | Paint roughness. M section 2 says 0.45-0.6 (the ref's dull army paint). M section 10 says 0.3-0.45 with clearcoat | Car paint 0.30-0.45 with clearcoat 0.5-1.0, minus 0.1-0.2 for the wet coat. Truck and bus paint 0.45-0.6 |

---

## 3. The world: what to build

### 3.1 Layout (D units, 1 D = 0.6 m)

- **Deck.** Two carriageways of 3 lanes plus a hard shoulder: 3 x 5.8 + 4 = 21.4 D each, split by a 1.5 D median barrier. Model 1000 D (600 m) of straight deck with a gentle curve (radius about 1500 D) beyond 400 D, so the vanishing point stays in frame and rows of lamps curve away. Beyond 1000 D, a low-detail continuation card or mesh runs to 3000 D.
- **Elevation.** The deck stands 25-35 D above the city. Leave a gap past the outer barrier so a high camera sees down into dark streets with sparse lights. Those can be cards.
- **Barriers.** F-shape concrete, 1.6 D high, top bevelled 0.08 D, drain slots 0.6 x 0.15 D every 5 D, expansion joints across the deck every 50 D (steel strip, glossy).
- **Lamp masts.** Twin-arm on the median every 50-67 D (30-40 m, M), 20 D tall, sodium heads. Instance them (API row 43).
- **Sign gantry.** One overhead truss at about 180 D with green generic signs carrying code-drawn Thai text: no real operator logo.
- **Skyline.** At 2000-5000 D. 40-80 tower blocks of 60-500 D height, with emission window textures. 5-15 % of windows lit, mixed warm/cool. Add 4-8 blinking red aviation lights at 1 Hz. Towers use the `painted` class: emission only, no light sampling.
- **Sky.** A world gradient (5.1) plus a cloud-deck emission dome or card with code-drawn clouds.

### 3.2 Depth layers (every shot needs all three, M)

| Layer | Planar depth | Content | DOF |
|---|---|---|---|
| FG clutter | 0.5-4 D | barrier edge, cone, glass shards, a shoe, an umbrella, a wet bonnet edge, a hanging cable | soft (near CoC) |
| Action | 4-25 D | hero car, Kong, the driver, rescue pickup, wrecks | sharp band |
| BG rows | 25-1000 D | car rows, masts, gantry, smoke plumes, other emergency lights | fog plus mild defocus |
| Far | > 2000 D | skyline, cloud deck | soft, foggy band |

### 3.3 Vehicles

LOD rule:
- **Hero** (within 15 D of camera in any shot): at least 15 separate sub-parts (M). Body shell, 4 doors with handles and shut-line gaps, bonnet, boot, bumpers, grille (slats every 3-4 px on screen), head and tail lamp units, number plate (code-drawn generic Thai plate, fake number), mirrors, wipers, sills, wheel arches, fuel cap. Hero cars also get roof rack or light bar, antennas, and a damage set.
- **Mid** (15-150 D): at least 5 sub-parts. Shell, glass, 4 wheels, lamp units, bumpers.
- **Far** (> 150 D): one bevelled shell, wheels, emissive tail/head lamp dots.

Base models (4-6, plus colour and damage variants): sedan, hatchback, pickup (very common in Thailand), SUV, taxi (generic two-tone colours, no brand), passenger van, 6-wheel truck, tour bus, and Kong's rescue pickup with a red/blue light bar and "RESCUE" livery drawn by us (no real foundation logo).

Geometry:
- **Bevel.** A Bevel modifier on every hard edge: width 0.03-0.06 D, 2 segments, limit method Angle 30 deg, harden normals. Apply it at build time to save sync per frame.
  - Check: highlight width 1-3 px in a medium shot. At 32 mm and 15 D, 0.05 D = 3.8 px.
  - Close-ups: 4-8 px.
- **Panel grooves.** 3-5 px. Use a normal or bump map from a code-drawn panel-line texture plus a darker cavity line in base colour. Boolean cuts only on the hero.
- **Wheels.** Separate tyre with sidewall bulge and tread band, 5-10 spoke rim, brake disc, dark arch gap.
- **Glass.**
  - Mid and far cars: opaque dark Principled, roughness 0.03-0.08, reflecting the sky and lamps.
  - Hero car: Transparent mixed with Glossy by Fresnel, with no refraction so the driver card shows through.
  - Hero car overlays: a spiderweb crack texture (alpha), rain droplets as a normal map, and a smeared wiper arc.
- **Damage.** Crumpled fronts (lattice or displace), 3-6 open doors in a wide, deployed airbags (white soft blobs), missing panes, glass piles on the road (200-400 instanced 0.03-0.08 D cubes, roughness 0.1).

Materials, all Principled (M):

| Surface | Base | Roughness | Other |
|---|---|---|---|
| car paint | per variant, albedo ≤ 0.7 | 0.30-0.45, minus 0.1-0.2 wet | clearcoat 0.5-1.0, clearcoat roughness 0.05-0.1 |
| truck and bus paint | dull | 0.45-0.6 | |
| chrome and steel trim | metallic 1 | 0.15-0.25 | |
| rubber and black plastic | 0.03-0.05 | 0.6-0.8 | |
| grime | lower 25 % of every body | +0.15 | darker. Mask = Generated Z through a ColorRamp, broken by noise |
| head lamps (off) | glossy lens | 0.05 | |
| tail lamps | emission red `#ff1a1a`, strength 2-4 (they bloom) | | `emission_sampling = NONE` (5.2) |

### 3.4 Ground, the wet deck (M, L)

- **Asphalt.**
  - Base albedo 0.06-0.10, near-neutral, slightly blue.
  - Aggregate normal map at 2-4 px on screen near the camera (texel density at least 1 texel per screen pixel in the closest shot).
  - Grit specks 2-4 px.
- **Puddles.**
  - A code-drawn mask over 25-40 % of lane area, concentrated in ruts and along the barrier gutter.
  - Roughness: puddle 0.05-0.12, damp asphalt 0.30-0.45, ruts in between.
  - Puddles mirror the sky: target `#2d3554` / `#282d4a` (hue 228-240, S 0.4-0.5, V 0.28-0.35) where the sky is reflected.
- **Tyre tracks.** A ribbed roughness and normal stripe at a 10-14 px pitch, with bright specular rims on the ruts.
- **Lane paint.** 18-30 px wide near the camera, worn and broken, white and yellow, roughness 0.5 (paint is less wet).
- **Long reflections.** Every emitter must draw a long vertical streak on the deck (L: stretched 3-6x along the view direction).
  - First try the physics: damp-zone roughness 0.12-0.2 at grazing angles makes the streaks by itself.
  - Fallback in post (section 8 step 4): a vertical directional blur of road highlights inside the road index mask.
- **Debris.** At least 50 instances in the near third (M): glass cubes, bumper shards, a hubcap, mirrors, paper, leaves, plastic bags, a shoe, a phone, an umbrella, cones.
- **Grime streaks** under barrier tops and drain slots, 10-40 px long. These read more than texture resolution (M3).

### 3.5 Prop list and counts per shot

Kinds (at least 12 visible per shot):
1. cars, by type
2. lamp masts
3. barriers and median
4. gantry and signs
5. cones and water-filled barrier
6. glass piles
7. debris (bags, shoes, phone, umbrella)
8. smoke plumes
9. fires (2-4 burning wrecks)
10. emergency light bars and beacons
11. rescue gear (bag, cable, cutter case)
12. skyline
13. wires and cables
14. expansion joints and drains
15. airbags and open doors

Instances: at least 40 visible per shot (M). Count objects whose projected bounding box is ≥ 4 px and not fully occluded (9, check 14).

Rows to the horizon (M6, C): in wides, at least 20 cars visible, shrinking from about 60 % of frame width down to ≤ 15 px. At 32 mm a 7.7 D car is 15 px wide at z ≈ 580 D, so the gridlock must extend past 600 D.

---

## 4. Puppets in the world

- **Cards.** Emission-only cards, never lit. The stage module is unchanged and is used as is (`v3/stage`, read-only).
- **Night tint.** The graded head must read `#dcd3dc`-`#e6dee4` (luma 0.82-0.88, a 5-10 % lilac cast) (L). Put the tint on the card's emission colour (about 0.90, 0.86, 0.92) at runtime in the take's own module, after the actors are built, or multiply in post through the actor index mask. Never edit stage files.
- **Sizes.**

| Use | Height |
|---|---|
| Kong in establishing and medium shots | 0.15-0.30 H |
| Medium head | about 120 px (z ≈ 9.5 D at 32 mm) |
| MCU | 0.45-0.5 H |
| Extras and silhouettes (infected far down the rows) | 0.03-0.08 H |

  Head-centre band 0.35-0.59 H and whole heads above y 880 (CONVENTIONS) still apply to the main character.
- **Grounding.**
  - Real cast shadows come from the nearest sodium Light and the beacons: several hard shadows, a faint dark shadow away from the lamp.
  - Add a soft contact-shadow decal under each actor: an ellipse 1.2-1.6x the stance width at 0.6-0.8 of the local ground value. Build it as a transparent dark plane with a radial alpha. It is our own module, not stage.
- **Reflection.** Cards must stay `visible_glossy`, so the wet deck mirrors them blurred for free. Check that the stage leaves it on (API row 77 names the flag).
- **Contact with geometry, every shot** (M8). Kong touches, leans on or is hidden by real geometry: the door he cuts, a bonnet, a barrier. In the cutter shots the cutter jaws sit on the door pillar (pinned with `world_to_local`).
- **Hero prop.** The cutter is drawn on the card in wide and medium shots. In macro inserts it is a 3D model with at least 15 parts: jaws, cylinder, handle, trigger, battery pack with 3 bar LEDs, hose-free body, strap.
- **Sharpness.** Puppets are excluded from DOF (the actor index mask) and streak only above 40 px/frame (7.5).

---

## 5. Light

### 5.1 Rig (L section 6; energies are **predicted**, so calibrate them with the LS 4.3 white-card test first)

| Source | Build | Colour | Target on screen |
|---|---|---|---|
| Sky / moon | World: gradient `#4a4f76` (top) to `#989dbd` (cloud gaps), hue 228-236. Moon disc at upper left on the cloud dome, no bloom. **World light to diffuse rays = 0** (Light Path `Is Diffuse Ray` → strength 0), so the world only shows to camera and glossy rays | | Sky 2.5-4x the ground luma. Cloud deck is the brightest large area. Optional sodium-polluted horizon undersides, hue 25-35 at S ≤ 0.25, under 10 % of frame |
| Ambient | LS emission term A in every set material: `Emission = albedo x A`, A = blue hue 230-240 at 0.05-0.08 linear | | Shade out of any pool reads `#17161d`-`#1e1c26`, hue 245-262 |
| Sodium masts | Spot Light per head, pointing down. Spot size 60-70 deg, blend 0.4-0.5, radius 0.1-0.15 D (hard shadows). Visible bulb = separate emitter mesh, strength 8-15, `emission_sampling NONE` | Light (1.0, 0.45, 0.12) linear. Bulb `#fdf9c9`-`#ffd27a` above 1.0 linear | Pool `#74421e` (hue 22-30, S 0.65-0.8), radius 6-10 D, falls to black within one radius. Starting energy from LS 4.2: energy = g x 4 pi^2 d^2 with d = 20, g ≈ 1.5 → about 24 000 W (D units). Calibrate it |
| Emergency red beacons | Rescue pickup light bar, plus 1-2 police or highway units down the row. Point or spot Lights, radius 0.05-0.1 D. Emitter meshes as above | `#ff1a1a`-`#e0201c`, hue 355-5 | Strobe 2-3 Hz, alternating left/right, about 50 % duty, 2-frame ramps (no 1-frame pops). Wet-road spill hue 0-10, S ≥ 0.7 within 3-5 D. Never the key: red chroma share 8-15 % |
| Hazard lights | 3-6 abandoned cars blinking amber at 1.5 Hz (emitter only, plus a small Light on the 2 nearest) | `#ffa31a` | orange accents |
| Headlights | 2-4 abandoned cars with headlights on: spot Lights at 25-35 deg cone, emitter lens mesh | warm white | long road reflections, rain lit in the beams |
| Fires | 2-4 burning wrecks: flipbook emission card (8 code-drawn frames) plus one point Light flickering ±25 % at 6-10 Hz random | `#e2bb6c`, core `#ffffd0` | local orange. They do not light the far scene much |
| Cars facing a lamp | (falls out of the rig) | | orange rim on the lamp side, `#080708`-`#15141c` on the far side |

- **Key direction rule** (stage REVIEW, trap 3): the head's crescent and thick ink sit at the lower right, so the dominant light on Kong should come from screen upper left, or set `actor.head_flip` as v3 does.
- **Light budget.** Real Light objects only within about 250 D of the camera and in or near the frustum.
  - Farther masts keep the bulb mesh and get a **pool card**: an emission-free ellipse decal, a slightly glossy orange-tinted asphalt patch, or an additive emission plane at strength ≤ 0.3 with `emission_sampling NONE`.
  - Light tree on (Cycles default).

### 5.2 Light-sampling traps (cost and noise)

- The ambient-emission term turns every set material into an emitter. Set `material.cycles.emission_sampling = 'NONE'` on every ambient-term, `painted` and bulb material. Only Light objects are sampled as lights. **To verify** the property name in bpy 5.3; it exists since Blender 3.5.
- Glossy fireflies from small bright bulbs mirrored in puddles. Counter them with:
  - `sample_clamp_indirect` 3-5,
  - `blur_glossy` (Filter Glossy) 0.5-1.0,
  - OIDN with albedo and normal guides.
- Persistent data stays OFF (stage REVIEW 1: it saves nothing and causes stale sprites). Revisit only if scene sync exceeds 3 CPU s, and then with `render.drop_cache` discipline.

---

## 6. Atmosphere: fog, cones, smoke, rain

None of these goes through a Cycles volume.

### 6.1 Fog (post, from the Z pass)

Fog is two terms. Both are computed in linear light before the grade.

- **Extinction lift.** `out = c x T + F x (1 - T)`, with `T = exp(-z / z0)`.
  - Start with z0 = 300 D and tune it on check 9.
  - F = fog colour = base `#2a2a36` (encoded) + 0.15-0.3 x Gaussian(σ 80-120 px) of the emitters-only image, so fog glows warm near sodium and red near beacons.
  - Effect: mid rows (100-300 D) lift by +0.03-0.08 luma.
- **Horizon band.** Sky, skyline and pixels with z > 1500 D get the inverted-fog band, luma 0.18-0.30 (L: 0.20-0.47 in the ref), so far cars at 300-1000 D read as dark silhouettes (luma 0.03-0.06) against it.
- **Mist layer.** 0-0.8 D above the deck, +0.03-0.05 luma: a soft gradient by screen distance to the road mask, or a thin additive card at deck level.

### 6.2 Light cones (cards)

- Under each of the nearest 4-8 sodium heads and each active headlight: a cone mesh with an emission gradient, transparent, `emission_sampling NONE`, `visible_shadow` off. Brightest at the lamp; alpha 0.08-0.15 at the bulb, 0 at the pool.
- Rain inside the cone is brighter (6.4 does this automatically).

### 6.3 Smoke and steam (cards)

- 3-6 plumes from wrecks, `#86838e` (luma 0.45-0.55, hue about 254), 40-70 px wide at mid distance, densest at the base, fading upward over about 150 px.
- Camera-facing cards with an 8-frame code-drawn alpha flipbook, slow upward UV scroll. Emission tinted by the sky, plus +20 % warm where a fire sits below.

### 6.4 Rain (post, 2D, per frame), L5 and resolution 3

- **Fresh set every frame**, seeded by film frame g so it is reproducible. Ref C has no continuous drop motion.
- **Generate 180-240 streaks** in three depth classes. Each streak gets a random depth.

| Class | Depth | Count | Width | Length | Notes |
|---|---|---|---|---|---|
| near | 1.5-6 D | 15-25 | 2-3 px | 60-110 px | Gaussian-softened σ = CoC at that depth (7.4) |
| mid | 6-40 D | 90-120 | 1.5-2 px | 22-45 px | |
| far | 40-150 D | 70-100 | 1 px | 10-20 px | |

  Median length ends up 25-30 px and p90 80-95 px (L).
- **Angle.** Vertical ±3 deg, the same for the whole shot. Up to 8 deg in one wind-gust shot if wanted.
- **Occlusion.** Draw a streak pixel only where the scene Z at that pixel is greater than the streak depth. Puppets occlude through the actor mask with their card depth.
- **Light.**
  - Added luma = 0.04 + 0.6 x Lb, where Lb = Gaussian(σ 25 px) of the scene's linear luminance, clipped to 1.
  - Colour = 50/50 mix of the normalised blurred local colour and cool white `#c8d0e0`.
  - Effect: streaks take sodium orange or beacon red near lights and drop to 20-30 % opacity over unlit black.
- **Splashes.** 30-60 per frame: 3-6 px bright ellipse ticks inside the road mask at z < 60 D, living 2-3 frames.
- **Puddle rings** (optional): 3-6 px ring normals in the near puddles in post, or skip them. The ref does not resolve them.
- **Order.** Rain goes after DOF and before motion blur (section 8).

---

## 7. Camera, edit, DOF, motion blur (C section 9 plus the director's brief)

### 7.1 Lens and heights

- **Lens.** Default 32 mm (59 deg vertical). 22-24 mm at ground level, in a car or POV. 40-60 mm for long-lens high angles that stack the gridlock rows (like f_102/f_108) and for macro (cutter jaws, battery bars, phone).
- **Heights** (D above the deck):

| Angle | Height | Pitch |
|---|---|---|
| Eye | 2.5-3 D | 0-3 deg down |
| Low | 0.5-1.5 D | 5-10 deg up |
| High | 6-25 D | 8-30 deg down |

  Top-down only for the ending rise (brief). Ref C never goes past 35 deg.
- **Angle budget** across EP.1: high about 40 %, eye 30 %, low 15 %, insert/macro 5-8 %, transitions 8-10 %. At least 5 angle types (brief). Dutch 8-15 deg only from the driver lifting his head onward.

### 7.2 Moves

| Item | Target |
|---|---|
| Setup length | median 1.3-1.6 s; a framing change every 1.1-1.7 s |
| Drift | zoom 5-17 %/s (median 9), pan about 70 px/s, push-ins and pull-outs about equal |
| Snap / whip | 7-16 frames, peak 1500-4000 px/s at the frame corner, 2-8 % zoom per frame, eased (`SINE` or `QUINT` + `EASE_IN_OUT`, written through channelbags, API rows 72-74) |
| Static | ≤ 14 frames, except icon reads (30-60 frames) and the final hold |
| Camera path | ref C moves like a drone through one connected world. Prefer one continuous camera per take with fly-throughs between setups |

### 7.3 Transitions

- No cross-dissolves.
- Hard cuts for time jumps.
- 1-2 impact-flash cuts per episode: a white star with ink outline, 150-250 px, for 2-4 frames, plus thin white arcs with glow (radius 80-130 px) for 8-12 frames.
- At most 2 whip/snap transitions (brief).
- At most 1 torn-paper or white-flash wipe.

### 7.4 Depth of field (post, from Z; never Cycles DOF, API row 70)

- CoC sigma in px: `s(z) = K x |1 - z_f / z|`, clamped to 10 px. z_f is the focus depth: Kong, or the cutter in inserts.

| Shot | K (sigma at infinity) | Check |
|---|---|---|
| Wide / establishing | 1.0-1.5 | background/actor Laplacian energy ratio 0.28-0.47 |
| Medium | 1.5-2.5 | |
| MCU (Kong, low) | 3-4, so background at 3 z_f gets about 2.5-3 px | background/actor ratio 0.04-0.11 |
| Macro insert | 6-10 | subject plane σ ≤ 0.5. Near and far 4-8 px, wet asphalt and beacons turn to round bokeh. Use a disc kernel for pixels above 1.0 linear |

- **Implementation.** 6-8 depth slices, premultiplied Gaussian (disc for highlights) per slice, composited back to front. Actor pixels (index mask) are excluded and laid back on sharp.
- Optional: the compositor Defocus node on the Z input. **To verify** in 5.3: socket names, and that it works with `compositing_node_group`.
- Cycles DOF only if a 360x640 OIDN test proves it adds no noise (C's decision, kept).

### 7.5 Motion blur (post)

- Reuse the v3 method (`v3/shots/post.py`): fit a camera similarity from g-1, g, g+1. Streak along the motion over a 0.5-frame shutter (C), where the frame corner moves above 20 px per frame.
  - Above 40 px/frame: the whole frame, actors included.
  - 20-40 px/frame: plate only. Actors sharp, using the index mask, or `render_layers.py` plate/matte on those few frames if ghosting shows.
- Icons and captions are added after this step: always sharp.
- Optional alternative: a Vector pass plus the Vector Blur node (**to verify** in 5.3). It handles per-object motion (a swinging car door), which the similarity fit cannot.

### 7.6 Post finish

- Vignette -5 to -10 % at the edges (an ellipse mask, feather about 0.5, multiply 0.92), no ring.
- No grain, no sharpening, no chromatic aberration.

---

## 8. Post chain, in order

Blender writes one half-float multilayer EXR per frame with these passes:
- Combined.
- Depth (Z, API row 64).
- Object Index: road 1, actor cards 2, sky/world 0, icons none. With alpha cards the index respects `pass_alpha_threshold` 0.5, so the actor matte comes free in the same render.
- Light groups `base`, `red`, `amber`. **To verify:** `view_layer.lightgroups.add(name=...)`, `object.lightgroup = name`, and `world.lightgroup`.

`post_c.py` (numpy/OpenCV, in linear light until the grade) runs:

1. **Strobe re-mix** (only when light groups are present): `base + red x r(g) + amber x a(g)`. This animates strobes without new noise, and lets a static icon-hold plate be rendered **once**.
2. **Night tint of actor pixels** (if not done on the card).
3. **Fog** (6.1).
4. **Road-reflection streaks**, fallback only. Take pixels above 0.6 linear inside the road mask, apply a downward vertical blur of 40-90 px, and add 0.5x.
5. **DOF** (7.4).
6. **Bloom.** `sum_i w_i x Gaussian_i(max(L - 1, 0))` with σ 4, 10, 22 px, weights tuned so the half-height radius is 12-16 px and the tail ends at 35-40 px. Heads and painted surfaces stay below 1.0, so they never bloom.
7. **Rain and splashes** (6.4).
8. **Motion blur** (7.5).
9. **Grade.** View transform Standard. CDL slope (1.0, 0.99, 0.98), night offset (0.004, 0.004, 0.008), saturation 1.00-1.05. Then sRGB encode.
10. **Vignette** (7.6).
11. **Icons and graphics** (section 10): drawn sharp, world-anchored by homography.
12. Write PNG `frames/g_%04d.png`. The conform step adds captions later (CONVENTIONS).

Measured post cost to beat: about 3-4 CPU s per frame in total (section 11).

---

## 9. Acceptance bands and how to measure each

Write the measuring script as `qa_refc.py` in the folder of whoever builds the look (suggestion: `v3/look_c/`). Reuse:
- `scratchpad/work_refC/m1.py` (edges, Laplacian, S, V),
- `scratchpad/rcl/m4.py` (rain detector),
- `scratchpad/rcl/m2.py` (tonal band colours),
- `scratchpad/rcam/dof2.py` (defocus tiles),
- `hue_report.stats`.

Run every check on at least 3 graded stills per shot plus one moving frame, with the caption band masked. "Ref" is the ref C value measured by the lenses.

| # | Check | Pass band | Ref | Method |
|---|---|---|---|---|
| 1 | luma mean | 0.24-0.32 | 0.27 | Rec.709 on encoded values |
| 2 | luma p5 / p50 / p99.5 | ≤ 0.03 / 0.16-0.22 / 0.85-0.97 | 0.004 / 0.19 / 0.85 | percentiles |
| 3 | pixels with V < 0.25 | 35-48 % | 47-48 % | HSV V |
| 4 | clipped V > 0.97 | 0.3-1.5 % | 0.4 % | lamp cores, beacons, headlights only. Heads must read ≤ 0.90 |
| 5 | saturation mean | 0.30-0.40 | 0.33 | HSV S |
| 6 | chroma share by hue family | blue 50-65, orange 15-25, red 8-15, violet ≤ 6, magenta ≤ 3, green ≤ 2 | 71 / 17 / 10 / 1 / 0 / 0 | `hue_report.stats(files)` |
| 7 | shadow colour (luma < 0.25 mean) and midtones (0.25-0.6) | shadows hue 245-262, S 0.15-0.25. Mids `#62637a`-`#6e6d80`, hue 236-250 | `#19171d` h262, `#6e6d80` h244 | `rcl/m2.py` method |
| 8 | warm / cool / emergency-red pixel shares | warm 10-15 %, cool 25-35 %, red 3-6 % | warm 11, cool 29 | warm = hue 340-50 at S > 0.25. Cool = hue 190-260 at S > 0.25. Red = hue 350-10 at S > 0.5 |
| 9 | fog by depth | luma std per depth band (Z pass): near 0.15-0.17, mid 0.09-0.11, far ≤ 0.10. Far-third contrast cut 40-60 % against the same frame without fog. Horizon band luma 0.18-0.30, far cars 0.03-0.06 | f_067 bands | needs the Z pass; render one frame with the fog step skipped |
| 10 | sky / ground luma | 2.5-4x | 4.1 | sky = index 0 pixels, ground = road index |
| 11 | sodium pool | mean `#74421e` ± 12 levels, hue 22-30, S 0.65-0.8. Falls to below 0.12 of pool luma within one pool radius | `#74421e` | sample a disc in the pool |
| 12 | wet road | 3-6 % of road pixels specular (V > 0.7, S < 0.3). Open wet road mean hue 228-249. Every emitter in frame has a reflection streak 3-6x longer than wide | 3-5 % | road index mask; count streaks by eye on a sheet |
| 13 | bloom profile | radial luma from a bulb centre: half height at 12-16 px, background by 35-40 px. No bloom ring on heads | r12 0.74, r32 0.41 | `rcl/m3.py` profile method |
| 14 | detail density | ≥ 12 prop kinds, ≥ 40 instances, 3 depth layers | 15-25 kinds, 40-80+ | count from the scene: objects with projected bbox ≥ 4 px and visible (`world_to_camera_view` plus an index/cryptomatte hit) |
| 15 | world extent (wides) | ≥ 20 cars visible, smallest ≤ 15 px wide, vanishing point inside frame, masts every 50-67 D | rows 400 → 21-45 px | from the scene projection |
| 16 | edge density, stills | top third 2-6 %, middle 6-18 %, bottom 8-30 %. Fast frames may drop to 1.5-4.5 % per band | M table | `work_refC/m1.py` (Canny 60/140 after 3x3 blur) |
| 17 | sharpness profile | Laplacian variance per 160 px band: top band < 50 (sky), peak band between 0.55 and 0.85 H, background 5-30x below the peak; last band softer than the peak when an FG layer is present | f_067: 11 / ... / 13389 / 12978 / 5964 | `m1.py` band variant |
| 18 | DOF by shot size | wides: tiles above σ 1.5 ≤ 15 %, background/actor Laplacian ratio 0.28-0.47. MCU: ratio 0.04-0.11, background σ 2.5-3.5. Macro: subject σ ≤ 0.5, near/far 4-8 | C section 4 | `rcam/dof2.py`, calibrated on f_102 |
| 19 | rain | detected streaks 50-110 per frame; coverage 0.6-1.5 %; median length 21-30 px, p90 70-95; width 1.5-2.2 px; angle median within 3 deg of the shot's set angle; contrast +0.15 to +0.4. Positions uncorrelated between consecutive frames (overlap of streak masks < 5 %) | L5 | `rcl/m4.py` detector unchanged |
| 20 | puppet size and placement | Kong 0.15-0.30 H (wide/medium), 0.45-0.5 (MCU). Head-centre band and whole head above y 880 (CONVENTIONS) | M8 | `probe.py`-style projection |
| 21 | puppet head colour | `#dcd3dc`-`#e6dee4`, luma 0.82-0.88 | `#e0d6dd` | 9 points inside the head |
| 22 | puppet grounding | contact ellipse present, 1.2-1.6x stance, 0.6-0.8 of local ground value. Kong touches or is occluded by geometry in every shot. Card reflection visible on wet ground | M8 | sheet check plus a value sample |
| 23 | lens | 32 mm default. Every shot's lens logged and within its class (7.1) | C3 | from `camera.data.lens` |
| 24 | camera motion | framing change every 1.1-1.7 s. Static runs ≤ 14 frames except tagged icon holds. Whips 7-16 frames, peak 1500-4000 px/s. Drift zoom 5-17 %/s | C2 | `v3/shots/qa_motion.py` |
| 25 | motion blur | streak length 0.4-0.6 of the per-frame displacement on fast frames. Actors streak only above 40 px/frame. Icons sharp | C5 | `qa_motion` speed plus a sheet |
| 26 | vignette / grain / sharpening | edges at mid-height 0.90-0.95 of centre on the mean image. Flat-block high-pass std ≤ 0.5/255. No halos | C6 | mean of all frames in a shot |
| 27 | red strobe | beacon flicker 2-3 Hz, no 1-frame pops (popcheck) | brief | `v3/shots/popcheck.py` |
| 28 | icons | world-anchored ones stay registered (≤ 2 px drift against their anchor). Nearest icon 0.12-0.2 W. Pop per section 10. About one every 4-6 s. Never on the caption band | C7 | projection of the anchor quad |
| 29 | cost | ≤ 30 CPU s per final 720x1280 frame, averaged per shot. No single frame above 40 | section 11 | `time.process_time` of all processes, or `/usr/bin/time` user+sys |

---

## 10. Icons (brief plus C7)

- **Library and colours.** From `plan/BRIEF_camera_and_icons.md`: battery bars by the cutter, phone with a red "4" badge, broken pinky, sound-wave rings, eye with red pupil, 60 s stopwatch, warning triangle, "!" spark lines, "?" swirl, sweat drop, red light rays. Palette: red `#e2453b`, yellow `#ffd23f`, infected green-grey `#8fa37a`, white `#f4f1ea`, ink `#1f1d24`.
- **Style.** Flat fill about 90 % opaque, thick rounded strokes, slightly wobbly ink (brief).
- **Placement.**
  - **World-anchored** wherever an icon labels an object: X over wrecked cars, a check on the passable lane, battery bars by the cutter, a red pupil over the driver, a "1.2 KM" yellow distance tape laid on the asphalt in the manner of C's "0.9 MILE" tape. Implement each as a 3D quad in the take whose four corners are projected per frame (`world_to_camera_view`). The icon PNG is warped by that homography and drawn in post step 11, so it keeps perspective but escapes DOF, fog, rain and motion blur.
  - Screen-space only for rules (stopwatch, counters).
- **Pop.** 4-frame overshoot 0 → 115 → 100 % (brief, user-requested), or ref C's 2-frame 50 → 100 %. Pick one per episode and keep it.
- **Series.** Stagger 2-4 frames apart, near to far. Nearest icon 0.12-0.2 W. Hold the camera 30-60 frames on a read.

---

## 11. Render-cost plan (4-core CPU, ≤ 30 CPU s per final frame)

### 11.1 Anchor

v3 office, true 3D, 12 samples, no denoiser: 17.2-20.2 CPU s per frame (`v3/out/QA.md`). EP.1's set is far heavier: many lights, glossy wet road, thousands of instances, denoiser. So the plan moves every effect that is not geometry or direct light out of Cycles.

### 11.2 What goes where

| Effect | Where | Why |
|---|---|---|
| geometry detail, bevels, panel lines | 3D (bevels applied at build, panels as normal maps) | parallax is the look |
| wet reflections, card reflections | 3D (glossy_bounces 1) | free with the road material; impossible to fake well |
| sodium pools, beacon spill, headlights, hard shadows | 3D Light objects near camera; pool cards far | real shadows from cars and puppets |
| ambient shade | emission term in materials (`emission_sampling NONE`) | noise-free, zero samples |
| sky, skyline, windows, bulbs, tail lamps | `painted` emission, not sampled as lights | zero light-sampling cost |
| strobes, hazards | light groups re-mixed in post | static plates reusable, no new noise |
| fog, horizon band, mist | post from Z | a volume would cost 3-10x |
| light cones | emission cone cards | as above |
| smoke, steam, fire | flipbook cards plus one flickering Light per fire | as above |
| rain, splashes | post 2D, per frame | regenerated each frame like the ref; zero Cycles cost |
| DOF | post from Z | API row 70; Cycles DOF needs samples |
| motion blur | post (v3 similarity streak) | Cycles MB needs samples |
| bloom, grade, vignette | post | as LS |
| icons | post, homography from projected quads | stays sharp, as in the ref |

### 11.3 Cycles settings

- CPU, `threads` 2 per process, one render process per agent (CONVENTIONS), so each frame has ≤ 15 s wall.
- Samples: 16, adaptive on, threshold 0.05, min 8. Fixed seed. OIDN with albedo and normal, prefilter `FAST` (**to verify** the enum name). Tests: 360x640, 8 samples, OIDN.
- Bounces: max 2, diffuse 0, glossy 1, transmission 0, volume 0, transparent 12. Caustics off. Clamp direct 0, indirect 4. Filter Glossy 0.7.
- Light tree on. Lights culled beyond about 250 D (5.1).
- Textures ≤ 2048 px. Total texture memory ≤ 1.5 GB. Instances via linked meshes or collection instances (API row 43). Modifiers applied. Persistent data off (stage REVIEW).
- Motion blur off, DOF off, no volumes, no Freestyle (CONVENTIONS).

### 11.4 Per-frame budget (CPU s, 720x1280)

| Stage | Budget |
|---|---|
| sprite raster (Chromium), per actor in frame | 0.3-0.5 (x 1-3 actors) |
| scene sync and BVH | ≤ 3 |
| path tracing, 16 samples adaptive | ≤ 18 |
| OIDN | ≤ 3 |
| EXR write and read | ≤ 0.5 |
| post (fog 0.3, DOF 1.0, bloom 0.4, rain 0.5, streak 0-1, grade, vignette and icons 0.4) | ≤ 4 |
| **total** | **≤ 30** |

### 11.5 Plates where the camera allows (LS tier idea, used sparingly)

- **Icon holds and the end hold (30-60 static frames).** Render the set once with light groups. Re-render only the actor cards per frame with the rest as holdout, or composite sprites in 2D if the actor does not move in depth. Strobes and rain are post. Cost: one frame for the whole hold.
- **Long-lens (40-60 mm) high drifts of the far rows.** Parallax is small. Render a 1.5x plate and move it in 2D (check `qa_parallax.py`; C's long-lens rows are close to flat).
- Everything else: every frame in 3D.

### 11.6 Gates (run in this order before building shots)

1. **Calibration still at 360x640.** White card under one sodium spot and one beacon (LS 4.3), then the wet-road patch: check 11 and check 12.
2. **Cost gate.** One wide (≥ 20 cars, ≥ 10 Lights) at 720x1280, 16 samples, 2 threads, timed over 3 frames.
   - Over 30 CPU s: (a) samples 12 with OIDN; (b) cull Lights to 150 D and use more pool cards; (c) render at 75 % (540x960), Lanczos up. Ref C is codec-soft with no sharpening, so re-check 16 and 17 after the upscale; (d) the shot becomes a plate per 11.5.
   - Over 45 CPU s after (a) to (c): simplify mid-LOD cars before anything else.
3. **API gate** (no build until each is answered): `emission_sampling`, light groups on the view layer and objects, the OIDN prefilter enum, the Defocus or Vector Blur nodes if you use them, and the World Light Path trick for diffuse rays.
4. **Look gate.** One graded 360x640 still per depth layer setup, measured with checks 1-19, then a contact sheet beside `ref/c/frames2/f_066.png`, `f_067.png`, `frames/f_017.png` and day-rain f_070 (rain density only).

---

## 12. Open questions

1. The 1 D = 0.6 m world scale is a judgement. It makes the puppet the height of a real adult beside real cars, as in ref C (puppet next to vehicles). Change it only before the set is built.
2. The ref C night grade rests on two frames (f_066, f_067; L1), and the rain numbers come from day rain. Bands 1-8 are therefore wider than one frame would give. Re-centre them after the first approved still.
3. Emergency red is not in ref C. Its 8-15 % chroma share comes from the story palette (L). If it pushes violet above 6 % in fog, lower the red fog-glow weight first (6.1), not the beacons.
4. Director decisions: whip count (ref C 6 vs brief 2), icon pop style (2-frame vs 4-frame overshoot), and the camera lens rule for the brief's 9:16 / 16:9 double framing. The 16:9 framing at 32 mm needs the deck about 1.8x wider on screen: model barriers, median and the opposite carriageway fully.
5. `hue_report.py`'s main still crashes until its reference paths point at existing frames. That needs a fix by the owner of `v3/tools`, not by shot agents. Until then, import `stats()`.
