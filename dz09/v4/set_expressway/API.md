# v4/set_expressway: EP.1 Bangkok elevated expressway, night, heavy rain (detailed 3D set)

Folder: `PROJ/v4/set_expressway/` (PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`).
bpy 5.3, Cycles CPU, no Freestyle, no EEVEE, no network. Spec: `PROJ/spec/LOOK_SPEC_C.md` (look of ref C). Only files in this folder were written; `v4/cast_dz09` (stand-in actors) and `v3/tools/hue_report.py` are imported read-only.

World scale: 1 BU = 1 D = 0.6 m. Z is up and the deck top is at z = 0. The city floor is at z = -30.

## Files

| File | What it does |
|---|---|
| `expressway.py` | The set. `build()`, render setup, the 8 camera presets x 2 aspects, `render_still()` (EXR passes + post). |
| `vehicles.py` | Procedural vehicles. Lofted cars of 6 types (sedan, taxi, hatch, pickup, SUV, van), wheels, opening and dented doors, a crumple deformer, the interior with a RHD driver seat, motorbikes with green delivery boxes, the rescue pickup (livery, light bar, floodlight mast), a 6-wheel truck, a bus, and the 3D rescue cutter (29 parts). |
| `kit.py` | bpy helpers: the material builder `MB` (Principled + ambient emission term, `emission_sampling = NONE`), loft, lathe, sweep, bmesh bevel, quad, instancing, look-at with roll/up, keyframes with a CYCLES modifier. |
| `tex.py` | Code-drawn textures (numpy + PIL, Thai set in Kanit through raqm), cached in `tex/`: green gantry signs, amber LED message board, Thai plates (fake numbers), RESCUE 09 livery, delivery-box pictogram, tower windows, city streets, spiderweb windscreen crack, rain droplets, smoke and fire flipbook cards, car panel-line maps. |
| `post.py` | The LOOK_SPEC_C post chain on the EXR passes: fog from Z, DOF from Z, bloom, rain streaks and splashes, CDL grade, vignette, magenta clamp, sRGB. |
| `standins.py` | Optional. Puts `cast_dz09` actors on the anchors: Kong (wet, cutter, 3 bars) and the driver seated in the hero car. Used for drafts only; shots own their actors. |
| `drafts.py` | Draft renders of every preset in both aspects, sheets, the reference comparison, the hue report, the final-frame timing, and `repost` (re-run post on kept EXRs). |
| `out/` | `drafts/` (16 drafts, `_raw.png` without post, `_z.exr` depth, `_depth.png`), `sheet_916.jpg`, `sheet_169.jpg`, `compare_ref.jpg`, `hue.txt`, `timing.json`, `anchors.json`, `final/` (the timed 720x1280 frames with all passes). |

## How to call it

```python
import sys; sys.path.insert(0, PROJ + "/v4/set_expressway")
import bpy, expressway as X

A = X.build()                        # ~5 s; clears the file (read_factory_settings) and builds everything; returns anchors
X.setup_render(quality="draft", threads=2)     # preview 4 spp | draft 8 | final 8 @75 % (= final8) | final12 12 @75 % | native 16 @100 %; shafts="post" (default) or "cards"
cam = X.use_camera("eye", "9:16", scale=0.5)   # 360x640 test; scale=1.0 -> 720x1280 (16:9 -> 1280x720)
# ... add your actors (cards must be pass_index 2 so DOF keeps them sharp), pose them for `cam` ...
r = X.render_still("/abs/out/eye_916", frame=7)  # returns dict of paths and cpu/wall seconds
# r["png"]        graded 720x1280 frame (post applied)       r["raw"]  same composite without post
# r["z"]          <out>_z.exr  planar camera depth in D, 32-bit float (sky 1e10)
# r["depth_png"]  <out>_depth.png  16-bit, z / 2000 D
# r["rgb"], r["env"], r["idx"]  geometry (premultiplied, film transparent), sky (Environment pass), object index
```

- `X.build(clear=True, seed=9, with_city=True, haze_cards=True)`.
- `X.CAMERAS` lists the 8 preset names. `X.use_camera(name, aspect)` also:
  - retargets every camera-facing card (smoke, steam) to the camera;
  - shows the 3D cutter only for presets that ask for it (`macro_cutter`);
  - stores `cam["focus"]` (world point) and `cam["dof_k"]` (DOF strength) for post.
- `X.P(s, o, z)`: world point at path length s, lateral offset o, height z. `X.heading(s)`: the deck direction there. For s < 420 the deck is straight and `P(s, o, z) = (o, s, z)`.
- `X.anchors_json(A, path)`: writes the anchors.
- Command line:

```
python3 drafts.py drafts [--threads 2] [--only eye,high] [--no-actors]   # out/drafts/<preset>_916|169.png
python3 drafts.py sheets                                               # sheet_916.jpg, sheet_169.jpg, compare_ref.jpg
python3 drafts.py hue                                                  # out/hue.txt
python3 drafts.py timing eye --threads 2 [--quality final|final8|native] [--no-haze]   # out/timing.json
python3 drafts.py repost <out_noext> <preset> <9:16|16:9> <focus_z> <k>  # post again on kept EXRs
```

### Post options

Pass `post_opts` to `render_still`, or put them in the `info` dict of `post.process`:

| Option | Default | Effect |
|---|---|---|
| `fog_z0` | 300 D | fog extinction depth |
| `dof` | True | depth of field on/off |
| `k` | per preset | DOF sigma at infinity, px at 1280 |
| `bloom` | 0.55 | bloom strength |
| `rain` | True | rain streaks and splashes on/off |
| `rain_angle_deg` | 2 | rain angle; keep it the same for a whole shot |
| `rain_density` | 1.0 | rain amount |
| `frame` | | seeds the rain, so it is regenerated every frame and reproducible |
| `no_magenta` | True | the magenta clamp in the grade |

Motion blur is not in `post.py`. Moving shots reuse the v3 similarity streak (`v3/shots/post.py`), or add a Vector pass.

## Layout (D)

Path: straight for s from -260 to 420, then a left curve of radius 1500 D to s = 1400, then straight to s = 3000. o is the lateral offset, + to the right of traffic heading +s.

| Element | Where |
|---|---|
| Our carriageway, the gridlock (heading +s, Thai left-hand traffic) | o -22.15 .. -0.75 |
| Lane centres | 1: -3.65, by the median, yellow edge line; 2: -9.45; 3: -15.25 |
| Hard shoulder | -18.15 .. -22.15 |
| Opposing carriageway | o 0.75 .. 22.15, nearly empty |
| Median F-barrier | o ±0.75, 1.6 D tall, with a W-beam rail on our side |
| Outer F-barriers | o ±22.15 .. 23.1, with two galvanised rails on posts every 3 D |
| Slab | 2.4 D deep |
| Piers | every 50 D, down to the city at z = -30 |
| Expansion joints | every 50 D |
| Gutter drains | every 25 D |
| Lamp masts (twin-arm, sodium) | on the median every 60 D from s = -90; heads at o ±5.45, z 19 |
| Sodium spot Lights | for masts with s from -40 to 260: 10 heads, 72° cone, radius 0.12 D, hard shadows, soft light-cone cards |
| Far masts | bulb emitters plus additive pool decals out to s = 1700 |
| Sign gantry | s = 180; truss of 4 chords plus diagonals; green signs ดินแดง / Din Daeng with an exit tag 2-04 and พระราม 9 / Rama IX, lit by sign lamps; amber LED board อุบัติเหตุข้างหน้า / ACCIDENT AHEAD SLOW over lane 1 |
| City | 76 towers at 1700-5200 D (window textures, 5-15 % lit, warm and cool; 8 aviation lights blinking at 1 Hz); 140 low-rise blocks beside and under the deck; a street-light ground plane; 3 haze-layer cards |
| Sky | world gradient (zenith `#1e2948` to cloud gaps `#8c98b8`), noise cloud deck, moon upper left, a faint sodium glow at the horizon. Seen by camera and glossy rays only: diffuse rays get 0 and the world is never light-sampled. |

The hero cluster sits at s -10..95. It has 19 individually built cars, the rescue pickup, 4 motorbikes, a bus and two 6-wheel trucks.

| Car | Built as |
|---|---|
| hero_car (s 34, lane 2) | silver sedan, front crumpled, crumpled driver door ajar 9° (the cutter's target), airbag, see-through cracked windscreen, see-through side glass, interior with a RHD driver seat |
| car_ahead | pickup, hazards |
| l1_a, l1_c, l3_a, l3_b, sh_a, opp_b | doors open |
| l2_c | crashed, hazards |
| l2_b | headlights on (real spot Lights and beams) |
| opp_a | headlights toward the default cameras |
| opp_burn (opposing side, s 112) | burning SUV: fire cards plus a flickering Light, smoke plume |

The rows continue to s = 1350 as 339 collection instances of 8 proto cars. Colours come from `Object Info > Random`; some protos have hazards or an open door.

Debris:
- about 360 glass shards in 3 piles;
- 7 cones, one knocked over;
- 3 water-filled barriers;
- plastic bags, a shoe, an umbrella, a phone, a hubcap, a bumper shard, a mirror, wet paper;
- a medic bag, an open cutter case, a crowbar;
- a cable from the floodlight mast to the tailgate.

Smoke and steam cards: steam from the hero car's bonnet, the burning wreck's plume, and 4 distant plumes down the road.

## Anchors (`A`, world units; `out/anchors.json`)

| Key | Value | Meaning |
|---|---|---|
| `kong_mark` | (-6.72, 33.61, 0) | Kong's feet at the hero car's driver door. A contact-shadow decal is there. |
| `kong_to_door_deg` | -101 | Z rotation that turns a -Y front toward the door (stage25 `facing_deg`). |
| `crew_mark` | (-5.96, 36.21, 0) | the crew member by the front wing. It has a decal. |
| `kong_phone_mark` | (-5.2, 28.0, 0) | a clear spot for the phone call. |
| `driver_seat` | (-9.18, 33.00, 1.29) | top of the driver cushion (hip point). The seat faces `hero_heading`. |
| `driver_head` | (-9.23, 32.76, 2.43) | where the seated driver's head is. |
| `door_pillar`, `door_mid` | | driver-side B pillar and the middle of the crumpled door (pin the cutter jaws here). |
| `windscreen` | | centre of the cracked windscreen. |
| `hero_heading` | -0.192 rad | heading of the hero car (local +Y). Its local +X, the driver side, is `(cos h, sin h)`. |
| `cutter3d`, `cutter_jaw`, `cutter_leds` | | the 3D cutter object; its jaw tips (0.22 D into the door seam at the B pillar); its LED gauge. |
| `rescue_truck`, `flood_head`, `tailgate` | | Kong's pickup on the shoulder at s 21; the floodlight head; behind the tailgate. |
| `burning_car` | (14.6, 112, 1.6) | |
| `key_dir` | (0.62, 0.73, -0.29) | travel direction of the hard key. |
| `lamp_heads` | | the 18 sodium heads with s < 400. |
| `gantry_s` | 180 | |
| `lanes` | | lane centres. |
| `cams` | | the preset table below. |

## Light (all keyframed, so any frame renders on its own)

- **Hard key**: `flood_key`, a spot on the rescue truck's mast aimed at the hero car's driver door.
  - 30 000 W, 44° cone, radius 0.06 D, so cast shadows are hard.
  - For the default cameras it comes from the upper left, as the puppet crescent rule wants (stage REVIEW, trap 3).
  - A soft beam card shows the cone.
- **Sodium**: 10 spot Lights, 26 000 W, colour (1.0, 0.45, 0.12), with real shadows. The bulbs are emitters at strength 14.
- **Beacons**: 2 red and 2 blue domes on the light bar, each with a point Light.
  - 2.5 Hz (12-frame cycle), left and right alternate, red and blue in opposition.
  - 2-frame ramps, about 50 % duty.
  - Both the emission and the Light energy are keyed, with a CYCLES modifier.
- **Hazards**: the shared amber material blinks at 1.5 Hz (20 frames). Two small Lights are on the nearest hazard cars.
- **Headlights**: 4 spot Lights on 2 cars.
- **Fire**: one point Light with a NOISE modifier, ±50 % flicker.
- **Aviation lights**: emission, 1 Hz.
- **Ambient**: in every set material, `Emission = albedo x (0.030, 0.040, 0.088)` (hue about 236), with `emission_sampling = NONE`. Shade is therefore blue and noise free.
- **Tail lamps**: `#ff1a1a` at strength 2.4.

## Camera presets (`X.use_camera(name, "9:16" | "16:9")`)

Sensor 36 mm, fit AUTO, so the 36 mm lies on the long side in both aspects. Each 16:9 preset is the same scene with its own override, listed here as "16:9 changes".

| Name | 9:16 | 16:9 changes | Focus / DOF k |
|---|---|---|---|
| `low` | (-3.0, 25.6, 0.75) toward (-8.2, 36, 3.3), 24 mm, pitched up about 11°. Kong looms by the crashed car, lamps above, debris in the foreground. | (-2.6, 24.6, 0.8) toward (-8.5, 36, 2.6) | Kong's head / 2.0 |
| `eye` | (-2.2, 22.4, 2.75) toward (-8, 40, 2.2), 32 mm. Kong at the driver door, the gridlock, gantry signs, skyline. | (-1.6, 21.2, 2.75) toward (-7.5, 40, 2.3); the median and the opposing lanes come in | Kong's head / 1.8 |
| `high` | (6.5, 2, 20) toward (-9.5, 44, 0), 40 mm, about 25° down over the opposing lanes. The rows stack toward the curve; burning wreck. | 35 mm | Kong's feet / 1.2 |
| `top_down` | 72 D overhead, up = +s, 32 mm. The gridlock's scale, the rescue zone, beacon spill. | 60 D, up = +x, so the deck runs across the frame | Kong / 1.0 |
| `dutch` | (-3.9, 28.6, 2.25) toward the driver window, 28 mm, roll 12° | 26 mm | driver's head / 2.2 |
| `ots` | Kong's mark + (1.45, -1.75, 3.15), looking at the crumpled door, 32 mm. Kong's card fills one side; the driver is visible inside. | + (1.8, -2.4, 3.1) | door / 2.6 |
| `pov_windscreen` | 2.35 D ahead of the windscreen and 0.55 up, looking at the driver's head through the spiderweb crack, 24 mm | 22 mm | driver's head / 3.0 |
| `macro_cutter` | the cutter's own frame (0.25, -1.2, 0) looking along it, 45 mm. Battery LED gauge sharp, the cylinder and jaws biting the door seam soft behind. The 3D cutter shows only here. | 38 mm | LED gauge / 7.0 |

## Passes and post (LOOK_SPEC_C 6-8)

The film is transparent. One EXR per pass is written by the compositor's File Output node: `_rgb.exr` (premultiplied geometry, RGBA), `_env.exr` (Environment pass), `_z.exr` (planar depth), `_idx.exr` (object index).

Object index:

| Index | What |
|---|---|
| 0 | sky |
| 1 | road |
| 2 | actor cards (`standins` sets it; shots must set it too) |
| 3 | car bodies |
| 4 | everything else |

`view_layer.pass_alpha_threshold = 0.99`: only opaque surfaces and cut-out cards write Z.

`post.process` runs these steps in order:

1. Clean the passes. Alpha, Environment and Z are median-filtered where coverage is partial; OIDN denoises colour only.
2. **Fog** on the geometry only: `rgb x T + F x (1 - T) x alpha + env`.
   - `T = exp(-min(z, 650) / 300)`.
   - F = `#2a2a36` + 0.22 x the 100 px blur of the emitters, so fog glows warm near the sodium lamps and red near the beacons.
   - A horizon haze band where the far deck and skyline meet the sky, and a low mist over the road.
3. **DOF**: `sigma = k x |1 - z_f / z|`, clamped at 10 px, from blurred copies at 7 sigmas. Actor pixels (index 2) stay sharp. Above k = 4 the bright highlights become disc bokeh.
4. **Bloom** above 1.0: sigmas 4, 10 and 22 px.
5. **Rain**, regenerated every frame from the seed `frame`:
   - about 210 streaks in near, mid and far depth classes, each hidden by the scene Z;
   - lit by the 25 px blur of the scene, so streaks are orange by the lamps, red by the beacons and faint over black;
   - 45 splash ticks on the road nearer than 60 D.
6. **Grade**: CDL slope (1.0, 0.99, 0.98), offset (0.004, 0.004, 0.008), saturation 1.03.
7. **Vignette**: -10 % at the corners.
8. **Magenta clamp**: hues 258-342° (mixes of red reflections and the blue sky reflection on the wet deck) are turned toward 250° or 355°.

`final` renders at 75 % (540x960) and upsamples colour to 720x1280 with Lanczos, and depth and index nearest, before post (LOOK_SPEC_C 11.6 gate, options a + c).

## Measured

Machine: 4 cores shared with other agents. Load average was 4 to 10 during every measurement, and Cycles got about 1 core: wall time ≈ CPU time.

| What | Number |
|---|---|
| `build()` | 4.5-6.2 s CPU; 2014 objects plus 339 instanced cars, 22 Light objects |
| Draft, 360x640 / 640x360, 8 spp + OIDN, with stand-ins | 12.4-19.6 CPU s render, 0.4-0.7 s post (`out/draft_times.json`) |
| Final 720x1280 `eye` (12 spp at 75 %, Lanczos, OIDN, 2 threads) | render 50.0 CPU s, post 3.8 CPU s, **53.9 CPU s per frame** (load 10) |
| `final8` 720x1280 `eye` (8 spp at 75 %, no haze cards, 2 threads) | render 32.9 CPU s (18.2 s wall), post 5.0 CPU s, **37.9 CPU s per frame** (load 6-9). Visually clean after OIDN (`out/final/eye_916_final8.png`). |
| Profile at 360x640 | scene sync about 4.5 CPU s per frame (persistent data stays off, stage REVIEW 1). Turning off world light sampling saved 30 %. The procedural asphalt costs about 15 %, clearcoat 11 %, the transparent fx cards 17 %. Lights cost almost nothing (light tree). |
| Hue | see `out/hue.txt`. Magenta 0.0-2.3 % and violet 0.1-5.7 % on every preset in both aspects, all within the night band. The eye/low/top-down/dutch frames sit in the night band for blue (50-72 %). Red runs high (18-33 %) in frames full of tail lights (eye, high, ots). Orange is high where the floodlight fills the frame (pov, ots, macro). |

## Known gaps

- **Cost** is about 54 CPU s per frame for `final` and about 38 for `final8`, against the 30 s target, measured under heavy machine load. Ways to cut it further:
  - the `final8` tier;
  - `haze_cards=False` (post already draws a horizon band);
  - clear coat only on the hero cluster (already off on the 339 row instances);
  - cutting sodium Lights to 150 D;
  - plates for holds (LOOK_SPEC_C 11.5).
  Scene sync (about 4.5 s) is paid every frame.
- **Not in post:** motion blur and icons. Icons belong to `v4/iconfx`.
- **The DOF is a gather approximation.** Slight halos can appear where a sharp foreground edge meets a blurred background.
- **Cars are lofted shells.**
  - Panel lines are a bump plus cavity map: no boolean cuts.
  - Pickups have a tonneau cover instead of an open bed.
  - Wheel arches are notches, not liners.
  - Glass on row cars is opaque dark Principled; only the hero car's glass is see-through.
  - The crumple is a noise deformer, not a simulation.
  - Up close the vehicles read cleaner than ref C's textured tanks: there are no decals, mud or scratches.
- **Textures.** Asphalt, concrete and steel are procedural Principled with bump. No photo textures exist, so close-ups are cleaner than ref C's cobble and grass.
- **Fake volumes.** Smoke, steam, fire and light cones are cards, not volumes. Cones fade at their edges but have no real in-scatter, and rain inside them is not brighter in 3D (post lifts streaks near lights instead).
- **Colour:**
  - Red share runs above the night band in gridlock-heavy frames because every abandoned car shows tail lamps at the spec's strength.
  - Saturation and value are a little high in sky-heavy 9:16 frames.
  - The magenta clamp is a grade operation. The source fixes are the bluer sky and haze and the blue ambient.
- **Scale.** At D = 0.6 m (LOOK_SPEC_C), the `cast_dz09` Kong (3.3 D, drawn for D = 0.52 m) stands about 2.0 m tall next to the cars. Scale the actor root by about 0.87 if that matters.
- **Stand-ins.** In `ots` and `low` the stand-in Kong faces three-quarters toward the camera rather than into the door, because the puppets have no back view.
- **Not checked by eye:**
  - beacon strobe frames other than frame 7 (the keys are correct by construction);
  - the 16:9 `top_down` vertical composition;
  - the gantry LED board from the `high` preset at final resolution.


## Independent review (2026-11-25): defects found and fixed

All fixes are inside this folder. Scratch scripts and before/after images: `review/` (`review/builder_out/` keeps the builder's sheets, hue table and draft times; `review/*.orig.py` the builder's code).

| # | Defect (how found) | Fix |
|---|---|---|
| 1 | POV through the windscreen showed no driver: a flipped-normal `*_cabin` box (opaque `interior`) sat between the glass and the seat (ray cast from the camera to the driver's face: glass, then `hero_car_cabin`). The same wall hid him from the side windows. | `vehicles._cabin`: the shell is transparent where back-facing, so the near wall vanishes and the far wall stays as a dark backdrop. Driver now reads in `pov_windscreen`, `dutch`, `ots`. |
| 2 | The deployed airbag (0.45 D ball) filled the driver's face area; a sodium-lamp glint sat on his face. | Airbag is spent: deflated and hanging (scale 0.8 x 0.22 x 0.55). POV camera 0.95 D above the windscreen centre instead of 0.55 (glint off the face). |
| 3 | Stand-ins at 1.15 x scale (cast drawn for D = 0.52 m): Kong 2.0 m tall, the seated driver's hair poked through the roof. | `standins.CAST_SCALE = 0.52 / 0.60` on both actor roots; the seat drop uses it. Presets aim at the scaled heads (`KH` = mark + 2.35 D; driver head scaled about the seat). |
| 4 | `macro_cutter` unreadable: camera behind the tool, 2 of the 3 LED bars off frame, the gauge a green blob (strength 2.2), jaws hidden. | Camera on the battery side, 32 mm in both aspects: all 3 bars in the lower third (about 32 px apart at 720 wide), tool body and door seam behind, DOF k 4.5. LED emission 1.1, bars 0.026 x 0.034. |
| 5 | Render cost 53.9 CPU s per final frame (target 30). Profiled: the 10 sodium cone cards plus the flood-beam lathe cost about 40 % of the frame (every camera ray in a cone crossed 2 transparent surfaces); sample count the rest. | Light cones moved to post (`shafts.py`: depth-tested gaussian disks along each cone axis, density matched to the cards, gain 0.6 fitted against card renders of eye/high/low: k 0.56-0.64). Cards are hidden during the render and kept for `setup_render(shafts="cards")`. `final` = 8 spp at 75 % (old tier = `final12`). Wide post blurs (sigma > 12 px) run on a downsampled copy. |
| 6 | Wet deck read matte: damp roughness 0.32, puddles on ~30 % of the lane, so tail lights smeared and nothing mirrored. | Puddle threshold 0.49 (about 45 %), puddle roughness 0.015, damp 0.20, damp albedo one step lighter so puddles contrast. Tail lights, the medic bag and the bike now reflect as sharp streaks. |
| 7 | Car paint read as dry plastic (flat cream hero car). | `_paint_core`: box-projected rain beads and runs (droplet map, 1.7 per D) on the coat normal; road-spray speckle on the grimy lower body (darker, rougher). |
| 8 | Unreadable foreground blobs in `low`/`eye`: the umbrella (a grey dome right in front of both cameras) and the open cutter case (a black slab). | Umbrella moved to lane 2 at s 30.5, lying open; the case gets a grey foam insert. |
| 9 | LED board latin line read "ACCIDENTAHEAD" (word gap lost at 15 px in a Black face). | Words placed one by one with a 9 px gap (`led_board_r1`). Thai lines on the board, gantry signs, plates and livery were checked at full size: vowels and tone marks stack correctly. |

Checked and found right: build and every preset run headless; beacons cycle every 12 frames (2.5 Hz) with a one-frame half-energy step at each swap (frames 1, 2, 7, 8 of each cycle are the half steps, so frame 7 drafts show beacons at half); 16:9 `top_down` composition (deck across the frame, rescue zone centred).

### Measured after the fixes (load average 2-4, 2 threads)

| What | Before | After |
|---|---|---|
| Final 720x1280 `eye` | 50.0 render + 3.8 post = 53.9 CPU s (12 spp) | 21.4 + 3.2 = **24.6 CPU s** (8 spp, post shafts) |
| Final 720x1280 `high` | not measured | 27.4 + 2.8 = **30.3 CPU s** |
| Same frame, cards vs post shafts, 12 spp | 43.9 CPU s | 27.2 (cards hidden) |
| Drafts 360x640 | 12.4-19.6 CPU s | 9.6-18.7 CPU s |
| Hue, all presets 9:16 | red 20.7, orange 33.9, blue 40.8, violet 1.6, magenta 0.5 | see `out/hue.txt` (red 14.9, orange 38.6, blue 41.1, violet 1.7, magenta 0.6; max magenta 2.0, max violet 6.1 on `high`) |

Build (about 5-9 CPU s) is paid once per process, not per frame.

### Still open after the review

- Colour: blue share 39-41 % against the night band's 50-65; orange high in `ots`, `pov`, `macro` (floodlight on the orange suit, cutter and cream car); `top_down` and `high` 0.6-0.86 dark pixels against 0.35-0.48.
- Stand-in Kong's white head renders lavender (red + blue beacon rims mixed in `cast_dz09`'s toon shader); hue about 250, inside the 240-260 band, but not white. Cast lane, not changed here.
- `pov_windscreen` 16:9 cuts the stand-in Kong in half at the left edge; shots own their actors.
- Panel lines are still bump maps, row-car glass is opaque, smoke and fire are cards, no motion blur, no icons (v4/iconfx).
