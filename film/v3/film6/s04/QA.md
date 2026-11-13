# s04 QA: film 6, shot 4 (Henry unaware in the back, kit smiles at us, flour cloud), bakery MORNING

Delivered `take.mkv` = g 174..264 (91 frames, 720x1280, 12 samples, libx264rgb crf 6, first_g 174): g 174..179 in-handle,
**g 180..258 = shot 4** (plan 6.00-8.62 s), g 259..264 out-handle (rendered in 3D). transition_in = **dissolve** (shot 3 is the
market; if the conform cuts, start at g 180). Also meta.json, cues.json, contact.jpg, compare.jpg, shot.py, deliver.py, take.json;
numbers in `work/qa.txt`.

## What happens (framing change every ~1.3 s)
- **A g 174..218** medium from the street, slight left drift (24 mm): the customer has gone, kit dusts his floury hands behind the
  counter (hidden stool, as s01); Henry in the background by the roaring oven bobs a loaf in each hand, squinting, unaware.
  On "เจ้านายเขา" (6.17 s = g 188) kit jerks a thumb (one finger out) back over his shoulder at Henry with a smirk (g 186..204).
- **B g 219..264** punch-in on kit (26 mm, slow push): smiles into the lens, claps his floury hands at **g 232** -> a cartoon flour
  cloud (crisp puffs + specks, drawn PropCard) bursts in front of his apron and drifts / fades; kit grins (expression change
  behind a blink). Henry is not rendered in B (his position would put his head half out of the left edge).

## Client rules
- No depth of field anywhere; all sharp.
- Heads above the caption band: kit centre y 527-552 (0.41-0.43 H), head 202-360 px; henry y 628 (0.49 H), 102-105 px. No head
  bottom below 880.
- Mouths: no quoted line -> only static expression mouths (happy, smirk, grinning); Henry's closed.

## Numbers
18.3 s wall / 35.8 s CPU per frame. One planned pop (g 218 -> 219 framing change), no others; no near-still pairs; no black / magenta.
Hue: red 41 orange 47 magenta 9, sat 0.42 val 0.58 dark 0.06 (bakery set look, same as s01).

## Differences from the plan
- Plan's "counter" preset replaced by s01-style custom street-side cameras (the preset puts kit at 141 px behind the board loaves).
- The flour cloud comes from a clap (kit dusting his hands), not from a sack.
