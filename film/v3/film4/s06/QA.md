# s06 QA: film 4, shot 6 (the master's rigid tower), pagoda set v2, DAY

Delivered: `take.mkv` = `frames/g_0249.png .. g_0360.png` (112 frames, 720x1280, 12 samples, 2 threads, no captions, no audio);
`meta.json` (first_g 249, n_frames 112, transition_in / transition_out, parts, DOF), `cues.json` (12 cues, film seconds), `contact.jpg`
(16 frames), `compare.jpg` (one final frame per part beside its ref a frame). Scripts: `shot.py`, `take_cfg.py` + `deliver.py`
(frames, meta, cues, sheets, take.mkv and the QA numbers in `work/qa.txt`). Raw renders + per-frame json in `raw/p1..p3`.

Shot 6 = [256, 354) (8.53 .. 11.81 s). In-handle g 249..255 (6A camera) for the 10-frame dissolve from s01 (mixed g 251..260;
s01's out-handle covers 256..262). Out-handle g 354..360 (6C crane continues) for the 10-frame dissolve into s07 (mixed g 349..358;
s07's in-handle covers 347..353). The handle frames in take.mkv are raw, unmixed.

## Timing
| part | g | what | ref a |
|---|---|---|---|
| 6A | 249-299 | low angle (pitch +27 deg) on the master on his tower's scaffold deck (z 9), hammering the big joint; blows g 270, 286 (mallet head pinned to the nail point on each blow); slow push + rise | t0013 / t0045 |
| 6B | 300-327 (cut) | ECU insert: iron joint plate with nails; a 3D mallet drives the long nail: out 0.42 -> 0.17 D at g 306 (plan 10.1 s), flush at g 321 ("แน่น"); push in | t0003 (insert grammar) |
| 6C | 328-360 (cut) | low wide from the courtyard ground up the rigid tower in its scaffold, the master small at the top hammering (blow g 343, "ก้อนหิน"); crane up + push | t0013 low angle, wide |
Framing changes g 256 (dissolve), 300, 328, 349-358 (dissolve out): 1.47 s, 0.93 s, 0.87 s; the camera moves in every frame.

## Staging (work/qa.txt)
| part | head | width px | centre x | centre y (H) | below 880 |
|---|---|---|---|---|---|
| 6A | master | 146 -> 172 | 335-358 | 0.45-0.47 | none |
| 6C (wide) | master | 41-45 | 364-373 | 0.42-0.47 | none |
head_flip False (DAY key from the south-west lands screen-left in both cameras). Mouth closed (frown) throughout. Nobody's back to camera.
Popcheck: pops only at the two cuts (299->300, 327->328). No near-still transitions, no black / magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report.row, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s06 part 1 (g 249-299)                          9.4   20.5    0.0    0.0    0.0   64.0    2.5    3.6  0.44 0.45 0.26
s06 part 2 (g 300-327)                          5.1   28.4    0.0    0.0    0.0   63.2    2.0    1.3  0.35 0.49 0.20
s06 part 3 (g 328-360)                          3.2    9.5    0.0    0.0    0.0   85.8    0.5    0.9  0.58 0.62 0.11
s06 all (g 249-360)                             5.8   16.8    0.0    0.0    0.0   73.9    1.5    2.0  0.45 0.51 0.20
ref a t0013 t0045 t0003 t0031                  36.8   46.0    3.4    0.1    0.1    7.4    3.1    3.2  0.39 0.56 0.07
```
Out of band: blue 74 / red 6. This shot is an exterior day sky + the tower's south face in blue-violet scaffold shadow, against reference
interiors (red throne room); shade reads blue-violet, never magenta (magenta 2.0). Part 1 is darker (dark 0.26) because the camera looks
up into the tower's shaded eaves. Accepted, not regraded (the set's grade is shared by all takes).

## Seconds per frame
10.64 s wall / 20.8 s CPU mean (2 threads; two processes). Per part: 6A 11.3 / 22.0, 6B 13.1 / 25.5, 6C 7.5 / 14.9.

## Differences from the plan / the reference
- The plan names `two_buildings low`; I used custom cameras: 6A low angle on the scaffold (authority from below, like t0013), 6C a low
  courtyard wide on the tower. The pagoda is not in shot 6 (it was in s01 shot 5 just before).
- The tower had no scaffold in the set: shot.py builds one at runtime (poles, ledgers, two plank decks, rails, rope lashings, a nail box).
- The nail insert is a runtime 3D detail at G.JOINT (iron plate, 7 nail heads, the keyed hero nail, a 3D mallet on a swing pivot); the
  master's sprite mallet is used in 6A / 6C. The plate stays on the tower in later takes only if they add it themselves.
- The master's pose is master_plaster with the mallet prop (no STORY4 master hammer pose exists); his mallet wind-up is partly behind his head.
