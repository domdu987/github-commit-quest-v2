# QA-art, TAKE gate: s26 (shot 26, HALL hall_table EVENING, the money bag, film end) — FIX-FIRST

Frames checked (take index / g): 0/2077, 9/2086, 25/2102, 35/2112, 45/2122, 60/2137, 70/2147, 82/2159 (full size + 360x640).
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artend/s26_*.jpg

| Criterion | Score |
|---|---|
| Set density / ornament | 8 |
| Lighting & colour | 7 |
| Composition / phone legibility | 4 |
| Acting (grin, King's nod) | 6 |
| Key moment (Parliament pays the carpenter) | 3 |
| Match to refs / client taste | 6 |
| **Overall** | **5.5** |

## Why FIX-FIRST
The payoff of the whole film is "Parliament had to pay the carpenter". At phone size the money bag does not read.
- The bag lands BEHIND Harrison on the table (he stands in front of the table, back to it). It is a dark brown sphere about 50-60 px, next to his hand, and reads as a pot, a cannonball or the globe. No neck tie, no coins, no gold.
- Harrison faces the lens and grins; his gaze (0.2, 0.1) does not visibly go to the bag, so nothing links him to the money.
- The King is a 67-85 px head at the far end, and at f 25-45 his head sits directly beside/behind Harrison's head (overlap/tangent: the QA-art set note says Harrison and the King must not overlap in hall_table). His nod is invisible at phone size.
- On the last word "ช่างไม้" (g 2147) and the final frame g 2159 the push has made Harrison a big single (head 360 px), the bag is out of frame and the King is hidden. The film ends on a man smiling, not on "the carpenter got paid".
- Lower 30 % is dark floor under the table in every frame.
- Median frame-diff 3.93 (under 4); fine to fix with the new camera.

## Fixes (shot.py)
1. Staging: put Harrison BEHIND the table edge (or at its near corner, side-on) so the bag lands on the table between him and the lens. Move `HAR_M` to about (-0.9, 1.6, 0) and drop the bag in front of him at about (0, 1.1) on the tabletop (`bag0` = table-top point in front of him, not `+BAG_DX` right). The bag must be the FG subject, 1-2 D from the lens, in the lower third (y 800-1000, below the heads).
2. Prop: make the bag read as money: scale `bag_full` about 1.8x (target 150-220 px wide), use the `full` variant's tie/neck facing camera, warm gold key on it; add 4-6 coins bouncing out on the land (g 2107-2115) if the set has coin hooks. A squash on the land (scale z 0.8 for 2 f) sells the weight.
3. King: move `KING_M` from (1.00, 8.00) to the head of the table nearer the lens, about (1.3, 5.0), clear of Harrison's head by at least 1 head width in x for every frame; make the nods bigger (pitch amplitude about 2x) so they read at 360x640.
4. Harrison's acting: on the land turn him to the bag (`yaw` toward it, `gaze` down-right, e.g. (0.6, -0.5) for g 2107-2125), hands come to the bag (one hand on it), THEN look up to the lens and grin by g 2135. Keep the bounce.
5. Camera / end frame: end on a three-element tableau: bag FG, Harrison grinning behind it, King nodding beyond, all in frame at g 2147-2159. Replace the big push with `push=0.06` from a slightly higher `CAM_LOC0` z about 3.1 looking down onto the table (fills the dead floor area with tabletop), keep `slide_px` about 60 and the snap `k=1.10` aimed at the bag+Harrison (shift about (0.5, -0.3)), still moving on the last frame for the hard cut.

## Continuity
- Costumes match (old Harrison as s23; King blue coat as s24). EVENING light consistent (dusk window, warm practicals). Chair on, stubs 10 on the table (small cups behind Harrison): good, but they read better if a few of the stubs are visible beside the bag after the restage.
- The H4: Harrison carried it in (s23), the King held it (s24); here it is nowhere. Put the H4 on the table beside the bag or in Harrison's hand (`h4_watch` prop) for one clean prop line.

---
# Re-review after the fix round (TAKE gate, key takes): FIX-FIRST, 6.5

Frames checked (take index / g): 9/2086, 25/2102, 40/2117, 60/2137, 70/2147 (last word), 82/2159 (last frame) at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s26_*.png

| Criterion | Before | Now |
|---|---|---|
| Set density / ornament | 8 | 8 |
| Lighting & colour | 7 | 6.5 |
| Composition / phone legibility | 4 | 6.5 |
| Acting (grin, King's nod) | 6 | 6 |
| Key moment (Parliament pays the carpenter) | 3 | 5 |
| Match to refs / client taste | 6 | 6.5 |
| **Overall** | **5.5** | **6.5** |

## Earlier fixes
1. Staging: the bag lands on the table between Harrison and the lens: **FIXED.** It lands on the near table edge beside him, at y about 700-830.
2. Prop reads as money (bigger, tie toward camera, gold, coins, squash): **OPEN.** At 1.35x it is a plain brown round sack with no visible tie and no gold. At 360x640 it reads as a clay pot or vase. The squash is there, but the coins in the 'full' model are too small to see, and the gold stub cups around it get read as "coins" only by accident.
3. The King is clear of Harrison by a head and nods bigger: **PARTLY FIXED.** The King is now clear to the right, with no overlap. But his head is 97-134 px and the nod barely reads. In f 60-82 the lit candelabra sits right in front of his face (the flames cross his chin). In the final frame his head is cut by the right edge.
4. Harrison turns to the bag, hand on it, then looks to the lens: **PARTLY FIXED.** His arm reaches toward the bag (f 40), but his head and eyes stay on the lens the whole time. The link from his look to the money is still missing.
5. End tableau with bag, Harrison and King in frame at g 2147-2159, and a higher camera to fill the dead floor: **PARTLY FIXED.** All three are in frame at the end, which is good. But the lower 30-35 % of every frame is still dark floor under the table, with a pale translucent light wedge (a candle or lamp cone) over it. That is dead area at the most important moment of the film.
6. H4 in Harrison's hand: **FIXED** (small watch at his left hip).

## Fixes (shot.py)
1. Money: set the bag scale from 1.35 to 1.6 and move it 0.25 D toward the camera and 0.3 D right, so it no longer covers Harrison's face. In shot.py, dress 8-12 gold coins (h19_hall M['coin'] material, 0.06 D discs) that spill out from the base on the land (g 2107-2112, small hops), plus 3-4 coins stacked at the open neck. Give the sack a warm key: a small area light 1.5 D in front of the bag, about 2700 K, aimed at it. A gold spill is what tells "money" at phone size.
2. Harrison's look: from g 2107 to g 2125 set gaze (0.5, -0.6), pitch 0.25 and yaw toward the bag (+0.2), with a hand on the bag (arm_r hand on the bag's top). Then return to the lens with the grin by g 2132.
3. Camera: CAM_LOC0 z +0.5 and look target z -0.3 (or tilt down 6 deg), so the tabletop fills y 750-1100 and the dark floor is gone. Keep the snap at k 1.10 and moving at the cut, but add slide so the King's head stays inside x 680 at g 2159.
4. King: move KING_M 0.4 D left (or the candelabra 0.5 D right) so no flame crosses his face. Nod pitch amplitude x2 again (about 0.25 rad) and keep the happy eyes.
5. Light wedge: find the cone or volume that draws the pale trapezoid on the floor (likely a candle area light under or near the table edge) and hide it for this shot, or the restaged camera will crop it out anyway.
