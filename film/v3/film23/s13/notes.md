## What is in the take
S13 "cover + QUOTE พวกเราอเมริกัน แข็งแรงมาก", LANE day, cut in. Medium two-shot in depth: the French cyclists in the foreground left of centre, the four lifters behind them holding the
rubber tank overhead (`tank_lift` keyed `GH.set_lift(1.0)` every frame, flagged airborne: **the only airborne tank**). Real cast23 cards. Lifters: `lift_pose` (hands exactly at the belly,
wobble, strain); the smiler (`gi_smile`, the lifter nearest the camera, big sweat drop) is the ONLY mouth that moves: **lip-sync `talk_mouth(g)` (cast6 4-6 Hz pattern with pauses) over the
quote window g 1428-1502 (shot-local 60-134, the last ~2.4 s of the estimated 4.5 s narration), `grin` outside it**. Re-render the lip-sync with real loudness if the narration drifts > 0.3 s.
Cyclists: `ride_frame` rolls up and BRAKES to a stop by shot-local frame 16 (g 1384, before the mid frame 1435), then stare (stunned face, held open mouths, sweat). On the quote's last
words (shot-local 112, g 1480) the cap man leans back (3-frame wobble) and SITS DOWN dazed, unhurt, on the grass (`fall_pose`: stars circling, bike lying beside him) while the beret man stares.
No weapons, nobody hurt.

## QA_ART_SET per-shot note for S13
- **Cyclists brake and stay in frame: done.** Cyclists were re-marked (-4.3,-36.2) / (-2.7,-37.6) on the lens axis, the camera re-aimed (start (-0.7,-45,3.6) -> (-5.2,-31.5,-1.2), 24 mm, zoom 0.10/s,
  slide -6 px/s); measured on every frame: beret man head x 249-279, cap man x 341-409 (QA: 0.15-0.85 = 108-612), centre y 399-518 standing and <= 671 sat (head bottom <= 763),
  all heads above y 860. (The first final was discarded: cyclists at x 115-190 with a flat 0.84 frame diff, seat head at y 830+.)
- Lifters' heads: y 268-472 (the camera tilts down so the tank top is cropped at the end of the push; head width 46-120 px), all above y 880.
- Shade hue: first g 1368 = 258.0, mid g 1435 = 253.6, last g 1537 = 250.9 (rule 240-260).
- **Deviations:** frame-diff median 1.83 / p90 2.39 (rule 4 / 12): the push is a steady 0.10/s lens zoom with no extra punch-in; the lower 40 % of the frame is open dirt lane (the planned
  hay fg prop is a small orange shape at the bottom left in the first half). The tank top is cut by the frame during the push.
