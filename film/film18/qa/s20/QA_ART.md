# QA-art round 14b s20: FIX-FIRST
s20 is reveal A, the redesigned side-view gallop: "fire behind, the oxen run forward only" (g 1515-1595). I extracted all 93 frames (g = 1509 + n). I judged every 5th frame (about 6 fps) on a 144x256 phone sheet, full-size frames at g 1530/1560/1580/1595, and an action-band strip (x 0-720, y 540-800) every 6th frame from g 1521 to 1593. I measured plain ground with smooth 20 px blocks below y 600 every 6th frame. I compared against R5/R4.

## Checks
1. **Does "fire behind, the oxen run forward" read on a phone? NO.**
   - The oxen gallop screen-left in a single nose-to-tail row at the same depth (y 590-790).
   - Each ox's reed bundle angles up and back, so it ends on the next ox's head.
   - The flames are small (about 25-40 px).
   - On the phone it reads as "a row of oxen holding torches at each other's heads", not as fire chasing the herd from behind.
2. **The lead ox's head is fully in frame: DONE.** The lead is the centre ox (head at x about 180-260). The head is inside the frame from the whip landing on, with no edge cut.
3. **Its own flame is in frame: DONE.** The lead's flame is at about x 590-620, well inside x 700.
4. **No neighbour's flame on its face: NOT DONE, on every sampled frame.**
   - At g 1521, 1527, ... 1593, the reed bundle and flame of the ox behind and to its left sit on the lead's horn and brow. The gap is 0-10 px, often touching the horn tip (for example g 1530: flame at about x 270, y 605, against the lead's horn at x 250-260).
   - The same geometry puts the lead's own bundle and flame across the next ox's muzzle and mouth (g 1530: about x 520-610, y 650-670), all the way through the shot.
   - This is the round-13 blocker in a new layout.
5. **Ground ≤30 %: NOT DONE.**
   - The block share is 33-38 % on every sampled frame (median about 36 %).
   - The bottom 40 % (y 790-1280) is open field with sparse small jars and reed bundles, which do not break it up.
   - The lead is about 200 px tall (16 % of frame height) against the director's 25-30 %, so the herd is a thin band.
6. **Motion is real: YES (note).**
   - The gallop cycle is visible, and the trees, tower and moat slide with the tracking.
   - The frame diff is median 4.73 and p90 6.56. p90 is below the guide of 9, but the tracking move is visible, so I accept it.
   - The whip-in at g 1509-1520 lands cleanly.

## Phone read
The cool night field and warm saddle cloths are good, and the snorts and open mouths act well. But the key reveal fails at the composition level: the flame placement, a small herd, and a large empty field below it.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 3 | 7 | 4 | 7 | 6 |

## Verdict: FIX-FIRST (2 blockers, each measurable)
1. **Flames behind, never on a head:**
   - Stagger the herd in depth. Put the lead alone in the near lane and the others in a mid lane at least 0.2 frame-heights higher and at 0.6-0.7 scale.
   - Or keep one row but space the oxen so that each tail tip ends at least 1.6 ox-lengths apart, and lean the flames 20-30° more upward.
   - Lengthen the lead's own flame trail behind it (at least 120 px, ending at x ≤ 700) so that it is the biggest fire in frame.
   - Pass check: no flame or reed-bundle pixel within 30 px of any visible ox head (face, horns, blades) on any frame from g 1521 to 1595, measured on the render.
2. **Scale and ground:**
   - Move the camera closer and lower so that the lead is 25-30 % of frame height (director spec) and the herd band sits at y 0.45-0.72.
   - Lay dark low foreground props (jars, reed bundles, a toppled cart wheel) densely enough along the bottom that no full-width bare band remains.
   - Pass check: block share ≤30 % at g 1524, 1533, 1548, 1554, 1563 and 1587, and no prop over the lead's head.

## Notes
- The rim works on the oxen: a thin light-blue top and right edge, clean, with no ghosting.
- The blue point lights on the ground give a warm-plus-cool frame (§I).
