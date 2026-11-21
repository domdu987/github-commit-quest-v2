# QA_TECH s10 ROUND 2 (shots 24-26, g1336-1520, acdfec4) -- FAIL (2 blocking)
Method: all 185 frames extracted from take.mkv; per-frame edge density and frame-diff measured; about 40 frames viewed (montages plus full-size pairs g1360/1366, 1384/1405, 1411/1419, 1420/1426, 1436/1457, 1459/1473, 1474/1484/1500, 1446/1450/1454/1520).

## Blur verdict (by eye)
- g1420-1427 and the rest of the flagged 1420-1458 range: SHARP. Crisp ink outlines on drawer, box, tabs and carpet at 1420, 1426, 1436, 1446, 1450, 1454. The metric flag is a low-texture artifact. Same for the card frames g1475-1520 (1484, 1500, 1520 sharp). The team is right here. No defocus anywhere.
- The team is WRONG that the whip smears only 3 frames. Measured edge pixels are 0.00 % on g1371-1377 (7 frames), 0.64 % at g1378, 1.13 % at g1370. Viewed: 1371-1374 are horizontal streaks, 1375-1377 heavy defocus/mush (wall, stove and table unreadable), 1378 still soft. That is about 8-9 smeared frames (0.3 s), as in round 1. Sharp-to-smear pop 1369 -> 1370 (frame diff 42 -> 60) is unchanged. Client rule is 1-3 frames.

## Round-1 items
| R1 | Status |
|---|---|
| 1 whip smear 9 frames | NOT FIXED (BLOCKING) |
| 2 calipers on Dupont's head | NOT FIXED (BLOCKING) |
| 3 yank | Partly. Hand grips the ring (g1384 hand at ~(165,655); g1405 ~(840,745)), drawer ajar. But the drawer is already open at g1384 and Bertillon is a near-static pose g1384-1405 (22 f). No visible pull. |
| 4 cut at 1406 | FIXED (hard cut at 1406, diff 55) |
| 5 box lift / lid | Partly. A hand and sleeve enter (g1446 hand on box, 1450-1457 hand rising away) but the lid never lifts and the box never moves. Nothing is lifted. |
| 6 finger/ear inserts | PRESENT. Finger g1406-1419, ear g1459-1473. Ear reads well (jaws across the ear, g1473). Finger: see below. |
| 7 one lit box | FIXED. Others go dark; one warm box remains g1420-1473. |
| 8 card exposure/rim | Exposure OK (portraits and tally readable at g1500, 1520). Rim light not done (team admits). |

## Blocking
B1. Whip g1370-1378 (peak 1371-1377, full-frame, 0 edges). Needs <=3 smeared frames. Ramp with displaced sharp frames; cut the pan to ~8 f total or hard-cut with a 2-3 f streak. Also soften the 1369->1370 pop.
B2. Shot 24 g1336-1367: the calipers are NOT on the head. g1360: bar at y~735-870, x 0-300, in front of Bertillon's chest and below Dupont's chin. g1366: bar y~820-870, x 725-1040 (in the pair image: Dupont's face spans y 600-880, so the bar sits at his chin). It never spans the skull (head is y ~560-880 on Dupont). Beat "calipers on head, 0.8 s" is not visible, so "head this long" has no picture. Fix: raise the jaws to Dupont's head height (front-to-back across the cap/skull) and hold contact. The 2-3 f tighten on "ระดับนี้" is also not done and cannot be seen.

## Should fix
S1. Finger insert g1406-1419: the calipers (silver, ~(215,690) at g1415) sit behind Dupont's brown fist and the blue-sleeved arm with its cuffed hand points away to the far left (~(40,690)). The calipers are not visibly gripped, and no raised finger is measured. Put the jaws visibly on the finger, hand gripping the bar.
S2. g1446-1458 lid/box: the hand arrives and leaves but the lid does not follow it, and the box stays closed and static. Lift the lid with the hand, or lift the box. The "hand following the lid edge" check fails: the hand at g1450 (x~730-800,y~230-320 in the 2000 px montage) is a hand above the box with a gap.
S3. g1484-1520 card: it floats about 80-100 px above the box (g1500, g1520: card y~250-340 in the 1182 px view, box top below it) with no hand. It reads as a magic rise, which is OK for "card rises", but it is not held. No rim light on the card (team note). Lamp bloom is still flat.
S4. g1384-1405: Bertillon is almost still, with a slow push. Add a visible pull (drawer closed at 1384, a few frames of arm motion).
S5. Phone size: the dark boxes (g1426-1473) are bluish-black at left of the lit box; they stay readable but low contrast. The lit box is the clearest object. Lifting them slightly (5-10 %) would help. Not blocking.

## Checks that pass
- Calipers held: g1360/1366 held by Bertillon's hand at his chest (hand ~(150,885) at g1360). Ear insert g1459: held by a pale hand at left (~(30,880)); g1473 the bar is across the ear.
- Hand on the drawer: yes, g1384 and 1405 (hand on the ring).
- No see-through cards. No beam shafts on characters (shot.py hides the beam_fx materials). Dust 0.4 (set_dust 0.4) <= 0.5.
- Chins: Bertillon's beard bottom ~y865 at g1405 (limit 880, no margin; do not lower him). Dupont's chin y<=850 at g1473. Others lower than that: none. OK.
- No frozen holds: minimum frame diff 1.92 outside cuts, no run <0.1. Longest quiet stretch g1475-1476 is 2 f. No black frames (min mean luma 68), no magenta (QA_AUTO 0.0 %).
- Mouths: nobody speaks; no mouth motion seen. Thai text: none.
- Leftover geometry: no rings or rods seen. Only the drawer's small white foot stop at ~(195,910) at g1420-1426, which is part of the drawer. A few white dust specks on the carpet (g1384) are dust.
- Cuts: 1374/1375 inside the whip (benign), 1406, 1420, 1459 and 1474 are real cuts (diff 54-62).

## Verdict: FAIL
Blocking: B1 (whip 8-9 frames), B2 (calipers not on the head). Should-fix: S1-S5. The qa_auto blur FAIL on 1420-1458 and 1475-1520 is a false positive and can be waived. The whip frames 1370-1378 are real blur and cannot be waived.
