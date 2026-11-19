# QA_TECH: set3d19 SET gate (film 19)

**VERDICT: FAIL**

t_anim.py: ALL OK (82 checks). Hooks/presets/marks in SPEC.md all present in API.md and in code (grep of every set_* def and every mark name: no gaps). Review done on contact.jpg and ship_contact.jpg at the sheet scale; individual tiles were not inspected at 100 %, so blur, z-fighting and slivers are judged from the sheets only.

## Issues

1. S02_ship_aerial_NOON (cost_report.txt): 43.4 cpu-s, limit 40. FAIL. ship_cost.txt also lists ship_aerial_STORM_DUSK at 40.9 (OVER) and ship_deck NOON/STORM at 39.1/39.4 (no margin). Fix: lower spp or sea-surface cost on ship_aerial (glitter/foam), re-measure; cost_report and ship_cost must agree (they differ by 3 s for the same tile).
2. S06_ship_rocks_STORM (hue_report.txt): magenta 19.9 %, flagged CHECK, limit 10 %. ship_hue.txt: ship_rail STORM_DUSK 20.1 %, ship_rocks NOON 13.9 %, DAY 14.1 %, STORM 18.8 %, all OUT. Fix: find the magenta source (probably the dark-violet hull/boat interior in the FG) and shift it to brown/navy; re-run the hue report.
3. Hue measurement missing for all 7 S* tiles and all 18 ship_work tiles: shade hue None, median None, cast 0.0 %. The outdoor 225-265 shade check was never measured (the sun-only render found no cast pixels). Fix: measure on a lit area with real shadows, or add a ground-plane sample. Missing measurement = FAIL.
4. H01/H02_hall_wide (cost_report heads): mocker head y 883, harrison 926, chin 932/984, so heads and chins fall inside the caption band y 880-950. The astros sit at y 764-852, mostly below 760. Heads must be in 450-760. The crowd is crammed into the lower left (heads cut by tile edge in the contact). Fix: raise the camera or move marks mocker_table, harrison_table, astro_a..e back so that heads land at y 450-760.
5. H07/H08_hall_window: mocker head y 793 to chin 957, head width 315 px (giant). Head is outside 450-760 and the chin sits in the caption band. Fix: pull the mark back or lower the camera.
6. H03/H04_hall_table: harrison head 616-698, king 571 (fine), but the table FG (green baize, papers) is bright and busy in the band y 880-950 on H03/H04 and hall_window (white papers at about y 1000, the baize at 880). Fix: darken or move the FG papers.
7. Caption band busy or bright, y 880-950:
   - W03/W04/W09 shop_bench: bright lantern, shavings and bench edge cross the band.
   - W05/W10 shop_clock and shop_bench: bright light patches and shavings on the bench top.
   - W01/W02 shop_wide: rug medallion and gear on the floor, saturated pattern.
   - H01/H02 hall_wide: busy carpet medallion and figures.
   - S03/S04 ship_deck: bright lantern and deck planks; S05 ship_rail: sun glitter and hull edge; S06 ship_rocks: bright sky/white rain lines near the band; S02 ship_aerial: strong glitter across the band, S07 ship_coast: glitter.
   Fix: dim and simplify the FG in y 880-950 (low-contrast rug, cloth or shadow), move the lantern and glitter out of the band.
8. Floating props: W03/W04/W09 shop_bench and W07/W08 shop_door: loose planks and offcuts on the floor read as flying or unattached (the plank at the right of shop_door is at an odd angle and appears to hover). H07/H08 hall_window: a floating telescope/tripod relation (the barrel at the left edge is cut by the frame). Fix: ground the planks and put the tripod legs on the floor.
9. Clipped and intersecting geometry:
   - S03/S04 ship_deck: blocky stair-stepped rail/binnacle with a cube-like blue column (mast boxed), the faceted sail and the blue mast are untextured flat navy (placeholder look); the mast stump is a flat dark-blue slab. Fix: texture or tint with wood.
   - S05 ship_rail: a huge flat navy hull wedge fills the lower-left of the frame (a flat, unfinished region).
   - S06 ship_rocks: faceted low-poly rocks. The boat interior is flat black (S06 and ship_rocks NOON/DAY).
   - H05/H06 hall_low: table front and chairs clip the frame bottom (a flat brown table slab); the telescope tube penetrates the bookcase at the left.
   - H09/H10 hall_door: door leaf clips the lintel and a flat cream slab fills the doorway (see 10).
10. Empty or unfinished areas the camera sees:
    - H09/H10 hall_door: the doorway is a flat uniform cream/yellow rectangle, with no corridor detail. Blown-out too (see 11).
    - W07/W08 shop_door: the door daylight is a flat green/blue card (W08 flat navy). Needs a visible landscape or corridor.
    - S03/S04 ship_deck: the sail is a flat grey plane, and the sea strip is a thin line. S05 ship_rail: the sail is a flat beige plane at the top.
    - S01_ship_hero: lower 45 % of the tile is empty flat teal sea (weak gradient only).
    - S02_ship_aerial: the lower half is repeated glitter only.
11. Blown-out areas: H09/H10 hall_door (doorway fully clipped to cream); W03/W04/W09 shop_bench (lantern body, flat white-yellow); S05 ship_rail (sun glitter patch); H03 hall_table (window sunlight, the candles are fine).
12. Blur/DOF: none seen on the sheets (DOF off in make_camera). S06 ship_rocks STORM (fog haze, not DOF). Needs a 100 % check of W05 and H07 by the QA lead (soft texture on the gears).
13. Readable text: none seen. Check the shop_door shelf (W07) and the hall map/charts at 100 %.
14. Black/magenta/placeholder textures: boat interior of S06 and the ship_rocks NOON/DAY boat floor are flat black (about 10 % of the frame); in W02/W04 the lower gears have black slivers (the NIGHT gear train reads as black holes). H05/H06 the carpet band at the very bottom is placeholder-flat. Fix: lift the shadow floor on the boat interior and the gear train (add an ambient fill), and shade gear rims brass.
15. Black slivers / z-fighting: the shop_clock gear panel (W05, W10) shows dark gap lines in the H1 gear train; W06 (NIGHT) shows black voids. A visible shimmer on the stair-stepped deck planks (S03). Fix: close the gaps and apply an offset on coplanar planks.
16. Medium-shot head room (450-760):
    - OK: shop_wide 560/584, shop_bench 580, shop_clock 460, shop_door 556-565, hall_table 571-616, hall_low 643, hall_door 618.
    - FAIL: hall_wide (764-926), hall_window (793).
    - UNVERIFIED: all ship presets. cost_report lists no heads for S01-S07. The deck marks (captain_wheel, william_rail, sailor_a..c, astro_deck, crew_bow) and shore marks were not projected into y 450-760. t_anim only checks that the marks exist. Fix: add placeholder staging for ship presets and print head_pixels per tile.
17. Stale/inconsistent inputs: ship_work tiles (DAY/NOON/STORM_DUSK x6) are a different render set to h19_work S01-S07 (different times, cost numbers disagree: aerial 39.7 vs 43.4). Contact tile labels use the h19_work set. Fix: keep one set and regenerate both reports from it.

## Round 2

**VERDICT: FAIL (two small items: S06 orange slab, S05 band hot spot)**

t_anim.py: ALL OK (82 checks). Tiles inspected at full size (W03/W05/W06/W07, H01/H05/H07/H09, S03/S05/S06/S07) plus pixel stats of y 880-950 for every tile. Caption shade card removed on purpose, not demanded.

### Round-1 status
1 Cost: FIXED. cost_report max 38.4 (W05), ship_cost max 37.7. Reports differ by up to 4 s on the same tile (different runs), both under 40. W05 margin is thin.
2 Magenta: FIXED. Max 6.9 % (S06 STORM), all under 10 %.
3 Hue missing: FIXED. All S and ship tiles now measured. Deck/rail/rocks sit in 225-265. Open-sea tiles referred to QA-art: ship_hero NOON 216.7, ship_hero STORM_DUSK 210.4, ship_aerial NOON 212.4, ship_aerial STORM_DUSK 213.5, ship_coast NOON/DAY 204.8/205.2 (S01, S02, S07 on the contact).
4 H01/H02 heads: FIXED. Heads 600-743, chins at most 783. Mocker feet 898 and harrison feet 943 sit in the band (feet only, accepted).
5 H07/H08: FIXED. Head 689, chin 751, 122 px.
6 H03/H04 FG: FIXED. Band mean 33, no bright papers.
7 Caption band: mostly FIXED. Interiors have band mean 23-112, clipped share 0. Remaining items below (S05, S02, S07).
8 Floating props: FIXED. W07 plank lies on the floor and the telescope stands on its tripod legs.
9 Geometry: FIXED. Deck rail and mast are textured, the hull is wood, the rocks are smoother, the doorway is open.
10 Empty areas: FIXED. H09 shows a corridor and W07 a garden. S02 lower half is still plain glitter water (acceptable for an aerial).
11 Blown-out: partly FIXED. H09, W03 and H03 are fine. S05 glitter still blown out (see N1).
12 Blur: FIXED. W05 and H07 are crisp at full size.
13 Text: FIXED. No readable text.
14 Black areas: FIXED. The boat interior is now plank. NIGHT tiles are 7-11 % near-black by design, with no voids.
15 Slivers: FIXED. Gear train is continuous on W06; no z-fight seen on S03.
16 Ship heads: FIXED. y 590-689, chins at most 733, listed in ship_heads.txt.
17 Stale inputs: FIXED. Contact sheets and both reports are from consistent runs.

### New failures
N1. S05_ship_rail_NOON (also ship_rail NOON/DAY): foam and glitter clip to white across x 523-719 inside the band, 7.6 % of band pixels at 240 or above (DAY 9.1 %). A glaring hot spot. Fix: lower sun glitter/foam strength, or tilt the camera so the sea sits above y 880.
N2. S06_ship_rocks_STORM and ship_rocks NOON/DAY/STORM: a saturated flat orange and yellow slab at top right, with no shading, reads as placeholder geometry and is out of palette. Fix: give it a material (wood/canvas) or remove or dim it.

### Notes, not failed
- S07_ship_coast band mean 217 (bright sand, no heads or text in the band, 0.8 % clipped). Consider a slightly darker sand FG.
- S02_ship_aerial band has 3.2 % clipped glitter at x 30-136. Minor.
- W05 cost 38.4 s has little margin.
