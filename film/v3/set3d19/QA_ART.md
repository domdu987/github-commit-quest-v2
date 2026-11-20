# QA-art: set3d19 SET gate (27 tiles + ship_contact)

Compared with board.jpg, styleboard/QA_ART.md and film 16's set contact sheet. All tiles are sharp, with no DOF and no readable text. Film 16's set sheet showed lived-in rooms with characters placed well in every preset. This sheet is not at that level: several presets cannot stage the shots planned for them.

## WORKSHOP: FIX-FIRST
| density | light/colour | composition | materials | board match |
|---|---|---|---|---|
| 7 | 5 | 5 | 6 | 6 |

The shop_wide tile is good: it is dense, its practicals are warm, and the H1 frame and balls now read as brass. The closer presets fail on the colour rules and the must-fix list.
1. **BLOCKING, colour.** shop_clock DAY and the H4 tile are monochrome orange: the wall, bench and floor all sit at hue 25-31. Cut the sun's warmth on the bench top by 30 %. Add the blue-violet fill (about 6500 K, 40 W) on the walls and floor. Set the bench wood to a darker walnut (#6b4a2e) so that the honey and brass stand out against it.
2. **BLOCKING, NIGHT.** NIGHT looks almost the same as DAY, except in the window. Lower the ambient to 35 %. Keep only the candle and lantern pools, and put a cool moon patch on the floor and wall.
3. **BLOCKING, must-fix carry-over.** Black gear-tooth slivers are still on the wall gears (W06/W10 at x 240-280, y 230-300) and inside H1 (W04 at x 200-310, y 560-640). The blue-grey iron bars on the wall and beam are still there (W04 at y 200-230; W10 at x 380-600, y 180-380; W08 at y 650). Make them warm iron #3a3430, or remove them.
4. **BLOCKING, shot 14.** The H4 is about 70 px wide. Move it to the front of the bench and make it 150 px or more wide. Move Harrison 120 px left, because he is half cut at the right edge.
5. **BLOCKING, H3.** The H3 reads as a wooden crate. Give the box the brass material (#cb9f48) and make the two balances big polished rings on top.
6. **NOTE.** The rag rug in shop_wide is a bullseye target. Use muted stripes or a braid in ochre, rust and grey. Move the gear lying on the rug onto the bench.
7. **NOTE.** shop_bench: the bottom 30 % is the blank bench front and dark floor. Put the plane and a curl of honey shavings 1-2 D from the lens at the bottom-left, for shot 1.
8. **NOTE.** shop_door is not in the shot plan, but its door is a blank dark slab, the wall is empty, and there is a cream ring with no source at the top-left. Fill the wall with a coat peg, saws and a window, or drop the preset.

## HALL: FIX-FIRST
| density | light/colour | composition | materials | board match |
|---|---|---|---|---|
| 7 | 6 | 4 | 6 | 6 |

The crimson room, chandelier, Moon picture, telescope, bookcases and table read well. Problems:
1. **BLOCKING, garish carpet.** The concentric yellow and red medallions are a target. They cover about 35 % of hall_table and hall_low, which is over the 25 % limit. Change the gold to #a8894a, desaturate the red to #7a2a2a, and replace the rings with a soft oval medallion that is 50 % smaller. Tilt hall_table's camera up 4°.
2. **BLOCKING, heads.** In hall_wide the heads sit at y 764-926, and Harrison's at 926 and the mocker's at 883 are past the y 880 limit. Raise the crane camera 0.4 D and tilt it down 3°, or move the marks 1 D upstage, so that every head is at y 760 or above.
3. **BLOCKING, mocker missing.** In hall_low the mocker's card (head y 643, x 298) is hidden behind the chair backs and the table leg. In hall_window his head is at x -466, off frame. Shots 7, 8, 9, 20, 23 and 25 need him. Move mocker_telescope into frame clear of the furniture, at about x 360 with the head at y 520-600. Push hall_low's table 1.5 D right of the lens line.
4. **BLOCKING, crude door / empty corridor.** In hall_door the left leaf is three separated slabs with light showing between them. The corridor is a flat cream void. Build each leaf as one panelled piece (3 raised panels, a brass knob, a gilt moulding). Dress the corridor with a floor runner, two sconces, a portrait and a far wall at 4 D, and lower its emission to 60 %.
5. **BLOCKING.** The King's chair (hall_wide and hall_table) is a flat gold slab. Model it as a gilt armchair with crimson velvet seat and back, as the spec asks.
6. **NOTE, EVENING.** EVENING looks like DAY with a blue window. Cut the fill by 40 % and let the candles and chandelier carry the pools.
7. **NOTE.** The charts in hall_window are big cream cards with dots and read as placeholders. Make them smaller, yellowed and slightly curled, with fine lines. The window's X muntins look wrong: use a Georgian grid.

## SHIP: FIX-FIRST
| density | light/colour | composition | materials | board match |
|---|---|---|---|---|
| 5 | 5 | 3 | 5 | 6 |

ship_hero and ship_coast keep the approved look. The deck, rail and rocks presets are dark navy blocks.
1. **BLOCKING, ship_deck.** A navy-violet mast fills the right 25 % of the frame. The wheel is grey-violet, and the binnacle is a gold blob on a grey box again. The wheel fills the head band, so there is no room for 2-4 characters. Warm the mast to a lit wood or black of #3a2e26 and keep it under 10 % of the frame width. Make the wheel wood with brass caps. Build the binnacle as a wooden pedestal with a brass hood. Move the wheel to the frame side, 1-2 D from the lens, and clear deck from y 450-1000 for William, the captain and the astronomer. Shot 15 also needs a short mast shadow on the deck in frame. Use the warm sail colour (#e8dcc0), not grey-mauve.
2. **BLOCKING, ship_rail.** The dark navy bulwark covers about 40 % of the frame diagonally. There is no cap rail, no bow wave and no foam in view, and the deck strip is too narrow to hold William (shot 18). Add a lighter cap rail (#5a4632) and plank seams. Turn the camera 20° outboard and forward so that the bow wave and the lacy foam bands can be seen. Widen the deck strip to 35 % of the frame width. Confine the glitter to one path 15 % wide.
3. **BLOCKING, ship_rocks.** Magenta is 19.9 % (the limit is 10 %), so the whole frame is violet-mauve. The rocks are grey faceted pyramids, and a single clean fair-weather cloud floats in the storm. There is no fog. The lantern is a sliver at the edge. The foreground cannon is a navy block and the gun carriage is magenta. Grade the frame to blue-grey slate. Make the rocks rounded black basalt (#1c1c20) with wet highlights and foam at their base. Replace the cloud with a low storm deck. Add two fog layers. Bring a lantern into frame at 1.5 D with a warm 2200 K pool. Give the captain room for shot 4 at the left with the head at y 500-650.
4. **BLOCKING, bow wave and wake.** In ship_hero the bow wave is a flat white sled at the waterline and the V-wake cannot be read. Make it a curling roll at the stem with lacy breakup, and make the stern V visible. In ship_aerial, remove the floating foam patch (x 240-460, y 830-880) and the square glitter tiles (x 0-200, y 1000-1100). Its glitter spreads over 40 % of the sea. Confine it to one path.
5. **BLOCKING, cost.** ship_aerial costs 43.4 CPU-s (40-41 s in ship_cost), over the 40 s limit. Cut the samples or the sea subdivision.
6. **BLOCKING, ship_coast.** It has no place for people, but shots 19 and 21 need William, the crew and the astronomer. Add a deck or longboat foreground, or a beach with marks shore_a and shore_b in frame. The ship is cut by the left edge, so move it 60 px right. The foam squiggles at x 0-150, y 800-1280 read as noise.
7. **BLOCKING, hue check.** The ship hue check found no cast-shadow pixels ("None") on every tile, so the outdoor shade band of 225-265 has not been checked. Fix the sun-only pass and report the shade hue.
8. **NOTE.** In ship_hero and ship_coast the bottom 45 % of the sea is empty. Add a swell crest with a thin foam line, or a floating spar, as foreground near the lens.

## Preset coverage against the shot plan
- The shot plan names `ship_wide`, `set_ship_roll`, `set_moon` and a NIGHT-to-DAWN light (shot 13), but the API provides `ship_hero` or `ship_aerial`, `set_roll`, no set_moon, and no DAWN light. Align the plan or add DAWN to the set. **NOTE**
- The ship presets were rendered with no placeholder actors, so their staging has not been tested. Re-run the contact with placeholders on every deck and coast preset. **BLOCKING**

## Overall: FIX-FIRST
The WORKSHOP is closest to passing. The HALL needs the carpet, the head positions, the mocker in frame and the door. The SHIP deck, rail and rocks presets are not usable. Re-render the contact sheet after these fixes, before any render team starts.

## SET gate round 2
I checked both contact sheets, the full-size W/H/S tiles, all 18 ship tiles and the reports. All heads are inside the rule. Cost is at most 38.4 CPU-s.

**Shade-hue ruling: accepted as an exterior exception.** The hull shadow on the emission sea (hero, aerial and coast at NOON/DAY, 205-217) stays teal. The exception covers only the water: deck, sail, hull and sand shade must stay at 225-265, and they do (239-257).

### WORKSHOP: FIX-FIRST (one item)
| density | light/colour | composition | materials | board match |
|---|---|---|---|---|
| 8 | 7 | 7 | 7 | 7 |
Round 1: 1 colour **done**. 2 NIGHT **done** (luma 50 against 93-101). 3 **half done**: the iron is warm #452e2a, but the slivers remain. 4 H4 **done** (about 220 px). 5 H3 **done**. NOTEs 6-7 **done**.
1. **BLOCKING, black slivers (carried over again).** They show at the wall-gear overlaps (W10 x 180-240, y 230-300; W06 rings) and as cracks inside H1 (W04 x 200-260, y 570-680). Fix: offset each overlapping gear by 0.02-0.03 D along its normal so the teeth do not intersect. Give the inner and back faces the gear material. Re-render W04, W06 and W10.
- NOTE: shop_bench DAY has a milky haze over its lower half. shop_clock DAY has hot patches under the bench (y 990-1150). H1 half-hides William in shop_wide. NIGHT has no moon patch on the floor.

### HALL: PASS
| density | light/colour | composition | materials | board match |
|---|---|---|---|---|
| 8 | 7 | 8 | 7 | 7 |
Round 1 items 1-5 are **done**: carpet, heads (743 at most), mocker in frame, panelled door with a dressed corridor, gilt chair.
- NOTE: In hall_table, Harrison (x 435) covers the King (x 474), so teams should offset a mark. The window arch is stair-stepped and its muntins are still a fan. EVENING hall_window keeps a warm sun shaft. hall_wide has medallion arcs in its bottom corners.

### SHIP: FIX-FIRST
| density | light/colour | composition | materials | board match |
|---|---|---|---|---|
| 7 | 6 | 7 | 6 | 7 |
Round 1 status:
- **Done:** 1 deck (mast, wheel, binnacle, clear deck), except the sail colour. 2 rail. 5 cost. 6 coast (beach, longboat, three people, whole ship). 7 hue (with the ruling above). Placeholders on every preset.
- **Partly done:** 3 rocks (grade, basalt and storm deck done; the lantern is wrong). 4 hero mostly done. The aerial foam patch is gone, but the aerial glitter is not fixed.
1. **BLOCKING, ship_rocks lantern.** It is a flat #fe8200 block about 190×420 px, cut by the top edge, with no pool. Fix: make it about 110 px wide, fully in frame at x 520-640, y 260-440, with a warm-iron frame (#3a3430), amber glass about #ffb060 and emission halved. Add a 2200 K point light that pools on the deck by the captain.
2. **BLOCKING, sails.** The deck and rail sails measure #b0b1d9 (hue 240, lavender), but the hero's sails are cream. Fix: set the sail base to #e8dcc0 with translucency at 0.1 or less.
3. **BLOCKING, ship_aerial glitter.** It still covers the left 40 % of the sea (x 0-300, y 280-900), glares across the caption band at y 860-900, and the square tiles remain at x 0-250, y 1000-1100. Fix: rotate the sun azimuth or raise the roughness to leave one path 15 % wide or narrower, behind the ship and above y 700. Remove the low tiles.
- NOTE: The rocks cannon is violet #332a3e; make it iron #2a2a2c. The rocks sailor stands outboard of the bulwark, so move him inboard. The fog is a flat band. The hero bow wave is still a sled. On coast, a brown disc floats on the sea (x 490-560, y 600). Foam dots float on rail.
- NOTE: ship_contact.py burns the cyan guide into ship_work/final/*.png. Draw it on a copy.

### Other NOTEs
API.md still documents `caption_shade`; delete it. The shot plan still names ship_wide, set_moon and DAWN; align it.

### Overall: FIX-FIRST
HALL teams may start. The WORKSHOP needs only the sliver fix, and the SHIP needs fixes 1-3.

## SET gate round 3
I judged W04/W06/W10, S02-S07 and all 18 ship tiles at full size, with crops, plus both contact sheets and all reports. Heads are inside the rule and cost is at most 35.4 CPU-s.

| # | Item | Status |
|---|---|---|
| 1 | Gear slivers | **W04 FIXED** (H1 shows a clean dark cavity with no cracks). **W06 and W10 OPEN**: black V-wedges at every rim joint and tooth root. On W06 they line both front wheels (x 0-500, y 150-430); on W10 they sit at x 60-330, y 180-330. |
| 2 | Rocks lantern | **OPEN (half)**. The size (115 px, x 524-639), framing and shape are fixed. Still wrong: the bars render amber (#b77e3f) instead of iron, the glass is matte orange (#b97b36) with no glow, and the deck shows no warm pool in any light. It does not read as lit. |
| 3 | Deck/rail sails cream | **FIXED** at NOON/DAY (#e7d9c2, hue 36-38). |
| 4 | ship_aerial | **FIXED**. One path about 100-110 px wide (14-15 %), behind the ship and above y 500. No tiles and no hot pixels below y 820, in all three lights. |
| 5 | N1 rail band glare | **FIXED**. NOON 0 % clipped, DAY 1.7 % (x 662-719), STORM 0.2 %. |
| 6 | N2 lantern slab | **FIXED** as geometry (cage, cap, base). See item 2 for the art misses. |

**Shade-hue ruling: accepted.** Cream sail shade (hue about 36) is an exception, like the sea. By eye, the deck shadows are blue-violet: S03 #4f4852 and S04 #434251 (hue 245). The rail cast shadows on deck are cool grey. QA-tech should mask the sail material out of the hue measurement instead of reading the mixed mean.

**Sail shading.** At NOON/DAY the sails are slightly flat but readable, with rigging shadows and a soft gradient. **New blocker:** `_sail_self_cream` mixes 85 % emission at a constant level, so in STORM_DUSK the sails stay at luma 190-214 while the deck drops to 63. They glow in the storm.

### WORKSHOP: FIX-FIRST
1. **BLOCKING, slivers on W06 and W10.** The cause is in `h19_kit.gear()`: the rim chord is sized at the centre radius r, so the outer corners open on thick rims. Fix: `seg = 2*(r+rim/2)*tan(pi/n)*1.05`, or use n ≥ 24 on the wall gears. Re-render W06 and W10.

### HALL: PASS (unchanged)

### SHIP: FIX-FIRST
1. **BLOCKING, storm sails.** Scale the sail emission per light (STORM_DUSK k ≤ 0.15) or drop the mix factor to 0.4 or less. Re-render deck, rail and hero at STORM_DUSK.
2. **BLOCKING, rocks lantern lit.** Set the bars to unlit #3a3430, give the glass a visible emission toward #ffb060, and raise `pool_e` until a warm pool reads at the captain's feet. Re-render ship_rocks ×3 and S06.

### NOTEs render teams must respect
- The rail inner bulwark shade is warm brown-black (#3b2723). Accept it as local colour, but keep characters off it.
- A bright yellow gunport slot sits at S05 x 395-440, y 920-1090.
- The aerial STORM wake fans read as light rays. A gull sits on the bowsprit (x 220-270, y 730-790).
- The coast ship's square sails render grey.
- The ship_rocks sail reads lavender (#908fa5).
- The ship_hero tiles (not re-rendered) still carry the burned cyan guide.
- The round-2 NOTEs stand: cannon colour, outboard sailor, flat fog, sled bow wave, H1 hiding William, Harrison covering the King, and the window muntins.

### Overall: FIX-FIRST
HALL proceeds. Render teams may also start on ship_aerial and ship_coast, and on ship_deck and ship_rail at NOON/DAY.
