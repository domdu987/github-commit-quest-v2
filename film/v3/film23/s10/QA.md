# s10 QA: film 23, shot S10 (CAMP, NIGHT)

## What is in the take
S10 "count (radio, fake insignia)", CAMP night. Side-tracking from the radio tent out to the second truck. Real cast23 cards, no placeholders: radio man
(`gi_radio_talk`: handset at the ear, a HELD talk drawing, not lip-sync; sway, blinks), painter (`paint_frame`: the brush sweeps, white paint on the hands, at the
truck bumper with the fresh star badge), a GI carrying a crate (`gi_carry_pump`, bob + blinks). Night tint `#c8ccf0` / ink `#1e142e`. Lanterns flicker
(`GH.flicker` every frame). All mouths are held drawings (no quote in this shot). Everyone stands on the grass with a contact shadow (`GH.contact_shadow`).

## QA_ART_SET per-shot notes for S10
- **Crate text out of y 880-950: done.** The crate whose "U.S. ARMY" text sat at y ~930 is the set crate `crate.019`; it is moved 1.6 D nearer the lens after the build
  (and re-snapped). The text is now at y ~1000-1140 on every frame where it is visible (see contact.jpg: text below the cyan line).
- **Tent wall dressed: done.** The flat orange back wall of the radio tent (the glowing `tent_in` face) now carries four radio sets (olive boxes, front panel, three
  glowing dials and a red lamp each) and a pinned map (PIL-painted: grid, coast, red and blue arrows, unit boxes). Runtime only (`dress_tent_wall`), the set module is not edited.
- Camera: the set's end pose is slid 2.2 D to the left so the painter ends near mid frame instead of at the left edge.
- Radio man and painter enter / leave the frame on purpose (side track): head x outside 0..720 only on frames where the figure is off screen.
- **Deviation (camera rhythm numbers):** frame-diff median 3.05 / p90 4.34 against the film-2 targets 4 / 12. The move is the set's eased side-track (about 40 px/s lateral
  with 6-10 %/s change), no shake, jitter 0.19 px median; the night scene is calm and the tail is 25 % extra. No quick punch-in was added to this take.


## Frame budget
g0 1050, g1 (planned) 1191, g1_render 1227 (planned x 1.25 tail), first_g 1050 (in-handle 0), n_frames 178, transition_in cut 0 f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (48.5 MB, split in 40 MB parts: `cat take.mkv.part* > take.mkv`).
Render cost: 15.4 s wall / frame (2 threads, two renders at once), 26.8 CPU s / frame.

## Automatic QA (all run on take.mkv)
- `ground_check --every 10`: checked objects: 41   rows: 779   FAIL rows: 0   **result: PASS** -> GROUND.md
  - checked objects: 41   rows: 779   FAIL rows: 0   **result: PASS**
- `qa_auto.py take.mkv --first_g 1050`: QA_AUTO PASS  (_tmp_S10.mkv, 178 frames, 30.00 fps, g 1050-1227) (QA_AUTO.md, phone_sheet.jpg)
- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `overall median jitter px 0.19`
- frame diff on 90x160 grey, in-shot frames: median 3.05, p90 4.34 (rule: >= 4 / >= 12), min 0.18
- shade hue (ghost_hue.shade_hue, rule 240-260): first g1050 = 240.3 (shaded share 0.26), mid g1120 = 246.2 (shaded share 0.31), last g1227 = 241.5 (shaded share 0.52)
- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):
  - radio: centre y 605 .. 628, x -174 .. 335, head width <= 62 px  (bottom of the head <= 660)
  - paint: centre y 613 .. 641, x 340 .. 1041, head width <= 92 px  (bottom of the head <= 687)
  - sold: centre y 636 .. 663, x 17 .. 673, head width <= 88 px  (bottom of the head <= 707)

Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`.
