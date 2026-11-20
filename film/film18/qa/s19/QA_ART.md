# QA-art round 17 s19: PASS
This is the head-on reframe, with oxen bursting out of the wall holes toward the camera (in-film g1427-1514, take g1421-1520, g = 1421 + frame index).

How I checked it:
- I extracted all 100 frames.
- I made a 144x256 phone sheet of every 5th frame (about 6 fps).
- I viewed full-size frames at g1457, 1476, 1487, 1494, 1500 and 1507.
- I made a jaw strip (y 460-880, with a line drawn at y 860) of every 3rd frame from g1451 to g1505.
- I made flame crops (y 460-720) at g1460, 1466, 1475, 1478, 1493 and 1499.

Working files are in /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa17/ (s19_phone.jpg, s19_full1.png, s19_full2.png, s19_jaw.jpg, s19_flames.png).

## Beat on a phone: READS
- The lit wall has broken holes, and several raging dragon-coat oxen come out of them, head-on toward the lens.
- The red-orange flames sit on the raised tail tips, behind and above each body.
- The oxen are about 15-25 % of frame height, and 3-6 oxen are visible per tile from g1457 to g1503.
- "Oxen burst out of the holes in the wall, glowing tails" reads without zooming. This is the strongest version yet.

## Specific checks
- **Mouths at y <= 860: OK.** On the jaw strip, every open mouth is above the y 860 line. The lowest lead jaw is about y 760-800 (for example g1490 and g1493). No face reaches the caption band.
- **No pot or prop on a jaw: OK.** No pot over any face on any strip frame from g1451 to g1505. The pots and reed bundles sit on the ground below y 820, and their tops stay below every muzzle. The round-16 blocker is gone.
- **Flames never on a face: OK.**
  - Every flame is at the tip of an upturned tail, above the back or the horns.
  - The closest case is a small far ox at g1466, where a flame passes about 40 px above its head. The flame does not overlap the head.
  - No flame overlaps any eye, muzzle or horn base in the crops.
- Hard rules otherwise: no half-cut hero, no poles through faces, no ghosting or glitches.
  - Edge oxen are cut only as they pass out of frame.
  - The wall ladder at the right is behind everything.

## Notes (not blocking)
1. **Flames are small:** about 30-45 px, roughly 5 % of frame width. They read as "glowing tails" but not as a blaze. If there is a cheap re-render, scale the flame cards to 1.3-1.5x, keeping the gap to the faces.
2. **Oxen look more like they trot than burst.** A little more forward lunge or dust at the hole lip would sell "burst".
3. **Whip-out (g1505-1514) lands on silhouette soldiers at the outer wall.** This is the designed transition, and the blur is accepted as before.
4. **Ground** is a QA-tech number. Visually the foreground is dressed with pots and reed bundles and does not look empty.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 7 | 7 | 7 |
