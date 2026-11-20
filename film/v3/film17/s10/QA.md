# film17 s10 (shots 24-26, THE REVEAL) QA, round 3

take.mkv: g 1336..1520 (185 frames, 720x1280, 12 samples + OIDN, libx264rgb crf 6), stored as take.mkv.partaa/ab (`cat take.mkv.part* > take.mkv`). Cut-in g1342, cut-out g1515, 6 handle frames each side. Hard cuts: 1406, 1420, 1459, 1474; whip (location change) 1373-1375.

## Numbers
- rhythm.py --cuts 1374,1375,1406,1420,1459,1474: in-shot median 8.69, p90 20.06 (targets >= 4 / >= 12) PASS.
- qa_auto (same cuts): no black/blank/magenta/frozen. One FAIL "suspected blur on 48 frames": the Laplacian-vs-median metric on the dark records frames (waived by the director as a metric artifact) + the 3 whip frames. Smear exists on g1373-1375 ONLY (post.py WHIP table 40/44/40 px); g1372 and g1376 are sharp.

## Round 3 fixes, verified against full-res frames (full6.jpg: g1360, 1412, 1420, 1426, 1434, 1440, 1450, 1372, 1373, 1375, 1376, 1510)
1. HEAD g1336-73 re-rendered. Cause of the earlier "bar at his chin" was an unclamped ease (the tip target sank after g1350). Now the calipers (prop scale 1.35, jaws open to the skull width) rise and lie across Dupont's brow with the beam at y ~ 600-640 (g1360 checked) and the far jaw at the right edge of the head, held by Bertillon's hand to the whistle (no sinking). Dupont's ears drawn. 2-3 frame tighten on "ระดับนี้": a small push-in kick g1343-1346 + jaws squeeze. NOT verified: the exact tip pixels you named (x380/y640, x640/y600); the near tip is hidden behind Bertillon's head in the 3/4 view.
2. BOXES g1420-41: six boxes of the same size (the hero box is scaled to match) on a ledger slab, all in frame, all lit at g1420 (checked by eye, bright pale tops), switched to dark ones hard at g1422, 1426, 1430, 1434, 1438 until only the hero box (front right) stays lit. NOT measured numerically against your brightness thresholds (>=100 / <=35); my spot-sample was not reliable.
3. BOX LIFT: the hand enters g1430-1442 and the lid opens g1442-1457 with the hand attached to the lid's front edge (position computed from the hinge geometry each frame); g1450 shows hand + lid rising. The box itself does not leave the drawer.
4. FINGER INSERT g1406-19 re-rendered: close camera on Dupont's outstretched arm, one extended finger drawn between the jaws (hand_for_anchor jaws pinned to the finger tip), calipers gripped by Bertillon's drawn hand/forearm. Hand + calipers + finger span roughly half of the frame width at g1412 (checked), finger about 45 px wide at full res.
5. WHIP: smear on g1373-75 only, sharp g1372 and g1376 (checked, g1372 = the stove, g1376 = records room). g1369/70 have no blur (the pan itself starts there).
6. DRAWER YANK: Bertillon steps back only 0.22 m (beard margin), leans back harder with a pull sway g1376-1405; drawer slide 0 -> 0.78 m over g1376-1398; framing shifted so his head does not cover the drawer. Beard above y 880 NOT re-measured on every frame.
- Card shot: camera moved to see the hero box and card, card lamp 20 W + post exposure -17 % + paper +10 %; the card rises g1476-1500 from below the rim (g1478 checked: hidden), portraits and bottle read at g1510. Card is cropped slightly at the right edge at g1516.

## Not done
- Warm rim on the card; card held by a hand/resting on the box; dark boxes +5-10 %.
- Exact brightness numbers for the box countdown; exact tip pixels in the head beat.
