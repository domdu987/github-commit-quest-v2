# set3d19 style board: John Harrison / longitude

Three 720x1280 stills, Cycles CPU (4 threads) + OIDN, no DOF, no text, 22 mm / 36 mm camera, one hard sun with real cast shadows,
blue-violet ambient, painterly two-tone noise materials (film 16 machinery), grade = saturation 1.08-1.1. Grey cards are 3 D (1.62 m) stand-ins for the puppets.
Rebuild: `bash asm.sh && python3 sb.py shop|ship|hall|all [draft]`; `python3 hue_check.py`; `python3 make_board.py`. `sb.py` is the assembled self-contained scene (parts: machinery, part_common, part_clouds, part_shop, part_ship, part_hall, part_main).

| still | what it shows | render |
|---|---|---|
| sb1_workshop.jpg | Lincolnshire workshop, late-afternoon sun through a 6x5 small-pane window (shaft + floor patch with mullion shadows). Plaster, timber beams, treadle lathe + flywheel, longcase clock with open wooden movement, wooden gear wheels and saws on the wall, chisel rack, heavy bench with vise, plane, mallets, brace, square, glue pot, candle, oil lamp, **H1-style brass sea clock** (brass frame, exposed gears, two crossed dumbbell balance bars, four balls), leaning boards, chest, barrel, log stack, hanging lamp, herbs, sawhorse, stool, bucket, ~45 shavings. Dark foreground layer: sawhorse, plank, bucket, stool. About 28 distinct objects. | 131 s |
| sb2_ship.jpg | 50-gun RN ship from the quarterdeck: black hull with ochre stripe (bulwarks, platform), balustrade, ship's wheel, binnacle, rope coils, waist deck with 7 cannons on carriages, barrels, capstan, hatch grating, foremast with 3 sails, shrouds with ratlines, bowsprit, pennant, cumulus, island + tiny dark sail on the horizon. **Sea** = real wave mesh (about 320k tris built per camera pixel, 13 wave trains, fine ripples only as normals) with painted layers: deep blue-teal, turquoise crest tint, foam lines, haze to the horizon colour, sun-glitter path. | 95 s |
| sb3_hall.jpg | Georgian hall: arched sash window with sun shaft and floor patch, crimson curtains + gilt pelmet, dark wainscot, pilasters, gilt cornice, painted Moon disc, framed pictures, bookcase, brass refractor on a tripod pointed at the window, celestial + terrestrial globes, long table with green baize and star charts (dots and lines only), orrery, candelabra (table, floor), chandelier, chairs, navy rug with crimson border. About 30 objects. | 137 s |

Palette: honey wood #c28b3e, brass #cb9f48 family, terracotta plaster #b4663a, wood #976c4d, crimson walls #7e3028, navy rug, deck honey #9a7440, sea #08607f-#3cc8b8, sky #4a78cd-#92b7e7.

## Hue numbers (hue_report.txt; shade = real cast-shadow pixels from a sun-only mask render)
- sb1_workshop: cast-shadow mean hue 282.4 (median 265.4), band 225-265 -> OUT by the mean (median in band); magenta 9.3 % (<=10). Warm candle/lamp and sunlit-floor bounce pull the shade of brown wood to mauve; bluer fill fixes the hue but makes the room cold and dark (tried: hue 262 / blue 58 % of chroma). Same interior effect as film 16's chamber.
- sb2_ship: 257.5 (median 240), magenta 3.4 %, OK. Exterior: blue 69 % of chroma (sea + sky).
- sb3_hall: 255.8 (median 230), magenta 6.05 %, OK.

## What the full set will add
Workshop: second window and door, wall shelf of jars, a half-built sea clock frame, more hanging tools, rope and sacks, a distinct light-shaft volume. Ship: gun deck below, main and mizzen masts and the full rigging, a second camera on the poop looking aft, a view with sails above, the hull side and white wake along it from a boat-level camera, flags, lanterns. Hall: Board table with chairs both sides, wall maps, second window, more instruments, orrery arms animated, stairs and door.
