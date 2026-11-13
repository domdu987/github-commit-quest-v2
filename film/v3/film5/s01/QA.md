# s01 QA: film 5, shots 1-4 (the opening), mine set (tunnel LAMP + pithead DUSK)

Delivered: `frames/g_0000.png .. g_0321.png` (322 frames, 720x1280, 12 samples, 2 threads, one render process, no captions, no audio).
g 0..314 = shots 1-4 ([g0, g1) = [0, 315)); g 315..321 = 7-frame out-handle (4d camera keeps moving, rendered in 3D).
Also `meta.json` (first_g 0, n_frames 322, transitions, shot ranges incl. 4a-4d), `cues.json` (19 cues, film seconds), `contact.jpg` (16 frames,
labels above the picture), `compare.jpg` (one final frame per shot beside its ref a frame). Scripts: `shot.py`, `deliver.py`, `qa.py` (-> `work/qa.txt`),
`sheet.py`. Raw renders + per-frame json in `raw/s1..s7` (s4 = 4a to g 213, s5 = 4b from g 198 for the dissolve). Drafts: `work/d1..d8.jpg`, `work/f1.jpg`, `work/f2.jpg`.

## Client note applied (director, mid-task)
- **No depth of field anywhere**: `M.setup_dof(scene, None, None)` at build and again before every render (cage_insert / lamp_insert defaults never applied). No motion-streak blur (no whips in this take; the shot-3 punch-in is a plain 8-frame camera move).
- Denoiser: OIDN albedo+normal. ACCURATE prefilter tested against FAST on shot 1 and shot 2 at 720x1280 (`work/pf/crops.png`): no visible difference on the coal / timber texture or the canary outline, +12 CPU s per frame -> FAST kept. Without the denoiser 12 samples are visibly grainy (`s1_noden_12`), so it stays on.
- The canary insert is crisp by framing (bird head 179 -> 282 px, the whole bird ~45 % of the frame width) and lighting (keyed warm rim lamp behind the cage + key lamp), not by blur.

## Timing (captions.json, narration at +0.10 s)
| shot | g | what | ref a |
|---|---|---|---|
| 1 | 0-41 | medium, eye level: alfie (screen-left) lifts the 3D brass cage from his hip to beside his face (g 0-14, eased), the canary sings on its perch (3 notes); miner1 with a flame lamp, miner2 digging, miner3 far; slow push | t0001 |
| 2 | 42-80 (cut) | ECU of the canary singing, 5 notes floating up, cage wires behind it, hanging lamp warm above, alfie's cap/face soft-edge in the left background; orbit + push, tilt with the notes | t0003 |
| 3 | 81-156 (cut) | low angle looking outbye: tub "37" foreground left, alfie holding the cage up on screen-left, the bright pit bottom (exit) screen-right; point at the bird lands g 86 ("ถ้าเสียงมัน"), punch-in g 119-127 (middle g 123 = plan t 4.0), point flung at the exit lands g 135 ("ให้วิ่งทันที" 4.41 s), turns to camera g 141-147 | t0007 / t0009 |
| 4a | 157-205 (cut) | pithead DUSK high establishing: chimney + smoke, engine house, headframe + wheels, heaps, terraces, first-aid hut lit; crane down + push toward the bank | t0029-t0033 |
| 4b | 206-250 (12-f dissolve g 200-211) | tunnel eye level, faint gas haze (set_gas 2.0) in the depth, slow push inbye | |
| 4c | 251-287 (cut) | the hanging lamp (y 13.75) in the haze (2.4), drifting layers | |
| 4d | 288-314 + handle 315-321 (cut) | low under the roof lamp of set 8, haze layers under the roof (2.4), push | |
Framing changes g 0, 42, 81, 119-127, 157, 200-211, 251, 288: gaps 1.40, 1.30, 1.27, 1.00, 1.43, 1.50, 1.23, 0.9 s.
Gas drift: the haze material's position input gets a keyed offset in my scene (y -0.9 D/s, z +-0.1 sine), so the layers slide past the lamps; the set file is untouched.

## Staging (`work/qa.txt`)
| shot | head | width px | centre x | centre y (H) |
|---|---|---|---|---|
| 1 | alfie | 245 -> 276 | 217-236 | 0.51 |
| 1 | miner1 / miner2 / miner3 | 123-131 / 90-94 / 52-54 | 599-648 / 435-442 | 0.43-0.52 |
| 1 | canary (head 0.18 D) | 41-45 | 359-377 | 0.54-0.64 |
| 2 | canary | 179 -> 282 | 291-328 | 0.47-0.55 |
| 2 | alfie (ECU background, cut by the frame) | 502-595 | 106-165 | 0.50-0.54 |
| 3 | alfie | 192 -> 251 (punch) | 284-305 | 0.45-0.47 |
| 3 | canary | 32-42 | 160-184 | 0.49 |
Near/far shot 1: 276 / 54 = 5.1. Hand on the cage ring (fist pinned 0.04 D above the ring loop, world target): 0.0 px median and max in shots 1 and 3.
Mouths: alfie's never moves (shot 1 "happy" closed smile, static; shot 3 "frown"); miners closed. Nobody's back to the camera. Heads all above y 880
except alfie in the shot-2 ECU (framed through on purpose). Bird visible in every frame of shots 1-3 (cage on alfie's hand).
Actor lamps: keyed `lamp_light` per frame: alfie's belt lamp (hip anchor), miner1's flame lamp (prop tip), shot 2 adds lamp_rim / lamp_key near the cage.
Popcheck: pops only at the cuts 41/42, 80/81, 156/157, 250/251, 287/288, plus 83->84 (2.4 levels: the fast back_out swing of the arm toward the bird, a gesture).
No black / magenta frames, no retried frames, no clipped sprites.

## Colour (`hue_report.row`, final frames)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s01 shot 1 (g 0-41)                            12.9   28.3    1.8    0.0    0.0   37.4    9.7    9.9  0.31 0.49 0.05
s01 shot 2 (g 42-80)                            3.0   57.6   15.4    0.0    0.0   19.8    2.0    2.2  0.44 0.54 0.08
s01 shot 3 (g 81-156)                          11.2    8.3    0.1    0.0    0.0   58.8   16.0    5.6  0.34 0.43 0.05
s01 shot 4a (g 157-205)                        27.9   42.4    1.5    0.0    0.0    5.7   10.5   12.0  0.36 0.55 0.03
s01 shot 4b (g 206-250)                         5.9   12.4    0.4    0.0    0.0   63.8   14.2    3.3  0.26 0.47 0.00
s01 shot 4c (g 251-287)                         6.1   35.6    6.8    0.0    0.0   45.5    4.2    1.8  0.35 0.49 0.02
s01 shot 4d (g 288-321)                         6.0   13.0    0.3    0.0    0.0   71.8    5.5    3.3  0.36 0.42 0.02
s01 all (g 0-321)                              11.4   31.2    4.5    0.0    0.0   38.3    8.8    5.7  0.34 0.48 0.04
ref a t0001 t0003 t0007 t0009 t0031            23.8   39.1    5.4    0.2    0.1   21.8    3.3    6.3  0.26 0.55 0.05
```
Underground is blue-dominant by the set's design (LAMP night look, mine_REVIEW: tunnel finals red 11 / blue 42): red 11 and blue 38 are outside the
interior band, orange 31 / magenta 5.7 / val 0.48 inside. Shot 2 is the warm gold insert (orange 58, like ref t0003). 4a is the dusk exterior
(red 28, orange 42, magenta 12: the orange-pink sky). Shade reads blue, never magenta. Dark share 0.04 (band 8-15, ref 0.05).

## Seconds per frame
12.75 s wall / 25.6 s CPU mean (2 threads, denoise FAST). Per shot CPU: 1: 27.5, 2: 28.9, 3: 24.1, 4a: 20.2, 4b: 29.6, 4c: 25.9, 4d: 25.3.
Shots 1, 2, 4b are 2.5-4.6 s over 25 (five actors + four keyed lamps in 1; 2048 px/D bird sprite in 2; gas slabs in 4b), at 12 samples (not raised).

## Differences from the plan / known issues
- Cage: the set's 3D brass cage (set_cage keyed per frame) carried by alfie's pinned fist, the canary is a cast5 `canary` sprite standing on the
  perch. In shots 1/3 the cage hangs 0.28 D behind alfie's card plane so the cage never hides his arm (in front, it hid the fist and the cage
  looked floating); it reads a little smaller than the ref's dragon in shot 1 (bird head 45 px). In shot 2 the bird card stands 0.27 D in front of
  the cage centre (just outside the front wires) so no wire crosses the bird; the camera is level with the perch so the perch dowel stays under its feet.
- Shot 1 g 0-6: the cage starts at alfie's hip next to his belt lamp; the brass catches a hot glow (bloom) for a few frames until it rises.
- Shot 2 continuity: alfie stays visible (his cap / face fill the left background) because the ring is at the frame top; no lamp bokeh (no DOF by client note).
- Shot 3: custom low camera looking outbye (not the set's tunnel_low, which looks inbye) so the exit (bright pit bottom) is on screen and the point lands on it.
- Shot 4: split 4a/4b/4c/4d for the 1.0-1.5 s rhythm; 4a uses a custom high camera (the set's pithead_wide is at 2.4 D); no actors at the pithead.
- Out-transition: 7-frame handle rendered; the conform decides cut or dissolve into shot 5.
