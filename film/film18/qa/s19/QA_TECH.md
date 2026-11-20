# QA-tech round 12 s19: FAIL
Checked: 6 fps g1427-1514 (contact sheet), every frame g1450-1490 (crops x220-720, y640-940), 2x zooms of g1456/1458/1460/1462, full-size g1458/1470/1484 with y 860/880 lines. Method: eyeballed on rendered pixels; no automatic face/flame segmentation available (no scipy/cv2), so gap numbers are zoom estimates (+-5 px).

## Blocking
1. Flame-to-horn/face rule (>= 15 px gap, no overlap) is violated. The small "tail flame" of the OX BEHIND sits on the horn/head of the ox in front, because the herd is dense and flames are at head height:
   - g1456, g1458: flame overlaps the front ox's right horn tip (gap 0, overlap ~10-15 px; horn tip runs into the flame's tail-torch).
   - g1460: gap ~5 px to the horn tip. g1462-1463: flame again overlaps the horn tip (0 px).
   - g1454-1455, g1464-1465: flame within ~5-10 px of horn / on the second ox's head.
   - g1479: flame sits on the lead ox's horn tip (0 px). g1480-1482: flame overlaps the horn/head of the second ox (0 px; ~35 px blob on the head at g1482). g1490: flame within ~10 px of the rear ox's horn.
   - Clear (>= 15 px): g1450-1453, g1466-1478, g1483-1489 (big flames well behind and above).
   The team did not run a pixel test and checked only g1436/1458/1484 -- g1458 and 1484 region is exactly where it fails. Their own measure.txt reports "flame<60 frames 68".
   Fix: for the rear ox's flame, offset the tail-flame card back along the tail by ~40-60 px in screen space (longer tail/torch) or lower the flame scale to 0.6 in g1454-1465 and g1479-1482, or shift that ox laterally/deeper by ~0.5 D so its tail tip clears the front ox's horn by >= 15 px. Then measure on rendered pixels (flame bright-orange mask vs horn/head mask) every frame g1450-1490.

## Passed hard checks
- Mouths/faces: lowest mouth chin ~855-858 (g1458, g1484 crops against the y 860 line); none seen below 860 in the dense run. Accepted (very tight, 2-5 px margin).
- Placeholders: no grey/navy untextured props; wall stones are textured, pots terracotta, fg helmet textured.
- Subject in frame: yes. Night, no text. Mouths: held roars, no lip-sync. No pulsing seen (eased dolly/truck); director 11.55 / 14.39 accepted.
- Blur g1505+: accepted (whip landing).

## Notes
- Plain ground: team claims 16-23 %. My estimate (area y>870 is ~32 % of frame, minus helmet and pots) is ~27-30 % at g1450-1490 (g1458/1484: ~29-30 %, lower third almost all bare gravel). Within the 25-30 % note band but not 16-23 %; adding a pot or two in the lower corners at g1475-1495 would fix it.
- g1484-1490: a pot at lower right clips an ox's chin/legs (team already notes it).
- g1450-1452: black Qi silhouette is large (covers ~1/4 of width) but acceptable.
