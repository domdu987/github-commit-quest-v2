# QA s23 (shot 23, TOWER tower_fair DAY 1910, g 1656..1731 + handles g 1648..1655 (dissolve in) and 1732..1739 (dissolve out into shot 24))
Checked at 6 fps contact + phone sheet.
- Heads: Eiffel_old head centre y 596-700, width 145-269 px, chin <= 786 (< 880); all frames pass head_report.
- Mouths: never animated.
- Callback of shot 15 (same two-shot in depth, official behind-right), but a PULL (10 %/s) with slide/arc/tilt drift; snap x1.9 on 'อีก 70 ปี' (g 1706).
- Document: official holds it out g 1664-1676, Eiffel takes it (g 1676), moves it to the left hand behind a blink (g 1696), then on g 1706 (blink swap: bowler off, worried -> proud smile) he holds the bowler out at chest height with the right hand.
- DEVIATION: the cast20 arm rig cannot lift a hand overhead (hand y saturates ~1.0), so the bowler is "doffed" held out beside the chest, not raised above the head.
- 1910 vs 1889: set_year(1910) differs only in the crowd/pavilion layout and the biplane (not in frame here); the 1910 read is carried by the old-Eiffel swap (white beard, stoop) and the document, as QA_TECH 17 allowed.
- Lamp-post FG shows at the left/right edge; bench out of frame.
- Frame-diff (90x160 grey, in-shot g 1657..1731): median 5.23, p90 11.10 (target 4 / 12: p90 slightly under).
