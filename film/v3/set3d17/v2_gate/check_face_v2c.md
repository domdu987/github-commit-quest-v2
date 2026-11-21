# film 17 v2: check_face (B7), all takes

Facing error = |story face - direction to the camera| on every frame where the card is in frame above 15 %H and not on BACK_VIEW.
FAIL when > 60 deg anywhere, or > 35 deg in the STRICT windows for the speaker / hero (lip-sync g493-651 inspector, g1128-1196 inspector; BIGZOOM ends g97-148 Bertillon, g1500-1530 Bertillon; P1 g1515-1545 and 6c g1545-1616 Bertillon; P2 g1671-1695 inspector; P3 g2018-2052 inspector).
Yaw rate = the clamped card yaw change per frame on those frames (PLAN §6.1 asks <= 2 deg/frame; the higher values are close orbit passes).

| take | verdict | max facing error (deg), anchor | strict window: max error (deg), anchor | anchors | max yaw rate (deg/frame), anchor |
|---|---|---|---|---|---|
| T1 | PASS | 39 (prisoner_q) | 25 (bertillon) | 17 | 4.6 (bertillon) |
| T2 | PASS | 8 (thief) | 1 (inspector) | 13 | 2.0 (clerk_ladder) |
| T3 | PASS | 14 (prisoner_chair) | no strict window | 9 | 6.1 (prisoner_chair) |
| T4 | PASS | 25 (bertillon) | no strict window | 6 | 5.2 (bertillon) |
| T5 | PASS | 15 (gend_b) | 2 (inspector) | 5 | 3.8 (gend_b) |
| T6 | PASS | 17 (inspector) | 6 (bertillon) | 7 | 6.6 (inspector) |
| T7 | PASS | 4 (bertillon) | no strict window | 7 | 1.3 (bertillon) |
| T8 | PASS | 23 (crowd2) | 1 (inspector) | 8 | 12.3 (crowd2) |

Per anchor: `python3 prefecture17.py faces`. Face keys: `v2_gate/face_keys.json` ({take: {anchor: [[g, deg azimuth], ...]}}).
