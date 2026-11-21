# s11 QA: film 23, shot S11 (LANE, DAY)

## What is in the take
S11 "bikes", LANE day, dissolve 13 in (in-handle 9 frames, g 1182-1190; the camera is extrapolated backwards from its start velocity so it is already moving). Side tracking
with two French cyclists along the lane behind the low hedgerow (the real 3D hedge fills the lower third as the planned foreground frame). Real cast23 cards: `fr_beret`
(green bike, baguette in the basket, pedals: `ride_frame` phase = g / 14, wheels spin, cranks turn) and `fr_cap` (maroon bike), riding at 4 D/s side by side 3.4 D apart,
heads turned toward each other (`look` 0.3), blinks and head rolls. They chat: the beret man's mouth is the HELD `talk_a` drawing, the cap man's a held smile
(no quote in this shot: no lip-sync). Contact shadows on the lane; wheels on the dirt (`C.gz`: set surface minus 3.5 cm).

Camera: the set's side-track (start (7.4,-88,3) -> end (7.6,-75.6,3), 24 mm) with the lens tightened to 34 mm at runtime (`T.tweak`) so the riders read at head ~70-86 px
instead of tiny at the left edge (first draft: head 55 px, one cyclist cut by the left edge). The camera stays behind the hedge. The cyclists ride at a constant 4 D/s and stay at
x 183-489 of 720 on every frame (head centre y 647-686, bottom <= 730).
- Deviation: frame-diff median 4.44 (rule >= 4) but p90 5.36 (rule >= 12): a steady side track with no quick punch-in. The sky takes the upper 45 % (the horizon sits mid-frame).


## Frame budget
g0 1191, g1 (planned) 1284, g1_render 1308 (planned x 1.25 tail), first_g 1182 (in-handle 9), n_frames 127, transition_in dissolve 13 f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (45.6 MB, split in 40 MB parts: `cat take.mkv.part* > take.mkv`).
Render cost: 10.7 s wall / frame (2 threads, two renders at once), 20.0 CPU s / frame.

## Automatic QA (all run on take.mkv)
- `ground_check --every 10`: checked objects: 40   rows: 560   FAIL rows: 0   **result: PASS** -> GROUND.md
  - checked objects: 40   rows: 560   FAIL rows: 0   **result: PASS**
- `qa_auto.py take.mkv --first_g 1182`: QA_AUTO PASS  (_tmp_S11.mkv, 127 frames, 30.00 fps, g 1182-1308) (QA_AUTO.md, phone_sheet.jpg)
- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `overall median jitter px 0.32`
- frame diff on 90x160 grey, in-shot frames: median 4.44, p90 5.36 (rule: >= 4 / >= 12), min 1.60
- shade hue (ghost_hue.shade_hue, rule 240-260): first g1182 = 251.6 (shaded share 0.11), mid g1237 = 253.8 (shaded share 0.12), last g1308 = 244.7 (shaded share 0.13)
- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):
  - cya: centre y 646 .. 663, x 378 .. 488, head width <= 71 px  (bottom of the head <= 699)
  - cyb: centre y 658 .. 686, x 183 .. 327, head width <= 86 px  (bottom of the head <= 729)

Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`.
