# QA-art R2, film 17 take s10 (THE REVEAL, shots 24-26, g1336-1520, commit acdfec4, render17/team9): FIX-FIRST

Reviewer: QA-art (opus), TAKE gate for a key shot. The client delegated approval to QA, so this verdict decides the take.
How I reviewed: phone_sheet.jpg first, then 360x640 strips of every f6 frame, then full res at g1366, 1411 (crop), 1420/1446/1451, 1516.
I also measured Laplacian sharpness and box luminance myself.
Rhythm: 7.26 / 17.08 against a target of >= 4 / >= 12. Pass.

## The team's claims checked against the frames
| Claim | Frames say | |
|---|---|---|
| g1336-66 "calipers settle on Dupont's skull" | **False.** The caliper bar is horizontal at y~820-900 full res (g1366): across Bertillon's chest and below Dupont's chin. It never touches a head. This is the same as round 1, and R1 fix #2 was not done. | FAIL |
| Whip g1367-83 | Better. Laplacian is 6-15 on g1372-1376 (5 smeared frames). g1371 (23) and g1377 (27) are soft but readable, and g1378 (62) is clean enough. Round 1 had 9 frames, so this is a real improvement but still over the 3-frame allowance. | minor |
| g1376-1405 "yanks the big drawer, which holds six lit boxes" | The drawer is a strip at the left edge (x 0-260, y ~560-760) under Bertillon's outstretched arm. He faces camera and points, and the drawer barely moves. No boxes are visible in this shot at all. | weak |
| g1406-19 finger insert | It exists, but it is a medium two-shot, not an insert. Dupont's "finger" is a 40 px round mitten-fist, and the caliper jaws float beside it (g1411 crop). At phone size it reads as "Dupont holds his arm out", not as a finger being measured. | weak |
| g1420-58 "boxes go dark one by one until one lit box remains" | **Not what is on screen.** At g1420 there are only 3 boxes. Two small ones sit cropped at the left edge (x 60-360). They are **never lit**: mean luma 65 and 54, against 112 for the hero box. The hero box is lit and about twice their size from frame 1. Their "going dark" (65 -> 37) is invisible at 360x640. A viewer sees one glowing box from the start, not a search that narrows. | FAIL |
| Lid lift g1442-57 | The hand reaches in, and at g1451 the lid is simply gone while the empty hand rises. This reads acceptably at speed. Nit: the glove is white, while Bertillon's hand at g1411 is pink. | ok |
| g1459-73 ear insert | **Good.** The big ear is clamped between the caliper jaws (g1466-1473) and reads instantly at phone size. This is the model the other two steps should follow. | PASS |
| g1474-1520 card rises | **Good.** The card is sharp: Laplacian 210-231 at g1501-1516, with no blown pixels (0 % >= 248). Hand, fingerprint and both mugshots are readable at phone size, and it lifts out of the one lit box into a warm pool. Still a pity: the camera *pulls out* g1476-1481 (the plan says push-in 9 %/s), and the card ends at only 65 % of frame width, floating ~90 px above the box. | PASS, polish |

## What a first-time phone viewer gets now
- **Ear -> one card:** lands, and it is the most satisfying 2 s of the take.
- **Finger -> one box:** half lands. "One box" is clear because there is only ever one lit box, but it is never "one box *left*".
- **Head -> big drawer:** does not land. There is no head measurement, and the drawer is a sliver behind a pointing man.

The three-step "measure X -> fewer left" rhythm only becomes visible on step 3. The payoff works, but the build-up to it (the *system*) is still mostly told, not shown.

## Scores (1-10, R1 -> R2)
| Area | R1 | R2 | Notes |
|---|---|---|---|
| Mechanism clarity (phone) | 4 | **5** | Ear 8, card 8, box 5, finger 4, head 2, drawer 4. |
| Key image / beauty | 7 | 8 | The card rising into the light, and the glowing box in the dark drawer. |
| Acting | 5 | 5 | Faces are good. The calipers miss the head, and the "yank" is a point. |
| Set density | 8 | 8 | Unchanged and rich. |
| Light / colour | 8 | 8 | Warm pools against blue-violet shadow. The card is not blown. The rim light is not needed. |
| Camera | 6 | 6.5 | Whip shorter. The drawer shot still frames Bertillon, and the card shot pulls out against the plan. |

## Verdict: FIX-FIRST
This is close. The payoff (ear + card) already works. What fails is the build-up, steps 1-2, which is what makes the payoff earned. Fixes in priority order:

1. **Head: calipers ON the skull (re-render g1336-1373; same set and camera; R1 fix #2, still open).**
   - Open the jaws front-to-back across Dupont's head: one tip on his forehead at about x 380 / y 640 full res (g1366), the other at the back of his skull at about x 640 / y 600.
   - Raise the bar to y ~560-620. It is at y ~830 now.
   - Hold contact from g1350 to the whip. Do the 2-3 frame tighten on "ระดับนี้".
   - Copy the ear-insert staging (g1466), which already works.
2. **Make "only one box left" visible (re-render g1420-1441).**
   - At g1420, show 5-6 boxes of the **same size** fully inside the frame. Pull the camera back or slide right so nothing is cropped at x < 40.
   - **All of them warm-lit**, with box-top luma >= 100, the same as the hero.
   - Switch them off one at a time, about every 4 frames (g1422, 1426, 1430, 1434, 1438), each dropping to luma <= 35 (a hard light-off, not a fade).
   - The last lit box is the hero, and the lamp pool stays only on it.
   - Fallback with no re-model: scale the existing two small boxes up to the hero's size and light them for g1420-1428 before they go dark.
3. **Finger: make it a real insert (re-render g1406-1419).**
   - Frame Dupont's hand and the jaws to fill >= 40 % of the frame width (about 300 px or more at full res). Today the jaws are about 40 px.
   - Give the hand one extended middle finger, a separate shape at least 18 px wide, with the jaws closed on it.
   - Same rule as the ear: the body part plus the calipers *is* the picture.
4. **Whip: trim to 3 smeared frames (post only).** Smear only g1373-1375. Make g1372 a sharp or eased frame from the measure room, and g1376 the sharp drawer-room frame. Today g1372-1376 all have Laplacian <= 15.
5. **Drawer (g1381-1405), should-do.**
   - Slide the camera or Bertillon ~0.5 D right so the drawer front sits at frame x 120-420 and is not cut off at the edge.
   - Show it slide out >= 150 px over g1381-1395, with Bertillon turned toward it in a lean-back pull pose.
   - If budget is short, do 1-4 first. With 2 done, the drawer interior carries the beat anyway.

Non-blocking polish (card_hero):
- Replace the g1476-1481 pull-out with a slow push-in so the card ends at >= 80 % of frame width by g1510.
- Hold it sharp for >= 15 frames to the cut.
- The warm rim light and the "ระดับนี้" tighten (folded into fix 1) are optional beyond that.
- Continuity nit: Dupont has no visible ears in g1336-1366 but large ears from g1406. Nobody will mind at phone speed, but make it consistent if fix 1 re-renders shot 24 anyway.

Re-check after fixes:
- Head and finger read as "measuring that body part" on the 360x640 sheet.
- At g1420 a phone viewer can count several lit boxes, and by g1440 one.
- qa_auto blur list = 3 whip frames plus <= 2 per snap.
