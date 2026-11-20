# QA-art — film 22 style board (set3d22), board_1..3

Reviewer: QA-art (opus), look approval delegated by the client. Date 2026-11-20.
Inputs: board_1.png, board_2.png, board_3.png at 720x1280 and resized to 360x640 (phone), style_board.jpg, NOTES.md, stats.json.
Compared with: ref_shorts R3, R5, R2 and R4 sheets, plus 6 frames of film 2 (sky_poker_v3.mp4 at 3/12/22/32/45/55 s).
Rules: QA_TEAM.md QA-art, §G, §H, §I; film22/WORLD.md.

## Verdict: **FIX-FIRST**

The palette and numbers are in range: sat 0.72 / 0.54 / 0.57, vivid 82 / 55 / 51 %. Signs mostly read. The crowd rim (orange outline) works.
Three things block approval:
1. The still-1 skyline is a modern downtown of tall glass-box towers. It is not 1930s London.
2. Still 3 does not read as a deep dark-blue tunnel. It reads as a bright lilac and white tiled tube with an orange glow at the end.
3. Still 2 is framed from too low with a 22 mm lens. The ceiling takes the top 38 % of the frame, the floor takes the bottom 30 %, and the story props (old map, cork board, Beck) are pushed to the edges.

Against R3, R4 and R5 the board is busier in colour but weaker in readable storytelling, and the layers are less clear.

## Scores (1-10)

| still | set density / ornament | lighting & colour | composition / framing | period correctness | match to refs |
|---|---|---|---|---|---|
| 1 london_dusk | 7 | 7 | 6 | **3** | 5 |
| 2 beck_lodgings_night | 5 | 6 | **4** | 7 | 5 |
| 3 platform_tunnel | 6 | **5** | 5 | 6 | 5 |

"Rich and detailed?" (§H.3): still 1 yes, with reservations. Stills 2 and 3: **no**, because of the empty floor and ceiling areas.

## Still 1: london_dusk

What works:
- The high, wide view reads as a city.
- Warm windows against blue shade.
- The red lodging house in the left foreground gives a frame.
- The UNDERGROUND roundel and PUBLICITY DEPT both read at 360x640.
- The river glitter, the lamp halos and the hatted crowd.

What fails:
- **Skyline (top 30 % of frame).** Tall flat slabs in saturated royal blue with regular grids of lit windows and pyramid caps. They read as a 2020s CBD or Manhattan.
  - 1930s London was low: 4-6 storey brick and Portland stone, pitched slate roofs, chimney stacks with pots, smoke, church spires, St Paul's dome, Big Ben.
  - The midground blocks have the same problem: identical boxes with flat lilac tops and grid windows, no roofs and no chimneys. This is the single worst period error on the board.
- **Sky.** Only the magenta-to-orange part of the gradient is visible. The deep-blue zenith never shows because the camera pitches down about 40 degrees.
  - Magenta covers 23 % of the top 20 % of rows. The top of frame reads purple-pink, not deep night blue.
  - The orange band is very tall, because the towers' bases sit in it.
- **Empty floor.** The bottom-right quarter is a flat purple pavement or road with three lamps and a handful of cards, around x 450-720, y 1000-1280. It is the emptiest zone in the frame.
- **Bus.** The bus is a dark box with a lit window strip. It does not read as a red double-decker.
- **Small signs.** ROOMS is rotated vertically and illegible on a phone. The NEWS kiosk sign is about 6 px tall at phone size.
- The clock tower is a generic spire with a white disc. It is acceptable but bland.

## Still 2: beck_lodgings_night

What works:
- Amber against blue.
- The green banker's lamp.
- NOTICE reads.
- The diagram reads as red/blue/green/yellow at 0/45/90 degrees with rings.
- Ink bottles in the line colours.
- The night window with the HQ behind it.
- The wallpaper pattern.

What fails:
- **Ceiling dominance.** The bare ceiling plane and beams fill y 0-480 (top 38 %). Top-third luma is 114 and middle-third luma is 134, so the brightest, largest area is an empty ceiling.
- **Lens distortion.** The camera sits at 3.4 with a 22 mm lens looking up. The table converges strongly, the paper balls in the foreground are huge, and the rug flowers stretch.
- **Empty floor.** The bottom 30 % is rug plus crumpled paper. The paper is a nice idea, but at this scale it is filler.
- **Story props off-frame.** The OLD map and the cork board are about 45 px wide on the phone, behind the lamp at the right edge. The old map is supposed to be a story object (it pays off in a match cut). Here it is unreadable: a pale blue river and grey lines.
- **Missing period props.** The bed corner, kettle, coat on hook, T-square and rolled drawings are not visible.
- **Beck's placement.** The Beck placeholder is jammed against the left frame edge, partly cut. His feet are hidden behind the basket, so grounding cannot be confirmed (§G.2).
- **Set squares.** The cyan and green set squares sit on top of the diagram and hide the interchange area.
- **Luma.** Luma 112 is above the §G limit of 110.

## Still 3: platform_tunnel

What works:
- The tiled vault with the maroon ribs is period-correct.
- The PICCADILLY CIRCUS roundel and the clock read on a phone.
- The crowd cards have a warm rim.
- There are layers of figures receding toward the end wall.

What fails:
- **The tunnel does not read deep dark blue.** The vault is lit near-white lavender (top-third luma 151).
  - The far end is filled by the orange-lit train face and a bloom. The tunnel mouth is invisible.
  - Shade hue is blue (250), but the frame reads lilac, white and orange. It needs to read as a dark blue tube lit by globes.
  - R5 and R2 both get their mood from large areas of deep saturated dark blue with small hot practicals. This still has the opposite ratio.
- **Empty floor.** Rows 900-1280 are bare blue floor tiles: about 30 % of the frame and the dullest part of it.
- **Foreground clutter.** The dark slab in the left foreground (counter or bench) is an unreadable block cut by the frame edge.
- **Mirrored text.** The left-wall WEMBLEY poster prints as "YELBMEW". It must be fixed.
- **Hidden boards.** The MIND THE GAP board is hidden behind a passenger card ("MI…AP").
- **Old map at a grazing angle.** At x 70-100 on the left wall it is unreadable at full size and invisible on a phone.
- **Camera angle.** Eye-level, straight down the axis. §H.2 says to avoid this as the default.
- **Blown lamp.** The globe lamp at the top right is clipped by the frame and blown out.
- **Grounding.** The nearest cards' feet read, but there are no contact-shadow discs (NOTES says they are "implied by the bright floor"). §G.2 needs a visible contact shadow.

## Changes for the builder (beck.py / beck_tex.py), in priority order

1. **Replace the modern skyline with 1930s London (still 1)** in `build_london` far-field rows (beck.py about lines 281-291) and `beck_tex.skyline()`.
   - Far-field boxes:
     - Cap the heights at 8-14 (now 12-38).
     - Top every block with `pitched()` slate roofs (#3a3550) or a parapet, plus 1-3 chimney stacks (box 0.8x0.8x2.5 with 2-4 terracotta pots).
     - Use brick (#8a3a2a to #6a2c28) and stone (#cbbd9a) facades, not royal blue.
     - Light only about 25 % of windows, and use smaller ones.
   - `skyline()` cutouts:
     - Building heights 40-110 px of 512.
     - Near-black blue silhouette (#141838).
     - Add 2 church spires, St Paul's dome with lantern, Big Ben (tall thin tower with a lit face), a gasholder ring, and smoke plumes.
     - Window probability 0.15.
   - Nothing on the horizon may be taller than the clock tower.
2. **Sky and horizon (still 1).**
   - Raise CAM1 `shift_y` to about 0.30, or lower the far-field and skyline heights, so the deep-blue zenith fills the top 15-20 % of frame.
   - In `dusk_sky`, narrow the magenta stop from 0.09 to about 0.055 and desaturate it to about (0.42, 0.20, 0.55). Pull the deep-blue stop (0.17) down to 0.11.
   - Target: magenta under 8 % of sky pixels; a thin orange band showing only between low rooftops.
3. **Make still 3's tunnel deep dark blue.**
   - Retint the vault tiles toward a cool blue-grey (#7f8cc8 diffuse) and cut the globe energies about 40 %. Make the ceiling fall off to #1a2466 between the globes.
   - Build a real tunnel mouth: a large black-blue disc (#070d33) with a liner ring on the end wall. Push the train back inside it so only two hot headlamp points plus a small warm spill show.
   - Keep the headlamp spot as the key and the globes as the warm practicals.
   - Targets: top-third luma ≤ 110; the end-wall area dark blue (hue 225-245, value < 0.35); overall luma 90-105.
4. **Reframe still 2 (CAM2).**
   - Raise the camera to about 4.8, tilt down about 10 degrees, lens 30. Ceiling ≤ 12 % of frame, floor ≤ 20 %.
   - Move the `old_map` and `old_map_img` parts and the cork board in beside the left edge of the drafting board, facing camera. Size them so the old map is at least 18 % of frame width, with a sepia tangled-lines look and a frame.
   - Stand the Beck placeholder fully in frame, side-on at the board, holding a pen, with a contact shadow and the blue window rim.
   - Add the bed corner and patchwork quilt (left foreground), a coat on a hook, a kettle on a small stove, a T-square on the board edge and rolled drawings in a pot.
   - Move the set squares to the board margin so they don't cover the interchanges.
   - Lower the lamp and pendant energy about 10 % to bring luma to ≤ 108.
5. **Fill the empty floors.**
   - Still 3, rows 900-1280: add a near bench with a seated passenger reading a folded map, a porter's trolley with suitcases, dropped newspapers, a chocolate vending machine (period "Nestlé-style" red box, no brand), and floor light pools under each globe.
   - Still 3: replace the anonymous dark slab at the left with a readable wooden bench end or a ticket-machine silhouette.
   - Still 3: consider a raised camera (z about 4.5, looking slightly down the platform) or a 3/4 angle across the track instead of the straight axis view.
   - Still 1, bottom-right road and pavement: add a flower stall, a newspaper kiosk with a readable NEWS board, parked black cabs, railings, a pillar box and another 30-40 crowd cards.
6. **Fix the text and signs for the phone.**
   - Un-mirror the WEMBLEY poster: flip its UVs in `build_platform`.
   - Move MIND THE GAP so no card covers it.
   - Turn the platform `old_map` (about line 616) to face the camera at ≥ 30 degrees off the wall, or move it to the end-wall side panel. At least 12 % of frame width.
   - Rotate the ROOMS sign horizontal and enlarge it to at least 14 px cap height at 360x640.
   - Enlarge the NEWS kiosk sign and the diagram station labels.
   - Check every sign on a 360x640 crop.
7. **Period props, still 1.**
   - Make the bus a red (#c8201e) double-decker: two window rows, open rear platform and stair, cream band between decks, front route board.
   - Give the clock tower Big Ben features: gothic pinnacles and a gold-trimmed face.
   - Give the dome a stone colour (#cfc4a8) and a lantern, not pale pink.
8. **Grounding of the placeholder actors (§G.2).** Add explicit soft contact-shadow discs (dark multiply alpha, about 1.2x foot width) under every crowd card in stills 1 and 3 and under Beck in still 2. Keep the orange and blue rim as it is.

After 1-4 are done, re-render the board and send it back to QA-art. 5-8 can land in the same pass.

---

# Round 2 (re-review after the builder applied items 1-8)

Inputs: round-2 board_1..3.png at 720x1280 and at 360x640, stats.json, and the NOTES.md round-2 section. Compared with the same references as round 1 (R3, R5, R2 and R4 sheets, and the film-2 frames).

All three stills now pass the colour gates:

| still | sat | luma | vivid |
|---|---|---|---|
| 1 | 0.685 | 87.0 | 69 % |
| 2 | 0.645 | 98.2 | 64 % |
| 3 | 0.623 | 88.4 | 76 % |

Magenta now covers 1.7 % of the top 20 % of rows in still 1 (it was 22.7 %).

## Verdict: **SHIP** (look approved for the full set build)

The board now reads as the intended world:
- low 1930s London at dusk under a deep-blue sky;
- an amber lodging room lit by a lamp against a blue night window;
- a dark-blue tiled tube with warm globes and a headlamp in the tunnel mouth.

It is in the same family as R5 (deep blue with hot practicals) and R4 (warm interior against a blue window), and as vivid as film 2. The problems that remain are local and do not change the look. They are listed below as mandatory carry-forwards for the full build, not as board blockers.

## Scores, round 2 (round 1 in brackets)

| still | density / ornament | light & colour | composition | period | match to refs |
|---|---|---|---|---|---|
| 1 london_dusk | 8 (7) | 8 (7) | 7 (6) | 7 (3) | 7 (5) |
| 2 beck_lodgings_night | 7 (5) | 7 (6) | 7 (4) | 7 (7) | 7 (5) |
| 3 platform_tunnel | 6 (6) | 8 (5) | 6 (5) | 7 (6) | 7 (5) |

"Rich and detailed?" (§H.3): yes for 1 and 2. Still 3 is a marginal yes, because the bottom third is still mostly bare floor.

## What is still wrong (fix in the full build)

### Still 1
- **Skyline cards float.** The two far skyline cards are horizontal strips with an orange band showing under each one (around y 300-320 and y 400-440 at 720 wide). They read as floating silhouette strips, not continuous ground to the horizon.
- **Two domes.** The skyline card has a domed silhouette on the horizon AND the near St Paul's is in the frame.
- **Plain near dome.** It is smooth lavender plastic with no ribs, drum columns or stone tone.
- **Bus roof.** It shows red diagonal streak artefacts (glare or texture).
- **ROOMS** is cut by the frame edge.

### Still 2
- **Floor share.** The rug still covers about 30 % of the frame (y 870-1280) with only table legs on it.
- **Ink bottles are oversized.** Each is about the size of Beck's head.
- **Board text hidden.** The NOTICE table hides the bottom of the diagram, and a red "UNDERGRO…" label sits half-hidden on the ledge.
- **Beck is small.** He is about 15 % of frame height and stands idle by the window. That is fine for a set still, but not for a shot.

### Still 3
- **Bare floor.** The bottom 30 % is still bare tiles with two newspapers.
- **Unreadable foreground blocks.** The pink-mauve box at the bottom right and the left benches read as blocky slabs, not wooden benches. They need slats, ironwork legs and a wood tone.
- **Actor cut in half.** The right-edge passenger card (brown coat) is cut in half by the frame (§G.3).
- **Mid-left props.** The vending machine and trolley read as grey boxes.
- **Blown globe.** The globe lamp at the top right is still blown and cropped by the frame.
- **Small map.** MAP OF LONDON on the end wall is borderline on a phone.

## Look rules the FULL set build must carry forward (all 4 locations, all shot_plan cameras)

1. **Palette.**
   - Deep-blue night or tunnel as the base field, with warm amber practicals and the four Tube-line colours as accents.
   - Magenta ≤ 5 % of any sky. Orange only as a thin band between low rooftops.
   - Per shot: sat ≥ 0.50, vivid ≥ 45 %, luma 85-110. Check top-third luma ≤ 115, so ceilings and vaults never become the brightest area.
2. **Period skyline everywhere London is seen** (s02 and s15 BIGZOOMs, window views from the lodgings and from PUBLICITY).
   - Only 4-6 storey brick and stone, pitched roofs, chimney pots and smoke, spires, ONE St Paul's dome, ONE Big Ben. No towers taller than the clock tower.
   - Skyline cards must sit on a continuous dark ground or overlap each other, never over an orange strip. Remove the dome from the skyline card.
   - Give the near dome ribs, a drum colonnade and a stone colour.
   - Re-check the skyline from every s02 and s15 camera height, not just CAM1: the cards must not show their edges or float from higher or lower viewpoints.
3. **Floors and ceilings.**
   - In every interior shot the ceiling is ≤ 15 % of the frame and visible bare floor is ≤ 20 %.
   - Fill floors with motivated clutter at the right scale: rugs with edges, chairs, trunks, papers, luggage, benches with wooden slats and iron legs, light pools.
   - Lodgings: add a chair, a trunk and a rag rug edge in the open rug area. Shrink the ink bottles to about 0.35x their size.
   - Platform and ticket hall: benches, trolleys, litter, light pools, and passengers sitting as well as standing.
4. **Lenses and angles.**
   - Lens ≥ 28 for interiors. The 22 mm lens on the board caused the round-1 distortion; use it only for the extreme-wide crane moments.
   - Keep the camera at about 4.5-5 D for rooms, looking slightly down.
   - Follow shot_plan's "foreground prop 1-2 D from the lens", but the prop must be readable: a lamp, an ink bottle or a ticket barrier, never an anonymous box.
   - No eye-level, straight-down-the-axis platform shots as the default.
5. **The tunnel stays deep dark blue.**
   - The tunnel mouths, the noodle-tunnel cutaway and the carriage windows are near-black navy.
   - Warm light comes only from globes, headlamps and lit carriage windows.
   - Do not light the vault to near-white again.
6. **Story objects read on a phone.**
   - The OLD map is ≥ 12 % of frame width whenever it is the subject: s03 ends on it, and there is a match cut from the platform to the lodgings.
   - The diagram, NOTICE and all signs must be legible at 360x640 (cap height ≥ 14 px).
   - Check every sign texture for mirrored UVs: this happened 3 times on the board.
   - Nothing sits in front of a sign the beat needs (MIND THE GAP, WAY OUT, PUBLICITY DEPT, the diagram's lower edge).
7. **Actors.**
   - The placeholder puppets and crowd cards are replaced by the cast22 models for every named character. Crowd cards may stay only for the far crowd (under about 8 % of frame height).
   - Every actor needs a contact shadow, a rim light (cool blue indoors from the window, warm outdoors from lamps), a prop in hand, and an action (§I.5).
   - No actor cut in half by the frame edge (§G.3). Beck at the board holds a pen or ruler and leans in.
   - BIGZOOM ends frame the character at 35-60 % of frame height.
8. **Lights and artefacts.**
   - Keep globe and lamp discs from clipping to flat white at the frame edge: dim them or reframe.
   - Remove the red streaks on the bus roof.
   - Keep warm halos and bloom small, as on the board, so they stay crisp on a phone.
