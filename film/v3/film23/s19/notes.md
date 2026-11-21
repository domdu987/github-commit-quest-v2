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
