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
