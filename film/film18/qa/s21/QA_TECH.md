# QA-tech round 14 s21: FAIL
Checked: all 99 frames at 5-frame steps plus every frame g1640-1688 for the mouth; tongue/mouth-outline mask per frame; 1:1 crops with the y860 line; frame-diff 90x160 (director 8.19 / 16.33 accepted). Dark-opening blur accepted.

## Blockers
1. g1596-1645 (pre-snap) - ground 40-46 % of the frame (limit for the round-12 note is 35 %). The wall base is at y ~690 at g1596 and ~740 at g1640, so floor = y 690-1280 = 46 % at g1596 and ~42 % at g1640 (the plaza between the soldiers and the wall counts). It is also not "dark unlit": it is a lavender/pink-orange soft gradient with long shadow bands. Fix: tilt the camera up / lower the floor so the wall base sits at y <= 830 (floor <= 35 %), or add a dark fg prop (overturned table, jars) over the bottom-right; keep the ground dark.
   After the snap (g1650+) the herd covers it, ground ~25 %: OK.

## Asked checks
- Hero mouth lowest pixel <= y 860: PASS on every in-film frame g1596-1682. Mouth/chin outline, measured: 700-735 g1640-1650, 750-775 g1660, 820-835 g1671-1679, 849 g1681, ~858-860 g1682 (margin 0-2 px at the last in-film frame). Handle frames g1683-1688 reach 885, they are outside the film (s22 cuts in). Note: no margin at g1682; if the push is touched, shorten it by 3-4 frames.
- Soldier rim: yes, a hard 6-8 px bright yellow-gold outline on three black silhouettes; reads as fire-side rim (a little neon). Shock reads g1646-1665 (arms raised, leaning back); after g1668 the herd hides them.
- Cup falling: a gold cup leaves the right soldier's hand at g1647 and falls to the ground by g1664, visible as a ~25 px gold blob (small but readable on the 6 fps sheet).
- Tan posts: none. A small grey block at the left edge, g1590-1600 (x 0-10, y 880-1000): brief, note.
- Flames on tails: yes, flame cards on tails from g1630, a wall of fire behind the herd from g1645. Rage faces read.
- Frame-diff: low in the pre-snap push (2-7), held snap g1645 (18). No pulsing.

## Notes
- Soldiers are pure black silhouettes (no costume); accepted so far.
- Glints: a star at g1647-1650 over the left horn; optional.
- Opening blur: accepted by the director.
