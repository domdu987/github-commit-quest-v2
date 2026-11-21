# QA_TECH s10 ROUND 3 (shots 24-26, g1336-1520, e6fe1c2) -- FAIL (2 blocking)
Method: all 185 frames extracted; Laplacian variance, frame diff and box luma measured; about 26 frames viewed full size (g1336, 1340, 1345, 1355, 1366, 1372, 1373, 1375, 1376, 1390, 1405, 1412, 1420, 1430, 1440, 1449, 1456, 1466, 1481, 1500, 1516) plus 4 six-frame montages (1342-48, 1369-80, 1381-1404, 1406-19, 1442-57).
Rhythm 8.69 / 20.06 (target >= 4 / >= 12): pass.

## Team claims
| Claim | Verdict |
|---|---|
| HEAD: beam across brow y600-640, jaws at skull width, ears drawn, tighten g1343-46 | TRUE. Beam at y~600-640 at g1355 and g1366 (R1/R2 blocker fixed). Right jaw hangs at the skull edge, ears drawn. A visible jump and push at g1343-44 (diff 23/28). Caveat: no hand is visible on the bar after g1342 (see S1). |
| BOXES: 6 same-size boxes in frame and lit at g1420, off hard 1422/26/30/34/38, hero stays lit | PARTLY. 6 near-equal boxes, all in frame, all lit at g1420: yes (the hero lid is clear glass, a little different). Off events at g1422 (box E), 1426 (D), 1430 (C), 1434 (B), ~1428-36 (A, an 8 f fade, not hard). Hero stays lit (luma ~120). **Brightness measured: lit 96-122 (A 96, B 99 fall just short of 100); OFF boxes measure 61-78, not <=35** (g1430 off boxes 61-78, g1440 63-76). They read as dim purple, not dark. FAIL on the off target. Also the camera moves from g1430 and boxes crop at the left edge from ~g1432. |
| LID lifts g1442-57, attached to the front edge | TRUE for g1442-49: the glove grips the lid front edge and the lid tilts open (g1449). FAIL after: from g1451 the lid is gone (vanishes between 1449 and 1451) and the empty hand rises away (1454, 1456). |
| FINGER insert g1406-19: close-up, one finger between the jaws, calipers in Bertillon's hand | FALSE. It is still a medium two-shot (frame is about 720 px wide, Dupont's arm ends in a ~40 px pink tube/mitten). Calipers ARE in Bertillon's blue-sleeved hand, but the jaws hang at his own waist (x~230-260, y 650-720 at g1412/1417) and never close on the tube. No finger is between the jaws. Not a close-up. |
| WHIP: smear only g1373-75, g1372/1376 sharp | TRUE. Laplacian: g1372 82, g1373 7, g1374 15, g1375 6, g1376 109 (clean). Viewed: 1373-75 are heavy streaks; 1372 (stove room) and 1376 (card-wall room) are readable. 3 smeared frames. Cut 1374/1375 is inside the smear. |
| DRAWER: pull sway, beard above y880 | TRUE. Drawer slides open g1381 -> 1394, hand on the knob (g1384, 1390, 1405), Bertillon leans back. Beard bottom ~y775 (g1390), ~y830 (g1405). Limit 880 respected. |
| CARD rises g1476-1500, slightly cropped right by g1516 | RISES: true (g1481 low in the box, g1500 well above, g1516 ~320-590). CROPPED: not so. At g1516 the card is fully in frame (x 155-560 of 720). Nothing wrong with that. The card floats with no hand (same as R2). Not blown (0 % >= 248, mean luma 207-212), portraits and tally readable. |

## Blur
Metric FAIL is a false positive.
- g1479-87 flagged: Laplacian 154-231, viewed g1481 sharp (camera pull-out only). Waived.
- 1420-1458 and 1475-1520 (low-texture dark/records): sharp. Waived.
- Real blur: g1373-75 only (3 f). <=3: pass.

## Blocking
B1. g1430-1441 (and 1420-1441 overall): the "off" boxes are only dimmed to luma 61-78 (target <=35), so the narrowing-down beat reads as a dim, not a switch-off. Brightness must drop to <=35 on g1422/26/30/34/38 (the A box should also go off in one frame, not a fade over ~8 f), and B (99) and A (96) should be raised to >=100 at g1420. Also keep all boxes inside the frame through g1441 (the left boxes crop at x<0 from ~g1432).
B2. g1406-1419 finger insert: not done. Make it a close-up (hands + jaws filling >= 40 % width), with the jaws closed on one finger and the calipers visibly in Bertillon's hand. Currently the jaws hang by Bertillon's waist (g1412, 1417: x~230-260, y~650-720) and no finger is between them.

## Should fix
S1. g1346-1368: no hand is visible gripping the caliper bar (g1355, g1366). It reads as floating, held only by the tight framing. Show Bertillon's hand at the bar or its stem.
S2. g1451-1457: the lid disappears and the hand rises empty. Carry the lid (hand holding the front edge) or leave it visible standing/tilted on the box. Glove is also clipped white (63 % of pixels >= 248 at g1449); tone the glove down.
S3. g1484-1520: the card floats about 80-100 px above the box with no hand. Acceptable as a magic rise but a hand or a visible lift would be better.
S4. g1476-1481: the camera pulls out (the plan wants a push-in). Minor.

## Checks that pass
- No see-through cards, no beam shafts, no leftover geometry (only the drawer's small white foot stop at ~(195,910) g1420-30, which is part of the drawer).
- Dust 0.4 (shot.py set_dust 0.4) <= 0.5.
- Chins above y880: Bertillon 775-830, Dupont lower than that nowhere.
- No mouths moving. Not seen in any viewed frame.
- No frozen holds: min diff outside cuts 2.6 at g1475 (single frame). No black or magenta (min mean luma 84, QA_AUTO magenta 0.0 %).
- Cuts at 1374/1375 (inside the whip), 1406, 1420, 1459, 1474 are real (diff 55-67).
- Ear insert g1459-73 is good: bar across the ear, held by a hand at left.

## Verdict: FAIL
Blocking B1 (off boxes not dark, <=35), B2 (finger insert not a close-up, finger not in the jaws). Should-fix S1-S4. Fixed since R2: head calipers (R2 B2), whip trimmed to 3 f (R2 B1), drawer pull, lid grip, 6 same-size boxes.
