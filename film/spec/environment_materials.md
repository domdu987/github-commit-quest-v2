# Environments, materials and set dressing (lens: environment_materials)

Reference: clip A "Why Perfect Railroads Don't Work" (`ref/a/tSS.S.jpg`), clip B "The Ancient Jar That Warned an Empire" (`ref/b/tSS.S.jpg`), 720x1280, 30 fps. All pixel values are in 720x1280 frames. `D` = character head diameter including its outline (same unit as `character_anatomy.md`; a standing character is about 3.1-3.4 D from head top to feet).

Evidence: 26 frames opened at full resolution (A t04.0 t09.0 t11.0 t16.0 t27.5 t29.5 t32.0 t34.0 t36.0 t45.0 t48.5 t53.0 t60.5; B t03.0 t07.0 t18.5 t22.0 t23.0 t27.5 t30.0 t32.0 t41.0 t44.0 t46.0 t49.0 t62.0), plus 8 contact sheets covering every second of both clips and 11 zoomed crop sheets. Crops: `ref/crops/env/*.jpg`. Measurement scripts: `ref/crops/env/tools/` (`metrics.py` global stats, `prof.py`/`lines.py` line profiles, `pal.py`/`samp.py` colours, `tex.py` texture, `blur.py` depth of field, `shots.py` camera motion, `vp.py` vanishing points, `heads.py` head sizes). Extra 30 fps frames: `ref/extra/env/`.

Prototype of the recipes below, drawn by code and rasterised with Chromium (no Blender): `spec/env_proto/gen_styleframes.py` -> `office_styleframe.png`, `beach_styleframe.png`, `tex_floor_planks.png`, `tex_wall_office.png`, overview `proto_overview.jpg`. Its measured statistics are in section 2.9.

Accuracy: video compression blurs edges by 1-2 px, so line widths are +/- 1 px. Prop counts are hand counts and are approximate. Items I could not determine are listed in section 1.9.

---

## 1. Observations

### 1.1 The two clips build their worlds differently

**Clip A is a real 3D world with no ink on the environment.**
- The camera travels through the set with strong perspective in almost every shot. Of 129 frame pairs 0.5 s apart, only 16 (12 percent) can be explained by a 2D zoom/pan of a flat picture; the rest show parallax.
- Geometry is visibly polygonal: the canyon wall is a flat-shaded low-poly mesh with triangular facets 60-150 px across, plus thin dashed strata lines (A t45.0, crop `A_surfaces.jpg`). Ballast stones are individually shaded pebbles 10-25 px with their own shadows (A t16.0). Sleepers, rails, crates, the trestle and the station roof ribs are modelled boxes and beams (A t34.0, A t48.5, A t60.5).
- Light is a hard sun: projected shadows have crisp edges and a blue-plum tint (A t32.0 newspaper shadow, A t34.0 roof-rib shadows, A t53.0 umbrella shadow).
- No object in the environment has a drawn outline. Edges are made by (a) colour change between flat blocks, (b) contrast trim strips, for example a 13 px yellow-green band along every red panel in the train car (A t27.5), (c) dark seams painted into plank textures (A t32.0), (d) cast shadows. Zoomed proof: `A_edge_zoom6.jpg`.
- Only the characters carry ink.

**Clip B is an inked storybook illustration, with a few 3D-rendered inserts.**
- Sets are drawn like a painted backdrop: flat fills with soft painted gradients, a dark ink line around every object, thinner tinted lines for bricks, tiles and wood grain (crops `B_outline_detail1.jpg`, `B_outline_detail2.jpg`, `B_outline_zoom6.jpg`).
- 55 of 129 frame pairs (43 percent) fit a 2D zoom/pan: most shots are a slow push-in or drift over a flat painting. The exception is the orbit around the jar (B t08.0-t13.0), where the hall turns in true perspective.
- Nothing casts a hard projected shadow. Characters, benches and tables meet the floor with no shadow at all in B t07.0, B t23.0, B t27.5 and B t44.0 (crop `B_contact_shadows.jpg`); the most that appears is a faint soft smudge directly under a figure (guard in B t41.5, frog in B t46.5, crop `B_shadow_check.jpg`). All light is painted: a warm bright pool in the middle of the frame, darker top and bottom, glowing candles and torches.
- The hero props are different: in close-ups the jar, dragons, frogs and the goblet are 3D-shaded objects with a thin 1-2 px contour, soft shading and specular highlights (B t01.0, B t03.0, B t20.0). The pendulum shots inside the jar (B t49.0-t55.0) are fully 3D: riveted plates, bronze bob, bloom on the lights, still with thin dark contours (crop `B_3d_inserts.jpg`). In wide shots the same jar is drawn flat with a 3-4 px ink line (B t32.0).
- Shallow depth of field is used only in the tight close-ups B t03.0-t05.0 and the balcony shot B t17.0; everything else is sharp front to back.

### 1.2 Outlines on the environment
- Clip A: none (see 1.1). Do not add ink to terrain, sky, walls or floors when imitating A.
- Clip B: three line weights, used consistently.
  1. Object silhouettes: 2-6 px, mostly 3-5 px. Colour is not pure black: a very dark, warm brown in warm scenes (`#1f0000`, `#210c07`, `#321d1a`, `#3f0708`) and dark navy-purple at night (`#1d1449`, `#190217`).
  2. Interior detail lines (brick joints, floor tiles, plank lines, drapery folds): 1-2 px, drawn in a darker tint of the surface itself at 0.65-0.70 of its luminance (day) or 0.42-0.55 (night). Example: mortar `#8c785f` on stone `#c3b4a1`.
  3. Contours of the 3D hero props: 1-2 px, near black (`#2c0000`, `#2f1e0e`, `#1a191f`).
- For comparison the character ink is 5-10 px (B t07.0 8 px, B t23.0 9 px, A t27.5 10 px, A t45.0 10 px). So the hierarchy is character : set object : detail = about 8 : 3 : 1.5 px.

### 1.3 Textures
- A: stylised 3D-game surfaces. Large areas are perfectly flat colour (carpet, far sand, sky), and texture appears only where it describes a material: wood planks with dark seams and faint grain, ballast pebbles, faceted rock with strata bands, rusty joint bar with noise (A t38.5). Nothing photographic.
- B: flat cel fills plus ornament. Surfaces are covered with drawn repeat patterns (fleur-de-lis backdrop, tufted cushion, brick courses, carpet diamonds, roof slates) and small scattered marks (pebbles with a highlight, grass tufts, cracks). Over that sits a soft painted light gradient.
- Neither clip shows procedural noise as a visible texture, and neither has specular reflections on walls or floors.

### 1.4 Colour blocking
- A interior (A t27.5): five hue blocks at high saturation: orange ceiling `#c53b14`, red seats `#a1001c` to `#da0045`, maroon-purple plank walls `#5e1f36`, dark wood wainscot `#491309`, navy carpet `#152a63` falling to `#17153a`, yellow-green trim `#76712e`, warm white bulbs `#fffeec`.
- B interior (B t07.0, B t23.0): red drapery `#b64f4b`, dark red backdrop `#5e2221`, gold `#cb9f48`, navy carpet `#26395e` with red border `#562025`, cool grey stone `#7d858e`, dark wood `#26140a`.
- Both interiors therefore use the same scheme: warm reds, browns and gold on the walls and furniture, one cool dark block (navy) on the floor, cream or white only for small accents. The white heads are the brightest large shapes in frame.
- A exterior: two-block complementary scheme, orange-red ground against blue sky (A t09.0 sand `#f3ad6f`, sky `#639de9`), shadows pushed to plum.
- B exterior: one dominant light colour per time of day: day stone cream `#c8bdac` with blue sky `#6497d6` (B t27.5), sunset rose to apricot (B t30.0, B t32.0), night monochrome blue-violet `#545493`/`#7673b5` with small warm window accents (B t44.0).

### 1.5 Depth staging and haze
- A: the ground plane runs to a true horizon. Distant landforms change hue with distance: near sand `#e79a4f`, far sand `#e78c6d`, mesas lavender `#8d78b0`, farthest hills sky blue `#7393d0` (A t09.0). The canyon void fades to saturated blue `#3a65c3` then `#12258b` (A t04.0). Three clear planes: foreground ground texture, character plane, far vista.
- B: depth is a value ramp. Foreground is darkest (B t32.0 near grass `#5a512e`, V 0.35), midground lit (`#a78039`), far city pale and sky-tinted (`#ec918c`, V 0.93; B t46.0 far castle `#cdaa88`, far hill `#f4c3a9`). A dark foreground element often frames the top or a side (tree branch in B t32.0 and B t46.0, banner in B t17.0). Far objects keep outlines but thinner and lighter.
- Both clips keep the bottom of the frame darkest and the middle band brightest (section 2.2). This comes from the picture content (dark floors and foregrounds, light pooled on the subject), not from a lens vignette; `color_light_post.md` measured no separable vignette on flat walls.

### 1.6 Ground and sky
- A grounds: plank floors with seams (A t32.0, A t34.0, A t48.5), ballast with sleepers (A t16.0), flat sand with a few footprint marks (A t09.0), carpet (A t27.5). A skies: smooth gradient, darker blue at the top, pale at the horizon, with soft airbrushed clouds that have no outline (A t09.0); sunset version lavender to cream to pink (A t60.5).
- B grounds: tan road with darker cart-track bands, inked pebbles and grass tufts (B t27.5); patterned carpet runner on grey stone tiles (B t07.0, B t18.5); grass built from strokes plus flower dots (B t32.0). B skies: gradient with two-tone clouds (violet top, cream underside), radial sun rays, a flat sun disc (B t30.0); night gradient with a glowing moon (B t44.0).

### 1.7 Text-bearing props (all in clip A)
- Newspaper (A t32.0, A t33.0): cream sheet, masthead in mixed-case old-style serif, double hairline rule, two-line headline in bold widely spaced slab capitals filling about 85 percent of the sheet width, an engraving-style line drawing in a ruled box, tiny capitals in the top corners. Ink is warm brown-grey, not black.
- Calendar (A t36.0): red card, cream slab capitals "CALENDAR", italic line, bold year, two stars, double gold rules at both sides; white tear-off page with a large red fat-face month name, a hairline, weekday initials and pale grey numerals.
- Signs: cream board with an inset dark border, red slab capitals and a small dark sub-line, four corner nails ("ALL ABOARD!", A t35.0); white banner with red and blue stripes and two lines of fat-face capitals in navy and red (A t11.0); station name in thin gold capitals on a dark fascia (A t11.0, A t29.5).
- Rule: one or two lines are large and legible, everything else is greeked. The small text in the reference is not readable (crop `A_text_props.jpg`).
- Clip B has almost no text, only pictograms on notices and banners (B t27.5).

### 1.8 Prop density
- A is sparse outdoors (4-12 distinct set objects) and moderate indoors (11-16). B is dense everywhere (25-35 objects plus ground scatter). Counts in section 2.7.

### 1.9 Not determinable
- The production method. Garbled small lettering and mirrored chalk marks (A t45.0) suggest generated footage; I cannot confirm how either clip was made, so "true 3D" above means "behaves and shades like 3D".
- The focal length. One rough estimate from floor tiles (section 2.8) carries about 30 percent error.
- Neither clip contains sea, rain or an office. The sea and storm palettes in section 3 are extrapolated from the blues that do appear (A t04.0, A t53.0, B t41.0, B t44.0).

---

## 2. Measurements

### 2.1 Whole-frame statistics (caption band y 850-960 excluded)

| Quantity | Clip A (130 frames) median, p10-p90 | Clip B (130 frames) median, p10-p90 | v1 frame20 / frame45 |
|---|---|---|---|
| Mean HSV saturation | 0.485, 0.34-0.62 | 0.405, 0.28-0.57 | 0.288 / 0.289 |
| Mean HSV value | 0.655, 0.46-0.74 | 0.584, 0.40-0.74 | 0.734 / 0.724 |
| Canny edge density (60/140) | 0.060, 0.024-0.091 | 0.067, 0.022-0.107 | 0.016 / 0.017 |
| Mean absolute Laplacian | 6.5 | 9.9 | 3.5 / 3.6 |
| Occupied colour bins (4 bits per channel, over 0.2 percent) | 99.5 | 100 | 64 / 65 |
| Share of featureless 40 px blocks (high-pass std under 3) | 0.30 | 0.27 | 0.63 / 0.64 |

Single frames, featureless share: B t18.5 0.06, B t07.0 0.09, B t27.5 0.08, B t23.0 0.18, A t34.0 0.05, A t32.0 0.10, A t27.5 0.46, A t09.0 0.82.

### 2.2 Where the light sits (mean luminance 0-255 on an 8 x 5 grid)

| Zone | Clip A all frames | Clip B all frames | A train interior t27.0-t28.5 | B throne room, 11 frames | v1 |
|---|---|---|---|---|---|
| Top row | 119 | 108 | 100 | 60-70 | 213 |
| Middle rows | 120 | 125 | row 3 centre 136 | row 3 centre 169 | 154 |
| Bottom row | 93 | 79 | 32-47 | 49-65 | 160 |
| Four corners / centre | 104 / 123 | 92 / 128 | - | - | 186 / 143 |

Background luminance in a ring around each head: A median 120 (p25 95, p75 164, 72 heads), B median 136 (104-170, 51 heads).

### 2.3 Outlines and seams

| Item | Value | Frame |
|---|---|---|
| Share of pixels on thin dark lines (black-hat over 28) | B 0.11-0.36 (t23.0 0.109, t44.0 0.170, t07.0 0.177, t27.5 0.198, t62.0 0.356); A 0.001-0.017 on walls, facade, canyon; v1 wall and floor 0.000 | as listed, A t34.0, A t27.5, A t45.0 |
| Table edge ink | 5 px, `#1f0000` | B t23.0 x=460 |
| Curtain edge ink | 4 px, `#321d1a` | B t07.0 y=500 |
| Halberd pole ink | 3 px each side of an 8 px pole, `#210c07` | B t07.0 y=620 |
| Banner edge ink | 2-3 px, `#510d0a` | B t27.5 y=260 |
| Haystack edge ink, night | 2-3 px, `#1d1449` | B t44.0 y=560 |
| Jar edge in a wide shot | 3-4 px, `#3f0708` | B t32.0 y=600 |
| Brick joint | 2 px, luminance 123-144 on 185-207 (ratio 0.65-0.70), `#8c785f` | B t27.5 x=10 |
| Brick course height | 23.5-26 px | B t27.5 x=10, x=250 |
| Night brick joint | 2-4 px, `#293272` to `#061655`, luminance 25-77 on 127 | B t44.0 x=100 |
| 3D hero prop contour | 1-2 px, `#2c0000` / `#2f1e0e` / `#1a191f` | B t49.0 y=740, B t03.0 y=620, B t03.0 y=1010 |
| Character head ink (for the ratio) | 8, 9, 10, 10 px | B t07.0, B t23.0, A t27.5, A t45.0 |
| Floor plank seam | 5 px wide, `#432219`, luminance 42 on 120-135 (ratio 0.33-0.40) | A t32.0 y=1020 |
| Floor plank width | 52 px at y=1020, 67 px at y=1150; head 240 px, so 0.28 D | A t32.0 |
| Cross-plank seams | 2-3 px, spacing 12 to 25 px from y=900 to y=1100 | A t34.0 x=100 |
| Carriage siding plank | 60 px median (head about 280 px, 0.21 D), seam ratio 0.53-0.55 | A t29.5 y=1050, y=1150 |
| Wall plank | 25 px (0.16 D), seam ratio 0.68-0.70 | A t27.5 y=460 |
| Deck board | 31 px, seam ratio 0.66 | A t48.5 y=900 |
| Contrast trim band | 13 px wide, luminance 95-105 against 52 | A t27.5 x=200 |
| Repeat pattern pitch | fleur-de-lis 48 x 58 px (0.32 x 0.38 D at D 152); cushion tufts 29 px (0.19 D) | B t07.0 |

### 2.4 Surface texture strength (std of luminance after removing a 3 px Gaussian)

| Surface | Value | Frame |
|---|---|---|
| A flat areas: carpet, far sand, sky | 0.3, 1.0, 0.5 | A t27.5, A t09.0 |
| A plank wall, ceiling planks, floor planks | 7.0, 3.4, 7.8 (21.3 in raking light) | A t27.5, A t32.0, A t34.0 |
| A canyon wall, ballast | 5.7, 18.2 | A t45.0 |
| B stone floor, backdrop, carpet, table | 17.3, 22.7, 11.9, 16.6 | B t07.0, B t23.0 |
| B stone wall day / night, road, grass | 19.6 / 18.3, 5.3-7.2, 10.1 | B t27.5, B t44.0, B t32.0 |
| v1 wall, v1 floor | 0.5, 0.7 | v1 frame20 |

### 2.5 Light, shadow, focus

| Item | Value | Frame |
|---|---|---|
| Cast shadow darkness, A | shadow / lit luminance 0.36 (42-47 on 116-123), 0.41 (57-59 on about 140), 0.28 (40 on 141) | A t32.0 y=1010, A t34.0 x=300, A t53.0 y=700 |
| Cast shadow colour, A | `#2a2836` on floor `#7d523f`; `#494860` on `#a07452` (blue channel kept, red cut to 0.34-0.46) | A t32.0, A t34.0 |
| Cast shadow edge, A | full transition within 8 px | A t32.0 |
| Cast shadows, B | no hard shadows anywhere; none at all in four frames, a faint soft smudge under the figure in two | none: B t07.0, B t23.0, B t27.5, B t44.0; smudge: B t41.5, B t46.5 |
| Lamp bulb | core `#fffeec`, 62 x 70 px = 0.40-0.45 D; halo ring out to 1.3-1.6 core radii at luminance 130 falling to 99, ambient 68-92; holder `#e2a630` | A t27.5 |
| Background blur in close-ups, B | edge 10-90 percent width 9.3 px behind, 1.6 px on the prop (Gaussian sigma about 3.6 px) | B t03.0 |
| Same, other shots | B t04.0 8.4 px, B t17.0 4.7 px, all other B shots 1.6-2.3 px, all A shots 1.9-3.1 px | as listed |

### 2.6 Scale of props against the head diameter D

| Prop | Size | Frame (D in px) |
|---|---|---|
| Armchair: frame width, back width, height | 2.2 D, 1.37 D, 3.7 D | A t27.5 (157) |
| Side table: top width, height | 0.9 D, 1.65 D | A t27.5 |
| Room height at the back wall | 3.95 D (low train car) | A t27.5 |
| Newspaper | 1.08 x 1.4 D (ratio 0.76) | A t32.0 (240) |
| Toolbox width | 1.0 D | A t45.0 (160) |
| Beach umbrella width | 3.85 D | A t53.0 (100) |
| Throne: width, height | 2.2 D, 4.4 D | B t07.0 (152) |
| Halberd length | 4.3 D | B t07.0 |
| City gate opening | 3.5 x 4.9 D | B t27.5 (66) |
| Wall banner | 0.75 x 3.8 D | B t27.5 (bystander 85) |
| Jar (hero prop) | 2.8 x 4.4 D | B t32.0 (about 95, read from a grid) |
| Head width itself | A 130-212 px, B 135-223 px in medium shots; v1 196-224 px | several |

### 2.7 Prop counts (hand counts; architecture shell, repeated bricks or planks and characters excluded)

| Frame | Distinct set objects | Scatter |
|---|---|---|
| A t27.5 train interior | 11 (16 with ceiling beams): armchair, 2 seat partitions, tripod table, ball, 2 pendant lamps, 2 sconces, 2 window slivers | - |
| A t32.0 concourse | 9: carriage with 5 lit windows, 3-globe lamp post, 2 potted palms, 5 roof trusses, red carpet strip | - |
| A t34.0 station facade | 15: clock, 8 bunting swags, crate stack, 2 sacks, locomotive | about 36 windows |
| A t45.0 trackside | 9: toolbox, thermometer, calendar, caliper, flag, rail, 3 sleepers | about 250 stones |
| A t16.0 track low angle | 4 types: rails, sleepers, far trestle, fence | stones |
| A t53.0 deck | 12: umbrella, deck chair, table, glass, 3 lamp posts, rails, fence, 3 mesas | - |
| B t07.0 throne | 26: throne, crest, 2 curtains, 3 swags, 6 tassels, 2 tie-backs, 2 halberds, candelabrum, 2 windows, 2 shields, 3 finials, carpet | about 60 wall motifs |
| B t23.0 banquet | 26: chandelier, rose window, throne group, 2 candelabra, column, banner, topiary, halberd, statue, 2 frogs, table, bench, 3 goblets, jug, roast, bread, candle, steps, carpet, 3 arches | - |
| B t27.5 city gate | 30 | about 24 stones and tufts |
| B t32.0 camp | 35 | about 70 flowers |
| B t44.0 night gate | 25 | about 70 stones and tufts |
| v1 frame20 | 5: map, desk, 2 papers, cabinet sliver | - |

### 2.8 Camera and layout

| Item | Value | Frame |
|---|---|---|
| Frame pairs 0.5 s apart that fit a 2D zoom/pan (inlier ratio over 0.35) | A 16 of 129; B 55 of 129 | all |
| Zoom rate inside those pairs | B median 6.4 percent/s (p90 27); A median 2.2 percent/s | all |
| Background stability at 30 fps | residual 0.9-1.8 of 255, drift under 0.1 px/frame (no line boil) | B t44.0, `ref/extra/env/b44_*` |
| Eye line (vanishing point height) | 45 percent of frame height A t32.0; 33 percent A t48.5; 67 percent A t16.0 (low angle); 43 percent B t23.0; 42 percent B t44.0; 54 percent B t27.5 | as listed |
| Interior zones, top to bottom | ceiling 0-18, upper wall 18-45, dark wainscot 45-66, floor 66-100 percent | A t27.5 |
| Interior zones | floor starts at about 45-50 percent; throne alcove 245 px wide = 34 percent of frame width | B t07.0, B t18.5 |
| Horizon in exteriors | 50, 34, 43 percent (A); about 20-23 percent (B, high storybook horizon) | A t09.0, A t48.5, A t53.0; B t32.0, B t46.0 |
| Focal length, rough | about 660 px, vertical field of view about 88 degrees, equal to an 18-20 mm lens on a 36 mm long side | A t32.0 floor tiles |
| Sky gradient, day | zenith `#4b74c2`, middle `#6197e5`, horizon `#99bee9` | A t04.0, A t53.0 |
| Sky gradient, sunset | `#b5a6ba`, `#dcd2cc`, `#eee2c8`, `#ebbeb7` (A); `#dc667f`, `#fba98e`, `#ffc88b` (B) | A t60.5; B t30.0 |
| Sky gradient, night | `#113299`, `#1d49bb`, `#2a67d2` | B t44.0, B t41.0 |

### 2.9 Prototype check (`spec/env_proto/*.png`, no characters in frame)

| Quantity | Office prototype | Reference interiors B t07.0 / t18.5 / t23.0 | A t27.5 | Beach prototype | A t53.0 | B t27.5 |
|---|---|---|---|---|---|---|
| Saturation | 0.44 | 0.47 / 0.32 / 0.37 | 0.74 | 0.49 | 0.50 | 0.32 |
| Edge density | 0.055 | 0.114 / 0.110 / 0.089 | 0.020 | 0.039 | 0.044 | 0.114 |
| Luminance top / middle / bottom | 66 / 106 / 39 | 66 / 114 / 70, 66 / 131 / 43, 63 / 131 / 52 | 89 / 64 / 27 | 157 / 136 / 129 | 124 / 116 / 53 | 136 / 159 / 132 |
| Corners / centre | 43 / 123 | 73 / 110, 57 / 140, 54 / 139 | 56 / 76 | 143 / 137 | 93 / 121 | 122 / 157 |

The office prototype reproduces the luminance shape and saturation of the B interiors but reaches only half their edge density; add more fine detail lines and small props to close that gap. The beach prototype matches A's saturation and edge density; its bottom edge is too bright (129 against 53) and needs a stronger foreground fall-off.

---

## 3. How to reproduce

### 3.1 Which clip to follow

| Scene | Target | Why |
|---|---|---|
| Interior office | **Clip B** hall and throne-room treatment (B t07.0, B t18.5, B t23.0): inked objects, flat fills with drawn patterns, 25 or so set objects, warm walls with one navy floor block, light pooled on the middle of the frame, no hard shadows. Borrow two things from A t27.5: glowing lamp bulbs with a tight halo, and contrast trim strips on furniture edges. | The office is a dialogue set seen in slow push-ins, which is exactly how B shoots its interior (43 percent of pairs are flat zoom/pans). The hall interior fills about 21 s of B (t00-t13, t18-t26) against about 2 s of enclosed interior in A (t27.0-t28.5), so B is the richer reference. The set must carry text props (map, calendar, sign), which are SVG work anyway. Inked props sit naturally next to inked characters. |
| Exterior beach and sea | **Clip A** staging and light (A t09.0, A t48.5, A t53.0): real ground plane running to a horizon at 34-50 percent of frame height, gradient sky with soft un-inked clouds, hue shift with distance, one hard sun with plum shadows, saturated warm ground against blue. Terrain, sea and sky carry no ink. Man-made objects (houses, poles, boat, fence, signs) keep the B-style 3 px ink. | A is the only reference with open vistas under a sun, and the advancing wave needs real depth and a moving camera. Keeping ink on the man-made objects is my judgement call so the beach and the office read as one film; a strict copy of A would drop it. |

If one style had to serve the whole film, choose B: it is cheaper to render, fully controlled by the artwork, and it avoids the "default Blender" look that made v1 miss.

### 3.2 Rules for both sets

1. Units. Build in D (head diameter). The v1 rig has D = 0.88 m; multiply every size below by the D of the final rig. Furniture is sized to the big heads, not to the thin bodies (section 2.6).
2. Colour management. Set `scene.view_settings.view_transform = 'Standard'`, look `'None'`. The bpy 5.3 default is `'AgX'`, which would shift every hex in this file.
3. Shading wrapper. This file gives albedo colours and textures. Wrap them with `lightkit_clp.env_material()` and the presets of `color_light_post.md` (`INTERIOR_LAMP` or `INTERIOR_DAY` for the office, `EXTERIOR_NOON` and `LATE_AFTERNOON` for the beach). Use only Diffuse and Emission; no Principled, no specular, no bump. If the light kit is not used, fallback graph: Image or RGB -> Mix Shader (Fac 0.2) between Emission (strength 1.0) and Diffuse BSDF (roughness 1.0).
4. Where patterns come from. Man-made patterned surfaces, anything with ink, and all text: SVG rasterised to PNG and used as an Image Texture. Large natural surfaces (sand, sea, sky, plaster variation): procedural nodes (section 3.6). Texture resolution: at least 1 texel per screen pixel at the closest shot, in practice 2048 px for a wall or floor, 1024 px for a prop face, 512 px for a small card.
5. Line weights at 720 px frame width: character ink 5-10 px (other spec), set-object silhouette 3 px (allowed 2-5), detail lines 1.5 px, wires 1.3 px. Silhouette ink colour `#2a1712` in warm or daylight scenes, `#1d1449` in night or storm scenes. Detail line colour = surface colour x 0.68 (x 0.45 at night).
6. Contrast trim. Give every furniture top a lighter front edge strip (top colour x 1.25, height 0.06 D) and every cabinet or panel a darker inset line (colour x 0.6). This is what replaces ink in clip A and it also survives when lines get thin.
7. Density. Wide office shot: 20-26 distinct set objects in frame. Any shot with characters: at least 8 objects behind them and at least three hue families. Beach wide: 12-18 objects plus 150-400 ground specks.
8. Brightness structure of interior frames: the wall band behind the heads must read luminance 95-170 (target 120), the top of frame 60-70, the bottom 40-70. Paint this fall-off into the set (gradients multiplied into the wall and floor textures, or large soft dark cards at the ceiling and floor edges). Do not apply it as a full-frame vignette, because the heads must stay near white everywhere.
9. Camera, as far as it affects the set: lens 20-24 mm with the 36 mm sensor on the 1280 px side for wides (v1 used 32 mm), eye line at 42-45 percent of frame height, and a continuous slow move in every shot (push-in about 6 percent per second). Build a ceiling and both side walls, because a lens this wide shows them.
10. Focus. Blur the set behind a tight close-up only (Gaussian sigma about 3.6 px); keep all other shots sharp.

### 3.3 Putting outlines on the environment in Blender

Use the first method that fits each object.
- Flat cards and textured surfaces: draw the ink in the SVG. Stroke width in texels = 3 x (texture px across the surface) / (screen px the surface covers in the widest shot).
- Box-like 3D props (desk, cabinet, teletype, houses, poles): inverted hull. Solidify modifier with `offset = 1`, `use_flip_normals = True`, `use_rim = False`, `material_offset = 1`; second material slot = Mix Shader driven by Geometry > Backfacing between an ink Emission and a Transparent BSDF (same construction as in `character_anatomy.md` 3.5). Thickness for a 3 px line: `t = 3 x d x 36 / (f x 1280)`, with d the camera distance and f the lens in mm. At f = 22 mm that is `0.0038 x d`: 0.015 D at d = 4 D, 0.03 D at d = 8 D. Set it once for the distance of the main shot.
- Alternative for all 3D props at once: a second Freestyle line set restricted to the set collection (`select_by_collection`), `select_silhouette`, `select_border`, `select_crease` on, absolute thickness 3.0 px, colour `#2a1712`, crease angle left at the default 134 degrees. Slower, but the width stays 3 px at any distance. All attribute names were checked in bpy 5.3 without rendering.
- Never outline: sky, clouds, sea, sand, haze cards, light shafts, glow cards.
- Far objects: thin the line to 1.5 px and lighten it toward the haze colour, as B does on its far castle.

### 3.4 Recipe 1: the 1938 weather-bureau office

Style frame: `spec/env_proto/office_styleframe.png` (generator functions can be reused per surface).

**Shell geometry (all planes and boxes, normals inward)**

| Part | Size in D | Notes |
|---|---|---|
| Floor | 9 wide x 8 deep | planks run toward the back wall |
| Back wall | 9 x 4.8 | carries the map, centred |
| Left wall, right wall | 8 x 4.8 | window in the left wall |
| Ceiling | 9 x 8, plus 3 cross beams 0.3 x 0.35 in section | ceiling `#3a2620`, beams `#2b1a17` |
| Carpet runner | 2.2 wide, from the back wall to the camera | lies 0.01 above the floor |

**Wall treatment, bottom to top (one SVG, `tex_wall_office` pattern, 2048 px = 9 D)**

| Band | Height in D | Colour and pattern |
|---|---|---|
| Baseboard | 0 to 0.15 | `#3b1c12`, 3 px ink top edge |
| Wainscot | 0.15 to 1.5 | dark wood `#55291a`; raised panels `#5f2e1d` every 0.9 D with a 2 px inset line `#33180f` and a 1.5 px highlight `#7f3d27` under the top edge |
| Chair rail | 1.5 to 1.6 | `#7b3b26`, inked |
| Wallpaper | 1.6 to 4.2 | base `#a8663f`; vertical stripes `#9e603b` 0.08 D wide at 0.16 D pitch; small diamonds `#cd7c4d` with a `#72452b` 1 px line, 0.32 x 0.38 D pitch, staggered |
| Picture rail | 4.2 to 4.27 | cream `#d9b98a`, inked |
| Frieze | 4.27 to 4.8 | `#8a5334` |

Side walls use the same texture multiplied by 0.8. Multiply a soft gradient into the wall texture: 1.0 between 1.5 and 3.5 D, falling to 0.55 at the ceiling and to 0.7 at both ends.

**Floor**: planks 0.28 D wide, base `#8e6045`, each plank x 0.90-1.08 at random, seam `#432219` at 7 percent of the plank width, butt joints staggered every 3-6 D, two or three grain streaks per plank at x 0.86-0.90. Multiply a gradient from 1.0 at the back wall to 0.45 at the camera end. Runner: navy `#26395e`, red border `#562025` 0.15 D, gold line `#cb9f48` 0.04 D, red diamonds with gold outline every 1.5 D.

**Props (boxes, cylinders and SVG cards; every item inked 3 px unless noted)**

| # | Prop | Size in D | Build | Colours |
|---|---|---|---|---|
| 1 | Wall map in frame (hero) | 4.2 x 2.6 outer, centre 3.0 above the floor | box frame 0.15 wide + SVG card 2048 px | frame `#3d1c12`, gold inner line `#cb9f48`, sea `#b9d7e4`, land `#f1e3c0`, isobars `#6f93a8` 1.2 px, grid `#8fb0bf` 0.8 px, storm track `#c2311e` 5 px with arrowhead, labels `#3d2a22` |
| 2 | Sign board "U.S. WEATHER BUREAU" | 3.8 x 0.4, above the map | SVG card | board `#1c403d`, slab capitals `#e9d9b0` |
| 3 | Desks, 2 or 3 | 3.0 wide x 1.5 deep x 1.45 high | box body + top slab + 3 drawer insets + knee-hole | body `#5b2e1c`, side in shade x 0.72, top `#8a5a35`, edge strip `#ad7142`, drawer fronts `#6b3621`, knobs `#e2a630` |
| 4 | Chairs, 2 | back 1.4 wide, top at 2.6, seat at 1.2 | boxes | `#5b2e1c`, seat `#8a5a35` |
| 5 | Pendant lamps, 2 or 3 | shade 1.0 across, bulb 0.42, bulb centre 4.0 above the floor | cone + sphere + cord | shade `#2d664a`, bulb emission `#fffeec`, cord ink |
| 6 | Banker's lamps, 2 | shade 0.7 wide, 0.6 high | half cylinder + stem + base | shade `#2d7a52`, brass `#e2a630`, emissive slit `#fffeec` |
| 7 | Teletype | 1.3 x 1.0 x 0.8 on a desk or stand 1.3 high | box + sloped top + key strip + paper roll cylinder + paper card + tape ribbon | body `#2b2630`, top `#3a3442`, keys `#e9d9b0`, roll `#d9c9a8`, paper `#f6efe2` with grey lines `#9a8f86`, tape 0.08 wide hanging 1.5 |
| 8 | Filing cabinets, 2 to 4 | 1.1 wide x 1.2 deep x 3.0 high, 4 drawers | box + drawer insets | body `#3c7250`, fronts `#437d55`, inset line `#284a33`, label cards `#f3e7c9`, pulls `#e2a630`; a box `#b08a52` and a paper stack on top |
| 9 | Banjo barometer | 0.55 x 1.4, dial 0.5 | SVG card | board `#6d3a1f`, dial `#f3e7c9`, brass ring `#e2a630`, thermometer line `#c2311e` |
| 10 | Wall clock | 0.9 across | cylinder + SVG face | rim `#3d1c12`, face `#f3e7c9`, hands ink |
| 11 | Tear-off calendar | 0.8 x 1.1 | SVG card | header `#b61d32` with `#f3d9a8` capitals, page `#f6efe2`, numeral `#b61d32` |
| 12 | Notice board with 3 pinned sheets | 0.9 x 1.2 | SVG card | cork `#7a5a34`, sheets `#f6efe2`, pins `#c2311e` |
| 13 | Coat stand with hat and coat | 3.4 high | cylinder + SVG card | pole `#6d3a1f`, coat `#3b3350`, hat `#4a3a2c` |
| 14 | Window | 2.0 x 2.8, sill at 1.6 | frame boxes + emissive pane + light-shaft card | frame `#6f3522`, pane gradient `#7da5e6` (top) to `#b9d3ee`, shaft `#ffe2a8` at 13-16 percent, additive, soft edges |
| 15 | Small dressing, 8 to 10 pieces | 0.2 to 0.8 | boxes and cards | telephone `#1c1a22`, ink bottle `#26395e`, paper stacks `#f6efe2`, red pencil `#c2311e`, wastebasket `#7a5a34`, rolled charts `#f1e3c0`, wall thermometer, second small chart, radiator `#5d5560` |

Count target: rows 1-14 give 19-23 objects and row 15 adds 8-10; arrange them so that 20-26 are inside any wide frame and at least 8 remain behind the characters in a two-shot.

**Emitters**: bulbs are the only surfaces above 1.0 (emission `#fffeec`, strength about 8 as in `lightkit_clp.emissive_material`). Bloom so that the halo ends at 1.3-1.6 bulb radii. Four to six glowing points should be visible in a wide shot (A t27.5 has four).

**Office palette**

| Role | Hex |
|---|---|
| Wall paper / stripe / motif | `#a8663f` / `#9e603b` / `#cd7c4d` |
| Dark wood, panels, rails | `#55291a`, `#5f2e1d`, `#7b3b26`, `#3b1c12` |
| Floor plank / seam | `#8e6045` / `#432219` |
| Cool block: runner, ink bottle | `#26395e` (border `#562025`, line `#cb9f48`) |
| Furniture | `#5b2e1c`, `#8a5a35`, `#ad7142` |
| Green accents: cabinets, lamp shades, sign | `#3c7250`, `#437d55`, `#2d664a`, `#1c403d` |
| Red accents: track line, calendar, pins | `#c2311e`, `#b61d32` |
| Brass and gold | `#e2a630`, `#cb9f48` |
| Paper and dials | `#f6efe2`, `#f3e7c9`, `#f1e3c0` |
| Machine black | `#2b2630`, `#1c1a22` |
| Light: bulb, shaft, sky pane | `#fffeec`, `#ffe2a8`, `#7da5e6`-`#b9d3ee` |
| Ink | `#2a1712` |

The hero wears teal and the boss yellow, so the walls stay in the orange-brown family and green is confined to small props at the sides.

### 3.5 Recipe 2: the beach town

Style frame: `spec/env_proto/beach_styleframe.png`.

**Geometry**

| Part | Size in D | Build |
|---|---|---|
| Sand | 300 x 300, 64 x 64 subdivisions | plane + Displace modifier (Clouds texture, noise scale 6 D) of 0.3 D everywhere and 1.5-3 D in a dune band 15-40 D inland |
| Sea | from the shoreline to 600 D out, 0.1 D below the sand edge | plane; optional Ocean modifier is not needed for the calm shots |
| Wet sand and foam | strips 1.5 D and 1 D wide following the shoreline | curve-extruded strips, `#c9a07a` and `#f1eef7` |
| Sky | world gradient or an emissive dome | plus 4-6 cloud cards with soft alpha and one sun-glow card |
| Far headlands | 2 cards at 400-600 D, about 4 percent of frame height | lavender `#8d78b0`, farther one blue `#7393d0` |
| Houses, 5 to 8 | 7 wide x 6 deep, eaves at 4.2, ridge at 6 | box + gable prism roof + porch slab + door 1.4 x 3.7 + 2 windows 1.2 x 1.2 with shutters + chimney box |
| Telegraph poles, 6 to 8 | 9 high, radius 0.15, spaced 14 | cylinder + crossarms 2.2 and 1.6 wide + 4 insulators + wire curves sagging 0.7 |
| Dressing | rowboat 6 long with oar, striped umbrella 3.85 across, deck chair, 6 fence posts 1.5 high with rope, crate 1.2, bucket, sign board 2.6 x 1.0, picnic basket, towels | simple meshes or cards |
| Scatter | 150-400 pebble and shell specks 0.03-0.12, denser near the camera; 40-80 dune-grass tufts 0.8-1.2 high, 4 blades each; 12-16 footprints | particle instances or cards |

Count target: 12-18 distinct objects in a wide shot, plus the scatter.

**Materials**

| Surface | Recipe |
|---|---|
| Sand | Noise Texture (object coordinates, scale 0.4 per D, detail 4, roughness 0.6) -> ColorRamp `#d28a50` at 0.35, `#e79a4f` at 0.5, `#f3ad6f` at 0.7. Multiply ripples: Wave Texture (bands, scale 1.5 per D, distortion 3, detail 2) through a ColorRamp 0.9-1.0, factor 0.12. Distance tint: Camera Data > View Distance -> Map Range (20 D to 150 D) -> mix toward `#e78c6d`, then `#f0b98c` at the far end. |
| Sea | Same distance factor: near `#2f55b8`, far `#6f9fe6`, and a thin pale band `#b9d3ee` (about 10 px on screen) at the horizon. Swell streaks: Wave Texture (bands running parallel to the shore, scale 0.5 per D, distortion 4, detail 3, detail scale 2) -> ColorRamp with a narrow step 0.48-0.52 -> mix `#e6eefc` at 0.6. Matte, no reflection. |
| Sky | Vertical gradient zenith `#4b74c2`, `#6197e5` at 60 percent, horizon `#99bee9`. |
| Clouds | White-lavender `#e6e9f8` with lighter tops `#f4f3fb`, flat bottoms, edges blurred over 20 px or more, covering 20-35 percent of the sky, no outline. Either SVG cards (blurred ellipses, as in the prototype) or Noise Texture (scale 1.5, detail 5, roughness 0.55, distortion 0.4, stretched 4:1) -> ColorRamp 0.52-0.62. |
| House siding | SVG: horizontal clapboard lines 1.2 px at 0.21 D pitch in siding colour x 0.68; side wall in shade x 0.7. Bodies cream `#ebddc8`, red `#b84735`, blue-grey `#7f8fbf`. Roofs `#5b211d` or slate `#4d3e3f`; gable end = body x 0.92; doors roof colour x 1.1; panes `#9cc0f0`. |
| Poles, fence, boat | wood `#6d3a1f` and `#5a3526`, fence `#8a5a35`, rope `#d9c9a8`, insulators `#b9d7e4`, hull `#c2311e` with gunwale `#f6efe2`, umbrella `#c2311e` and `#f6efe2` gores |
| Dune grass | strokes in `#67832c`, `#8aa23a`, `#4f6b2a` |
| Sign | cream `#f6efe2`, red slab capitals `#b61d32`, 3 px ink border |

**Light and depth**: one sun from upper left with a soft angle of 1-1.5 degrees so shadow edges stay within 8 px, shadows at 0.36-0.41 of the lit luminance and tinted plum-blue (target shadow on sand about `#605e6e`, computed from the per-channel ratios of A t32.0 and A t34.0; on wood `#494860`, A t34.0). Take the sun and ambient numbers from the `EXTERIOR_NOON` or `LATE_AFTERNOON` preset. Haze: mix far cards and the far ground toward `#a0bfec`, up to 60 percent at the horizon. Foreground: let the nearest 15 percent of the frame fall to about half brightness (a dune or fence in shade), which the prototype still lacks.

**Variants needed by the script** (extrapolated palettes, see 1.9)

| Beat | Sky top -> horizon | Sea | Sand | Notes |
|---|---|---|---|---|
| Sunny last swim | `#4b74c2` -> `#99bee9` | `#6f9fe6` -> `#2f55b8` | `#f3ad6f` | as above |
| Grey drizzle morning | `#a79da6` -> `#dfdfe7` | `#83757a` -> `#a79da6` | `#b9a48f` | no sun and no cast shadows, saturation of all objects halved, thin rain strokes at 15 percent |
| Storm arriving | `#32336c` -> `#7673b5` | `#183ca1`, wave face `#285bc9`, base `#261735` | `#68609f` | ink switches to `#1d1449`; foam `#c7afde` to `#eef2fe`; lit windows `#ffd995`; from B t41.0 and B t44.0 |

The wave: an extruded arc profile across the whole frame, at least 8 D high (house ridge is 6 D), first a pale flat band on the horizon (`#c9bfbd`, the "fog bank"), then darkening to `#183ca1` as it nears; foam crest as a scalloped SVG card; two or three overlapping bands with wavy top edges and speckle for depth, in the manner of the strata in B t62.0.

### 3.6 Procedural node recipes (all node types exist in bpy 5.3: checked without rendering)

- Floor planks without SVG: Brick Texture, `offset = 0.5`, `offset_frequency = 2`, Scale 1, Row Height = plank width (0.28 D in object units), Brick Width = 4-6 D, Mortar Size tuned until the seam is 7 percent of the plank width, Color1 `#8e6045`, Color2 `#99684b`, Mortar `#432219`. Rotate the mapping so rows run toward the back wall. Grain: Wave Texture (bands along the plank, scale 2, distortion 6, detail 2) -> ColorRamp 0.9-1.05, multiply at 0.15.
- Plaster or painted wood variation: Noise Texture scale 1.5 per D, detail 2 -> ColorRamp 0.96-1.04, multiply. Keep it this weak: the reference has flat fills, the pattern is drawn.
- Brick or stone (if needed): Brick Texture with Row Height 0.3 D, Brick Width 0.6 D, mortar colour = stone x 0.68.
- Pebble scatter on a texture: Voronoi Texture (F1, scale 40 per D) Distance -> ColorRamp step at 0.12 -> mix darker speck colour at 0.7.
- Distance tint (haze): Camera Data > View Distance -> Map Range -> factor of a Mix (colour) toward the horizon colour.
- Sky: Texture Coordinate (Generated or Window Y) -> Gradient Texture -> ColorRamp with the three stops. The Sky Texture node in this build offers `SINGLE_SCATTERING`, `MULTIPLE_SCATTERING`, `PREETHAM`, `HOSEK_WILKIE`; do not use it, a plain ramp matches the reference better.

### 3.7 Text-bearing props

- Layout: one or two large lines, everything else greeked (grey bars or illegible micro-text). Frame the sheet with a thin ruled border.
- Sizes: a held sheet is 1.08 x 1.4 D; the headline cap height is about 0.10 of the sheet width and the headline spans 85 percent of it; a calendar month name is twice the cap height of its header (45 px against 23 px in A t36.0).
- Colours: paper `#fff5df`, printed ink `#836d4e` (about half the paper's lightness, never black), red `#b61d32`, navy `#081148`, cream lettering on colour `#edb48c` to `#f3d9a8`.
- Type. Headlines and signs: bold slab or fat-face capitals with 1-2 px letter spacing. Mastheads: mixed-case old-style serif. Teletype output: typewriter face. Installed and usable now: `DejaVu Serif Bold` (slab-like), `Liberation Serif`, `Courier 10 Pitch`. Closer period faces exist on npm and were found reachable (`npm view`, version 5.3.0 each, not installed by me): `@fontsource/abril-fatface`, `@fontsource/alfa-slab-one`, `@fontsource/rye`, `@fontsource/old-standard-tt`, `@fontsource/im-fell-english`, `@fontsource/special-elite`.
- The wall map needs at most two legible labels (the date and one city); the storm track must be the most saturated mark on the wall.

### 3.8 Acceptance checks for a rendered frame

Run `ref/crops/env/tools/metrics.py` style statistics on a frame with characters in it.

| Check | Pass | Reference |
|---|---|---|
| Mean saturation | 0.40-0.50 | A 0.485, B 0.405 |
| Canny edge density | at least 0.05 | A 0.060, B 0.067 |
| Featureless 40 px blocks | at most 0.30 (office at most 0.25) | A 0.30, B 0.27 |
| Office luminance top / middle / bottom | about 65 / 105-130 / 40-70, top darker than middle | B interiors |
| Luminance behind heads | 95-170 | A 120, B 136 |
| Set objects in a wide shot | office 20-26, beach 12-18 | section 2.7 |

---

## 4. Differences vs v1, ranked by visual impact

1. **The set is nearly empty.** v1 shows about 5 set objects (map, desk, two papers, a cabinet sliver) against 11-16 in the A interior and about 26 in the B interiors. Featureless area is 0.63 of the frame against 0.27-0.30; edge density 0.016 against 0.060-0.067.
2. **The brightness structure is upside down.** v1 is brightest at the top (blank cream wall `#e0d6bc`, luminance 213) and bright again at the bottom (160), with the middle at 154. The reference is brightest in the middle (120-125) with the top at 108-119 and the bottom at 79-93; reference interior walls sit at value 0.30-0.50 with saturation 0.4-0.7, v1's wall at value 0.88 with saturation 0.16. The v1 floor also gets lighter toward the camera (`#765a3e` far to `#c59c71` near); the reference floor gets darker.
3. **Surfaces have no drawn pattern.** v1 wall and floor are untextured gradients (texture strength 0.5 and 0.7) against 3-8 on A's planks and 12-23 on B's surfaces. There are no plank seams (reference: 5 px seams at 0.33-0.40 of plank luminance, planks 0.28 D wide), no wallpaper, no panels, no trim.
4. **One hue family instead of four or five.** v1 is beige to brown (saturation 0.29, 64 colour bins) against 0.41-0.49 and about 100 bins. There is no cool block (navy floor), no red or green accent, no gold.
5. **No linework or trim on the environment.** v1's Freestyle set covers the characters only. Clip B inks every set object at about 3 px in dark warm brown and draws detail lines at 1-2 px; clip A uses contrast trim bands and seams instead. v1 has neither, so objects are separated only by soft shading.
6. **No visible emitters.** The reference interior always shows glowing points (four bulbs in A t27.5, candles and torches throughout B) with a tight halo. v1's lamp and window are outside the frame.
7. **Photographic soft shading.** v1 uses Principled materials with specular, a soft area light and bounce light, giving smooth photographic gradients and soft shadows. The reference has either hard plum-tinted sun shadows at 0.36-0.41 (A) or no shadows at all with painted light (B). Neither has specular highlights on walls or floors.
8. **Lens and shell.** v1 uses a 32 mm lens looking flat at one wall: no ceiling, no side wall, no converging floor lines. The reference interior shows ceiling, both side walls and floor in one wide frame (A t27.5), with an estimated 18-20 mm lens, and the floor pattern converging to an eye line at 42-45 percent.
9. **Text props are weak.** The v1 map is pastel (saturation 0.22-0.26, value 0.87) with thin low-contrast serif labels and a plain brown frame, so it merges with the wall. Reference text props use two large bold lines, saturated red or navy accents, a ruled frame and cream paper that is the brightest thing after the heads.
10. **Furniture is undersized for the heads.** The v1 desk top is 0.91 D high; the reference side table is 1.65 D high and its chair back 1.37 D wide. Small furniture makes the heads look even larger and the room emptier.

---

## 5. Files

- This spec: `spec/environment_materials.md`
- Prototype generator and outputs: `spec/env_proto/gen_styleframes.py`, `office_styleframe.svg/.png`, `beach_styleframe.svg/.png`, `tex_floor_planks.svg/.png`, `tex_wall_office.svg/.png`, `proto_overview.jpg`
- Evidence crops: `ref/crops/env/` (contact sheets `sheet_a_*.jpg`, `sheet_b_*.jpg`; zooms `A_interior_detail.jpg`, `A_station_detail.jpg`, `A_edge_zoom6.jpg`, `A_surfaces.jpg`, `A_text_props.jpg`, `B_outline_detail1.jpg`, `B_outline_detail2.jpg`, `B_outline_zoom6.jpg`, `B_surfaces.jpg`, `B_contact_shadows.jpg`, `B_shadow_check.jpg`, `B_3d_inserts.jpg`; gridded frames `grid_*.jpg`)
- Measurement scripts: `ref/crops/env/tools/*.py`
- Extra 30 fps frames: `ref/extra/env/`
