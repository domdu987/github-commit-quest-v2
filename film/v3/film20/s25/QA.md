# QA s25 (shot 25, g 1853..1911; take g 1849..1915)
RESTO resto_table DAY 1889, callback of shot 2 from the same table: fork bite, chew, a sip of wine (glass raised ~g 1891-1911), napkin, blissful. Starts at the framing where s02 ended (head 143 px, girders + Paris), pushes 15 %/s with slide + orbit; SNAP PUSH x1.6 g 1877..1892 on "ที่เดียว" (event g 1879) to head ~285 px (22 % of frame height).
- Colour (QA §G): runtime grade -0.9 EV, saturation 1.45. qa_stats: **saturation 0.564, brightness 98.5**, in-shot motion **median 4.99 p90 11.13** (deliver.py in-shot 4.42 / 11.45; target 4 / 12: median passes, p90 marginally under).
- Heads: centre y 659-686, bottom max 806; never cut; no face > 35 % of frame height. No mouth moves. Nothing floats; no bars over his face.
- qa_auto PASS. 4-frame handles each side (cut in from shot 24, cut out to shot 26).
- The shot is 58 frames (the plan moved its start from 1814 to 1853): the fork cycle and wine sip were re-timed to fit.
- GOTCHA: cap_g("แทบทุกวัน") matches the 5.24 s caption first; use g_of(t) for repeated phrases.
