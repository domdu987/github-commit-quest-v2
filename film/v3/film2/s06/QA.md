# s06 QA: film 2, shot 6, vault set LANTERN

Delivered: `take.mkv` (frames g 351..454, 104 frames, `first_g` 351, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), `meta.json`, `cues.json`, `contact.jpg`. Take script `shot.py` (CLI shared with s04), delivery `deliver.py` (helpers `../s04/tk.py`). Raw renders + per-frame json (gitignored): `raw/s6`. Numbers: `work/qa.txt` (gitignored, reproduced below).

## Timing
| event | g | s |
|---|---|---|
| in-handle (12-frame dissolve in from shot 5), dolly already moving | 351-358 | 11.70-11.93 |
| shot 6 starts | 359 | 11.97 |
| low dolly along the left barrel rows toward the door (sine, 0.25 constant-speed share) | 351-384 | |
| eased reframe onto the soldier on guard, he turns his head a little toward us on "ทางการเก็บ" (g 388) | 384-405 | 12.80-13.50 |
| snap in onto the crossed-cannon stencil (10 f, quint; streaked g 408-414) on "ดินปืนไว้" (g 405) | 405-415 | 13.50-13.83 |
| "เกือบ 90 ตัน" lands on the insert (stencil centred, x 375 y 656) | 424 | 14.13 |
| slow push on the stencil to the end + out-handle (10-frame dissolve into shot 7) | 415-454 | |
Framing changes: 351 (dolly), 384 (reframe), 405-415 (snap), 424 (insert settles into the slow push): gaps 1.1, 0.7, 0.6 s, then a 1.0 s push to the cut at 448.

## Camera (fastest of 9 screen points at 8 D)
min 1.15, median 7.4, peak 857 px/frame at g 410 (the snap swings past the soldier: frames 408-414 carry a horizontal streak, 22-140 px). Static runs: none. Constant-speed run: g 363-371 (9 frames, middle of the dolly's sine segment, speed within 2 %).

## Staging
Soldier (soldier_guard, breathing squash, blinks, head turn) at the set's soldier_mark (-1.05, -9.1): head 128 -> 277 px wide as the dolly closes in, centre y 0.37-0.42 H on g 351-409 (0.31 / 0.12 only on the streaked snap frames 410-411), lowest head bottom 638 px. head_flip False (lantern key from screen-left). Mouth closed throughout. Stencil: on screen (377, 659) at g 416, (375, 656) at g 424, (360, 635) at g 454.
Popcheck: no pops; no near-still transitions; no black / magenta cards; no retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s06 shot 6 (g 351-454)                         45.1   33.1    0.4    0.0    0.0   12.5    1.4    7.6  0.41 0.46 0.09
```
Lantern interior: orange, violet, magenta, saturation, value and darks in band; red 45 above the 30-41 band and blue 12.5 under 14 (the insert half of the shot is filled by the lit barrel head and brick; the set's own 4-camera average was red 40.6 / blue 16.3). Shade on the floor and barrel sides reads blue-violet.
Seconds per frame: 13.7 s wall / 26.3 s CPU mean (with a second render process on the machine).

## Differences from the plan
- One camera move instead of two set-ups: dolly_barrels -> soldier reframe -> snap to barrel_insert, so the take has no internal cut.
- The barrel_insert camera ends 2 % closer than the set's pose (slow push).
