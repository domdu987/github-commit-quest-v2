# s01 QA: film 9, shots 1-2 (the hook): wall_site, DAY

Delivered: `take.mkv` split into `take.mkv.partaa` + `take.mkv.partab` (50.1 MB > 45 MB; `cat take.mkv.part* > take.mkv`). It holds 115 frames,
g 0..114 at 720x1280, 12 samples, 2 threads, OIDN FAST, libx264rgb crf 6, 30 fps, first_g 0, with no captions and no audio.
- g 0..53 = shot 1 (plan 0.00-1.80 s).
- g 54..108 = shot 2 (plan 1.80-3.62 s). It has an internal cut at g 82 (2a pour / 2b trowel).
- g 109..114 = the 6-frame out-handle, rendered in 3D.
- There is no in-handle: the take opens the film.

Also delivered: `meta.json`, `cues.json` (9 cues), `contact.jpg` (16 frames; the cyan line is y 880), and the scripts `shot.py`, `c9.py` (film8/common.py switched to cast9 + set3d9/wall.py), `deliver.py` + `TAKE.json`, `qa.py` (-> work/qa.txt), and `sheet.py`. The frames, raw and work folders stay out of git.

## Set-ups (one build: wall_site, preset `cauldron`, DAY, lin 18 / general 21; one process per set-up)
| id | g | camera | action |
|---|---|---|---|
| 1 | 0-53 | custom, closer than preset `cauldron`: (-9.0,20.8,6.1)->(-9.9,19.6,5.7), 24 mm, push + slight orbit | Lin on his platform stirs the giant steaming wok (lin_stir, flipped to face the wok; hands on a 24-frame ellipse, paddle 58+-8 deg) |
| 2 | 54-81 | preset `pour_close` (client-approved shot-2 set-up), slow push | Lin tips the bucket (pour 0.35->0.95); a milky stream runs into the rice-mortar trough; the bucket empties |
| 3 | 82-114 | custom medium along Lin's rice-mortar section from the site side, (-10.2,9,2.5)->(-9.5,8.6,2.45), 24 mm | cut on "ปูนก่อ" (2.64 s): Lin at the foot of the wall trowels the creamy mortar into the brick joints (16-frame strokes) |

## Client / QA rules
- **Sharp, no DOF:** DOF is switched off at build and before every render. Laplacian variance on full frames: min 255, median 428. Steam billows are the set's hard-edged cartoon ones.
- **Wide/medium, dense, lit set:** the frames show the wok with its fire mouth, the scaffolded rice-mortar wall, the trough, jars and brick stacks. No close-ups and no text signs.
- **Heads above y 880:** Lin's head centre sits at y 535-592 (0.42-0.46 H) and the head bottom never goes below 880. Head widths: 88-105 px (shot 1), 164-189 px (2a), 172-205 px (2b).
- **Grounded:** Lin has a cast contact shadow (stage proxy shadow) on the platform at z 1.5, at the trough and at the wall foot.
- **Mouths:** there is no quote in shots 1-2, so the mouths are static `determined` expressions (no lip-sync). Blinks are at g 22, 47, 70 and 100.
- **Motion:** the only pops are the planned cuts 53->54 and 81->82. There are 0 near-still transitions (median change 4.6 levels).
- **Frame checks:** no black, magenta or blank frames, and no retried frames.

## Colour (hue_report, final frames)
```
s01 shot 1 (g 0-53)            red 22.3 orange 60.8 yellow 5.3 green 0.8 blue 5.6 violet 2.4 magenta 2.7  sat 0.39 val 0.62
s01 shot 2a pour (g 54-81)     red 22.9 orange 54.5 yellow 1.8 green 0.7 blue 9.2 violet 3.6 magenta 7.2  sat 0.41 val 0.50
s01 shot 2b trowel (g 82-108)  red 23.2 orange 63.3 yellow 2.2 green 3.3 blue 5.9 violet 0.7 magenta 1.4  sat 0.44 val 0.58
```
The frames are warm and orange-dominant, as the set's DAY preset measures (wall_API section 5), with the blue only in the shade. hue_report flags them "OUT" against ref A's whole-clip averages: the DAY light is warm by design.

## Seconds per frame
19.65 s wall / 36.7 s CPU mean (2 threads, two processes at once on 4 cores).

## Differences from the plan / known issues
- Shot 2 is split by an internal cut at g 82: the pour on the approved `pour_close` camera, then the trowelling at the wall foot. This avoids a prop pop (bucket -> trowel) inside one set-up and gives a framing change at ~0.9 s / 1.1 s.
- The set's own paddle is merged into the cauldron mesh. Lin's sprite paddle overlaps it on the same line, so it reads as one paddle; at some phases of the stir, a second shaft end is visible near his hands.
- Shot 1 runs the steam at 0.75 (instead of 1.0) so the plume at frame left does not swallow Lin and the wok.
- In 2b the trowel is small on screen (scale 1.8, ~60 px with its mortar dollop) and sits just in front of the low course rather than inside a joint, because the card must stay in front of the wall face.
