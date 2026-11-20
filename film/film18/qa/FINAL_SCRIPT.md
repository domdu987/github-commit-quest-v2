# Film 18 FINAL gate — script checks (director, 2026-11-20 20:15 UTC)
Film: release18/oxclerk_v1.mp4 (conform18.py: 25 PASSED takes by exact blob, 5 whip joins, per-shot grade, captions, mix, true-peak loudnorm)

| check | value | target | result |
|---|---|---|---|
| duration | 70.40 s, 2112 frames | 70.40 s | PASS |
| qa_stats2 saturation | 0.504 | >= 0.50 (§I) | PASS |
| qa_stats2 vivid % | 45.4 | >= 45 (§I) | PASS (marginal) |
| luma | 96.3 | 85-110 (§G) | PASS |
| in-shot motion median / p90 | 6.79 / 13.18 | >= 4 / >= 12 (film rule) | PASS |
| film 2 reference | sat 0.490, vivid 49.4, luma 94.0, motion 4.75 / 16.93 | | |
| hard cuts (plan) | 9 (+9 dissolves, 5 whips, 1 whip-in) | <= 12, target 4-10 (§I) | PASS |
| integrated loudness | -12.2 LUFS | -14 .. -11 | PASS |
| true peak | -1.1 dBTP | <= -1 | PASS |
| qa_auto frozen / black / magenta | 0 / 0 / 0.0 % | 0 | PASS |
| qa_auto blur flags | 192 frames: dissolve blends, whip streaks, extreme-wide BIGZOOM starts, dark s21 opening (all accepted at the TAKE gate) | | NOTE |
| missing frames | 6 take-boundary frames filled from outgoing handles (g1308 1387 1426 1514 1595 1806) | 0 | PASS |
