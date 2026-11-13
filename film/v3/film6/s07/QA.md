# s07 QA: film 6, shots 7-10 (Henry + the hand balance; kit the tray boy; the steam motif), bakery MORNING

Delivered `take.mkv` = g 454..795 (342 frames, 720x1280, 12 samples, libx264rgb crf 6, first_g 454): g 454..459 in-handle (shot 7
framing), **g 460..789 = shots 7-10** (plan 15.34-26.32 s), g 790..795 out-handle (shot 10 B continues). transition_in = **dissolve**
(shot 6 is the market; if the conform cuts, start at g 460); out = cut to shot 11. Also meta.json (shot ranges, events), cues.json,
contact.jpg (24 frames), compare.jpg (g 530 vs ref a t0043 huge low face, g 630 vs t0100 mechanism ECU, g 760 vs t0097 rising smoke),
shot.py, deliver.py, take.json; numbers in `work/qa.txt`.

## Shots (framing change every 1.0-1.6 s: 506, 549, 597, 642, 681, 720, 753)
- **7 (g 454..548)** Henry from below (camera in the counter opening just above the sill, 22 mm), the hand balance in the foreground.
  A: he lowers a crumb onto the loaf pan (g 486) -> the beam swings from -2 (short) to +2.2 (too heavy). B (g 506, from the left, low):
  he plucks the crumb back (g 520, beam back to -2), squints at it in front of his face and snaps it in half (g 538; half-crumb drawing).
- **8 (g 549..641)** A: level camera across the beam, Henry behind it; his hand (two fingers out) lowers the HALF crumb (g 572), the beam
  wobbles +0.8 / -0.3 / +0.1 and settles EXACTLY level at g 606, held level through "ไม่ขาด ไม่เกิน" (g 611..645). B (g 597): tight
  on the pivot and pointer, perfectly level, Henry sighting along it with one eye shut, then a smug nod (g 620..633).
- **9 (g 642..719)** A: bakery_wide-like (camera started just past the window shaft, see below), kit tiny scrubbing an iron tray beside a
  wash tub (bubbles) and a stack of dirty trays, oven roaring (1.3), steam off the table. B (g 681): closer on kit; g 704..712 he
  looks round toward the steaming table, smiling.
- **10 (g 720..795)** A: kit's chin on the far edge of the table, dreamy (happy eyes), watching white wisps rise off the loaves.
  B (g 753): ECU of the loaves with big cartoon wisps + set steam 0.9, the camera tilting up with the rising steam = the steam motif
  planted clearly (paid off at 86 s).

## Client rules
- No depth of field anywhere; all sharp (steam drawn as crisp strokes, no blur).
- Heads above the caption band: henry centre y 486-646 (0.38-0.50 H), head 291-438 px; kit (9) y 606-703 (0.47-0.55 H; wide);
  kit (10) y 553-559 (0.43 H). No head bottom below y 880.
- Mouths: no quoted line in 7-10 -> only static expression mouths (unimpressed, determined, wink, smug, neutral, happy). No lip-sync.
- Steam near faces: shot 10 A keeps the set steam at 0.45 and only two wisp cards (on loaves away from kit's face); a thin set
  ribbon passes the left edge of his face.

## Numbers
17.6 s wall / 34.4 s CPU per frame. Pops only at the 7 planned framing changes; near-still pairs only on the last eased frame of a
part (504, 547, 595, 640; one pair each). No black / magenta / retried frames.
FIXED: shot 9 A first final had a global exposure step at g 658 -> 659 (the camera dolly crossed the window's camera-only sun-shaft
sheet); the path now starts past the sheet and g 642..680 were re-rendered (luma steady 111-115).
"cycles ERROR Failed to load 2 image files" in the logs from g 642 on = the hidden (hide_render) Henry card in shots 9-10 having no
sprite for those frames; harmless (he is not rendered).
Hue (all): red 41 orange 49 magenta 6, sat 0.41 val 0.59 dark 0.05: the bakery set look (as s01). Not graded here.

## Differences from the plan
- Shot 7 "adds a crumb, removes a crumb" extended into shot 8: the half crumb is what makes the beam exactly level.
- Shot 8's "fat fingers": the cast's ball hand with fingers_l = 2 (pinch).
- Shot 9 uses a camera 0.2 D off the bakery_wide preset (sun-shaft crossing, above); kit's tray / stack / tub are drawn 2D prop cards.
- Shot 10 kit is placed on the table's far side (5.62, 4.0) with a hidden crouch (feet z -0.2) so his chin rests on the table top.
