# QA-art round 12 s19: FIX-FIRST
s19: burning oxen burst out of the wall holes at night (g 1427-1514). I extracted all 100 frames (g = 1421 + n), and judged every 5th frame (about 6 fps) plus every frame from g 1450 to g 1490. I viewed them at full size with a line at y 860, at 4x zoom for the flame-to-head contacts and the mouths, and on a 180x320 phone sheet. All the numbers below are measured on pixels.

## Round-12 asks
1. **Flame: no overlap with a face, horn or blade, and at least a 15 px gap: NOT done.** The team did not run a pixel test (QA.md says so), and its own `measure.txt` still reports "flame<60 on 68 frames, worst -73". On the rendered frames, a tail flame in the middle lane keeps landing on the horns or head of the ox next to it, with a gap of 0 px:
   - g 1440: a flame at x 430-450, y about 735 sits against the second ox's horn and the edge of its face.
   - g 1443: a flame at x 490-515, y 745-760 sits on the centre ox's right horn.
   - g 1454-1461: a flame at x 368-470, y 750-795 is crossed by the near lead's right horn. The lead's horn passes over the flame card at g 1456 and g 1459 (4x zoom).
   - g 1463-1465: a flame at x 560-640, y 755-780 sits on the horns of the ox behind.
   - g 1470 and g 1474-1475: a flame at x 497-530, y 756-783 is overlapped by the near ox's right horn.
   - g 1477-1481: a flame at x 585-628, y 755-783 is overlapped by the lead's left horn, and its white tip touches the forehead and ear of the third ox (x 620-630, y 780).
   - g 1493: a flame at x 500-545, y 765-790 sits on the next ox's horn.

   On the phone this reads as fire on the oxen's heads, not trailing behind them. It breaks rule 3, which is the film's key idea.
2. **Mouths at y 860 or above: almost done. The team says 858, but that is the round-11 number.** The lowest edge of the open mouth measures: g 1479 at about 853, g 1481 at about 864, g 1483-1484 at about 873-875, and g 1485 at about 878, where the pot cuts it off. g 1486-1491 are all above 840. So the worst is about 878 over 5 frames. That is a big gain on round 11 (950-985), and nothing reaches the caption band at y 880, but the ask was 860.
3. **Plain ground 30 % or less: NOT verified. The team's 16-23 % does not reproduce.** I measured smooth, outline-free 20 px blocks below y 840 every 3rd frame. Most frames come out at 25-29 %, but g 1442 is 31.5 %, g 1445 is 32.6 %, g 1448 is 31.0 % and g 1457 is 31.5 %. At g 1442-1448 the band from y 900 to 1280 is bare earth across the whole width, apart from three small pots. Under the director's rule, anything over 30 % blocks.
4. **Pots read warm terracotta: half done.** The middle-ground pots are good: median hue 11-22 deg (g 1437 centre pot (137,93,69); g 1485 lit pot (124,86,64)). The largest pots, which are the near foreground pots at g 1430-1447 and g 1497-1512, still come out violet: hue 252-269 deg (g 1437 (64,55,99), g 1507 (69,55,94)). On the phone sheet those are the pots you notice, and they read as lavender.

## Phone read
The beat reads: red-coated, angry oxen pour out of the breaches along a lit wall at night, and the flames are warm against the blue. But the herd sits in a thin band (y 700-860, about 12 % of the frame height) under a wall that fills 60 % of the frame. At g 1427-1453 the large black Qi silhouettes run in FRONT of the lead ox and cover the reveal. The shot plan puts them behind the oxen. The flames are small, and because they sit on the heads, the reading is "oxen with torches on their heads" rather than "fire behind them".

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 6 | 7 | 6 | 7 | 7 |

## Verdict: FIX-FIRST (2 blockers, 1 small fix)
1. **Flames clear of heads (blocker):** In the middle lanes, swing each tail down so the flame trails at or below the ox's back line rather than up at head height. Or offset the following ox 0.6 D sideways, or delay it 4-6 frames. As a last resort, scale a flame card to 0.6 while it is near a head. Check it with an ID or matte pass (flame cards against ox head, horn and blade) and a distance transform on every frame from g 1427 to g 1514. Pass when the minimum distance is at least 15 px. Re-check the frames listed in ask 1 by eye.
2. **Ground at or below 30 % on every frame (blocker):** Add a dark rubble clod or a lit fg prop low in the lower left for g 1439-1460 (wall debris fits this), or slide a near fg pot through it. Measure g 1442, 1445, 1448 and 1457 with the same block method and get them to 28 % or less. Do not tilt down.
3. **Lead mouth (small):** Over g 1479-1486, raise the near lead ox's path about 20 px in frame, or keep it 0.1-0.15 D farther from the camera, until the lowest mouth outline is at y 860 or above. Measure g 1481, 1483, 1484 and 1485.

## Notes (not blockers)
- The near fg pots should come out warm: lift the albedo toward terracotta, or add a warm rim from the fire on the side toward it, so the moon side stays around hue 0-40 deg rather than 260.
- Move the Qi silhouettes behind the lead ox or to the frame edges at g 1427-1453, so the burst is not covered.
- The automated blur at g 1505+ is the whip. Accepted by the director.
- Frame-diff median 11.49 / p90 14.38. Good.
