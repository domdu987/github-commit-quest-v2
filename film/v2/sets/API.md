# v2/sets/office.py : illustrated 1938 U.S. Weather Bureau office (pure 2D SVG)

Python 3 stdlib only (numpy / cv2 / Pillow are used only by `measure()` and `frames()`).
Rasterise with headless Chromium (Playwright); `raster.js` next to this file is the reference rasteriser.
Fonts: system `DejaVu Serif` Bold (all lettering) with fallbacks Caladea / Liberation Serif. Nothing is fetched or embedded.
Reviewed and repaired on 2026-11-11: see `REVIEW.md` (findings, numbers, what changed), `review.py` (re-runnable checks), `review_compare.jpg`, `review_anchors.png`, `review_states.jpg`. The API below is unchanged from the first build except where marked **(review)**.

## World convention (unchanged)
- Unit = D (head diameter). x right, y DOWN. Actors' floor contact line y = 0, heads near y = -2.5.
- x = 0 is the horizontal centre of the wall map. Eye line / vanishing point of the painted perspective: (0, -2.5).
- Camera = (cx, cy, zoom) with zoom = screen px per D, frame 720x1280.
- Every fragment is already in D units (internally drawn at 100 units per D inside `<g transform="scale(0.01)">`).
- All ids (gradients, patterns, clip paths) are prefixed with `uid`.

## build(state=None, uid='of') -> dict
```
{ 'layers': [ {'name','svg','parallax','depends'[, 'blend']} ... ],   # back to front
  'defs':   '<defs>...</defs>',      # put once in the document (it may also be nested in your own <defs>)
  'world':  (-4.6, -8.2, 4.6, 4.8),  # x0, y0, x1, y1 in D: the painted extent
  'anchors': {...} }
```
Layers, in order:

| name | parallax | blend | content | depends on |
|---|---|---|---|---|
| `bg` | 1.0 | normal | ceiling, beams, fan, side walls, back wall (paper, frieze, rails, wainscot), window, calendar, barometer, thermometer, sign, clock, pin board, wall map + ledge, plank floor + navy rug, painted light and fall-off, 3 pendant lamps | line, erase, t |
| `mid` | 1.0 | normal | radiator, teletype on its stand, waste basket, chart basket, coat stand with coat and fedora, filing cabinets (steel-violet **(review)**), barograph, box file | - |
| (actors) | 1.0 | | the compositor inserts the puppets here | |
| `fg` | 1.12 | normal | desk corner (lower left) with banker's lamp + glow, telephone, papers, ink bottle, red pencil; chair back (lower right) | - |
| `light` | 1.0 | `screen` | lamp halos, window light shaft, dust specks | t |

Notes
- `bg` deliberately has parallax 1.0 (not the suggested 0.92): the hero's hand must stay registered on `map_ny`, and his feet on the floor. Depth comes from the `fg` layer.
- Parallax formula used by `layer_transform(cam, parallax, W, H, pivot)`:
  `translate(W/2 H/2) scale(zoom) translate(-(px + (cx - px) * p), -(py + (cy - py) * p))` with pivot `(px, py) = anchors['parallax_pivot'] = (0, -1.70)` (centre of `cam_wide`). With p = 1 it is the plain camera transform. The fg art extends far below and beside the world box, so any other parallax formula is safe too.
- `light` is drawn with alpha on transparent, so it also works with plain alpha-over; `screen` (or additive) is what was reviewed.
- `bg` uses `mix-blend-mode` (screen / multiply) internally; it is opaque, so it can be pre-rasterised on its own. `mid` and `fg` use no blend modes.
- Cost: `build()` about 8-14 ms; a 720x1280 frame rasterises in 300-420 ms (SVG about 262 kB). No blur filters anywhere. **(review)**
- **(review)** Painted shading: while `build()` runs, every inked shape (stroke = set ink, width at least 0.013 D) automatically gets a second, fill-only copy with a soft gradient (`<uid>sv`: warm light from above, plum shade below). Wainscot panels, cabinet drawers, the sign, dials, coat, baskets and lamp shades get a stronger or a round-form overlay (`<uid>svs`, `<uid>scyl`, `<uid>srad`), the map sheet a light pool, old-paper corners and a frame shade, the floor and rug soft light and dark patches. All are plain gradients (no filters). Primitives take `shade=False` to opt out; `tone(shape, gradient_id)` lays any gradient over a primitive's shape.
- **(review)** For a close-up with a soft background (reference: Gaussian sigma about 4-5 px behind heads of 300 px and more), blur the `bg` and `mid` groups in the compositor; the set itself stays sharp.

### state (all keys optional)
| key | range | effect |
|---|---|---|
| `line` | 0..1 | how much of the red forecast track is drawn, from the storm symbol off Florida to New York. From 0.97 to 1.0 the arrow head grows at the New York end. |
| `erase` | 0..1 | fraction of the drawn track rubbed out, starting at the New York end. Leaves a pink smudge with rubbing strokes on the map and eraser crumbs on the ledge. `erase = 1` removes the whole red line; the printed storm symbol stays. **(review)** The arrow head is rubbed out first and continuously (erase 0..0.06; it used to vanish in one frame), a pink ghost of it stays; rubbing strokes are fixed on the paper and fade in as the eraser passes; crumbs appear one at a time. Largest change between two states 0.0025 (line) or 0.005 (erase) apart: 2.4 percent of the line's red pixels. |
| `t` | seconds | ambient life only: clock second hand (ticks once per second) and pendulum, slow ceiling fan, dust drift in the light shaft. About 0.5 percent of pixels change. |

### anchors (set world, D)
| key | value | meaning |
|---|---|---|
| `floor_y` | 0.0 | actors' contact line |
| `wall_base_y` | -0.40 | back wall meets the floor |
| `eye_line_y` | -2.5 | vanishing point height |
| `map_rect` | (-1.60, -3.68, 1.60, -1.32) | outer frame of the wall map (x0, y0, x1, y1) |
| `map_paper_rect` | (-1.50, -3.58, 1.50, -1.42) | paper inside the frame (title strip above y = -3.30) |
| `map_track` | 85 points | the red track polyline, storm -> New York, length 1.076 D |
| `map_storm` | (0.2349, -1.6183) | start of the track (storm symbol) |
| `map_ny` | (0.0623, -2.6197) | New York end of the track |
| `pencil_tip` | point | point on the track at fraction `line` (where the pencil is now) |
| `line_end` | point | end of the still-visible red line = fraction `line * (1 - erase)` (where the eraser is now) |
| `hero_mark` | -0.55 | x where the hero stands (left of the track). Shoulder (-0.31 slim / -0.205 regular, -2.0) to `map_ny` = 0.72 / 0.68 D, inside a 0.74 D arm. `map_ny` is 0.62 D from his head centre, so the head never covers it. **(review)** Checked with the real `puppet.py` hero (feet on y = 0 puts his head centre at y = -2.47): `arm_r` with a hand target at `map_ny` reaches it. |
| `boss_mark` | 1.30 | x where the chief stands (head 0.80..1.80, clear of the track). **(review)** The real boss puppet is taller: feet on y = 0 puts his head centre at y = -2.87, head top -3.38, hat top about -3.61, so the hat just reaches the bottom edge of the date slip (y -3.615) and his head straddles the right edge of the map frame (x 1.5..1.6). |
| `hero_shoulder_y` | -2.0 | shoulder height assumed above |
| `lamps` | [(-1.7, -4.72), (1.7, -4.72), (0.0, -6.30)] | pendant bulb centres (radii in `lamp_radius`: 0.20, 0.20, 0.27) |
| `banker_lamp` | (-2.12, 0.053) | glow slit of the fg desk lamp (fg layer coordinates) |
| `desk_top` | {y_back 0.628, y_front 1.18, x_right_front -1.32, x_right_back -1.122, layer 'fg'} | top surface of the fg desk (extends left out of frame) |
| `ledge_y`, `ledge_x` | -1.325, (-1.69, 1.69) | top of the pencil ledge under the map |
| `eraser_on_ledge`, `red_pencil_on_ledge` | (0.805, -1.35), (-0.69, -1.34) | props the actors can pick up |
| `window_rect`, `sign_rect`, `clock`, `calendar_rect` | see code | for eyelines |
| `parallax_pivot`, `world` | (0, -1.70), world box | |
| `cam_wide` | (0.0, -1.70, 110) | frame x -3.27..3.27, y -7.52..4.12; eye line at 43 percent |
| `cam_two_shot` | (0.33, -2.16, 150) | frame x -2.07..2.73, y -6.43..2.11; heads at 46 percent |
| `cam_medium_hero` | (-0.20, -2.18, 200) | frame x -2.0..1.6, y -5.38..1.02 |
| `cam_push_in` | (-0.12, -2.38, 250) | end of a push-in on the hero and the track |

Helpers: `track_point(u) -> (x, y, heading_deg)`, `track_slice(u0, u1) -> points`.

## build_insert_map(state=None, uid='ofi') -> dict
Dedicated full-frame close-up drawing of the map wall: same structure as `build()` (layers `bg`, `mid`, `light`; no `fg`), same state keys, and **the same world coordinates** as the main set, so hands and props can reuse positions.
Differences: every line is 0.69 x thinner (3 px object / 1.5 px detail lines at zoom 218), the map is redrawn with extra detail (2.5 degree graticule, more stations, greeked labels, pressure numerals, legend box, compass, scale bar, water lining).
Anchors: `map_track`, `map_ny`, `map_storm`, `pencil_tip`, `line_end`, `map_rect`, `map_paper_rect`, `ledge_y`, `ledge_x`, `eraser_on_ledge`, `red_pencil_on_ledge`, `world`, and
- `cam` = `cam_insert` = (0.0, -2.16, 218): the map fills 97 percent of the width; frame y -5.10..0.78. Map occupies y px 309..823, so the track and the ledge crumbs stay above the caption band (850..960); sign and two half-seen pendants above, wainscot, waste basket and a strip of rug below.
- `cam_insert_tight` = (0.12, -2.42, 300): optional push-in end centred on the track.

## compose(built, cam, actors='', W=720, H=1280, extra_defs='') -> str
Reference compositor: returns a complete SVG document. `actors` is an SVG fragment in set world D units; it is inserted just before `fg` (or before `light` when there is no `fg`). `dummy_actors()` gives two stand-in puppets for staging checks.

## Line weights and style numbers
- Object silhouettes 0.020 D = 3.0 px at zoom 150 (2.2 px wide, 4 px medium, 5 px push-in); ink `#2a1712`. **(review)** The largest props (map frame, sign, clock, cabinets, coat) carry 1.2-1.3 x that. Detail lines 0.010 D = 1.5 px at zoom 150 in surface colour x 0.5-0.74. Lines scale with the camera.
- Red track 0.038 D (5.7 px at zoom 150; was 0.032) **(review)**, `#c8301c`: the most saturated mark on the wall.
- Text props: paper `#fff5df`, printed ink `#836d4e` / `#574430`. Legible: U.S. WEATHER BUREAU, DAILY WEATHER MAP, SEPT 20 1938, SEPTEMBER 20, N.Y., BOSTON, FLA., H. Everything else is greeked.
- **(review)** Palette (the resolved palette of `spec/LOOK_SPEC.md` 3.2 and 8.1 row 10): wallpaper rose `#9c3139` with a tan-gold sprig `#d59a58` (was orange-brown `#ad6039`, one hue family with wainscot, floor and map), frieze `#7a3037`, wainscot `#5f2a1a` / panels `#7a3a21`, planks mauve-brown `#99695c`, ceiling `#64323c`, rug navy `#233a68` with border `#84222a` and gold `#cb9f48`, filing cabinets steel-violet `#51578f` / `#5f66a3` (were green; green is now only the lamp shades and the sign, 2 percent of the frame), map land old gold `#c49b58`, sea teal `#6b9aad` with water lining and slate isobars (were `#c9ab78` / `#82abb8`), fall-off tint plum `#260a38`.
- Lamp halo (light layer): the glow falls to 10 percent 14-18 px beyond the bulb in the wide, 18-24 px in the two-shot, 24 px in the medium (target 12-24). **(review)**
- No hard cast shadows; only faint contact smudges under mid furniture.

## CLI
`python3 review.py all | anchors | states | contract | halos` re-runs the review checks (needs numpy, cv2, Pillow; reads `v2/puppet/puppet.py` for the real cast if it is there).
`python3 office.py frames` writes into this folder: `office_wide.png`, `office_two_shot.png`, `office_medium.png`, `office_insert.png` (line 1, erase 0), `office_states.png` (line 0, 0.5, 1, then erase 0.5, 1), `compare.jpg` (ref b/t07.0 | our two-shot | ref b/t18.5), `office_staged_two_shot.png`, `office_staged_medium.png` (with stand-in puppets), `metrics.json`. Scratch SVGs go to `v2/tmp/`.

## Measured after the review (set only, no actors; `python3 review.py all`)
| frame | saturation | Canny edge | featureless 40 px blocks | luminance top / middle / bottom | ring behind heads (hero, boss; real puppet head heights) |
|---|---|---|---|---|---|
| wide | 0.485 | 0.122 | 0.057 | 58 / 105 / 44 | 148, 125 |
| two-shot | 0.459 | 0.110 | 0.031 | 68 / 116 / 68 | 148, 125 |
| medium | 0.436 | 0.104 | 0.021 | 89 / 131 / 95 | 148, 145 |
| insert | 0.437 | 0.104 | 0.017 | 98 / 133 / 87 | - |
| acceptance | 0.40-0.50 | at least 0.085 (two-shot) | at most 0.25 | about 65 / 105-130 / 40-70 (wide and two-shot) | 95-170 |
| reference b/t07.0, t18.5, t23.0 (same code) | 0.47, 0.32, 0.37 | 0.114, 0.110, 0.089 | 0.09, 0.10, 0.21 | 66 / 114 / 70, 66 / 131 / 43, 63 / 132 / 52 | 104-170 |

"middle" = the two central rows of an 8-row grid, which reproduces the spec's reference numbers. Full tables (colour statistics, palette, halo, texture, contract checks): `REVIEW.md`.
