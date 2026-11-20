# QA-art round 13 s22: FIX-FIRST
Shot: REVEAL close-medium, "หางลุกเป็นไฟ เขาติดมีดวาววับ" (g 1683-1742). I extracted all 71 frames (g = 1677 + n). I judged them on a 180x320 phone sheet every 5th frame (about 6 fps), at full size with guides at x 0.08/0.45/0.65/0.90 and y 860, on soldier crops at 1:1, and on mouth crops every 3rd frame.
I measured the mouth on every frame: the lowest tongue pixel (RGB about 227,113,63), then down to the bottom of the dark mouth outline. I measured the flame extent per frame from flame pixels, and the ground with a chroma mask (overlay checked by eye).

## Asked fixes
1. **Ox head in x 0.08-0.45, mouth at y ≤860 on every frame: NOT DONE in the second half.**
   - **Head position:** The head sits at x about 0.10-0.48 for most of the take, which is fine, with only the ear past 0.45. At g 1736-1742 the cheek reaches x 0.04.
   - **Mouth:**
     - g 1683-1712: the mouth outline is at 824-858. OK.
     - g 1713-1742 is over 860 on most frames: 862-866 (g 1713-1717, g 1723-1724), 870-877 (g 1725-1727, g 1733-1734), and 886-890 (g 1736-1737).
   - The team's "about 800 at g 1738" does not match the render (I measure about 870).
2. **Tail flame in frame: MOSTLY DONE.** The hero flame is in frame at x 0.75-0.98 from g 1683 to 1713. It touches the right edge at g 1715-1717 and is cut by the edge from g 1733 to 1742, the last 10 frames.
3. **Soldier fully in frame at x 0.65-0.90, turned toward the ox, behind the tail: PARTLY DONE.**
   - **Position: DONE.** The soldier is at x 0.70-0.86, head to feet in frame, for the whole take.
   - **Depth: DONE.** He stands behind the ox.
   - **Facing: NOT DONE.** He is still square to the lens with his pupils centred on camera. He is the soldier who must react to the ox, so the eye-line exception applies to him.
4. **No brazier: DONE.** There is no tripod or navy cone anywhere.
5. **Blue sky: DONE.** The sky is blue with the moon and clouds.
6. **Ground ≤30 %: DONE, at the limit.** With the chroma mask, it measures 28-32 % raw. The mask also catches part of the muzzle and pot (about 1-1.5 %), so the true value is about 27-30.5 %, slightly lower after g 1713. It sits on the line, not clearly over it, so I log it as a note. The team's 3-5 % is not a real measurement.
7. **Does the reed bundle read as a broom held by the soldier? YES, and now as a flaming TORCH.**
   - The hero's tail bundle rises from the rump diagonally across the soldier's chest and right hand (x 500-640, y 400-560), and the tall flame stands just above his shoulder.
   - g 1683-1703: the flame's left edge is 0-10 px from his face. g 1723: about 25 px.
   - On the phone, every tile reads "terrified soldier holding a torch". That breaks rule 3 (a flame next to a face) and the "nothing through a face" spirit of §G.
8. **Does "tail ablaze, blades glinting" read? HALF.** The gold horn blades and the glint star at g 1733-1739 read. "Tail ablaze" does not, because the fire reads as the soldier's torch. The glint lands on the horn root and coat, not on a blade tip (optional per the director).

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 8 | 6 | 5 | 7 |

## Verdict: FIX-FIRST (2 blockers, each measurable)
1. **Tail and soldier staging (the reveal):**
   - Re-aim the hero tail so that the bundle trails back and to the right at or below the rump line (y 0.40-0.50), and the flame rises from x 0.55-0.68, between the rump and the soldier.
   - Or move the soldier to the far side of the flame at x 0.74-0.90.
   - Pass checks, on the render:
     - No bundle or flame pixels overlap the soldier's silhouette.
     - The flame is at least 30 px from his face on every frame.
     - The flame is ≤ x 700 on every frame, including g 1715-1717 and g 1733-1742.
     - On the phone sheet the flame visibly grows from the ox's rump and the soldier's hands are empty.
   - In the same pass, yaw the soldier 30-40° toward the ox with his pupils on the ox.
2. **Mouth at y ≤860 on g 1713-1742:**
   - Lift the ox 30-35 px in frame over the second half, by reducing the push's downward drift or by raising the look-at, or keep it 0.1 D farther from the lens.
   - Measure the rendered mouth outline at g 1713, 1725, 1733, 1736, 1737 and 1742.

## Notes (not blocking)
- Ground at about 27-30.5 %: if you lift the ox for fix 2, slide the pot or reed bundle about 40 px toward the centre to keep it under 30.
- The grey-blue bundle of sticks at the bottom reads cool and nearly untextured on the phone. Warm it a little.
- The rage face and the grade are good. Keep them.
