# s07 QA: film 4, shot 7 (kenta sets the top storey loosely, no nails), pagoda set v2, DAY

Delivered: `take.mkv` = `frames/g_0347.png .. g_0479.png` (133 frames, 720x1280, 12 samples, 2 threads, no captions, no audio);
`meta.json` (first_g 347, n_frames 133, transitions, parts, DOF), `cues.json` (10 cues), `contact.jpg`, `compare.jpg`.
Scripts: `shot.py`, `take_cfg.py` + `deliver.py` (QA numbers in `work/qa.txt`). Raw renders + json in `raw/p1..p3`.

Shot 7 = [354, 480) (11.81 .. 16.00 s). In-handle g 347..353 (7A camera already orbiting) for the 10-frame dissolve from s06 (mixed
g 349..358; s06's out-handle covers 354..360; handle frames are raw). Hard cut out to s08 at g 480 (new sentence), no out-handle.

## Timing
| part | g | what | ref a |
|---|---|---|---|
| 7A | 347-401 | medium: kenta on a scaffold deck beside the pagoda at the top storey's level, both fists on the hoist chain, paying it out hand over hand; the top storey hangs on four ropes behind / above him and comes down 1.6 -> 0.2 D (eased), swinging a little; orbit 30 -> 18 deg yaw | t0017-t0021 (orbit round the object) |
| 7B | 402-441 (cut) | insert raking low over the third storey's roof: a bare dowel peg on the roof ring, the top storey's balcony deck (bunting) settles over it, touch-down g 417 (plan 13.8 s) with a 0.03 D bump, then a loose wobble (x +-0.055 D, decaying) - no nail, no hammer | t0023 / t0025 |
| 7C | 442-479 (cut) | medium from the south-east: ropes gone, the storey sits loose and still rocks faintly; kenta lifts both open hands on "ไม่ตอกเลย" (g 454-460), shakes his head, then a small smirk | t0025 |
Framing changes g 354 (dissolve), 402, 442: 1.6 s (orbit throughout), 1.33 s, 1.27 s. The camera moves in every frame.

## Staging (work/qa.txt)
| part | head | width px | centre x | centre y (H) | below 880 |
|---|---|---|---|---|---|
| 7A | kenta | 150 -> 159 | 366-415 | 0.55-0.57 | none |
| 7C | kenta | 146 -> 166 | 262-275 | 0.52-0.53 | none |
head_flip False (DAY key screen-left in 7A and 7C). Kenta's mouth: static clench (7A), frown -> smirk (7C, a swap at g 468, no talking).
Popcheck: pops only at the two cuts (401->402, 441->442). No near-still transitions, black / magenta frames, retries or clipped sprites.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s07 part 1 (g 347-401)                          5.9   15.6    0.0    0.0    0.0   73.0    4.1    1.4  0.50 0.61 0.03
s07 part 2 (g 402-441)                         24.0   21.9    0.0    0.0    0.0   20.4   23.3   10.5  0.37 0.48 0.16
s07 part 3 (g 442-479)                          4.6   19.8    0.0    0.3    0.0   71.8    2.6    0.9  0.47 0.64 0.02
s07 all (g 347-479)                             8.9   18.2    0.0    0.1    0.0   62.7    7.2    2.9  0.45 0.58 0.07
ref a t0017 t0023 t0025                        23.0   48.9    2.0    0.0    0.0   18.0    3.4    4.6  0.33 0.39 0.20
```
7A / 7C are high exteriors against the sky (blue ~72). 7B magenta 10.5 comes from the red bunting and the red balcony posts in
violet shade (looked at full size: reads red / violet, no magenta cast). Accepted, not regraded.

## Seconds per frame
11.19 s wall / 22.1 s CPU mean (2 threads). Per part: 7A 10.2 / 20.0, 7B 14.0 / 27.5 (DOF + close set geometry), 7C 9.6 / 19.5.

## Differences from the plan / the reference
- Plan: "cutaway_insert -> street_eye". The story beat (lowering a storey loosely) needed a high vantage, so: custom cameras on a
  runtime scaffold at the top storey's level (7A / 7C) and a custom raking insert over the third roof (7B). No street_eye.
- The storey that is lowered is the top one (storey_4 pivot keyed in z / x / roll; everything parented to it follows, incl. the hanging
  pillar, its lanterns and bells). shot.py adds: the scaffold, four dowel pegs on storey 3's roof ring, peg holes under storey 4 and four
  hoist ropes (hidden in 7C). The hoist itself is never in frame (ropes and kenta's chain run out of the top of frame).
- At rest after this take the top storey is back at its set position (offsets only decay to +-0.012 D in 7C).
