# s03 QA: film 3, shots 3-5, harbor set WINTER

Delivered: `take.mkv` = g 114..428 (315 frames, first_g 114, 720x1280, 12 samples, 2 threads). In-handle g 114..121 (8 frames for the 12-frame dissolve from s01), shots 3-5 g 122..421, out-handle g 422..428 (7 frames for the 10-frame dissolve into shot 6), all rendered in 3D. Internal dissolves mixed here (smoothstep): 3 -> 4 g 199..208, 4 -> 5 g 321..330 (raw handles shot 3 to g 210, shot 4 g 197..332, shot 5 from g 319). `meta.json`, `cues.json` (13 cues), `contact.jpg`. Scripts: `shot.py`, `deliver.py`, `qa.py` (`work/qa.txt`).

## Timing
| event | g |
|---|---|
| shot 3 street_wide push + rise (2 cubic segments, joint at "เมืองบอสตัน" g 164); a three-car El train (red-brown, cream band) runs along the east track away from the camera toward the tank | 114-210 |
| shot 4 low angle up the wall, worker climbing the caged ladder; tilt up, rim against the sky on g 255 (word g 258) | 197-255 |
| reframe right and push toward the filling pipe rising over the rim, lands g 281 ("กากน้ำตาล" g 279) | 256-281 |
| shot 5 kids in the snow in Commercial Street; kid1 winds up and throws a snowball g 372, the girl ducks; a worker walks across behind | 319-428 |

## Staging
| shot | head | width px | centre y (H) | below 880 |
|---|---|---|---|---|
| 3 (wide, exempt) | kid1, kid2, worker2 | 15-19 | 0.58-0.63 | none |
| 4 | climber (scale figure, no main head) | 76-96 | 0.32-0.60; leaves frame left in the pipe reframe | none |
| 5 | kid1 (main) | 158-202 | 0.49-0.52 | none |
| 5 | kid2 / walking worker1 | 87-98 / 68-76 | 0.52-0.55 / 0.49-0.52 | none |
head_flip per shot from the key side: False in shots 3 and 4, True in 5. Mouths do not move (static expressions).

## Camera / pops
qa.py: shot 3 min 1.24 px/frame, no static/constant runs; shot 4 min 0.25, peak 97 (pan g 267), constant-speed runs g 209-214 and 300-312, static 331-332 (last handle frame only); shot 5 min 0.32, constant-speed runs g 337-347 and 388-406 (slow drift). Popcheck: no pops; near-still pixel transitions g 281-293 (pipe hold, slow drift on a big sky area) and 317-319. No magenta / black cards.

## Colour (hue_report)
```
s03 shot 3  red 18.2 orange  2.2 blue 74.2 violet 1.6 magenta 3.2  sat 0.41 val 0.57 dark 0.04
s03 shot 4  red  1.5 orange  2.8 blue 94.2 violet 0.6 magenta 0.7  sat 0.48 val 0.56 dark 0.03
s03 shot 5  red  3.0 orange 24.0 blue 68.6 violet 0.5 magenta 1.0  sat 0.43 val 0.55 dark 0.04
ref b t0010 t0030 (exteriors) red 8.6 orange 3.4 blue 77.4
```
Winter exteriors with sky: blue-dominant like the reference exteriors (b t0010/t0030 77 % blue); shot 4 is a low angle on grey steel against the sky (94 % blue). Darks below band (sunlit wall / open sky); shade-only barrels at the foot of shot 4's opening and crates in shot 5's near left help little. Shade blue-violet, magenta <= 3.2.
Render: 10.3 s wall / 19.9 s CPU per frame mean (shot 3 9.2, shot 4 10.3, shot 5 11.2 wall).

## Differences from the plan / runtime set changes
- Shot 4 is not the set's tank_low camera: a custom camera 8 D out at azimuth -100 deg (ladder right of centre, the pipe further right). The stable (and the snow_patches object, which carries the snow on its roof) is hidden from the camera in shot 4 only (visible_camera off; its shadow on the tank stays) because it blocks this view. Life added: a worker1 card climbing the ladder cage, rivet rows, the pipe.
- Shot 5 is a custom low camera near the street end (1.6, -19.2, 1.0) rather than street_low (from y -50), so the kids are the main subject under the looming tank. The stable cannot be seen from inside the street (the east warehouse row hides it); it is visible in shot 3's wide. No horse asset exists, so the horse is only in the sound cue.
- Train built in shot.py (3 cars, ink hull), visible only in shot 3. Set seep 0.6, paint 0.
