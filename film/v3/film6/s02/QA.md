# s02 QA: film 6, shot 2 (ECU: the extra loaf lands, steam puffs), bakery MORNING

Delivered `take.mkv` = g 57..113 (57 frames, 720x1280, 12 samples, libx264rgb crf 6, first_g 57): g 57..62 in-handle, **g 63..107 = shot 2**
(plan 2.10-3.60 s), g 108..113 out-handle (all rendered in 3D). transition_in = **cut** (from s01). Also meta.json, cues.json, contact.jpg,
compare.jpg (g 76 vs ref a t0022 jar insert, g 100 vs ref a t0004 dragon ECU), shot.py, deliver.py, take.json; numbers in `work/qa.txt`.

## What happens
- Slow push-in + slight tilt over the whole take (never static): s01's customer basket (same card, same world place, 12 loaves) on the
  inside counter, the oven chimney breast and shelves behind.
- g 66 the **13th loaf (paler: cast6.loaf_svg recoloured lighter, continuity "the 13th is the pale one")** drops in from the top of frame,
  lands on the top of the pile at **g 74** ("ที่สิบสามลง" 2.23 s = g 70), squash/stretch settle g 75..78.
- g 74..99 a cartoon steam puff blooms off it (crisp-edged white puffs + curling wisps, rising, fading); from g 80 thin wisps keep rising
  (24-frame loop) through the out-handle. Set steam 0.5 (thin ribbons elsewhere).

## Client rules
- No depth of field (Take.no_dof at build and before every render); everything sharp, steam drawn crisp (no blur).
- No heads / actors in this insert -> no mouths; the loaf + puff sit at y 590..300 px (above the caption band); basket body
  reaches y ~950 (it is the object, not a head).

## Numbers
- 18.1 s wall / 33.4 s CPU per frame (2 threads, two processes). No retried / black / magenta frames, no pops.
- Near-still pair only g 57->58 (start of the eased push, first handle frame).
- Hue: red 48 orange 47 magenta 5, sat 0.44 val 0.61 dark 0.02 -- the bakery set's warm look (same as s01 44/44); blue 0 (no window
  in this ECU). Not graded here.

## Differences from the plan
- No kit hand in the ECU: the loaf falls into frame (kit's drop was already shown in s01's medium).
