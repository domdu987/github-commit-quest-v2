# QA-art round 16 s20: FIX-FIRST
s20 is reveal A, the side-view gallop: "fire behind, the oxen run forward" (g 1515-1595). I extracted all 93 frames (g = 1509 + n). I judged:
- a 144x256 phone sheet every 5th frame (about 6 fps)
- full-size frames at g 1530/1560/1590
- an action-band strip (x 0-720, y 480-740) every 6th frame from g 1521 to 1599
- 1.5x crops of the rear ox's head (x 240-560, y 580-780) at g 1521-1593
- a flame mask (orange-red, V > 235) to measure flame size

Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa16/ (s20_phone.jpg, s20_full.jpg, s20_band.jpg, s20_rear.jpg, s20_zoom.jpg).

## Checks
1. **Two rows and a lead of about 20 %: DONE.** The lead (centre, facing left) is about 20 % of frame height. The herd band is at y about 600-780, and a second ox follows at the right. Ground: the lower field is now dressed with jars, bowls and reed bundles. It does not look empty (note: it is busy and moon-grey, but fine).
2. **Is no flame on any ox's head? The flame is not on a head, but the lead's tail is through the rear ox's mouth. This is a hard-rule break (prop through a face) on every frame from g 1521 to 1595.**
   - The lead's tail rope runs straight back (to the right) from its rump and passes through the rear ox's open mouth and muzzle.
   - The lead's reed bundle lies across the rear ox's lower face and neck. The rope enters at the mouth corner at about x 420-470, y 700-720 in g 1569-1593.
   - The flame itself sits about 40-50 px behind the rear ox's head, on its shoulder (g 1590: flame x 537-571, y 692-720, against the rear ox's head at x about 400-495).
   - On the phone this reads as "the second ox carries the lead's torch in its teeth". It is the same failure as the round-14b blocker ("the lead's own bundle and flame across the next ox's muzzle"), and still not fixed with the 2.2-ox-length spacing.
3. **Are the flames visible enough? NO.**
   - The measured flame core is about 35 x 27 px (g 1545-1590), under 5 % of frame width, and only about 7 px on a phone.
   - On the phone sheet the fire reads as small red specks on the oxen's backs, not as "fire behind them". The biggest fire in the frame is still smaller than a horn blade.
4. **A half-cut ox at the left edge: NOTE, close to a blocker.** The ox ahead of the lead is cut by the left edge for the whole shot (only its coat and hindquarters are visible at x 0-100). The camera tracks with it, so it is never an exit.
5. **Kept and good:**
   - The gallop cycle and tracking move are real (frame-diff median 6.0, p90 7.7, under the guide but with a visible tracking move).
   - The rage faces and snort puffs act well.
   - The moon-blue rim is clean, and the warm saddle cloths stand against the blue field.

## Verdict: FIX-FIRST (2 blockers)
1. **Tail off the rear ox's face:**
   - Either droop each tail 25-35° downward, so that the rope and bundle pass below the following ox's chin at chest or knee height and the flame trails low behind,
   - or open the front-row spacing to at least 3 ox lengths, so that each tail tip ends at least 30 px short of the next ox's muzzle,
   - or put the follower in the rear row, offset at least 0.12 frame-heights higher, so that the tail line passes under its head.
   - Pass check: no tail rope, bundle or flame pixel within 30 px of any visible ox face (eyes, muzzle, mouth, horns) on every frame from g 1521 to 1595, checked at 2x zoom.
2. **Make the fire read:**
   - Give the lead's flame at least 70 px of bright core (about 2x now), streaming back and up behind it, and let it carry a strong warm glow on the ground.
   - Make it the brightest and biggest warm shape in the frame. A phone viewer must see "fire chasing them" without zooming.
   - Keep it at least 30 px from any head.

Also, in the same render, bring the left-edge ox fully in or take it fully out (no ox body cut by an edge for more than 0.5 s).

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 4 | 6 | 5 | 7 | 6 |
