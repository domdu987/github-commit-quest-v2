# s08 QA: film 8, shots 8-9 (the wall and the dome, time-lapse): desert_ice plain, DAWN

Delivered: `frames/g_0602.png .. g_0786.png` (185 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 602, 185 frames; 61.7 MB, so it is committed as `take.mkv.partaa` + `.partab`
(`cat take.mkv.part* > take.mkv`)). g 602..607 = in-handle (dissolve in from shot 7, 8 frames), g 608..719 = shot 8 (plan 20.28-24.00 s),
g 720..780 = shot 9 (plan 24.00-26.03 s), g 781..786 = out-handle (rendered in 3D). Plan cut 8 -> 9 at g 720 inside the take.
Scripts: `shot.py` (stills / final; one build per set-up), `deliver.py` (frames, meta, cues, contact, compare, mkv, `work/qa.txt`, `work/hue.txt`).

## What happens
- **Shot 8 (g 602-719)**: 3/4 view from the channels looking ESE along the wall. Time-lapse: farid at the wall foot heaves a mud brick
  up to the wall every 15 frames (crouch to the pile -> lift -> back), while the wall rises out of the ground from 2.2 D to its full
  15 D (3 storeys) by g 712. Brick stacks, a mould, a mud heap with straw, jars, a bucket and a basket dress the strip. The camera pushes
  and cranes up with the crest (az 120 -> 124, pitch 2.5 -> 6.5, z 2.9 -> 3.1), pink-gold sunrise sky beyond, water in the channels.
- **Shot 9 (g 720-786)**: the giant stepped dome, warm-lit, finishes growing (z scale 0.62 -> 1.0 by g 762) beside the finished wall;
  farid stands proud on the bank, arms folded, small idle sway. Push + slight crane (22 mm).

## Runtime changes (desert.py untouched)
- Wall rise: the set's `wall` object is keyed in z (sunk into the ground, rising each frame). Dome growth: `dome` + `dome_vent` keyed z scale.
- DAWN key direction overridden before each build through `D.LIGHTS['DAWN']` (the materials bake the key direction): shot 8 sun from the
  north-east (11 deg) so the wall's north face is lit warm instead of a flat blue-violet shade; shot 9 sun from the north-west (13 deg) so
  the dome's face is lit (the painted sunrise glow stays behind it as a rim). User taste: warm lit set, not silhouettes.
- Channels: `ice='water'` in shot 8 (before night 1); shot 9 ice (0.06, 0) a faint frost so the water is not a blown white mirror.

## Checks (`work/qa.txt`)
| set-up | head width px | centre x | centre y (H) | below 880 |
|---|---|---|---|---|
| shot 8 (g 602-719) | 68-78 | 506-592 | 0.55-0.63 | none |
| shot 9 (g 720-786) | 69-80 | 202-277 | 0.58-0.60 | none |
Shot 8 is a medium-wide (the wall is the subject); its head centre reaches 0.63 H at the end of the crane (bottom <= 846 px).
Popcheck: one jump, the planned cut 719 -> 720. No near-still frames (median change 3.1 levels: the wall rises every frame). No
magenta / black frames, no retried frames. No DOF. No text signs. No mouth movement (no quote).

## Colour (`work/hue.txt`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 shot 8 wall time-lapse (g 608-719)         63.6    1.5    0.1    0.0    0.0   15.1   15.3    4.5  0.41 0.69 0.00
s08 shot 9 dome (g 720-780)                    54.4    4.4    0.0    0.0    0.0   14.2   18.7    8.3  0.32 0.71 0.00
ref a t0061 (sunrise)                          54.5   26.1    1.9    0.0    0.0    0.0    3.9   13.6  0.49 0.68 0.26
```
Warm red-orange mud lit by the low sun, blue-violet sky and shade; magenta 4.5-8.3 (below the sunrise ref's 13.6, the shade stays violet).

## Seconds per frame
12.7 s wall / 24.3 s CPU (shot 8), 13.8 / 26.0 (shot 9); two processes x 2 threads on 4 cores.

## Differences from the plan
- Shot 8 is a custom 3/4 camera, not the wall_low preset (the preset looks straight at a shaded wall face).
- The wall "rises" by coming up out of the ground (keyed z), not course by course; the dome grows by z scale. Time-lapse cartoon reading.
- Dawn key directions differ from desert's DAWN preset and between the two set-ups (see above).
- Farid in shot 9 stands on the bank in front of the dome (readable size) rather than at its door.
