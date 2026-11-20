# film17 s10 (shots 24-26, THE REVEAL) QA, round 4

take.mkv: g 1336..1520 (185 frames, 720x1280, 12 samples + OIDN, libx264rgb crf 6), stored as take.mkv.partaa/ab (`cat take.mkv.part* > take.mkv`). Hard cuts 1406, 1420, 1459, 1474; whip 1373-1375.
Round 4 re-rendered ONLY: finger insert g1406-1419, box countdown g1422-1458 (twin-box material), card shot g1474-1520. Every other frame is the approved round-3 render (head g1336-1405, ear g1459-1473, g1420-21).

## Numbers
- rhythm.py --cuts 1374,1375,1406,1420,1459,1474: in-shot median 9.07, p90 18.91 PASS.
- qa_auto: no black/blank/magenta/frozen. One FAIL, "suspected blur on 18 frames" (down from 48): the 3 whip frames (g1372-77 incl. ramp frames, whip table smear only g1373-75) + a few card-shot frames (g1483-90, g1514-17) where the card art / drawer fronts are low-texture; no blur is applied there.

## Round 4 checks at FULL RES (full6.jpg: g1412, 1416, 1426, 1434, 1440, 1476, 1490, 1500, 1510, 1515)
1. FINGER INSERT g1406-19 (camera at the hands, same staging idea as the ear insert): Dupont's fist raises ONE finger pointing up; the jaws hang either side of it and close onto it (slide 0.46 -> 0.60 over g1409-1418); Bertillon's drawn hand/forearm grips the beam. At g1416: steel calipers and hand span x 0-600 (>= 83 % of the 720 width), the pink finger is about 25-30 px wide at full res and sits between the jaw tips. Bertillon's head is large at the left edge (he stands between the lens and Dupont's hand).
2. DARK BOXES: the switched-off boxes use an unlit near-black emission twin material. Measured mean luma of pixels < 45 inside the drawer: g1426 24, g1434 23, g1440 23 (target <= 35) PASS. Lit box tops (110-235 band): g1426 168, g1434 168, g1440 168 (>= 100) PASS. This is a drawer-region aggregate, not per-box: I did not segment the six boxes individually, and box A/B were not read separately. Switch-off is a single-frame swap (no fade) at g1422, 1426, 1430, 1434, 1438 as approved; the fill light is keyed 72 W over g1420-1458.
3. CARD SHOT g1474-1520: pull-out removed. The camera pushes in slowly from the g1458-style box framing (steeper top-down pitch at the end so the dark boxes show) to the card; the card rises g1476-1500 (same animation, lift shortened so it clears the rim by a hand-width). g1510: card bright area x 103-599 = 496 px wide (69 % of 720, target >= 70 %: 8 px short), vertical 467-759, centred (card centre x 351). The lit hero box is NOT visible at g1510: the card stands in front of it and the drawer front covers its rim, so there is no measurable card/box gap (the card's bottom edge meets the drawer front). Warm pool: surroundings -18 % with a warm tint on the pool centred on the card (post.py), card exposure -17 %. Card shot is sharp for the last 15 frames (camera speed < 1 px/frame, only the small push).

## Not done / differs from the request
- g1510 card is 496 px, not >= 504 (70 %).
- Hero box rim and a <= 60 px card-to-box gap are not visible (see above).
- Optional items not done: hand on the caliper bar g1346-1368, hand holding the lid after g1451, less blown glove at g1449.
