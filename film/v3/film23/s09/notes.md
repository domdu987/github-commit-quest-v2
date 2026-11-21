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
