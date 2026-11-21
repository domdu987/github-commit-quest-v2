# s09 QA: film 23, shot S09 (CAMP, NIGHT)

## What is in the take
S09 "count (speakers, 20+ km)", CAMP night. Crane from the tank rows (high, looking down the rows under the moon) down to the sound truck, then a push toward the
flared horn. Real cast23 cards: the sound man (`gi_sound_switches`, headphones: his right hand taps the switch row on the desk in a 36-frame cycle, lean and head
roll, blinks), two guards (`gi_stand_designer`, `gi_carry_pump`: sway, blinks). The gramophone `record` on the desk spins at 33 rpm (`GH.set_record` keyed per
frame, 6.6 deg/frame), the lanterns flicker per frame. Night tint `#c8ccf0` / ink `#1e142e`. No quote in this shot: every mouth is a held drawing.

## QA_ART_SET per-shot note for S09
- **Sound man's head <= y 760 in the last frame: done.** The end of the BIGZOOM path was re-keyed at runtime (`T.tweak`): look-at z 4.8 -> 1.9 at the end key and 3.0 -> 2.6
  at the middle key, end camera z 4.2 -> 4.0, so the figure sits higher in frame. Measured head centre of the sound man: g 1050 (planned end) y 693, g 1086 (last
  frame, end of the x 1.25 tail) y 713 (head width 127 px, bottom 777). He enters the frame at g 1005 (x 712, y 766) from the right edge and stays above y 773 until the end.
  The sound man is off screen (head x / y outside the frame) while the crane is still high on the tank rows (g 896-1004): the large x / y values in QA_NUMBERS.json
  for `snd` are those off-screen frames.
- Guard `gd0` head: the sprite of the far-left guard is flagged `clipped` by the stage on the high-angle frames (upper-body stretch at the crane start); the guard is
  <= 63 px and stands at the frame edge there, the clip is not visible in the frames.
- **Deviation:** frame-diff median 4.35 (rule >= 4) but p90 6.28 (rule >= 12): the crane + push are continuous and eased, no quick punch-in was added.


## Frame budget
g0 906, g1 (planned) 1050, g1_render 1086 (planned x 1.25 tail), first_g 896 (in-handle 10), n_frames 191, transition_in dissolve 15 f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (83.2 MB, split in 40 MB parts: `cat take.mkv.part* > take.mkv`).
Render cost: 19.6 s wall / frame (2 threads, two renders at once), 35.2 CPU s / frame.

## Automatic QA (all run on take.mkv)
- `ground_check --every 10`: checked objects: 41   rows: 820   FAIL rows: 0   **result: PASS** -> GROUND.md
  - checked objects: 41   rows: 820   FAIL rows: 0   **result: PASS**
- `qa_auto.py take.mkv --first_g 896`: QA_AUTO PASS  (_tmp_S09.mkv, 191 frames, 30.00 fps, g 896-1086) (QA_AUTO.md, phone_sheet.jpg)
- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `overall median jitter px 0.25`
- frame diff on 90x160 grey, in-shot frames: median 4.35, p90 6.28 (rule: >= 4 / >= 12), min 1.44
- shade hue (ghost_hue.shade_hue, rule 240-260): first g896 = 242.3 (shaded share 0.68), mid g978 = 244.1 (shaded share 0.55), last g1086 = 244.0 (shaded share 0.63)
- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):
  - snd: centre y 692 .. 1978, x 378 .. 3564, head width <= 127 px  (bottom of the head <= 2041)
  - gd0: centre y 576 .. 1132, x 264 .. 1056, head width <= 63 px  (bottom of the head <= 1164)
  - gd1: centre y 586 .. 763, x 596 .. 1041, head width <= 43 px  (bottom of the head <= 784)

Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`.
