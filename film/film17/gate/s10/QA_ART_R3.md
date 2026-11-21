# QA-art R3: film 17 take s10 (THE REVEAL, shots 24-26, g1336-1520, commit e6fe1c2, render17/team9): FIX-FIRST (2 fixes, both small)

Reviewer: QA-art (opus), TAKE gate for a key shot. The client delegated approval to QA, so this verdict decides the take.

How I reviewed:
- I checked the claims against the frames, not against the team's QA.md.
- I looked at phone_sheet.jpg first.
- I extracted all 185 frames from take.mkv and checked that they match f6/.
- I built 360x640 strips for each beat: head, whip, drawer, finger, boxes (every frame from g1420 to 1427, then every 1-4 frames), lid, ear and card.
- At full res I looked at g1345, 1360, 1366, 1412 (crop), 1420/1438/1441, 1448/1451, 1480 and 1512.
- I measured these myself: Laplacian variance and mean luma on every frame, box-top luma, and the card's bounding box.

Rhythm: 8.69 / 20.06 against a target of >= 4 / >= 12. Pass.

## Claims against the frames
| # | Team claim | What the frames show | |
|---|---|---|---|
| 1 | Head: beam across the brow, jaws at skull width, tighten at g1343-46 | **Mostly true.** The beam lies across Dupont's head at y ~600-630 (g1360-1366), and the far jaw hangs just behind his ear at x ~690. At phone size it reads as "a tool across his head", which is a real improvement over the chin bar. Nits: at g1343-1349 the bar is at eye level, so it covers his eyes like a blindfold. Bertillon's hand is at his chest (x ~230 / y ~900), so the calipers float with no hand on them. Bertillon's pince-nez cord runs down Dupont's face (x ~455). None of this blocks. | OK |
| 2 | Six same-size lit boxes, hard off every 4 frames to the hero box | **True, and it is the best new image in the take.** g1420 has 6 equal boxes, all lit, all in frame (box-top luma 95-127). They go off hard at g1422, 1426, 1430, 1434 and 1438, and at g1438 five are dark (61-77) with the hero lit (132). The dark boxes are not <= 35, but they lose their cream rims and turn purple, so the count reads at 360x640. A phone viewer sees 6 become 1. | PASS |
| 3 | Hand lifts the lid g1442-57 | Mostly true. The hand is on the lid at g1444-1448, and the lid swings open. From g1451 the hand floats ~50 px above the lid edge instead of holding it. Reads fine at speed. | OK |
| 4 | "Close finger insert" | **False.** g1406-1419 is still a medium two-shot: Bertillon is full figure, from head to shoes. The calipers are ~150 px wide (x 120-300, y 620-700). The "finger" is a 110x30 px pink capsule at x 300-420 / y 610-650, sitting *above* the bar, and the jaws hang below it, not closed on it. At phone size it reads as "he measures Dupont's outstretched arm". R2 fix 3 is not done. | FAIL |
| 5 | Whip smear on 3 frames | **True.** Laplacian: g1372 82, g1373 7, g1374 15, g1375 6, g1376 109. Smear is on exactly 3 frames. | PASS |
| 6 | Bertillon pull sway on the drawer | **True.** The drawer front is visible at x 0-260, Bertillon grips the handle and leans back, and the drawer slides out clearly over g1384-1398. Still near the left edge, but it reads as a yank. | PASS |
| - | Card shot (not in the claims, but changed: "camera moved") | **Regression.** g1474-1486 is now a bigger pull-out (the drawer handle shrinks ~40 %), against the plan's push-in 9 %/s. The card ends at 380-398 px wide (53-55 % of the frame) at g1512-1515, against 65 % in R2. It floats ~110-120 px above the box rim (card bottom y ~583, rim ~700). There is no real lamplight pool: shot luma drops to 85-90. The portraits and hand still read at phone size from g1500, and the card is sharp (Laplacian 210-250). But the film's payoff image is smaller and cooler than last round. The qa_auto blur hits at g1479-1487 come from this pull-out. | WEAK |
| - | Ear insert g1459-73 | Unchanged from R2 and still reads at once. | PASS |

## What a first-time phone viewer gets now
They get head -> drawer -> (arm) -> **6 lit boxes becoming 1** -> lid -> ear -> card. The narrowing is now *seen*, which was the core R2 failure, and the box countdown carries it.

Two things are left:
- The finger beat reads as "arm" and is too small to register as its own step.
- The payoff card is a smallish white rectangle floating in a dim wall of drawers instead of "one card rising into the lamplight".

## Scores (1-10, R1 -> R2 -> R3)
| Area | R1 | R2 | R3 | Notes |
|---|---|---|---|---|
| Mechanism clarity (phone) | 4 | 5 | **7** | Boxes 8, ear 8, head 6, drawer 6.5, lid 6.5, card 6.5, finger 3. |
| Key image / beauty | 7 | 8 | 7.5 | The new box countdown is lovely. The card is weaker than in R2. |
| Acting | 5 | 5 | 6 | The drawer pull works. The calipers float with no hand on them. |
| Set density | 8 | 8 | 8 | Unchanged. |
| Light / colour | 8 | 8 | 7.5 | The lit/dark boxes are great. The card shot is dim, with no warm pool on the card. |
| Camera | 6 | 6.5 | 7 | The whip and drawer are fixed. The card shot still pulls out against the plan, and more than before. |

## Verdict: FIX-FIRST
Only shots 25a (finger) and 26 (card) need re-rendering. Everything else is accepted as it is: head, whip, drawer, boxes, lid and ear. Do not touch them, and I will not re-review them.

### 1. Card shot g1474-1515: restore the payoff (camera and lamp only; same animation)
- Remove the g1474-1486 pull-out. Start at the g1458 framing (the open hero box, close), and push in slowly at ~6-9 %/s while the card rises.
- **Target at g1505-1515:**
  - The card is >= 500 px wide (>= 70 % of the frame), centred at x ~360, with its centre around y 450-550.
  - The top edge of the hero box and its rim are still in frame below it, so the viewer sees *where* it came from.
  - The gap between the card's bottom and the box rim is <= 60 px at full res. Lower the card's end height, or tilt the camera down; either is fine.
- Light: aim the existing 20 W card lamp so the card and the open box sit in the one warm pool. The surrounding drawers should be ~15-20 % darker than now (shot mean luma ~75-80), not the card. Keep the card unblown, with < 1 % of pixels >= 248.
- Keep it sharp for >= 15 frames to the cut.

### 2. Finger g1406-1419: a real insert (re-render 14 frames, camera plus one rig fix)
- Put the camera at the hands. The calipers, Dupont's hand and the finger should fill >= 300 px of width (>= 40 %). The pivot of the current shot is around x 300 / y 650 full res.
- Bertillon's face may be out of frame. The body part and the calipers *are* the picture, as in the ear insert g1466.
- Move the jaws up ~25-30 px so the finger capsule sits **between** the two tips (today it lies above the bar), and close them 2 frames before the cut.
- Fallback if a camera move is impossible: render this shot alone at 2x (1440x2560) and crop to the hands. Do not upscale the current 720 frames.

### Non-blocking (do only if you are re-rendering anyway; I will not hold the take for them)
- g1343-1349: raise the caliper bar ~20 px so it is not over Dupont's eyes.
- Shot 24: put Bertillon's hand on the caliper beam.
- g1451-1457: keep the hand on the lid edge (it is now ~50 px off).
- Dark boxes: they are at luma 61-77, not <= 35. They read anyway, so leave them.

### Re-check for R4 (shots 25a and 26 only)
- At 360x640, the finger beat reads as "finger between calipers", not "arm".
- At g1510 on the phone sheet, the card fills most of the width, sits just above its glowing box, and reads as the brightest, warmest thing on screen.
- The qa_auto blur list has no card-shot frames left.
