# QA-tech round 14b s20: FAIL
Checked: all frames g1515-1595 at 6 fps, every frame g1515-1523, every 2nd g1523-1595 (crops y520-860), red-flame x-extent measured on all 81 frames (hsv mask), ground block mask, frame-diff 90x160 (median 4.74, p90 6.56; matches meta, so the median gate passes).

## Blockers
1. Neighbour's flame at the lead's face (repeat of round 13). The ox just ahead (left) of the lead trails a tail pole whose red flame sits on the lead's horn root/brow: 0-8 px gap at g1529-1567 (tip touches the horn at g1529, 1539, 1547, 1553, 1559, 1567; checked 1.6x crop at g1553). Rule is >= 15 px. Fix: delay or drop the ahead ox's pole/flame so it is >= 40 px clear of the lead's head, horns and ears for g1521-1595 (e.g. shift that ox 150 px left or raise its pole 60 px), or shorten its pole.
2. Lead's flame ends beyond x 700. Max red-flame x: 705 g1515, 701 g1521, then 717-719 (frame edge, clipped) on g1525-1532, 1536-1537, 1539, 1541-1542, 1544, 1547, 1550-1552, 1559, 1561, 1563-1565, 1575, and 719 on every frame g1584-1595. The flame is cut by the right edge. Fix: truck the camera ~40 px right in g1525-1565 and g1584-1595 or shorten/raise the pole by ~0.15 D; keep >= 120 px length (it is ~160 px).
3. Ground > 30 %. Block mask (outline-free smooth blocks below the horizon, props excluded) 0.38-0.45 on all frames (0.39 g1517, 0.44 g1541, 0.45 g1553, 0.44 g1589). Team's "rough mask 0.5" admits it. The band y 860-1280 is dirt with only a few small jars/bundles. Fix: lower the camera/raise the herd line so the herd sits at y 0.55-0.70, and fill the bottom third with dark low props (jars, sacks, reed bundles with outlines) covering >= 15 % of the frame.

## Passed
- Lead ox head fully in frame from g1515 (big lead enters g1517, head x >= 60 from g1518; the ox cut at the left edge is the one ahead, not the lead). Side view, rage face, ~17-20 % of frame height.
- Lead flame length ~160 px (>= 120).
- Contact shadows: soft dark smear under planted hooves, light warm pools alongside. Faint (see notes), counted as present.
- Frame-diff median 4.74 >= 4; p90 6.56 < 9 but the follow camera slide (0.97x herd speed, wall/ground parallax) is a visible eased slide, no pulsing.
- No placeholders, no pulsing, mouths held (open, no lipsync flap), blue rim clean, no props across the lead's face (fg jar low, below y 860 after g1550).

## Notes
- Contact shadows are weak (about 15-20 % darkening); the orange pools are not tied to the hooves (e.g. g1553 pool ~100 px right of the lead). Strengthen to 35 % dark ellipses.
- The lead's own tail pole passes in front of the following ox's muzzle (g1529-1553); the flame the trailing ox shows reads as lying on its own back.
- Whip landing g1515-1517: lead is small and the wall fills the frame; fine as a landing.
