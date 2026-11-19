# QA_RECHECK s20 v2 (shots 20-24, THE REVEAL, g 1301-1683) -- TAKE gate, QA-art + tech -- VERDICT: FAIL

Checked: all 383 frames extracted; 6 fps plus every cut +-3 (1368, 1453, 1503, 1599) on 180 px and 360x640 phone tiles;
full size (540 px panels) on g 1307, 1317, 1322, 1332, 1347, 1362, 1383, 1413, 1433, 1458, 1478, 1498, 1523, 1558, 1590, 1640, 1658, 1672.
Sheets: scratchpad/rc20/p20..p24.jpg, f20*.jpg, f21..f24.jpg.

## QA_AUTO blur = FALSE POSITIVE (per-shot Laplacian, own numpy 4-neighbour kernel)
shot20 med 91 (63-170), 21 med 219 (166-257), 22 med 500 (297-629), 23 med 701 (163-850), 24 med 754 (693-881); take median 517.
Vs per-shot median <60 %: only g 1492 (bee-cloud gap) and 1503-1510 (wide opening of 23 before the swarm fills it). Frames crisp at full size. No blur issue.
Cuts clean and on plan. Heads above y 880. No black/frozen frames seen.

## v1 items
TECH 1 fat white wire ............ FIXED (thin grey rope, bow faintly visible; reads as a line on the phone)
TECH 2 chest push not on screen ... NOT (wire crosses her at ear/eye level, no V, she is out of frame by g ~1319)
TECH 3 / ART 1 shot 21 swing ...... PARTLY (roofs gone, near 2-3 hives swing hard with knocks + puffs g 1405-1445; far hives tiny; bottom ~40 % is foreground grass)
TECH 4 bees late / wrong source ... FIXED for timing (bees from g 1453); source still mostly behind the hive, not the entrance slit (minor)
TECH 5 density "thousands" ........ FIXED (fat cloud fills frame, sustained to the cut)
TECH 6 garland stripes on eye ..... FIXED (loose clouds; eye >= 90 % clear) -- but the cloud now sits on the EAR, not around eye/trunk
TECH 7 night elephant 23-24 ....... FIXED in 23-24 (graded, cool, contact shadow) -- NOT in shot 20 (see B1)
TECH 8 trumpet .................... PARTLY (mouth closed until ~1646, then open + squint; trunk raised behind the bee column, faint at full size, not readable on phone)
TECH 9 lantern pool ............... FIXED in 22; shot 21 foreground ground still hot orange (minor)
TECH 10 blue triangle ............. FIXED
ART 2 shot 20 contact point ....... NOT
ART 3 act the attack .............. PARTLY (wide eye g 1640, wince/open mouth 1654+; ears not clearly flared, no readable swat)
ART 4 roof undersides night grade . NOT (near-white peach in 1327-1367 and 1453-1502)

## Direct answers
- Mechanism on a phone: one wire YES (thin line threading posts); chest push NO; whole row swinging/knocking PARTLY (near hives only); bees bursting YES.
- Bees over her face: NO, not too much; eye reads in every frame. They overload the ear instead; "around the eye and in the trunk" is weak.
- Trumpet: PARTLY -- open mouth + squint read, raised trunk does not on phone.
- Shot 20 elephant night-tinted: NO -- same flat bright grey + bright pink blush as v1; brightest shape in frame.
- Shot 21 bottom 40 % grass: YES (~38-40 %, warm-lit foreground blades; hives in a band at y ~40-58 %).

## Blockers (4)
B1 g 1301-1319 (shot 20): elephant card not night-graded. Fix: same grade as 23-24 (x0.70, tint 0.78/0.82/1.0, cool rim, blush down 50 %).
B2 g 1313-1326 (shot 20): a detached grey trunk (striped tube with nostril tip) floats along the wire right of the hive, separate from her head
   (head shows no trunk). Reads as a severed trunk. Fix: draw the trunk on the card attached to the head, or hide the separate trunk object.
B3 g 1307-1367 (shot 20): the push is not shown -- wire at ear height, no V/bow at her chest, she leaves frame by ~1319, then 45 frames of
   poles/roofs with ~45 % sky and bright peach roof undersides. Fix: wire at chest height with the V clearly bent toward camera, hold ~12 frames
   on chest+V, then slide with the bow travelling; tilt down (sky <= 25 %), darken/cool roof undersides 35-40 %.
B4 g 1368-1452 (shot 21): row wave only reads on the 2 near hives; ~40 % of frame is foreground grass. Fix: raise/tilt camera so grass <= 15 %,
   hives fill the middle 50 %, far hives >= 120 px, keep the 0.7 rad swing + knock puffs; dim the orange ground.

Non-blocking: in 23-24 move ~1/3 of the ear cloud into a ring round the eye and a stream up the trunk; keep trunk silhouette clear at 1650-1665 so the
trumpet reads; bees in 22 should leave from the entrance slit.
