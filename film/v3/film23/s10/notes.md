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
