# QA-tech round 13 s20: FAIL
Checked: all frames g1515-1595 at 6 fps, every 2nd frame band y520-860, 2x crops of the lead head g1517-1533 and the left flame g1547-1567, red-flame x-extent measured per 2 frames, frame-diff re-measured 90x160 (median 4.78, p90 7.38: median gate met; p90 <9 is a guide only), ground colour mask, hoof crops.

## Blockers
1. Lead ox head cut by the left edge. g1515-1519 the lead is a small ox at x 110-240, then from g1517-1519 a big ox enters left already cut; g1521-1533 the head is cut: snout/horn tip at x<0 (g1521, g1527-1531 muzzle at x 0-5, horn root cut), at g1523 the nose touches x 0. Requirement is whole head in frame from the first frame. Fix: start the camera 60-80 px further left (head x 40-200 from g1515) and hold the head inside x >= 30 through g1535.
2. Neighbour's flame touches the lead ox's face. A small tail flame (from a pole held beside the black Qi at the left, g1547-1567) trails right into the lead's head: g1553 flame tip touches the brow (gap 0), g1555 about 5 px, g1557 and g1559 overlap the forehead/horn root, g1561 and g1563 overlap the ear/horn base, g1565 about 5 px. Gap >= 15 px only from g1567. Fix: move that ox/Qi pair 150 px further left or higher/lower so the flame stays 40 px clear of the lead's head from g1547 to g1567.
3. Lead's own flame (the large flame at the end of the long pole, about 160 px) runs to the right edge: red flame max x = 717-719 (frame edge) g1545-1567 and g1591-1595, x 702 at g1543. The requirement is x <= 700. Fix: pan/truck 30-40 px right in those windows or shorten the pole 0.1 D; keep >= 120 px length.
4. Contact shadows absent. At g1530/1550/1564/1578 crops: hooves end on motion-blurred gravel with no dark shadow; the lit orange blobs on the ground are floating spots unrelated to hoof positions. Fix: dark soft contact ellipse under every hoof of the lead and the two nearest oxen (30-40 % black, ~60 px wide).

## Judged
- Fg jar covering the lead's rump (g1569-1584): it covers the neighbours' hindquarters/legs rather than the lead's head, and at g1583-1591 hides the lead's rear legs. The problem is the look more than the position: the jar is a flat violet-navy shape with a single outline and almost no texture (read as a navy slab, rule 2), also a clipped bowl of logs low-left. Fix: retexture/warm-glaze the jar (terracotta with the film's grade) and keep it at x > 0.55 and below y 900 so it never covers an ox leg.
- The lead's tail pole passes in front of the second ox's horn/ear at g1523-1535 (pole through a neighbour's head). Note.

## Passed
- Lead is side view, face rage, about 22-25 % of frame height. Flame >= 120 px: yes (about 160 px).
- Ground (mask incl. props): 0.32 g1529, 0.30 g1549, 0.295 g1564, 0.294 g1579, 0.33 g1589; plain ground about 0.26-0.30 after subtracting the jar: note, borderline.
- Frame-diff 4.78 / 7.38. No pulsing. No text, mouths held. Flames on tails (yes). Whip landing g1515-1519 OK.
