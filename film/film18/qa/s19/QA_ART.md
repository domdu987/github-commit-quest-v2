# QA-art round 14b s19: FIX-FIRST
s19: burning oxen burst out of the wall holes at night (g 1427-1514). I extracted all 100 frames (g = 1421 + n). I judged every 5th frame (about 6 fps) on a 144x256 phone sheet, full-size pairs at g 1443/1457 and 1470/1484, 1.5-3x crops of the action band (x 240-720, y 580-900), and a 2-frame strip of the lead at g 1476-1492. I measured plain ground with smooth 20 px blocks below y 600 (luma std < 9, not dark) every 3rd frame, and counted ox coats as red blobs over 150 px. All numbers are measured on the rendered pixels. I compared against R5/R4.

## Round-14b checks
1. **Flame gaps of 10-14 px at g 1443, 1445 and 1457: FINE (note).** At g 1443/1445 a neighbour's reed bundle and flame sit just above the lead's horn (about x 480, y 660). At g 1457 a small flame sits just above the far ox's head. Each case lasts 1-2 frames (0.1 s in all) on oxen about 70-110 px tall. On the phone it flickers past and does not read as a burning head. The rest of the take holds at least 15 px, and the flames trail behind their oxen.
2. **Ox mouths at y ≤860: DONE.** The lowest point of the lead's mouth is about y 805 at g 1482-1484 (3x zoom). No frame reaches 860.
3. **Ground ≤30 %: NOT DONE. This is a regression.** Pitching the camera down for the mouths filled the bottom of the frame with plain dirt.
   - Raw block share is 28-37 %, median about 34.5 %.
   - It is above 30 % on 26 of the 34 sampled frames, for example 37 % at g 1421, 1445, 1457 and 1460, and 35-36 % at g 1481-1490.
   - The pebble-dot texture fails my smoothness test, so the true plain-dirt share is somewhat higher, not lower.
   - At g 1457 everything from y 800 to 1280 is bare ground apart from one pot.
4. **Herd density: NOT DONE (team admits it).**
   - The red-coat count is 1-3 in almost every frame (1 at g 1448-1454, 1469-1475 and 1496-1502).
   - The oxen are 90-130 px tall (7-10 % of frame height), in a band at y 640-800 under a wall that fills 55 % of the frame.
   - The far lane shows as 2-3 small heads plus the black Qi silhouettes.
   - On the phone it still reads as "an ox trots out, then another". The burst only arrives after the whip (g 1505+, 4-6 oxen).
5. **The new painted blue rim on the cards: GOOD.** It is a clean single light-blue edge, 2-4 px, on the top and right of the oxen and horns, with no doubling. It reads as moonlight against the warm fire key and fits §I.
6. **New §G finding: a pot is over the lead's jaw at g 1482-1486.** The near terracotta pot (x 600-700, y 820-890) covers the lead's lower jaw and mouth for 5 frames, so it reads as "the ox drinks from the pot". At g 1486-1490 the lead also leaves through the right edge behind the pot (an exit, which is acceptable).

## Phone read
The fire-against-moon-blue palette is good, the wall is rich, and the angry faces read. But the subject is small, sits in a thin band, and rests on a third of bare dirt. There is no herd until the whip. On the R5/R4 sheets the action fills the frame, and here it does not.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 7 | 4 | 7 | 6 |

## Verdict: FIX-FIRST (3 blockers, each measurable)
1. **Ground ≤30 % on every frame:**
   - Fill the lower field (y 860-1280) with dark lit foreground props: rubble and broken bricks spilling from the holes, dropped reed bundles, overturned baskets, low pots. Keep their tops below y 860 so the mouths stay clear.
   - Or tilt the look-at up about 4° and move the camera 0.3 D lower so that the action band sits at y 0.50-0.65.
   - Pass check: block share ≤30 % on every 3rd frame from g 1427 to 1502, measured on the render. Pebble-textured dirt counts as plain.
2. **Herd:**
   - Halve the near-lane spacing (one ox every 8-9 frames instead of 18).
   - Bring the far lane 20-30 % closer, so that its oxen are at least 60 px tall and its heads are never in the same screen row as a near-lane flame.
   - Pass check: at least 4 oxen identifiable in every 0.5 s phone tile from g 1435 to 1500, and at least one tile with 3 oxen emerging from different holes within 10 frames.
   - Keep the flame gap at 15 px or more, with up to 3 isolated frames at 10-14 px allowed as now.
3. **Prop off the face:**
   - Move the near pot at x 600-700 out of the lead's path, or drop it below y 900.
   - Pass check: no prop pixel over any ox head from g 1476 to 1492.

## Notes
- The near foreground pots are now terracotta with warm rims, which fixes the round-13 note.
- The blur at g 1504-1518 is the designed whip. Accepted.
- The frame diff (median 11.21, p90 14.19) is good and comes from real camera travel, with no pulses.
