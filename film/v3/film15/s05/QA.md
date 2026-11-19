# QA s05 (film 15, shots 5-9, g184-488, take first_g 176, 319 frames incl. 8 dissolve-in + 6 tail handles)
Render: 720x1280, 12 samples, ~12.4 s/frame wall per process (2 processes x 2 threads). Set A GOLDEN, cast15 cards, per-frame camera drift (slide + push + sway + eased punch pulses).
## motion_check (cuts 246,344,398,424)
```
frames 319  in-shot diffs 306  median 7.0  p90 13.9  (target median>=4, p90>=12; film 2: 5.3/19.1)
  shot from g176: median 2.6 p90 2.9  LOW
  shot from g184: median 6.6 p90 13.8
  shot from g246: median 6.6 p90 12.9
  shot from g344: median 8.8 p90 17.3
  shot from g398: median 6.7 p90 14.9
  shot from g424: median 8.4 p90 17.3
  shot from g489: median 5.3 p90 5.5
```
Overall median 7.0, p90 13.9 (targets >= 4 / >= 12). Handle frames (g176-183, 489-494) are low by design.
## qa_auto: PASS (QA_AUTO.md, phone_sheet.jpg). Notes: "no visible change" at 246/344/398 are same-scene cuts.
## Per shot
- 5 (184-245): high wide crane, coach on bleacher, Dick/boys at run-up, boy1 straddles over the bar; camera pulls back + whip pulses. Plan camera replaced (closer, lower) so cards read.
- 6 (246-343): side 3/4 (camera moved from run-up side to the left): boy1 and boy2 straddle-roll cleanly, land in sawdust, sit up, walk off.
- 7 (344-397): Dick straddles, knocks the bar (bar_fall at g380), tumbles into the pit.
- 8 (398-423): bar bounces, Dick sits up sheepish with chips. FG sawdust-edge prop dropped (it filled ~35 % of the frame).
- 9 (424-488): Dick waits, runs the curve, flops backwards over the bar, lands. Bar on pegs (cut from 8).
## Differences from plan / known
- Shot 5 crane is lower than the plan camera; shot 6 camera relocated; shot 9 flop arch is small at the high-angle orbit.
- Mouths: all still (no quote window in this take). Heads above y 880 in all frames checked on the contact sheet.
- Shot 8 Dick's head is large (camera close to the pit by plan).

## r2 polish (director notes)
- Shot 6 g246-258: boy1 now in frame at the cut (run starts nearer the camera, slower approach); shot 6 slide raised (p90 12.9).
- Shot 7 g344-360: Dick waits at his mark in frame and takes a short run; camera slide sign flipped so he starts near centre.
- Shot 9 g448-488: sustained push-in (+3 m) so the flop arch spans most of the frame width; Dick sits nearer the camera, the bar clears his neck (hair tufts touch the bar line at g488).
- Optional shot 8 bar bounce not changed.
