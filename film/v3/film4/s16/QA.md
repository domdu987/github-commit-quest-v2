# s16 QA: film 4, shot 16 (NIGHT wide: the rigid tower snaps and falls, dust column, no people), pagoda set v2

Delivered: `take.mkv` = `frames/g_1425.png .. g_1528.png` (104 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 1432..1521 = shot 16 ([g0, g1) = [1432, 1522)); g 1425..1431 = 7-frame in-handle (shot 16 camera before its start, 3D; the plan's
15 -> 16 is a hard cut, the handle is there in case the conform dissolves); g 1522..1528 = 7-frame out-handle (dust keeps rising) for a
10-frame dissolve into shot 17. Also `meta.json` (first_g 1425, n_frames 104), `cues.json` (8 cues), `contact.jpg`, `compare.jpg`
(3 final frames beside ref a t0093 / t0095 / t0097). Scripts: `shot.py`, `base4.py` (shared, same file in s13 / s14), `deliver.py`.

## Timing (narration_bankky.wav at +0.10 s)
| part | g | what |
|---|---|---|
| A | 1425-1466 | camera in the east courtyard (21.6, -30.2, 3.0) -> (13, -3, 12): pagoda left (swaying, amp 1.15 at 1.1 Hz), tower centre in front of the moon; slow push; quake 1.0, shake 0.55 deg. Tower joint: crack 2 + both plaster patches, splits open (crack 3) at g 1452; collapse u 0 -> 0.15 over g 1440-1474 (joint opens, top leans, puffs at the break) |
| B | 1466-1472 snap | punch-in toward the break, just before "หักกลางลำ" (49.11 s = g 1476); the top half topples (u 0.15 -> 0.62, g 1474-1494) and falls toward the camera, hits the courtyard at g 1500 (u 0.8), impact shake 1.85 deg |
| C | 1498-1506 snap | pull back and tilt up with the dust column (u 0.8 -> 1.0 at g 1528): rubble pile, flying timbers, dust column from the pile up past the moon to the frame top (ref t0095 / t0097) |
Framing changes g 1432 (cut in), 1466-1472, 1498-1506: gaps 1.13, 0.87 s, then 0.73 s of tilt to the shot end (+ handle).

## Motion / popcheck
No cuts inside. Change spikes at g 1456->1457 (7.5, crack + shake) and 1477->1478 (10.2, the top half starts to fall + snap move);
median frame change 7.2 levels (hard quake shake all through); no near-still frames, no static runs. No black / magenta frames, no retried
frames, no warnings in `work/final_log.txt`. No actors.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s16 shot 16 (g 1425-1528)                       0.5    0.0    0.0    0.0    0.0   99.0    0.3    0.1  0.72 0.54 0.02
ref a t0093 t0095 t0097                        10.1   74.3   13.1    1.2    0.0    0.1    0.1    1.0  0.41 0.78 0.00
```
The plan sets this shot at NIGHT; the reference second it copies (t0093-t0097) is a golden morning, hence the opposite hue make-up.
Moonlit blue like the reference's other night shots (t0067-t0091: blue 85); saturation 0.72 is above the reference night (0.54).
Shade blue, never magenta.

## Seconds per frame
5.97 s wall / 11.2 s CPU mean (2 threads).

## Differences from the plan / the reference
- Camera: not the set's `two_buildings` (its framing put the tower's falling top over the whole frame and cut the dust column) but a
  custom wide from the east courtyard, so pagoda, tower, moon and the full dust column read in one portrait frame.
- The set's collapse throws the top half south, toward the camera, then the dust column rises from the pile; the dust is the set's
  faceted spheres (they show their facets at full size), lit cool by the moon instead of the reference's warm smoke.
- A dark wall banner of the set shows at the upper right edge in A / C.
