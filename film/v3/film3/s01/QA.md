# s01 QA: film 3, shots 1-2 (the hook), harbor set WINTER

Delivered: `take.mkv` = g 0..129 (130 frames, first_g 0, 720x1280, 12 samples, 2 threads, no captions or audio). g 0..121 = shots 1-2; g 122..129 = 8-frame out-handle (shot 2 camera continues, rendered in 3D) for the 12-frame dissolve into s03. `meta.json`, `cues.json` (15 cues, film seconds), `contact.jpg`. Scripts: `shot.py`, `deliver.py`, `qa.py` (numbers below: `work/qa.txt`).

## Timing (event g = round((t + 0.10) * 30); boundaries round(t * 30))
| event | g | s |
|---|---|---|
| tommy slides the tin bucket under the bucket seam (hand pinned to the rim, error 0.000 D) | 0-19 | 0.00-0.63 |
| glossy amber drop runs down the seep strip, hangs at its tip, lets go | 0-22 | |
| drop lands in the bucket (t 0.9) | 30 | 1.00 |
| snap pull-up (quint): back 10 D and tilt up, the wall + ladder tower over him, rim and sky at the top | 33-51 | 1.10-1.70 |
| hard cut to the foreman (base_eye) | 52 | 1.73 |
| two brush jabs up at the tank | 61, 69 | |
| shove: brush and paint pot thrust at tommy | 78-86 | |
| snap punch-in on the brush, lands on "สีมาทาทับแทน" (g 87) | 83-89 | 2.77-2.97 |
| slow lateral drift to the end of the handle | 89-129 | |

## Staging (raw/*/g_*.json)
| shot | head | width px | centre y (H) | below y 880 |
|---|---|---|---|---|
| 1 close (g 0-32) / after pull-up | tommy | 241-257 / 60 | 0.43 / 0.65 (wide reveal: whole head above 880) | none |
| 2 | foreman (main) | 207 -> 300 after punch | 0.37-0.50 | none |
| 2 | tommy (far) | 96-109 | 0.49-0.56 | none |
head_flip True in both shots (key from screen-right for cameras facing the bucket seam). Foreman's mouth is closed (expr angry, mouth clench) throughout; nobody's back to camera.

## Camera / pops
qa.py: shot 1 min 0.40 px/frame, peak 183 (pull-up g 41), no static or constant-speed runs; shot 2 min 0.35, peak 72 (punch g 86), no static runs, one constant-speed run g 105-113 (mid post-punch drift). Popcheck: one pop 51 -> 52 = the hard cut. No magenta / black cards, no retried frames.

## Colour (hue_report)
```
s01 shot 1 (g 0-51)    red 41.4 orange 38.2 blue 17.7 violet 0.4 magenta 2.3  sat 0.24 val 0.59 dark 0.02
s01 shot 2 (g 52-129)  red 37.8 orange 29.8 blue 28.2 violet 0.9 magenta 3.3  sat 0.30 val 0.54 dark 0.06
s01 all                red 39.2 orange 33.0 blue 24.2 violet 0.7 magenta 2.9  sat 0.28 val 0.56 dark 0.05
```
Hue families in band (lit ochre yard, warm key). Saturation low because the WINTER tank is grey steel (story: unpainted). Darks low in shot 1 (sunlit close at the wall foot); shade-only barrels at the left in the pulled-up frame and a crate stack at the left in shot 2 help a little; shot 2 also has the tank's big blue-violet shadow. Shade reads blue-violet, never magenta.
Render: 14.8 s wall / 27.4 s CPU per frame mean.

## Differences from the plan / fixes at runtime
- The set's dark drip dot is hidden; replaced by an animated glossy amber drop (gloss BSDF + painted highlight, no shadow) that runs down the bucket-seam strip (which reaches the rim at seep 1), swells, falls and enters the bucket at g 30; a second drop falls in the pull-up (lands g 60, unseen).
- Set seep = 1.0 in this take (full strips), paint 0.
- Shot 2: tommy stands beside the bucket (0.3 D right of it, 1.45 D out) rather than at hero_mark so he sits in line with the shove; the foreman is boss_mark + 0.9 D out, 0.35 D left. The foreman holds the brush in his screen-left hand and the paint pot in the other (foreman_order_paint carries no pot); custom pose, jabs then shoves.
- Shot 2 g 90..129 were re-rendered after adding a lateral drift (the first render had a static camera g 89-99 and 120-129).
