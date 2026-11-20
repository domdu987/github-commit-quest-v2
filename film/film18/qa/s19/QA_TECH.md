# QA-tech round 16 s19: FAIL
Checked: 6 fps sheet, 1:1 crops at g1476-1492 every 2 frames, ground_share step 2.

## Blockers
1. Pot over the lead jaw, g1482-1486 (previous blocker NOT fixed). The terracotta pot at lower right sits in front of the lead ox's chin/lower jaw at g1482 and g1484 (rim covers the jaw, y ~800-840) and still touches it at g1486. Fix: move the pot 150 px right or 150 px lower (rim top >= y 870), or delete it, for g1478-1490.
2. Ground: director max 0.324 (median 0.20). ground_share frames > 0.30: g1485 0.32, g1487 0.32, g1489 0.32, g1499 0.31, g1501 0.31 (5 of 44 samples, not 1-2). Fix: cover the lower ground at g1483-1501 with dark textured props or raise the horizon (the camera is leaving the wall to the open field here).

## Passed
- Ox mouths: lowest about y 823 at g1484, never > 860.
- Flame overlap: none seen (far-lane flames clear of neighbours; gaps >= 10 accepted).
- No pulsing, no placeholders, mouths held; lead exits right g1484-1488 (accepted).

## Notes
- Oxen visible per 0.5 s tile: 2-3 (lead plus 1-2 small far oxen) in g1427-1500; about 6-7 from g1507 (whip landing).
- Grey wall-breach rocks have a heavy navy outline and read slightly like low-poly lumps; textured, so not a placeholder.
- Near pots g1427-1450 are violet, not warm. Flames tiny at phone size.
