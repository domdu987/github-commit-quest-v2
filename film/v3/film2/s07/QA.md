# s07 QA: film 2, shot 7, tower set DAY (bell chamber, eye level)

Delivered: `take.mkv` (frames g 441..541, 101 frames, `first_g` 441, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), `meta.json`, `cues.json`, `contact.jpg`. Take script `shot.py` (ropes and CLI from `../s04/shot.py`), delivery `deliver.py` (helpers `../s04/tk.py`). Raw renders + per-frame json (gitignored): `raw/s7`. Numbers: `work/qa.txt`.

## Timing
| event | g | s |
|---|---|---|
| in-handle (10-frame dissolve in from shot 6) | 441-447 | 14.70-14.90 |
| shot 7 starts: baker (left), nico (middle, smallest), woman (right) haul their ropes; slow bell swing (14 deg, 48-frame cycle) | 448 | 14.93 |
| "เด็กดึงเชือก": nico's big haul down | 459-466 | 15.30-15.53 |
| the rope shoots up and lifts him off his feet (dangling legs, shocked face), peak 0.62 D at "ระฆัง" (g 482) | 469-482 | 15.63-16.07 |
| snap push / tilt onto nico in the air (10 f, quint) | 472-482 | |
| hangs and kicks, bobbing on the rope; the adults turn and stare (stunned) | 482-506 | |
| drops back on "น้อยที่สุด" (g 506), squash on landing | 506-512 | 16.87-17.07 |
| hauls again and is lifted again (0.45 D) into the out-handle | 520-541 | |
| out-handle (10-frame dissolve into shot 8) | 535-541 | 17.83-18.03 |
Framing changes: 448 (drift), 472-482 (snap), 506-512 (camera follows him down), 524 (push resumes, tilt up with the second lift): gaps 0.8, 0.8, 0.6, then 0.6 s to the cut. The camera tilts up with his lift (smoothed, a little late), so his head stays in the band.

## Camera (fastest of 9 screen points at 8 D)
min 0.53, median 4.2, peak 58 px/frame (g 512, following the drop). Static runs: none. Constant-speed runs: none.

## Staging (raw/s7/g_*.json)
| head | width px | centre y (H) | lowest head bottom |
|---|---|---|---|
| nico (main) | 188-253 | 0.35-0.58 | 863 px |
| baker | 188-269 | 0.31-0.56 | 844 px |
| woman | 199-264 | 0.36-0.57 | 852 px |
All three stand on one line (y -0.3 / -0.15), so nico reads as the smallest (0.79 of the adults). head_flip False (sun from screen-left). Ropes: three 3D ropes with striped sallies, 0.10 D behind each card; nico's rope carries him (his feet leave the floor by the rope's rise; the dangling-leg drawing is placed 0.32 D higher, STORY2_META lift). Hand pins: max solve error 0.059 D. No talking: nico's "shocked" face (round eyes, open "o") is held while he hangs, clench otherwise.
Popcheck: no pops, no near-still transitions, no black / magenta cards, no retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s07 shot 7 (g 441-541)                         12.8   40.3    0.2    2.2    4.1   32.7    4.1    3.5  0.41 0.51 0.24
```
Violet, magenta, saturation, value in band; orange 40 just above, blue 33 just above, red 13 under (the chamber's wood floor and ochre arch read orange, the sky through the north arch and the shaded stone blue), darks 0.24 (the beamed ceiling and the bell interior) above 0.15. The set's own DAY chamber_eye still measured red 13.9 / blue 44 / dark 0.29: this take is closer to the band than the empty set. Shade reads blue-violet.
Seconds per frame: 15.0 s wall / 28.8 s CPU mean (two render processes on the machine).

## Differences from the plan
- The two adults are the baker and the woman (padre is not in this shot; he laughs in shot 9).
- The lift is 0.62 D (not higher): a bigger lift put nico's cap into the bell rim.
- Frames g 469-541 were re-rendered once with the follow-tilt (the first render had nico's head at 0.27 H while hanging).
