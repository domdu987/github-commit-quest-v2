# s13 QA: film 23, shot S13 (LANE, DAY)

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


## Frame budget
g0 1368, g1 (planned) 1503, g1_render 1537 (planned x 1.25 tail), first_g 1368 (in-handle 0), n_frames 170, transition_in cut 0 f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (83.5 MB, split in 40 MB parts: `cat take.mkv.part* > take.mkv`).
Render cost: 16.1 s wall / frame (2 threads, two renders at once), 31.7 CPU s / frame.

## Automatic QA (all run on take.mkv)
- `ground_check --every 10`: checked objects: 45   rows: 810   FAIL rows: 0   **result: PASS** -> GROUND.md
  - checked objects: 45   rows: 810   FAIL rows: 0   **result: PASS**
- `qa_auto.py take.mkv --first_g 1368`: QA_AUTO PASS  (_tmp_S13.mkv, 170 frames, 30.00 fps, g 1368-1537) (QA_AUTO.md, phone_sheet.jpg)
- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `overall median jitter px 0.13`
- frame diff on 90x160 grey, in-shot frames: median 1.83, p90 2.39 (rule: >= 4 / >= 12), min 0.88
- shade hue (ghost_hue.shade_hue, rule 240-260): first g1368 = 258.0 (shaded share 0.09), mid g1435 = 253.6 (shaded share 0.08), last g1537 = 250.9 (shaded share 0.06)
- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):
  - cya: centre y 399 .. 518, x 248 .. 279, head width <= 157 px  (bottom of the head <= 597)
  - cyb: centre y 472 .. 671, x 341 .. 408, head width <= 184 px  (bottom of the head <= 763)
  - lf0: centre y 268 .. 428, x 339 .. 362, head width <= 82 px  (bottom of the head <= 469)
  - lf1: centre y 333 .. 465, x 196 .. 236, head width <= 111 px  (bottom of the head <= 521)
  - lf2: centre y 275 .. 432, x 523 .. 688, head width <= 87 px  (bottom of the head <= 475)
  - lf3: centre y 345 .. 472, x 483 .. 634, head width <= 120 px  (bottom of the head <= 532)

Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`.
