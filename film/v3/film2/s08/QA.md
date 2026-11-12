# s08 QA: film 2, shot 8 (the book insert), room set NIGHT, book_insert

Delivered: `take.mkv` (g 528..604, 77 frames, first_g 528, 720x1280, 12 samples, 2 threads, libx264rgb crf 6) from `frames/g_0528.png .. g_0604.png` (not in git). g 535..604 = shot 8 ([g0, g1) = [535, 605)); g 528..534 = 7-frame in-handle for the 10-frame dissolve from shot 7 (rendered in 3D, camera already drifting). Hard cut out to shot 9 (no out-handle). `meta.json`, `cues.json` (8 cues), `contact.jpg`. Scripts: `shot.py`, `deliver.py`.

## Timing
| event | g | s |
|---|---|---|
| in-handle, top-down drift + roll over the open book (whole spread, candle top right) | 528-555 | |
| nico's right hand rests on the right page, left hand pinches the left page (breathing) | 528-552 | |
| right hand crosses the gutter to the diagram (arc lift) | 552-566 | |
| snap push-in on the diagram (quint), lands "ฟ้าผ่าชอบ" g 562 | 556-566 | 18.53-18.87 |
| fingertip taps the bolt, slides to the rod's point | 566-576 | |
| fingertip runs down the rod, along the wire, to the ground stake ("วิ่งลงเหล็ก" g 590), camera follows down | 576-599 | 19.20-19.97 |
| hard cut out | 605 | 20.17 |
Framing changes: 528 (open drift), 556-566 (push), 576-599 (follow down): gaps 0.93 s, 0.33 s, then a continuous follow. Frame-to-frame change min 0.52 / median 4.73 levels: no still runs, no pops.
Fingertip on screen (px, 720x1280): g 562 (341, 449), g 576 (373, 359) on the rod point, g 590 (432, 625) on the wire, g 599 (430, 736) at the ground stake. All diagram action sits above y 760 (captions below 880).

## Staging
No actor card: a top-down view of a vertical puppet card cannot work (stage API trap 4). Nico's hands are built in 3D in the puppet's language: ink balls (r 0.052 D) on rubber-hose ink arms (r 0.026 D), emission `#3a2832` (puppet ink), coming in from the bottom of frame (he sits in front of the stool), a short thumb stroke on the left hand and an index stroke on the right (puppet "point" hand). They cast no shadow (unlit puppets; a moon shadow uncovered a pale warm blob on the page). Candle flame emission flickers (5.0 +- 16 %).

## Colour (hue_report.row on the 77 final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 g 528-604                                   0.3    3.3    0.3    0.0    0.0   81.3    7.2    7.7  0.28 0.55 0.09   OUT: red,orange,blue,violet,sat
ref a t0080 t0088                               5.7    1.1    0.0    0.0    0.1   74.8   12.1    6.3  0.46 0.54 0.04
```
NIGHT preset: blue-dominant as expected for night (reference night 74.8 blue, 12.1 violet); magenta 7.7 (under 10), dark 0.09 in band. First final had magenta 11.9-13.0: where the set's warm candle pool (1.3, 0.95, 0.12) met the blue moon key on the white page it went pink. Fixed at runtime from shot.py (set module untouched): `R.PRESETS["NIGHT"]["pools"]` colour -> (1.15, 1.05, 0.22); the page now reads cream/grey-lavender with a warm side. Saturation 0.28 is low because the page is a big pale area (reference night 0.46).
Seconds per frame: 10.23 s wall / 19.49 s CPU mean.

## Differences from the plan
- "page flip" sfx: there is no page turn (a turning page would land showing the wrong texture); the cue is the pages settling under the left hand at the start; the real action is the finger tracing the diagram.
- Candle pool colour changed at runtime (see Colour). The candle itself is at the top right in the wide part and out of frame after the push.
