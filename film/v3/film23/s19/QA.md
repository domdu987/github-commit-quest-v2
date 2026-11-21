# s19 QA: film 23, shot S19 (LANE, DAY)

## What is in the take
S19 "ending", LANE day, dissolve 17 in (in-handle 11, g 1969-1979). Wide -> medium push that ends on the Major (head 189 px at the end, centre y 652-703). Real cast23 cards:
the Major sits on his crate, red-faced, steam from the ears, cheeks puffed, blowing balloon after balloon (`balloon_frame`, 72 frames per balloon, colour changes each
balloon); the crew grins: `gi_designer` waves at us (`wave_frame`), `gi_pump` belly-laughs (`laugh_frame` bounce), `gi_driver` grins arms akimbo. The pile (`GH.set_pile`) grows
0.70 -> 1.0 and is keyed on EVERY frame (measured 2 ms per call, so no stepping was needed). On the last word (g 2096) the last balloon leaves his hands and loops away
up-left (`balloon_loose`, the other airborne thing), the Major looks up, jaw dropped. Mouths: all held drawings (no quote in this shot).
Fix found at full size: `GH.set_loose_balloon` writes WORLD coordinates onto an object that is parented to the LANE root, so the balloon sat 700 D away (invisible) in the first
final; the script now keys the local position (`world - root`). The first final was discarded and re-rendered.

## QA_ART_SET per-shot notes for S19
- **Crate text out of y 880-950: done.** The "DECOY M4" crate is the set's `crate_chalk` (S08's chalk crate, not the fg prop); it is hidden for this shot (with its contact blob), so no crate
  text is in frame at all. The planned fg prop was swapped for a hay bale (`fg=('hay', ...)`, no text).
- **Shadow hue under the pile: done / measured.** Shade hue (ghost_hue.shade_hue) of the final frames: first g 1969 = 248.4, mid g 2044 = 249.2, last g 2142 = 250.7 (QA's 273 was the
  violet under the pile; the ground-shade hook `SH_K` is left at 1: the re-keyed camera and the pile's own colours already land at 248-251).
- Camera: the set's push is re-keyed to a nearer end pose (9.2, 1.9, 3.7) -> (10.6, 9.3, 2.6) with the lens 22 -> 30 mm (quick push-in on the last word), so the Major ends medium.
- The driver (`cr2`) is moved to (14.2, 4.4) (the set mark (17.8, 6.2) left the frame during the push); he walks out of the right edge around g 2050 (head x > 720 from then on); while in frame his head is above y 790.
- Deviations: frame-diff median 3.35 / p90 4.69 (rule 4 / 12); the lower third of the frame is open grass in the first half (the hay bale prop is out of frame at the start camera).


## Frame budget
g0 1980, g1 (planned) 2109, g1_render 2142 (planned x 1.25 tail), first_g 1969 (in-handle 11), n_frames 174, transition_in dissolve 17 f. 720x1280, 12 samples, 30 fps; take.mkv libx264rgb crf 6 (93.2 MB, split in 40 MB parts: `cat take.mkv.part* > take.mkv`).
Render cost: 13.3 s wall / frame (2 threads, two renders at once), 25.9 CPU s / frame.

## Automatic QA (all run on take.mkv)
- `ground_check --every 10`: checked objects: 144   rows: 2682   FAIL rows: 0   **result: PASS** -> GROUND.md
  - checked objects: 144   rows: 2682   FAIL rows: 0   **result: PASS**
- `qa_auto.py take.mkv --first_g 1969`: QA_AUTO PASS  (_tmp_S19.mkv, 174 frames, 30.00 fps, g 1969-2142) (QA_AUTO.md, phone_sheet.jpg)
- `qa_jitter.py take.mkv` (every second must be <= 2.0 px; it prints a line only for a second above 2): `overall median jitter px 0.11`
- frame diff on 90x160 grey, in-shot frames: median 3.35, p90 4.69 (rule: >= 4 / >= 12), min 0.10
- shade hue (ghost_hue.shade_hue, rule 240-260): first g1969 = 248.4 (shaded share 0.05), mid g2044 = 249.2 (shaded share 0.06), last g2142 = 250.7 (shaded share 0.08)
- heads (screen px, 720x1280, head centre; a head is out of the caption band while centre y + w/2 < 880):
  - maj: centre y 651 .. 702, x 256 .. 395, head width <= 189 px  (bottom of the head <= 797)
  - cr0: centre y 597 .. 609, x -338 .. 122, head width <= 149 px  (bottom of the head <= 683)
  - cr1: centre y 589 .. 603, x -30 .. 227, head width <= 95 px  (bottom of the head <= 651)
  - cr2: centre y 697 .. 860, x 444 .. 2399, head width <= 396 px  (bottom of the head <= 1058)

Contact sheet: `contact.jpg` (16 frames, cyan line = y 880); phone sheet: `phone_sheet.jpg`. Scripts: `shot.py` (probe / stills / final / ground), `c23.py`, `deliver.py`, `mkqa.py`.
