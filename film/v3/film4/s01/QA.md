# s01 QA: film 4, shots 1-5 (the opening), pagoda set v2, DAY  (re-render 3: runner fix)

Delivered: `frames/g_0000.png .. g_0262.png` (263 frames, 720x1280, 12 samples, 2 threads, one render process, no captions, no audio).
g 0..255 = shots 1-5 ([g0, g1) = [0, 256)); g 256..262 = 7-frame out-handle (shot 5's camera keeps moving, rendered in 3D) for a 10-frame dissolve into shot 6.
Also: `meta.json` (first_g 0, n_frames 263, transitions, dof per shot), `cues.json` (15 cues, film seconds), `contact.jpg` (16 frames, labels above the picture),
`compare.jpg` (per shot one final frame beside its ref a frame, same size). Scripts: `shot.py`, `deliver.py`, `qa.py` (-> `work/qa2.txt`), `qa_cam.py`, `sheet.py`.
Raw renders + per-frame json in `raw/s1..s5` (shot 4 to g 191, shot 5 from g 178 = dissolve handles). Drafts of this pass: `work/e1`, `work/e1a.jpg`.

## Re-render 3 (runner fix, pagoda_REVIEW2.md section 5)
Set only: the red runner is now centred, 1.95 D wide, drapes over each step, wider inside the ground storey and along the street / gate;
carpet ring borders changed. Nothing in shot.py changed (same cameras, DOF, keys, 12 samples, one process, 2 threads); raw/ and frames/
fully re-rendered. Pre-check at 360x640 (`work/f1a.jpg`, g 20 and g 140): runner centred on the approach path and following the step
profile up to the platform in shot 4, runner / carpet in front of kenta in shot 1. Final log `work/final_log3.txt`: no warnings.

## Re-render 2 (director's note)
- Set: the rebuilt v2 pagoda (`G.build("DAY")`: open base, warm interior, golden dragon pillar foot, yard / street dressing, lanterns, banners).
  shot.py's `build_dressing()`, `open_ground_front()`, `warm_interior()` (and their helpers) are removed; the take adds only the shot-5 balcony.
- Depth of field per shot, as `pagoda_work/v2/s01_v2.py` (`G.setup_dof`, Z-pass blur): shot 1 focus kenta's card f 3.5; shot 2 the dragon head
  (0.2, -0.62, FOOT_Z+0.5) f 6.0; shot 3 (-3.6, -3.4, 6.0) f 7.0; shot 4 kenta's card f 6.0 (pagoda_API.md 1b text says 3.0; I used the
  director's / s01_v2.py value 6.0); shot 5 off. Checked at full size: kenta and the dragon head sharp, foreground stone / background soft.
- Narration: `film4/audio/narration_bankky.wav`, captions `film4/script/captions_bankky.json`. Sentences 0-1 kept their times, so shot bounds are
  unchanged; the word times inside moved by +1..+5 frames and the keys were moved with them:
  | event | word (new t) | old g | new g |
  |---|---|---|---|
  | point lands | "พอแผ่นดินไหว" 4.20 | 128 (arm from 126) | 129 (arm from 125, 85 % out by 129) |
  | punch-in | "ให้วิ่ง" 4.98 | 149-157 | 148-156, middle / peak speed g 152 |
  | jab into the door | "เข้ามาในนี้" 5.48 | 166 | 167 |
  | cue "Yipun" (shot 5) | "ญี่ปุ่น" 6.75 | 204 | 205 |

## Timing
| shot | g | what | ref a |
|---|---|---|---|
| 1 | 0-38 | medium: kenta beside the opened, draped ground storey, fists on the hanging chain, two pulls; eased push | t0001 |
| 2 | 39-74 (cut) | ECU raking low: golden dragon head over the bronze foot, the dark gap over the stone; push + rise | t0003 |
| 3 | 75-110 (cut) | over-the-eave: ground-storey roof corner + banner in the foreground, lantern-hung storeys rising; crane up | t0005 |
| 4 | 111-184 (cut) | medium: kenta left, opened base right with merchant / woman2 / farmer behind the drapes; point g 125-133, glance g 136-145, punch g 148-156, jab g 167 | t0007 / t0009 |
| 5 | 185-255 (10-frame dissolve g 180-189) | high wide from a balcony on the street axis: balustrade, runner up the street, gate, courtyard, pagoda + tower, mountains; slow push + tilt down | t0029-t0033 |
Framing changes g 0, 39, 75, 111, 148-156, 180-189: gaps 1.30, 1.20, 1.20, 1.23, 1.07 s, then 2.2 s of slow push.

## Camera (`qa_cam.py`, px/frame)
| shot | min | median | peak | static runs | constant-speed runs (>= 4 f) |
|---|---|---|---|---|---|
| 1 | 1.37 | 3.44 | 8.7 | none | none |
| 2 | 1.53 | 2.65 | 5.5 | none | none |
| 3 | 0.87 | 1.88 | 4.7 | none | none |
| 4 | 0.28 | 1.89 | 127 (g 152, punch) | none | g 126-132, 171-176 |
| 5 | 0.25 | 1.02 | 1.3 | none | g 204-236 (middle of the slow push) |

## Staging
| shot | head | width px | centre x | centre y (H) | head bottom below 880 |
|---|---|---|---|---|---|
| 1 | kenta | 236 -> 270 | 160-189 | 0.55-0.57 | none |
| 4 | kenta | 193 -> 304 after the punch | 241-267 | 0.54-0.56 | none |
| 4 | merchant / woman2 / farmer (doorway, soft focus) | 81-96 / 84-101 / 95-117 | 456-790 | 0.36-0.43 | none |
| 5 (wide) | kenta / merchant / woman2 / farmer, tiny | 26 / 37 / 40 / 47 | | 0.60-0.79 | merchant, woman2, farmer (wide-shot extras) |
Near/far shot 4: 304 / 96 = 3.2 after the punch. head_flip False (DAY key from screen-left in every view). Nobody's back to the camera.
Mouths: kenta's never moves (shot 1 "clench" static, shot 4 "frown" closed); townspeople closed. No pinned hands (all targets puppet-local).
Popcheck: pops only at the three hard cuts (38->39, 74->75, 110->111). Near-still: g 111->112 (shot 4 starts from rest) and 156-158 (punch settles).
No black / magenta frames, no retried frames, no clipped sprites, no warnings in `work/final_log3.txt`.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 shot 1 (g 0-38)                            45.9   25.4    0.0    0.4    0.0   11.2    7.9    9.1  0.55 0.48 0.16
s01 shot 2 (g 39-74)                            9.8   89.5    0.1    0.0    0.0    0.0    0.0    0.6  0.58 0.61 0.03
s01 shot 3 (g 75-110)                           5.1   15.1    0.0    0.0    0.0   71.9    6.3    1.6  0.59 0.58 0.06
s01 shot 4 (g 111-184)                         33.2   39.9    1.3    0.1    0.0    9.4    8.9    7.3  0.45 0.57 0.07
s01 shot 5 (g 185-262)                         29.2   11.1    0.1    1.4    0.0   54.0    1.5    2.6  0.38 0.65 0.02
s01 all (g 0-262)                              25.0   34.5    0.4    0.4    0.0   30.7    4.8    4.1  0.48 0.59 0.06
ref a t0001 t0003 t0005 t0007 t0031            27.9   43.4    5.5    0.1    0.1   14.8    2.4    5.8  0.28 0.55 0.04
```
Whole take vs band: orange 34.5, violet 4.8, magenta 4.1, val 0.59 in band; red 25 (band 30-41, ref 28), blue 30.7 (at the edge: sky in 3 and 5),
sat 0.48 (edge), dark 0.06 (band 8-15; ref 0.04). Against the v1 render red went 11 -> 25, blue 38 -> 31, violet 7 -> 5: much closer to ref a.
Shot 2 is the gold insert by design (orange 90, as ref t0003); shot 3 sky + shaded eaves (blue 72); shot 5 a sunlit exterior wide (blue 54, dark 0.02).
Shot 1 red 46 / sat 0.55 is warmer and more saturated than t0001 (drapes, carpet, bracket band). Shade reads blue-violet, never magenta.

## Seconds per frame
10.10 s wall / 20.5 s CPU mean (2 threads); re-render 2 was 9.91 / 20.1, v1 8.87 / 18.0. Per shot: 1: 12.4 / 25.0, 2: 11.5 / 23.2, 3: 7.0 / 14.3, 4: 12.6 / 25.4, 5: 7.4 / 15.2.

## Differences from the plan / the reference
- Shot 1: the chain is kenta's own `chain_up` sprite (taller canvas); its top end shows under the bracket band, not the set's pillar chain (14 D up).
  Custom eye-level camera from the south-east; behind him is the opened, draped interior with the dragon pillar (standing in for the jar), little town.
- Shot 2: the taut chain is not in frame (ECU of the foot only); the canopy's bead chains of the v2 set are out of this framing.
- Shot 3: no character; DOF f 7.0 is only a hint at this distance.
- Shot 4: custom eye-level courtyard camera (not street_eye) so the base sits right of kenta like the jar in t0007; townspeople in the doorway
  (now behind the v2 drapes, soft). kenta's point is re-aimed horizontally into the doorway, expression "determined" (closed mouth).
- Shot 5: custom balcony camera on the street axis (axial like t0031), not the set's diagonal town_wide; no figure on the balcony; the tiny
  street extras sit below y 880 (wide-shot extras).
- Transitions: plan names none; three hard cuts (insert rhythm) and one internal 10-frame dissolve 4 -> 5.
