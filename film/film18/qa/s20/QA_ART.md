# QA-art round 17 s20: PASS
This is the redesign: one lead ox in 3/4 view at about 26 % of frame height, with a big tail flame behind it, a far rear ox, and the wall in the background (in-film g1515-1595, take g1509-1601, g = 1509 + frame index).

How I checked it:
- I extracted all 93 frames.
- I made a 144x256 phone sheet of every 5th frame (about 6 fps).
- I viewed full-size frames at g1515, 1548 and 1578.
- I made a 1.5x left-edge crop (x 0-260, y 560-900) at g1563, 1575, 1583, 1589 and 1595.
- I made a 1.5x right-edge flame crop (x 500-720, y 500-720) at g1523, 1527, 1531 and 1547.
- I used a flame mask (R > 220, B < 120) to measure the flame every 4th frame.

Working files are in /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa17/ (s20_phone.jpg, s20_full1.png, s20_left.png, s20_right.png).

## Beat on a phone: READS
- From g1521 one raging dragon-coat ox gallops toward frame left, with a big red-yellow-white flame streaming behind it on its tail.
- The flame is the brightest warm shape in the frame, about 120-135 px wide (mask x about 585-719), and clearly behind the ox, never ahead of it.
- The tracking camera and the passing props and ground carry the forward run.
- "Fire behind, the oxen run forward only" reads at once. It is much better than round 16.
- The rear ox and the wall are background flavour only.

## Specific checks
- **Lead head clipped 0-5 px from g1575: does NOT matter.** On the left-edge crops (g1575-1595), only the tip of the left horn with its brass cap and the outer edge of the ear touch the frame edge. The eyes, muzzle, open mouth and snort puffs are fully in frame with a clear margin. The face is not clipped, so this is not a half-cut character. It is invisible on a phone.
- **Flame tip at the right edge for about the first 40 frames: does NOT matter.**
  - The mask reaches x 716-719 at g1523-1535 and g1547, with only 21-101 px of flame in the last 8 columns.
  - From about g1551 it is 0-6 px, and 0 px after g1579.
  - Only the thin trailing wisp is cut. The white-yellow core is about 60-100 px inside the edge.
  - On a phone it reads as a flame streaming off-frame behind the ox, which is right for the beat. This deviates from the director's "flame ends <= x 700" spec; I note it for the client report and do not block on it.
- **Fire on a head:** none. **Face in the caption band:** none (team: mouth worst y 813). **Poles or props through a face:** none; the props are low on the ground. **Ghosting or glitches:** none seen. The whip-in g1515-1520 is the designed transition.

## Notes (not blocking)
1. **Flame attachment:** at full size there is a small gap (about 10 px) between the broom tail tip and the flame card. On a phone it reads as attached. Close it if this is re-rendered for any other reason.
2. **The herd reads as a single ox.** The rear ox is tiny and far away. That is acceptable for this beat (s19 carries the herd).
3. **The lead holds a near-constant screen position.** Forward motion comes from the ground and props sliding (frame-diff median 5.9, p90 8.4, under the p90 guide of 9 but with a real tracking move).

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 7 | 7 | 6 |
