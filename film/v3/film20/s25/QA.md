# QA s25 (shot 25, g 1814..1911; take g 1810..1915)
RESTO resto_table DAY 1889, callback of shot 2: fork bite, chew, a sip of wine (glass raised ~g 1870-1898), fork again; napkin; eyes closed in bliss. Camera starts at the framing where shot 2 ended (head ~140 px, girders + Paris visible), pushes 15 %/s with slide and orbit; SNAP PUSH x1.6 g 1836..1851 on "แทบทุกวัน" (event g 1838) to head ~270-310 px.
- Checked at 6 fps + cut sides: head centre y 658-686, bottom max 819 (< 880); no mouth movement (smile); qa_auto PASS.
- The head is large at the end (312 px wide) but entirely in frame (x <= ~540).
- Frame-diff median 4.19, p90 9.43 (target 4 / 12): median passes, p90 under (post-snap drift only).
- s/frame 11.5 wall / 21.3 cpu. First pass (push 8 %/s) scored 3.3/8.1 and was re-rendered.
- GOTCHA: cap_g("แทบทุกวัน") matches the 5.24 s caption first; the event is g_of(61.15) = 1838.
