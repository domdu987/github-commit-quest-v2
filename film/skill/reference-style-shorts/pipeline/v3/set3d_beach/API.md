# v3/set3d_beach/beach3d.py : a 1938 Long Island beach colony as a real 3D set (bpy 5.3, Cycles CPU)

Files: `beach3d.py` (the set, the controls, the CLI), `beach_tex.py` (cottage walls, shingles, boardwalk planks, the sign, the far-bluff silhouette; SVG rasterised by Chromium through `v3/set3d/raster.js`, cached in `tex/` by content hash), `still_<PRESET>_<cam>.png` (final quality, two placeholder actors), `still_strip_fog_wave.png` (fog and wave at 0, 0.33, 0.66, 1). Working files and review passes: `v3/tmp/beach/` (`p1` to `p6` preview passes, `rev/`, `sprites/`, timing frames, logs).

Reused by import, never copied: `v3/set3d/office3d.py` (`MB` mesh builder, `mat_ink`, `make_camera`, `setup_render`, `no_bounce`, `hex_lin`, collection helpers), `spec/grade_compositor.py` (the grade), `v3/stage` (`actors.Actor`, `sprites`) for the placeholder actors.

World: 1 unit = 1 D, Z up, sand z = 0 where actors stand (flat from the road y = -12 to y = 12.2, so every mark including surf_a / surf_b stands on z = 0; review fix: it used to slope from y = 10 and the surf actors floated 0.05 D), the sea lies toward +y beyond the still-water line `SHORE_Y = 14`, the cottage row and the boardwalk run along x. Camera 22 mm on 36 mm, 720x1280, 30 fps, Standard view.

## 1. Functions

```python
import sys; sys.path.insert(0, ".../v3/set3d_beach"); import beach3d as B

A = B.build(preset="GREY_DRIZZLE", clear=True)    # "GREY_DRIZZLE" | "STORM" | "SUMMER_SUN"  -> anchors dict (section 2)
cam = B.make_camera(A["cams"]["sea_view"], name="cam")   # office3d.make_camera + clip 0.05..5000 + parents the rain field to it
B.attach_rain(cam)                                # only needed for a camera you made yourself (camrig.make_camera): the rain lives in camera space
B.setup_render(scene, "final" | "preview")        # final: 720x1280, 12 samples, 4 threads; preview: 360x640, 6 samples, 2 threads
B.set_fog_bank(amount, frame=None)                # section 3; frame=N inserts a LINEAR key, None sets it statically
B.set_wave(progress, frame=None)
B.set_rain(amount, frame=None)
B.set_sea(t_seconds, frame=None)
B.set_wind(amount, frame=None)
B.wave_state(p)                                   # {'y_toe', 'lip_y', 'crest', 'height'} of the wave at progress p (what the drivers compute)
B.stage_actors(cam, [p_hero, p_boss])             # two placeholder stage.actors cards (stills / timing / review only)
B.ground_z(x, y)                                  # sand height; 0 on the whole beach, dunes inland of y = -12, slope under the sea
```

`build()` works in the current scene: collections `BEACH` (41 objects: sand, sea, 16 cottages, poles, wires, boardwalk, fence, rope, dune grass, umbrella, boat + inside, lifeguard chair + sign + flag pole + flag, BATHING BEACH sign + face, deck chair, towel, bucket and spade, picnic basket, crate, footprints, two far bluffs), `BEACH_FX` (`beach_ctl` control empty, `fog_bank`, `wave` + child `wave_foam`, `rain`), `LIGHTS` (`key_sun`), the world `W_beach` (sky), render settings and the grade. No actors, no camera. `clear=True` removes every object of the scene first; `clear=False` keeps actors and cameras and rebuilds the set (call `attach_rain(cam)` again afterwards). Materials are named `BEACH_*` and rebuilt on every call. Deterministic: fixed seeds for every scatter, Cycles seed 0, no animated seed, no particles, rain driven by the frame number.

Distinct objects in a wide shot: cottages, porches and steps, telegraph poles with wires, boardwalk, rope-and-post fence, dune grass, rowing boat with oar, striped umbrella, lifeguard chair with flag, BATHING BEACH sign, deck chair, towel, bucket, picnic basket, crate, far bluffs = 15, plus ground scatter (pebble / shell specks in the sand shader, wind ripples, footprints, wet band, swash line).

## 2. Anchors (world units)

| key | value | meaning |
|---|---|---|
| `beach_marks` | (0, 7.6, 0), (2.5, 8.4, 0), (-2.2, 8.9, 0), (4.4, 7.1, 0) | open sand between the fence (y 5.75) and the surf; flat z = 0; face the sea (+y) or the camera |
| `marks` | dict | `sand_a..d` (= beach_marks), `surf_a` (-0.8, 11.6, 0), `surf_b` (3.0, 11.9, 0) (wet sand, the wave's lip at progress 1 hangs over y 12.1), `road_a` (3.6, -7.2, 0), `road_b` (0.6, -8.4, 0) (sandy road behind the cottages, for `low_cottages`), `boardwalk` (1.0, 3.85, 0.36) |
| `cottages` | 16 dicts | `name`, `scheme` (cream, red, blue, cedar, yellow), `center`, `x` (x0, x1), `y_back`, `y_front`, `porch_front`, `steps_front`, `size` (w, d), `eave`, `ridge`. Row along x from -38.5 to 66.5, every 7 D; backs at y about -3.2, porches toward the sea |
| `nearest_cottage` | `cottage_06`, x 1.9..5.1, back y -3.2, front 0.0, porch to 1.45, steps to 2.3, eaves 2.6, **ridge 4.04 D** | the yardstick: an actor (hero 2.9 D) reaches past the eaves; the wave at progress 1 crests at 17.5 D, 4.3 times the ridge |
| `poles`, `pole_height` | 9 poles at y 2.75, x = -35 + 14 k; 7.4 D | between the cottages, beside the boardwalk; four wires sag 0.55 D per 14 D span |
| `boardwalk` | x -60..110, y 3.05..4.65, deck z 0.36 | |
| `fence_y` | 5.75 | posts every 2.5 D, 1.35 D high, two sagging ropes; gap x -3.4..-1.2 by the sign |
| `props` | sign (-4.9, 6.15), deck chair (9.6, 8.6) | umbrella (7.2, 9.4), boat (-4.6, 10.9), lifeguard chair (-9.2, 10.4), towel (6.2, 10), bucket (4.9, 10.7), basket (8.4, 10.3), crate (-9.4, 2.5) |
| `shore_y`, `sea_z` | 14.0, -0.12 | still-water line; the surf swashes about +-0.6 D around it (set_sea) |
| `sea_dir`, `horizon_dir`, `shore_dir` | (0, 1, 0), (0, 1, 0), (1, 0, 0) | the sea and its horizon lie toward +y; the shore, the cottage row, boardwalk, poles and fence run along x to one vanishing point |
| `fog_radius` | 300 | the fog band is a ring of this radius about the origin over the sea half (azimuth 4 to 176 deg) |
| `wave` | `wave_state` at 0, 0.33, 0.66, 1 | toe y 437 / 230 / 84 / 17, crest z -0.9 (sunk) / 11.9 / 14.7 / 17.5, height 9 / 11.6 / 14.3 / 17 |
| `key_dir` | per preset | unit travel direction of the sun |
| `cams`, `cam_notes` | dict of `{loc, look_at, lens}` | section 4 |
| `render` | | samples, A, A_pale, K, sun angle, lift of the preset |

## 3. Animated elements

All five live as custom properties on the empty `beach_ctl` (`fog`, `wave`, `rain`, `sea_t`, `wind`). The setters set the property and, with `frame`, insert a LINEAR key. Everything that moves reads them through drivers with simple expressions (no Python at render time, so `bpy.ops.render.render` and any render loop see the keyed state of the current frame).

- `set_fog_bank(a)`: a soft-topped grey-white bank on the horizon ring (radius 300). Height 30 x a^0.75 D (review: was 30 a; a = 1 unchanged, about 5.7 degrees, 80 px in `sea_view`; a = 0.33 now 13.7 D, about 28 px, so a low amount is already a visible bank), opacity min(1, 3a) x 0.95 to 0.97, billowing top (the edge height wanders 0.42 to 0.97 of the band along the ring, soft 0.28 fade), colour from `fog_foot` at the base to `fog` at the top (`#b9b6c6`->`#d2ccd2` sun, `#b6bacb`->`#dcdee6` drizzle, lighter than the drizzle sky so it reads as a bank, `#5d6690`->`#8890b4` storm). 0 = gone.
- `set_wave(p)`: ONE wall of water, a sculpted mesh: profile with a concave face, a curling lip, a long back slope, extruded 1240 D along x with a crest that rises and falls (+-18 percent) and a lip that varies, plus a thin finely scalloped foam lip. Toe at y = 17 + 420 (1 - p)^1.7, height 9 + 8 p (scaled about the base). p < 0.2 sinks it under the sea (p = 0 fully hidden; at p = 0 it also stands 137 D behind the fog ring). Material (`mat_wave`, review rewrite): painted by height (`P['wave']`: near-black navy base, deep blue-teal face, a lighter translucent teal band under the lip, white crest) with streaks running UP the face, a white churn band at the toe and spray specks under the lip; mostly self-coloured (emission art x `wave_emit`) plus the preset key (Lambert, art x `wave_gain` x K), so it reads as water against every sky; foam lip flat two-tone (`mat_wave_foam`, white top, `foam_shade` underside). No ink; distance haze toward the FOG colour (97 percent at 260 D), so far off it reads as the fog bank and only turns into water as it comes in. On screen in `low_cottages` the crest clears the nearest ridge from p = 0.82 on and stands 257 px above it at p = 1 (REVIEW.md 2.4). Key it at several frames if you want an ease (the drivers turn p into position and height, so p itself can be keyed linearly).
- `set_rain(a)`: about 1300 thin streak quads (1 px wide at their depth, 1.8 to 11 D from the lens; review: was 1800 at 1.2 px from 1.3 D, which drew fat white bars across the faces) in a camera-parented field that falls by `fmod(frame * 0.33, 12)`; a streak shows when its random rank < a, so a sets the density (0.3 drizzle, 1 storm); opacity 0.18 to 0.5 per streak (near ones halved) x min(1.3, 0.6 + 0.7 a), colour `rain_col` (default `#cfd6ec`); slant 0.10 + 0.22 x wind radians; hidden below 0.002. Camera rays only, no shadows. Deterministic per frame. At final resolution the storm rain touches 8.8 percent of the pixels of `sea_view` (drizzle 1.8 percent).
- `set_sea(t)`: seconds. Surf line swash 0.45 sin(0.9 t) + 0.15 sin(2.3 t) D (sand wet band and swash line follow), swell streaks drift 0.35 D/s, breaker lines move shoreward 0.55 D/s every 3.4 D. Key `set_sea(0, frame=1); set_sea(T, frame=1 + 30 T)` for real time.
- `set_wind(w)`: 0 calm, 1 storm. Dune grass shape key `wind` (blades lean onshore, toward -y), umbrella tilts 0.22 w rad and shivers (0.035 w sin(0.7 frame)), flag yaws and flaps, rain slants.

Stills states (`STATES`): SUMMER_SUN fog 0, wave 0, rain 0, wind 0.15; GREY_DRIZZLE fog 0.25, wave 0, rain 0.3, wind 0.3; STORM fog 1, wave 1, rain 1, wind 1; sea t = 2.

## 4. Cameras (`A["cams"]`, all 22 mm)

| name | loc | look_at | what it shows |
|---|---|---|---|
| `vista_high` | (-13, 8.2, 6.2) | (30, 1.6, 0.6) | like a/t58.5: high wide down the colony toward +x; boardwalk, fence, poles and wires, cottage row and surf line converge to one vanishing point, sea at left, horizon at 0.42 H, far bluff at the vanishing point; actors at sand_a / sand_b about 60 px heads |
| `low_cottages` | (5.4, -11.3, 0.85) | (3.0, 0.0, 3.6) | low angle from the sandy road behind the colony: an actor at road_a looms (head about 200 px), the nearest cottage and the sky behind it fill the upper frame; at wave 1 the wave towers behind the roofs (crest about 28 degrees up against the ridge's 18) |
| `eye_beach` | (3.6, 13.2, 2.75) | (1.0, 7.6, 2.15) | eye level from the surf side at the group on sand_a / sand_b (heads about 150 and 120 px); porches, cottages, poles and wires behind |
| `sea_view` | (1.0, 4.4, 2.75) | (1.0, 30, -1.5) | their point of view: sand, surf, open sea, horizon at 0.40 H; fog band and wave come in here (at wave 1 the face fills the top half) |
| `wave_low` | (1.0, 6.4, 0.7) | (1.0, 20, 9.5) | 0.7 D above the sand, seaward of the fence, pitched up 33 degrees past actors at surf_a / surf_b: at 0.33 a band on the horizon, at 0.66 the wave rises over the fog, at 1 its face fills the frame with the foaming crest along the top edge (strip row 2) |
| `boardwalk_eye` | (-7, 3.85, 2.85) | (30, 3.4, 1.6) | eye level on the boardwalk: planks, poles, wires to the vanishing point |
| `surf_side` | (-8, 12.6, 2.3) | (30, 8.6, 0.6) | along the surf line toward +x: wet sand, foam lines, lifeguard chair, boat, the colony at right |

Keep cameras out of the cottages (x0..x1, y -3.6..2.4, below z 4.2), poles (y 2.75), the lifeguard chair (x -10..-8.4, y 9.6..11.2, below 5.3) and the umbrella canopy (radius 2 around (7.2, 9.4), z 2.6..3.5). `make_camera` sets clip 0.05..5000 (the sea and sand run 1500 D, the fog ring 300, the wave starts at 437).

## 5. Light model and presets

Same model as the office (`office3d` section 5), per material (`mat_lit`):
`pixel = art x gain x K x visibility / max(cos, 0.12) [toon] + mix(art x A, luma(art) x shade_tint, shade_mix) x F + LIFT`, then a Mix toward the haze colour by `((view distance - d0) / (d1 - d0))^0.75 x haze_max`. F = 1 + dot(normal, form). A is `A_pale` for albedos with saturation under 0.25 (LOOK_SPEC 3.3 pale-surface ambient). The `shade_tint` mix is the colour-lesson fix: on the orange sand the plain `art x A` shade came out hue 290 (magenta); pulling half of it toward one blue-violet tint puts every shade at hue 235 to 250 while it keeps some local colour. The sea is painted (emission, grazing-angle gradient, horizon band, streaks, foam, breakers) and hazed; the sky is the world (camera rays only, invisible to bounce rays): ramp by elevation, clouds on a perspective sky plane (noise of x/z, y/z, faded to the horizon), optional glow toward the sun. Grade: `grade_compositor` (bloom above 1.0, plum CDL black point, no vignette) with the preset's saturation. Ink (inverted hull, camera rays only) only on man-made objects, thickness 0.00384 x distance from the main shots (0.014 to 0.07); sand, sea, sky, clouds, fog, grass, wave, rain: no ink.

| | SUMMER_SUN | GREY_DRIZZLE | STORM |
|---|---|---|---|
| A / A_pale | (0.10, 0.25, 0.98) / (0.21, 0.25, 0.51) (review: darker shade, was (0.12, 0.30, 1.15)) | (0.54, 0.555, 0.68) / (0.52, 0.54, 0.67) (review: less blue, the brown sand x blue ambient went magenta) | (0.06, 0.09, 0.24) / (0.09, 0.115, 0.26) |
| shade_tint, mix | (0.22, 0.20, 0.38), 0.5 | (0.50, 0.52, 0.70), 0.35 | (0.08, 0.10, 0.25), 0.5 |
| K, key travel, elevation, sun angle | (0.92, 0.80, 0.24), (0.55, -0.45, -0.70), 44 deg, 1.0 deg; toon | (0.16, 0.16, 0.17), (0.25, -0.35, -0.90), 64 deg, 14 deg (faint soft shadows); toon | (1.75, 1.08, 0.48), (-0.80, 0.48, -0.22), 13 deg from +x on the land side, 0.8 deg; Lambert (grazing on the ground, full on walls and the wave face facing the light) |
| lift | (0.008, 0.010, 0.026) | (0.010, 0.013, 0.030) | (0.006, 0.010, 0.028) |
| object saturation, grade saturation | 1.0, 1.04 | 0.92, 1.16 | 0.92, 1.08 |
| sky zenith -> horizon | `#4a78cd` `#6898e0` `#8ab1ea` `#a9c6ec` + cumulus `#f4f3fb` / `#b7c2ea` | `#6f7ba0` `#8c96b6` `#aab3cc` `#c0c6da`, overcast `#c2c4d4` / `#8c91ad` | `#0f1534` `#27326a` `#43508c` `#6672aa`, cloud masses `#55628f` / `#1f2a52`, warm break `#e8a070` at 0.35 toward the key (review: was `#f0b070` at 0.6, read as a sunset) |
| sand (3 tones), wet | `#d47844` `#de8e50` `#e8a462`, `#b6765c` (review: spans the red / orange hue boundary like clip A's ground); far tint `#dc7c64` -> `#e6a28a` | `#b8875a` `#c29264` `#cba070`, `#8e6e58` | wet and dark `#9c6a52` `#a6745a` `#b08062`, `#6e5458` (review: the summer sand under the warm key read as a sunset beach) |
| sea near / far / horizon band | `#3559b0` / `#6f9fe6` / `#b9d3ee` | `#4c5c80` / `#7d87a8` / `#c3c5d6` | `#102766` / `#2a4890` / `#7684b8`, streaks 0.75 |
| haze, max, distance | `#a6c2ec`, 0.62, 25..420 D | `#b8bccf`, 0.80, 14..220 D | `#4e5a8e`, 0.55, 18..300 D |
| ink | `#2a1712` | `#2a1d2c` | `#1d1449` |
| wave ramp (z 0 -> 0.97), wave_lite, wave_emit / wave_gain | `#15285e` .. `#f4f8fe`, `#7fb4e0`, 0.62 / 0.30 | `#1f2e55` .. `#e2e8f0`, `#8fa9c8`, 0.70 / 1.2 | `#08122e` `#0f2f5e` `#17507f` `#236f9c` `#4d9cc0` `#b7dcea` `#eef6fb`, `#3f86b0`, 0.78 / 0.16 |

Tone numbers chosen for the two presets without a reference (GREY_DRIZZLE, STORM): no neutral grey (every grey leans blue, hue 225 to 245), no pure black (lift, CDL offset), plum-blue shade. Measured on the final stills with `v3/tools/hue_report.py` (section 7).

## 6. Command lines

```
python3 beach3d.py stills          # still_<PRESET>_<cam>.png for vista_high, low_cottages, eye_beach, sea_view in all three presets
                                   # (two placeholder actors) + still_strip_fog_wave.png (row 1 GREY_DRIZZLE sea_view, row 2 STORM wave_low; fog = wave = 0, 0.33, 0.66, 1)
python3 beach3d.py timing          # final-quality seconds per frame (wall and CPU), sea_view, rain 1, wave 0.7 (STORM 1), fog 0.6 (STORM 1), two actors, every preset
python3 beach3d.py strip           # only the strip
python3 beach3d.py review <outdir> [PRESETS] [cams]   # preview stills (360x640) for the self-review loop
python3 beach_tex.py               # rasterise the textures (build() does it when needed)
```

## 7. Measured on the final stills and frames

Hue make-up (`python3 v3/tools/hue_report.py`, percent of chroma per hue family; sat, val, share of pixels darker than V 0.25), four stills per preset with two placeholder actors:

| set | red | orange | yellow | green | cyan | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clip A exterior frames t09.0 t13.5 t16.0 t48.5 t53.0 t58.5 | 15.3 | 20.0 | 0.1 | 0.0 | 0.0 | 52.8 | 2.5 | 9.2 | 0.42 | 0.70 | 0.07 |
| SUMMER_SUN (after review, 4 stills) | 27.3 | 16.0 | 0.1 | 0.6 | 0.0 | 54.6 | 0.4 | 0.9 | 0.44 | 0.80 | 0.01 |
| GREY_DRIZZLE (after review, 7 cameras) | 30.0 | 2.0 | 0.0 | 1.4 | 0.0 | 61.0 | 0.9 | 4.7 | 0.24 | 0.65 | 0.01 |
| STORM (after review, 7 cameras) | 11.4 | 2.4 | 0.0 | 0.8 | 1.3 | 78.7 | 2.3 | 3.0 | 0.44 | 0.47 | 0.04 |

The builder's rows (SUMMER 11.4 / 26.9 / blue 59.8, GREY 27.7 / 2.2 / magenta 5.9, STORM 28.4 / 3.0) were measured before the independent review; REVIEW.md has both and the per-camera numbers.

Violet stays under 5 and magenta under 10 in every preset (the office came out magenta 25 to 28). Cast shadow on the lit sand in SUMMER_SUN: before the shade-tint fix (99, 84, 104), hue 290 (magenta); with it the shade reads hue 235 to 250 at V about 0.42 of the lit sand (target 0.35 to 0.60). The whole-film band (blue 14 to 30, dark 8 to 15) is for the mix of interiors and exteriors; the clip A exterior frames themselves sit at blue 53 and dark 7, and these stills follow them. Deep darks are the weak point (1 to 5 percent, reference exteriors 0 to 17, median 7): see section 9.

Cost: see REVIEW.md section 2.6 for the review's measurements (machine nearly free: STORM sea_view 4.1 to 4.2 s wall in a frame loop, 5.4 to 6.1 s for a still that re-rasterises the actor sprites). Builder's measurement below. (`python3 beach3d.py timing`: sea_view, rain 1, wave 0.7 / 1, fog 0.6 / 1, two actor cards, 720x1280, 12 samples, 4 threads). OTHER JOBS WERE RUNNING the whole time (load average 8.3 to 9.0 on 4 cores; two other agents' Cycles renders and two Python jobs); the machine was never free during this session.

| preset | frames 2 to 4, wall | CPU per frame | first frame (build of BVH and textures) |
|---|---|---|---|
| GREY_DRIZZLE | 7.95 s | 15.4 to 15.6 s | 11.3 s |
| SUMMER_SUN | 7.90 s | 15.2 to 15.9 s | 11.1 s |
| STORM | 9.56 s | 18.7 to 19.2 s | 13.2 s |
| office3d eye_two_shot at 12 samples, measured right after under the same load | 7.2 to 7.5 s | 13.8 to 14.4 s | |

The office frame costs 3.8 to 4.2 s wall on four free cores (`set3d/API.md` 7, 16 CPU-s at 16 samples, i.e. CPU / wall about 4). By the same ratio a beach frame is 3.9 to 4.0 s (drizzle, sun) and 4.8 s (storm) on a free machine: inside 6 s. Under this session's load the storm frame measured 9.6 s wall, above the 9 s hard limit; that is the contention, not the frame (the office frame took 7.2 to 7.5 s in the same conditions against its 4 s).
What it costs: the sun's shadow rays and the sand shader are the largest parts; the first rain (three full-frame transparent planes) cost 15 CPU-s and was replaced by streak geometry (1.7 CPU-s); hiding the world sky from bounce rays saved about 4 CPU-s. Preview stills (360x640, 6 samples, 2 threads) take 1.5 to 3.5 s.

## 8. Self-review loop (six preview passes, `v3/tmp/beach/p1` to `p6`, sheets beside a/t58.5, a/t16.0, a/t48.5, a/t09.0; final stills checked the same way)

| pass | five largest visible differences against clip A | what changed |
|---|---|---|
| 1 | sky empty and too saturated; sea streaks hard and dark, surf foam band too wide; cast shadow on the sand magenta (hue 290); no red family (red 2 to 10); vista too steep and top-down | shade-tint model, sand/plank hues, grade saturation per preset, thinner streaks, narrower foam, vista lowered |
| 2 | clouds brushed cirrus streaks instead of soft masses; drizzle rain too dense and bright; storm sand bright summer orange under a slate sky (toon key on grazing light); storm sky glow pink; the wave read as a pale flat wall | STORM switched to a real Lambert key (dim grazing ground, lit walls), glow mixed and narrowed, wave gain and taller wave (17 D), softer clouds, fewer drizzle streaks |
| 3 | wave crest read as snowy mountains (faceted lumps, warm-white top); wave face featureless; storm sky violet 9.9 percent; facets from True Normal on smooth meshes; summer clouds too few | smooth normals in the light model, finer foam ribbon, darker banded face, storm palette moved to hue 225 to 240 |
| 4 | sand read red (hue under 20) not orange; drizzle saturation 0.16 (dead grey); bands on the wave face too regular; storm darks thin | sand back to hue 25, drizzle object saturation 0.92 and grade 1.1, irregular bands, darker storm zenith |
| 5 / final | vista sky a big smeared haze; BATHING BEACH sign mirrored from the beach; LIFEGUARD sign facing the sea; frame cost 40 CPU-s (rain planes, world on bounce rays) | clouds smaller and distinct (like a/t58.5), signs turned, geometry rain, world hidden from bounce rays; wave_low moved seaward of the fence so the crest is in frame |

## 9. Known limits (see REVIEW.md section 4 for what the review left open)

- Deep darks: 1 percent of pixels below V 0.25 in SUMMER_SUN and GREY_DRIZZLE (5 in STORM); clip A exteriors reach 7 percent from canyon walls and rail ties. The spec's "nearest 15 percent of the frame at half brightness" (a foreground dune or fence in shade) is not built in; stage a foreground object in shade per shot if a frame needs it.
- The cottages are 4 D to the ridge as the brief asks (LOOK_SPEC 3.3 says 6), so a 2.9 D hero reaches their eaves; doors are 1.55 D.
- The wave is one sculpted mesh moved and scaled by drivers; it does not break, and nothing floods the beach or the cottages. At progress 1 its lip hangs over y 12.1, just past the surf marks.
- The fog ring and the wave are wide but finite (ring azimuth 4 to 176 degrees, wave x -620..620); a camera far down the beach looking back could see their ends.
- Rain streaks are drawn over the actor cards (they are nearer the lens), as real rain would be.
- Placeholder actors use `stage.actors` with `contact=True`; `head_flip` is set from the key's screen side per camera in `stage_actors`.
- Timing was measured only under load (section 7).
