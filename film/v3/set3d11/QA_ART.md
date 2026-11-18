# QA-art, SET gate, film 11 (set3d11 / dairy.py), 2026-11-18

Reviewer: QA-art (opus), read-only. Looked at all 11 tiles in `dairy_work/final/` at full size (720x1280) and at phone size (360x640 Lanczos),
next to `board/still_A.png` (approved main look), `still_B.png`, `still_C.png`, `film/ref/a`, `film/ref/b` and `film/analysis/sheets/*.jpg`.
The placeholder cards (girl in red, etc.) are ignored. Only the set is judged.

## Verdict: FIX-FIRST

The 4 exteriors are close to board B and nearly ready. Five of the seven interiors (barn_milking, barn_high, barn_door and all three rooms)
have lost the approved golden-morning look. They read as a lavender wash with the warm light in small patches. The cause is in the light
parameters (section 2), not the geometry, so most of it can be fixed with parameters only. The three room presets also look almost the same,
and the bed does not read as a bed.

Your first impression, checked:
- Interiors far bluer and murkier than board A: **confirmed**, and measured (table 1). Board A warm/cool ratio is 2.26. barn_milking is 0.21,
  barn_high 0.35 (still_C itself is 0.91), barn_door 0.69, and the rooms 0.07-0.08. Only barn_wide (1.68) is near A.
- The three rooms look almost identical: **confirmed**. They use the same camera, the same lavender grade and the same props. The mean absolute
  pixel difference between them is 15-22 (out of 255). barn_wide vs barn_milking, for comparison, is 45. room_morning has no visible sun on the
  floor (floor p95 luminance 0.47, below room_day's 0.64).
- Hero cow in barn_milking reads as a pale blob: **confirmed**. The cow (3D marker at the blossom point) stands in shade, so its white coat goes
  pale lavender and its outline is lost against the lavender hay heaps behind it. The sun pool lands about 3 D to the left, on the floor by the door.
- barn_high cluttered and dim: **confirmed, with a cause.** The bottom 40 % is a dark blue mass of silhouetted near-camera props. A long rod or
  pole crosses the lower frame diagonally. The sun-beam wedge renders as a hard-edged translucent "glass box" (a bright parallelogram from the
  ladder to the right edge, with a hard bottom edge at about y 860). That box is the worst artefact in the set.
- No visible bed in the rooms: **partly true**. A bed exists (patchwork quilt at the left, about y 560-650), but it is cut by the left frame
  edge and has no visible pillow or headboard. In flat lavender shade, at phone size, it reads as a low table or counter. In room_day and
  room_night the boy card seems to stand on a bench.

## 1. Measurements (my script, whole frame; L = Rec.709 luminance 0-1)

warm = chromatic pixels with hue < 70 or >= 345 deg; cool = hue 180-290. W/C = luminance-weighted warm/cool ratio.
litW = share of warm hue among the brightest 25 % of chromatic pixels (do the lit areas read warm?). R/B = mean red / mean blue.

| tile | meanL | top | mid | low (880+) | sat | warm % | cool % | **W/C** | **litW %** | R/B |
|---|---|---|---|---|---|---|---|---|---|---|
| board still_A (target) | 0.34 | 0.26 | 0.42 | 0.33 | 0.39 | 46 | 36 | **2.26** | **97.6** | 1.23 |
| board still_C (target C) | 0.30 | 0.19 | 0.45 | 0.24 | 0.47 | 23 | 66 | **0.91** | **85.1** | 0.89 |
| barn_wide | 0.39 | 0.26 | 0.44 | 0.48 | 0.38 | 40 | 52 | 1.68 | 94.7 | 1.13 |
| barn_milking | 0.30 | 0.23 | 0.38 | 0.27 | 0.41 | 9 | 86 | **0.21** | **30.5** | 0.73 |
| barn_high (C) | 0.31 | 0.30 | 0.40 | 0.22 | 0.48 | 12 | 73 | **0.35** | **35.2** | 0.77 |
| barn_door | 0.32 | 0.20 | 0.47 | 0.26 | 0.39 | 22 | 73 | **0.69** | 83.6 | 0.86 |
| garden_hut | 0.56 | 0.74 | 0.49 | 0.45 | 0.37 | 36 | 39 | 1.16 | 51.6 | 1.07 |
| lane_wide | 0.60 | 0.73 | 0.51 | 0.56 | 0.32 | 50 | 29 | 1.96 | 64.2 | 1.13 |
| lane_high | 0.58 | 0.73 | 0.51 | 0.50 | 0.34 | 40 | 11 | 8.19 | 99.5 | 1.31 |
| garden_queue | 0.63 | 0.76 | 0.57 | 0.56 | 0.33 | 54 | 25 | 2.48 | 99.9 | 1.23 |
| room_day | 0.33 | 0.28 | 0.38 | 0.33 | 0.43 | 3.5 | 89 | **0.07** | **10.5** | 0.67 |
| room_night (C) | 0.27 | 0.24 | 0.32 | 0.25 | 0.51 | 3.1 | 89 | **0.08** | **8.8** | 0.62 |
| room_morning | 0.33 | 0.28 | 0.39 | 0.32 | 0.43 | 4.0 | 90 | **0.07** | **9.6** | 0.67 |
| ref a t0005 (palace interior) | 0.41 | | | 0.55 | 0.32 | 63 | 2 | 43 | 99.9 | 1.35 |
| ref a t0027 (night exterior) | 0.25 | | | 0.15 | 0.35 | 23 | 63 | 0.62 | 74.4 | 0.98 |

The reference interiors (palace hall, pachinko hall, prize counter, railcar) are warm and high-key, with red/gold dominant and practicals glowing.
Even their night shots keep W/C around 0.6 and litW above 70 %. Our rooms are at 0.07 and 10 %: in every room, the lit parts are blue.

## 2. Root cause (in `dairy.py`, compared with the approved board `dairy_board.py`)

| param | board MORNING (approved A) | finals A | board AFTERNOON (approved C) | finals C / barn_high |
|---|---|---|---|---|
| key | (1.95, 1.50, 0.88) | same | **(2.25, 1.28, 0.50)** | (1.65, 0.92, 0.36), **-27 %** and redder |
| bounce (r, g, b, strength) | (1.0, 0.66, 0.36, **0.20**) | (1.0, 0.72, 0.40, **0.07**) | (1.0, 0.55, 0.30, **0.10**) | **0.05** |
| shade_mix | **0.62** | 0.82 (barn), 0.82 (rooms) | 0.80 | 0.85 |
| shade (barn presets) | (0.102, 0.136, 0.34) | (0.146, 0.153, **0.47**) | (0.070, 0.105, 0.36) | (0.105, 0.108, **0.49**) |
| shade (rooms) | | (0.18, 0.195, **0.59**) x1.6 | | (0.13, 0.135, **0.52**) |

The builder cut the warm bounce to a third, raised shade_mix (so the painted violet now replaces the timber's own brown) and raised the blue of
the shade by 40-75 %. The result is a brighter but violet interior: the timber and roof that glow orange on board A are now grey-lavender.
Board A met the rules (hue 240.4, magenta 6.9 %) with the old values, so the old values are safe to go back to.

## 3. Scores (1-10)

| # | preset | density / ornament | lighting & colour | composition / phone | match board + refs | **mean** |
|---|---|---|---|---|---|---|
| 1 | barn_wide | 8 | 7 | 6 | 7 | **7.0** |
| 2 | barn_milking | 6 | 3 | 5 | 3 | **4.3** |
| 3 | barn_high | 6 | 3 | 3 | 3 | **3.8** |
| 4 | barn_door | 5 | 4 | 6 | 4 | **4.8** |
| 5 | garden_hut | 8 | 8 | 7 | 8 | **7.8** |
| 6 | lane_wide | 6 | 8 | 6 | 7 | **6.8** |
| 7 | lane_high | 9 | 8 | 8 | 8 | **8.3** |
| 8 | garden_queue | 8 | 8 | 7 | 8 | **7.8** |
| 9 | room_day | 6 | 3 | 4 | 3 | **4.0** |
| 10 | room_night | 6 | 3 | 4 | 3 | **4.0** |
| 11 | room_morning | 6 | 2 | 4 | 2 | **3.5** |

Per tile, briefly:
- **barn_wide**: Dense, warm sun pool, lanterns glow, and the lower third is full. Weak points: the top 30 % is a dark plank ceiling; a dark post
  splits the frame at x about 380; the stalled cows on the right are a brown mass without a readable head; the near hens and stools are big at
  22 mm (the white hen at lower left is about 130 px). The loft hay reads as clouds.
- **barn_milking**: The hero cow is a pale lavender silhouette with no light on it. The sun is on the floor by the door, not on the nook. The
  lower 40 % is a flat lavender floor with dark hen silhouettes. The ceiling fills the top 35 %. Its hanging onions read as purple beads.
- **barn_high**: Glass-box beam artefact. Dark lower 40 % with silhouetted crates, stools and sacks plus a diagonal pole. The amber pool is
  small and does not rake across the floor as on still_C. The door is not legible as a door, so the "crowd in the doorway vs milkmaids in the
  sun" contrast does not read.
- **barn_door**: Good idea and good motes. But the exterior is washed out (pale haze, low contrast) where board A's exterior glows gold. The
  interior floor in the lower third is a bare lavender plane with 3 pails. The ceiling is a flat dark plank field over the top 35 %.
- **garden_hut**: Closest to board B: good thatch, hut, flowers, sky. The near-camera "lollipop" flowers (flat yellow/orange discs about
  100-150 px at y 900-1150) look toy-like. The bed of plain brown soil at the lower right is bare. The hut interior is flat teal.
- **lane_wide**: Lovely church tower and lane perspective. But the lower 40 % is an almost empty dirt lane (a few pebbles): this breaks the
  brief's "lower third must not be empty". The cloud is clipped at the top edge. The right cottage wall is a large flat violet plane.
- **lane_high**: Best tile: dense, warm, readable crowd stage, cottages, hut, hills. Minor: the sheep are white lollipop blobs and the smoke
  columns are chunky.
- **garden_queue**: Good warm light and cottage. The picket fence fills the lower-mid 25 % and hides the queue's bodies. A reddish deer/dog shape
  at mid-right reads as a toy. The fringe of the hut thatch at the left edge is cut.
- **rooms (all three)**: The same camera, props and grade, with the same lavender wash. The hearth fire at the right edge is the only warm thing.
  Hanging hams and onions read as floating pale-violet balloons (very visible at phone size). No candle is visible in room_night (it is hidden
  behind the chair/card, or too small). room_morning has no visible morning sun. The bed is at the left frame edge and reads as a counter.

## 4. Fixes, ordered by impact (apply in this order, re-render, re-measure with the table-1 script)

Measurement script: `/tmp/claude-0/-home-user-github-commit-quest-v2/638adbb0-ae0c-585b-9c21-d694df47b93f/scratchpad/qa/m.py`
(copy it into `dairy_work/` if the scratchpad is gone). The client rules still apply after every change: shade hue 240-260 and
magenta <= 10 % (`python3 dairy_hue.py`).

### F1. Restore the approved board light values (all barn presets, A and C), dairy.py LIGHTS + PRESETS[p]['P']  [biggest single win]
- `LIGHTS['A']`: `bounce=(1.0, 0.70, 0.36, 0.18)`, `shade_mix=0.64`, `shade=(0.102, 0.136, 0.34)`, `shade_tint=(0.087, 0.118, 0.37)`.
- barn_wide / barn_milking / barn_door `P`: delete the `shade`/`shade_tint`/`lift` overrides (or set them to the board values above).
- `LIGHTS['C']` and barn_high `P`: `key=(2.25, 1.28, 0.50)`, `bounce=(1.0, 0.55, 0.30, 0.10)`, `shade_mix=0.80`, `shade=(0.070, 0.105, 0.36)`,
  `shade_tint=(0.06, 0.10, 0.41)`, `lift=(0.002, 0.008, 0.026)`.
- If magenta goes above 9 % on a ceiling, first shift the bounce colour toward yellow (G from 0.70 to 0.78, B 0.36 to 0.30), and only then lower
  the strength (never below 0.14). If the shade hue falls below 240, raise `lift` B by +0.01 at a time.
- **Targets**: barn_wide and barn_door W/C >= 2.0, litW >= 95 %, R/B >= 1.15. barn_high (C) W/C 0.8-1.2, litW >= 85 %. Roof timbers in
  barn_wide must read brown-orange: mean hue of region y 0-300 in 15-40 deg for >= 50 % of chromatic pixels.

### F2. Rooms: build three real looks with warm practicals (room_day / room_night / room_morning)
Common to all three:
- `P`: drop the `shade` x1.6 overrides and use `shade=(0.12, 0.13, 0.36)`, `shade_tint=(0.11, 0.115, 0.39)`, `shade_mix=0.66`,
  bounce strength 0.18.
- Add a **warm window fill**: a no-shadow AREA light in each window opening (left window 5 x 2.9 D, back window 3.4 x 2.7 D), colour
  (1.0, 0.80, 0.55), facing into the room. Strength: tune until the targets below are met.
- Re-texture the hanging hams and onions in warm brown/ochre (`gain` 1.2), or remove the two near-camera ones (the pale balloon at about
  x 500, y 220-360 and the one at x 320, y 380).

Per preset (they must differ):
- **room_day** (neutral-warm daylight, high key): sun az 140, el 38 through the back window so a sharp sun rectangle lands on the rag rug and the
  table. Targets: meanL 0.42-0.48, floor (y 700-1100) p95 >= 0.75, W/C >= 1.5, litW >= 90 %.
- **room_morning** (low golden sun raking): sun az 190, el 12 through the LEFT window, so long golden shafts cross the bed and the floor to the
  right. Key (2.0, 1.45, 0.75). Motes on. Window fill 1.3x room_day's. Targets: meanL 0.40-0.46, a continuous lit band >= 35 % of the floor
  area y 700-1100 with L >= 0.6, the bed quilt region L >= 0.55, W/C >= 2.0. Must differ from room_day by a mean abs pixel diff >= 35.
- **room_night** (C, candle drama): exposure -0.5 EV versus room_day. Windows deep blue (no fill light), so the shade carries the blue.
  **Candle**: move the candlestick to the near table corner so it is visible on frame, at about x 520-600, y 600-700. Point light colour
  (1.0, 0.55, 0.22), radius 0.15, strength so that a warm pool r >= 180 px on the table, quilt and floor reaches L >= 0.5. Hearth light x2.
  Targets: meanL 0.22-0.28, W/C 0.6-1.0 (as on ref a t0027), litW >= 80 %, shade hue 245-258. Mean abs diff vs room_day >= 40.

### F3. Make the bed read (all rooms)
- Camera: room presets `look_at` from (-1.0, 5.0, 1.3) to (-2.6, 5.6, 1.4) (the camera pans about 12 deg left). The bed then sits in the
  left-middle third and is not cut by the frame edge. Re-check that the right-wall door is still in frame for room_night: if not, give
  room_night its own camera (2.4, -2.8, 2.8) -> (-1.5, 5.2, 1.4).
- Geometry: add a tall carved headboard at y 8.8 (top z 3.6) and a footboard at y 2.4 (top z 2.6). Add a fat white pillow (1.6 x 0.9 x 0.45 D)
  at the head. Make the quilt drape over the side to z 0.6, with a valance. Remove anything that occludes the bed from the camera.
- Target: at 360x640 the bed is recognisable (headboard + pillow + quilt) and occupies >= 8 % of the frame area.

### F4. barn_milking: put the hero nook in the light
- Either move the nook into the existing pool: stool (-5.6, 12.6), pail (-4.6, 13.4), `blossom` stand (-5.4, 15.0), `sarah` (-5.6, 12.6, 0.85).
- Or keep the positions and change the sun to az 200, el 18 (so the door pool reaches x about -2). Check visually that the pool covers the
  cow flank.
- Also add a warm no-shadow AREA "door spill" (4 x 5 D at x -9.8, y 12..17, colour (1.0, 0.78, 0.48)) aimed at the nook.
- The cow (marker and later the 2D puppet) needs a darker backdrop: the lavender hay heaps directly behind it at y 350-500 should go
  darker/warmer (shade them, or move them 2 D to the right) so the white coat has contrast.
- Targets: cow flank region mean L >= 0.6 with R/B >= 1.15. Local contrast cow vs background (|dL| at the cow outline) >= 0.2. Tile W/C >= 1.5,
  litW >= 90 %. Hanging onions recoloured warm (now purple beads).

### F5. barn_high: kill the glass box, clear the foreground, rake the amber
- Sun-beam wedges: for barn_high set `beams=0` or feather the wedge edges (alpha ramp over the last 30 % of each edge, max alpha <= 0.06).
  Target: no straight luminance step > 0.08 along any line inside the frame that is not a geometry edge (check y 840-880, x 300-720).
- Remove the diagonal pole and the three silhouetted near-camera props at y > 1050 (move `fg_props` for this preset >= 2.5 D farther from
  the camera, or into the sun).
- Sun az 195, el 11, so the amber band runs from the door across the floor through both milkmaids toward the camera (as on still_C).
- Camera: pitch down so the roof is <= 15 % of the frame: `look_at` (-5.4, 13.6, 0.6) to (-5.6, 12.8, -0.2).
- Make the door legible: a brighter sunlit lane outside (exterior seen through the door L >= 0.7), with the pockmarked villagers silhouetted
  against it.
- Targets: lower third (y 880-1280) meanL >= 0.30 (now 0.22). Amber lit floor >= 25 % of the y 600-1100 area. W/C 0.8-1.2. Magenta <= 9 %.

### F6. barn_door: golden exterior, lit floor, less ceiling
- Sun az 195, el 18 so a long golden pool runs from the door toward the camera along the floor, with Sarah backlit (rim).
- Reduce the haze on the exterior: `air` opacity 0.30 to 0.15 for this preset. The exterior through the door must keep sat >= 0.40.
- Camera `look_at` z 2.6 to 1.8: the ceiling goes from about 35 % to <= 25 % of the frame.
- Add straw strands, a hen and a basket in the lit pool in the lower third.
- Targets: lower third meanL >= 0.40 with litW >= 90 %. Tile W/C >= 1.8.

### F7. barn_wide polish
- Move the near hens and stools 1.5 D farther from the camera (the white hen at lower left: <= 90 px wide).
- Move the centre post (x about 380 on frame) out of the frame's centre third, or swap it for a thinner one.
- Turn the nearest stall cow's head toward the aisle so one cow reads as brown-and-white with a face.
- Lanterns are good; add 1-2 hanging harness/tack items on the ceiling planks to break the top 30 %.
- Target: top 30 % meanL >= 0.30 with warm hue (follows from F1).

### F8. Exterior polish (small)
- lane_wide: dress the lane in the lower 40 %: wheel ruts with puddles catching the sky, straw, a hen family, a handcart, a basket of
  cabbages at the right verge. Target: no 200x200 px block in y 880-1280 with luminance std < 0.04. Move the sky dome or tilt the camera so the
  cloud is not clipped at the top.
- garden_hut: replace the near "lollipop" flowers with fine flower clusters (<= 60 px heads at 720 width), add tufts in the brown bed,
  and give the hut doorway a warm interior (a lit lantern or a warm fill).
- garden_queue: lower the fence 0.4 D or raise the camera 0.8 D so the queue's torsos read above it; remove the reddish deer/dog toy at mid-right
  or swap it for a hen group.
- lane_high: optional, softer sheep (wool lumps + head) and thinner smoke billows.

## 5. Expected after fixes
If F1-F7 hit their targets, all interiors should reach >= 8 on lighting and match, because the approved A/C values are known-good. The rooms then
need F2 + F3 to score >= 8 on composition and to be told apart. Re-run this review on the new `contact.jpg` and the phone sheet before the client
sees the set.
