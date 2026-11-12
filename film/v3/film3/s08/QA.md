# s08 QA: film 3, shot 8, harbor set WINTER

Delivered: `take.mkv` = g 620..752 (133 frames, first_g 620, 720x1280, 12 samples, 2 threads, libx264rgb crf 6). Shot 8 is g 620..746. Its first frame is a hard cut in. g 747..752 is the 6-frame out-handle for the 9-frame dissolve into shot 9, rendered in 3D with the camera continuing. Also `meta.json`, `cues.json`, `contact.jpg`, the scripts `shot.py`, `take3.py` (shared engine) and `deliver3.py`, and `work/qa.txt`.

## Timing
| event | g | s (film) |
|---|---|---|
| hard cut: depth two-shot. The foreman laughs in the foreground (foreman_laugh: eyes shut, tears, belly heaving, mouth held open and not animated). Tommy stands small and far off by the bucket at the tank foot. worker1 / worker2 laugh behind him | 620 | 20.67 |
| eased drift (speed change at g 641) | 620-657 | |
| snap reframe onto the foreman (10 f, quint), lands at 22.0 s (g 663). The camera orbits so tommy sits over his shoulder | 657-667 | |
| quoted line: mouth moves (talk_a / talk_b / talk_o / flat, a new drawing every 2 f), eyes smug. Mouth is flat in the word gaps g 694-695 and 708-709 | 666-741 | 22.20-24.70 |
| he swings his arm out and points at the tank on "pai ao si nam tan ma tha sa" | 706-713 | 23.53 |
| slow push with a speed change at g 700, out-handle | 667-752 | |
Before g 666 and after g 741 the foreman's mouth is a held drawing (open laugh, then smile) and does not move. The workers' mouths are held laughs.

## Staging
| head | width px | centre x | centre y (H) | below y 880 |
|---|---|---|---|---|
| foreman (main) | 208 wide -> 295 after the snap | 184-276 | 0.46-0.51 | none |
| tommy (far) | 70-83 | 400-583 | 0.52-0.56 | none |
| worker1 / worker2 (behind; leave frame screen-right after the snap) | 74-97 / 93-114 | | 0.48-0.51 | none |
Near/far head ratio is 3.0 wide and 3.6 after the snap. This is a depth two-shot, not a matched two-shot. head_flip is False (key from screen-left at camera heading -8 to -27). Nobody turns their back to the camera.

## Camera / pops
Camera speed: min 0.25, median 1.5, peak 69 px/frame at g 662 (the snap). No frame is static. Frames flagged by the frame-difference check (661-666) are the snap itself. There are no near-still frames, no retried frames and no black or magenta cards.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 shot 8 (g 620-746)                         30.4   16.0    0.0    0.1    0.0   49.3    1.0    3.1  0.34 0.55 0.09   OUT: orange,blue,sat
```
Blue is high from the WINTER sky and the long shadows. Orange is low because the steel tank reads beige, not orange. Darks (0.09) are in band thanks to the shaded barrels at the near right and the foreman's vest and shadow. Shade reads blue-violet and magenta is 3. Render time: 11.2 s wall / 21.8 s CPU per frame on average.

## Differences from the plan
- The camera is a custom base_eye: heading -8 to -27 so the key comes from screen-left, eye height 2.5. After the snap it orbits so tommy stays visible over the foreman's shoulder. The two laughing workers drop out of frame screen-right after the snap.
- In the wide part (g 620-660) the shaded barrels at the near-right edge are cut by the frame and read as a dark block in the corner.
- Set state: paint 0, seep 0.8, the bucket at bucket_mark with fill 0.55, and the animated drop at the seam. Set changes are made at runtime only, as in s06/QA.md.
