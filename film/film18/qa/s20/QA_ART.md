# QA-art round 13 s20: FIX-FIRST
s20 is reveal A: "fire behind, the oxen run forward only" (g 1515-1595). I extracted all 93 frames (g = 1509 + n). I judged them on a 180x320 phone sheet every 5th frame (about 6 fps), on full-size head crops (x 0-400, y 640-900) every 3rd frame, at 2x zoom on the lead's face, and on tail-region crops every 4th frame. I measured the flame extent per frame from pure-red flame pixels and the ground with 20 px block masks.

## Asked fixes
1. **The lead ox's head is fully in frame: MOSTLY DONE.** From g 1530 on, the whole head is inside the frame. At g 1519-1527, which is the whip landing plus about 4 frames, the left edge cuts the muzzle.
2. **Its own flame is in frame and at least 120 px long: LENGTH DONE, EDGE NOT DONE.**
   - **Length:** The lead's flame is large and bright, about 160-200 px long, and it reads strongly as fire behind the ox.
   - **Edge:** The director set the limit at x 700. The flame touches or crosses the right edge (x 719) on g 1545-1563, which is 19 frames, the middle of the shot, and again on g 1591-1595. It is ≤ 700 on g 1567-1589.
3. **No neighbouring flame touches its face: NOT DONE. This is the worst problem in the take.** A flame from the ox just ahead and to the left trails back into the lead's face for almost the whole shot:
   - g 1533-1537: it overlaps the brow and forehead (0 px).
   - g 1541-1557: the flame tip is at the forehead and eye (0-10 px).
   - g 1560-1575: it is at the nose and snort puffs (about 5-20 px).
   - g 1587-1593: about 15-40 px from the nose.

   On the phone, every tile shows a little fire in front of the lead's face. That reads as "the ox is breathing fire, with flame ahead", which is the opposite of reveal A.
4. **Ground ≤30 %: NOT DONE on the frames without a jar.** With the block method, it measures 32-33 % at g 1524, 1533, 1548, 1554, 1563 and 1587, and 29-31 % elsewhere. The frames that read lower owe it to a jar body, which the mask counts as smooth. The full width from y 860 to 1280 is plain dirt whenever no jar is in. The team's 21-26 % does not reproduce.
5. **Other oxen overtake it, real motion: PARTLY DONE.** The tracking parallax on the wall and the mid-ground herd gives visible motion (team frame-diff: median 4.72, p90 7.27; a visible tracking move is acceptable under 9). On the phone, no ox clearly passes the lead in the near or middle lane. The mid-ground row just shuffles.
6. **The big fg jar at g 1569-1584 covers its rump: NOTE, worse than stated.**
   - The jar rim crosses the lead's chest and legs on g 1539-1545, g 1557, g 1566 and g 1581.
   - At g 1589 the rim runs across the lead's muzzle and mouth. That breaks §G: no prop through a face.
   - Together these frames also half-cut the lead behind a prop.

## Phone read
The lead's big own flame now sells "fire behind". But the neighbour's flame at its nose undoes the reveal, and the herd is a thin band (y 0.52-0.70) under 45 % empty sky with a plain bottom third.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 8 | 4 | 7 | 6 |

## Verdict: FIX-FIRST (3 blockers, each measurable)
1. **Nothing burning in front of the lead:**
   - Hide or pull back the ox that runs ahead and to the left of the lead, or delay it until its tail is past the left edge.
   - Pass check: no flame or reed-bundle pixel within 30 px of the lead's head (face, horns, blades) on any frame from g 1521 to 1595, measured on the render.
2. **Lead flame inside x ≤ 700 on every frame:** On g 1545-1563 and g 1591-1595, shorten the bundle 15 %, lean the flame 20° more upward, or truck the camera so that the lead sits about 30 px further left. Do not cut the head (see note 1).
3. **Ground ≤30 % on every frame, with no prop over the lead's face:**
   - Replace the big jar that rises to the lead's chest with low props (a sack, a spilled basket, reed bundles, low jars) whose tops stay below y 900, spread across the bottom third so that no frame has a bare full-width band.
   - Measure g 1524, 1533, 1548, 1554, 1563 and 1587.
   - Pass check: no prop pixels over the lead's head on any frame (g 1589 now fails).

## Notes
- Head at the left edge for g 1519-1527: shift the start 20-30 px right if fix 2 allows.
- To make "others overtake it" read on the phone, one near-lane ox passing the lead by g 1560 would sell it. Keep its flame behind it.
- The lead is about 20 % of the frame height (horn tip to hoof, about 250 px). The director set 25-30 %, so a little more size would help the reveal.
