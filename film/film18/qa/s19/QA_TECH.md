# QA-tech round 17 s19: PASS
Checked: 6 fps sheet; 1:1-scale crops (y 560-1080) of every 2nd frame g1440-1505 (all oxen, pots, flames).

## Verified
- Ox mouth/jaw lowest pixel: about y 750-800 on every checked frame (worst lead jaw about y 790 at g1484-1492); never > 860. Team's "mouth worst 782" is consistent. No face in y 880-950.
- No flame overlaps any ox face, horn or blade (tail flames sit above/behind the bodies; neighbour gaps visibly >= 10 px in all crops).
- No pot or prop touches any ox jaw or face. Pots/bundles are at hoof level or lower (rims y >= 880); the round-16 blocker (pot over jaw g1482-1486) is gone.
- No half-cut ox beyond movement exits: the lead exits at the right edge g1490-1500 (accepted), small far oxen cross the left edge briefly.
- No pulsing, no placeholders, no pole through a face, mouths still. Whip-out blur g1507+ accepted.

## Notes
- Ground (director): max 0.356 at g1433-1460 and g1499, median 0.27. Frames are heavily dressed with pots, bundles and rubble; no bare flat area near a third of the frame. NOTE only.
- Pots g1427-1450 are violet, not warm; flames are small at phone size. Oxen visible per 0.5 s tile 2-4.
- Props at the lower edge are large and dark-outlined (near pots at y 1100-1280); fine as foreground.
