# QA-tech s11 ROUND 3 (shots 27-28, g1509-1700, cut g1579, snap ~g1653-1667) - VERDICT: PASS (no blockers; 4 should-fix)

Method: 192 frames extracted from take.mkv; viewed full size g1564, 1599, 1609, 1629, 1645, 1655, cut strip 1577-1581, snap strip 1650-1657, eye strip 1604-1614, zooms 1564/1599. Per-frame diff run for frozen/black.

## Blockers from R2
1. Shot-28 card held (g1589-1654): FIXED, marginal. Bertillon's pinned arm (screen-left, mirrored) bends down from the shoulder; dark cuff plus fist sit on the card's lower-right edge (g1599 fist ~x440,y705; g1629 ~x460,y695; g1645 ~x500,y690). Connected to the arm, tracks the card through the camera drift, no hips pose, no propping on the chair. Reads as "holding the board's corner" at phone size, though weakly: the card is big/tilted and has a thick frame, so it reads a bit like a wall board.
2. Rods near Bertillon (g1599-1614): FIXED. No white crossed rods in any viewed frame (1599, 1604-1614, 1629, 1645). Remaining set pieces (clock, ruler, chair, measure table) are legit.
3. Shot-27 hand-as-ball: FIXED/acceptable. g1564: Bertillon's arm rises to the card's left edge with a cuff, hand hidden behind the card = connected. Dupont's open hand (g1564 ~x410-440,y745) is at the card's lower-right corner, small spider-like fingers, not a ball.

## Claim check
- Bottle panel visible and uncovered: YES. Yellow panel + bottle ~60 px tall (g1599 y480-545), nothing covers it; Bertillon's head clips only its last ~20 px of right end from g1629 (x~465+). Bottle not clipped.
- Bertillon+card in frame to g1650: YES (Bertillon head right edge ~x690 at 1599, ~x715 at 1645; clipped only from ~g1655 during snap). Inspector enters from the left g1645+, fine.
- Ticks ~17 px: YES (g1564 zoom: stacked white chevrons ~20 px, right end of rows, unobstructed, readable).
- Sweat fades g1607-1614: YES (drops shrink 1607->1614, still present at 1614).
- Fist = plain fist: confirmed, acceptable.
- Cut g1579: clean hard cut (diff 50), no black/magenta frames.

## Regression checks
- Lip-sync: none; Dupont/Bertillon mouths static; inspector static "o" (g1655+) OK.
- Chins: Bertillon ~y690-700, Dupont ~y770-800, inspector ~y700 at g1655, all < 880.
- See-through cards: none. Beam shafts: none. Dust: a few specks only (<=0.5). Blur: none seen incl. snap g1655.
- Frozen hold: none (min frame diff > 0.2 everywhere; camera drifts continuously). Black/magenta: none.
- Expression pop: Dupont eyes go half-lidded -> wide in ONE frame g1606->1607 (not at the snap g1653-1667). Sweat now persists, which helps, but it is still a pop.

## SHOULD-FIX (non-blocking)
1. g1606->1607: 1-frame eye widen (R2 #5 still open). Add 3-4 f blink/widen tween.
2. g1589-1655 (S28): chair back post (x~275-335, y555-730) sits in front of the card's left third, cutting the circle icon and making the card look wall-mounted behind it. Nudge card/camera or hide the post, so the card reads as held in front.
3. g1589-1650: card could show more of the arm gripping (fist is below/at the corner, ~30 px in from the right edge); raising the fist ~40 px to mid-edge would sell "held" at phone size.
4. g1564 (S27): Dupont's hand still sits on the card's lower-right corner; move it ~40 px away.
5. Carried from R2 (minor): Dupont seated pose: arms bent stiffly with claw hands on chair arms, ok now; bottle icon ~60 px (up from 45) is still smaller than the requested 100 px.
