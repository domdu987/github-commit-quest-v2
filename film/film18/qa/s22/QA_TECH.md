# QA-tech round 12 s22: FAIL

Checked: all 71 frames extracted; g1683-1742 at 4-frame steps plus every frame g1729-1742; x 0.08/0.45/0.65/0.90 and y 860 guide lines; mouth crops (y 600-960) of 10 frames; soldier crops; right-edge crops g1730-1742. Pixel measures on the rendered frames. The brazier and sky are fixed; the rest is not.

## Blockers
1. g1732-1742 - ox mouth below y 860 (hard check). Mouth/tongue bottom measured on crops: g1683 ~815, g1695 ~845, g1710 ~850, g1725 ~860, g1731 ~855; after the punch g1733 ~880, g1735 ~890, g1737 ~920, g1739 ~890, g1742 ~900. The cream muzzle bottom reaches ~830-843 at g1734-1736. The team figure "mouth 808" is wrong after the punch. Fix: the +15 % punch pushes the head down; tilt the camera up (or lift the ox) by ~60 px at g1731 so the mouth outline stays at y <= 840 through g1742; re-measure the mouth, not the head box.
2. g1733-1742 - ox head leaves the x 0.08-0.45 band and is cut by the left edge (rule 4). Head left edge is x ~30 at g1733, x 0 from g1735; at g1742 the left eye is half cut at x 0 and the left cheek is cropped. Before the punch the head is OK on the left (x ~110-180 at g1683-1710) but the ear/right side reaches x ~330-380 (> 0.45 = 324). Fix: truck 120 px right at the punch so the whole head lies in x 58-324 (scale the head 0.9 if it can't fit) and hold through g1742.
3. g1683-1730 - soldier outside x 0.65-0.90. His helmet/body span x ~590-720 (0.82-1.0) at g1683-1720 (g1683: helmet x 590-715, right shoulder touching the frame edge); only from g1736 does he drift to x ~0.62-0.85. At g1683-1730 he is clipped by the right edge together with his torso. He is behind the ox's rear (good) and the tail/flame are in front of him (good), but he is FRONTAL: head square to the lens, eyes toward the camera, torso front-on, not front-3/4 toward the ox (g1683, 1700, 1720, 1742 crops). Fix: put him at x 0.65-0.88 for the whole take (move ~80 px left at g1683-1730, hold it after the punch) and yaw him 35-40 deg toward the ox with his eyes on the ox.
4. Ground about 36 % - over the 30 % gate. Measured: ground-colour pixels (no ox, no figure, no sky/wall) below y 0.50: g1683 38 %, g1695 37 %, g1710 38 %, g1725 35 %, g1731 36 %, g1735 31 %, g1742 33 %. Ground edge is at y ~0.57-0.62; the bottom ~35 % is smooth salmon dirt with a few faint pebbles and a shadow streak. No dark fg prop, not dark foliage, so not "dressed". Team says about 45 %; it is 31-38 %. Fix: tilt the camera down 4-5 deg so the horizon is at y ~0.50 (also lifts the mouth, helping blocker 1), or add dark lit fg props (dropped shield, sacks, barrel) in the lower corners the whole take; target <= 25 %.

## Passed
- Tripod brazier: GONE. At g1736-1742 x > 0.80 there is only the wall ladder (dark navy rails with rungs, g1739/1742 at x 650-720, y 390-620) and the tail flame. No tan tripod legs, no navy cone slab. The ladder is a wall prop at the edge; fine.
- Blue sky: stays (moon, cloud streaks, deep blue).
- Flames: the herd torches and the hero's tail flame sit on the tail tip (g1736-1742 flame base at the reed tail tip, x 650-720, trailing up/back). Flame never on a face. It is clipped by the right edge at g1736-1742 (a note).
- Soldier is not between the lens and the tail/flame (the tail reed crosses in front of his chest at g1683-1742).
- No pulsing (one held punch at g1731), mouths held (rage mouth open, the soldier's "O" fixed), no text, no placeholders.
- Frame diff (my re-measure, 90x160): median 11.46, p90 15.76. OK.

## Notes
- The glint star at g1732-1737 is big and sits on the horn root/coat, not a blade tip; it hides the head's left edge at g1735-1737. Optional.
- The soldier's face is partly hidden by the ox's tail/head at g1739-1742; still readable.
