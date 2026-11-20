# QA-art round 13 s19: FIX-FIRST
s19: burning oxen burst out of the wall holes at night (g 1427-1514). I extracted all 100 frames (g = 1421 + n). I judged every 5th frame (about 6 fps) on a 180x320 phone sheet, every 2nd frame on full-size action-band crops (y 680-920), and the mouth and plume contacts at 2x and 4x zoom with lines at y 850/860/870/880. All numbers below are measured on the rendered pixels.

## Round-13 asks
1. **Flames clear every face, horn and blade by at least 15 px: DONE.** On every 2nd frame from g 1427 to 1513, each flame trails off its own reed bundle behind its own ox. No flame card touches another ox's head, horn or blade. The closest case is g 1503, where the flame at x about 690, y 740 is about 90 px from the next horn tip. The team's matte number (worst 38 px) is plausible. I could not reproduce it exactly, because a colour mask picks up the flame cores and the wall lamps.
2. **Ox mouths at y ≤860: NOT DONE. The team's 857 at g 1484 does not reproduce.** At 4x zoom, the lowest point of the lead's open-mouth outline is:
   - about 876 at g 1481
   - about 887 at g 1482
   - at least 880 at g 1483-1484, where the pot rim hides the lower edge

   g 1479-1480 and g 1486 onward are above 860. This is no better than round 12 (about 878), and g 1482 enters the caption band.
3. **Ground ≤30 %: DONE (note band).** I measured smooth, outline-free 20 px blocks below y 700 every 3rd frame. Raw values are 23-31 %, median 27 %. The block mask also catches pot interiors and the dark hole openings (about 2-4 % of the frame), so the true plain ground in-shot is about 24-28 %. The whip-landing frames g 1505-1514 read 30-32 % raw, which is design (whip).
4. **Qi silhouettes behind the oxen: DONE.** At g 1429-1449 they run behind the ox row, and the ox heads overlap them, not the other way round.
5. **Pots warm: NOTE (as agreed).** The mid-ground pots are terracotta. The large near pots at g 1427-1449 are still lavender-violet.
6. **Does "oxen burst out of the holes" read as a herd? NO.** On the phone sheet, every tile from g 1427 to g 1502 shows 1 or 2 oxen, occasionally 3, each about 110 px tall (8 % of the frame height), in a thin band under a wall that fills 60 % of the frame. It reads as "an ox trots out of a hole, then another", not as a burst. The herd only appears in the far row after the whip (g 1507+, 6-8 small oxen). The director relaxed the flame rule to 15 px precisely to keep a dense herd. Trading the herd away for the flame rule does not meet that intent.

## New §G finding
- **A prop crosses a face.** The plumed helmet on the ground at frame centre (x about 330-460) sits in the lead lane, and its striped plume lies across the oxen's mouths:
  - g 1453-1456: the plume is over the left ox's muzzle and mouth (x 335-375, y 790-830).
  - g 1475-1480: the plume is over the lead ox's chin and mouth (x 430-470, y 830-860).

  On the phone it reads as an ox chewing a fan. Elsewhere the bell-shaped helmet with its fan plume reads as a bell or a broom, not a helmet.

## Phone read
Warm fire against blue moon-shade is good, the angry faces read, and the flames now clearly trail behind. But the burst is a trickle, and the herd beat is carried only by the last 8 frames after the whip.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 5 | 7 | 5 | 7 | 7 |

## Verdict: FIX-FIRST (3 blockers, each measurable)
1. **Herd density:**
   - Have at least 5 oxen visible in every 0.5 s phone tile from g 1435 to 1500, and at least 3 of them in a single tile emerging from different holes within the same 10 frames.
   - Keep the 15 px flame rule. Ways to do both:
     - Add a second lane of oxen running at the lens in front-3/4 or head-on (out of holes nearer the camera). Their own flames are then hidden behind their bodies, so the flame-to-face rule holds trivially.
     - Or add a farther lane at 0.5-0.6 scale, timed so that its heads are never in the same screen row as a near-lane flame.
     - Or start the far row seen at g 1507 earlier and visibly (g 1460+, along the field beyond the wall end).
   - Re-run the matte check over g 1427-1514.
2. **Prop off the faces (§G):**
   - Move the plumed helmet out of the ox lane (x < 250 or x > 560), or lay it on its side so the plume is under y 900.
   - Pass check: no prop pixels over any ox head on g 1450-1460 and g 1472-1484.
3. **Lead mouth:**
   - Over g 1479-1486, raise the lead's path about 30 px in frame, or keep it 0.15 D farther from the lens.
   - Measure the lowest mouth outline on the RENDERED g 1481, 1482, 1483 and 1484. All must be ≤860.

## Notes (not blockers)
- Near fg pots: still lavender at g 1427-1449. Warm their albedo or add a fire rim.
- The automated blur at g 1505+ is the whip. Accepted.
- The team's frame-diff (median 11.11 / p90 13.74) is good.
