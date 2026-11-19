# Film 19 "ไอ้ช่างไม้": draft shot plan (beats only)

Times are filled in once the narration exists. fal.ai balance was exhausted on 2026-11-19, which blocks the narration.

Target:
- 24-26 shots, about 68 s.
- Camera grammar of film 2 (production-lessons §10): every shot moves, FG props 1-2 D from the lens, DIS on place/time changes, CUT on beats/quotes.
- Mouths move ONLY on the astronomer's two quotes, boss and false.

## Locations (set3d19, NEW)
- **WORKSHOP**: Harrison's village workshop (Lincolnshire). Presets `shop_wide`, `shop_bench`, `shop_clock`.
  - Lights: DAY (warm low sun through the window), NIGHT (candles and lamp, blue-violet moon fill).
  - Hooks: `set_clock(1|2|3|4)` shows H1 big brass on the bench, H2, H3, or the H4 watch on a cloth; balance bars swing; shavings; `set_age(k)` is cast-side only.
- **SHIP**: a 1760s 50-gun warship at sea. Presets `ship_deck`, `ship_rail` (outboard: hull, wake, foam), `ship_wide` (the ship from the sea), `ship_rocks`, `ship_coast` (Jamaica/Barbados palm coast and harbour).
  - Lights: NOON (high sun, glitter), STORM_DUSK (rocks: grey-violet, lantern), DAY.
  - Hooks: `set_sea(t)` animates waves, foam and wake; `set_ship_roll(t)` parents the deck cast to `ship_root`; `set_sun_overhead(k)`.
- **HALL**: the astronomers' hall, which is also used for the ending. Presets `hall_wide`, `hall_table`, `hall_low`, `hall_window`.
  - Lights: DAY, EVENING (the King's sessions, candles).
  - Hooks: `set_box(state)` shows the box with three wax seals, open or closed; `set_moneybag(on)`; `set_moon(k)` lights the Moon disc / orrery; the King's chair.

## Shots (sentence → beats)
| # | sent | set / preset | action | camera |
|---|---|---|---|---|
| 1 | hook | WORKSHOP shop_bench DAY | HOOK IMAGE: the carpenter, shavings on his apron, holds up a big brass sea clock (H1) whose balance bars rock, and grins | low, push 8 %/s, plane and shavings in FG |
| 2 | hook | SHIP ship_wide NOON | "where the ship is mid-sea": tiny warship alone on an endless glittering sea | aerial drift, slide |
| 3 | hook | HALL hall_wide DAY | "scholars can't": astronomers squint through the telescope, scratching wigs | crane down, chandelier FG |
| 4 | pivot | SHIP ship_rocks STORM_DUSK | "nobody knew where": captain peers at a blank sea chart, fog | push, rope coil FG |
| 5 | pivot | SHIP ship_rocks | "ships sank by the dozen": the ship lurches past black rocks; sailors bail (comic, no injury) | whip, shake 1 |
| 6 | pivot | HALL hall_table DAY | "Parliament set a prize": a fat money bag lands on the baize table; astronomers' eyes glint | push-in on "สองหมื่นปอนด์" |
| 7 | boss | HALL hall_window | "must measure the Moon and stars": astronomers at the telescope, the Moon disc glows | slide, telescope FG |
| 8 | boss | HALL hall_low | MOCKER (pompous astronomer, big wig, star-gown) turns and laughs, belly bounce, quote "นาฬิกาเนี่ยนะ!" lip-sync | low, push 9 %/s |
| 9 | boss | HALL hall_low | "ให้พระราชามาจับเวลาเองเลย!" lip-sync, mimes timing a pocket watch with a mock-royal bow | quick push-in on the dare |
| 10 | nickname | HALL hall_wide | all scholars laugh, wigs bounce; the carpenter at the door holding his clock; snap to him on "ไอ้ช่างไม้" | slide, snap |
| 11 | count | WORKSHOP shop_wide DAY | H1 on the bench, the carpenter saws and files ("5 years"); sun moves | push |
| 12 | count | WORKSHOP shop_clock NIGHT | H3 on the bench, candles; he is older, hair greyer ("10+ years") | slide |
| 13 | count | WORKSHOP shop_clock NIGHT→DAWN | "hair all grey": he leans back, white-haired, rubs his eyes | push-in |
| 14 | reveal | WORKSHOP shop_bench DAY | he lifts the H4 watch, saucer size, beside the big H1: one image of the shrink | snap, whip |
| 15 | reveal | SHIP ship_deck NOON | "noon at sea, sun overhead": son William shoots the sun with a quadrant; the shadow under the mast is tiny | crane up to the sun |
| 16 | reveal | SHIP ship_deck NOON | "the watch still shows home time": open H4 in his palm, home-time hands visible (no numerals needed) | push to the watch, rail FG |
| 17 | reveal | SHIP ship_wide NOON | "each hour = 15°": the ship sails on with the wake; a dotted line of the sun's arc… (IN-WORLD only: the ship's shadow and the sun) | aerial slide |
| 18 | aha | SHIP ship_rail NOON | William crosses the sea with H4 tucked in his coat, wake and foam below | outboard track |
| 19 | aha | SHIP ship_coast DAY | Jamaica palm coast; "only 5 seconds off": William holds up the watch, the crew cheers | push-in on "ห้าวินาที" |
| 20 | false | HALL hall_low DAY | mocker shrugs: "ฟลุ๊ค! ต้องลองใหม่!" lip-sync | hard CUT, push |
| 21 | crisis | SHIP ship_coast DAY (Barbados variant) | second trial; the Moon-method astronomer fumbles a big quadrant while H4 ticks | slide |
| 22 | crisis | HALL hall_table DAY | half a money bag slid across; then the watch is locked in the box, three red seals stamped | push-in on the seals |
| 23 | ending | HALL hall_window EVENING | old Harrison (≈80) shuffles in with H5; the KING (George III, star sash) takes it | dissolve, crane down |
| 24 | ending | HALL hall_table EVENING | the King times the watch himself, day after day (candles burn down, calendar of 10 weeks = 10 candle stubs) | slide, time-lapse |
| 25 | ending | HALL hall_low | "exactly as the astronomer dared": the mocker in the background, jaw dropped | snap |
| 26 | ending | HALL hall_table | Parliament's money bag lands in front of the old carpenter; last image: he winds the watch, the mocker's wig slides off | push-in, hard cut on the last word |

## Cast (cast19)
| Character | Description |
|---|---|
| `harrison19` | carpenter-clockmaker. Leather apron over a shirt, brown waistcoat. Variants: young brown hair (1730s), grey (1750s), white-haired old (80) |
| `william19` | his son. Young adult, blue coat, tricorne |
| `astro19` | the MOCKER, an invented astronomer. Big powdered full-bottom wig, plump, dark gown with gold stars, spectacles pushed up |
| `astro19_b`, `astro19_c` | other astronomers / Board members |
| `king19` | George III (generic Georgian king, no portrait likeness). Powdered wig, blue coat with a star and a sash |
| `captain19`, `sailor19_a/b` | ship's crew |

Hand props are drawn on the cast cards: H4 watch, quadrant, pocket watch.
