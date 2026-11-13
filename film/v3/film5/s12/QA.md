# s12 QA: film 5, shot 12 (next day: one note, the canary droops and drops to the cage floor), mine tunnel LAMP

Delivered: `take.mkv` = `frames/g_1085.png .. g_1211.png` (127 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 1093..1203 = shot 12 ([36.42, 40.14) s -> [1093, 1204)); g 1085..1092 in-handle and g 1204..1211 out-handle (8 = 12/2 + 2), rendered in 3D.
`meta.json` (first_g 1085, n_frames 127, transition_in dissolve_or_cut), `cues.json`, `contact.jpg`, `compare.jpg` (one frame per framing beside
ref a t0041), `work/qa.txt` (numbers below). Scripts: `shot.py` (this take), `base.py` (shared engine of s12-s14, s01 structure), `deliver_lib.py`,
`deliver.py`. Drafts `work/d1..d3.jpg`.

## Client rules
- **No DOF / no blur**: `M.setup_dof(scene, None, None, cam=...)` at build and before every render (the cage_insert default never applied). No whips, no streaks.
- **Bird inside the cage**: the cage hangs on its nail (no one holds it) -> the set's 3D cage; the cast5 `canary` sprite's feet are on `A['cage']['perch']`
  = the cage centre, so the front wires cross the bird and the back wires are behind it (checked full size, every framing). For the drop the card moves
  straight down the cage axis to `A['cage']['floor']` while `lie` goes 0 -> 1, so it lands on the cage floor inside the bars.
- **Gentle bird**: eyes close as soft lash curves (`eyes` 0.85 -> 0, never X); it lies belly-down with a faint breathing pump (`breath` 0.18) after landing.

## Timing (captions.json, +0.10 s)
| framing | g | what | ref a |
|---|---|---|---|
| 12a | 1093-1131 (handle from 1085) | front three-quarter from outbye: the bird quiet and ruffled on its perch, half-lid blinks; slow push | t0041 |
| 12b | 1132-1167 (cut) | closer, inbye side: ONE note (beak opens 1142-1145, note floats up-right 1144-1167, "โน้ตเดียว" 38.04 s), then droop, eyes close softly | |
| 12c | 1168-1203 (cut, handle to 1211) | low, near the cage floor: it tips off the perch and drops g 1172-1181 (gravity ease, small settle), lies still with its eyes closed; slow push | |
Framing changes 1093, 1132, 1168: 1.30 / 1.20 / 1.20 s. Camera always moving (no run of identical frames).

## Staging (`work/qa.txt`)
| framing | bird head width px | centre y (H) |
|---|---|---|
| 12a | 176-231 | 0.43-0.46 |
| 12b | 174-209 | 0.46-0.48 |
| 12c | 143-175 | 0.37-0.53 (the drop) |
All heads above y 880. Pops only at the cuts 1131/1132, 1167/1168. No black / magenta / retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s12 12a (g 1085-1131)                           2.1   58.7    5.6    0.0    0.0   18.2   12.7    2.7  0.43 0.49 0.13
s12 12b (g 1132-1167)                           1.2   58.5    5.2    0.0    0.0   23.5    6.2    5.3  0.48 0.49 0.15
s12 12c (g 1168-1211)                           1.5   38.9    5.0    0.0    0.0   40.9   10.8    2.9  0.45 0.43 0.13
s12 all (g 1085-1211)                           1.6   52.4    5.3    0.0    0.0   27.0   10.1    3.6  0.45 0.47 0.14
```
The gold insert look (as s01 shot 2: orange 58): brass + yellow bird on the blue-shaded coal; shade blue, magenta 2.7-5.3. Red is low (no red objects).

## Seconds per frame
10.9 s wall / 21.1 s CPU mean (2 threads, denoise FAST), run beside the s13 final.

## Differences from the plan / known issues
- Lighting: one keyed warm rim lamp behind the cage (a second key lamp in front blew the brass tray out, removed). The brass tray still catches a warm
  highlight under the bird.
- The single note floats up to the right of the cage and is partly cut by the cage hoop / frame edge in 12b (it reads as a note at full size).
- No chalk tally for "next day"; the in-handle is there for a dissolve from shot 11.
