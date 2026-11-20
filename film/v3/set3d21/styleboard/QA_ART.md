# QA-art, STYLE BOARD, set3d21 (film 21, Stirling Bridge)

Reviewer: Opus QA-art. The client delegated look approval to this review.
Inputs: still1 = hill_over, still2 = camp_bank, still3 = valley_loop (720x1280, MORNING, 64 samples), board.jpg with the caption band drawn, the 360x640 phone downscale, stirling_hue.py numbers, set3d10 contact_small.jpg and QA_ART.md as the series level.

## VERDICT: REJECT (re-shoot the three stills with the fixes below, then a quick re-check)
- **Approved as the direction:** hill_over's look. That means the low-poly lit world, cel clouds, teal river with white foam edges, red/cream and blue/gold pavilions, warm grass and a small castle rock. The builder should keep building in this look.
- **Rejected:**
  - camp_bank breaks the story. There is no river between the camp and the hill. It is also cold and empty.
  - valley_loop, the key reveal, breaks two client hard rules. The top 45 % is a haze that reads as blur. The river is a perfect-circle, ruler-straight band with a glow outline, which reads as a flat 2D diagram, not a river in a lit 3D valley.
- **Re-check:** re-rendering three stills costs about 4 minutes. Re-check them, not a new board round. If fixes 1-6 land, the set may go to the SET gate without another look round.

## Measurements (stirling_hue.py; caption band excluded)
| still | red | orange | blue | violet | magenta | sat | val | dark | shade hue | notes |
|---|---|---|---|---|---|---|---|---|---|---|
| target | 30-41 | 22-38 | 14-30 | 0-5 | <= 10 | 0.38-0.48 | 0.45-0.63 | 0.08-0.15 | 240-260 | exteriors may sit a little outside the band if there is a reason |
| hill_over | 27.5 | 13.4 | 31.4 | 8.3 | **12.3** | 0.34 | 0.57 | 0.11 | 251.6 | magenta over the limit (pink cobbles); orange low |
| camp_bank | 12.6 | **2.8** | **46.2** | 3.9 | 3.2 | 0.27 | **0.72** | **0.01** | 240.5 (edge) | cold, washed out, no shadows |
| valley_loop | **1.5** | 17.4 | 8.7 | 0.3 | 0.5 | 0.35 | **0.77** | **0.00** | **226.4** | flat noon look; shade hue out of band |

Sharpness: Laplacian variance by band (y 0-320 / 320-640 / 640-880 / 950-1280).
- hill_over: 129 / 476 / 897 / 306. Sharp.
- camp_bank: 101 / 305 / 880 / 1091. Sharp; the top band is sky.
- valley_loop: **8.8** / 398 / 673 / 655. The top band is land, not sky, so this is blur-like haze.

Density:
- Edge share (edge > 40): 0.073 / 0.103 / 0.059.
- Featureless 40 px blocks: 0.18 / 0.22 / 0.20. This passes, but in camp_bank the edges come from repeated grass spikes, not from objects.

Heads: every head is above y 880.
- hill_over: cy 612-664.
- camp_bank: cy 678-696.
- valley_loop: no heads.

## Scores (1-10)
| still | set density / ornament | lighting & colour | composition / framing | key-moment clarity | match to series level |
|---|---|---|---|---|---|
| 1 hill_over (hook) | 6 | 6 | 5 | 4 | 6 |
| 2 camp_bank | 4 | 3 | 3 | 2 | 4 |
| 3 valley_loop (reveal) | 5 | 3 | 5 | 5 | 3 |

Notes per still:
- **hill_over:**
  - Best of the three, and close to film 9/10 level in the middle distance: the camp, the bridge with a crossing column, foam-edged water and the castle rock.
  - The hook does not read. The eye lands on the bright central castle rock, not the bridge. The bridge is about 140 px long and about 10 px tall, with the knights at about 3-4 px. On the 360x640 phone sheet it is a brown line.
  - Two near-black tree trunks take about 25 % of the width at both edges.
  - The ground the Scots stand on is a carpet of orange/pink cobble blobs. It reads as rubble, not as Abbey Craig heather, gorse and crags, and it pushes magenta over 10 %.
  - The camera sits on a flat plateau. Shot 22 needs a slope to run down.
- **camp_bank:**
  - Cressingham's spot shows grass, three tents, a spear rack, a huge flagpole and a bald pink mound.
  - No river is visible. The bridge is a fence line at y about 660, half hidden behind the cards.
  - No Scots are on the hill, so he points at nothing (shots 11, 12, 18, 19, 25).
  - The sky is 45 % of the frame, with cold blue light, purple-shaded grass spikes, no long shadows and no warm sun.
  - Abbey Craig is a smooth pink dome with lollipop pines: no grey crags, no heather, no gorse.
- **valley_loop:**
  - The bottle/neck idea reads at phone size. Good.
  - It is drawn as a symbol, not a place:
    - a perfect circle on a straight, uniform navy band with a cyan glow outline and right-angled neck corners
    - a checkerboard field grid that dissolves into fog
    - pavilions seen as flat round beach-umbrella discs
    - scattered white cubes
    - two big dark cloud-shadow slabs across the camp
  - Abbey Craig is cut in half at the right edge, with no Scots on it, so the "cork" has nothing to come from.
  - The south bridge end and part of the camp sit in the caption band.
  - Film 10's reveal was rejected for being "far away and schematic". This is the same failure.

## Fixes the set builder must make (most important first)
1. **valley_loop: remove the haze, rebuild the distance.**
   - Kill the volumetric or mist fog over the land. Do aerial perspective with colour only: mix far terrain at most 25 % toward a pale blue-violet (hue 235-250) and keep silhouettes and edges crisp.
   - Target: Laplacian variance of the top band at least 40 % of the middle band (now 8.8 against 398).
   - Replace the checkerboard grid with irregular fields of 4-6 tints (green-gold, ochre, heather brown), plus hedgerows, tree lines, 3-5 farmsteads and lanes.
   - Pitch the camera to -55..-65 deg so the horizon sits at y <= 160 or out of frame.
2. **valley_loop: make the river a real river.**
   - Organic loop: not a circle. Use an egg or pear meander that narrows smoothly into the neck, with bank width varying ±20 % and no right-angle corners.
   - Remove the cyan glow outline.
   - Water layers:
     - deep teal centre (hue 185-205, not navy 225)
     - lighter turquoise shallows along the banks
     - broken white foam lines on the outer bends
     - a warm sun-glitter path (sparkle specks) across one stretch
     - V wakes trailing downstream of every bridge pier
     - current streaks
   - Banks get a 6-10 px mud or shingle strip and reed clumps.
3. **valley_loop: frame the reveal.**
   - Move or aim so the whole Abbey Craig (crags, pines, heather) is in frame upper right (x about 430-700, y about 250-560).
   - Put a visible Scots line on its lower slope: at least 30 figures, a dark band with light-catching spear tips.
   - Keep the bridge mouth or "cork" near frame centre (x 330-390, y 560-700).
   - Shift the frame so the river runs between y about 620 and 820 and the south bridge end and the nearest camp sit above y 870. The loop should span 65-80 % of the frame width.
   - Pavilions must read from above as peaked or conical tents: ridge or centre pole, scalloped valance, guy ropes, a pennant. Replace the white cubes with clustered bell tents, horse lines, carts and 3-4 campfire smoke columns.
   - Cloud shadows: at most 15 % darkening, soft-edged, and not covering the camp.
4. **camp_bank: put the river and the bridge in the shot (shots 7, 11, 12, 18, 19, 25 depend on it).**
   - Move the camera to the south-bank edge, 1.2 D high, so a band of teal water at least 70 px tall crosses the frame at y about 560-680, with reeds and mud at the near bank and a glitter path on the water.
   - Show the bridge full length in the left or centre third, about 260 px or more wide: plank deck, rails, timber piers standing in the water, and a few knights two by two on it.
   - Leave x 260-560 at the bridge's height clear of cast heads; put Cressingham at x 120-240 and Surrey right of the bridge.
5. **camp_bank: warm it and fill the camp.**
   - Light: a low warm key from the south-east, about 20-28 deg high, so long shadows cross the grass, with gold rim light on tents and figures. Shade stays blue-violet (240-260).
   - Colour targets: orange >= 22, red >= 28, blue <= 30, sat 0.38-0.46, val 0.50-0.62, dark 8-12 %.
   - Sky at most 30 % of the frame.
   - Grass: cut the triangular spike density by about 50 % and shade the spikes warm green-gold, not purple. Add a worn path, flowers, mud near the bank and tent pegs with ropes in the foreground.
   - Dress in view:
     - 4-6 pavilions (red/cream stripes, blue/gold)
     - 2-4 banners on poles with simple lions or chevrons, no text
     - a horse line with caparisoned horses
     - a cart, a weapon rack and a cooking pot on a smoking fire
   - Keep the big pole only as a deliberate 1-2 D foreground banner pole at the frame edge (x > 620) with its banner in frame (shot 18).
6. **Abbey Craig everywhere: build it as a crag, not a dome.**
   - A grey rock cliff face on the west/south-west side, with stepped outcrops.
   - Heather clumps in purple-brown (hue about 300-330 kept dark so magenta stays at or under 10 %, or shift them to brown 20-30).
   - Yellow-flowered gorse and irregular Scots pines (red trunks, flat dark crowns), not a lollipop row.
   - The same model must read from the camp (camp_bank, valley_river), from above (valley_loop, valley_wide) and from its own slope (hill_eye, hill_low).
7. **hill_over: make the far bridge the hook.**
   - Raise or move the camera up the slope and pitch it down -12..-18 deg so the bridge sits near frame centre (x 240-480, y 540-640), at least 240 px long, with knights readable two by two (each pair at least 8 px).
   - Move the castle rock off-centre (upper left third) and at most 70 % of its current size, so it stops competing.
   - Frame the bridge between two Scots' backs with spear shafts angled in (the shot plan wants spear shafts in the foreground).
   - Replace the two near-black trunks with one trunk at most 60 px wide on one edge, plus gorse and heather.
   - Replace the orange/pink cobble carpet with heather, gorse, crag rock and a path. Keep one grey boulder at most in the foreground.
   - Targets: magenta <= 10 %, orange >= 20 %.
   - The slope must visibly fall toward the bridge, 20-35 deg, with a run path for shot 22, where the lens rides down behind the charging Scots.
8. **Water rule across all river presets** (hill_over, camp_bank, valley_*, bridge_*, riverbank, river_low):
   - smooth layered water with foam lines, sun glitter and pier wakes, never flat polygons
   - for riverbank and river_low: water-level reeds, mud, shallow ripples, and room for spray-crown splashes (shots 29-31)
   - the bridge presets need trestle piers standing in the water with foam collars, and a deck exactly two horses wide (shots 2, 9, 26, 27)
9. **Life and density for the 31 shots.**
   - Every exterior preset has 12-18 distinct object types in view plus moving life: fluttering banners, 2-4 smoke columns, a few birds, swaying reeds and grass.
   - The Scots line along the lower slope (hill_eye, hill_low, valley_*) needs at least 40 extras with spears.
   - The English column on the bridge, the north causeway and the loop meadow must be settable by count (shots 15, 17, 20, 24).
   - Add Cressingham's money table (camp_table) with coin chest, scale, coin stacks and a ledger with no text.
   - Stirling castle rock with its small castle (as in still1) must appear in valley_wide.
10. **Cloud style (minor).** The lavender offset drop-shadow under each cloud reads as a pasted 2D sticker at phone size. Shade the cloud undersides instead, and keep clouds at most 30 % of any frame.

## Re-check criteria (re-render the same three presets plus the 360x640 phone sheet)
- All three stills: heads above y 880, shade hue 240-260, magenta at or under 10 %, dark share 5-15 %, orange at least 20 %.
- valley_loop: the top band is sharp (fix 1). A blind phone-size look shows "an army trapped in a river loop with one narrow bridge".
- camp_bank: water visible between the camp and the hill, and the bridge visible.
- hill_over: on the phone sheet the first thing seen is the bridge with knights on it.

## Re-check R2 (after the builder's re-render; NOTES.md read, numbers re-measured)

### VERDICT: APPROVE-WITH-FIXES
The builder may build the full set in this look and must apply the fixes below. I check them at the SET gate.
- Fixes 1-2 (the camp_bank bridge read and the camp_bank clutter) are **SET-gate blockers**.
- The rest must be in place at the SET gate, but a small miss there can go into the takes.

The R1 hard-rule breaches are gone:
- valley_loop is sharp (Laplacian variance, top band against middle, is 464/593 = 0.78), and the haze is now done with colour only.
- The river is an organic loop in a lit 3D valley, not a diagram.
- camp_bank now has the river between the camp and the hill.
- hill_over's hook bridge reads.

### Measured (stirling_hue.py; caption band excluded)
| still | red | orange | blue | violet | magenta | sat | val | dark | shade hue | sharp (Laplacian variance by band) |
|---|---|---|---|---|---|---|---|---|---|---|
| hill_over | 19.8 | 28.2 | 11.6 | 11.5 | 4.9 | 0.35 | 0.58 | 0.06 | 257.8 | 73 (sky) / 1114 / 812 / 803 |
| camp_bank | 15.5 | 32.3 | 33.3 | 9.4 | 5.3 | 0.29 | 0.60 | 0.06 | 251.8 | 165 (sky) / 1014 / 967 / 837 |
| valley_loop | 22.1 | 28.8 | 21.8 | 2.4 | 2.7 | 0.36 | 0.48 | 0.00 | 224.1 | 464 / 593 / 933 / 354 |

Heads (cy): hill_over 519-758, camp_bank 510-648. All are above y 880.

### Scores R2 (density / light & colour / composition / key moment / series level)
| still | density | light & colour | composition | key moment | series level | R1 |
|---|---|---|---|---|---|---|
| 1 hill_over | 7 | 7 | 7 | 8 | 7 | 6/6/5/4/6 |
| 2 camp_bank | 6 | 6 | 4 | 5 | 5 | 4/3/3/2/4 |
| 3 valley_loop | 7 | 6 | 7 | 7 | 6 | 5/3/5/5/3 |

Notes:
- **hill_over** is now a good hook. The bridge sits at frame centre, about 280 px long, with knights two by two readable on the phone sheet. The castle rock is off to the upper left and the camp is dense. The weak part is the bottom 40 %: a busy, dark spiky purple/orange sprig carpet (luma 62-68 in the bottom three eighths). The far mountain range is mottled pink/green noise.
- **camp_bank** has the river and the bridge, but the bridge is a thin line about 10-15 px tall (about 6 px on the phone sheet): no piers, no knights. There are also problems that read as errors:
  - white pyramid tents stand on the water surface at x about 140-340, y 515-565
  - about 20 black stubs (pegs?) 20-30 px tall are scattered over the meadow at x 250-620, y 580-900
  - two dark banner poles run the full height at x about 515-560 and split the frame in half
  - no Scots line is visible on the far hill, so Cressingham still points at an empty hill
- **valley_loop** now reads as the trap at phone size: a pear loop, the bridge at the neck, the English inside, the camp outside, and Abbey Craig with its crag upper right. Its problems:
  - The white parallel bars downstream of the bridge read as a zebra crossing.
  - The hill's camera-facing slope lies in its own shadow, so the 90-figure Scots line is a dark seam.
  - The bottom 35 % is a uniform carpet of about 230 identical white bell tents with identical shadows, which reads like scattered teeth or confetti.
  - The pavilions still read as beach umbrellas.

### Remaining fixes (most important first)
1. **camp_bank: make the bridge and the Scots read. BLOCKER.**
   - Bridge at least 35 px tall (deck, rails and piers in the water) and at least 300 px long.
   - At least 4 pairs of knights on it, each at least 10 px tall.
   - Do it by moving the camera upstream toward the bridge's south end (bridge at most 60-80 m away), or lens 28-32 with the bridge in the middle third, y 420-560.
   - The far-hill Scots line: at least 15 figures, each at least 6 px tall, lit, with light-catching spear tips. Cressingham must point at something.
2. **camp_bank: clean the frame. BLOCKER.**
   - Remove the tents standing on the water.
   - Shrink the black stubs to at most 8 px rope-and-peg pairs, or delete them.
   - Move the two centre banner poles to the right edge (x ≥ 640) as the foreground banner pole for shot 18, or drop one.
   - Replace about half of the spike grass with a worn bank path, mud and reeds at the water.
   - Bring sunlit red/cream pavilion faces into frame: red ≥ 25, sat ≥ 0.33.
3. **valley_loop wakes.** Replace the white parallel bars with one short V foam trail per pier, 30-60 px long, fading. No straight parallel strokes.
4. **valley_loop: the hill and the cork.**
   - Give the hill's camera-facing slope a fill light so its shade is at least 0.3 of the lit luminance.
   - The Scots line: a lit band of tan/ochre bodies 3-4 px tall with spear glints, readable on the phone sheet.
   - Reserve a clear north-bridge-end slot for the spear wall (shot 24), so the cork reads as a block at least 40x15 px.
   - Loop width 60 % → about 65-70 % if the frame allows (not a blocker).
5. **valley_loop camp.**
   - Cut the bell tents by about 40 % and group them into 6-8 clusters with lanes, horse lines, carts and fire rings.
   - Vary tent sizes and colours (cream, ochre, faded red), with no identical shadow rows.
   - Pavilions need a visible dark valance or side-wall ring and a centre pole and pennant, so from 50 deg they read as tents, not umbrellas.
6. **hill_over foreground.**
   - Thin the sprig carpet by about 50 % and mix in heather mounds, gorse, one rock and the run path.
   - Bottom three eighths luma 62-68 → 80-110. Violet 11.5 → at most 8.
   - Smooth the far range's mottled pink/green into 2-3 calm tint bands.
7. **Remaining presets for the 31 shots** (the R1 fixes 8-9 apply), at the SET gate:
   - bridge_deck, bridge_end_north and bridge_end_south: a deck two horses wide, piers with foam collars
   - bridge_high
   - riverbank and river_low: reeds, mud, ripples, splash room
   - camp_table: chest, scale, coin stacks, a ledger with no text
   - camp_wide, hill_eye, hill_low, valley_wide (castle rock with its castle), valley_river
   - settable English counts on the bridge, the causeway and the loop meadow
8. **Notes, not blocking:**
   - valley_loop dark share 0.001 and shade hue 224: accepted for this aerial; the teal river dominates the shaded pixels and the picture reads fine.
   - Red below 30 on the two ground stills: accepted if the real cast's red/gold surcoats and the pavilions bring it up. Re-measure at the SET gate.
   - Clouds still look a little like stickers: acceptable.
   - Placeholder stand points are fine. On hill_over the Scots stand on the ledge looking over to the bridge. In camp_bank, Cressingham is at x 178 on the bank and Surrey at x 640. Keep every extra on grass, not on the water's edge, once the camera moves.
