# Sets: every place, what is in it, how it is built

Paths are relative to the skill's `pipeline/` folder (after `scripts/bootstrap.py` they are relative to your project folder) unless they start with `__PROJ__` (the film-1 project, not shipped). Scene units: 1 unit = 1 D = one head diameter, Z up, floor or sand at z = 0. Screen sizes are px at 720x1280. Times are seconds and film frames `g` at 30 fps. Hex is sRGB `#rrggbb`. "Reference" = the two clips A and B (frame names `a/tSS.S`, `b/tSS.S`, one still every 0.5 s).

Sheets (our own film frames, graded v1.1 sharp frames without captions, labelled set | light preset | camera | shot and frame):
- `../../assets/bible/sets_office.jpg`: the office in office_day, office_grey and office_storm, plus the wall map as terrain.
- `../../assets/bible/sets_beach.jpg`: the beach in beach_sunny, grey_drizzle, storm_approach and storm.
- `../../assets/bible/sets_kitchen.jpg`: the kitchen in kitchen_grey and kitchen_storm.

## The rules in brief

1. A set is real geometry built by one Python function `build(preset)` that returns an anchors dict: actor marks, prop positions and named cameras. Shots never place things by eye.
2. Every surface texture is SVG drawn in Python and rasterised by headless Chromium (`raster.js`). Artwork is drawn in the colour the surface shows in neutral light.
3. One hard key (a Sun) plus a flat ambient injected as emission (`office3d.mat_lit`). Shade must land at hue 240-260. Only real emitters exceed scene-linear 1.0, so only they bloom.
4. Man-made props have thickness and a 3 px inverted-hull ink line: hull = 0.00384 x camera distance in D. Never ink sky, sea, sand, fog, grass or rain.
5. Build depth into the set: a dark foreground layer near the lens, the lit subject band in the middle, a far wall or horizon behind. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.
6. Dress where the cameras look: 20-26 distinct objects in an interior wide shot, 12-18 outside. One or two legible lines per text prop; greek the rest. Keep the caption band (y 880-950) free of text.
7. Add to a set only through an extension module that imports it and adds objects after `build()`. Every setter takes `frame=None` (set now) or `frame=N` (keyframe).
8. Texture caches are not shipped. Regenerate them first (section 2.2, or `examples/setup_kit.sh`): about 1.5 minutes in all.
9. Accept a set only on measured stills from its named cameras with stand-in actors (section 9.2): hue band, shade/lit 0.15-0.31, cast-shadow edge 4-21 px, caption band, at least one emitter that blooms.

---

## 1. Reference (measured)

Source: `spec/environment_materials.md` (sections 1-2), `spec/LOOK_SPEC.md` 3.1-3.5.

### 1.1 The places the reference shows

| clip / frame | place | built as | distinct objects (scatter) |
|---|---|---|---|
| a/t27.5 | train car interior, lamp-lit | modelled 3D, no ink on the environment | 11 (16 with ceiling beams): armchair, 2 seat partitions, tripod table, ball, 2 pendant lamps, 2 sconces, 2 window slivers |
| a/t32.0 | station concourse | 3D | 9: carriage with 5 lit windows, 3-globe lamp post, 2 potted palms, 5 roof trusses, red carpet strip |
| a/t34.0 | station facade | 3D | 15: clock, 8 bunting swags, crate stack, 2 sacks, locomotive (about 36 windows) |
| a/t45.0 | trackside, canyon | 3D, low-poly faceted rock 60-150 px facets | 9: toolbox, thermometer, calendar, caliper, flag, rail, 3 sleepers (about 250 stones) |
| a/t16.0 | track, low angle | 3D | 4 types: rails, sleepers, far trestle, fence (stones) |
| a/t53.0 | deck by the sea | 3D | 12: umbrella, deck chair, table, glass, 3 lamp posts, rails, fence, 3 mesas |
| a/t09.0 | sand and mesas | 3D, flat colour | sparse (featureless share 0.82) |
| b/t07.0 | throne room | inked painted backdrop | 26 (about 60 wall motifs) |
| b/t23.0 | banquet hall | inked painted backdrop | 26 |
| b/t27.5 | city gate, day | inked painted backdrop | 30 (about 24 stones and tufts) |
| b/t32.0 | camp | inked painted backdrop | 35 (about 70 flowers) |
| b/t44.0 | city gate, night | inked painted backdrop | 25 (about 70 stones and tufts) |
| b/t49.0-t55.0 | pendulum inside a jar | fully 3D insert with thin contours and bloom | - |

Neither clip contains a sea, rain or an office; film 1's sea and storm colours were extrapolated from the blues that do appear.

### 1.2 How the places are built

| property | clip A | clip B |
|---|---|---|
| geometry | real 3D world, camera travels through it; 16 of 129 frame pairs (12 %) fit a flat 2D zoom/pan | painted 2.5D backdrops; 55 of 129 pairs (43 %) fit a flat zoom/pan; the jar orbit (b/t08.0-t13.0) turns in true perspective |
| outlines on the set | none: edges come from colour blocks, contrast trim strips (13 px yellow-green band on red panels, a/t27.5), painted seams, cast shadows | three weights: object silhouettes 2-6 px (mostly 3-5) in very dark warm brown (`#1f0000`, `#210c07`, `#321d1a`, `#3f0708`) or navy-purple at night (`#1d1449`, `#190217`); detail lines 1-2 px at 0.65-0.70 of the surface luminance (night 0.42-0.55); 3D hero prop contours 1-2 px |
| ink ratio character : set object : detail | | about 8 : 3 : 1.5 px |
| light | hard sun: crisp blue-plum shadows, full transition within 8 px | no hard projected shadows; light painted as a warm pool mid-frame |
| focal length (rough) | about 660 px focal, vertical FOV about 88 deg (18-20 mm on 36 mm), 30 % error | - |

Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.

### 1.3 Depth: foreground, middle, background

- Three planes in A (a/t09.0): textured foreground ground, character plane, far vista. Far landforms shift hue with distance: near sand `#e79a4f`, far sand `#e78c6d`, mesas `#8d78b0`, farthest hills `#7393d0`.
- B uses a value ramp: darkest foreground (b/t32.0 near grass `#5a512e`, V 0.35), lit midground (`#a78039`), pale sky-tinted far city (`#ec918c`, V 0.93). A dark foreground element often frames the top or a side (branch in b/t32.0 and b/t46.0, banner in b/t17.0).
- Both clips keep the bottom of the frame darkest and the middle band brightest. This comes from content, not from a vignette.

Mean luminance (0-255) on an 8 x 5 grid:

| zone | A all | B all | A train interior a/t27.0-t28.5 | B throne room |
|---|---|---|---|---|
| top row | 119 | 108 | 100 | 60-70 |
| middle rows | 120 | 125 | row 3 centre 136 | row 3 centre 169 |
| bottom row | 93 | 79 | 32-47 | 49-65 |
| corners / centre | 104 / 123 | 92 / 128 | | |

Background luminance in a ring around each head: A median 120 (p25 95, p75 164), B median 136 (104-170).

Layout:

| item | value |
|---|---|
| interior zones top to bottom (a/t27.5) | ceiling 0-18 %, upper wall 18-45, dark wainscot 45-66, floor 66-100 |
| floor start (b/t07.0) | 45-50 % of frame height |
| eye line (vanishing point height) | 45 % a/t32.0; 33 % a/t48.5; 67 % a/t16.0 (low angle); 43 % b/t23.0; 42 % b/t44.0; 54 % b/t27.5 |
| exterior horizons | A 50, 34, 43 % (a/t09.0, a/t48.5, a/t53.0); B about 20-23 % (b/t32.0, b/t46.0) |
| room height at the back wall (a/t27.5) | 3.95 D |

### 1.4 Materials, textures, colour blocks

| surface | texture strength (luma std after a 3 px blur) | frame |
|---|---|---|
| A carpet, far sand, sky | 0.3, 1.0, 0.5 (flat colour) | a/t27.5, a/t09.0 |
| A plank wall, ceiling planks, floor planks | 7.0, 3.4, 7.8 (21.3 in raking light) | a/t27.5, a/t32.0, a/t34.0 |
| A canyon wall, ballast | 5.7, 18.2 | a/t45.0 |
| B stone floor, backdrop, carpet, table | 17.3, 22.7, 11.9, 16.6 | b/t07.0, b/t23.0 |
| B stone wall day / night, road, grass | 19.6 / 18.3, 5.3-7.2, 10.1 | b/t27.5, b/t44.0, b/t32.0 |

Measured details: floor plank seam 5 px `#432219` at ratio 0.33-0.40 of the plank, plank width 0.28 D (a/t32.0); wall plank 0.16 D, seam ratio 0.68-0.70 (a/t27.5); deck board 31 px, seam 0.66 (a/t48.5); brick joint 2 px `#8c785f` on `#c3b4a1`, course 23.5-26 px (b/t27.5); B repeat pattern fleur-de-lis 0.32 x 0.38 D, cushion tufts 0.19 D (b/t07.0). No photographic texture and no visible procedural noise in either clip; no specular on walls or floors.

Colour blocks (interiors): warm reds, browns and gold on walls and furniture, one cool dark block (navy) on the floor, cream or white only as small accents. A interior (a/t27.5): orange ceiling `#c53b14`, red seats `#a1001c`-`#da0045`, plank walls `#5e1f36`, wainscot `#491309`, navy carpet `#152a63` to `#17153a`, trim `#76712e`, bulbs `#fffeec`. B interior: drapery `#b64f4b`, backdrop `#5e2221`, gold `#cb9f48`, navy carpet `#26395e` with border `#562025`, stone `#7d858e`, dark wood `#26140a`. Exteriors: A orange-red ground against blue sky (sand `#f3ad6f`, sky `#639de9`); B one dominant light colour per time of day. Full palette: `references/bible/colour-light.md`.

Whole-frame numbers (caption band excluded): saturation A 0.485, B 0.405; Canny 60/140 edge density A 0.060, B 0.067; featureless 40 px blocks A 0.30, B 0.27.

Prop scale against D: armchair 2.2 D wide, 3.7 D high; side table 0.9 x 1.65 D; newspaper 1.08 x 1.4 D; toolbox 1.0 D; beach umbrella 3.85 D; throne 2.2 x 4.4 D; halberd 4.3 D; city gate opening 3.5 x 4.9 D; wall banner 0.75 x 3.8 D; jar 2.8 x 4.4 D.

### 1.5 Signs and text in the picture (all in clip A; B has only pictograms)

- Newspaper (a/t32.0): cream sheet, mixed-case old-style serif masthead, double hairline rule, two-line bold slab headline across about 85 % of the width, engraving in a ruled box. Ink warm brown-grey, never black.
- Calendar (a/t36.0): red card with cream slab capitals, white tear-off page with a large red fat-face month name.
- Signs: cream board, inset dark border, red slab capitals, a small dark sub-line, four corner nails ("ALL ABOARD!", a/t35.0); striped banner (a/t11.0); thin gold capitals on a dark fascia (a/t11.0, a/t29.5).
- Rule: one or two lines large and legible, everything else greeked.

### 1.6 What moves in the background

Measured: the background moves only with the camera. At 30 fps the residual on a held background is 0.9-1.8 of 255 and the drift is under 0.1 px a frame: no line boil (b/t44.0). Light sources glow: bulbs in A, torches and candles in B (torch flame core 8 px, glow to 40 px, b/t38.5). The specs do not list other animated background elements (smoke, flags, crowds); that is not established here.

---

## 2. Our build: what all sets share

### 2.1 Common machinery (`v3/set3d/office3d.py`, imported by every set)

| item | name in code | value |
|---|---|---|
| lit surface | `S.mat_lit(name, color or image, gain, shade_mul, alpha, form)` | `pixel = art x gain x KEY x visibility + (art x SHADE x shade_mul + LIFT) x F`. The diffuse colour is divided by the true cosine to the sun (min 0.12), so every face that sees the sun gets the full key. `shade_mul` may be 3 numbers (tints one surface's shade). |
| ambient form and depth | `F = (1 + dot(normal, form)) x (1 + falloff_y x y / 9)` | office `form` (0.14, -0.04, 0.26), `falloff_y` 0.30: top faces 26 % lighter in shade, undersides 26 % darker; the ambient falls toward the camera-side wall, so the foreground is the darkest layer |
| unlit surface | `S.mat_emit(name, color, image, strength)` | sky cards, bulbs (6), glowing slits; strength above 1 blooms |
| actor card | `S.mat_card(name, png)` then `S.no_bounce(card)` | emission to camera rays only, alpha cut-out, casts the sun's shadow |
| ink | `S.add_hull(ob, thickness)`, material `ink` `#2a1712` | inverted hull, camera rays only; `hull(d) = 0.00384 x d` gives 3 px at distance d |
| mesh builder | `S.MB()`: `.box(lo, hi, mat, mats={'front'..}, tile)`, `.quad`, `.frustum`, `.sphere`, `.obj(name, coll, hull)` | front = the -y face |
| render | `S.setup_render(scene, 'final'|'fast'|'preview')` | final 720x1280, 16 samples, 4 threads; fast 12 samples; preview 360x640, 8 samples, 2 threads. Takes used 12 samples on 2 threads. |
| grade in the render | `S.setup_grade(scene)` | `spec/grade_compositor.py`: bloom above 1.0 (size 0.05, strength 0.5), CDL offset, saturation from the preset |
| bounce rays | `S.no_bounce(ob)` | every set object and every card is hidden from bounce rays; the frame is exactly ambient + one key |

### 2.2 Texture caches: not shipped, regenerate first

Measured in this session on a fresh copy of `pipeline/` (4 cores, machine shared with other jobs):

| cache | command (run from the project folder) | time | size | if missing |
|---|---|---|---|---|
| office textures `v3/set3d/tex/` (23 PNG + manifest) | `python3 v3/set3d/textures.py` (also runs inside `office3d.build()`) | 3.7 s | 4.8 MB | rebuilt by `build()` |
| paper artwork `v3/paper/tex/` (28 items, `registry.json`) | `python3 v3/paper/paper.py build` (`all` also writes `sheet.jpg` and Thai crops) | 51 s | 62 MB | `office_props` puts magenta striped placeholder cards (listed in `PA['placeholders']`); `kitchen3d` and `beach_ext` fail on import |
| hi-res map `v3/set3d_ext/props/tex/map_6000.png` | `python3 v3/set3d_ext/props/make_hi_map.py` | 5.6 s | 11 MB together with the props' own cards (written on first `X.build`) | made on demand |
| office grey/storm skies and rain loops `v3/set3d_ext/light/tex/` | `python3 v3/set3d_ext/light/gen_tex.py` | 15.8 s | 36 MB | `OL.apply` raises `FileNotFoundError ... (run gen_tex.py)` |
| beach textures `v3/set3d_beach/tex/` | `python3 v3/set3d_beach/beach_tex.py` (also inside `beach3d.build()`) | 1.3 s | 0.3 MB | rebuilt by `build()` |
| kitchen textures `v3/set3d_kitchen/tex/` (incl. 92-frame wave, 24-frame steam and drizzle loops) | `python3 v3/set3d_kitchen/kitchen_tex.py` (also inside `kitchen3d.build()`, 16 s on first build) | 15.7 s | 34 MB | rebuilt by `build()` |

Order: fonts, then paper, then everything else. Total about 1.5 minutes and 150 MB.

Font prerequisite: `paper.py` embeds `fonts/th/Kanit_800ExtraBold.ttf`, `fonts/th/Kanit_900Black.ttf` and `/usr/share/fonts/opentype/tlwg/Loma-Bold.otf`. The skill ships both Kanit files in `fonts/th/` (SIL Open Font License, `fonts/th/OFL-Kanit.txt`); bootstrap copies them into the project. Without them `paper.py build` stops at once with `FileNotFoundError` naming the font. Loma comes with the system Thai fonts package (inferred: `fonts-tlwg-loma-otf`); `scripts/check_env.sh <PROJ>` checks all three.

```bash
python3 v3/paper/paper.py build          # 51 s
python3 v3/set3d/textures.py             # 4 s
python3 v3/set3d_ext/props/make_hi_map.py   # 6 s
python3 v3/set3d_ext/light/gen_tex.py    # 16 s
python3 v3/set3d_beach/beach_tex.py      # 1 s
python3 v3/set3d_kitchen/kitchen_tex.py  # 16 s
```

Run with this session: all six (fonts copied from `__PROJ__/fonts/th/`). Every cache is keyed by a sha1 of its SVG, so a rerun only rasterises what changed.

---

## 3. The office (film 1's main set)

`v3/set3d/office3d.py` (+ `textures.py`, drawing code `v2/sets/office.py`), extensions `v3/set3d_ext/props/office_props.py`, `v3/set3d_ext/light/office_light.py`, `v3/set3d_ext/mech/office_mech.py`. The 1938 U.S. Weather Bureau office. Sheet: `sets_office.jpg`.

### 3.1 Units and dimensions

Room x -3.8..3.8 (7.6 D wide), y -9..0 (9 D deep), floor z 0, ceiling z 5.3. The map wall is the plane y = 0; the room runs toward -y; x = 0 is the centre of the wall map; +x is to the right for a viewer facing the map. Window in the right wall x = 3.8. Camera 22 mm on 36 mm, 782 px focal at 720x1280. `build()` creates collection `SET` (46 objects including `track_ctl`), collection `LIGHTS` (`key_sun`), world `W_office` (black), render settings and the grade.

### 3.2 Layout plan in words

Facing the map wall: the framed wall map in the centre (paper 3.0 x 2.16 D, bottom at z 1.42) with a chalk ledge under it; the green U.S. WEATHER BUREAU sign hangs above it on two brass chains; left of the sign the tear-off calendar, below it the banjo barometer; right of the map the wall clock with drop case, the framed certificate, a thermometer, and far right a cork pin board. Two blue filing cabinets stand in the left corner with a box file on top, a waste basket of rolled charts beside them. A radiator under the right half of the map; the teletype on its iron stand in the right corner. The left wall carries a second notice board over a radiator and a coat stand near the map. Crimson-terracotta wallpaper above a walnut wainscot, a frieze, picture rail and crown; orange-brown ceiling boards with three cross beams; four green pendant lamps at different depths; tan plank floor with a navy rug running from the camera-side wall to 0.62 D short of the map. The right wall has a tall window with four glazing bars and a transom: the sun comes through it, low (10.4 deg), and throws the bar shadows across floor and map wall. Near the camera side, left of the rug: a desk with banker's lamp, telephone, papers and ink bottle, and a chair with its back to the camera: the dark foreground layer.

### 3.3 Coordinates (D; boxes as x, y, z ranges)

| element | object | position and size | colour / texture |
|---|---|---|---|
| floor | `floor` | x -3.8..3.8, y -9..0, z 0 | `planks` tile 3.92 x 6.0 D (14 planks of 0.28 D), tan `#a6764e`, seams `#2e1d22` |
| rug | `rug` | x -1.2..1.2, y -9..-0.62, z 0.014; fringed end 0.9 D | `rug` tile 2.4 x 2.0 D (navy `#283a74`, red border), `rug_end` alpha |
| ceiling | `ceiling` | z 5.3 over the whole room | `ceiling` boards 0.37 D, `#8c5030`, dark seams |
| beams | `beams` | 3 at y -1.9, -4.4, -6.9: 0.34 deep, z 4.94..5.31, full width; chamfer strip y +-0.2 | `beam` side art `#4a2616` with iron straps at 1.9 and 5.7 D; ink hull 0.021 |
| walls | `walls`, `wall_relief` | map wall y 0; left x -3.8; back y -9 (no rails); right x 3.8 with the window opening | bands: base z 0..0.16; wainscot 0.16..1.18 (panel art 0.76 x 1.02 D, 0.03 proud); chair rail 1.18..1.27 (0.085 deep); wallpaper 1.27..4.72 (tile 0.32 x 0.76 D, `#aa3e2c`); picture rail 4.72..4.80; frieze 4.80..5.30 (tile 0.4 x 0.5, `#6a2a1e`); crown z 5.2..5.3; stiles every 0.76 D |
| window | `window` | right wall x 3.84..3.95; y -7.72..-1.74, z 0.36..5.08; bars at y -6.71, -5.51, -4.31, -3.12 (0.11 wide); transom z 2.45; sill z 0.29..0.36; reveal slab 0.25 thick | frame `#6f3522`, reveal `#b88a68` |
| sky card | `sky` | plane x 10.8, y -34..20, z -4..11.2; casts no shadow | `sky` art: `#5f79b4` to `#cfd6e2`, clouds, roofline; emission 1.0 |
| map paper | `map_paper` | x -1.5..1.5, z 1.42..3.58, surface y -0.05 | `map` 3000 x 2160 px (1000 px per D); 6000 px version `map_6000.png` for lenses closer than 1 D |
| map frame, gold slip | `map_frame`, `map_slip` | frame x -1.6..1.6, z 1.32..3.68, front y -0.11; slip 0.022 wide | `#3d1c12`, gold `#cb9f48` |
| chalk ledge | `map_ledge` | x -1.69..1.69, y -0.19..0, z 1.215..1.315; brackets at x -1.35, 1.35 | wood `#7b3b26`, lip `#a85a38` |
| ledge props | `ledge_props` | eraser block x -1.32..-1.08; pink eraser x 0.74..0.87 (`eraser_on_ledge` (0.805, -0.10, 1.37)); red pencil x -0.86..-0.50 (`red_pencil_on_ledge` (-0.68, -0.105, 1.35)); blue pencil x 1.18..1.48; chalk stub x -0.3..-0.2 | `#3a3e4c`, `#e58d86`, `#c8301c`, `#2f5a8a` |
| red track | `track_red`, `track_smudge`, `track_arrow`, `track_arrow_ghost`, control `track_ctl` | hand-drawn stroke of 85 points from `map_storm` (0.2349, -0.0515, 1.6183) to `map_ny` (0.0623, -0.0515, 2.6197); width 0.038 D; arc 1.076 D, chord 1.016 D; chord leans 9.78 deg west; arrow barbs 0.13 D at 150 deg; smudge 0.099 D | `#c8301c` gain 0.55; displays about (237, 3, 0) in sun |
| sign | `sign`, `sign_face` | board x -1.50..1.50, y -0.075..-0.015, z 3.90..4.34; face 3.04 x 0.48 D at y -0.078, centre z 4.12; chains at x -1.2, 1.2 up to z 4.74 | green `#1c403d`, gold rule, text `#e9d9b0` |
| calendar | `calendar`, `calendar_face` | block x -2.12..-1.56, z 3.72..4.50, y -0.045..-0.005; face 0.60 x 0.82 centred (-1.84, 4.12); anchor `calendar_rect` x -2.14..-1.54, z 3.71..4.53, y -0.048 | red band, SEPTEMBER, 20 |
| barometer | `barometer` | card 0.72 x 1.44 centred (-1.92, 2.78), y -0.04 | banjo barometer art |
| clock | `clock`, `clock_face` | drum centre (2.12, 4.05), r 0.40, y -0.01..-0.13; drop case x 1.96..2.28, z 3.26..3.78; face card 0.952 D | `#4a2216`, brass, cream face; shows 9:41 |
| certificate | `certificate`, `certificate_face` | frame x 1.98..2.52, z 2.36..3.04; face 0.50 x 0.64 at (2.25, 2.70) | greeked |
| thermometer | `thermometer` | plate x 1.76..1.86, z 1.66..2.14; red column z 1.72..1.96 | `#f3e7c9`, `#c2311e` |
| pin board | `pinboard`, `pinboard_face` | x 2.62..3.56, z 3.10..4.32; face 0.94 x 1.22 at (3.09, 3.71) | cork `#8f6b3c`, five pinned greeked sheets |
| left notice board | `board_left`, `board_left_face` | left wall, y -3.5..-2.4, z 2.35..3.75 | pin-board art |
| left radiator | `radiator_left` | x -3.74..-3.54, y -3.55..-2.35, z 0.08..0.98 | `#5d6478` |
| filing cabinets | `cabinets`, `cabinet_top` | two: x -3.76..-3.01 and -3.00..-2.25, y -0.95..-0.02, z 0..3.0; box file x -3.6..-3.26, z 3.06..3.38; papers x -2.95..-2.45 | blue `#34508c`, drawer art `cab_front` |
| waste basket | `basket` | centre (-2.05, -0.5), r 0.20..0.27, h 0.62; three rolled charts up to z 1.25 | `#8a6a3e`, `#f1e3c0` |
| radiator | `radiator` | x 1.95..3.2, y -0.26..-0.06, z 0.08..0.98 | `#5d6478` |
| teletype | `teletype` | stand x 2.72..3.62, y -1.25..-0.4, top z 1.2..1.28; body z 1.28..1.88; paper x 2.90..3.44, z 1.88..2.36, y -0.70 (anchor `teletype_sheet`, `feed_top` (3.17, -0.685, 2.36)) | body `#20263c`, `teletype` front art |
| coat stand | `coatstand` | alpha card at (-3.3, -1.75), turned to the room | coat and fedora art |
| pendant lamps | `pendants`, `pendant_bulbs` | at (-2.6, -1.3, 4.30), (0.4, -2.6, 4.27), (-1.7, -4.4, 4.05), (0.2, -6.4, 4.32); green shade r 0.47, bulb r 0.2 | shade `#2d7a52`; bulb `#fffeec` emission 6 (the bloom source) |
| desk | `desk` | x -3.45..-1.45, y -5.0..-3.75; top slab x -3.49..-1.41, y -5.04..-3.71, z 1.35..1.45 | `desk_front`, `desk_top` art (lamp pool painted in) |
| banker's lamp | `banker_lamp`, `banker_glow` | (-1.95, -4.05), base z 1.45, shade z 1.95..2.15; glow slit emission 3.6 | brass, green |
| desk props | `desk_props` | telephone x -3.28..-2.67, y -4.25..-3.95; paper stack x -2.55..-2.05; ink bottle (-1.63, -4.22); red pencil; typed sheet x -1.9..-1.58, y -4.86..-4.45; blue pencil | `#1c1e2c`, paper, navy |
| chair | `chair` | centre (-2.45, -5.75), seat z 1.1..1.22, back to z 2.62, back to the camera | `#55291a` |
| key light | `key_sun` (in `LIGHTS`) | travel direction `key_dir` (-0.600, 0.780, -0.180): from the window wall toward the map, 10.4 deg down; angle 0.45 deg | for map-facing cameras the sun is at screen right; shadows fall to screen left, 0.29 D left and 0.09 D lower than a card 0.37 D from the map |

Keep cameras out of: the desk block (x -3.5..-1.4, y -5.05..-3.7, below z 2.2), the chair (x -3.05..-1.85, y -6.3..-5.2, below z 2.65), the beams (y -1.9, -4.4, -6.9, above z 4.94), the lamp shades (r 0.47, z 4.0..4.8).

### 3.4 Signs and text in the office (exact)

| where | text | style |
|---|---|---|
| sign over the map | `U.S. WEATHER BUREAU` | slab bold, cream `#e9d9b0`, fitted to 2.42 D, gold lozenges at both ends |
| map title | `DAILY WEATHER MAP` | printed ink `#836d4e` |
| map labels | `N.Y.`, `BOSTON`, `FLA.`, `H` (high), isobars `1012`, `1016`, `1008`, `996`, latitudes 25-50 deg, longitudes 100-50 deg, compass `N` | `#574430` |
| date slip on the map | `SEPT 20 1938` | pinned at the top right, red pin |
| calendar | `SEPTEMBER` / `20` | cream on red; big red numeral |
| clock | no text, hands at 9:41 | |
| pin boards, certificate, teletype, papers | greeked only | |

### 3.5 Marks where actors stand

| mark | (x, y, z) | from | use |
|---|---|---|---|
| `hero_mark` | (-0.55, -0.42, 0) | set | hero at the wall, left of the track, 0.37 D in front of the map (`wall_gap`) |
| `boss_mark` | (1.30, -0.42, 0) | set | chief at the wall, right of the track |
| `near_mark` | (2.6, -1.95, 0) | set | near actor of a two-shot; his wall shadow lands on the right part of the map, clear of the track |
| `teletype_mark` | (2.25, -1.70, 0) | props | shot 4 chief |
| `hero_tt`, `chief_tt` | (-1.10, -1.50, 0), (2.20, -1.95, 0) | props | shot 14 |
| `senior_a_row`, `chief_row`, `senior_b_row` | (-0.70, -1.20, 0), (0.35, -1.45, 0), (1.40, -1.20, 0) | props | shot 6 |
| `senior_a_front`, `chief_front`, `senior_b_front` | (-1.55, -2.62, 0), (0.40, -2.62, 0), (1.25, -3.05, 0) | props | shot 9a |
| `gloat_near` | (2.40, -1.70, 0) | props | hero in the gloat framing G (shots 10, 18, 25) |
| `senior_a_desk`, `senior_b_desk`, `chief_wall12` | (-1.95, -3.00, 0), (0.20, -2.80, 0), (0.0, -0.55, 0) | props | shot 12 (hero at `hero_mark`) |

Staging limits: bodies and heads at the three set marks with arms down never shadow the track or the N.Y. label. An arm reaching across the map does (every shadow lies 0.29 D left of its caster): keep the hero's hand on or left of the line, check with `S.track_shadow_report()` or `X.track_shadow_report()`. From `low_medium` the hero's head hides the New York end; shoot drawing beats from `eye_two_shot`, `desk_fg`, `low_rake` or `insert_rake`. Hand registration: `S.line_up(target, cam_loc, card_y)`.

### 3.6 Named cameras (all 22 mm)

The office cameras are listed once, in `camera.md` section 2.2 (loc, look_at, height, pitch, horizon, what each frames, which shot used it, all printed from the built anchors). This chapter does not repeat them, so the two cannot drift apart.

- Set cameras, `A['cams']`, 10: `insert_rake`, `low_medium`, `low_rake`, `eye_two_shot`, `high_two_shot`, `high_steep`, `wide_high`, `desk_fg`, `top_down`, `window_side`. Make one with `S.make_camera(A['cams'][name])`.
- Prop-module cameras, `PA['cams']`, 18: `calendar_cam`, `spinner_rake`, `coast_rake`, `low_three`, `chalk_rake`, `chalk_wide`, `high_wide`, `insert_front`, `corridor_cam` (props version), `low_boss`, `G` (the gloat framing), `low_two_wall`, `insert_rake_ny`, `label_insert`, `window_tt`, `G_prime`, `G_prime_dolly`, `sheet_full`. `X.all_cams(A, PA)` gives both sets in one dict.
- Mechanism cameras: section 4.4.

### 3.7 Light presets

| preset (plan name) | how to get it | SHADE / LIFT | KEY, angle | sky, bulbs | shots | measured (hue_report, five cameras with actors) |
|---|---|---|---|---|---|---|
| `INTERIOR_DAY` (office_day) | `S.build('INTERIOR_DAY')` | (0.20, 0.27, 0.54) / (0.0, 0.010, 0.026) | (2.30, 1.65, 0.74), 0.45 deg; shell casts the window patch and bar shadows | day sky 1.0, bulbs 6 | 1-7, 9-14 | red 36.6, orange 27.8, blue 24.1, violet 1.1, magenta 4.6, sat 0.45, val 0.46, dark 0.16 |
| `office_grey` | `S.build('INTERIOR_DAY')` then `OL.apply('office_grey')` | (0.20, 0.23, 0.41) / (0.002, 0.005, 0.014) | (0.66, 0.58, 0.50), 3 deg; no shell shadows (no sun patch) | `sky_grey.png`, bulbs 8, drizzle on the window | 17-22 | 38.7, 33.5, 20.6, 0.6, 2.7, 0.41, 0.45, 0.13 |
| `office_storm` | `OL.apply('office_storm')`, then `OL.tint_cards()` after actors exist | (0.068, 0.082, 0.165) / (0.003, 0.003, 0.007) | (0.12, 0.13, 0.19), 3 deg; lightning `OL.lightning(f)` = a second sun x3.2 for 3 frames | `sky_storm.png` (lit panes), bulbs 12, lash rain | 25 | 41.4, 16.2, 31.7, 0.9, 6.1, 0.40, 0.28, 0.43 (special light, outside the band on purpose) |
| `INTERIOR_LAMP` | `S.build('INTERIOR_LAMP')` | (0.40, 0.33, 0.52) | no sun; dusk sky 0.12, bulbs 9 | | none | smoke-tested only |

Per-surface ambient tints, key gains and the grade of each preset: `v3/set3d_ext/light/API.md` section 2 and `references/bible/colour-light.md`. `OL.apply()` returns the numbers it set; in this session it returned grade offset (0.003, 0.004, 0.008) for office_grey, while that API table says (0.002, 0.0045, 0.010): trust the return value.

### 3.8 Textures and how they are made

`textures.py` draws with the v2 functions (`v2/sets/office.py`, imported read-only; the colour pass re-binds `FRIEZE`, `FLOOR`, `SEAM`, `STEEL`, `STEEL_HI`, `NAVY`, `WOOD`, `PANEL` in memory) and rasterises through `v3/set3d/raster.js`. Items and sizes in D (`T.SIZE`): `wallpaper` 0.32 x 0.76 tile (1000 px/D), `frieze` 0.4 x 0.5, `wainscot` 0.76 x 1.02 panel, `planks` 3.92 x 6.0, `rug` 2.4 x 2.0, `rug_end` 2.4 x 0.9, `ceiling` 3.7 x 3.0, `beam` 7.6 x 0.37, `map` 3.0 x 2.16 (1000 px/D), `sign` 3.04 x 0.48, `clock` 1.0, `calendar` 0.66 x 0.9, `pinboard` 1.0 x 1.3, `barometer` 0.8 x 1.6, `certificate` 0.5 x 0.64, `sky` 16 x 9 (60 px/D), `cab_front`, `desk_front` 2.2 x 1.25, `desk_top` 2.3 x 1.3, `paper` 0.5 x 0.65, `teletype` 0.9 x 0.6, `coatstand`, `radiator`. Cycles does not mip-map: a texture far finer than the screen shimmers; switch the map to 6000 px only when the lens is under about 1 D (`X.set_map_res(True)`).

### 3.9 Functions that build and change the office

Build: `A = S.build(preset='INTERIOR_DAY', clear=True)`. `clear=False` rebuilds only `SET` and `LIGHTS` and keeps actors and cameras (bit-identical frame). Deterministic: two processes give identical pixels.

Set setters:

| function | arguments | what it shows |
|---|---|---|
| `S.set_track(line, erase, frame=None)` | line 0..1, erase 0..1 | grows the red line from the storm symbol to N.Y. (arrow head over line 0.97..1); erase removes it from the N.Y. end (arrow first, gone at erase 0.06), leaving a pink smudge and an arrow ghost |
| `S.track_point(u)` | u 0..1 by arc length | world point on the track; `set_track(u, 0)` ends the line there within 1 px |
| `S.make_camera(setup, name='cam')` | `{loc, look_at, lens, up?, roll?}` | creates or reuses the camera and makes it `scene.camera` |
| `S.track_shadow_report()`, `S.sun_blocker(p)`, `S.line_up(target, cam_loc, plane_y)` | | staging checks |
| `S.placeholder_actor(...)`, `S.stage_placeholders(A, 'hero'|'wall'|'two_shot', cam_loc)` | | stand-in cards for stills and reviews only |

Prop setters (`X = office_props`, after `PA = X.build(A, hi_map=False)`; collection `PROPS`, control `props_ctl`; `X.reset()` = the clean map of shot 4):

| setter | what it shows | shots |
|---|---|---|
| `set_spinner(u, xz, angle, wobble, squash, scale, show, fast, pin_out, which)` | storm spinner disc 0.16 D on a brass pin, hard shadow; `which='ghost1..3'` grey ghosts; `spinner_angle(t)` = 0.5 rev/s, 3 deg wobble | 5-11, 19-22, 25 |
| `set_chalk(grow, crumble, alpha, head)` | white dashed chalk curve 0.020 D, bends at `CHALK_BEND` (0.29, 2.06), out to sea | 7 on |
| `set_ghost(i, grow, alpha)`, `ghost_fan_keys(f_first, every=3)` | six faded grey-blue old tracks, rest alpha 0.35 | 7, 21 |
| `set_tick(alpha, scale, xz, rot_deg)` | tick-stamp impression 0.20 D | 7 |
| `set_ruler(on, side)`, `set_ruler_hand(loc, angle_deg, facing, show)` | maple ruler 1.30 x 0.11 x 0.014 D laid on the map west of the line, or held | 9, 11 |
| `set_label(show, tilt_deg, swing_deg, away, scale, curl, flutter, pin, pin_out, res, raise_d)` | nickname label 'ทางด่วนพายุ' 1.15 x 0.34 D pinned at world (0.05, -0.054, 3.395) | 13, 17-22, 25 |
| `set_smudge(level)` | pink smudge halo, 1 = N.Y. end .. 3 = whole line | 11 |
| `set_crumbs(amount)` | 70 eraser crumbs on the ledge | 11 |
| `set_sheet(loc, facing, roll_deg, show, scale, word1, word2, stamp, pop1, pop2, bow)` | forecast sheet 1.08 x 1.40 D with popping words; `sheet_hold` (1.75, -2.20, 2.05) | 14 |
| `set_teletype(feed, stamp, yaw_deg, show)` | paper rising out of the slot (z 1.88) | 14 |
| `set_stamp(loc, face_dir, roll_deg, scale, show)` | 3D rubber stamp | 14 |
| `set_calendar(day, lift, flutter, tear)` | pad 21 plus a hinged leaf 20 that lifts, flutters and tears off | 4, 17, 18, 25 |
| `set_map_res(hi)` | swap the map to 6000 px | 9c, 19, 20, 22 |

Light setters (`OL = office_light`): `apply(name)`, `tint_cards()`, `set_rain(drizzle, lash, frame, phase)` (96-frame loop on a card at x 3.895 inside the glazing), `flash(amount, frame)`, `lightning(f, pattern=(1.0, 0.35, 0.8))`, `set_flash_energy(e)`, `state()`.

What a shot must call first, in this order: `S.build` -> `X.build` (if props) -> `M.build` (if the mechanism) -> `OL.apply` (after every build, because it re-tints every lit material that exists) -> actors -> `OL.tint_cards()` (storm) -> per-frame setters -> render. Takes render 720x1280 at 12 samples on 2 threads.

```python
# run from the project folder; tested in this session (preview render of eye_two_shot, 2.2 s)
import sys; sys.path[:0] = ["v3/set3d", "v3/set3d_ext/props", "v3/set3d_ext/mech", "v3/set3d_ext/light"]
import bpy, office3d as S, office_props as X, office_mech as M, office_light as OL
A = S.build("INTERIOR_DAY")          # 1.0 s with the texture cache warm; SET has 46 objects
PA = X.build(A)                      # 3.7 s; PROPS 62 objects; PA['placeholders'] must be []
OL.apply("office_grey"); OL.set_rain(drizzle=1.0, lash=0.0)
S.set_track(1, 0); X.set_label(1.0)
S.setup_render(bpy.context.scene, "preview")      # "final" for takes, then scene.cycles.samples = 12
S.make_camera(PA["cams"]["G"])
bpy.context.scene.render.filepath = "/tmp/office_G.png"; bpy.ops.render.render(write_still=True)
```

Cost of a final frame: bare set 17.9 CPU s at 12 samples (about 4.5 s wall on 4 idle threads); with all props 19.7-20.6 CPU s; office_grey 19.4, office_storm 18.7 CPU s; a lightning frame costs the same as an unlit one.

### 3.10 Shots of film 1 in the office

Shots 1-7, 9-14 (office_day; shots 1-3 are the opening `v3/shots/film.py`, g0-128; takes `v3/film/s04`..`s07`, `s09`..`s14`), 17-18 (office_grey, `s17`, `s18`), 19-22 (map as terrain, office_grey, `s19`..`s22`), 25 (office_storm, `s25`): 1515 of the film's 1965 frames. Runners: `v3/film/s10/otake.py`, `v3/film/s17/otake.py` (with `OL.apply` and `tint_cards`).

### 3.11 What the set reviews found (`v3/set3d/REVIEW.md`, `v3/out/COLOUR.md`)

| found | repair | measured after |
|---|---|---|
| far shadow edges too soft (bars 5-8 D from the surfaces: up to 32 px) | sun angle 0.7 -> 0.45 deg | edge median 5-10 px, max 22 px |
| shadows on wall surfaces shallow (0.32-0.36 of lit) | map shade 0.56, gains rebalanced | 0.25-0.28 (map, wallpaper), wainscot 0.21, floor 0.155 |
| sunlit wallpaper clipped to pure red (green 0) | wallpaper base and gain changed | sun patch `#e43625` |
| ceiling had no readable converging lines (no edge in the top quarter) | boards with dark seams and a highlight line, inked textured beams | edge density of the two-shots 0.070 -> 0.086 |
| boxes and corners had no tonal form in shade; foreground as bright as the wall | `form` term and `falloff_y` | foreground is the darkest layer |
| high and low cameras not steep enough | `high_two_shot` -22 deg, `wide_high` -25 deg, new `low_rake`, `high_steep` | horizon classes as the office table in `camera.md` 2.2 |
| colour pass: 25-28 % magenta (violet ambient, rose wallpaper, plum ceiling) | blue ambient, per-surface shade tints, crimson-terracotta wall `#aa3e2c`, orange-brown ceiling `#8c5030`, tan floor `#a6764e`, blue cabinets `#34508c`, navy-plum black point | magenta 3.5-4.2, all in band |

Still different from the reference: actor shadows fall on the wall, not the floor (the 10 deg sun keeps the whole map lit; the reference sun is 35-50 deg); shadows on map and walls 0.25-0.28 of lit against 0.08-0.25; wall ring around the near head 70 against 95-170; no light shafts in the window; `top_down` shows cards flat.

---

## 4. The wall map as terrain (the mechanism, shots 19-22)

`v3/set3d_ext/mech/office_mech.py` (`M`). It builds on the office and its props; it edits neither. Worked example: `v3/film/s19/shot.py` (245 frames).

### 4.1 Geometry and units

`M.world(a, s, h, u=None)` = the point `a` D east of the hand-drawn line (negative = west), `s` D along it by arc length from the storm (or `u` = track fraction), `h` D proud of the paper toward the room. `world(0, 0, 0, u)` lies on the red line within 0.1 mm. Paper plane y = -0.05. Line arc `M.TLEN` 1.076 D, chord `M.CHORD` 1.016 D; the line bows up to 0.154 D west of the chord near u 0.5.

| element | position and size | look |
|---|---|---|
| two pressure walls 'E' (Atlantic) and 'W' (land) | flank the line from u 0.05 to 0.92 (`U_WALL`); corridor faces 0.11 D each side of the smoothed line (`LANE_HALF`, lane 0.22 D); four terraces of 0.125 D, total height 0.50 D; nominal widths east 0.72 / 0.56 / 0.42 / 0.30, west 0.50 / 0.40 / 0.31 / 0.23 (+ the bow); west outer edge pushed out 0.151 D | pale blue-grey paper `#c4c6d4` east, `#cac6d2` west, ink hull 3.5 mm, navy Latin H on the top terrace and on each corridor face |
| lane | u 0.04-0.95, 0.6 mm proud, 180 segments | pale body, white dashes on both edges |
| speed sign | default u 0.62, a +0.085, disc 0.62 D proud, faces south | '100' and Thai 'กม./ชม.', 0.21 D at scale 0.8 |
| compass | `COMPASS_XZ` (0.50, 2.86) | red north point, Latin N |
| no-turn pictograms | on brackets out of the corridor faces | no words |
| wind arrows | 14 pale arrowhead cards, 0.05-0.30 D up | |
| wake | red-hot streak on the line | glows |

### 4.2 Setters

| setter | what it shows |
|---|---|
| `build(A, PA, wall_height=0.50)` | everything, hidden; returns `MA` |
| `reset()` | walls sunk, all extras hidden |
| `set_wall(side, rise, slide, lock, fade, pulse, frame)` | rise 0..4 (terrace k grows in k..k+1; key 0 -> 4 over 18 frames for four thuds); slide 0..1 squeeze onto the lane edge; lock 0..1 stepped -> vertical face (stamps the H); fade; pulse = height x (1 + 0.15 pulse) |
| `set_lane(grow, red, fuse, alpha, glow, frame)` | lane unrolls; dashes turn red and fuse into the pencil line (shot 22) |
| `set_compass(show, scale=0.8, rot_deg, ping, xz)` | compass pop and ping |
| `set_picto(side, show, scale, s, h, yaw_deg, wobble_deg, tilt_deg)` | 'E' no right turn, 'W' no left turn |
| `set_wind(progress, amount, span)` | arrows streaming north; amount 0.33 / 0.66 / 1 = three waves |
| `set_speed_sign(show, spin_deg, scale, u, a, height)` | the 100 km/h sign; spin and settle |
| `set_spinner_fx(ring, ring_pulse, drop, drop_slide)` | isobar ring and sweat drop on the spinner |
| `set_wake(head_u, length_u, alpha)` | red wake (20, 21, 25) |
| `set_ghost_spinner(i, s, angle, show, alpha, scale)`, `set_shell(show, which)` | ghost storms crawling on old tracks, snail shell |

Call order: `S.build` -> `X.build(A, hi_map=True)` -> `M.build(A, PA, wall_height=0.50)` -> `OL.apply('office_grey')` (after `M.build`). Every lens under about 1 D needs `hi_map=True`.

### 4.3 Light

office_grey only. The walls take most of a close frame, so blue runs high: s19 v1 measured red 28.1, blue 45.5, sat 0.37 (out of band). The v1.1 grade warmed the sequence to blue 27/31/19 for s19/s20/s21. Cost: about 23 s wall per frame at 12 samples on 2 threads under load 6-8.

### 4.4 Cameras (`M.cams()`, `M.cam(name)`)

Builders: `M.corridor(u_lens, h, look_u, look_h, a='auto', ...)`, `M.plan(u_center, dist, a, roll)`, `M.rake(target, dist, elev_deg, az_deg, up)`, `M.lerp_setup(a, b, t)`. Check a camera with `M.sight_margin(...)` (< 0 = a wall hides the target).

`M.cams()` returns 13 named cameras: `rake_spinner`, `rake_north`, `corridor_cam` (mechanism version, THE CORRIDOR VIEW), `corridor_far`, `plan_view_start`, `plan_view`, `spinner_high`, `launch_end`, `sign_cam`, `atlantic_rake`, `label_end`, `whole_map`, `ny_arrow`. Their definitions, loc / look_at, what they frame and the shots that used them are listed once, in `camera.md` section 2.2 ("Map mechanism"). Two cameras share the name `corridor_cam`: the props version (`PA['cams']`, shot 9c) and the mechanism version (`M.cams()`, shots 19 and 20).

Keep cameras south of u 0.05 or above h 0.55 unless inside the lane, and inside the lane keep |a| < 0.08 from the line.

### 4.5 What the reviews found

The sequence read as a cold explainer diagram (v1: blue 46/62/67 %, sat 0.36/0.35/0.28 for s19/s20/s21); fixed only by a per-take grade. The ghost storms of shot 21 stayed too small to read (under 120 px). Next time: light the terrain with the room's warm key (cream-tan wall faces, warm highlights) from the start, and make anything the story needs at least about 120 px.

---

## 5. The beach

`v3/set3d_beach/beach3d.py` (`B`, + `beach_tex.py`), extension `v3/set3d_ext/beach/beach_ext.py` (`BX`), runner `v3/set3d_ext/beach/bshot.py`, QA `bqa.py`. A 1938 Long Island beach colony. Sheet: `sets_beach.jpg`.

### 5.1 Units and dimensions

Sand z = 0, flat from the road y = -12 to y = 12.2, then a 1:15 slope to the still-water line `SHORE_Y` 14 (sea z -0.12). The sea and horizon lie toward +y; the cottage row, boardwalk, poles and fence run along x to one vanishing point. Sand and sea run 1500 D; cameras clip 0.05..5000. Collections: `BEACH` (41 objects), `BEACH_FX` (`beach_ctl`, `fog_bank`, `wave` + `wave_foam`, `rain`), `BEACH_EXT` (147 objects with the dressing), `LIGHTS`.

### 5.2 Layout in words

From the road inland: a sandy road (y about -7 to -8), then a row of 16 shingled cottages with porches toward the sea, every 7 D along x; telegraph poles between them with four sagging wires; a boardwalk on the sea side of the porches; a rope-and-post fence with a gap; open sand with umbrella, deck chair, towel, bucket and spade, picnic basket, a rowing boat and a lifeguard chair; wet sand and surf; the sea with breaker lines; far bluffs; a fog ring and the wave beyond the horizon. The beach framing looks along the shore toward +x: sea and surf at left, sign mid-right, boardwalk, fence and cottages with poles at right.

### 5.3 Coordinates

| element | position and size | colour |
|---|---|---|
| cottages `cottage_00`..`cottage_15` | x centres exactly -38.5 + 7 k (k 0..15); width 3.2 x a per-cottage scale, depth 3.2; floor 0.6, eaves 2.6, ridge about 3.95 (3.83-4.32 measured); backs at y about -3.2, porch to about 1.45, steps to about 2.3 | scheme chosen per cottage by a fixed seed (00 cream, 01 red, 02 blue, 03 cedar, 04 yellow, 05 blue, 06 cream, 07 cedar, 08 red, 09 yellow, 10 cream, 11 blue, 12 red, 13 cedar, 14 yellow, 15 cream): cream body `#ebddc8`, red `#b84735`, blue `#7f8fbf`, cedar `#a7745a`, yellow `#e3c27a`; roofs `#5b211d` or `#4d3e3f` |
| measured cottages (x0..x1, scheme) | 05 blue -5.21..-1.79; 06 cream 1.90..5.10 (the yardstick: ridge 4.04, back y -3.2, front 0.0); 07 cedar 8.83..12.17 (porch at x 9.15, y 1.05); 08 red 15.89..19.11 | |
| poles | 9 at y 2.75, x = -35 + 14 k, height 7.4 D; wires sag 0.55 D per 14 D span | |
| boardwalk | x -60..110, y 3.05..4.65, deck z 0.36 | planks art |
| fence | y 5.75, posts every 2.5 D, 1.35 D high, two ropes; gap x -3.4..-1.2 | post `#8a5a35`, rope `#d9c9a8` |
| BATHING BEACH sign (set) | (-4.9, 6.15), board 2.2 x 0.95 D; hidden by `beach_ext` | cream `#f6efe2`, red `#b61d32` |
| umbrella | (7.2, 9.4), canopy r 2, z 2.6..3.5 | red and cream stripes |
| deck chair | (9.6, 8.6) | |
| boat | (-4.6, 10.9), yaw 62 deg | |
| lifeguard chair + sign + flag | (-9.2, 10.4), x -10..-8.4, y 9.6..11.2, up to z 5.3 | sign `LIFEGUARD` |
| towel, bucket, basket, crate | (6.2, 10), (4.9, 10.7), (8.4, 10.3), (-9.4, 2.5) | |
| fog ring | radius 300 about the origin, azimuth 4..176 deg; height 30 x a^0.75 D | |
| wave | one sculpted mesh x -620..620; toe y = 17 + 420 (1 - p)^1.7; height 9 + 8 p; crest 17.5 D at p = 1 | navy base to white crest |
| LONG ISLAND sign (ext) | (2.0, 4.9), face yawed 65 deg toward -x; two posts 2.95 D, board 2.3 x 0.98 D on chains from z 2.85 | registry `beach_sign` |
| landing + step (ext) | fence gap x -3.2..-1.4: deck y 4.6..5.95 at z 0.36, step y 5.95..6.25 at z 0.18 | |
| vane and brick chimney (ext) | on `cottage_07`; second chimney on `cottage_06` | |
| towel line (ext) | porch front of `cottage_06`; towel 0.7 x 0.78 D | red and cream |
| lit windows, shutters (ext) | every cottage front: panes 0.40 x 0.60 D; shutters `#3d5a6e` | dark `#2b3150` to `#ffd995` at 1.9 |
| cobweb + spider (ext) | between (7.2, 9.4) and (9.6, 8.6), z 0.4-1.2; cobweb 0.9 D | |

Keep cameras out of the cottages (y -3.6..2.4, below z 4.2), the poles (y 2.75), the lifeguard chair (x -10..-8.4, y 9.6..11.2, below z 5.3) and the umbrella canopy (radius 2 round (7.2, 9.4), z 2.6..3.5).

### 5.4 Signs (exact text)

| sign | text |
|---|---|
| set sign (`beach_tex.sign`, hidden in film 1) | `BATHING BEACH` / `NO LIFEGUARD AFTER 5 P.M.` / `SUFFOLK COUNTY  1938` |
| lifeguard chair | `LIFEGUARD` (cream on red) |
| ext sign (registry `beach_sign`) | `LONG ISLAND` / `BATHING BEACH · SUFFOLK COUNTY 1938` |

### 5.5 Marks

`sand_a` (0, 7.6, 0), `sand_b` (2.5, 8.4, 0), `sand_c` (-2.2, 8.9, 0), `sand_d` (4.4, 7.1, 0) open sand; `surf_a` (-0.8, 11.6, 0), `surf_b` (3.0, 11.9, 0) wet sand; `road_a` (3.6, -7.2, 0), `road_b` (0.6, -8.4, 0) behind the cottages; `boardwalk` (1.0, 3.85, 0.36). In the beach framing the man's mark is about 5 D ahead of the lens; the woman's porch (cottage_07) is at x 9.15, y 1.05.

### 5.6 Cameras (22 mm)

Set cameras `A['cams']` from `B.build` (7): `vista_high`, `low_cottages`, `eye_beach`, `sea_view`, `wave_low`, `boardwalk_eye`, `surf_side`; extension cameras (3, also in `BX.CAMS` and `BX.cam_pose(name)`): `beach_shore_eye` (THE BEACH FRAMING), `beach_high`, `beach_low_wave`. `BX.build` puts all ten in `A['cams']`. Their loc, look_at, pitch, horizon, head widths and shots are listed once, in `camera.md` section 2.2 ("Beach").

### 5.7 Light presets

| plan name | preset | ambient A / key K | sky | measured (hue_report) | shots |
|---|---|---|---|---|---|
| `beach_sunny` | `SUMMER_SUN` | A (0.10, 0.25, 0.98), K (0.92, 0.80, 0.24), sun 44 deg up, 1.0 deg, toon | `#4a78cd` zenith to `#a9c6ec` horizon, cumulus | red 27.3, orange 16.0, blue 54.6, sat 0.44, val 0.80, dark 0.01 | 8 |
| `grey_drizzle` | `GREY_DRIZZLE` | A (0.54, 0.555, 0.68), K (0.16, 0.16, 0.17), 64 deg, 14 deg | `#6f7ba0` to `#c0c6da` overcast | 30.0, 2.0, 61.0, sat 0.24, val 0.65, dark 0.01 | 16 |
| `storm_approach` | `STORM_APPROACH` (ext): GREY_DRIZZLE with K, A x 0.75, shade tint (0.36, 0.36, 0.56) | | bruise violet `#3a3466` -> `#6a5f8e` -> `#8e7f98`, sick yellow band `#c2b27c`; glassy sea `#2e3658` / `#4c5076` | s23 v1: violet 55.3, sat 0.30, dark 0.01 | 23 |
| `storm` | `STORM` | A (0.06, 0.09, 0.24), K (1.75, 1.08, 0.48) 13 deg, 0.8 deg, Lambert | `#0f1534` to `#6672aa`, warm break `#e8a070` at 0.35 | 11.4, 2.4, 78.7, sat 0.44, val 0.47, dark 0.04 | 24 |

Shade on the sand is pulled toward a blue-violet tint (`shade_tint`, mix 0.35-0.5) so it lands at hue 235-250, not magenta. Exteriors sit outside the interior band (clip A exteriors measure blue 52.8, dark 0.07).

### 5.8 Functions

Build: `A = BX.build(light, clear=True, dressing=True, boater=False)` (light = plan name) or `A = B.build(preset)` for the bare set. Camera: `B.make_camera(setup)` (also parents the rain to it); `B.attach_rain(cam)` for a camera made elsewhere.

| setter | what it shows |
|---|---|
| `B.set_fog_bank(a)` | horizon bank, height 30 a^0.75 D, opacity min(1, 3a) x 0.95-0.97 |
| `B.set_wave(p)` | the wall of water (p < 0.2 sunk); key with an ease; `B.wave_state(p)` |
| `B.set_rain(a)` | about 1300 streaks in camera space; 0.3 drizzle, 1 storm; judge only at full size |
| `B.set_sea(t)` | surf swash, swell and breaker motion; key `set_sea(0, frame=1); set_sea(T, frame=1+30T)` |
| `B.set_wind(w)` | grass, umbrella, flag, rain slant |
| `BX.set_sign_swing(amp_rad)`, `set_vane(deg)`, `set_towel(0/1)`, `set_windows(0..1)`, `set_shutters(0..1)`, `set_spider(0..1)`, `set_fog_near(k)` (ring radius 300 x k), `set_boater(frame, loc, spin_deg, scale, visible, cam)` | dressing controls |

```python
# tested in this session: build 1.5 s, preview render 2.2 s
import sys; sys.path.insert(0, "v3/set3d_ext/beach")
import bpy, beach_ext as BX
A = BX.build("grey_drizzle")
cam = BX.B.make_camera(BX.cam_pose("beach_shore_eye"))
BX.B.set_rain(0.35); BX.B.set_fog_bank(0.25); BX.B.set_wind(0.3); BX.B.set_sea(2.0)
BX.B.setup_render(bpy.context.scene, "preview")   # final: 720x1280, 12 samples
bpy.context.scene.render.filepath = "/tmp/beach.png"; bpy.ops.render.render(write_still=True)
```

A take uses the runner: define `TAKE`, `SHOTS`, `LIGHT`, `G0`, `G1`, `cam(g)`, `state(g)`, `ACTORS`, `actors(g)`, `CUES` and end with `BS.run(...)`; commands `probe`, `still`, `draft`, `render`, `post`, `qa` (`v3/set3d_ext/beach/API.md` section 4; bundled tested example `examples/beach/shot.py`; film-1 takes `__PROJ__/v3/film/s16/shot.py`, `__PROJ__/v3/film/s23/shot.py`, not bundled). Cost: 4.1-4.2 s wall per storm frame in a loop on a nearly free machine.

### 5.9 Shots of film 1 on the beach

8 (beach_sunny, beach_high, g401-504), 16 (grey_drizzle, beach_shore_eye, g1013-1085), 23 (storm_approach, beach_shore_eye, g1664-1719), 24 (storm, beach_low_wave, g1720-1787). Frame ranges are inclusive (`__PROJ__/plan/shot_plan.json` t0, t1 x 30).

### 5.10 What the reviews found (`v3/set3d_beach/REVIEW.md`, `__PROJ__/deliver/QA_film*.md`)

Repaired in the set review: magenta sand shade (hue 290) -> shade tint; the wave read as clouds and was rewritten as a painted, self-coloured mesh; drizzle fog the colour of the sky -> lighter billowing bank; rain bars over faces -> 1 px streaks; storm sand read as a sunset beach -> wet dark sand; the surf marks floated 4-6 px -> flat sand to y 12.2. Left open: deep darks 1 % (reference 7 %, target 8-15) because an open beach has no dark mass; SUMMER_SUN value 0.80 against 0.69-0.70; GREY_DRIZZLE saturation 0.24; the wave does not break. In the film: shot 16 was washed out and the tilt held on empty sky (sat 0.24, dark 1 %); the fog bank of shot 23 was a 40-60 px strip, unreadable on a phone; the violet sky of 23 is flat; no sun bloom or haze in shot 8.

---

## 6. The kitchen

`v3/set3d_kitchen/kitchen3d.py` (`KS`, + `kitchen_tex.py`, `kitchen_geom.py` bpy-free numbers, `kshot.py` take machinery, `kqa.py`). A table corner by a four-pane window in a cottage, 21 September 1938. Built from the office's light model and helpers; only what the planned camera sees exists. Sheet: `sets_kitchen.jpg`.

### 6.1 Units and layout

Window wall = plane y = 0, room toward -y. Wall x -2.6..2.8, up to z 4.4; wainscot (office `wainscot.png`) z 0..1.62 with a chair rail at 1.62; papered wall (`kwall`) above. The table stands in front of the window; on it a folded newspaper leans back on a bread box with its weather box toward the lens; a cup and saucer stand on the paper's bottom-right corner; a toast plate at left. Blue gingham curtains on a brass rod, the calendar pad 21 left of the window. An unseen cupboard edge behind the lens (`fg_blocker`, camera-invisible) shades the near table, so the light pools on the paper and cup.

| element | object | position and size | colour / texture |
|---|---|---|---|
| window | `window`, `exterior` | glass x -0.40..0.90, z 1.98..3.06; mullion x 0.25, transom z 2.52 (four panes 0.65 x 0.54); reveal 0.2 D; sill z 1.90-1.98; exterior card at y 0.9, x -1.9..2.3, z 0.9..4.1 (300 px/D) | frame `#8a4a2a`; drizzle loop or the 92-frame wave sequence |
| crack | `crack` | card on the pane at x 0.31.., hidden until `crack=k` | 6 frames |
| curtains, rod | `curtain_l`, `curtain_r`, `rod` | rod x -0.66..1.32, y -0.12, z 3.30 | blue gingham |
| calendar | `calendar_block`, `calendar_face` | x -1.02..-0.74, z 2.10..2.48 (registry `calendar_pad_21` at 0.42 scale) | |
| floor | `floor` | x -3..3, y -4.5..0 | office `planks.png` |
| table | `table_top`, `table_legs` | top z 1.30, x -1.6..0.98, y -1.95..-0.02; oilcloth drop 0.24 D | red-check `oilcloth` |
| bread box | `bread_box` | x -0.55..0.45, y -0.66..-0.12, z 1.30..2.00 + lid | `#8a4a2a`, top `#a85e34`, brass handle |
| newspaper | `newspaper`, `newspaper_back` | registry `newspaper` at 0.9 scale (1.35 x 1.755 D), folded; lower half leans back 62 deg; foot y -1.15, 0.075 D lip flat | weather box centre `wb_point(1.0, 1.42)` = (0.225, -0.944, 1.638); ฝนตก (0.225, -0.965, 1.598); ลมกระโชก (0.225, -1.062, 1.415); header (0.225, -0.792, 1.924) |
| cup and saucer | `saucer_rig` > `saucer`, `spoon`, `cup_rig` > `cup`, `coffee`, `steam` | rest `CUP_REST` (0.38, -1.40); cup turned -50 deg | cream `#f1e4cb`, navy rim `#2e4686` |
| toast plate | `plate`, `toast` | (-0.50, -1.50) in code | |
| chair | `chair` | (1.30, -1.10), shoved to (1.60, -1.40) and turned 24 deg by `chair=1` | |
| drop | `drop` | falling drop, emission `#cfe0ff` 1.4 | |

No actor marks: the takes add an arm card (`kshot.py`).

### 6.2 Cameras

`A['cams']` from `KS.build` (3): `table` (THE TABLE FRAMING), `steep`, `window_tight`; the same poses bpy-free in `kitchen_geom.CAM_TABLE`, `CAM_STEEP`, `CAM_WINDOW`. Their loc, look_at, pitch, what they frame and shots are listed once, in `camera.md` section 2.2 ("Kitchen").

### 6.3 Light presets (values from the code)

| preset | SHADE | KEY, direction, angle | window | grade | shots |
|---|---|---|---|---|---|
| `kitchen_grey` | (0.25, 0.27, 0.52) | (0.56, 0.53, 0.54), `key_dir` (0.42, 0.62, -0.66), 2.0 deg | drizzle loop at 1.0 | saturation 1.22 | 15 |
| `kitchen_storm` | (0.050, 0.072, 0.20), falloff 1.2 | (0.28, 0.20, 0.125), same direction, 4.0 deg; `flash_sun` from (-0.15, -0.75, -0.62), x3.2 in lightning | wave sequence at 0.85 (x1.6 in lightning) | saturation 1.15 | 26 |

### 6.4 Functions

`A = KS.build(light)`; `KS.set_state(cup, saucer, ripple=(phase, amp), steam=frame_index_int, window=('drizzle'|'wave', k_int), flutter=(t, amp), bleed=0..11, lightning=0..1, crack=0..5, chair=0..1, drop=(x, y, z))`. Every call resets what it is not given. `steam` and `window` k must be integers (frame indices); a float raises `TypeError`.

```python
# tested in this session: build 16 s on the first run (it rasterises the kitchen textures), 1.0 s after; preview 1.8 s
import sys; sys.path.insert(0, "v3/set3d_kitchen")
import bpy, kitchen3d as KS
A = KS.build("kitchen_grey")
KS.set_state(steam=5, window=("drizzle", 3))
KS.S.make_camera(A["cams"]["table"]); KS.S.setup_render(bpy.context.scene, "preview")
bpy.context.scene.render.filepath = "/tmp/kitchen.png"; bpy.ops.render.render(write_still=True)
```

Cost: 5.8 s per frame at 8 samples on 2 threads on an idle machine (12 samples: 8.5 s, no visible difference).

### 6.5 Shots and reviews

Shot 15 (kitchen_grey, steep -> table, g956-1012) and shot 26 (kitchen_storm, window_tight -> table, g1873-1964). The film review found shot 15 all warm (red 52.1, orange 40.2, blue 6.5) with no cool shade, and the "dark wall of water" in the panes of 26 reading as white puffy clouds and rain. Next time: let the window light the near paper and cup with a cool rim, and put real dark blue mass in the window card.

---

## 7. Paper artwork registry (`v3/paper/paper.py`, `tex/registry.json`)

Drawn in D units with the v2 helpers; Thai shaped by Chromium from embedded fonts. Style: paper `#fff5df` with faint grain, printed ink `#836d4e`, dark ink `#574430`, red `#b61d32`, navy `#081148`, cream on red `#f3d9a8`; ink outline `#2a1712` about 6 px. Use: map the PNG 1:1 onto a quad of `size_D`; alpha items use the alpha. `P.REGISTRY[name]` = {svg, png, size_D, px, kind, note, transparent}.

| name | size_D | px | text (exact) | used in |
|---|---|---|---|---|
| `forecast_sheet` | 1.08 x 1.40 | 1580 x 2048 | `U.S. WEATHER BUREAU`; typewriter `OFFICIAL FORECAST` / `SEPT. 20, 1938`; typed Thai `ฝนตก`, `ลมกระโชก`; red round stamp `ทางการ` (ring: `U.S. WEATHER BUREAU ★ WASHINGTON D.C. ★`, `20 SEP 1938`); torn bottom | 14 |
| `forecast_sheet_teletype` | same | same | as above, no stamp, straight bottom | 14, the chief's paper |
| `forecast_sheet_base` | same | same | sheet without words and stamp | 14 |
| `forecast_word_1`, `forecast_word_2`, `forecast_stamp` | same | same | `ฝนตก` (pops 30.85 s), `ลมกระโชก` (31.30 s), the stamp (29.82 s), each alone | 14 |
| `forecast_sheet_en` | same | same | `RAIN,` / `GUSTY WINDS`, stamp `OFFICIAL` | not used |
| `nickname_label` | 1.15 x 0.34 | 2400 x 710 | `ทางด่วนพายุ` red-brown brush, red underline, doodled road with an up arrow; pin `P.LB_PIN` (0.50, 0.045) | 13, 17, 18, 19-22, 25 |
| `calendar_pad_20` | 0.66 x 0.90 | 1173 x 1600 | `SEPTEMBER` / `20` / `TUESDAY` / `1938` | 4 |
| `calendar_pad_21` | 0.66 x 0.90 | 1173 x 1600 | `SEPTEMBER` / `21` / `WEDNESDAY` / `1938` | 17, 18, 25, kitchen wall |
| `calendar_leaf_20`, `calendar_leaf_21` | 0.62 x 0.86 | 1153 x 1600 | the top leaf alone, at offset (0.02, 0.02) in the pad | flutter quad |
| `newspaper` | 1.50 x 1.95 | 2000 x 2600 | masthead `Long Island Daily`; `WEDNESDAY, SEPTEMBER 21, 1938`; weather box `พยากรณ์อากาศวันนี้`, big `ฝนตก`, smaller `ลมกระโชก`; lighthouse engraving; headline and columns greeked | 15, 26 |
| `newspaper_en` | same | same | `TODAY'S FORECAST` / `RAIN,` / `GUSTY WINDS` | not used |
| `newspaper_bleed` | same | 12 frames | drop and ink bleed on `ฝนตก`, f_00-f_11 | 26 from 64.95 s |
| `speed_sign` | 0.26 x 0.26 | 1600 | `100` (Kanit Black, navy), `กม./ชม.` | 20 |
| `speed_sign_back` | 0.26 x 0.26 | 1600 | painted back | 20 |
| `stamp_impression` | 0.34 x 0.34 | 1500 | the `ทางการ` stamp alone | |
| `stamp_face` | 0.34 x 0.34 | 1500 | mirrored stamp on red-brown rubber | 14 |
| `tick_stamp` | 0.20 x 0.20 | 1500 | tick mark, no words | 7 |
| `no_right_turn`, `no_left_turn` | 0.22 x 0.22 | 1500 | pictograms, no words | 19 |
| `compass` | 0.30 x 0.30 | 1500 | red north point, `N` | 19 |
| `spinner_disc`, `spinner_disc_ghost` | 0.16 x 0.16 | 1500 | red disc with cream spiral, grey ghost | 5-11, 19-22, 25 |
| `paper_tape` | 0.12 x 0.80 | 240 x 1600 | teletype tape, greeked rows | 4 |
| `desk_typed_sheet` | 0.50 x 0.65 | 1231 x 1600 | greeked typed sheet | 12 |
| `beach_sign` | 2.20 x 0.95 | 2400 x 1036 | `LONG ISLAND` / `BATHING BEACH · SUFFOLK COUNTY 1938` | 8, 16, 23 |

Text baked into set textures (not in the registry): office sign, map, date slip and calendar (section 3.4); beach set sign and LIFEGUARD (section 5.4). Language policy of film 1: forecast words, stamp, newspaper weather box, label and the km/h unit Thai; signs, map print, calendar, masthead and dateline English. Each function takes parameters (`forecast_svg(lang, words, stamp, torn, paper, only)`, `label_svg(seed)`, `calendar_svg(day, part)`, `newspaper_svg(lang, bleed)` and so on) and `long_px`. Thai is laid out one grapheme cluster per `<text>` so marks sit on their base letters; check at full size with `python3 v3/paper/paper.py crops`.

---

## 8. Dressing a set for a different story with what exists

Copy the set files into the new project and change them there, or (for one film) change things at runtime after `build()`. Every recipe below works on the built scene.

| change | how | where it shows |
|---|---|---|
| re-skin a sign or any card face | draw a new SVG at the face's `size_D`, rasterise with `raster.js`, swap the image on the object's material (recipe below). Office faces with their own material: `sign_face` (3.04 x 0.48), `calendar_face` (0.60 x 0.82), `clock_face`, `pinboard_face`, `certificate_face`, `board_left_face`, `barometer`, `coatstand`. For permanent changes edit `textures._sign()` (text string, fit width 2.42 D) and the other drawing functions | every camera that sees the wall |
| swap the wall artwork | the map is `map_paper` (3.0 x 2.16 D, `textures.wall_map`); any poster, chart or painting of that ratio swaps the same way. Keep the readable item beside the subject, not right behind it | the map wall |
| swap or move props | build new props with `S.MB()` boxes and `S.mat_lit` in an extension module (pattern: `office_props.py`), add an ink hull `S.add_hull(ob, 0.00384 x distance)`, call `S.no_bounce(ob)`. Hide an unwanted set object with `bpy.data.objects[name].hide_render = True` | |
| change the light | office: `OL.apply('office_day'|'office_grey'|'office_storm')`; beach: `BX.build(light)` with one of four plan names; kitchen: `KS.build('kitchen_grey'|'kitchen_storm')`. A new preset is a dict in `PRESETS` (office, kitchen) or `beach3d.PRESETS` (pattern: `STORM_APPROACH` in `beach_ext.py`) | |
| change the time of day outside | swap the sky card image (`sky`, `OL` skies) or the beach sky colours in the preset | window, horizon |
| change wall and floor colours | edit the hex values in `textures.py` (`WALL3`, `COLOUR` dict) and re-run; keep shade hue 240-260 with per-surface `shade_mul` (check with `hue_report.py`) | |

Re-skin recipe (tested in this session: the sign read "HARBOUR MASTER" from `low_rake`):

```python
import sys, os, json, subprocess; sys.path.insert(0, "v3/set3d")
import bpy, office3d as S
A = S.build("INTERIOR_DAY")
w, h, ppd = 3.04, 0.48, 600                      # the set's sign size in D
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{int(w*ppd)}" height="{int(h*ppd)}" viewBox="0 0 {w} {h}">
<rect x="0.02" y="0.02" width="{w-0.04}" height="{h-0.04}" fill="#3d1c12" stroke="#2a1712" stroke-width="0.025"/>
<rect x="0.055" y="0.055" width="{w-0.11}" height="{h-0.11}" fill="#1c403d" stroke="#cb9f48" stroke-width="0.016"/>
<text x="{w/2}" y="0.31" font-family="DejaVu Serif" font-weight="bold" font-size="0.19" fill="#e9d9b0"
 text-anchor="middle" textLength="2.42" lengthAdjust="spacingAndGlyphs">HARBOUR MASTER</text></svg>'''
os.makedirs("v3/tmp", exist_ok=True); open("v3/tmp/sign_new.svg", "w").write(svg)
json.dump([dict(src=os.path.abspath("v3/tmp/sign_new.svg"), out=os.path.abspath("v3/tmp/sign_new.png"),
                w=int(w*ppd), h=int(h*ppd), transparent=True)], open("v3/tmp/job.json", "w"))
subprocess.run(["node", "v3/set3d/raster.js", "v3/tmp/job.json"], check=True,
               env=dict(os.environ, NODE_PATH=os.environ.get("NODE_PATH", "/opt/node22/lib/node_modules")))
def swap_image(obj_name, png):
    for sl in bpy.data.objects[obj_name].material_slots:
        for n in sl.material.node_tree.nodes:
            if n.bl_idname == "ShaderNodeTexImage": n.image = S._img(os.path.abspath(png))
swap_image("sign_face", "v3/tmp/sign_new.png")
```

Light-change recipe (tested: returned the office_grey numbers and rendered):

```python
import sys; sys.path[:0] = ["v3/set3d", "v3/set3d_ext/light"]
import office3d as S, office_light as OL
A = S.build("INTERIOR_DAY"); print(OL.apply("office_grey")); OL.set_rain(drizzle=1.0, lash=0.0)
```

Thai text on a sign: use the paper module's per-cluster method (`paper.th(...)` with an embedded Kanit font), not a plain `<text>` in the system font.

---

## 9. Building a NEW set

### 9.1 Procedure

1. From the shot plan, list every framing the set must serve: camera height and pitch class (low 0.9-1.2 D at +14 to +20 deg, eye 2.1-2.6 D, high 3.7-4.75 D at -22 to -43 deg, inserts 0.7-0.9 D from a prop), where the actors stand, what text must read, what moves.
2. Copy the structure of `v3/set3d/office3d.py` (big set) or `v3/set3d_kitchen/kitchen3d.py` (one framing). Import `office3d` for `mat_lit`, `mat_emit`, `mat_card`, `add_hull`, `MB`, `no_bounce`, `setup_render`, `setup_grade`, `make_camera`. 1 unit = 1 D; floor z = 0; one back plane at a round coordinate.
3. Write the textures module: one function per surface returning SVG in D units, a sha1 cache, `raster.js`. Draw seams and detail lines at 0.65-0.70 of the surface (night 0.45); plank widths 0.16-0.28 D; repeat motifs about 0.3 D. At least one texel per screen pixel at the closest shot, never far finer.
4. Build in layers: shell (floor, walls, ceiling or sky) with relief strips; the subject band (where actors stand, the story prop); a foreground layer within 1-2 D of the main lenses (desk, chair, fence post, porch corner) in shade; a far wall, horizon or sky behind the subject band; emitters (bulbs, lamp slits, lit windows, flames) in frame in most framings. Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light.
5. Light: one Sun as the key, `SHADE` blue (B about 2 x R), `LIFT` small and slightly blue, per-surface `shade_mul` tints so warm woods shade orange-brown and reds shade crimson. Choose the sun height for where the shadows must fall: 35-50 deg puts whole-figure shadows on the floor (the reference); 10 deg puts them on the wall.
6. Return anchors: marks for every actor position, prop rectangles, named cameras `{loc, look_at, lens: 22}`, `key_dir`. Setters with `frame=None|N` driven by custom properties on one control empty (pattern `track_ctl`, `props_ctl`, `beach_ctl`).
7. Write `API.md` beside the file before any shot uses it.
8. Render stills of every named camera with stand-in cards (`S.placeholder_actor` or `stage.actors`), measure, compare with named reference frames, repair. One builder, one independent reviewer who repairs (template `workflows/08_assets_second_set_and_cast.js`, prompts to rewrite). Film 1's beach plus extra cast took about 1.5 hours of wall time.

### 9.2 Acceptance list (measured on the stills with stand-in actors)

| check | pass | tool |
|---|---|---|
| hue make-up over the named cameras | red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10 % of chroma; sat 0.38-0.48; val 0.45-0.63; dark (V < 0.25) 8-15 % (exteriors, night, storm may sit outside: say why) | `python3 v3/tools/hue_report.py "stills/*.png"` |
| shade against lit on the same surface | 0.15-0.31 of lit luminance; shade hue 240-260 | `v3/shots/qa_light.py` |
| cast-shadow edge | 4-21 px (10-90 % width) | `qa_light.py` |
| emitters glow | at least one source above scene-linear 1.0 in the main framings; halo 12-24 px beyond the core; heads do not glow (at most 1-3 levels in a 24 px ring) | look at the graded still |
| sharpness | Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. | look at full size |
| foreground element | something in shade within the nearest 15 % of the frame in wide and medium framings | look |
| caption band | no head and no text in y 880-950 | draw the band on the stills |
| signs readable | the story's text at least about 120 px tall or wide on a phone; one or two legible lines per prop; Thai marks on their base letters at full size | look at full size |
| density | interior wide 20-26 distinct objects, exterior 12-18; Canny 60/140 edge density at least 0.05 (office reached 0.081-0.086); featureless 40 px blocks at most 0.25-0.30 | count; `__PROJ__/ref/crops/env/tools/metrics.py` style measures (not bundled) |
| brightness structure | top eighth 40-90, brightest middle band 105-150, bottom eighth 30-70 (0-255); wall ring around heads 95-170 | measure |
| perspective | floor or ceiling lines converge to the vanishing point the camera matrix predicts; a 0.5 D sideways move gives real parallax (a flat 2D move explains 10-45 % of features) | `v3/shots/qa_parallax.py` |
| no shimmer | no texture far finer than the screen on a moving camera | draft a moving strip |
| contract | anchors drawn on every camera land where they should; a keyed state renders identical to the set state; two builds give identical pixels | debug markers, pixel diff |
| cost | under about 6 s wall per final frame on 4 free threads (about 18-23 CPU s at 12 samples) | time a frame loop |

---

## 10. What the reviews found wrong with the sets, and the better choice next time

| problem in film 1 | evidence | better choice next time |
|---|---|---|
| actor shadows on the wall, two leg lines on the floor | sun 10 deg up to light the whole map wall | sun 35-50 deg as in the reference; light the wall prop another way (lamp, painted pool) |
| colour went magenta (25-28 %) | violet ambient, rose wall, plum lift | blue ambient, per-surface shade tints, crimson-terracotta walls, real blue blocks; run `hue_report.py` on the first stills |
| explainer sequence cold for 15 s | mechanism blue 46-67 %, pale lavender walls | warm key on diagram props from the start |
| flat surfaces | edge density 0.051 against 0.062-0.068; thin-line share 0.051 against 0.065-0.074 | more fine seams, brush grain and small props in the texture code |
| things the story needs too small | fog bank 40-60 px strip, ghost storms tiny | at least about 120 px on screen; check at plan time |
| beach too bright and empty | deep darks 1 % (target 8-15); shot 16 sat 0.24 | a foreground dune lip, fence post or porch corner in shade per framing; never tilt onto empty sky |
| kitchen all warm | s15 blue 6.5 % | a cool window light and a real blue block |
| lamp discs flat white in v1 | V > 0.95 share 1.2 % against 5-6 % | bloom on emitters in the render from the opening (now in `setup_grade`) |
| caption band | two shots put text or heads in y 880-950 | check at planning time |
| design choice changed mid-production (ruled vs hand-drawn line) | two restarts | show both variants on the opening; keep each behind a switch (`TRACK_STYLE`) |

---

## Snippets run in this session

1. Cache regeneration, all six commands, on a fresh copy of `pipeline/` (times in 2.2). Without `fonts/th/Kanit_800ExtraBold.ttf` the paper step failed at once.
2. Office: `S.build`, `X.build`, `M.build`, anchors and camera names printed, preview render of `eye_two_shot` (values in sections 3 and 4 checked against the output: 46 SET objects, 62 PROPS, 47 MECH, 18 prop cameras, 13 mechanism cameras, track width 0.038, arc 1.07607, chord 1.01617).
3. Beach: `BX.build('grey_drizzle')`, cottage list, marks, cameras, preview render of `beach_shore_eye`.
4. Kitchen: `KS.build('kitchen_grey')`, anchors, `set_state(steam=5, window=('drizzle', 3))`, preview render of `table` (a float `steam` raised `TypeError`).
5. Re-skin of `sign_face` through `raster.js`, rendered from `low_rake`.
6. `OL.apply('office_grey')` with rain, rendered.
7. Fact-check re-run on a fresh copy of the bundled `pipeline/` with the caches in place: the office snippet of 3.9 (preview of `G`, 2.1 s), the re-skin recipe of 8 (rendered from `low_rake`), the beach snippet of 5.8 (3.0 s with build and render) and the kitchen snippet of 6.4 (17.8 s on a cold kitchen cache), all as printed here; anchors, marks and cameras printed from `S.build`, `X.build`, `M.build`, `BX.build`, `KS.build` agree with the tables of this chapter and of `camera.md` 2.2.

## Sources

`pipeline/`: `v3/set3d/office3d.py`, `textures.py`, `API.md`, `REVIEW.md`; `v2/sets/office.py`; `v3/set3d_ext/props/API.md`, `office_props.py`, `make_hi_map.py`; `v3/set3d_ext/light/API.md`, `office_light.py`, `gen_tex.py`; `v3/set3d_ext/mech/API.md`, `office_mech.py`; `v3/set3d_beach/API.md`, `REVIEW.md`, `beach3d.py`, `beach_tex.py`; `v3/set3d_ext/beach/API.md`, `beach_ext.py`; `v3/set3d_kitchen/API.md`, `kitchen3d.py`, `kitchen_tex.py`, `kitchen_geom.py`; `v3/paper/API.md`, `paper.py`; `v3/out/COLOUR.md`; `v3/film/s10/otake.py`, `s17/otake.py`, `s19/shot.py`, `s19/QA.md`; `spec/environment_materials.md`, `spec/LOOK_SPEC.md` (3.1-3.5); `__PROJ__/plan/shot_plan.json` (shots, sets_needed; not bundled). `__PROJ__`: `v3/film/s*/meta.json`, `deliver/QA_film.md`, `deliver/QA_film_v1_1.md`, `v3/film/out_v11/graded/` (sheet frames). Skill: `references/look.md`, `references/next-film.md`, `references/environment.md`.
